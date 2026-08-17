from __future__ import annotations

import pytest


def test_retrieval_hit_preserves_project_identity_and_freshness():
    from src.prime_core.retrieval import retrieval_hit

    hit = retrieval_hit(
        source_class="Repository",
        source_group="Repository",
        source_id="src/example.py",
        project_id="project-a",
        locator="src/example.py",
        text="current evidence",
        source_revision="abc123",
        content_hash="hash",
        relevance=0.8,
    )

    assert hit["project_id"] == "project-a"
    assert hit["source_revision"] == "abc123"
    assert hit["content_hash"] == "hash"
    assert hit["freshness_state"] == "CURRENT"
    assert hit["retracted"] is False


def test_grounded_ask_categories_require_citations():
    from src.prime_core.ai_service import AIInputError, _validate_output

    with pytest.raises(AIInputError, match="requires at least one citation"):
        _validate_output("ASK_PRIME", {"category": "SOURCE FACT", "answer": "fact", "citations": []}, {"source-1"})

    valid = _validate_output(
        "ASK_PRIME",
        {"category": "DERIVED INTERPRETATION", "answer": "derived", "citations": [{"source_id": "source-1"}]},
        {"source-1"},
    )
    assert valid["category"] == "DERIVED INTERPRETATION"


def test_unknown_ask_remains_citation_optional_and_fail_closed():
    from src.prime_core.ai_service import _validate_output

    result = _validate_output("ASK_PRIME", {"category": "UNKNOWN", "answer": "unsafe", "citations": []}, set())
    assert result["answer"] == "UNKNOWN: available evidence does not support this claim."
