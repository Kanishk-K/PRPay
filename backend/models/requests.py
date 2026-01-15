from pydantic import BaseModel, Field

from models.enums import ReviewStatus


class ClaimPRRequest(BaseModel):
    user_id: str = Field(..., description="GitHub user ID of the reviewer")
    pr_id: int = Field(..., description="ID of the pull request to claim")
    wallet_address: str = Field(..., description="Ethereum wallet address to receive payment")


class ClaimPRResponse(BaseModel):
    success: bool
    message: str
    review_id: int | None = None
    status: ReviewStatus | None = None
    transaction_hash: str | None = Field(None, description="Blockchain transaction hash if payment successful")
    error: str | None = Field(None, description="Error message if payment failed")


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None
