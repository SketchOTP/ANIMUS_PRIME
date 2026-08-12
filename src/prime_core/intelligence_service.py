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

    @staticmethod
    def _run_metadata(model: dict[str, Any]) -> dict[str, Any]:
        return {key: model.get(key) for key in ("run_id", "provider", "model", "profile_revision", "prompt_revision", "schema_revision", "privacy_mode", "source_revision_set", "status")}

    def execute_product(self, project_id: str, function: str, prompt_input: dict[str, Any], sources: list[dict[str, Any]], *, notion: Any | None = None, source_revision: str = "product-current", source_rank: int = 0) -> dict[str, Any]:
        """Execute one AI function through the product/service boundary.

        The AI boundary remains responsible for provider validation and durable
        ``ai_runs``. This layer owns PRIME side effects: documentation
        projection and memory admission/correction, so qualification can prove
        that the durable run and product result agree.
        """
        model = self.ai.execute(project_id, function, prompt_input, sources)
        response: dict[str, Any] = {"project_id": project_id, "function": function.upper(), "status": model["status"], "ai_run": self._run_metadata(model), "result": model.get("result", {})}
        if model["status"] != "SUCCEEDED":
            return response
        output = model["result"]
        if function.upper() == "DOCUMENTATION" and notion is not None:
            projection = notion.document(project_id, output.get("sections", {}), source_revision, source_rank, documentation_run_id=model["run_id"])
            response["projection"] = projection
            response["status"] = projection.get("status", response["status"])
        elif function.upper() == "MEMORY_ADMISSION" and output.get("admit") is True:
            citation = (output.get("citations") or [{}])[0]
            response["memory"] = self.memory.store(project_id, output.get("proposition", ""), "FACT", source_revision=source_revision, source_reference_id=citation.get("source_id"))
        elif function.upper() == "CORRECTION":
            citation = (output.get("citations") or [{}])[0]
            response["memory"] = self.memory.store(project_id, output["proposition"], "FACT", source_revision=source_revision, source_reference_id=citation.get("source_id"), supersedes_memory_id=output["supersedes_memory_id"], correction_reason=output.get("correction_reason"))
        return response

    def search(self, project_id: str, query: str, limit: int = 20) -> dict[str, Any]:
        repository = self.indexer.search(project_id, query, min(limit, 50))
        with connect(self.settings) as db:
            needle = f"%{query}%"
            authority = [dict(row) for row in db.execute(
                "SELECT authority_revision_id,source_path,source_hash,contract_version,validation_status,observed_at,canonical_commit "
                "FROM prime_core.authority_revisions WHERE project_id=%s AND (source_path ILIKE %s OR source_hash ILIKE %s OR validation_status ILIKE %s OR metadata::text ILIKE %s) ORDER BY observed_at DESC LIMIT %s",
                (project_id, needle, needle, needle, needle, min(limit, 50)),
            ).fetchall()]
            git = [dict(row) for row in db.execute(
                "SELECT checkpoint_id,commit_id,coverage_status,content_hash,captured_at FROM prime_core.git_history_checkpoints WHERE project_id=%s AND (commit_id ILIKE %s OR coverage_status ILIKE %s OR COALESCE(metadata::text,'') ILIKE %s) ORDER BY captured_at DESC LIMIT %s",
                (project_id, needle, needle, needle, min(limit, 50)),
            ).fetchall()]
            notion = [dict(row) for row in db.execute(
                "SELECT source_binding_id,page_id,page_url,access_mode,status,observed_revision,observed_hash,observed_at FROM prime_core.notion_knowledge_sources WHERE project_id=%s AND (page_id ILIKE %s OR COALESCE(page_url,'') ILIKE %s OR status ILIKE %s OR COALESCE(metadata::text,'') ILIKE %s) ORDER BY observed_at DESC NULLS LAST LIMIT %s",
                (project_id, needle, needle, needle, needle, min(limit, 50)),
            ).fetchall()]
            activity = [dict(row) for row in db.execute("SELECT event_id,event_type,observed_at,source_revision,payload FROM prime_core.events WHERE project_id=%s AND (event_type ILIKE %s OR payload::text ILIKE %s) ORDER BY observed_at DESC LIMIT %s", (project_id, needle, needle, min(limit, 50))).fetchall()]
            progress = [dict(row) for row in db.execute("SELECT assessment_id,progress_percent,confidence,freshness_state,created_at,summary,repository_revision FROM prime_core.progress_assessments WHERE project_id=%s AND (summary ILIKE %s OR item_results::text ILIKE %s) ORDER BY created_at DESC LIMIT %s", (project_id, needle, needle, min(limit, 50))).fetchall()]
            evidence = [dict(row) for row in db.execute(
                "SELECT evidence_id,source_reference_id,locator,source_revision,content_hash,privacy_class,parser_status,index_status,extracted_text,captured_at "
                "FROM prime_core.evidence_records WHERE project_id=%s AND retracted_at IS NULL AND purged_at IS NULL "
                "AND index_status='READY' AND (locator ILIKE %s OR COALESCE(extracted_text,'') ILIKE %s) "
                "ORDER BY captured_at DESC LIMIT %s",
                (project_id, f"%{query}%", f"%{query}%", min(limit, 50)),
            ).fetchall()]
        for row in evidence:
            row["source_class"] = "Evidence"
            row["source_group"] = "Evidence"
            row["source_id"] = row["evidence_id"]
            row["historical_authority"] = False
            row.pop("extracted_text", None)
        for group, rows in (("Repository", repository), ("Authority", authority), ("Git", git), ("Notion Knowledge", notion), ("Activity", activity), ("Progress", progress)):
            for row in rows:
                row["source_group"] = group
                row.setdefault("source_id", row.get("relative_path") or row.get("event_id") or row.get("authority_revision_id") or row.get("checkpoint_id") or row.get("source_binding_id") or row.get("assessment_id"))
        memory = self.memory.recall(project_id, query, min(limit, 8)).get("results", [])
        for row in memory:
            row["source_group"] = "Memory"
            row.setdefault("source_id", row.get("memory_id"))
        return {"project_id": project_id, "groups": {"Repository": repository, "Authority": authority, "Git": git, "Notion Knowledge": notion, "Activity": activity, "Progress": progress, "Memory": memory, "Evidence": evidence}}

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
        for row in sources["groups"]["Evidence"]:
            source_id = row["evidence_id"]
            citations.append({"source_class": "Evidence", "source_id": source_id, "source_reference_id": row.get("source_reference_id"), "content_hash": row.get("content_hash"), "source_revision": row.get("source_revision"), "historical": False})
            evidence = self.history.retrieve_evidence(project_id, source_id)
            model_sources.append({"source_class": "Evidence", "source_id": source_id, "source_reference_id": row.get("source_reference_id"), "locator": row.get("locator"), "project_id": project_id, "source_revision": row.get("source_revision"), "content_hash": row.get("content_hash"), "privacy_class": row.get("privacy_class"), "text": (evidence.get("content") or b"").decode("utf-8", errors="replace") if evidence.get("availability") == "EXACT" else ""})
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
