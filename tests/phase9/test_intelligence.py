from __future__ import annotations

import os

import pytest


pytestmark = pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for intelligence integration")


def test_ask_is_project_scoped_and_unknown_without_evidence(monkeypatch):
    if os.getenv("PRIME_QUALIFICATION_STATE", "clean").lower() == "persistent":
        pytest.skip("FRESH_STATE_REQUIRED — unseen activity cursor requires a pristine project; preserved fresh-state evidence remains authoritative")
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.intelligence_service import IntelligenceService
    from src.prime_core.service import CoreService
    settings = Settings()
    migrate(settings)
    project = CoreService(settings).create_project("Ask Project")
    service = IntelligenceService(settings)
    unknown = service.ask(project["project_id"], "not in project")
    assert unknown["epistemic"] == "UNKNOWN"
    core = CoreService(settings)
    core.emit_event("DECISION", {"summary": "bounded"}, project["project_id"], "ask-event")
    since = service.since_last_seen(project["project_id"])
    assert len(since["events"]) == 1
    assert service.since_last_seen(project["project_id"], advance=True)["advanced"] is True
