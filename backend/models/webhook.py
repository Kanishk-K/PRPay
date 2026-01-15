from datetime import datetime

from pydantic import BaseModel, Field


class GitHubUser(BaseModel):
    id: int
    login: str
    avatar_url: str | None = None
    html_url: str | None = None


class BranchInfo(BaseModel):
    ref: str
    sha: str
    repo_full_name: str | None = Field(None, alias="repo.full_name")

    class Config:
        populate_by_name = True


class RepositoryInfo(BaseModel):
    id: int
    name: str
    full_name: str
    html_url: str
    private: bool


class PullRequestData(BaseModel):
    id: int
    number: int
    html_url: str
    state: str
    title: str
    body: str | None = None
    merged: bool | None = None
    draft: bool | None = None
    created_at: datetime
    updated_at: datetime
    closed_at: datetime | None = None
    merged_at: datetime | None = None
    user: GitHubUser
    head: BranchInfo
    base: BranchInfo
    requested_reviewers: list[GitHubUser] = Field(default_factory=list)
    additions: int | None = None
    deletions: int | None = None
    changed_files: int | None = None


class PullRequestWebhookPayload(BaseModel):
    action: str
    number: int
    pull_request: PullRequestData
    repository: RepositoryInfo
    sender: GitHubUser
    requested_reviewer: GitHubUser | None = None


class ReviewData(BaseModel):
    id: int
    user: GitHubUser
    state: str
    submitted_at: datetime | None = None
    html_url: str


class PullRequestReviewWebhookPayload(BaseModel):
    action: str
    review: ReviewData
    pull_request: PullRequestData
    repository: RepositoryInfo
    sender: GitHubUser
