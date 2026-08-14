from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any


class GitProvenanceError(ValueError):
    """The repository cannot prove the requested Git relationship."""


def _git(root: Path, *args: str, check: bool = True) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=check,
            capture_output=True,
            text=True,
            timeout=8,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise GitProvenanceError("Git provenance is unavailable") from exc
    return result.stdout.strip()


def resolve_canonical_ref(root: Path, canonical_ref: str) -> str:
    if not canonical_ref.startswith(("refs/heads/", "refs/tags/")):
        raise GitProvenanceError("canonical ref must be a fully-qualified local branch or tag ref")
    if any(part in {"", ".", ".."} for part in canonical_ref.split("/")):
        raise GitProvenanceError("canonical ref contains an invalid path component")
    return _git(root, "rev-parse", "--verify", "--end-of-options", f"{canonical_ref}^{{commit}}")


def _is_ancestor(root: Path, ancestor: str, descendant: str) -> bool:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "merge-base", "--is-ancestor", ancestor, descendant],
            check=False,
            capture_output=True,
            text=True,
            timeout=8,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GitProvenanceError("Git graph relationship is unavailable") from exc
    return result.returncode == 0


def classify_acceptance(root: Path, canonical_commit: str | None, source_commit: str | None, dirty: bool) -> str:
    if dirty:
        return "WORKTREE_UNCOMMITTED"
    if not canonical_commit or not source_commit:
        return "UNKNOWN"
    try:
        _git(root, "cat-file", "-e", f"{canonical_commit}^{{commit}}")
        _git(root, "cat-file", "-e", f"{source_commit}^{{commit}}")
    except GitProvenanceError:
        return "UNKNOWN"
    if source_commit == canonical_commit:
        return "CANONICAL_HEAD"
    if _is_ancestor(root, source_commit, canonical_commit):
        return "ACCEPTED_IN_CANONICAL_HISTORY"
    if _is_ancestor(root, canonical_commit, source_commit):
        return "EXPERIMENTAL_UNMERGED"
    return "DIVERGED"


def inspect_git_state(root: Path, canonical_ref: str | None = None, canonical_commit: str | None = None) -> dict[str, Any]:
    root = root.resolve(strict=True)
    active_commit = _git(root, "rev-parse", "HEAD", check=False) or "UNBORN"
    active_ref = _git(root, "symbolic-ref", "--quiet", "--short", "HEAD", check=False) or "DETACHED"
    dirty_text = _git(root, "status", "--porcelain=v1", "--untracked-files=all", check=False)
    dirty = bool(dirty_text and dirty_text not in {"UNKNOWN", "UNAVAILABLE"})
    if canonical_ref and not canonical_commit:
        try:
            canonical_commit = resolve_canonical_ref(root, canonical_ref)
        except GitProvenanceError:
            canonical_commit = None
    worktree_path = str(root)
    common_dir = _git(root, "rev-parse", "--git-common-dir")
    common_path = Path(common_dir)
    if not common_path.is_absolute():
        common_path = (root / common_path).resolve()
    return {
        "status": "AVAILABLE",
        "repository_path": worktree_path,
        "worktree_path": worktree_path,
        "worktree_identity": str(common_path),
        "active_ref": active_ref,
        "branch": active_ref,
        "active_commit": active_commit,
        "canonical_ref": canonical_ref or "UNKNOWN",
        "canonical_commit": canonical_commit or "UNKNOWN",
        "canonical_revision": canonical_commit or active_commit,
        "dirty": dirty,
        "acceptance_classification": classify_acceptance(root, canonical_commit, active_commit, dirty),
    }


def capture_provenance(settings: Any, project_id: str, source_revision: str | None) -> dict[str, Any]:
    from .db import connect

    with connect(settings) as db:
        binding = db.execute(
            "SELECT r.canonical_path,b.canonical_ref,b.canonical_ref_commit "
            "FROM prime_core.project_bindings b JOIN prime_core.repositories r "
            "ON r.repository_id=b.repository_id WHERE b.project_id=%s",
            (project_id,),
        ).fetchone()
    base = {
        "project_id": project_id,
        "source_revision": source_revision,
        "canonical_ref": "UNKNOWN",
        "canonical_commit": "UNKNOWN",
        "active_ref": "UNKNOWN",
        "active_commit": "UNKNOWN",
        "dirty": None,
        "worktree_path": "UNKNOWN",
        "worktree_identity": "UNKNOWN",
        "acceptance_at_capture": "UNKNOWN",
        "current_acceptance_overlay": "UNKNOWN",
    }
    if not binding:
        return base
    try:
        state = inspect_git_state(Path(binding["canonical_path"]), binding["canonical_ref"], binding["canonical_ref_commit"])
    except (OSError, GitProvenanceError):
        return {**base, "canonical_ref": binding["canonical_ref"] or "UNKNOWN", "canonical_commit": binding["canonical_ref_commit"] or "UNKNOWN"}
    acceptance = classify_acceptance(Path(binding["canonical_path"]), state.get("canonical_commit"), source_revision, bool(state.get("dirty")))
    return {
        **base,
        "canonical_ref": state["canonical_ref"],
        "canonical_commit": state["canonical_commit"],
        "active_ref": state["active_ref"],
        "active_commit": state["active_commit"],
        "dirty": state["dirty"],
        "worktree_path": state["worktree_path"],
        "worktree_identity": state["worktree_identity"],
        "acceptance_at_capture": acceptance,
        "current_acceptance_overlay": acceptance,
    }
