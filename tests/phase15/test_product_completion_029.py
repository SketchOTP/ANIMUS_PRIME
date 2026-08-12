from __future__ import annotations

from apps.core.main import _context_markdown


def test_context_markdown_is_bounded_and_redacted() -> None:
    context = {
        "generated_at": "2026-08-12T22:00:00Z",
        "project": {"name": "Fixture A", "project_id": "project-a", "freshness_state": "CURRENT"},
        "repository": {"canonical_path": "C:/fixture-a", "node_name": "Atlas", "git": {"canonical_revision": "abc123", "branch": "main"}},
        "goal": {"revision": {"revision_number": 1, "status": "APPROVED", "content_hash": "hash", "content": "Keep the project understandable."}},
        "status": {"progress": {"progress_percent": 68, "confidence": 0.84}, "alignment": "UNKNOWN", "attention": []},
        "authority": {"latest": {"validation_status": "VALID"}},
        "memory": [{"memory_id": "memory-a"}],
        "evidence": [{"evidence_id": "evidence-a"}],
        "activity": [{"event_type": "PROGRESS_CHANGED"}],
    }
    exported = _context_markdown(context)
    assert "Fixture A" in exported
    assert "abc123" in exported
    assert "68" in exported
    assert "credentials, tokens, authorization headers, and chain of thought omitted." in exported
    assert "## PROVENANCE" in exported
    assert "Product029!Passphrase-2026" not in exported
    assert len(exported) < 8_000
