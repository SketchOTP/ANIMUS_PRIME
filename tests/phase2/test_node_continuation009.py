from pathlib import Path
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from src.prime_node.config import NodeSettings
from src.prime_core.node_trust import NodeTrustSettings, ensure_signing_key, issue_bootstrap
from src.prime_node.service import NodeService


def node_fixture(tmp_path: Path):
    trust = NodeTrustSettings(tmp_path / "ca.crt", tmp_path / "ca.key", tmp_path / "bootstrap-key.pem", tmp_path / "bootstrap-public.pem", tmp_path / "core.crt", tmp_path / "core.key", tmp_path / "credentials")
    ensure_signing_key(trust)
    token, _ = issue_bootstrap(trust, "node-test")
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "node-test")])).sign(key, hashes.SHA256())
    settings = NodeSettings(node_id="node-test", bootstrap_public_key_file=trust.bootstrap_signing_public_key, state_file=tmp_path / "state.json", tls_cert_file=tmp_path / "node.crt", allowed_roots=(tmp_path,))
    return settings, token, csr.public_bytes(serialization.Encoding.PEM).decode()


def test_node_identity_health_roots_and_snapshot_survive_reload(tmp_path: Path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    import subprocess
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
    settings, credential, csr_pem = node_fixture(tmp_path)
    service = NodeService(settings)
    proof = service.enroll(credential, settings.node_id, csr_pem)
    assert proof["approval_state"] == "PENDING_OPERATOR_APPROVAL"
    assert service.status()["health"] == "PENDING"
    service.approve("-----BEGIN CERTIFICATE-----\n" + ("A" * 120) + "\n-----END CERTIFICATE-----\n", "node-token", {"fingerprint": "test"})
    roots = service.set_allowed_roots([str(tmp_path)])
    assert roots == [str(tmp_path.resolve())]
    assert service.heartbeat(settings.protocol_version)["node_id"] == settings.node_id
    assert service.repository_snapshot(str(repo))["canonical_path"] == str(repo.resolve())
    reloaded = NodeService(settings)
    assert reloaded.state["node_id"] == settings.node_id
    assert reloaded.authenticate("node-token")
    assert reloaded.status()["approval_state"] == "ACTIVE"


def test_node_rejects_private_bind_and_path_symlink_escape(tmp_path: Path):
    settings, _, _ = node_fixture(tmp_path)
    try:
        NodeSettings(bind_host="0.0.0.0", node_id=settings.node_id, bootstrap_public_key_file=settings.bootstrap_public_key_file).validate()
    except ValueError as exc:
        assert "private interface" in str(exc)
    else:
        raise AssertionError("public wildcard bind must fail closed")
    outside = tmp_path.parent / "outside-prime-node.txt"
    outside.write_text("secret", encoding="utf-8")
    link = tmp_path / "escape.txt"
    try:
        link.symlink_to(outside)
    except OSError:
        return
    service = NodeService(settings)
    try:
        service.safe_path(str(link))
    except PermissionError:
        pass
    else:
        raise AssertionError("symlink escape must fail closed")
