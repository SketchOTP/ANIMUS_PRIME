from __future__ import annotations

import hashlib
import json
from pathlib import PurePosixPath
from typing import Any

from .db import connect, transaction
from .service import _id, now


class BrainService:
    def __init__(self, settings: Any):
        self.settings = settings

    def build(self, project_id: str, source_revision: str | None = None) -> dict[str, Any]:
        with transaction(self.settings) as db:
            latest = db.execute("SELECT source_revision FROM prime_core.repository_files WHERE project_id=%s ORDER BY observed_at DESC LIMIT 1", (project_id,)).fetchone()
            revision = source_revision or (latest["source_revision"] if latest else None)
            if not revision:
                return {"project_id": project_id, "source_revision": None, "nodes": [], "edges": [], "layout": "derived-only", "availability": "UNAVAILABLE"}
            rows = db.execute("SELECT relative_path,file_kind,content_hash,size_bytes FROM prime_core.repository_files WHERE project_id=%s AND source_revision=%s ORDER BY relative_path", (project_id, revision)).fetchall()
            nodes = []
            edges = []
            known = set()
            for row in rows:
                path = row["relative_path"]
                node_id = "file_" + hashlib.sha256(f"{project_id}:{path}".encode()).hexdigest()[:24]
                nodes.append({"id": node_id, "kind": "authority" if path.startswith(".agent/") else "file", "label": path, "size_bytes": row["size_bytes"], "content_hash": row["content_hash"], "source_revision": revision})
                known.add(path)
                parent = str(PurePosixPath(path).parent)
                if parent != ".":
                    parent_id = "dir_" + hashlib.sha256(f"{project_id}:{parent}".encode()).hexdigest()[:24]
                    if parent not in known:
                        nodes.append({"id": parent_id, "kind": "directory", "label": parent, "source_revision": revision})
                        known.add(parent)
                    edges.append({"from": parent_id, "to": node_id, "kind": "contains"})
            graph = {"project_id": project_id, "source_revision": revision, "nodes": nodes, "edges": edges, "layout": "derived-only"}
            db.execute("INSERT INTO prime_core.brain_snapshots(brain_snapshot_id,project_id,source_revision,graph,created_at) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (project_id,source_revision) DO UPDATE SET graph=EXCLUDED.graph,created_at=EXCLUDED.created_at", (_id("brain"), project_id, revision, json.dumps(graph), now()))
            return graph

    def build_historical(self, project_id: str, as_of: str) -> dict[str, Any]:
        """Build disposable Brain topology from the revision selected by Time Lens."""
        from .history_service import HistoryService
        context = HistoryService(self.settings).historical_context(project_id, as_of)
        revision = context.get("selected_revision")
        if context["source_statuses"].get("repository") != "EXACT" or not revision:
            return {"project_id": project_id, "as_of": as_of, "source_revision": revision, "availability": "UNAVAILABLE", "source_statuses": context["source_statuses"], "nodes": [], "edges": []}
        graph = self.build(project_id, revision)
        source_statuses = {**context["source_statuses"], "brain": "EXACT"}
        return {**graph, "as_of": as_of, "historical": True, "source_statuses": source_statuses, "availability": "EXACT"}

    def get(self, project_id: str, source_revision: str | None = None) -> dict[str, Any] | None:
        with connect(self.settings) as db:
            if source_revision is None:
                row = db.execute("SELECT graph FROM prime_core.brain_snapshots WHERE project_id=%s ORDER BY created_at DESC LIMIT 1", (project_id,)).fetchone()
            else:
                row = db.execute("SELECT graph FROM prime_core.brain_snapshots WHERE project_id=%s AND source_revision=%s ORDER BY created_at DESC LIMIT 1", (project_id, source_revision)).fetchone()
            return row["graph"] if row and isinstance(row["graph"], dict) else (json.loads(row["graph"]) if row else None)
