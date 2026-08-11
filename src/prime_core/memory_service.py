from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Callable

from src.prime_memory_adapter import AdapterResult, PrimeMemoryAdapter

from .db import connect, transaction
from .service import _id, now
from .history_primitives import record_historical_snapshot

SECRET_PATTERN = re.compile(r"(?i)(api[_-]?key|secret|password|token|private[_-]?key)\s*[:=]\s*[^\s]+")


class MemoryService:
    def __init__(self, settings: Any, adapter_factory: Callable[[str], Any] | None = None):
        self.settings = settings
        self.adapter_factory = adapter_factory or (lambda project_id: PrimeMemoryAdapter("http://127.0.0.1:18888", project_id))

    def store(self, project_id: str, content: str, content_class: str, source_revision: str | None = None,
              source_reference_id: str | None = None, branch_context: str | None = None) -> dict[str, Any]:
        if SECRET_PATTERN.search(content):
            return {"status": "REJECTED", "reason": "secret-sensitive content rejected"}
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
            db.execute(
                "INSERT INTO prime_core.memory_records(memory_id,project_id,source_reference_id,document_id,content_hash,content_class,content,status,bank_id,branch_context,source_revision,created_at,metadata) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (memory_id, project_id, source_reference_id, memory_id, content_hash, content_class, content, status, bank_id, branch_context, source_revision, created, json.dumps({"adapter_status": result.status, "adapter_reason": result.reason})),
            )
            record_historical_snapshot(db, project_id, "MEMORY", memory_id, source_revision, {"memory_id": memory_id, "content": content, "content_class": content_class, "status": status, "source_revision": source_revision}, created, content_hash)
            return {"status": status, "memory_id": memory_id, "bank_id": bank_id, "adapter_status": result.status}

    def recall(self, project_id: str, query: str, limit: int = 20) -> dict[str, Any]:
        adapter = self.adapter_factory(project_id)
        result: AdapterResult = adapter.recall(query)
        with connect(self.settings) as db:
            allowed = {row["document_id"]: dict(row) for row in db.execute("SELECT memory_id, document_id, source_revision, content_class, status FROM prime_core.memory_records WHERE project_id=%s AND status NOT IN ('TOMBSTONED','SUPERSEDED')", (project_id,)).fetchall()}
        results = []
        for item in result.payload.get("results", []) if isinstance(result.payload, dict) else []:
            document_id = item.get("document_id") if isinstance(item, dict) else None
            if document_id in allowed:
                results.append({"memory_id": allowed[document_id]["memory_id"], "document_id": document_id, "content_class": allowed[document_id]["content_class"], "source_revision": allowed[document_id]["source_revision"], "result": item})
            if len(results) >= limit:
                break
        return {"status": result.status, "results": results, "project_id": project_id}

    def tombstone(self, project_id: str, memory_id: str, reason: str, correction_type: str = "TOMBSTONE") -> None:
        with transaction(self.settings) as db:
            row = db.execute("SELECT 1 FROM prime_core.memory_records WHERE memory_id=%s AND project_id=%s", (memory_id, project_id)).fetchone()
            if not row:
                raise KeyError("memory not found")
            created = now()
            db.execute("UPDATE prime_core.memory_records SET status='TOMBSTONED' WHERE memory_id=%s AND project_id=%s", (memory_id, project_id))
            db.execute("INSERT INTO prime_core.memory_corrections(correction_id,project_id,memory_id,correction_type,reason,created_at,actor_type,actor_id) VALUES (%s,%s,%s,%s,%s,%s,'operator','operator')", (_id("correction"), project_id, memory_id, correction_type, reason, created))
            record_historical_snapshot(db, project_id, "MEMORY_CORRECTION", memory_id, None, {"memory_id": memory_id, "correction_type": correction_type, "reason": reason, "status": "TOMBSTONED"}, created)
