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
        node_id = enrolled.json()["node_id"]
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Prime-Node-Id": node_id,
            "X-Prime-Protocol": main.settings.protocol_version,
        }
        assert client.get("/v1/status", headers=headers).json()["node_id"] == node_id
        assert client.post("/v1/heartbeat", headers={**headers, "X-Prime-Protocol": "obsolete"}).status_code == 426
        identity = client.post("/v1/repositories/inspect", json={"path": str(repo)}, headers=headers)
        assert identity.status_code == 200
        assert identity.json()["is_bare"] is False
        denied = client.post("/v1/files/read", json={"path": str(tmp_path / "missing")}, headers=headers)
        assert denied.status_code == 400
        rotated = client.post("/v1/credentials/rotate", headers=headers)
        assert rotated.status_code == 200
        replacement = client.post("/v1/revoke", headers={**headers, "Authorization": f"Bearer {rotated.json()['node_credential']}"})
        assert replacement.status_code == 200
        assert client.post("/v1/repositories/inspect", json={"path": str(repo)}, headers=headers).status_code == 401
        reenrolled = client.post("/v1/re-enroll", json={"credential": replacement.json()["re_enrollment_credential"]})
        assert reenrolled.status_code == 200
        assert reenrolled.json()["node_id"] != node_id


def test_node_runtime_requires_complete_tls_mtls_configuration(monkeypatch):
    from src.prime_node.config import NodeSettings

    monkeypatch.delenv("PRIME_NODE_TLS_CERT_FILE", raising=False)
    monkeypatch.delenv("PRIME_NODE_TLS_KEY_FILE", raising=False)
    monkeypatch.delenv("PRIME_NODE_TLS_CA_FILE", raising=False)
    monkeypatch.delenv("PRIME_NODE_ALLOW_INSECURE_HTTP", raising=False)
    settings = NodeSettings()
    try:
        settings.uvicorn_kwargs()
    except ValueError as exc:
        assert "requires TLS/mTLS" in str(exc)
    else:
        raise AssertionError("service mode must not silently start without TLS/mTLS")


def test_node_runtime_emits_mtls_uvicorn_configuration(monkeypatch, tmp_path: Path):
    from src.prime_node.config import NodeSettings

    cert, key, ca = (tmp_path / name for name in ("node.crt", "node.key", "ca.crt"))
    for path in (cert, key, ca):
        path.write_text("placeholder", encoding="utf-8")
    monkeypatch.setenv("PRIME_NODE_TLS_CERT_FILE", str(cert))
    monkeypatch.setenv("PRIME_NODE_TLS_KEY_FILE", str(key))
    monkeypatch.setenv("PRIME_NODE_TLS_CA_FILE", str(ca))
    settings = NodeSettings()
    kwargs = settings.uvicorn_kwargs()
    assert kwargs["ssl_cert_reqs"] == 2
    assert kwargs["ssl_ca_certs"] == str(ca.resolve())
