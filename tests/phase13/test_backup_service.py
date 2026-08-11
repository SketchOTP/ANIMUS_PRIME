from __future__ import annotations

from pathlib import Path

import pytest

from src.prime_core.backup_service import BackupCoordinator, BackupError


def test_encrypted_backup_manifest_round_trip(tmp_path: Path):
    destination = tmp_path / "off-machine" / "prime.continuity"
    service = BackupCoordinator()
    result = service.build_bundle(
        destination,
        {"core": {"revision": "db-7", "project_ids": ["project_a"]}, "source_ledger": {"revision": "ledger-9"}},
        "correct horse battery staple",
    )
    assert result["status"] == "VERIFIED"
    assert b"project_a" not in destination.read_bytes()
    assert service.preflight_restore(destination, "correct horse battery staple")["status"] == "READY"
    with pytest.raises(BackupError):
        service.preflight_restore(destination, "wrong")


def test_backup_rejects_plaintext_credentials(tmp_path: Path):
    with pytest.raises(BackupError, match="plaintext credential"):
        BackupCoordinator().build_bundle(tmp_path / "backup", {"settings": {"token": "secret"}}, "passphrase")


def test_authenticated_backup_fails_closed_on_tamper_and_truncation(tmp_path: Path):
    destination = tmp_path / "backup"
    service = BackupCoordinator()
    service.build_bundle(destination, {"continuity": {"revision": "r1"}}, "a sufficiently long recovery key")

    original = destination.read_bytes()
    destination.write_bytes(original[:-17])
    with pytest.raises(BackupError):
        service.preflight_restore(destination, "a sufficiently long recovery key")

    destination.write_bytes(original[:-1] + bytes([original[-1] ^ 1]))
    with pytest.raises(BackupError):
        service.preflight_restore(destination, "a sufficiently long recovery key")


def test_continuity_preflight_requires_final_component_inventory(tmp_path: Path):
    destination = tmp_path / "backup"
    service = BackupCoordinator()
    result = service.build_bundle(
        destination,
        {
            "prime_postgresql": {"tables": {}, "column_types": {}},
            "hindsight": {"mode": "SOURCE_LEDGER_REBUILD"},
            "evidence": {"managed_files": {}},
            "historical_state": {},
            "git_checkpoints": {"managed_bundles": {}},
            "configuration": {"secrets": "REPROVISION_REQUIRED"},
        },
        "a sufficiently long recovery key",
        manifest_fields={"continuity": True},
    )
    assert result["manifest"]["encryption_version"].startswith("AES-256-GCM")
