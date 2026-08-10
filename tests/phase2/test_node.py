from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient


def test_node_enrollment_path_boundary_and_git_identity(tmp_path: Path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("secret", encoding="utf-8")
    import subprocess
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
    monkeypatch.setenv("PRIME_NODE_ALLOWED_ROOTS", str(tmp_path))
    monkeypatch.setenv("PRIME_NODE_STATE_FILE", str(tmp_path / "node-state.json"))
    from apps.node import main
    main.settings = main.NodeSettings()
    main.service = main.NodeService(main.settings)
    with TestClient(main.app) as client:
        enrolled = client.post("/v1/enroll", json={"credential": main.settings.bootstrap_credential})
        assert enrolled.status_code == 200
        token = enrolled.json()["node_credential"]
        headers = {"Authorization": f"Bearer {token}"}
        identity = client.post("/v1/repositories/inspect", json={"path": str(repo)}, headers=headers)
        assert identity.status_code == 200
        assert identity.json()["is_bare"] is False
        denied = client.post("/v1/files/read", json={"path": str(tmp_path / "missing")}, headers=headers)
        assert denied.status_code == 400
        assert client.post("/v1/revoke", headers=headers).status_code == 200
        assert client.post("/v1/repositories/inspect", json={"path": str(repo)}, headers=headers).status_code == 401
