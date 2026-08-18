from __future__ import annotations

from pathlib import Path
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

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
    monkeypatch.setenv("PRIME_NODE_ID", "node-test")
    monkeypatch.setenv("PRIME_NODE_TLS_CERT_FILE", str(tmp_path / "node.crt"))
    monkeypatch.setenv("PRIME_NODE_TLS_KEY_FILE", str(tmp_path / "node.key"))
    monkeypatch.setenv("PRIME_NODE_TLS_CA_FILE", str(tmp_path / "ca.crt"))
    public_key = tmp_path / "bootstrap-public.pem"
    from src.prime_core.node_trust import NodeTrustSettings, ensure_signing_key, issue_bootstrap
    trust = NodeTrustSettings(tmp_path / "ca.crt", tmp_path / "ca.key", tmp_path / "bootstrap-key.pem", public_key, tmp_path / "core.crt", tmp_path / "core.key", tmp_path / "credentials")
    ensure_signing_key(trust)
    credential, _ = issue_bootstrap(trust, "node-test")
    monkeypatch.setenv("PRIME_NODE_BOOTSTRAP_PUBLIC_KEY_FILE", str(public_key))
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "node-test")])).sign(key, hashes.SHA256())
    csr_pem = csr.public_bytes(serialization.Encoding.PEM).decode()
    from apps.node import main
    main.settings = main.NodeSettings()
    main.service = main.NodeService(main.settings)
    with TestClient(main.app) as client:
        enrolled = client.post("/v1/enroll", json={"credential": credential, "node_id": "node-test", "csr_pem": csr_pem})
        assert enrolled.status_code == 200
        node_id = enrolled.json()["node_id"]
        approved = client.post("/v1/enrollment/approve", json={"certificate_pem": "-----BEGIN CERTIFICATE-----\n" + ("A" * 120) + "\n-----END CERTIFICATE-----\n", "token": "node-token-012345678901234567890123456789", "metadata": {"fingerprint": "test"}})
        assert approved.status_code == 200
        token = "node-token-012345678901234567890123456789"
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
        created = client.post(
            "/v1/repositories/create",
            json={"parent_path": str(tmp_path), "repository_name": "created", "operation_id": "create-1"},
            headers=headers,
        )
        assert created.status_code == 200
        assert created.json()["canonical_path"] == str((tmp_path / "created").resolve())
        replay = client.post(
            "/v1/repositories/create",
            json={"parent_path": str(tmp_path), "repository_name": "created", "operation_id": "create-1"},
            headers=headers,
        )
        assert replay.status_code == 200
        assert replay.json()["idempotent_replay"] is True
        from src.prime_core.authority import REQUIRED_AUTHORITY_FILES
        authority_files = {relative: f"# {relative}\n" for relative in REQUIRED_AUTHORITY_FILES}
        authority = client.post(
            "/v1/repositories/authority/bootstrap",
            json={"repository_path": str(tmp_path / "created"), "files": authority_files, "operation_id": "authority-1"},
            headers=headers,
        )
        assert authority.status_code == 200
        assert authority.json()["valid"] is True
        authority_replay = client.post(
            "/v1/repositories/authority/bootstrap",
            json={"repository_path": str(tmp_path / "created"), "files": authority_files, "operation_id": "authority-1"},
            headers=headers,
        )
        assert authority_replay.json()["idempotent_replay"] is True
        goal_content = "# Goal\nPreserve a real approved project objective with validation evidence.\n"
        goal_hash = hashes.Hash(hashes.SHA256())
        goal_hash.update(goal_content.encode())
        goal = client.post(
            "/v1/repositories/goal",
            json={"repository_path": str(tmp_path / "created"), "content": goal_content, "content_hash": goal_hash.finalize().hex()},
            headers=headers,
        )
        assert goal.status_code == 200
        assert (tmp_path / "created" / ".agent" / "PROJECT_GOAL.md").read_text() == goal_content
        duplicate = client.post(
            "/v1/repositories/create",
            json={"parent_path": str(tmp_path), "repository_name": "created", "operation_id": "create-2"},
            headers=headers,
        )
        assert duplicate.status_code == 400
        outside_create = client.post(
            "/v1/repositories/create",
            json={"parent_path": str(tmp_path.parent), "repository_name": "denied", "operation_id": "create-3"},
            headers=headers,
        )
        assert outside_create.status_code == 400
        denied = client.post("/v1/files/read", json={"path": str(tmp_path / "missing")}, headers=headers)
        assert denied.status_code == 400
        rotated = client.post("/v1/credentials/rotate", headers=headers)
        assert rotated.status_code == 200
        replacement = client.post("/v1/revoke", headers={**headers, "Authorization": f"Bearer {rotated.json()['node_credential']}"})
        assert replacement.status_code == 200
        assert client.post("/v1/repositories/inspect", json={"path": str(repo)}, headers=headers).status_code == 401
        reenrollment, _ = issue_bootstrap(trust, "node-test")
        reenrolled = client.post("/v1/re-enroll", json={"credential": reenrollment, "node_id": "node-test", "csr_pem": csr_pem})
        assert reenrolled.status_code == 200
        assert reenrolled.json()["node_id"] == node_id


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
