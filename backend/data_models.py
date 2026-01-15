from datetime import datetime
from pydantic import BaseModel
from enums import ReviewStatus


class User(BaseModel):
    """User model representing a GitHub user"""
    github_user_id: str
    username: str | None = None
    created_at: datetime


class PullRequest(BaseModel):
    """Pull Request model"""
    id: int
    title: str
    body: str | None = None
    url: str
    created_at: datetime


class UserPRReview(BaseModel):
    """User PR Review model (M2M relationship)"""
    id: int
    user_id: str
    pr_id: int
    status: ReviewStatus
    payout: float
    timestamp: datetime


class PRReviewWithDetails(BaseModel):
    """Combined model with PR details and review information"""
    # PR fields
    pr_id: int
    pr_title: str
    pr_body: str | None
    pr_url: str
    pr_created_at: datetime

    # Review fields
    review_id: int
    user_id: str
    status: ReviewStatus
    payout: float
    review_timestamp: datetime
