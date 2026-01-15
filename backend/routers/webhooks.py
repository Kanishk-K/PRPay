import logging

from fastapi import APIRouter

from db import get_db
from models.enums import PRAction, ReviewAction
from models.webhook import PullRequestWebhookPayload, PullRequestReviewWebhookPayload
from services import webhook_handler

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/github/pull-request")
async def handle_github_pr_webhook(payload: PullRequestWebhookPayload):
    try:
        action = PRAction(payload.action)
    except ValueError:
        logger.debug("Ignoring action: %s", payload.action)
        return {"status": "ignored", "action": payload.action}

    db = get_db()
    pr = payload.pull_request

    match action:
        case PRAction.OPENED:
            webhook_handler.handle_pr_opened(db, payload)

        case PRAction.CLOSED:
            webhook_handler.handle_pr_closed(db, payload)

        case PRAction.REVIEW_REQUESTED:
            webhook_handler.handle_review_requested(db, payload)

    return {"status": "processed", "action": action, "pr_number": pr.number}


@router.post("/github/pull-request-review")
async def handle_github_pr_review_webhook(payload: PullRequestReviewWebhookPayload):
    try:
        action = ReviewAction(payload.action)
    except ValueError:
        logger.debug("Ignoring review action: %s", payload.action)
        return {"status": "ignored", "action": payload.action}

    db = get_db()
    pr = payload.pull_request

    match action:
        case ReviewAction.SUBMITTED:
            webhook_handler.handle_review_submitted(db, payload)

    return {"status": "processed", "action": action, "pr_number": pr.number}
