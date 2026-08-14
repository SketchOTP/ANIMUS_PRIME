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
