from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from src.prime_core.git_provenance import GitProvenanceError, inspect_repository_candidate
from src.prime_core.service import CoreService
from src.prime_core.workflow_primitives import resume_plan_payload, step_resume_decision


def test_step_replay_policy_is_fail_closed():
    assert step_resume_decision("SUCCEEDED", "NON_IDEMPOTENT_EXTERNAL") == "SKIP_COMPLETED"
    assert step_resume_decision("FAILED_RETRYABLE", "IDEMPOTENT_EXTERNAL") == "RETRY"
    assert step_resume_decision("RUNNING", "NON_IDEMPOTENT_EXTERNAL") == "REPAIR_REQUIRED"
    assert step_resume_decision("RUNNING", "IDEMPOTENT_EXTERNAL") == "RETRY"


def test_resume_plan_surfaces_completed_steps_resources_and_ambiguity():
    plan = resume_plan_payload(
        {"workflow_id": "workflow-test", "status": "REPAIR_REQUIRED"},
        [
            {"step_key": "A", "step_order": 0, "status": "SUCCEEDED", "replay_policy": "PURE_OR_DB_TRANSACTION"},
            {"step_key": "B", "step_order": 1, "status": "RUNNING", "replay_policy": "NON_IDEMPOTENT_EXTERNAL"},
        ],
        [{"resource_type": "repository", "resource_key": "child", "resource_locator": "/srv/child", "status": "CREATED"}],
    )
    assert plan["completed_steps"] == ["A"]
    assert plan["current_incomplete_step"] == "B"
    assert plan["required_reconciliation"] is True
    assert plan["next_safe_action"] == "REPAIR_REQUIRED"
    assert plan["recorded_resource_refs"][0]["resource_locator"] == "/srv/child"


def test_candidate_inspection_is_non_mutating_and_requires_canonical_continuity(monkeypatch, tmp_path: Path):
    root = tmp_path / "candidate"
    root.mkdir()
    expected = "a" * 40

    def fake_git(_root: Path, *args: str, **_kwargs: object) -> str:
        if args[:2] == ("rev-parse", "--show-toplevel"):
            return f"{root}\n.git\nfalse"
        if args[:2] == ("rev-parse", "--verify"):
            return expected
        if args[:2] == ("rev-parse", "HEAD"):
            return expected
        if args[:2] == ("rev-parse", "HEAD^{tree}"):
            return "b" * 40
        if args[:2] == ("rev-parse", "--is-inside-work-tree"):
            return "true"
        if args[:1] == ("status",):
            return ""
        return "c" * 40

    class Completed:
        returncode = 0
        stdout = "worktree\n"
        stderr = ""

    monkeypatch.setattr("src.prime_core.git_provenance._git", fake_git)
    monkeypatch.setattr("src.prime_core.git_provenance.subprocess.run", lambda *args, **kwargs: Completed())
    result = inspect_repository_candidate(root, "refs/heads/main", expected)
    assert result["non_bare"] is True
    assert result["canonical_ref_commit"] == expected
    assert result["worktree_admin_health"] == "HEALTHY"
    assert not (root / ".git").exists()


def test_candidate_inspection_rejects_canonical_mismatch(monkeypatch, tmp_path: Path):
    root = tmp_path / "candidate"
    root.mkdir()
    monkeypatch.setattr(
        "src.prime_core.git_provenance._git",
        lambda _root, *args, **_kwargs: f"{root}\n.git\nfalse" if args[:2] == ("rev-parse", "--show-toplevel") else "b" * 40,
    )
    with pytest.raises(GitProvenanceError, match="unexpected commit"):
        inspect_repository_candidate(root, "refs/heads/main", "a" * 40)


def test_rebind_identity_is_project_and_repository_stable():
    refusal = CoreService._rebind_refusal("project-a", "DIRTY_REBIND_REQUIRES_VERIFIABLE_WORKTREE_CONTINUITY")
    assert refusal["project_id"] == "project-a"
    assert refusal["continuity_verdict"] == "REFUSED"
    assert refusal["refusal_reason"] == "DIRTY_REBIND_REQUIRES_VERIFIABLE_WORKTREE_CONTINUITY"


def test_rebind_and_workflow_contracts_are_exposed():
    service = Path("src/prime_core/service.py").read_text(encoding="utf-8")
    migration = Path("migrations/prime/0030_rebind_and_workflow_steps.sql").read_text(encoding="utf-8")
    main = Path("apps/core/main.py").read_text(encoding="utf-8")
    for symbol in ("inspect_repository_rebind", "confirm_repository_rebind", "start_or_get_workflow", "begin_step", "complete_step", "workflow_resume_plan"):
        assert symbol in service
    for table in ("repository_continuity_anchors", "repository_rebind_preflights", "repository_rebind_history", "workflow_steps", "workflow_resources"):
        assert f"prime_core.{table}" in migration
    assert "/v1/projects/{project_id}/repository/rebind/preflight" in main
    assert "/v1/projects/{project_id}/repository/rebind/confirm" in main
