from __future__ import annotations

import os
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.prime_core.authority import provision_authority, validate_authority


def test_authority_provision_is_explicit_and_complete(tmp_path: Path):
    template = Path("authority-template/v1").resolve()
    target = tmp_path / "project"
    result = provision_authority(template, target)
    assert result["valid"] is True
    assert validate_authority(target)["files"]
    with pytest.raises(FileExistsError):
        provision_authority(template, target)


pytestmark = pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for Core onboarding integration")


def test_onboarding_binding_and_approved_goal(monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from apps.core import main
    main.settings = main.Settings()
    main.service = main.CoreService(main.settings)
    with TestClient(main.app) as client:
        client.post("/v1/auth/login", json={"password": "new phase1 password"})
        csrf = client.cookies.get("prime_csrf")
        headers = {"X-PRIME-CSRF": csrf}
        project = client.post("/v1/projects", json={"name": "Onboarding Project"}, headers=headers).json()
        node_id = "node-phase3-" + uuid.uuid4().hex
        node = client.post("/v1/nodes", json={"node_id": node_id, "name": "Local", "platform": "linux", "identity_fingerprint": uuid.uuid4().hex + uuid.uuid4().hex}, headers=headers)
        assert node.status_code == 200
        binding = client.post("/v1/repositories/bind", json={"project_id": project["project_id"], "node_id": node_id, "identity_fingerprint": uuid.uuid4().hex + uuid.uuid4().hex, "canonical_path": "/srv/repo"}, headers=headers)
        assert binding.status_code == 200
        goal = client.post(f"/v1/projects/{project['project_id']}/goal", json={"content": "Ship the approved goal", "approve": True}, headers=headers)
        assert goal.status_code == 200
        assert goal.json()["status"] == "APPROVED"
