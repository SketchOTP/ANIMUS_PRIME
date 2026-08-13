from __future__ import annotations

import os

import pytest


pytestmark = pytest.mark.skipif(
    not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for product completion integration"
)


def test_required_goal_evidence_is_enforced_then_retained(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.history_service import HistoryService
    from src.prime_core.progress_service import ProgressService
    from src.prime_core.service import CoreService

    settings = Settings()
    migrate(settings)
    project = CoreService(settings).create_project("Continuation 033 evidence enforcement")
    goal = CoreService(settings).create_goal_revision(project["project_id"], "Evidence-backed goal", approve=True)
    progress = ProgressService(settings)
    review = progress.propose_baseline(
        project["project_id"],
        goal["goal_revision_id"],
        [
            {"title": "required proof", "weight": 0.8, "required": True, "acceptance_expectations": ["required evidence"]},
            {"title": "optional polish", "weight": 0.2, "required": False},
        ],
    )
    progress.approve_baseline(review["review_id"])
    results = [
        {"title": "required proof", "completion": 1.0, "confidence": 0.9},
        {"title": "optional polish", "completion": 0.0, "confidence": 0.5},
    ]
    with pytest.raises(ValueError, match="required evidence missing"):
        progress.assess(project["project_id"], goal["goal_revision_id"], results, repository_revision="rev-A")

    evidence = HistoryService(settings).record_evidence(
        project["project_id"], "UPLOAD", "local://continuation-033", b"qualified evidence", source_revision="rev-A"
    )
    assessment = progress.assess(
        project["project_id"],
        goal["goal_revision_id"],
        results,
        repository_revision="rev-A",
        summary="Required evidence is attached.",
        evidence_refs=[evidence["source_reference_id"]],
    )
    assert assessment["progress_percent"] == pytest.approx(80.0)
    assert assessment["evidence_refs"] == [evidence["source_reference_id"]]
