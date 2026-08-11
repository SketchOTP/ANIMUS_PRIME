from pathlib import Path

from src.prime_node.config import NodeSettings
from src.prime_node.service import NodeService


def test_node_identity_health_roots_and_snapshot_survive_reload(tmp_path: Path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    import subprocess
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
    settings = NodeSettings(state_file=tmp_path / "state.json", allowed_roots=(tmp_path,))
    service = NodeService(settings)
    node_id, token = service.enroll(settings.bootstrap_credential)
    roots = service.set_allowed_roots([str(tmp_path)])
    assert roots == [str(tmp_path.resolve())]
    assert service.heartbeat(settings.protocol_version)["node_id"] == node_id
    assert service.repository_snapshot(str(repo))["canonical_path"] == str(repo.resolve())
    reloaded = NodeService(settings)
    assert reloaded.state["node_id"] == node_id
    assert reloaded.authenticate(token)
    assert reloaded.status()["approval_state"] == "APPROVED"


def test_node_rejects_private_bind_and_path_symlink_escape(tmp_path: Path):
    settings = NodeSettings(state_file=tmp_path / "state.json", allowed_roots=(tmp_path,))
    try:
        NodeSettings(bind_host="0.0.0.0").validate()
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
