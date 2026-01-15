import logging
from typing import Any, cast

from supabase import Client

from models.enums import ReviewStatus
from models.webhook import PullRequestWebhookPayload, GitHubUser

logger = logging.getLogger(__name__)


def upsert_user(db: Client, user: GitHubUser) -> None:
    """Upsert a GitHub user into the users table."""
    db.table("users").upsert(
        {"github_user_id": str(user.id), "username": user.login},
        on_conflict="github_user_id",
    ).execute()


def upsert_pull_request(db: Client, payload: PullRequestWebhookPayload) -> int:
    """
    Upsert a pull request into the pull_requests table.
    Returns the PR's database ID.
    """
    pr = payload.pull_request
    result = db.table("pull_requests").upsert(
        {
            "title": pr.title,
            "body": pr.body,
            "url": pr.html_url,
        },
        on_conflict="url",
    ).execute()

    data = cast(list[dict[str, Any]], result.data or [])
    if data:
        return int(data[0]["id"])

    # If upsert didn't return data, fetch by URL
    fetch_result = db.table("pull_requests").select("id").eq("url", pr.html_url).execute()
    fetch_data = cast(list[dict[str, Any]], fetch_result.data or [])
    return int(fetch_data[0]["id"])


def handle_pr_opened(db: Client, payload: PullRequestWebhookPayload) -> None:
    """Handle PR opened: upsert author and PR."""
    pr = payload.pull_request
    upsert_user(db, pr.user)
    upsert_pull_request(db, payload)
    logger.info("PR #%d opened by %s", pr.number, pr.user.login)


def handle_pr_closed(db: Client, payload: PullRequestWebhookPayload) -> None:
    """
    Handle PR closed: update review statuses.
    - merged=True → status=claimable
    - merged=False → status=ineligible
    """
    pr = payload.pull_request
    pr_url = pr.html_url

    # Get PR ID from database
    pr_result = db.table("pull_requests").select("id").eq("url", pr_url).execute()
    pr_data = cast(list[dict[str, Any]], pr_result.data or [])
    if not pr_data:
        logger.warning("PR not found in database: %s", pr_url)
        return

    pr_id = pr_data[0]["id"]
    new_status = ReviewStatus.CLAIMABLE if pr.merged else ReviewStatus.INELIGIBLE

    db.table("user_pr_reviews").update({"status": new_status.value}).eq("pr_id", pr_id).eq(
        "status", ReviewStatus.REQUESTED.value
    ).execute()

    action = "merged" if pr.merged else "closed"
    logger.info("PR #%d %s — reviews updated to %s", pr.number, action, new_status)


def handle_review_requested(db: Client, payload: PullRequestWebhookPayload) -> None:
    """
    Handle review requested: upsert reviewer, PR, and create review record.
    """
    pr = payload.pull_request
    reviewer = payload.requested_reviewer

    if not reviewer:
        logger.warning("No reviewer in review_requested event for PR #%d", pr.number)
        return

    # Upsert reviewer
    upsert_user(db, reviewer)

    # Upsert PR and get ID
    pr_id = upsert_pull_request(db, payload)

    # Insert review record (ignore if already exists)
    db.table("user_pr_reviews").upsert(
        {
            "user_id": str(reviewer.id),
            "pr_id": pr_id,
            "status": ReviewStatus.REQUESTED.value,
            "payout": 0.00,
        },
        on_conflict="user_id,pr_id",
    ).execute()

    logger.info(
        "Review requested: %s for PR #%d",
        reviewer.login,
        pr.number,
    )
