from __future__ import annotations

import json

from src.prime_core.notion_credentials import (
    KNOWN_GRANTED_PAGE,
    MYASSISTANT_REFERENCE,
    NotionCredentialRegistry,
)


def test_missing_myassistant_environment_is_reported_without_secret_material(tmp_path):
    registry = NotionCredentialRegistry(tmp_path / "credential.json", environ={})
    result = registry.import_myassistant()
    assert result.status == "SOURCE_ABSENT"
    assert result.credential_reference is None
    assert not (tmp_path / "credential.json").exists()


def test_import_is_idempotent_and_persists_only_reference_metadata(tmp_path):
    secret = "notion-secret-must-never-be-persisted"
    environ = {"NOTION_READONLY_KEY": secret}
    path = tmp_path / "credential.json"
    registry = NotionCredentialRegistry(path, environ=environ)
    first = registry.import_myassistant()
    second = registry.import_myassistant()
    assert first.status == "IMPORTED" and first.changed is True
    assert second.status == "NOOP" and second.changed is False
    stored = path.read_text(encoding="utf-8")
    assert MYASSISTANT_REFERENCE in stored
    assert secret not in stored
    assert "NOTION_READONLY_KEY" in stored
    assert registry.public_status()["known_granted_page"] == KNOWN_GRANTED_PAGE


def test_deliberate_prime_reference_is_not_overwritten(tmp_path):
    registry = NotionCredentialRegistry(tmp_path / "credential.json", environ={"NOTION_READONLY_KEY": "secret"})
    result = registry.import_myassistant(existing_reference="os-keychain/prime/notion")
    assert result.status == "CONFLICT"
    assert result.credential_reference == "os-keychain/prime/notion"
    assert registry.public_status()["credential_reference"] is None


def test_corrupt_metadata_degrades_without_trying_to_recover_secret(tmp_path):
    path = tmp_path / "credential.json"
    path.write_text("not-json", encoding="utf-8")
    registry = NotionCredentialRegistry(path, environ={})
    status = registry.public_status()
    assert status["status"] == "DEGRADED"
    assert "credential" not in json.dumps(status).lower() or "credential_reference" in json.dumps(status)
