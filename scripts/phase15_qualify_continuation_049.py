"""Bounded Continuation 049 qualification against the persistent Atlas project."""

from __future__ import annotations

import hashlib
import inspect
import json
import os
import subprocess
from pathlib import Path


ROOT = Path("/home/sketch/Projects/ANIMUS_PRIME")


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True).stdout.strip()


def main() -> None:
    from apps.core import main as app
    from src.prime_core.authority import authority_migration_plan, classify_authority_snapshot
    from src.prime_core.config import Settings
    from src.prime_core.db import connect, migrate
    from src.prime_core.git_provenance import GitProvenanceError, capture_provenance, classify_acceptance, inspect_git_state, resolve_canonical_ref
    from src.prime_core.service import CoreService

    settings = Settings()
    migrate(settings)
    with connect(settings) as db:
        rows = db.execute(
            "SELECT p.project_id,p.name,r.canonical_path,b.canonical_ref,b.canonical_ref_commit "
            "FROM prime_core.projects p JOIN prime_core.project_bindings b ON b.project_id=p.project_id "
            "JOIN prime_core.repositories r ON r.repository_id=b.repository_id WHERE r.canonical_path=%s",
            (str(ROOT),),
        ).fetchall()
    assert len(rows) == 1, f"expected one persistent project binding, got {len(rows)}"
    project = dict(rows[0])
    core = CoreService(settings)
    if not project["canonical_ref"]:
        configured = core.configure_canonical_ref(project["project_id"], "refs/heads/main", confirm=True)
        project.update(canonical_ref=configured["canonical_ref"], canonical_ref_commit=configured["canonical_ref_commit"])
    assert project["canonical_ref"] == "refs/heads/main"
    canonical_commit = resolve_canonical_ref(ROOT, project["canonical_ref"])
    assert canonical_commit == project["canonical_ref_commit"]

    state = inspect_git_state(ROOT, project["canonical_ref"], project["canonical_ref_commit"])
    assert state["canonical_ref"] == "refs/heads/main"
    assert state["canonical_commit"] == canonical_commit
    assert state["active_ref"] == "main"
    assert state["active_commit"] == git("rev-parse", "HEAD")
    assert state["worktree_identity"]
    assert state["acceptance_classification"] == "WORKTREE_UNCOMMITTED"
    assert classify_acceptance(ROOT, canonical_commit, canonical_commit, False) == "CANONICAL_HEAD"
    assert classify_acceptance(ROOT, canonical_commit, git("rev-parse", "HEAD^") , False) == "ACCEPTED_IN_CANONICAL_HISTORY"
    assert classify_acceptance(ROOT, canonical_commit, "not-a-commit", False) == "UNKNOWN"
    try:
        resolve_canonical_ref(ROOT, "main")
    except GitProvenanceError:
        pass
    else:
        raise AssertionError("short branch names must not configure canonical truth")
    try:
        resolve_canonical_ref(ROOT, "refs/heads/does-not-exist")
    except GitProvenanceError:
        pass
    else:
        raise AssertionError("missing canonical refs must fail visibly")

    provenance = capture_provenance(settings, project["project_id"], canonical_commit)
    assert provenance["project_id"] == project["project_id"]
    assert provenance["canonical_ref"] == "refs/heads/main"
    assert provenance["canonical_commit"] == canonical_commit
    assert provenance["worktree_path"] == str(ROOT)
    assert provenance["worktree_identity"]
    assert provenance["acceptance_at_capture"] == "WORKTREE_UNCOMMITTED"
    assert provenance["current_acceptance_overlay"] == "WORKTREE_UNCOMMITTED"

    # Authority paths are pure, explicit, and fail closed without rewriting history.
    current_files = {relative: "current" for relative in (
        "AGENTS.md", "CLAUDE.md", "COMMANDMENTS_OF_THE_CODE.md", "GEMINI.md",
        ".agent/PROJECT_GOAL.md", ".agent/PROJECT_PROFILE.md", ".agent/CURRENT.md",
        ".agent/DIRECTIVES.md", ".agent/OUTCOMES.md", ".agent/LEARNINGS.md",
        ".agent/RECORD.md", ".agent/REPO_MAP.md",
    )}
    assert classify_authority_snapshot(current_files) == "CURRENT"
    legacy_files = {key: "Date: 2026-08-01\nObjective: historical\nExclusions: none\nLEGACY-V1" for key in current_files if key.startswith(".agent/")}
    assert classify_authority_snapshot(legacy_files) == "LEGACY"
    assert authority_migration_plan(legacy_files)["decision"] == "MIGRATE_REQUIRED"
    assert authority_migration_plan({".agent/CURRENT.md": "unknown"})["decision"] == "REVIEW_REQUIRED"
    assert authority_migration_plan(current_files)["rewrite"] == "NONE"

    # DOD-045 route matrix: all mutating management routes require session; restore adds step-up.
    route_sources = {(route.path, method): inspect.getsource(route.endpoint) for route in app.app.routes for method in getattr(route, "methods", set())}
    checked = [
        ("/v1/projects", "POST"), ("/v1/nodes", "POST"), ("/v1/repositories/bind", "POST"),
        ("/v1/projects/{project_id}/authority/bootstrap", "POST"),
        ("/v1/projects/{project_id}/progress/challenge", "POST"),
        ("/v1/backups/restore", "POST"),
    ]
    for route in checked:
        source = route_sources[route]
        assert "require_session" in source, route
    assert "step_up" in route_sources[("/v1/backups/restore", "POST")]
    assert "CONFIRM" in route_sources[("/v1/backups/restore", "POST")]
    assert "origin_allowed" in inspect.getsource(app.security_middleware)
    assert "X-PRIME-CSRF" in inspect.getsource(app.require_session)

    print(json.dumps({
        "project_id": project["project_id"],
        "canonical_ref": project["canonical_ref"],
        "canonical_commit": canonical_commit,
        "active_ref": state["active_ref"],
        "active_commit": state["active_commit"],
        "dirty": state["dirty"],
        "acceptance": state["acceptance_classification"],
        "provenance": provenance,
        "authority": {"current": "PASSED", "legacy_migrate_plan": "PASSED", "malformed_review": "PASSED"},
        "dod045_route_matrix": "PASSED",
    }, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
