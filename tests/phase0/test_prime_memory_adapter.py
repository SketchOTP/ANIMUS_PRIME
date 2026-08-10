from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.prime_memory_adapter import PrimeMemoryAdapter


def test_bank_identity_is_derived_from_project_scope() -> None:
    adapter = PrimeMemoryAdapter("http://127.0.0.1:18888", "project-a")
    assert adapter.bank_id == "prime-project-a"


def test_project_id_cannot_be_a_path() -> None:
    try:
        PrimeMemoryAdapter("http://127.0.0.1:18888", "../project-b")
    except ValueError:
        return
    raise AssertionError("path-like project ID accepted")
