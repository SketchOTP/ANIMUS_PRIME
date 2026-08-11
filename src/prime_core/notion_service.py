from __future__ import annotations

import hashlib
import json
from typing import Any

from .db import transaction
from .service import _id, now
from .history_primitives import record_historical_snapshot

START = "<!-- PRIME_MANAGED_START -->"
END = "<!-- PRIME_MANAGED_END -->"


class NotionProjectionService:
    def __init__(self, settings: Any):
        self.settings = settings

    def project(self, project_id: str, existing_content: str, managed_content: str, available: bool = True) -> dict[str, Any]:
        if not available:
            self._record(project_id, "", "DEGRADED", {"reason": "notion unavailable"}, None)
            return {"status": "DEGRADED", "retryable": True}
        if START not in existing_content or END not in existing_content or existing_content.index(START) > existing_content.index(END):
            self._record(project_id, "", "CONFLICT", {"reason": "managed markers missing or ambiguous"}, existing_content)
            return {"status": "CONFLICT", "retryable": False}
        start = existing_content.index(START) + len(START)
        end = existing_content.index(END)
        replacement = f"{START}\n{managed_content.strip()}\n{END}"
        content = existing_content[: existing_content.index(START)] + replacement + existing_content[end + len(END):]
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        self._record(project_id, content_hash, "SYNCED", {"managed_hash": hashlib.sha256(managed_content.encode()).hexdigest()}, content)
        return {"status": "SYNCED", "content": content, "content_hash": content_hash, "idempotent": content == existing_content}

    def _record(self, project_id: str, content_hash: str, status: str, metadata: dict[str, Any], rendered_content: str | None) -> None:
        connection_status = {"SYNCED": "CONNECTED", "DEGRADED": "DEGRADED", "CONFLICT": "CONFLICT"}[status]
        with transaction(self.settings) as db:
            db.execute("INSERT INTO prime_core.notion_projects(project_id,connection_status,managed_content_hash,last_synced_at,updated_at) VALUES (%s,%s,%s,CASE WHEN %s='SYNCED' THEN now() ELSE NULL END,now()) ON CONFLICT (project_id) DO UPDATE SET connection_status=EXCLUDED.connection_status,managed_content_hash=EXCLUDED.managed_content_hash,last_synced_at=EXCLUDED.last_synced_at,updated_at=now()", (project_id, connection_status, content_hash or None, status))
            observed = now()
            revision_id = _id("notionrev")
            db.execute("INSERT INTO prime_core.notion_projection_revisions(projection_revision_id,project_id,content_hash,source_set,sync_status,observed_at,metadata,rendered_content,managed_section_key,notion_target_refs) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (revision_id, project_id, content_hash, json.dumps([]), status, observed, json.dumps(metadata), rendered_content, "PRIME_MANAGED", json.dumps({})))
            record_historical_snapshot(db, project_id, "NOTION_PROJECTION", revision_id, metadata.get("source_revision"), {"projection_revision_id": revision_id, "content_hash": content_hash, "sync_status": status, "rendered_content": rendered_content, "metadata": metadata}, observed, content_hash or None)
