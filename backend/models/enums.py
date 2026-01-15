from enum import StrEnum


class ReviewStatus(StrEnum):
    REQUESTED = "requested"
    APPROVED = "approved"
    CLAIMABLE = "claimable"
    CLAIMED = "claimed"
    INELIGIBLE = "ineligible"
    DONE = "done"


class PRAction(StrEnum):
    OPENED = "opened"
    CLOSED = "closed"
    REVIEW_REQUESTED = "review_requested"


class ReviewAction(StrEnum):
    SUBMITTED = "submitted"
