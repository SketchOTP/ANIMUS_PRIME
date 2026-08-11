from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from src.prime_core.evidence_validation import validate_external_locator, validate_node_locator
from src.prime_core.git_history import checkpoint_bundle_status, create_checkpoint_bundle
from src.prime_core.history_primitives import reconstruction_status


def test_reconstruction_status_is_truthful_for_exact_partial_and_unavailable():
    assert reconstruction_status({"repository": "EXACT", "evidence": "EXACT"}) == "EXACT"
    assert reconstruction_status({"repository": "EXACT", "evidence": "UNAVAILABLE"}) == "PARTIAL"
    assert reconstruction_status({"repository": "UNAVAILABLE", "evidence": "UNAVAILABLE"}) == "UNAVAILABLE"


def test_evidence_locators_reject_private_targets_and_path_escape(tmp_path: Path):
    approved = tmp_path / "approved"
    approved.mkdir()
    inside = approved / "report.pdf"
    inside.write_text("report", encoding="utf-8")
    assert validate_external_locator("https://example.com/evidence/report.pdf")
    assert not validate_external_locator("http://example.com/evidence/report.pdf")
    assert not validate_external_locator("https://127.0.0.1/evidence/report.pdf")
    assert validate_node_locator(str(inside), [str(approved)])
    assert not validate_node_locator(str(tmp_path / "outside.pdf"), [str(approved)])


def test_git_checkpoint_bundle_survives_ref_removal(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    run = lambda *args: subprocess.run(args, cwd=repo, check=True, capture_output=True, text=True)
    run("git", "init", "-q")
    run("git", "config", "user.email", "test@example.invalid")
    run("git", "config", "user.name", "Test")
    (repo / "history.txt").write_text("A\n", encoding="utf-8")
    run("git", "add", ".")
    run("git", "commit", "-qm", "A")
    checkpoint = run("git", "rev-parse", "HEAD").stdout.strip()
    (repo / "history.txt").write_text("B\n", encoding="utf-8")
    run("git", "commit", "-qam", "B")
    bundle = tmp_path / "cache" / "checkpoint.bundle"
    result = create_checkpoint_bundle(str(repo), checkpoint, str(bundle))
    assert result["commit_id"] == checkpoint
    assert checkpoint_bundle_status(str(bundle), result["content_hash"]) == "EXACT"
    run("git", "update-ref", "-d", "refs/heads/master")
    run("git", "reflog", "expire", "--expire=now", "--all")
    run("git", "gc", "--prune=now")
    assert checkpoint_bundle_status(str(bundle), result["content_hash"]) == "EXACT"
