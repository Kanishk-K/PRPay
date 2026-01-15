from datetime import datetime

from pydantic import BaseModel

from models.enums import ReviewStatus


class User(BaseModel):
    github_user_id: str
    username: str | None = None
    created_at: datetime | None = None


class PullRequest(BaseModel):
    id: int
    title: str
    body: str | None = None
    url: str
    created_at: datetime | None = None


class UserPRReview(BaseModel):
    id: int
    user_id: str
    pr_id: int
    status: ReviewStatus
    payout: float
    timestamp: datetime


class PRReviewWithDetails(BaseModel):
    pr_id: int
    pr_title: str
    pr_body: str | None
    pr_url: str
    pr_created_at: datetime
    review_id: int
    user_id: str
    status: ReviewStatus
    payout: float
    review_timestamp: datetime
