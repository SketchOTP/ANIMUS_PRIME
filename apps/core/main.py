from __future__ import annotations

import logging
import base64
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from typing import Any

from fastapi import Cookie, FastAPI, Header, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from src.prime_core.config import Settings
from src.prime_core.db import migrate, schema_version, connect
from src.prime_core.logging import configure
from src.prime_core.authority import validate_authority, provision_authority
from src.prime_core.indexer import RepositoryIndexer
from src.prime_core.memory_service import MemoryService
from src.prime_core.mcp_service import MCPService
from pathlib import Path
from src.prime_core.security import constant_time_equal
from src.prime_core.service import CoreService
from src.prime_core.remote_access_service import RemoteAccessSettings, TailscaleService
from src.prime_core.backup_service import BackupCoordinator, BackupError
from src.prime_core.reliability_service import ReliabilityService
from src.prime_core.history_service import HistoryService
from src.prime_core.intelligence_service import IntelligenceService
from src.prime_core.brain_service import BrainService

settings = Settings()
configure()
service = CoreService(settings)
indexer = RepositoryIndexer(service)
memory = MemoryService(settings)
mcp = MCPService(settings, memory)
remote_access = TailscaleService(RemoteAccessSettings(web_port=int(__import__("os").getenv("PRIME_WEB_PORT", "8000"))))
backups = BackupCoordinator()
history = HistoryService(settings)
intelligence = IntelligenceService(settings, memory)
brain = BrainService(settings)
startup_state: dict[str, Any] = {"database": "UNKNOWN", "migrations": "UNKNOWN"}
auth_failures: dict[str, list[float]] = defaultdict(list)


class Credentials(BaseModel):
    password: str = Field(min_length=1, max_length=256)


class Recovery(BaseModel):
    recovery_credential: str = Field(min_length=1, max_length=256)
    new_password: str = Field(min_length=12, max_length=256)


class JobRequest(BaseModel):
    job_type: str = Field(min_length=1, max_length=120)
    idempotency_key: str = Field(min_length=1, max_length=200)
    payload: dict[str, Any] = Field(default_factory=dict)


class EventRequest(BaseModel):
    event_type: str = Field(min_length=1, max_length=160)
    payload: dict[str, Any] = Field(default_factory=dict)
    dedupe_key: str | None = Field(default=None, max_length=240)


class ProjectRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class WorkflowRequest(BaseModel):
    workflow_type: str = Field(min_length=1, max_length=120)
    idempotency_key: str = Field(min_length=1, max_length=200)
    project_id: str | None = None


class NodeRequest(BaseModel):
    node_id: str = Field(min_length=1, max_length=160)
    name: str = Field(min_length=1, max_length=200)
    platform: str = Field(min_length=1, max_length=80)
    identity_fingerprint: str = Field(min_length=32, max_length=128)
    allowed_roots: list[str] = Field(default_factory=list)
    capabilities: dict[str, Any] = Field(default_factory=dict)


class RepositoryBindingRequest(BaseModel):
    project_id: str
    node_id: str
    identity_fingerprint: str
    canonical_path: str
    is_bare: bool = False


class GoalRequest(BaseModel):
    content: str = Field(min_length=1, max_length=200000)
    approve: bool = False


class AuthorityRequest(BaseModel):
    project_id: str
    source_path: str
    source_hash: str
    validation_status: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    content_snapshot: str | None = None
    canonical_commit: str | None = None


class MemoryRequest(BaseModel):
    content: str = Field(min_length=1, max_length=100000)
    content_class: str = Field(min_length=1, max_length=40)
    source_revision: str | None = None
    source_reference_id: str | None = None
    branch_context: str | None = None


class GrantRequest(BaseModel):
    client_id: str = Field(min_length=1, max_length=160)


class BackupRequest(BaseModel):
    destination: str = Field(min_length=1, max_length=4096)
    passphrase: str = Field(min_length=12, max_length=512)
    components: dict[str, Any] = Field(default_factory=dict)
    project_ids: list[str] = Field(default_factory=list)
    destination_class: str | None = Field(default=None, max_length=40)
    replace: bool = False
    safety_destination: str | None = None
    storage_root: str | None = None


