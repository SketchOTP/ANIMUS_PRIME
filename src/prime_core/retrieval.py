from __future__ import annotations

from typing import Any, TypedDict


class RetrievalHit(TypedDict, total=False):
    """The shared, project-scoped source representation used by Search and Ask."""

    source_class: str
    source_group: str
    source_id: str
    project_id: str
    locator: str
    text: str
    excerpt: str
    source_revision: str
    content_hash: str
    freshness_state: str
    authority_class: str
    relevance: float
    historical_authority: bool
    retracted: bool


def retrieval_hit(
    *,
    source_class: str,
    source_group: str,
    source_id: str,
    project_id: str,
    locator: str | None = None,
    text: str = "",
    excerpt: str | None = None,
    source_revision: str | None = None,
    content_hash: str | None = None,
    freshness_state: str = "CURRENT",
    authority_class: str = "DERIVED",
    relevance: float | None = None,
    **extra: Any,
) -> RetrievalHit:
    hit: RetrievalHit = {
        "source_class": source_class,
        "source_group": source_group,
        "source_id": source_id,
        "project_id": project_id,
        "locator": locator or source_id,
        "text": text,
        "excerpt": excerpt if excerpt is not None else text[:600],
        "freshness_state": freshness_state,
        "authority_class": authority_class,
        "historical_authority": authority_class == "AUTHORITATIVE",
        "retracted": freshness_state in {"STALE", "RETRACTED", "DETACHED"},
    }
    if source_revision is not None:
        hit["source_revision"] = str(source_revision)
    if content_hash is not None:
        hit["content_hash"] = str(content_hash)
    if relevance is not None:
        hit["relevance"] = float(relevance)
    hit.update(extra)
    return hit
