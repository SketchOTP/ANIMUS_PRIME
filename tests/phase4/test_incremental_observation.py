from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from src.prime_core.indexer import RepositoryIndexer


def test_incremental_changed_paths_are_deduplicated_and_root_bounded():
    root = Path("/srv/animus-prime")
    normalized = RepositoryIndexer._normalize_changed_paths(root, ["src/main.py", "src/main.py", "docs/README.md"])
    assert [item[0] for item in normalized] == ["docs/README.md", "src/main.py"]
    for invalid in ("../outside.txt", "/etc/passwd", ".git/config", "src/../../outside.py"):
        with pytest.raises(ValueError):
            RepositoryIndexer._normalize_changed_paths(root, [invalid])


def test_incremental_revision_relation_is_fail_closed_against_invalid_revision():
    root = Path(__file__).parents[2].resolve()
    head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    assert RepositoryIndexer._revision_relation(root, head, head) == "SAME"
    with pytest.raises(ValueError, match="valid Git commit"):
        RepositoryIndexer._revision_relation(root, head, "not-a-commit")

class _Result:
    def __init__(self, row=None):
        self.row = row

    def fetchone(self):
        return self.row


class _DB:
    def __init__(self, binding):
        self.binding = binding
        self.statements = []

    def execute(self, query, params=None):
        self.statements.append((query, params))
        if "FROM prime_core.project_bindings b JOIN prime_core.repositories" in query:
            return _Result(self.binding)
        return _Result(None)


class _Transaction:
    def __init__(self, db):
        self.db = db

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc, tb):
        return False


class _Service:
    def __init__(self, db):
        self.settings = object()
        self.db = db
        self.events = []

    def emit_coalesced_event(self, *args, **kwargs):
        self.events.append((args, kwargs))
        return {"event_id": "event-test"}


def test_observe_incremental_rejects_revision_mismatch_before_projection(monkeypatch):
    root = Path(__file__).parents[2].resolve()
    head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    db = _DB({"repository_id": "repo-test", "canonical_revision": head, "canonical_path": str(root)})
    service = _Service(db)
    monkeypatch.setattr("src.prime_core.db.transaction", lambda _settings: _Transaction(db))
    with pytest.raises(ValueError, match="OBSERVATION_REVISION_MISMATCH"):
        RepositoryIndexer(service).observe_incremental("project-test", ["README.md"], "not-" + head)
    assert db.statements and len(db.statements) == 1


def test_observe_incremental_preserves_dirty_same_head_provenance(monkeypatch):
    root = Path(__file__).parents[2].resolve()
    head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    db = _DB({"repository_id": "repo-test", "canonical_revision": head, "canonical_path": str(root)})
    service = _Service(db)
    monkeypatch.setattr("src.prime_core.db.transaction", lambda _settings: _Transaction(db))
    monkeypatch.setattr(RepositoryIndexer, "_worktree_status", staticmethod(lambda _root, _relative: " M"))
    result = RepositoryIndexer(service).observe_incremental("project-test", ["README.md", "README.md"], head)
    assert result["status"] == "OBSERVED_INCREMENTALLY"
    assert result["observation_basis"] == "WORKTREE_DIRTY"
    assert result["canonical_revision"] == head
    assert result["changed_paths"] == ["README.md"]
    assert result["dirty_paths"] == ["README.md"]
    assert result["observation_revision"].startswith("WORKTREE:" + head + ":")
    assert service.events


def test_observe_incremental_retracts_missing_changed_path(monkeypatch):
    root = Path(__file__).parents[2].resolve()
    head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    db = _DB({"repository_id": "repo-test", "canonical_revision": head, "canonical_path": str(root)})
    service = _Service(db)
    monkeypatch.setattr("src.prime_core.db.transaction", lambda _settings: _Transaction(db))
    monkeypatch.setattr(RepositoryIndexer, "_worktree_status", staticmethod(lambda _root, _relative: " D"))
    result = RepositoryIndexer(service).observe_incremental("project-test", ["evidence/phase15/qualification-continuation-047-missing.md"], head)
    assert result["observation_basis"] == "WORKTREE_DIRTY"
    assert result["files_indexed"] == 0
    assert result["files_retracted"] == 1
    assert result["observation_revision"].startswith("WORKTREE:" + head + ":")