class EvidenceUploadRequest(BaseModel):
    filename: str = Field(min_length=1, max_length=128)
    content_base64: str = Field(min_length=1, max_length=70_000_000)
    mime_type: str = Field(min_length=1, max_length=120)
    privacy_class: str = Field(default="PROJECT_PRIVATE", min_length=1, max_length=40)
    source_revision: str | None = None


class EvidenceReferenceRequest(BaseModel):
    source_type: str = Field(min_length=1, max_length=40)
    locator: str = Field(min_length=1, max_length=4096)
    privacy_class: str = Field(default="PROJECT_PRIVATE", min_length=1, max_length=40)
    source_revision: str | None = None


class EvidenceLinkRequest(BaseModel):
    evidence_id: str = Field(min_length=1, max_length=160)
    relation_type: str = Field(min_length=1, max_length=40)
    target_id: str = Field(min_length=1, max_length=240)


class EvidenceAnnotationRequest(BaseModel):
    annotation: str = Field(min_length=1, max_length=4000)


def error(code: str, message: str, request_id: str, retryable: bool = False, status_code: int = 400) -> JSONResponse:
    response = JSONResponse(status_code=status_code, content={
        "error_code": code, "message": message, "request_id": request_id, "retryable": retryable,
    })
    response.headers.update({
        "X-Request-ID": request_id,
        "Cache-Control": "no-store",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "no-referrer",
        "Content-Security-Policy": "default-src 'self'; frame-ancestors 'none'",
    })
    return response


def request_id(request: Request) -> str:
    return request.headers.get("X-Request-ID") or f"req_{uuid.uuid4().hex}"


def origin_allowed(request: Request) -> bool:
    origin = request.headers.get("origin")
    return not origin or origin in settings.allowed_origins


def client_allowed(client: str) -> bool:
    cutoff = time.time() - 300
    recent = [t for t in auth_failures[client] if t > cutoff]
    auth_failures[client] = recent
    return len(recent) < 10


def require_session(request: Request, token: str | None) -> dict[str, Any]:
    session = service.session(token) if token else None
    if not session:
        raise HTTPException(status_code=401, detail="authentication required")
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        csrf = request.headers.get("X-PRIME-CSRF")
        if not csrf or not constant_time_equal(csrf, request.cookies.get("prime_csrf", "")):
            raise HTTPException(status_code=403, detail="CSRF validation failed")
        if not constant_time_equal(__import__("src.prime_core.security", fromlist=["token_digest"]).token_digest(csrf), session["csrf_hash"]):
            raise HTTPException(status_code=403, detail="CSRF validation failed")
    return session


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        applied = migrate(settings)
        startup_state.update(database="CONNECTED", migrations=schema_version(settings), applied=applied)
    except Exception as exc:
        logging.getLogger("prime.core").warning("startup dependency degraded: %s", type(exc).__name__)
        startup_state.update(database="DEGRADED", migrations="UNKNOWN", error=type(exc).__name__)
    yield


app = FastAPI(title="ANIMUS PRIME Core", version="1.0.0-phase1", lifespan=lifespan)


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    rid = request_id(request)
    if request.method in {"POST", "PUT", "PATCH", "DELETE"} and not origin_allowed(request):
        return error("ORIGIN_REJECTED", "request origin is not allowed", rid, status_code=403)
    response = await call_next(request)
    response.headers.update({
        "X-Request-ID": rid,
        "Cache-Control": "no-store",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "no-referrer",
        "Content-Security-Policy": "default-src 'self'; frame-ancestors 'none'",
    })
    return response


@app.exception_handler(HTTPException)
async def http_error(request: Request, exc: HTTPException):
    return error("AUTHENTICATION_REQUIRED" if exc.status_code == 401 else "REQUEST_REJECTED", str(exc.detail), request_id(request), status_code=exc.status_code)


@app.get("/health/live")
def live():
    return {"status": "live", "service": "prime-core"}


