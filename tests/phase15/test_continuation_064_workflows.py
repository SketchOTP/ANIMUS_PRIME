import pytest

from src.prime_core.lifecycle_service import ACTION_DESCRIPTIONS, ACTION_TARGETS, ALLOWED
from src.prime_core.service import CoreService


def test_lifecycle_actions_are_explicit_and_distinct():
    assert ACTION_TARGETS["PAUSE"] == "PAUSED"
    assert ACTION_TARGETS["RESUME"] == "ACTIVE"
    assert ACTION_TARGETS["ENTER_COMPLETION_REVIEW"] == "COMPLETION_REVIEW"
    assert ACTION_TARGETS["CANCEL_COMPLETION_REVIEW"] == "ACTIVE"
    assert ACTION_TARGETS["REMOVE"] == "REMOVED"
    assert ACTION_TARGETS["ARCHIVE"] == "ARCHIVED"
    assert ACTION_TARGETS["DELETE"] == "DELETION_PENDING"
    assert ACTION_DESCRIPTIONS["REMOVE"] != ACTION_DESCRIPTIONS["ARCHIVE"]
    assert "ACTIVE" in ALLOWED["PAUSED"]
    assert "ACTIVE" in ALLOWED["ARCHIVED"]


def test_goal_proposal_requires_frozen_interview_fields():
    with pytest.raises(ValueError, match="goal proposal is incomplete"):
        CoreService.validate_goal_content("A short goal.")


def test_goal_proposal_accepts_complete_reviewable_content():
    CoreService.validate_goal_content(
        "What: build a local operator product. Why: preserve project continuity. "
        "Target operator: one trusted engineer. Desired end state: a usable persistent system. "
        "Functional requirements: lifecycle and repository workflows. Non-functional constraints: private and local-first. "
        "Success criteria: browser and regression evidence. Validation and evidence: focused and full tests. "
        "Non-goals: deployment. Failure rules: stop on unsafe mutation."
    )
