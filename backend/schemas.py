from pydantic import BaseModel, Field
from enums import ReviewStatus


class ClaimPRRequest(BaseModel):
    """Request body for claiming a PR"""
    user_id: str = Field(..., description="GitHub user ID of the reviewer")
    pr_id: int = Field(..., description="ID of the pull request to claim")


class ClaimPRResponse(BaseModel):
    """Response for claiming a PR"""
    success: bool
    message: str
    review_id: int | None = None
    status: ReviewStatus | None = None


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: str | None = None