@app.get("/health/ready")
def ready(request: Request):
    if startup_state.get("database") != "CONNECTED":
        return error("DEPENDENCY_DEGRADED", "canonical database is unavailable", request_id(request), retryable=True, status_code=503)
    return {"status": "ready", "schema_version": startup_state.get("migrations")}


@app.post("/v1/auth/bootstrap")
def bootstrap(body: Credentials, request: Request):
    try:
        return {"recovery_credential": service.bootstrap(body.password), "warning": "store this offline; it is shown once"}
    except ValueError as exc:
        return error("BOOTSTRAP_REJECTED", str(exc), request_id(request), status_code=409)


@app.post("/v1/auth/login")
def login(body: Credentials, request: Request, response: Response):
    client = request.client.host if request.client else "unknown"
    if not client_allowed(client):
        return error("AUTH_RATE_LIMITED", "too many authentication attempts", request_id(request), retryable=True, status_code=429)
    try:
        token, csrf = service.login(body.password)
    except PermissionError:
        auth_failures[client].append(time.time())
        return error("INVALID_CREDENTIALS", "invalid credentials", request_id(request), status_code=401)
    response.set_cookie("prime_session", token, httponly=True, secure=settings.cookie_secure, samesite="lax", max_age=settings.session_ttl_seconds, path="/")
    response.set_cookie("prime_csrf", csrf, httponly=False, secure=settings.cookie_secure, samesite="lax", max_age=settings.session_ttl_seconds, path="/")
    return {"authenticated": True, "actor_type": "operator", "csrf_token": csrf}


