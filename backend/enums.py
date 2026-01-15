from enum import Enum


class ReviewStatus(str, Enum):
    """Status enum for user PR reviews"""
    REQUESTED = "requested"
    CLAIMABLE = "claimable"
    CLAIMED = "claimed"
    INELIGIBLE = "ineligible"
    DONE = "done"
