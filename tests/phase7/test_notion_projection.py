from __future__ import annotations

import os

import pytest


pytestmark = pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for Notion projection integration")


def test_projection_preserves_user_content_and_degrades_safely(monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.notion_service import NotionProjectionService, START, END
    from src.prime_core.service import CoreService
    settings = Settings()
    migrate(settings)
    project = CoreService(settings).create_project("Notion Project")
    service = NotionProjectionService(settings)
    existing = f"User notes\n{START}\nold\n{END}\nMore user knowledge"
    first = service.project(project["project_id"], existing, "Current state")
    assert first["status"] == "SYNCED"
    assert "User notes" in first["content"] and "More user knowledge" in first["content"]
    second = service.project(project["project_id"], first["content"], "Current state")
    assert second["content"] == first["content"]
    assert service.project(project["project_id"], "user only", "bad")["status"] == "CONFLICT"
    assert service.project(project["project_id"], existing, "bad", available=False)["status"] == "DEGRADED"
