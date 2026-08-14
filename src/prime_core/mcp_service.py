from __future__ import annotations

import hashlib
import json
import secrets
from datetime import timedelta
from typing import Any

from .db import connect, transaction
from .memory_service import MemoryService
from .service import _id, now

CANONICAL_TOOLS = {
    "prime_memory_store", "prime_memory_recall", "prime_memory_timeline",
    "prime_memory_get", "prime_memory_report_problem", "prime_memory_context",
}
KIND_TO_CLASS = {
    "learning": "LEARNING", "decision_rationale": "RATIONALE", "failure": "FAILURE",
    "procedure": "PROCEDURE", "environment": "ENVIRONMENT", "constraint": "CONSTRAINT",
    "observation": "OBSERVATION", "experience": "EXPERIENCE", "world_fact": "FACT", "hypothesis": "HYPOTHESIS",
}


class MCPService:
    def __init__(self, settings: Any, memory: MemoryService | None = None):
        self.settings = settings
        self.memory = memory or MemoryService(settings)

    def issue_grant(self, project_id: str, client_id: str) -> dict[str, Any]:
        token = secrets.token_urlsafe(32)
        timestamp = now()
        with transaction(self.settings) as db:
            if not db.execute("SELECT 1 FROM prime_core.projects WHERE project_id=%s", (project_id,)).fetchone():
                raise KeyError("project not found")
            grant_id = _id("grant")
            db.execute("INSERT INTO prime_core.mcp_grants(grant_id,project_id,client_id,token_hash,created_at,expires_at) VALUES (%s,%s,%s,%s,%s,%s)", (grant_id, project_id, client_id, self.digest(token), timestamp, timestamp + timedelta(days=30)))
        return {"grant_id": grant_id, "client_id": client_id, "project_id": project_id, "token": token, "expires_at": timestamp + timedelta(days=30)}

    def revoke_grant(self, grant_id: str, project_id: str | None = None) -> None:
        with transaction(self.settings) as db:
            if project_id is None:
                row = db.execute("SELECT 1 FROM prime_core.mcp_grants WHERE grant_id=%s", (grant_id,)).fetchone()
            else:
                row = db.execute("SELECT 1 FROM prime_core.mcp_grants WHERE grant_id=%s AND project_id=%s", (grant_id, project_id)).fetchone()
            if not row:
                raise KeyError("grant not found")
            db.execute("UPDATE prime_core.mcp_grants SET revoked_at=now() WHERE grant_id=%s", (grant_id,))

    def list_grants(self, project_id: str) -> list[dict[str, Any]]:
        with connect(self.settings) as db:
            rows = db.execute("SELECT grant_id,project_id,client_id,created_at,expires_at,revoked_at FROM prime_core.mcp_grants WHERE project_id=%s ORDER BY created_at DESC", (project_id,)).fetchall()
        return [dict(row) for row in rows]

    def rotate_grant(self, project_id: str, grant_id: str, client_id: str | None = None) -> dict[str, Any]:
        with transaction(self.settings) as db:
            row = db.execute("SELECT client_id FROM prime_core.mcp_grants WHERE grant_id=%s AND project_id=%s AND revoked_at IS NULL", (grant_id, project_id)).fetchone()
            if not row:
                raise KeyError("active grant not found")
            db.execute("UPDATE prime_core.mcp_grants SET revoked_at=now() WHERE grant_id=%s", (grant_id,))
        return self.issue_grant(project_id, client_id or row["client_id"])

    def call(self, token: str, tool: str, body: dict[str, Any]) -> dict[str, Any]:
        if tool not in CANONICAL_TOOLS:
            return {"error_code": "INVALID_INPUT", "message": "unknown MCP tool"}
        grant = self._grant(token)
        if not grant:
            return {"error_code": "PROJECT_SCOPE_VIOLATION", "message": "invalid or revoked MCP grant"}
        if tool not in grant["capabilities"]:
            return {"error_code": "PROJECT_SCOPE_VIOLATION", "message": "capability not granted"}
        project_id = grant["project_id"]
        if tool == "prime_memory_store":
            required = ("kind", "summary", "content")
            if any(not body.get(key) for key in required):
                return {"error_code": "INVALID_INPUT", "message": "kind, summary and content are required"}
            content_class = KIND_TO_CLASS.get(body["kind"], body["kind"].upper())
            if content_class not in set(KIND_TO_CLASS.values()):
                return {"error_code": "INVALID_INPUT", "message": "unknown memory kind"}
            working_context = body.get("working_context") or {}
            if not isinstance(working_context, dict):
                return {"error_code": "INVALID_INPUT", "message": "working_context must be an object"}
            source_refs = body.get("source_refs") or []
            if not isinstance(source_refs, list) or any(not isinstance(ref, str) or not ref for ref in source_refs):
                return {"error_code": "INVALID_INPUT", "message": "source_refs must be a list of non-empty strings"}
            salience = body.get("salience", "normal")
            if salience not in {"normal", "high", "critical"}:
                return {"error_code": "INVALID_INPUT", "message": "invalid salience"}
            confidence = body.get("confidence", 0.0)
            try:
                confidence = float(confidence)
            except (TypeError, ValueError):
                return {"error_code": "INVALID_INPUT", "message": "confidence must be between 0 and 1"}
            if not 0.0 <= confidence <= 1.0:
                return {"error_code": "INVALID_INPUT", "message": "confidence must be between 0 and 1"}
            supersedes_id = body.get("supersedes_id")
            supersession_reason = body.get("supersession_reason")
            if supersedes_id and not supersession_reason:
                return {"error_code": "INVALID_INPUT", "message": "supersession_reason is required when supersedes_id is supplied"}
            source_revision = working_context.get("git_commit")
            source_reference_id = source_refs[0] if source_refs else None
            branch_context = working_context.get("worktree_path_or_id") or working_context.get("git_ref")
            result = self.memory.store(
                project_id, body["content"], content_class,
                source_revision=source_revision, source_reference_id=source_reference_id,
                branch_context=branch_context, supersedes_memory_id=supersedes_id,
                correction_reason=supersession_reason,
                metadata={"summary": body["summary"], "source_refs": source_refs,
                          "salience": salience, "confidence": confidence,
                          "working_context": {key: working_context.get(key) for key in ("git_ref", "git_commit", "worktree_path_or_id") if working_context.get(key) is not None}},
            )
            provenance_refs = list(source_refs)
            provenance_refs.extend([f"project:{project_id}", f"client:{grant['client_id']}"])
            response = {"status": result.get("status", "degraded").lower(), "memory_id": result.get("memory_id"),
                        "hindsight_document_id": result.get("memory_id"), "durability_verified": result.get("status") == "STORED",
                        "provenance_refs": provenance_refs}
            if result.get("adapter_status") and result["adapter_status"] != "CURRENT":
                response["reason"] = result.get("adapter_status")
            return response
        if tool == "prime_memory_recall":
            return self.memory.recall(project_id, str(body.get("query", "")), min(int(body.get("max_results", 8)), 8))
        if tool == "prime_memory_timeline":
            return self._timeline(project_id, min(int(body.get("max_results", 50)), 50))
        if tool == "prime_memory_get":
            return self._get(project_id, str(body.get("memory_id", "")))
        if tool == "prime_memory_report_problem":
            return self._problem(project_id, grant["client_id"], body)
        return self._context(project_id, str(body.get("objective", "")), min(int(body.get("max_tokens", 6000)), 6000))

    def _grant(self, token: str) -> dict[str, Any] | None:
        with connect(self.settings) as db:
            row = db.execute("SELECT project_id,client_id,capabilities FROM prime_core.mcp_grants WHERE token_hash=%s AND revoked_at IS NULL AND expires_at>now()", (self.digest(token),)).fetchone()
            if not row:
                return None
            value = dict(row)
            if isinstance(value["capabilities"], str):
                value["capabilities"] = json.loads(value["capabilities"])
            return value

    def _timeline(self, project_id: str, limit: int) -> dict[str, Any]:
        with connect(self.settings) as db:
            rows = db.execute("SELECT memory_id,content_class,status,created_at,source_revision,source_reference_id,branch_context,metadata FROM prime_core.memory_records WHERE project_id=%s ORDER BY created_at DESC LIMIT %s", (project_id, limit)).fetchall()
            return {"project_id": project_id, "results": [dict(row) for row in rows]}

    def _get(self, project_id: str, memory_id: str) -> dict[str, Any]:
        with connect(self.settings) as db:
            row = db.execute("SELECT memory_id,project_id,content_class,status,content,source_revision,source_reference_id,branch_context,created_at,metadata FROM prime_core.memory_records WHERE project_id=%s AND memory_id=%s", (project_id, memory_id)).fetchone()
            return {"result": dict(row)} if row else {"error_code": "SOURCE_UNAVAILABLE", "message": "memory not found"}

    def _problem(self, project_id: str, client_id: str, body: dict[str, Any]) -> dict[str, Any]:
        with transaction(self.settings) as db:
            memory_id = str(body.get("memory_id", ""))
            if not db.execute("SELECT 1 FROM prime_core.memory_records WHERE project_id=%s AND memory_id=%s", (project_id, memory_id)).fetchone():
                return {"error_code": "SOURCE_UNAVAILABLE", "message": "memory not found"}
            db.execute("INSERT INTO prime_core.mcp_problem_reports(report_id,project_id,memory_id,problem,note,client_id,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)", (_id("problem"), project_id, memory_id, body.get("problem", "other"), body.get("note", ""), client_id, now()))
        return {"status": "reported", "memory_id": memory_id}

    def _context(self, project_id: str, objective: str, max_tokens: int) -> dict[str, Any]:
        recall = self.memory.recall(project_id, objective, 8)
        return {"project_id": project_id, "objective": objective, "max_tokens": max_tokens, "memory": recall.get("results", []), "authority_refs": [], "derived": True}

    @staticmethod
    def digest(value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()
