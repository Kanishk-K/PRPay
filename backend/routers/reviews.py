from fastapi import APIRouter, HTTPException, Query

from db import get_db
from models.enums import ReviewStatus
from models.domain import PRReviewWithDetails
from models.requests import ClaimPRRequest, ClaimPRResponse

router = APIRouter(tags=["reviews"])


@router.get(
    "/getPRs",
    response_model=list[PRReviewWithDetails],
    summary="Get PR reviews for a user",
)
def get_prs(
    user_id: str = Query(..., description="GitHub user ID of the reviewer"),
    status: ReviewStatus | None = Query(None, description="Filter by review status"),
):
    """Get all PR reviews for a specific user, with optional status filter."""
    db = get_db()

    query = (
        db.table("user_pr_reviews")
        .select(
            "id, user_id, pr_id, status, payout, timestamp, "
            "pull_requests(id, title, body, url, created_at)"
        )
        .eq("user_id", user_id)
    )

    if status:
        query = query.eq("status", status.value)

    response = query.execute()

    results = []
    for item in response.data:
        pr_data = item.get("pull_requests")
        if pr_data:
            results.append(
                {
                    "pr_id": pr_data["id"],
                    "pr_title": pr_data["title"],
                    "pr_body": pr_data["body"],
                    "pr_url": pr_data["url"],
                    "pr_created_at": pr_data["created_at"],
                    "review_id": item["id"],
                    "user_id": item["user_id"],
                    "status": item["status"],
                    "payout": float(item["payout"]),
                    "review_timestamp": item["timestamp"],
                }
            )

    return results


@router.post(
    "/claimPR",
    response_model=ClaimPRResponse,
    summary="Claim a PR review",
)
def claim_pr(request: ClaimPRRequest):
    """Claim a PR review. Only works if the review status is 'claimable'."""
    db = get_db()

    review_response = (
        db.table("user_pr_reviews")
        .select("id, status")
        .eq("user_id", request.user_id)
        .eq("pr_id", request.pr_id)
        .execute()
    )

    if not review_response.data:
        raise HTTPException(
            status_code=404,
            detail=f"No review found for user_id={request.user_id} and pr_id={request.pr_id}",
        )

    review = review_response.data[0]
    current_status = review["status"]

    if current_status != ReviewStatus.CLAIMABLE:
        return ClaimPRResponse(
            success=False,
            message=f"Cannot claim PR. Current status is '{current_status}', must be 'claimable'",
            review_id=review["id"],
            status=ReviewStatus(current_status),
        )

    db.table("user_pr_reviews").update({"status": ReviewStatus.CLAIMED}).eq(
        "user_id", request.user_id
    ).eq("pr_id", request.pr_id).execute()

    return ClaimPRResponse(
        success=True,
        message="PR successfully claimed",
        review_id=review["id"],
        status=ReviewStatus.CLAIMED,
    )
