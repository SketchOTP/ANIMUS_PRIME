from __future__ import annotations

import os

import pytest


pytestmark = pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for progress integration")


def test_progress_requires_approved_baseline_and_is_explainable(monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.progress_service import ProgressService
    from src.prime_core.service import CoreService
    settings = Settings()
    migrate(settings)
    core = CoreService(settings)
    project = core.create_project("Progress Project")
    goal = core.create_goal_revision(project["project_id"], "Ship", approve=True)
    service = ProgressService(settings)
    items = [{"title": "Foundation", "weight": 0.6, "completion": 0.0, "confidence": 0.8}, {"title": "Validation", "weight": 0.4, "completion": 0.0, "confidence": 0.8}]
    review = service.propose_baseline(project["project_id"], goal["goal_revision_id"], items)
    with pytest.raises(ValueError):
        service.assess(project["project_id"], goal["goal_revision_id"], items)
    service.approve_baseline(review["review_id"])
    assessment = service.assess(project["project_id"], goal["goal_revision_id"], [{**items[0], "completion": 1.0}, {**items[1], "completion": 0.5}], summary="weighted evidence")
    assert assessment["progress_percent"] == pytest.approx(80.0)
    assert assessment["confidence"] == pytest.approx(0.8)
