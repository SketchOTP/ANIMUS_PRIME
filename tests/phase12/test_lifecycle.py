from __future__ import annotations

import os

import pytest


pytestmark = pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for lifecycle integration")


def test_lifecycle_completion_and_destructive_step_up(monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.lifecycle_service import LifecycleService
    from src.prime_core.service import CoreService
    settings = Settings()
    migrate(settings)
    project = CoreService(settings).create_project("Lifecycle Project")
    service = LifecycleService(settings, CoreService(settings))
    with pytest.raises(PermissionError):
        service.transition(project["project_id"], "DELETION_PENDING", confirmation=project["project_id"], step_up_recent=False)
    result = service.transition(project["project_id"], "DELETION_PENDING", confirmation=project["project_id"], step_up_recent=True)
    assert result["to_state"] == "DELETION_PENDING"
