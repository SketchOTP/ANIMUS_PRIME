from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .db import connect, transaction
from .git_provenance import search_git_history
from .history_service import HistoryService
from .indexer import RepositoryIndexer
from .memory_service import MemoryService
from .ai_service import AIExecutionService
from .retrieval import RetrievalHit, retrieval_hit
from .service import _id, now


# The pinned Hindsight 0.6.1 adapter does not expose a minimum-score request
# parameter. PRIME therefore applies a bounded floor after Recall, only for
# the Search/Ask retrieval boundary. The value is deliberately independent of
# any one qualification query and is exercised by positive/negative tests.
MEMORY_RELEVANCE_FLOOR = 0.25


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

    @staticmethod
    def _authority_text(row: dict[str, Any]) -> str:
        return str(row.get("content_snapshot") or row.get("metadata") or "")

    @staticmethod
    def _activity_text(row: dict[str, Any]) -> str:
        return f"{row.get('event_type', '')} {json.dumps(row.get('payload') or {}, sort_keys=True)}"

    def search(self, project_id: str, query: str, limit: int = 20) -> dict[str, Any]:
        bounded_limit = min(max(limit, 1), 50)
        repository_rows = self.indexer.search(project_id, query, bounded_limit)
        repository: list[RetrievalHit] = []
        authority: list[RetrievalHit] = []
        for row in repository_rows:
            relative_path = str(row["relative_path"])
            is_authority = (
                relative_path == "AGENTS.md"
                or relative_path.endswith("/AGENTS.md")
                or relative_path == "PROJECT_GOAL.md"
                or relative_path.endswith("/PROJECT_GOAL.md")
                or relative_path.startswith(".agent/")
            )
            group = "Authority" if is_authority else "Repository"
            target = authority if is_authority else repository
            target.append(retrieval_hit(
                source_class="Authority" if is_authority else "Repository",
                source_group=group,
                source_id=relative_path,
                project_id=project_id,
                locator=relative_path,
                text=row.get("text") or "",
                excerpt=row.get("excerpt") or row.get("text") or "",
                source_revision=row.get("source_revision"),
                content_hash=row.get("content_hash"),
                freshness_state=row.get("freshness_state", "CURRENT"),
                authority_class="AUTHORITATIVE" if is_authority else "AUTHORITATIVE",
                relevance=row.get("relevance"),
                size_bytes=row.get("size_bytes"),
                file_kind=row.get("file_kind"),
            ))

        with connect(self.settings) as db:
            needle = f"%{query}%"
            authority_rows = [dict(row) for row in db.execute(
                "SELECT authority_revision_id,source_path,source_hash,contract_version,validation_status,observed_at,canonical_commit,content_snapshot,metadata "
                "FROM prime_core.authority_revisions WHERE project_id=%s AND (source_path ILIKE %s OR source_hash ILIKE %s OR validation_status ILIKE %s OR COALESCE(metadata::text,'') ILIKE %s OR COALESCE(content_snapshot,'') ILIKE %s) ORDER BY observed_at DESC LIMIT %s",
                (project_id, needle, needle, needle, needle, needle, bounded_limit),
            ).fetchall()]
            for row in authority_rows:
                authority.append(retrieval_hit(
                    source_class="Authority",
                    source_group="Authority",
                    source_id=row["authority_revision_id"],
                    project_id=project_id,
                    locator=row.get("source_path") or row["authority_revision_id"],
                    text=self._authority_text(row),
                    source_revision=row.get("canonical_commit") or row.get("source_hash"),
                    content_hash=row.get("source_hash"),
                    freshness_state="CURRENT",
                    authority_class="AUTHORITATIVE",
                    relevance=1.0,
                    source_path=row.get("source_path"),
                    validation_status=row.get("validation_status"),
                    observed_at=row.get("observed_at"),
                ))

            activity_rows = [dict(row) for row in db.execute(
                "SELECT event_id,event_type,observed_at,source_revision,payload FROM prime_core.events WHERE project_id=%s AND (event_type ILIKE %s OR payload::text ILIKE %s) ORDER BY observed_at DESC LIMIT %s",
                (project_id, needle, needle, bounded_limit),
            ).fetchall()]
            activity = [retrieval_hit(source_class="Activity", source_group="Activity", source_id=row["event_id"], project_id=project_id, locator=f"event:{row['event_id']}", text=self._activity_text(row), source_revision=row.get("source_revision"), freshness_state="CURRENT", authority_class="DERIVED", relevance=1.0, event_type=row.get("event_type"), observed_at=row.get("observed_at")) for row in activity_rows]

            progress_rows = [dict(row) for row in db.execute(
                "SELECT pa.assessment_id,pa.progress_percent,pa.confidence,pa.freshness_state,pa.created_at,pa.summary,pa.repository_revision,pa.item_results "
                "FROM prime_core.progress_assessments pa WHERE pa.project_id=%s AND pa.freshness_state='CURRENT' AND NOT EXISTS (SELECT 1 FROM jsonb_array_elements_text(COALESCE(pa.evidence_refs,'[]'::jsonb)) AS ref(value) WHERE NOT EXISTS (SELECT 1 FROM prime_core.source_references sr WHERE sr.project_id=pa.project_id AND sr.source_reference_id=ref.value AND sr.freshness_state='CURRENT')) AND (pa.summary ILIKE %s OR pa.item_results::text ILIKE %s) ORDER BY pa.created_at DESC LIMIT %s",
                (project_id, needle, needle, bounded_limit),
            ).fetchall()]
            progress = [retrieval_hit(source_class="Progress", source_group="Progress", source_id=row["assessment_id"], project_id=project_id, locator=f"progress:{row['assessment_id']}", text=f"{row.get('summary') or ''} {json.dumps(row.get('item_results') or {}, sort_keys=True)}", source_revision=row.get("repository_revision"), freshness_state=row.get("freshness_state", "CURRENT"), authority_class="DERIVED", relevance=1.0, progress_percent=row.get("progress_percent"), confidence=row.get("confidence"), created_at=row.get("created_at")) for row in progress_rows]

            notion_rows = [dict(row) for row in db.execute(
                "SELECT s.source_binding_id,s.page_id,s.page_url,s.access_mode,s.status,s.observed_revision,s.observed_hash,s.observed_at,s.metadata,COALESCE(o.content->>'text','') AS content_text "
                "FROM prime_core.notion_knowledge_sources s LEFT JOIN LATERAL (SELECT content FROM prime_core.notion_source_observations o WHERE o.project_id=s.project_id AND o.source_binding_id=s.source_binding_id AND o.availability_status='CURRENT' ORDER BY o.observed_at DESC LIMIT 1) o ON TRUE "
                "WHERE s.project_id=%s AND COALESCE(s.status,'') NOT IN ('DETACHED','RETRACTED') AND (s.page_id ILIKE %s OR COALESCE(s.page_url,'') ILIKE %s OR COALESCE(s.metadata::text,'') ILIKE %s OR COALESCE(o.content->>'text','') ILIKE %s) ORDER BY s.observed_at DESC NULLS LAST LIMIT %s",
                (project_id, needle, needle, needle, needle, bounded_limit),
            ).fetchall()]
            notion = [retrieval_hit(source_class="Notion Knowledge", source_group="Notion Knowledge", source_id=row["source_binding_id"], project_id=project_id, locator=row.get("page_url") or row["page_id"], text=row.get("content_text") or json.dumps(row.get("metadata") or {}, sort_keys=True), source_revision=row.get("observed_revision"), content_hash=row.get("observed_hash"), freshness_state="CURRENT", authority_class="KNOWLEDGE", relevance=1.0, page_id=row.get("page_id"), page_url=row.get("page_url"), access_mode=row.get("access_mode"), observed_at=row.get("observed_at")) for row in notion_rows]

            evidence_rows = [dict(row) for row in db.execute(
                "SELECT evidence_id,source_reference_id,locator,source_revision,content_hash,privacy_class,parser_status,index_status,extracted_text,captured_at FROM prime_core.evidence_records WHERE project_id=%s AND retracted_at IS NULL AND purged_at IS NULL AND index_status='READY' AND (locator ILIKE %s OR COALESCE(extracted_text,'') ILIKE %s) ORDER BY captured_at DESC LIMIT %s",
                (project_id, needle, needle, bounded_limit),
            ).fetchall()]
        evidence: list[RetrievalHit] = []
        for row in evidence_rows:
            evidence.append(retrieval_hit(source_class="Evidence", source_group="Evidence", source_id=row["evidence_id"], project_id=project_id, locator=row.get("locator") or row["evidence_id"], text=row.get("extracted_text") or "", source_revision=row.get("source_revision"), content_hash=row.get("content_hash"), freshness_state="CURRENT", authority_class="DERIVED", relevance=1.0, source_reference_id=row.get("source_reference_id"), privacy_class=row.get("privacy_class"), parser_status=row.get("parser_status"), captured_at=row.get("captured_at")))

        git: list[RetrievalHit] = []
        with connect(self.settings) as db:
            binding = db.execute("SELECT r.canonical_path FROM prime_core.project_bindings b JOIN prime_core.repositories r ON r.repository_id=b.repository_id WHERE b.project_id=%s", (project_id,)).fetchone()
        if binding and binding.get("canonical_path"):
            for row in search_git_history(Path(binding["canonical_path"]), query, bounded_limit):
                git.append(retrieval_hit(source_class="Git", source_group="Git", source_id=f"git:{row['commit_id']}", project_id=project_id, locator=f"git:{row['commit_id']}", text=row["text"], source_revision=row["source_revision"], content_hash=row["content_hash"], freshness_state="CURRENT", authority_class="AUTHORITATIVE", relevance=row.get("relevance"), commit_id=row["commit_id"], subject=row["subject"], captured_at=row["captured_at"], canonical_ref=row.get("canonical_ref"), canonical_commit=row.get("canonical_commit")))

        memory_rows = self.memory.recall(project_id, query, min(bounded_limit, 8), min_relevance=MEMORY_RELEVANCE_FLOOR).get("results", [])
        memory: list[RetrievalHit] = []
        for row in memory_rows:
            memory.append(retrieval_hit(source_class="Memory", source_group="Memory", source_id=row["memory_id"], project_id=project_id, locator=f"memory:{row['memory_id']}", text="", source_revision=row.get("source_revision"), freshness_state="CURRENT", authority_class="DERIVED", relevance=row.get("relevance"), memory_id=row["memory_id"], source_reference_id=row.get("source_reference_id"), content_class=row.get("content_class"), metadata=row.get("metadata")))

        groups = {"Repository": repository, "Authority": authority, "Git": git, "Notion Knowledge": notion, "Activity": activity, "Progress": progress, "Memory": memory, "Evidence": evidence}
        return {"project_id": project_id, "groups": groups, "retrieval_policy": {"memory_relevance_floor": MEMORY_RELEVANCE_FLOOR, "revision": "prime-shared-retrieval-v1"}}

    def ask(self, project_id: str, question: str) -> dict[str, Any]:
        sources = self.search(project_id, question, 8)
        model_sources: list[dict[str, Any]] = []
        memory_content: dict[str, str] = {}
        with connect(self.settings) as db:
            memory_ids = [row["memory_id"] for row in sources["groups"]["Memory"]]
            if memory_ids:
                memory_rows = db.execute("SELECT memory_id,content FROM prime_core.memory_records WHERE project_id=%s AND memory_id = ANY(%s)", (project_id, memory_ids)).fetchall()
                memory_content = {row["memory_id"]: row["content"] for row in memory_rows}
        for group_rows in sources["groups"].values():
            for row in group_rows:
                source_id = row.get("source_id")
                if not source_id:
                    continue
                text = row.get("text") or row.get("excerpt") or ""
                if row.get("source_group") == "Memory":
                    text = memory_content.get(row["memory_id"], "")
                elif row.get("source_group") == "Evidence" and not text:
                    evidence = self.history.retrieve_evidence(project_id, row["source_id"])
                    text = (evidence.get("content") or b"").decode("utf-8", errors="replace") if evidence.get("availability") == "EXACT" else ""
                model_sources.append({
                    "source_class": row.get("source_class", row.get("source_group")),
                    "source_id": source_id,
                    "locator": row.get("locator") or source_id,
                    "project_id": project_id,
                    "source_revision": row.get("source_revision"),
                    "content_hash": row.get("content_hash"),
                    "freshness_state": row.get("freshness_state", "CURRENT"),
                    "privacy_class": row.get("privacy_class", "PROJECT_PRIVATE"),
                    "text": text,
                })
        model = self.ai.execute(project_id, "ASK_PRIME", {"question": question}, model_sources)
        result = dict(model.get("result") or {})
        admitted_by_id = {str(source["source_id"]): source for source in model_sources if source.get("source_id")}
        resolved_citations = []
        for citation in result.get("citations") or []:
            source_id = str(citation.get("source_id", ""))
            admitted = admitted_by_id.get(source_id)
            if admitted is None:
                continue
            resolved = dict(citation)
            for field in ("source_class", "source_id", "locator", "project_id", "source_revision", "content_hash", "freshness_state", "privacy_class"):
                if admitted.get(field) is not None:
                    resolved[field] = admitted[field]
            resolved_citations.append(resolved)
        result["citations"] = resolved_citations
        response = {"project_id": project_id, **result, "epistemic": result.get("category", "UNKNOWN"), "ai_run": {key: model.get(key) for key in ("run_id", "provider", "model", "profile_revision", "prompt_revision", "schema_revision", "privacy_mode", "source_revision_set", "status")}}
        if model["status"] != "SUCCEEDED":
            response.update({"answer": "UNKNOWN: available evidence does not support this claim.", "citations": [], "epistemic": "UNKNOWN"})
        return response

    def ask_at(self, project_id: str, question: str, as_of: str) -> dict[str, Any]:
        context = self.history.historical_context(project_id, as_of)
        citations = []
        for row in context["evidence"]:
            if row.get("retracted_at") is None:
                citations.append({"source_class": "Evidence", "source_reference_id": row.get("source_reference_id"), "content_hash": row.get("content_hash"), "source_revision": row.get("source_revision"), "historical": True})
        for row in context["progress"]:
            citations.append({"source_class": "ProgressAssessment", "assessment_id": row.get("assessment_id"), "repository_revision": row.get("repository_revision"), "historical": True})
        return {"project_id": project_id, "as_of": as_of, "selected_revision": context.get("selected_revision"), "reconstruction_status": context["reconstruction_status"], "answer": "Historical evidence is available in the cited sources." if citations else "UNKNOWN: no evidence available at the selected historical boundary.", "citations": citations[:16], "historical": True, "later_current_state_used": False, "question": question, "source_statuses": context["source_statuses"]}

    def since_last_seen(self, project_id: str, advance: bool = False) -> dict[str, Any]:
        with transaction(self.settings) as db:
            checkpoint = db.execute("SELECT last_seen_event_sequence FROM prime_core.activity_checkpoints WHERE project_id=%s", (project_id,)).fetchone()
            last = checkpoint["last_seen_event_sequence"] if checkpoint else 0
            events = [dict(event) for event in db.execute("SELECT event_id,event_type,project_sequence,observed_at,payload FROM prime_core.events WHERE project_id=%s AND COALESCE(project_sequence,0)>%s ORDER BY project_sequence", (project_id, last)).fetchall()]
            new_last = max([last, *[int(event["project_sequence"] or 0) for event in events]])
            if advance:
                db.execute("INSERT INTO prime_core.activity_checkpoints(project_id,last_seen_event_sequence,updated_at) VALUES (%s,%s,%s) ON CONFLICT (project_id) DO UPDATE SET last_seen_event_sequence=EXCLUDED.last_seen_event_sequence,updated_at=EXCLUDED.updated_at", (project_id, new_last, now()))
            return {"project_id": project_id, "events": events, "advanced_to": new_last, "advanced": advance}
