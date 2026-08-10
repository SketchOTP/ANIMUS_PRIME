from __future__ import annotations

import os

import pytest


pytestmark = pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for reliability integration")


def test_backup_record_and_diagnostics(monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.reliability_service import ReliabilityService
    settings = Settings()
    migrate(settings)
    service = ReliabilityService(settings)
    assert service.record_backup("CORE_DB", "local://backup", "a" * 64, True)["status"] == "VERIFIED"
    service.sample("workflow_queue", "CURRENT", {"queued": 0})
    assert service.diagnostics()["health"]["database"] == "CONNECTED"
