from __future__ import annotations

import io
import tarfile
from pathlib import Path

import pytest

from src.prime_core.service import CoreService


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
