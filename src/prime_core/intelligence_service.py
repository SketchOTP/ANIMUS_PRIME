from __future__ import annotations

from typing import Any
from pathlib import Path

from .db import connect, transaction
from .indexer import RepositoryIndexer
from .memory_service import MemoryService
from .history_service import HistoryService
from .ai_service import AIExecutionService
from .service import _id, now


class IntelligenceService:
    def __init__(self, settings: Any, memory: MemoryService | None = None):
        self.settings = settings
        self.memory = memory or MemoryService(settings)
        self.indexer = RepositoryIndexer(type("IndexerService", (), {"settings": settings})())
        self.history = HistoryService(settings)
        self.ai = AIExecutionService(settings)

    def search(self, project_id: str, query: str, limit: int = 20) -> dict[str, Any]:
        repository = self.indexer.search(project_id, query, min(limit, 50))
        with connect(self.settings) as db:
            activity = [dict(row) for row in db.execute("SELECT event_id,event_type,observed_at,source_revision FROM prime_core.events WHERE project_id=%s AND event_type ILIKE %s ORDER BY observed_at DESC LIMIT %s", (project_id, f"%{query}%", min(limit, 50))).fetchall()]
            progress = [dict(row) for row in db.execute("SELECT assessment_id,progress_percent,confidence,freshness_state,created_at FROM prime_core.progress_assessments WHERE project_id=%s ORDER BY created_at DESC LIMIT 1", (project_id,)).fetchall()]
        return {"project_id": project_id, "groups": {"Repository": repository, "Activity": activity, "Progress": progress, "Memory": self.memory.recall(project_id, query, min(limit, 8)).get("results", [])}}

    def ask(self, project_id: str, question: str) -> dict[str, Any]:
        sources = self.search(project_id, question, 8)
        citations = []
        model_sources = []
        repository_root = None
        memory_content: dict[str, str] = {}
        with connect(self.settings) as db:
            binding = db.execute("SELECT r.canonical_path FROM prime_core.project_bindings b JOIN prime_core.repositories r ON r.repository_id=b.repository_id WHERE b.project_id=%s", (project_id,)).fetchone()
            repository_root = Path(binding["canonical_path"]).resolve() if binding else None
            memory_ids = [row["memory_id"] for row in sources["groups"]["Memory"]]
            if memory_ids:
                memory_rows = db.execute("SELECT memory_id,content FROM prime_core.memory_records WHERE project_id=%s AND memory_id = ANY(%s)", (project_id, memory_ids)).fetchall()
                memory_content = {row["memory_id"]: row["content"] for row in memory_rows}
        for row in sources["groups"]["Repository"]:
            source_id = row["relative_path"]
            citations.append({"source_class": "Repository", "source_id": source_id, "path": source_id, "source_revision": row["source_revision"], "content_hash": row["content_hash"]})
            text = ""
            if repository_root is not None:
                candidate = (repository_root / source_id).resolve()
                try:
                    candidate.relative_to(repository_root)
                    if candidate.is_file() and candidate.stat().st_size <= 12000:
                        text = candidate.read_text(encoding="utf-8", errors="replace")
                except (OSError, ValueError):
                    text = ""
            model_sources.append({"source_class": "Repository", "source_id": source_id, "locator": source_id, "project_id": project_id, "source_revision": row["source_revision"], "content_hash": row["content_hash"], "freshness_state": row.get("freshness_state"), "text": text})
        for row in sources["groups"]["Memory"]:
            source_id = row["memory_id"]
            citations.append({"source_class": "Memory", "source_id": source_id, "memory_id": source_id, "source_revision": row.get("source_revision")})
            model_sources.append({"source_class": "Memory", "source_id": source_id, "locator": f"memory:{source_id}", "project_id": project_id, "source_revision": row.get("source_revision"), "text": memory_content.get(source_id, "")})
        model = self.ai.execute(project_id, "ASK_PRIME", {"question": question}, model_sources)
        if model["status"] == "SUCCEEDED":
            result = dict(model["result"])
            return {"project_id": project_id, **result, "epistemic": result.get("category", "UNKNOWN"), "ai_run": {key: model[key] for key in ("run_id", "provider", "model", "profile_revision", "prompt_revision", "schema_revision", "privacy_mode", "source_revision_set", "status")}}
        return {
            "project_id": project_id,
            "answer": "UNKNOWN: model execution is unavailable or the evidence does not support a safe answer.",
            "citations": citations[:16],
            "epistemic": "UNKNOWN",
            "status": model["status"],
            "error_class": model.get("error_class"),
            "ai_run": {key: model[key] for key in ("run_id", "provider", "model", "profile_revision", "prompt_revision", "schema_revision", "privacy_mode", "source_revision_set", "status")},
        }

    def ask_at(self, project_id: str, question: str, as_of: str) -> dict[str, Any]:
        """Build a read-only historical answer context; current search is never reused."""
        context = self.history.historical_context(project_id, as_of)
        citations = []
        for row in context["evidence"]:
            if row.get("retracted_at") is None:
                citations.append({"source_class": "Evidence", "source_reference_id": row.get("source_reference_id"), "content_hash": row.get("content_hash"), "source_revision": row.get("source_revision"), "historical": True})
        for row in context["progress"]:
            citations.append({"source_class": "ProgressAssessment", "assessment_id": row.get("assessment_id"), "repository_revision": row.get("repository_revision"), "historical": True})
        return {
            "project_id": project_id,
            "as_of": as_of,
            "selected_revision": context.get("selected_revision"),
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
