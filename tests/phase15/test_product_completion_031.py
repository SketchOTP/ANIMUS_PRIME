from __future__ import annotations

import io
import tarfile
from pathlib import Path

import pytest

from src.prime_core.service import CoreService
from apps.core.main import ForkRequest


def test_fork_archive_rejects_path_traversal(tmp_path: Path) -> None:
    payload = io.BytesIO()
    with tarfile.open(fileobj=payload, mode="w") as archive:
        member = tarfile.TarInfo("../escape.txt")
        member.size = 4
        archive.addfile(member, io.BytesIO(b"nope"))
    with pytest.raises(ValueError, match="path traversal"):
        CoreService._safe_archive_extract(payload.getvalue(), tmp_path / "destination")


def test_wave3_routes_and_controls_are_present() -> None:
    main = Path("apps/core/main.py").read_text(encoding="utf-8")
    web = Path("apps/web/index.html").read_text(encoding="utf-8")
    for route in (
        "/v1/projects/{project_id}/progress/baseline",
        "/v1/projects/{project_id}/progress/assess",
        "/v1/projects/{project_id}/progress/refresh",
        "/v1/projects/{project_id}/progress/challenge",
        "/v1/projects/{project_id}/agent-chain",
        "/v1/projects/{project_id}/activity",
        "/v1/projects/{project_id}/fork",
    ):
        assert route in main
    assert "REVOKED_AND_REISSUED" in main
    assert "id=\"load-brain-wave3\"" in web
    assert "id=\"fork-form-wave3\"" in web
    assert "id=\"activity-view-wave3\"" in web
    assert "/v1/projects/{project_id}/time-lens/brain" in main
    assert "Historical Goal:" in web
    assert "renderBrainGraph(await api" in web
    assert "progress-refresh" in web
    assert "progress-challenge-form" in web


@pytest.mark.parametrize(
    "parent_path",
    [
        "/",
        "/tmp/prime-fork",
        "/home/sketch/Projects/example",
        r"C:\Projects\Example",
        r"D:\Prime\Repos\Example",
    ],
)
def test_fork_request_keeps_node_paths_opaque(parent_path: str) -> None:
    request = ForkRequest(
        source_revision="a" * 40,
        destination_node_id="atlas-node",
        parent_path=parent_path,
        repository_name="example",
        project_name="Example child",
        notion_parent_id="approved-notion-parent",
        preflight_fingerprint="f" * 64,
        confirm=True,
    )

    assert request.parent_path == parent_path
    assert request.model_dump()["parent_path"] == parent_path


def test_fork_boundary_rejects_escape_and_symlink_escape(tmp_path: Path) -> None:
    allowed = tmp_path / "allowed"
    outside = tmp_path / "outside"
    allowed.mkdir()
    outside.mkdir()
    (allowed / "child").mkdir()
    (allowed / "link").symlink_to(outside, target_is_directory=True)

    assert CoreService._within_allowed_root(allowed / "child", [str(allowed)])
    assert not CoreService._within_allowed_root(allowed / ".." / "outside", [str(allowed)])
    assert not CoreService._within_allowed_root(allowed / "link" / "child", [str(allowed)])
