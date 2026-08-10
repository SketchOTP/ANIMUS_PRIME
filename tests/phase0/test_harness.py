from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_compose_file_uses_pinned_images() -> None:
    compose = (ROOT / "docker-compose.phase0.yml").read_text()
    assert "pgvector/pgvector@sha256:e04af45eb526378554a24ed05b37d9ea56fd623feca9adf264d4f47d875c9a93" in compose
    assert "hindsight@sha256:2b92c62863a0841e2a153907462987f6d6f1d7bf9ae07a8ad3d07430eb175217" in compose


def test_phase0_script_compiles() -> None:
    subprocess.run(["python3", "-m", "py_compile", "scripts/phase0_qualify.py"], cwd=ROOT, check=True)