@app.post("/v1/auth/logout")
def logout(request: Request, response: Response, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    service.logout(prime_session or "")
    response.delete_cookie("prime_session", path="/")
    response.delete_cookie("prime_csrf", path="/")
    return {"authenticated": False}


@app.post("/v1/auth/recover")
def recover(body: Recovery, request: Request):
    try:
        replacement = service.recover(body.recovery_credential, body.new_password)
        return {"recovery_credential": replacement, "warning": "store this offline; it is shown once"}
    except PermissionError:
        return error("INVALID_RECOVERY_CREDENTIAL", "invalid recovery credential", request_id(request), status_code=401)
    except ValueError as exc:
        return error("RECOVERY_REJECTED", str(exc), request_id(request), status_code=400)


@app.get("/v1/core/status")
def core_status(request: Request, prime_session: str | None = Cookie(default=None)):
    session = require_session(request, prime_session)
    return {"service": "prime-core", "actor_id": session["operator_id"], "schema_version": startup_state.get("migrations"), "health": startup_state}


@app.post("/v1/jobs")
def create_job(body: JobRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    session = require_session(request, prime_session)
    return service.create_job(body.job_type, body.payload, body.idempotency_key)


@app.post("/v1/events")
def emit_event(body: EventRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    return service.emit_event(body.event_type, body.payload, dedupe_key=body.dedupe_key)


@app.post("/v1/projects")
def create_project(body: ProjectRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    return service.create_project(body.name)


@app.get("/v1/projects")
def list_projects(request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    return {"projects": service.list_projects()}


@app.post("/v1/workflows")
def create_workflow(body: WorkflowRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return service.create_workflow(body.workflow_type, body.idempotency_key, body.project_id)
    except KeyError as exc:
        return error("PROJECT_NOT_FOUND", str(exc), request_id(request), status_code=404)


@app.post("/v1/nodes")
def register_node(body: NodeRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    return service.register_node(body.node_id, body.name, body.platform, body.identity_fingerprint, body.allowed_roots, body.capabilities)


@app.get("/v1/nodes")
def list_nodes(request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    return {"nodes": service.list_nodes()}


@app.post("/v1/repositories/bind")
def bind_repository(body: RepositoryBindingRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return service.bind_repository(body.project_id, body.node_id, body.identity_fingerprint, body.canonical_path, body.is_bare)
    except (KeyError, ValueError) as exc:
        return error("BINDING_REJECTED", str(exc), request_id(request), status_code=400)


@app.post("/v1/projects/{project_id}/goal")
def create_goal(project_id: str, body: GoalRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return service.create_goal_revision(project_id, body.content, body.approve)
    except Exception as exc:
        return error("GOAL_REJECTED", type(exc).__name__, request_id(request), status_code=400)


@app.post("/v1/authority/revisions")
def record_authority(body: AuthorityRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    return service.record_authority_revision(body.project_id, body.source_path, body.source_hash, body.validation_status, body.metadata, body.content_snapshot, body.canonical_commit)


@app.post("/v1/projects/{project_id}/index")
def index_project(project_id: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return indexer.build(project_id)
    except (KeyError, ValueError, FileNotFoundError, OSError) as exc:
        return error("INDEX_REJECTED", str(exc), request_id(request), retryable=True, status_code=400)


@app.get("/v1/projects/{project_id}/search")
def search_project(project_id: str, q: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    return {"project_id": project_id, "results": indexer.search(project_id, q)}


@app.post("/v1/projects/{project_id}/memory")
def store_memory(project_id: str, body: MemoryRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    return memory.store(project_id, body.content, body.content_class, body.source_revision, body.source_reference_id, body.branch_context)


@app.get("/v1/projects/{project_id}/memory")
def recall_memory(project_id: str, q: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    return memory.recall(project_id, q)


@app.get("/v1/projects/{project_id}/evidence")
def list_project_evidence(project_id: str, request: Request, include_retracted: bool = False, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    return {"project_id": project_id, "evidence": history.list_evidence(project_id, include_retracted)}


@app.post("/v1/projects/{project_id}/evidence")
def upload_project_evidence(project_id: str, body: EvidenceUploadRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        content = base64.b64decode(body.content_base64, validate=True)
        return history.store_uploaded_evidence(project_id, body.filename, content, body.mime_type, body.privacy_class, body.source_revision)
    except (ValueError, OSError) as exc:
        return error("EVIDENCE_REJECTED", str(exc), request_id(request), status_code=400)


@app.post("/v1/projects/{project_id}/evidence/reference")
def reference_project_evidence(project_id: str, body: EvidenceReferenceRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return history.record_evidence(project_id, body.source_type, body.locator, privacy_class=body.privacy_class, source_revision=body.source_revision)
    except ValueError as exc:
        return error("EVIDENCE_REJECTED", str(exc), request_id(request), status_code=400)


@app.get("/v1/projects/{project_id}/evidence/{evidence_id}")
def retrieve_project_evidence(project_id: str, evidence_id: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        result = history.retrieve_evidence(project_id, evidence_id)
        result.pop("content", None)
        return result
    except KeyError as exc:
        return error("EVIDENCE_NOT_FOUND", str(exc), request_id(request), status_code=404)


@app.post("/v1/projects/{project_id}/evidence/{evidence_id}/reindex")
def reindex_project_evidence(project_id: str, evidence_id: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return history.reindex_evidence(project_id, evidence_id)
    except KeyError as exc:
        return error("EVIDENCE_NOT_FOUND", str(exc), request_id(request), status_code=404)


@app.delete("/v1/projects/{project_id}/evidence/{evidence_id}")
def retract_project_evidence(project_id: str, evidence_id: str, reason: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return history.retract_evidence(project_id, evidence_id, reason)
    except (KeyError, ValueError) as exc:
        return error("EVIDENCE_RETRACTION_REJECTED", str(exc), request_id(request), status_code=404 if isinstance(exc, KeyError) else 400)


@app.post("/v1/projects/{project_id}/evidence/{evidence_id}/links")
def link_project_evidence(project_id: str, evidence_id: str, body: EvidenceLinkRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        if body.evidence_id != evidence_id:
            raise ValueError("Evidence path and body IDs must match")
        return history.link_evidence(project_id, evidence_id, body.relation_type, body.target_id)
    except (KeyError, ValueError) as exc:
        return error("EVIDENCE_LINK_REJECTED", str(exc), request_id(request), status_code=404 if isinstance(exc, KeyError) else 400)


@app.post("/v1/projects/{project_id}/evidence/{evidence_id}/annotations")
def annotate_project_evidence(project_id: str, evidence_id: str, body: EvidenceAnnotationRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return history.annotate_evidence(project_id, evidence_id, body.annotation)
    except (KeyError, ValueError) as exc:
        return error("EVIDENCE_ANNOTATION_REJECTED", str(exc), request_id(request), status_code=404 if isinstance(exc, KeyError) else 400)


@app.get("/v1/projects/{project_id}/time-lens/state")
def time_lens_state(project_id: str, as_of: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return history.time_lens(project_id, as_of)
    except ValueError as exc:
        return error("TIME_LENS_REJECTED", str(exc), request_id(request), status_code=400)


@app.get("/v1/projects/{project_id}/time-lens/now")
def time_lens_now(project_id: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    return history.return_to_now(project_id)


@app.get("/v1/projects/{project_id}/time-lens/brain")
def time_lens_brain(project_id: str, as_of: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    return brain.build_historical(project_id, as_of)


@app.post("/v1/projects/{project_id}/time-lens/ask")
def time_lens_ask(project_id: str, as_of: str, question: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return intelligence.ask_at(project_id, question, as_of)
    except ValueError as exc:
        return error("TIME_LENS_ASK_REJECTED", str(exc), request_id(request), status_code=400)


@app.post("/v1/projects/{project_id}/mcp/grants")
def issue_mcp_grant(project_id: str, body: GrantRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return mcp.issue_grant(project_id, body.client_id)
    except KeyError as exc:
        return error("PROJECT_NOT_FOUND", str(exc), request_id(request), status_code=404)


@app.post("/v1/mcp/{tool}")
def mcp_tool(tool: str, body: dict[str, Any], authorization: str | None = Header(default=None)):
    token = authorization[7:] if authorization and authorization.startswith("Bearer ") else ""
    return mcp.call(token, tool, body)


@app.get("/v1/system/remote-access")
def remote_access_status(request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    return remote_access.status()


@app.post("/v1/system/remote-access/tailscale/configure")
def configure_remote_access(request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return remote_access.configure_serve()
    except PermissionError as exc:
        return error("REMOTE_ACCESS_REFUSED", str(exc), request_id(request), status_code=409)


@app.post("/v1/system/remote-access/tailscale/disable")
def disable_remote_access(request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    return remote_access.disable()


@app.post("/v1/backups")
def create_backup(body: BackupRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        if body.components:
            return backups.build_bundle(Path(body.destination), body.components, body.passphrase, destination_class=body.destination_class)
        return backups.create_continuity_backup(settings, Path(body.destination), body.passphrase, project_ids=body.project_ids or None, destination_class=body.destination_class)
    except (BackupError, OSError, ValueError) as exc:
        return error("BACKUP_REJECTED", str(exc), request_id(request), retryable=True, status_code=400)


@app.post("/v1/backups/preflight")
def backup_preflight(body: BackupRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return backups.preflight_restore(Path(body.destination), body.passphrase)
    except (BackupError, OSError, ValueError) as exc:
        return error("RESTORE_PREFLIGHT_REJECTED", str(exc), request_id(request), status_code=400)


@app.post("/v1/backups/restore")
def restore_backup(body: BackupRequest, request: Request, prime_session: str | None = Cookie(default=None), step_up: str | None = Header(default=None, alias="X-PRIME-STEP-UP")):
    require_session(request, prime_session)
    if not body.replace and step_up != "CONFIRM":
        return error("RESTORE_STEP_UP_REQUIRED", "restore requires step-up confirmation", request_id(request), status_code=403)
    try:
        return backups.restore_bundle(
            settings,
            Path(body.destination),
            body.passphrase,
            replace=body.replace,
            safety_destination=Path(body.safety_destination) if body.safety_destination else None,
            storage_root=Path(body.storage_root) if body.storage_root else None,
        )
    except (BackupError, OSError, ValueError) as exc:
        return error("RESTORE_REJECTED", str(exc), request_id(request), retryable=False, status_code=409)


@app.get("/v1/system/reliability")
def reliability_status(request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    return ReliabilityService(settings).diagnostics()
