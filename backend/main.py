
import logging
from models.webhook import PRAction, PullRequestWebhookPayload
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from database import get_db
from data_models import PRReviewWithDetails
from schemas import ClaimPRRequest, ClaimPRResponse
from enums import ReviewStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/webhooks/github/pull-request")
async def handle_github_pr_webhook(payload: PullRequestWebhookPayload):
    try:
        action = PRAction(payload.action)
    except ValueError:
        logger.debug("Ignoring action: %s", payload.action)
        return {"status": "ignored", "action": payload.action}

    pr = payload.pull_request

    match action:
        case PRAction.OPENED:
            logger.info(
                "PR #%d opened: %s by %s — %s",
                pr.number,
                pr.title,
                pr.user.login,
                pr.html_url,
            )

        case PRAction.CLOSED:
            if pr.merged:
                logger.info(
                    "PR #%d merged at %s — %s",
                    pr.number,
                    pr.merged_at,
                    pr.html_url,
                )
            else:
                logger.info(
                    "PR #%d closed at %s — %s",
                    pr.number,
                    pr.closed_at,
                    pr.html_url,
                )

        case PRAction.REVIEW_REQUESTED:
            reviewer = payload.requested_reviewer
            logger.info(
                "PR #%d review requested from %s — %s",
                pr.number,
                reviewer.login if reviewer else "unknown",
                pr.html_url,
            )

    return {"status": "processed", "action": action, "pr_number": pr.number}


@app.get("/")
def read_root():
    return {
        "message": "PRPay API",
        "version": "1.0.0",
        "endpoints": {
            "GET /getPRs": "Get PR reviews for a user",
            "POST /claimPR": "Claim a PR review"
        }
    }


@app.get(
    "/getPRs",
    response_model=List[PRReviewWithDetails],
    summary="Get PR reviews for a user",
    description="Retrieve PR reviews for a specific user, optionally filtered by status"
)
def get_prs(
    user_id: str = Query(..., description="GitHub user ID of the reviewer"),
    status: Optional[ReviewStatus] = Query(None, description="Filter by review status")
):
    """
    Get all PR reviews for a specific user, with optional status filter.

    Args:
        user_id: GitHub user ID
        status: Optional status filter (requested, claimable, claimed, ineligible, done)

    Returns:
        List of PR reviews with full PR details
    """
    try:
        db = get_db()

        # Build query to join user_pr_reviews with pull_requests
        query = db.table("user_pr_reviews") \
            .select(
                "id, user_id, pr_id, status, payout, timestamp, "
                "pull_requests(id, title, body, url, created_at)"
            ) \
            .eq("user_id", user_id)

        # Add status filter if provided
        if status:
            query = query.eq("status", status.value)

        # Execute query
        response = query.execute()

        # Transform the data to match our response model
        results = []
        for item in response.data:
            pr_data = item.get("pull_requests")
            if pr_data:
                results.append({
                    "pr_id": pr_data["id"],
                    "pr_title": pr_data["title"],
                    "pr_body": pr_data["body"],
                    "pr_url": pr_data["url"],
                    "pr_created_at": pr_data["created_at"],
                    "review_id": item["id"],
                    "user_id": item["user_id"],
                    "status": item["status"],
                    "payout": float(item["payout"]),
                    "review_timestamp": item["timestamp"]
                })

        return results

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch PR reviews: {str(e)}"
        )


@app.post(
"/claimPR",
response_model=ClaimPRResponse,
summary="Claim a PR review",
description="Claim a PR review by updating its status from 'claimable' to 'claimed'"
)
def claim_pr(request: ClaimPRRequest):
    """
        Claim a PR review. Only works if the review status is 'claimable'.

        Args:
            request: ClaimPRRequest with user_id and pr_id

        Returns:
            ClaimPRResponse with success status and updated review details
    """
    try:
        db = get_db()

        # First, fetch the current review to check its status
        review_response = db.table("user_pr_reviews") \
            .select("id, status") \
            .eq("user_id", request.user_id) \
            .eq("pr_id", request.pr_id) \
            .execute()

        if not review_response.data:
            raise HTTPException(
                status_code=404,
                detail=f"No review found for user_id={request.user_id} and pr_id={request.pr_id}"
            )

        review = review_response.data[0]
        current_status = review["status"]

        # Check if status is 'claimable'
        if current_status != ReviewStatus.CLAIMABLE.value:
            return ClaimPRResponse(
                success=False,
                message=f"Cannot claim PR. Current status is '{current_status}', must be 'claimable'",
                review_id=review["id"],
                status=ReviewStatus(current_status)
            )

        # Update status to 'claimed'
        update_response = db.table("user_pr_reviews") \
            .update({"status": ReviewStatus.CLAIMED.value}) \
            .eq("user_id", request.user_id) \
            .eq("pr_id", request.pr_id) \
            .execute()

        if update_response.data:
            return ClaimPRResponse(
                success=True,
                message="PR successfully claimed",
                review_id=review["id"],
                status=ReviewStatus.CLAIMED
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to update review status"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to claim PR: {str(e)}"
        )
