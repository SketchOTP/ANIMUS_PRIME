from __future__ import annotations

from typing import Any

from .db import connect, transaction
from .indexer import RepositoryIndexer
from .memory_service import MemoryService
from .history_service import HistoryService
from .service import _id, now


class IntelligenceService:
    def __init__(self, settings: Any, memory: MemoryService | None = None):
        self.settings = settings
        self.memory = memory or MemoryService(settings)
        self.indexer = RepositoryIndexer(type("IndexerService", (), {"settings": settings})())
        self.history = HistoryService(settings)

    def search(self, project_id: str, query: str, limit: int = 20) -> dict[str, Any]:
        repository = self.indexer.search(project_id, query, min(limit, 50))
        with connect(self.settings) as db:
            activity = [dict(row) for row in db.execute("SELECT event_id,event_type,observed_at,source_revision FROM prime_core.events WHERE project_id=%s AND event_type ILIKE %s ORDER BY observed_at DESC LIMIT %s", (project_id, f"%{query}%", min(limit, 50))).fetchall()]
            progress = [dict(row) for row in db.execute("SELECT assessment_id,progress_percent,confidence,freshness_state,created_at FROM prime_core.progress_assessments WHERE project_id=%s ORDER BY created_at DESC LIMIT 1", (project_id,)).fetchall()]
        return {"project_id": project_id, "groups": {"Repository": repository, "Activity": activity, "Progress": progress, "Memory": self.memory.recall(project_id, query, min(limit, 8)).get("results", [])}}

    def ask(self, project_id: str, question: str) -> dict[str, Any]:
        sources = self.search(project_id, question, 8)
        citations = []
        for row in sources["groups"]["Repository"]:
            citations.append({"source_class": "Repository", "path": row["relative_path"], "source_revision": row["source_revision"], "content_hash": row["content_hash"]})
        for row in sources["groups"]["Memory"]:
            citations.append({"source_class": "Memory", "memory_id": row["memory_id"], "source_revision": row.get("source_revision")})
        return {"project_id": project_id, "answer": "Evidence is available in the cited project sources." if citations else "UNKNOWN: no grounded source matched the question.", "citations": citations[:16], "epistemic": "GROUNDED" if citations else "UNKNOWN"}

    def ask_at(self, project_id: str, question: str, as_of: str) -> dict[str, Any]:
        """Build a read-only historical answer context; current search is never reused."""
        context = self.history.historical_context(project_id, as_of)
        citations = []
        for row in context["evidence"]:
            if row.get("retracted_at") is None:
                citations.append({"source_class": "Evidence", "source_reference_id": row.get("source_reference_id"), "content_hash": row.get("content_hash")})
        for row in context["progress"]:
            citations.append({"source_class": "ProgressAssessment", "assessment_id": row.get("assessment_id"), "repository_revision": row.get("repository_revision")})
        return {
            "project_id": project_id,
            "as_of": as_of,
            "reconstruction_status": context["reconstruction_status"],
            "answer": "Historical evidence is available in the cited sources." if citations else "UNKNOWN: no evidence available at the selected historical boundary.",
            "citations": citations[:16],
            "historical": True,
            "later_current_state_used": False,
            "question": question,
            "source_statuses": context["source_statuses"],
        }

    def since_last_seen(self, project_id: str, advance: bool = False) -> dict[str, Any]:
        with transaction(self.settings) as db:
            checkpoint = db.execute("SELECT last_seen_event_sequence FROM prime_core.activity_checkpoints WHERE project_id=%s", (project_id,)).fetchone()
            last = checkpoint["last_seen_event_sequence"] if checkpoint else 0
            events = [dict(row) for row in db.execute("SELECT event_id,event_type,project_sequence,observed_at,payload FROM prime_core.events WHERE project_id=%s AND COALESCE(project_sequence,0)>%s ORDER BY project_sequence", (project_id, last)).fetchall()]
            new_last = max([last, *[int(event["project_sequence"] or 0) for event in events]])
            if advance:
                db.execute("INSERT INTO prime_core.activity_checkpoints(project_id,last_seen_event_sequence,updated_at) VALUES (%s,%s,%s) ON CONFLICT (project_id) DO UPDATE SET last_seen_event_sequence=EXCLUDED.last_seen_event_sequence,updated_at=EXCLUDED.updated_at", (project_id, new_last, now()))
            return {"project_id": project_id, "events": events, "advanced_to": new_last, "advanced": advance}
