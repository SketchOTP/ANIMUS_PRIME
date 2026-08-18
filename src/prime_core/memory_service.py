from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Callable

from src.prime_memory_adapter import AdapterResult, PrimeMemoryAdapter

from .db import connect, transaction
from .service import _id, now
from .history_primitives import record_historical_snapshot
from .git_provenance import capture_provenance
from .workflow_primitives import qualification_interrupt

SECRET_PATTERN = re.compile(r"(?i)(api[_-]?key|secret|password|token|private[_-]?key)\s*[:=]\s*[^\s]+")


class MemoryService:
    def __init__(self, settings: Any, adapter_factory: Callable[[str], Any] | None = None):
        self.settings = settings
        self.adapter_factory = adapter_factory or (lambda project_id: PrimeMemoryAdapter(self.settings.hindsight_base_url, project_id, timeout_seconds=self.settings.hindsight_timeout_seconds))

    def ensure_bank(self, project_id: str, parent_workflow_id: str | None = None) -> dict[str, Any]:
        """Create/reconcile the stable project bank through the durable ledger."""
        from .service import CoreService

        core = CoreService(self.settings)
        bank_id = f"prime-{project_id}"
        if parent_workflow_id:
            core.record_workflow_resource(parent_workflow_id, "HINDSIGHT_BANK", bank_id, bank_id, {"project_id": project_id, "creation": "STABLE_PUT"}, "EXPECTED")
            qualification_interrupt("FORK_PROJECT", "HINDSIGHT_BOUND", "BEFORE_EXTERNAL_CALL")
            result = self.adapter_factory(project_id).create_bank()
            qualification_interrupt("FORK_PROJECT", "HINDSIGHT_BOUND", "EXTERNAL_SUCCESS_BEFORE_PERSIST")
            status = "CREATED" if result.status == "CURRENT" else "RECONCILIATION_REQUIRED"
            core.record_workflow_resource(parent_workflow_id, "HINDSIGHT_BANK", bank_id, bank_id, {"project_id": project_id, "adapter_status": result.status, "reason": result.reason, "replay": "IDEMPOTENT_STABLE_PUT"}, status)
            return {"status": result.status, "project_id": project_id, "bank_id": bank_id, "reason": result.reason}

        workflow = core.start_or_get_workflow("ENSURE_HINDSIGHT_BANK", f"hindsight-bank:{project_id}", project_id, [
            {"step_key": "BANK_EXPECTED", "replay_policy": "PURE_OR_DB_TRANSACTION"},
            {"step_key": "BANK_CREATED", "replay_policy": "IDEMPOTENT_EXTERNAL"},
            {"step_key": "BANK_BOUND", "replay_policy": "PURE_OR_DB_TRANSACTION"},
        ])
        step = core.begin_step(workflow["workflow_id"], "BANK_EXPECTED")
        if step["decision"] != "SKIP_COMPLETED":
            core.record_workflow_resource(workflow["workflow_id"], "HINDSIGHT_BANK", bank_id, bank_id, {"project_id": project_id, "creation": "STABLE_PUT"}, "EXPECTED")
            core.complete_step(workflow["workflow_id"], "BANK_EXPECTED")
        step = core.begin_step(workflow["workflow_id"], "BANK_CREATED")
        result = AdapterResult("CURRENT", {})
        if step["decision"] != "SKIP_COMPLETED":
            qualification_interrupt("ENSURE_HINDSIGHT_BANK", "BANK_CREATED", "BEFORE_EXTERNAL_CALL")
            result = self.adapter_factory(project_id).create_bank()
            if result.status != "CURRENT":
                core.fail_step(workflow["workflow_id"], "BANK_CREATED", result.reason or "Hindsight bank unavailable", retryable=True)
                return {"status": result.status, "project_id": project_id, "bank_id": bank_id, "reason": result.reason, "workflow_id": workflow["workflow_id"]}
            qualification_interrupt("ENSURE_HINDSIGHT_BANK", "BANK_CREATED", "EXTERNAL_SUCCESS_BEFORE_PERSIST")
            core.record_workflow_resource(workflow["workflow_id"], "HINDSIGHT_BANK", bank_id, bank_id, {"project_id": project_id, "adapter_status": result.status, "replay": "IDEMPOTENT_STABLE_PUT"}, "CREATED")
            core.complete_step(workflow["workflow_id"], "BANK_CREATED", side_effect_state={"bank_id": bank_id})
        step = core.begin_step(workflow["workflow_id"], "BANK_BOUND")
        if step["decision"] != "SKIP_COMPLETED":
            core.complete_step(workflow["workflow_id"], "BANK_BOUND", {"bank_id": bank_id})
        core.complete_workflow(workflow["workflow_id"], "BANK_BOUND")
        return {"status": "CURRENT", "project_id": project_id, "bank_id": bank_id, "workflow_id": workflow["workflow_id"], "reconciled": step["decision"] == "SKIP_COMPLETED"}

    def store(self, project_id: str, content: str, content_class: str, source_revision: str | None = None,
              source_reference_id: str | None = None, branch_context: str | None = None,
              supersedes_memory_id: str | None = None, correction_reason: str | None = None,
              metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        if SECRET_PATTERN.search(content):
            return {"status": "REJECTED", "reason": "secret-sensitive content rejected"}
        bank = self.ensure_bank(project_id)
        if bank["status"] != "CURRENT":
            return {"status": "DEGRADED", "reason": bank.get("reason") or "Hindsight bank unavailable", "bank_id": bank["bank_id"]}
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        with transaction(self.settings) as db:
            duplicate = db.execute("SELECT * FROM prime_core.memory_records WHERE project_id=%s AND content_hash=%s AND status NOT IN ('TOMBSTONED','SUPERSEDED')", (project_id, content_hash)).fetchone()
            if duplicate:
                return {"status": "DUPLICATE", "memory_id": duplicate["memory_id"]}
            memory_id = _id("memory")
            bank_id = f"prime-{project_id}"
            adapter = self.adapter_factory(project_id)
            result: AdapterResult = adapter.retain_verified(content, memory_id)
            status = "STORED" if result.status == "CURRENT" else ("DEGRADED" if result.status in {"DEGRADED", "UNAVAILABLE"} else "QUEUED")
            created = now()
            record_metadata = {"adapter_status": result.status, "adapter_reason": result.reason, "correction_reason": correction_reason}
            record_metadata["git_provenance"] = capture_provenance(self.settings, project_id, source_revision)
            if metadata:
                record_metadata.update(metadata)
            db.execute(
                "INSERT INTO prime_core.memory_records(memory_id,project_id,source_reference_id,document_id,content_hash,content_class,content,status,bank_id,branch_context,source_revision,created_at,supersedes_memory_id,metadata) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (memory_id, project_id, source_reference_id, memory_id, content_hash, content_class, content, status, bank_id, branch_context, source_revision, created, supersedes_memory_id, json.dumps(record_metadata)),
            )
            if supersedes_memory_id:
                old = db.execute("UPDATE prime_core.memory_records SET status='SUPERSEDED' WHERE project_id=%s AND memory_id=%s AND status NOT IN ('TOMBSTONED','SUPERSEDED') RETURNING memory_id", (project_id, supersedes_memory_id)).fetchone()
                if not old:
                    raise ValueError("superseded memory is not current in this project")
                db.execute("INSERT INTO prime_core.memory_corrections(correction_id,project_id,memory_id,correction_type,reason,created_at,actor_type,actor_id) VALUES (%s,%s,%s,'SUPERSEDE',%s,%s,'system','ai-correction')", (_id("correction"), project_id, supersedes_memory_id, correction_reason or "AI correction", created))
            record_historical_snapshot(db, project_id, "MEMORY", memory_id, source_revision, {"memory_id": memory_id, "content": content, "content_class": content_class, "status": status, "source_revision": source_revision}, created, content_hash)
            return {"status": status, "memory_id": memory_id, "bank_id": bank_id, "adapter_status": result.status}

    def recall(self, project_id: str, query: str, limit: int = 20, min_relevance: float | None = None) -> dict[str, Any]:
        adapter = self.adapter_factory(project_id)
        result: AdapterResult = adapter.recall(query)
        with connect(self.settings) as db:
            allowed = {row["document_id"]: dict(row) for row in db.execute("SELECT m.memory_id, m.document_id, m.source_revision, m.source_reference_id, m.content_class, m.status, m.branch_context, m.metadata FROM prime_core.memory_records m LEFT JOIN prime_core.source_references sr ON sr.project_id=m.project_id AND sr.source_reference_id=m.source_reference_id WHERE m.project_id=%s AND m.status NOT IN ('TOMBSTONED','SUPERSEDED') AND (m.source_reference_id IS NULL OR sr.freshness_state='CURRENT')", (project_id,)).fetchall()}
        results = []
        for item in result.payload.get("results", []) if isinstance(result.payload, dict) else []:
            document_id = item.get("document_id") if isinstance(item, dict) else None
            if document_id in allowed:
                score = None
                if isinstance(item, dict):
                    candidates = [item]
                    nested = item.get("result")
                    if isinstance(nested, dict):
                        candidates.extend([nested, nested.get("scores")])
                    candidates.append(item.get("scores"))
                    for candidate in candidates:
                        if not isinstance(candidate, dict):
                            continue
                        for key in ("score", "relevance", "similarity", "final", "reranker", "semantic", "keyword"):
                            value = candidate.get(key)
                            if value is not None:
                                try:
                                    score = float(value)
                                except (TypeError, ValueError):
                                    continue
                                break
                        if score is not None:
                            break
                if min_relevance is not None and (score is None or score < min_relevance):
                    continue
                results.append({"memory_id": allowed[document_id]["memory_id"], "document_id": document_id, "content_class": allowed[document_id]["content_class"], "source_revision": allowed[document_id]["source_revision"], "source_reference_id": allowed[document_id]["source_reference_id"], "branch_context": allowed[document_id]["branch_context"], "metadata": allowed[document_id]["metadata"], "relevance": score, "result": item})
            if len(results) >= limit:
                break
        return {"status": result.status, "results": results, "project_id": project_id}

    def list_mental_models(self, project_id: str) -> dict[str, Any]:
        adapter = self.adapter_factory(project_id)
        result = adapter.list_mental_models()
        payload = result.payload if isinstance(result.payload, dict) else {}
        items = payload.get("items", []) if isinstance(payload.get("items", []), list) else []
        return {
            "status": result.status,
            "project_id": project_id,
            "bank_id": f"prime-{project_id}",
            "classification": "DERIVED_NON_AUTHORITATIVE",
            "authoritative": False,
            "items": items,
            "count": len(items),
            "reason": result.reason,
        }

    def create_mental_model(
        self,
        project_id: str,
        name: str,
        source_query: str,
        model_id: str | None = None,
        max_tokens: int = 2048,
    ) -> dict[str, Any]:
        adapter = self.adapter_factory(project_id)
        result = adapter.create_mental_model(
            name=name,
            source_query=source_query,
            model_id=model_id,
            max_tokens=max_tokens,
        )
        return {
            "status": result.status,
            "project_id": project_id,
            "bank_id": f"prime-{project_id}",
            "classification": "DERIVED_NON_AUTHORITATIVE",
            "authoritative": False,
            "operation": result.payload,
            "reason": result.reason,
        }

    def mental_model_operation(self, project_id: str, operation_id: str) -> dict[str, Any]:
        adapter = self.adapter_factory(project_id)
        result = adapter.mental_model_operation(operation_id)
        return {
            "status": result.status,
            "project_id": project_id,
            "bank_id": f"prime-{project_id}",
            "classification": "DERIVED_NON_AUTHORITATIVE",
            "authoritative": False,
            "operation": result.payload,
            "reason": result.reason,
        }

    def get_mental_model(self, project_id: str, model_id: str) -> dict[str, Any]:
        adapter = self.adapter_factory(project_id)
        result = adapter.get_mental_model(model_id)
        return {
            "status": result.status,
            "project_id": project_id,
            "bank_id": f"prime-{project_id}",
            "classification": "DERIVED_NON_AUTHORITATIVE",
            "authoritative": False,
            "mental_model": result.payload,
            "reason": result.reason,
        }

    def rebuild_from_source_ledger(self, project_id: str) -> dict[str, Any]:
        """Recreate a project bank from PRIME's current, provenance-bearing ledger.

        Hindsight observations and Mental Models are derived state. PRIME's
        memory_records and correction status remain authoritative, so rebuild
        deliberately reports SOURCE_LEDGER_REBUILD rather than pretending the
        native backend was restored bit-for-bit.
        """
        adapter = self.adapter_factory(project_id)
        deleted = adapter.delete_bank()
        if deleted.status == "UNAVAILABLE":
            return {"status": "UNAVAILABLE", "mode": "SOURCE_LEDGER_REBUILD", "project_id": project_id, "bank_id": f"prime-{project_id}", "restored": 0, "reason": deleted.reason}
        created = adapter.create_bank()
        if created.status == "UNAVAILABLE":
            return {"status": "UNAVAILABLE", "mode": "SOURCE_LEDGER_REBUILD", "project_id": project_id, "bank_id": f"prime-{project_id}", "restored": 0, "reason": created.reason}
        with connect(self.settings) as db:
            rows = db.execute(
                "SELECT memory_id,content,source_revision,content_class FROM prime_core.memory_records "
                "WHERE project_id=%s AND status NOT IN ('TOMBSTONED','SUPERSEDED') AND (source_reference_id IS NULL OR source_reference_id IN (SELECT source_reference_id FROM prime_core.source_references WHERE project_id=%s AND freshness_state='CURRENT')) ORDER BY created_at,memory_id",
                (project_id, project_id),
            ).fetchall()
        restored = 0
        unavailable: list[str] = []
        for row in rows:
            result = adapter.retain_verified(row["content"], row["memory_id"])
            if result.status == "CURRENT":
                restored += 1
            else:
                unavailable.append(row["memory_id"])
        return {
            "status": "CURRENT" if not unavailable else "DEGRADED",
            "mode": "SOURCE_LEDGER_REBUILD",
            "fidelity": "REBUILDABLE_NOT_BIT_IDENTICAL",
            "project_id": project_id,
            "bank_id": f"prime-{project_id}",
            "restored": restored,
            "eligible": len(rows),
            "unavailable_memory_ids": unavailable,
            "superseded_and_tombstoned_excluded": True,
        }

    def tombstone(self, project_id: str, memory_id: str, reason: str, correction_type: str = "TOMBSTONE") -> None:
        with transaction(self.settings) as db:
            row = db.execute("SELECT 1 FROM prime_core.memory_records WHERE memory_id=%s AND project_id=%s", (memory_id, project_id)).fetchone()
            if not row:
                raise KeyError("memory not found")
            created = now()
            db.execute("UPDATE prime_core.memory_records SET status='TOMBSTONED' WHERE memory_id=%s AND project_id=%s", (memory_id, project_id))
            db.execute("INSERT INTO prime_core.memory_corrections(correction_id,project_id,memory_id,correction_type,reason,created_at,actor_type,actor_id) VALUES (%s,%s,%s,%s,%s,%s,'operator','operator')", (_id("correction"), project_id, memory_id, correction_type, reason, created))
            record_historical_snapshot(db, project_id, "MEMORY_CORRECTION", memory_id, None, {"memory_id": memory_id, "correction_type": correction_type, "reason": reason, "status": "TOMBSTONED"}, created)
