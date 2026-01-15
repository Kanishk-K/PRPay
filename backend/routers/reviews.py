from typing import Any, cast
import logging

from fastapi import APIRouter, HTTPException, Query

from db import get_db
from models.enums import ReviewStatus
from models.domain import PRReviewWithDetails
from models.requests import ClaimPRRequest, ClaimPRResponse
from services.crypto_payment import get_payment_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["reviews"])


@router.get(
    "/getPRs",
    response_model=list[PRReviewWithDetails],
    summary="Get PR reviews for a user",
)
def get_prs(
    user_id: str = Query(..., description="GitHub user ID of the reviewer"),
    status: ReviewStatus | None = Query(None, description="Filter by review status"),
) -> list[dict[str, Any]]:
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
    data = cast(list[dict[str, Any]], response.data or [])

    results: list[dict[str, Any]] = []
    for item in data:
        pr_data = item.get("pull_requests")
        if isinstance(pr_data, dict):
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
def claim_pr(request: ClaimPRRequest) -> ClaimPRResponse:
    """Claim a PR review and send ETH payment on Base Sepolia. Only works if the review status is 'claimable'."""
    db = get_db()

    # Fetch the review details
    review_response = (
        db.table("user_pr_reviews")
        .select("id, status, payout")
        .eq("user_id", request.user_id)
        .eq("pr_id", request.pr_id)
        .execute()
    )

    data = cast(list[dict[str, Any]], review_response.data or [])
    if not data:
        raise HTTPException(
            status_code=404,
            detail=f"No review found for user_id={request.user_id} and pr_id={request.pr_id}",
        )

    review = data[0]
    current_status: str = review["status"]

    # Validate status is claimable
    if current_status != ReviewStatus.CLAIMABLE:
        return ClaimPRResponse(
            success=False,
            message=f"Cannot claim PR. Current status is '{current_status}', must be 'claimable'",
            review_id=review["id"],
            status=ReviewStatus(current_status),
        )

    # Validate wallet address
    try:
        payment_service = get_payment_service()
        if not payment_service.validate_address(request.wallet_address):
            return ClaimPRResponse(
                success=False,
                message="Invalid Ethereum wallet address",
                review_id=review["id"],
                status=ReviewStatus.CLAIMABLE,
                error="Invalid wallet address format"
            )
    except Exception as e:
        logger.error(f"Failed to initialize payment service: {e}")
        return ClaimPRResponse(
            success=False,
            message="Payment service unavailable",
            review_id=review["id"],
            status=ReviewStatus.CLAIMABLE,
            error=str(e)
        )

    # Execute crypto payment (fixed amount: 0.0000001 ETH)
    payment_amount = 0.0000001
    logger.info(f"Attempting to send {payment_amount} ETH to {request.wallet_address}")

    payment_result = payment_service.send_eth_payment(
        recipient_address=request.wallet_address,
        amount_eth=payment_amount
    )

    # Handle payment result
    if payment_result["success"]:
        # Payment successful - update status to claimed
        db.table("user_pr_reviews").update({"status": ReviewStatus.CLAIMED.value}).eq(
            "user_id", request.user_id
        ).eq("pr_id", request.pr_id).execute()

        return ClaimPRResponse(
            success=True,
            message=f"PR successfully claimed. {payment_amount} ETH sent to {request.wallet_address}",
            review_id=review["id"],
            status=ReviewStatus.CLAIMED,
            transaction_hash=payment_result["transaction_hash"]
        )
    else:
        # Payment failed - keep status as claimable
        logger.error(f"Payment failed: {payment_result['error']}")
        return ClaimPRResponse(
            success=False,
            message="PR claim failed due to payment error. Please try again.",
            review_id=review["id"],
            status=ReviewStatus.CLAIMABLE,
            error=payment_result["error"]
        )
