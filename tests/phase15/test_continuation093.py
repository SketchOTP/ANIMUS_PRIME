from __future__ import annotations

from pathlib import Path
import subprocess

import pytest
from pydantic import ValidationError

from apps.core.main import MemoryRequest
from src.prime_core.service import CoreService


def test_fork_contract_declares_every_child_owned_stage_and_operator_preflight():
    root = Path(__file__).parents[2]
    service = (root / "src/prime_core/service.py").read_text(encoding="utf-8")
    api = (root / "apps/core/main.py").read_text(encoding="utf-8")
    web = (root / "apps/web/index.html").read_text(encoding="utf-8")

    for step in (
        "GOAL_DRAFTED",
        "GOAL_APPROVED",
        "PROGRESS_BASELINE_CREATED",
        "NOTION_PROJECT_RECORD_BOUND",
        "MCP_SCOPE_ISSUED",
        "HINDSIGHT_BOUND",
        "PROJECT_BRAIN_INITIALIZED",
        "EVENT_STREAM_INITIALIZED",
        "FINALIZED",
    ):
        assert step in service

    assert 'remote_action not in {"CLEAR", "RETAIN_READ_ONLY", "REMAP"}' in service
    assert "disabled-by-prime://write-capability-unproven" in service
    assert "NEW_CHILD_PROJECT_RECORD" in service
    assert "NEW_CHILD_APPROVED_BASELINE" in service
    assert 'emit_event("PROJECT_FORKED"' in service
    assert '@app.post("/v1/projects/{project_id}/fork/preflight")' in api
    assert "preflight_fingerprint" in api
    assert "approve_child_goal" in api
    assert "approve_progress_baseline" in api
    assert "Review Fork preflight" in web
    assert "Child Progress baseline proposal" in web
    assert "Approved Notion parent ID" in web
    assert "Retain fetch URLs with push disabled" in web


def test_fork_browser_never_renders_one_time_mcp_secret():
    root = Path(__file__).parents[2]
    web = (root / "apps/web/index.html").read_text(encoding="utf-8")
    fork_handler = web[web.index("$('#fork-form-wave3')?.addEventListener('submit'") :]
    fork_handler = fork_handler[: fork_handler.index("$('#load-repository')")]
    assert "mcp_grant" not in fork_handler
    assert "token" not in fork_handler
    assert "Memory copy:" in fork_handler


def test_fork_preflight_is_invalidated_when_any_material_input_changes():
    root = Path(__file__).parents[2]
    web = (root / "apps/web/index.html").read_text(encoding="utf-8")
    assert "state.forkPreflight=null" in web
    assert "Fork inputs changed. Run the preflight again before creation." in web
    assert "fork preflight is stale or does not match the confirmed target" in (root / "src/prime_core/service.py").read_text(encoding="utf-8")


def test_fork_remote_display_removes_embedded_http_credentials():
    assert CoreService._display_remote_url("https://operator:secret@example.test/org/repo.git?ref=main") == "https://example.test/org/repo.git?ref=main"
    assert CoreService._display_remote_url("git@example.test:org/repo.git") == "git@example.test:org/repo.git"


def test_fork_cleanliness_rejects_tracked_changes_but_preserves_untracked_tool_state(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.email", "qualification@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.name", "Qualification"], check=True)
    tracked = tmp_path / "tracked.txt"
    tracked.write_text("committed\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "tracked.txt"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "baseline"], check=True)
    (tmp_path / ".tool-local").mkdir()
    (tmp_path / ".tool-local" / "state.json").write_text("{}\n", encoding="utf-8")
    assert CoreService._tracked_worktree_changes(tmp_path) == ""
    tracked.write_text("changed\n", encoding="utf-8")
    assert "tracked.txt" in CoreService._tracked_worktree_changes(tmp_path)


def test_fork_child_goal_wraps_legacy_approved_content_for_independent_review():
    legacy = "# Existing approved Goal\n\nBuild the frozen V1 safely.\n" * 3
    child = CoreService._fork_child_goal_draft("Qualification Child", legacy)
    CoreService.validate_goal_content(child)
    assert child.startswith("# Qualification Child Project Goal")
    assert "## Approved Parent Goal Context (verbatim)" in child
    assert legacy.rstrip() in child


def test_fork_child_goal_preserves_already_structured_content_verbatim():
    structured = """# Project Goal
What and why: preserve continuity.
Target user and operator: the operator.
Desired end state and outcome: an isolated child.
Functional requirements: retain provenance.
Constraints and non-functional requirements: remain private.
Success and acceptance: isolation is verified.
Validation and evidence: inspect durable identities.
Non-goals and out of scope: no deployment.
Failure and stop rules: stop on ambiguity.
"""
    assert CoreService._fork_child_goal_draft("Child", structured) == structured


def test_memory_api_rejects_unknown_content_class_before_database_mutation():
    with pytest.raises(ValidationError):
        MemoryRequest(content="Safe qualification observation.", content_class="QUALIFICATION_EVIDENCE")

    accepted = MemoryRequest(content="Safe qualification observation.", content_class="OBSERVATION")
    assert accepted.content_class == "OBSERVATION"
