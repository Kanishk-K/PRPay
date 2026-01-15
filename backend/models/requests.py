from pydantic import BaseModel, Field

from models.enums import ReviewStatus


class ClaimPRRequest(BaseModel):
    user_id: str = Field(..., description="GitHub user ID of the reviewer")
    pr_id: int = Field(..., description="ID of the pull request to claim")


class ClaimPRResponse(BaseModel):
    success: bool
    message: str
    review_id: int | None = None
    status: ReviewStatus | None = None


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None
