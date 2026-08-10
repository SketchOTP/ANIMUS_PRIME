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
