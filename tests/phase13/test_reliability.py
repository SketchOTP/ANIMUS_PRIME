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


def test_continuity_backup_manifest_and_schedule_controls(monkeypatch, tmp_path):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.backup_service import BackupCoordinator, BackupError
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.service import CoreService
    from src.prime_core.reliability_service import ReliabilityService

    settings = Settings()
    migrate(settings)
    project = CoreService(settings).create_project("Continuity contract")
    destination = tmp_path / "secondary" / "prime.continuity"
    result = BackupCoordinator().create_continuity_backup(
        settings, destination, "a sufficiently long recovery key", project_ids=[project["project_id"]], destination_class="operator-selected"
    )
    assert result["status"] == "VERIFIED"
    assert result["manifest"]["spec_revision"] == "PRIME-SPEC-V1.0.0"
    assert BackupCoordinator().preflight_restore(destination, "a sufficiently long recovery key")["status"] == "READY"
    with pytest.raises(BackupError):
        BackupCoordinator().preflight_restore(destination, "wrong wrong wrong")

    reliability = ReliabilityService(settings)
    schedule = reliability.configure_backup_schedule("/secondary/prime", "hourly", "operator-recovery-key")
    assert schedule["key_reference"] == "operator-recovery-key"
    assert reliability.due_backup_schedules()


def test_derived_queue_backpressure_is_active(monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    monkeypatch.setenv("PRIME_QUEUE_LIMIT", "0")
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.service import CoreService

    settings = Settings()
    migrate(settings)
    with pytest.raises(ValueError, match="backpressure"):
        CoreService(settings).create_job("REINDEX", {}, "backpressure-test")
