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


def test_mental_model_creation_uses_supported_project_bank_contract() -> None:
    adapter = PrimeMemoryAdapter("http://127.0.0.1:18888", "project-a")
    calls = []

    def fake_request(method: str, path: str, body: dict | None = None) -> dict:
        calls.append((method, path, body))
        return {"operation_id": "op-1"}

    adapter._request = fake_request  # type: ignore[method-assign]
    result = adapter.create_mental_model(
        name="ANIMUS PRIME Operating Model",
        source_query="What should future sessions preserve?",
        model_id="prime-operating-model",
    )

    assert result.status == "CURRENT"
    assert calls == [(
        "POST",
        "/v1/default/banks/prime-project-a/mental-models",
        {
            "name": "ANIMUS PRIME Operating Model",
            "source_query": "What should future sessions preserve?",
            "max_tokens": 2048,
            "trigger": {"refresh_after_consolidation": False},
            "id": "prime-operating-model",
        },
    )]


def test_mental_model_listing_is_full_detail_and_project_bound() -> None:
    adapter = PrimeMemoryAdapter("http://127.0.0.1:18888", "project-a")
    calls = []

    def fake_request(method: str, path: str, body: dict | None = None) -> dict:
        calls.append((method, path, body))
        return {"items": []}

    adapter._request = fake_request  # type: ignore[method-assign]
    result = adapter.list_mental_models()

    assert result.status == "CURRENT"
    assert calls == [(
        "GET",
        "/v1/default/banks/prime-project-a/mental-models?detail=full&limit=1000",
        None,
    )]
