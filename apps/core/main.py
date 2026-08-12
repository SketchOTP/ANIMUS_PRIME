from __future__ import annotations

import logging
import base64
import hashlib
import json
import secrets
import subprocess
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from typing import Any

from fastapi import Cookie, FastAPI, Header, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, JSONResponse
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
from src.prime_core.progress_service import ProgressService
from src.prime_core.notion_credentials import NotionCredentialRegistry, KNOWN_GRANTED_PAGE
from src.prime_core.notion_service import NotionApiProvider, NotionLifecycleService
from src.prime_core.ai_service import AIExecutionService

settings = Settings()
configure()
service = CoreService(settings)
indexer = RepositoryIndexer(service)
memory = MemoryService(settings)
mcp = MCPService(settings, memory)
remote_access = TailscaleService(RemoteAccessSettings(
    web_port=int(__import__("os").getenv("PRIME_WEB_PORT", "8000")),
    web_host=__import__("os").getenv("PRIME_WEB_HOST", "127.0.0.1"),
    state_path=Path(__import__("os").getenv("PRIME_REMOTE_ACCESS_STATE_PATH", "var/remote-access.json")),
))
backups = BackupCoordinator()
history = HistoryService(settings)
intelligence = IntelligenceService(settings, memory)
ai = AIExecutionService(settings)
brain = BrainService(settings)
progress = ProgressService(settings)
notion_credentials = NotionCredentialRegistry(Path(settings.notion_credential_state_path))
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
    description: str = Field(default="", max_length=4000)
    image_url: str | None = Field(default=None, max_length=2048)


class ProjectMetadataRequest(ProjectRequest):
    pass


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


class RepositoryInspectRequest(BaseModel):
    node_id: str = Field(min_length=1, max_length=160)
    path: str = Field(min_length=1, max_length=4096)


class RepositoryCreateRequest(BaseModel):
    node_id: str = Field(min_length=1, max_length=160)
    parent_path: str = Field(min_length=1, max_length=4096)
    repository_name: str = Field(min_length=1, max_length=160)
    confirm: bool = False


class AuthorityBootstrapRequest(BaseModel):
    confirm: bool = False


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


class AIExecutionRequest(BaseModel):
    function: str = Field(min_length=1, max_length=80)
    prompt_input: dict[str, Any] = Field(default_factory=dict)
    sources: list[dict[str, Any]] = Field(default_factory=list, max_length=32)
    privacy_mode: str | None = Field(default=None, max_length=40)


class ProductAIRequest(AIExecutionRequest):
    source_revision: str = Field(default="product-current", min_length=1, max_length=240)
    source_rank: int = Field(default=0, ge=0, le=2_147_483_647)
    project_notion_parent_id: str | None = Field(default=None, max_length=80)


class GrantRequest(BaseModel):
    client_id: str = Field(min_length=1, max_length=160)


class ForkRequest(BaseModel):
    source_revision: str = Field(min_length=7, max_length=200)
    destination_node_id: str = Field(min_length=1, max_length=160)
    parent_path: str = Field(min_length=1, max_length=4096)
    repository_name: str = Field(min_length=1, max_length=160)
    confirm: bool = False


class BaselineRequest(BaseModel):
    goal_revision_id: str = Field(min_length=1, max_length=160)
    items: list[dict[str, Any]] = Field(min_length=1, max_length=128)


class AssessmentRequest(BaseModel):
    goal_revision_id: str = Field(min_length=1, max_length=160)
    results: list[dict[str, Any]] = Field(min_length=1, max_length=128)
    repository_revision: str | None = Field(default=None, max_length=240)
    summary: str = Field(default="", max_length=4000)
    evidence_refs: list[str] = Field(default_factory=list, max_length=128)


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


class NotionCapabilityRequest(BaseModel):
    page_id: str = Field(default=KNOWN_GRANTED_PAGE, min_length=1, max_length=80)
    write_probe: bool = False
    probe_parent_id: str | None = Field(default=None, max_length=80)


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


def project_exists(project_id: str) -> bool:
    with connect(settings) as db:
        return db.execute("SELECT 1 FROM prime_core.projects WHERE project_id=%s", (project_id,)).fetchone() is not None


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


@app.get("/", include_in_schema=False)
def web_shell(request: Request) -> HTMLResponse:
    nonce = getattr(request.state, "csp_nonce", "")
    markup = (Path(__file__).parents[1] / "web" / "index.html").read_text(encoding="utf-8")
    markup = markup.replace("<style>", f'<style nonce="{nonce}">', 1)
    markup = markup.replace("<script>", f'<script nonce="{nonce}">', 1)
    return HTMLResponse(markup, headers={"Cache-Control": "no-store"})


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    rid = request_id(request)
    request.state.csp_nonce = secrets.token_urlsafe(18)
    if request.method in {"POST", "PUT", "PATCH", "DELETE"} and not origin_allowed(request):
        return error("ORIGIN_REJECTED", "request origin is not allowed", rid, status_code=403)
    response = await call_next(request)
    response.headers.update({
        "X-Request-ID": rid,
        "Cache-Control": "no-store",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "no-referrer",
        "Content-Security-Policy": (
            "default-src 'self'; "
            f"script-src 'self' 'nonce-{request.state.csp_nonce}'; "
            f"style-src 'self' 'nonce-{request.state.csp_nonce}'; "
            "object-src 'none'; base-uri 'self'; frame-ancestors 'none'"
        ),
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


@app.get("/v1/system/setup")
def setup_status(request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    nodes = service.list_nodes()
    notion = notion_credentials.public_status()
    return {
        "steps": {
            "operator_security": {"status": "READY", "detail": "Operator session is authenticated; credentials remain server-side."},
            "storage": {"status": "READY" if startup_state.get("database") == "CONNECTED" else "DEGRADED", "detail": "PostgreSQL/Core is the canonical persistence layer."},
            "ai_provider": {"status": "READY" if ai.default_provider != "unconfigured" else "DEGRADED", "detail": "Provider health is reported without exposing credential material."},
            "notion": {"status": notion.get("status", "NOT_CONFIGURED"), "detail": "Notion is optional and cannot block canonical project state."},
            "hindsight": {"status": "DEGRADED", "detail": "PRIME source-ledger memory remains available; approved Hindsight retain is not qualified in this environment."},
            "nodes": {"status": "READY" if nodes else "REQUIRES_ACTION", "detail": f"{len(nodes)} enrolled Node record(s)."},
            "allowed_roots": {"status": "READY" if any(node.get("allowed_roots") for node in nodes) else "REQUIRES_ACTION", "detail": "Repository operations are constrained to enrolled Node roots."},
            "backup": {"status": "REQUIRES_ACTION", "detail": "Configure and verify a recovery destination before release."},
            "system_health": {"status": "READY" if startup_state.get("database") == "CONNECTED" else "DEGRADED", "detail": "Core readiness and schema migration state."},
            "first_project": {"status": "READY" if service.list_projects() else "REQUIRES_ACTION", "detail": "Create or register one real Git-backed project."},
        },
        "resume": {"supported": True, "durable": True, "instruction": "Reopen this endpoint after restart; project onboarding state is stored in Core."},
    }


@app.get("/v1/system/ai/profiles")
def ai_profiles(request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    return {
        "status": "HEALTHY" if ai.default_provider != "unconfigured" else "DEGRADED",
        "provider_configured": ai.default_provider != "unconfigured",
        "profiles": ai.public_profiles(),
        "fallback_policy": "NONE_UNLESS_EXPLICIT_PROFILE",
        "credential_policy": "CORE_ONLY",
    }


@app.post("/v1/projects/{project_id}/ai/execute")
def execute_ai(project_id: str, body: AIExecutionRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return ai.execute(project_id, body.function, body.prompt_input, body.sources, project_privacy_mode=body.privacy_mode)
    except (KeyError, ValueError) as exc:
        return error("AI_EXECUTION_REJECTED", str(exc), request_id(request), status_code=400)


def _live_notion_lifecycle() -> NotionLifecycleService:
    """Resolve the approved Notion credential only for an explicit product write."""
    client = notion_credentials.client()
    return NotionLifecycleService(
        NotionApiProvider(client),
        state_path=Path(settings.notion_credential_state_path).with_name("notion-lifecycle-state.json"),
        settings=settings,
    )


@app.post("/v1/projects/{project_id}/ai/product")
def execute_product_ai(project_id: str, body: ProductAIRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        notion = _live_notion_lifecycle() if body.function.upper() == "DOCUMENTATION" and body.project_notion_parent_id else None
        if notion is not None and not notion.projects.get(project_id, None):
            notion.configure(project_id, "env/myassistant/notion-readonly")
            notion.create_project_record(project_id, body.project_notion_parent_id or "", f"PRIME Project {project_id}")
        return intelligence.execute_product(project_id, body.function, body.prompt_input, body.sources, notion=notion, source_revision=body.source_revision, source_rank=body.source_rank)
    except (KeyError, LookupError, ValueError) as exc:
        return error("PRODUCT_AI_REJECTED", str(exc), request_id(request), status_code=400)


@app.get("/v1/operator/state")
def operator_state(request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        projects = service.list_projects()
    except Exception:
        projects = []
    try:
        nodes = service.list_nodes()
    except Exception:
        nodes = []
    try:
        remote = remote_access.reconcile()
    except Exception as exc:
        remote = {"status": "DEGRADED", "error_code": type(exc).__name__}
    try:
        reliability = ReliabilityService(settings).diagnostics()
    except Exception as exc:
        reliability = {"status": "DEGRADED", "error_code": type(exc).__name__}
    return {
        "service": "prime-core",
        "startup": dict(startup_state),
        "projects": projects,
        "nodes": nodes,
        "notion": notion_credentials.public_status(),
        "ai": {
            "status": "HEALTHY" if ai.default_provider != "unconfigured" else "DEGRADED",
            "provider_configured": ai.default_provider != "unconfigured",
            "profiles": ai.public_profiles(),
            "fallback_policy": "NONE_UNLESS_EXPLICIT_PROFILE",
        },
        "remote_access": remote,
        "reliability": reliability,
        "operator_surfaces": {"state_vocabulary": ["LOADING", "EMPTY", "HEALTHY", "STALE", "DEGRADED", "OFFLINE", "ERROR", "NEEDS_ATTENTION"]},
    }


@app.post("/v1/system/notion/credential-import")
def notion_credential_import(request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    result = notion_credentials.import_myassistant()
    capability: dict[str, Any] | None = None
    if result.source_present and result.status in {"IMPORTED", "NOOP"}:
        try:
            capability = notion_credentials.client().capability_test(settings.notion_granted_page_id)
            notion_credentials.record_capabilities(capability)
        except Exception as exc:
            # The migration remains recorded even when the provider is down;
            # capability truth is surfaced separately and never inferred.
            capability = {"status": "DEGRADED", "error_code": type(exc).__name__}
    return {"migration": result.public(), "capability": capability, "notion": notion_credentials.public_status()}


@app.get("/v1/system/notion/status")
def notion_status(request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    return notion_credentials.public_status()


@app.post("/v1/system/notion/capability-test")
def notion_capability_test(body: NotionCapabilityRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        result = notion_credentials.client().capability_test(body.page_id, body.write_probe, body.probe_parent_id)
        return {"capability": notion_credentials.record_capabilities(result)}
    except LookupError as exc:
        return error("NOTION_CREDENTIAL_UNAVAILABLE", str(exc), request_id(request), retryable=True, status_code=503)
    except Exception as exc:
        from src.prime_core.notion_api import NotionApiError
        if isinstance(exc, NotionApiError):
            status_code = 401 if exc.status == 401 else 403 if exc.status == 403 else 503
            notion_credentials.record_capabilities({
                "status": "REAUTH_REQUIRED" if exc.status == 401 else "ACCESS_LOST" if exc.status == 403 else "DEGRADED",
                "page_id": body.page_id,
                "page_read": False,
                "block_read": False,
                "page_write": "NOT_TESTED",
                "managed_write": "NOT_TESTED",
            })
            return error("NOTION_CAPABILITY_FAILED", "Notion capability test failed", request_id(request), retryable=exc.retryable, status_code=status_code)
        return error("NOTION_CAPABILITY_FAILED", type(exc).__name__, request_id(request), retryable=True, status_code=503)


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
    return service.create_project(body.name, body.description, body.image_url)


@app.patch("/v1/projects/{project_id}")
def update_project(project_id: str, body: ProjectMetadataRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return service.update_project_metadata(project_id, body.name, body.description, body.image_url)
    except KeyError as exc:
        return error("PROJECT_NOT_FOUND", str(exc), request_id(request), status_code=404)


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


@app.post("/v1/projects/{project_id}/repositories/inspect")
def inspect_repository_for_onboarding(project_id: str, body: RepositoryInspectRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return service.inspect_repository_for_onboarding(project_id, body.node_id, body.path)
    except KeyError as exc:
        return error("ONBOARDING_NOT_FOUND", str(exc), request_id(request), status_code=404)
    except (PermissionError, ValueError, FileNotFoundError, OSError) as exc:
        return error("REPOSITORY_INSPECTION_REJECTED", str(exc), request_id(request), status_code=400)


@app.post("/v1/projects/{project_id}/repositories/register")
def register_existing_repository(project_id: str, body: RepositoryInspectRequest, request: Request, prime_session: str | None = Cookie(default=None), confirm: bool = False):
    require_session(request, prime_session)
    try:
        inspection = service.inspect_repository_for_onboarding(project_id, body.node_id, body.path)
        return {"inspection": inspection, "binding": service.bind_verified_repository(inspection, confirm=confirm)}
    except KeyError as exc:
        return error("ONBOARDING_NOT_FOUND", str(exc), request_id(request), status_code=404)
    except (PermissionError, ValueError, FileNotFoundError, FileExistsError, OSError) as exc:
        return error("REPOSITORY_REGISTRATION_REJECTED", str(exc), request_id(request), status_code=400)


@app.post("/v1/projects/{project_id}/repositories/create")
def create_repository_for_onboarding(project_id: str, body: RepositoryCreateRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return service.create_repository_for_onboarding(project_id, body.node_id, body.parent_path, body.repository_name, body.confirm)
    except KeyError as exc:
        return error("ONBOARDING_NOT_FOUND", str(exc), request_id(request), status_code=404)
    except (PermissionError, ValueError, FileNotFoundError, FileExistsError, OSError) as exc:
        return error("REPOSITORY_CREATION_REJECTED", str(exc), request_id(request), status_code=400)


@app.post("/v1/projects/{project_id}/authority/bootstrap")
def bootstrap_project_authority(project_id: str, body: AuthorityBootstrapRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return service.bootstrap_project_authority(project_id, body.confirm)
    except (PermissionError, ValueError, FileNotFoundError, FileExistsError, OSError) as exc:
        return error("AUTHORITY_BOOTSTRAP_REJECTED", str(exc), request_id(request), status_code=400)


@app.post("/v1/projects/{project_id}/authority/{decision}")
def review_or_adopt_project_authority(project_id: str, decision: str, body: AuthorityBootstrapRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return service.review_or_adopt_project_authority(project_id, decision.upper(), body.confirm)
    except (PermissionError, ValueError, FileNotFoundError, OSError) as exc:
        return error("AUTHORITY_DECISION_REJECTED", str(exc), request_id(request), status_code=400)


@app.get("/v1/projects/{project_id}/onboarding")
def project_onboarding_state(project_id: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        snapshot = _project_snapshot(project_id)
        project = snapshot["project"]
        return {"project_id": project_id, "step": project.get("onboarding_step", "UNKNOWN"), "state": project.get("onboarding_state", "UNKNOWN"), "lifecycle": project.get("lifecycle_state"), "binding": bool(snapshot.get("binding")), "authority": (snapshot.get("authority") or {}).get("validation_status", "UNKNOWN"), "goal": (snapshot.get("goal") or {}).get("status", "UNKNOWN"), "next": "REPOSITORY" if not snapshot.get("binding") else "AUTHORITY" if not snapshot.get("authority") else "GOAL" if not snapshot.get("goal") or snapshot["goal"].get("status") != "APPROVED" else "INDEX_AND_BASELINE"}
    except KeyError:
        return error("PROJECT_NOT_FOUND", "project not found", request_id(request), status_code=404)


@app.post("/v1/projects/{project_id}/goal")
def create_goal(project_id: str, body: GoalRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return service.create_goal_revision(project_id, body.content, body.approve)
    except Exception as exc:
        return error("GOAL_REJECTED", type(exc).__name__, request_id(request), status_code=400)


@app.post("/v1/projects/{project_id}/progress/baseline")
def propose_progress_baseline(project_id: str, body: BaselineRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return progress.propose_baseline(project_id, body.goal_revision_id, body.items)
    except (KeyError, ValueError) as exc:
        return error("BASELINE_REJECTED", str(exc), request_id(request), status_code=400)


@app.post("/v1/projects/{project_id}/progress/baseline/{review_id}/approve")
def approve_progress_baseline(project_id: str, review_id: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        result = progress.approve_baseline(review_id)
        if result.get("project_id") not in (None, project_id):
            return error("BASELINE_REJECTED", "baseline does not belong to project", request_id(request), status_code=400)
        return result
    except (KeyError, ValueError) as exc:
        return error("BASELINE_REJECTED", str(exc), request_id(request), status_code=400)


@app.post("/v1/projects/{project_id}/progress/assess")
def assess_project_progress(project_id: str, body: AssessmentRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return progress.assess(project_id, body.goal_revision_id, body.results, body.repository_revision, body.summary, body.evidence_refs)
    except (KeyError, ValueError) as exc:
        return error("PROGRESS_REJECTED", str(exc), request_id(request), status_code=400)


@app.get("/v1/projects/{project_id}/progress")
def project_progress(project_id: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    if not project_exists(project_id):
        return error("PROJECT_NOT_FOUND", "project not found", request_id(request), status_code=404)
    return progress.snapshot(project_id)


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
    if not project_exists(project_id):
        return error("PROJECT_NOT_FOUND", "project not found", request_id(request), status_code=404)
    grouped = intelligence.search(project_id, q)
    results = []
    for group, rows in grouped["groups"].items():
        results.extend([{**row, "result_group": group} for row in rows])
    return {"project_id": project_id, "results": results, "groups": grouped["groups"]}


def _repository_binding(project_id: str) -> dict[str, Any] | None:
    with connect(settings) as db:
        row = db.execute(
            "SELECT b.repository_id,b.canonical_revision,r.canonical_path,r.identity_fingerprint,n.node_id,n.name AS node_name,n.status AS node_status "
            "FROM prime_core.project_bindings b JOIN prime_core.repositories r ON r.repository_id=b.repository_id "
            "JOIN prime_core.nodes n ON n.node_id=b.node_id WHERE b.project_id=%s",
            (project_id,),
        ).fetchone()
    return dict(row) if row else None


def _safe_repository_path(project_id: str, relative_path: str = "") -> tuple[Path, Path]:
    binding = _repository_binding(project_id)
    if not binding:
        raise KeyError("project has no repository binding")
    root = Path(binding["canonical_path"]).expanduser().resolve(strict=True)
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError("repository path escapes the canonical repository root") from exc
    return root, candidate


def _git(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True, timeout=8)
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return "UNAVAILABLE"
    return result.stdout.strip() or "UNKNOWN"


def _git_state(project_id: str) -> dict[str, Any]:
    try:
        root, _ = _safe_repository_path(project_id)
    except (KeyError, OSError, ValueError):
        return {"status": "UNAVAILABLE", "repository_path": "UNKNOWN"}
    worktree_lines = _git(root, "worktree", "list", "--porcelain")
    worktrees: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in worktree_lines.splitlines():
        if not line.strip():
            if current:
                worktrees.append(current)
                current = {}
            continue
        key, _, value = line.partition(" ")
        if key == "worktree":
            current["path"] = value
        elif key == "HEAD":
            current["revision"] = value
        elif key == "branch":
            current["branch"] = value.removeprefix("refs/heads/")
        elif key == "detached":
            current["branch"] = "DETACHED"
    if current:
        worktrees.append(current)
    recent = []
    log_output = _git(root, "log", "-8", "--format=%H%x1f%h%x1f%ad%x1f%s", "--date=iso-strict")
    for line in log_output.splitlines():
        parts = line.split("\x1f", 3)
        if len(parts) == 4:
            recent.append({"revision": parts[0], "short_revision": parts[1], "timestamp": parts[2], "summary": parts[3]})
    canonical_revision = _git(root, "rev-parse", "HEAD")
    if canonical_revision == "UNAVAILABLE" and _git(root, "rev-parse", "--is-inside-work-tree") == "true":
        canonical_revision = "UNBORN"
    return {
        "status": "CURRENT" if _git(root, "status", "--porcelain") == "UNKNOWN" else "AVAILABLE",
        "repository_path": str(root),
        "canonical_revision": canonical_revision,
        "branch": _git(root, "branch", "--show-current") or "DETACHED",
        "dirty": bool(_git(root, "status", "--porcelain") not in {"", "UNKNOWN", "UNAVAILABLE"}),
        "worktrees": worktrees,
        "recent_commits": recent,
    }


def _project_context(project_id: str) -> dict[str, Any]:
    snapshot = _project_snapshot(project_id)
    binding = snapshot.get("binding") or {}
    git_state = _git_state(project_id)
    generated_at = time.time()
    with connect(settings) as db:
        goal = db.execute(
            "SELECT goal_revision_id,revision_number,content,content_hash,status,created_at,approved_at FROM prime_core.goal_revisions "
            "WHERE project_id=%s ORDER BY revision_number DESC LIMIT 1", (project_id,),
        ).fetchone()
        progress_history = [dict(row) for row in db.execute(
            "SELECT assessment_id,goal_revision_id,repository_revision,progress_percent,confidence,freshness_state,summary,evidence_refs,created_at "
            "FROM prime_core.progress_assessments WHERE project_id=%s ORDER BY created_at DESC LIMIT 12", (project_id,),
        ).fetchall()]
        authority_history = [dict(row) for row in db.execute(
            "SELECT authority_revision_id,source_path,source_hash,contract_version,validation_status,observed_at,metadata,content_snapshot,canonical_commit "
            "FROM prime_core.authority_revisions WHERE project_id=%s ORDER BY observed_at DESC LIMIT 8", (project_id,),
        ).fetchall()]
        memory_rows = [dict(row) for row in db.execute(
            "SELECT memory_id,content_class,content,status,source_revision,source_reference_id,branch_context,created_at,supersedes_memory_id "
            "FROM prime_core.memory_records WHERE project_id=%s ORDER BY created_at DESC LIMIT 16", (project_id,),
        ).fetchall()]
        evidence_rows = [dict(row) for row in db.execute(
            "SELECT evidence_id,source_type,locator,source_reference_id,source_revision,content_hash,privacy_class,parser_status,index_status,captured_at "
            "FROM prime_core.evidence_records WHERE project_id=%s AND retracted_at IS NULL AND purged_at IS NULL ORDER BY captured_at DESC LIMIT 16", (project_id,),
        ).fetchall()]
        notion_sources = [dict(row) for row in db.execute(
            "SELECT page_id,page_url,access_mode,status,observed_revision,observed_hash,observed_at,metadata FROM prime_core.notion_knowledge_sources WHERE project_id=%s ORDER BY observed_at DESC NULLS LAST LIMIT 12", (project_id,),
        ).fetchall()]
        ai_runs = [dict(row) for row in db.execute(
            "SELECT run_id,function,provider,model,profile_revision,prompt_revision,schema_revision,privacy_mode,source_revision_set,status,error_class,created_at "
            "FROM prime_core.ai_runs WHERE project_id=%s ORDER BY created_at DESC LIMIT 8", (project_id,),
        ).fetchall()]
        grants = [dict(row) for row in db.execute(
            "SELECT grant_id,client_id,capabilities,created_at,expires_at,revoked_at FROM prime_core.mcp_grants WHERE project_id=%s ORDER BY created_at DESC LIMIT 8", (project_id,),
        ).fetchall()]
        checkpoints = [dict(row) for row in db.execute(
            "SELECT checkpoint_id,commit_id,coverage_status,content_hash,captured_at,metadata FROM prime_core.git_history_checkpoints WHERE project_id=%s ORDER BY captured_at DESC LIMIT 8", (project_id,),
        ).fetchall()]
    authority_files: dict[str, dict[str, str]] = {}
    try:
        root, _ = _safe_repository_path(project_id)
        for name in ("PROJECT_GOAL.md", ".agent/CURRENT.md", ".agent/DIRECTIVES.md", ".agent/OUTCOMES.md", ".agent/LEARNINGS.md", ".agent/RECORD.md"):
            path = root / name
            if path.is_file() and path.stat().st_size <= 40_000:
                content = path.read_text(encoding="utf-8", errors="replace")
                authority_files[name] = {"sha256": hashlib.sha256(content.encode()).hexdigest(), "content": content}
    except (KeyError, OSError, ValueError):
        pass
    provenance = [
        {"claim": "project_identity", "source_class": "PRIME_CORE", "reference": f"prime_core.projects:{project_id}", "revision": snapshot["project"].get("updated_at")},
        {"claim": "repository_identity", "source_class": "GIT", "reference": git_state.get("repository_path", "UNKNOWN"), "revision": git_state.get("canonical_revision", "UNKNOWN")},
        {"claim": "approved_goal", "source_class": "PRIME_CORE_GOAL_REVISION", "reference": (goal or {}).get("goal_revision_id", "UNKNOWN"), "revision": (goal or {}).get("content_hash", "UNKNOWN")},
        {"claim": "authority_health", "source_class": "PRIME_CORE_AUTHORITY_REVISION", "reference": (snapshot.get("authority") or {}).get("authority_revision_id", "UNKNOWN"), "revision": (snapshot.get("authority") or {}).get("source_hash", "UNKNOWN")},
        {"claim": "progress", "source_class": "PRIME_CORE_PROGRESS", "reference": (snapshot.get("progress") or {}).get("assessment_id", "UNKNOWN"), "revision": (snapshot.get("progress") or {}).get("repository_revision", "UNKNOWN")},
        {"claim": "activity", "source_class": "PRIME_CORE_ACTIVITY", "reference": f"prime_core.events:{project_id}", "revision": git_state.get("canonical_revision", "UNKNOWN")},
    ]
    return {
        "schema": "prime.project-context.v1",
        "generated_at": generated_at,
        "project": snapshot["project"],
        "repository": {**binding, "git": git_state, "checkpoint_history": checkpoints},
        "goal": {"revision": dict(goal) if goal else None, "items": snapshot.get("goal_items", []), "history": progress_history},
        "current_work": {"authority": authority_files.get(".agent/CURRENT.md"), "directives": authority_files.get(".agent/DIRECTIVES.md")},
        "authority": {"latest": snapshot.get("authority"), "history": authority_history, "files": authority_files},
        "status": {"progress": snapshot.get("progress"), "progress_history": progress_history, "attention": snapshot.get("attention", []), "alignment": "UNKNOWN", "milestones": "UNKNOWN"},
        "continuity": {"notion": snapshot.get("notion"), "memory": snapshot.get("memory"), "evidence": snapshot.get("evidence"), "ai_runs": ai_runs, "mcp_grants": grants},
        "memory": memory_rows,
        "evidence": evidence_rows,
        "activity": snapshot.get("events", []),
        "sources": {"authority": authority_files, "notion": notion_sources},
        "provenance": provenance,
        "freshness": {"project": snapshot["project"].get("freshness_state", "UNKNOWN"), "repository": git_state.get("canonical_revision", "UNKNOWN"), "generated_at": generated_at},
        "redaction": {"credentials": "OMITTED", "session_tokens": "OMITTED", "authorization_headers": "OMITTED", "chain_of_thought": "OMITTED"},
    }


def _context_markdown(context: dict[str, Any]) -> str:
    project = context.get("project") or {}
    repository = context.get("repository") or {}
    git = repository.get("git") or {}
    goal = (context.get("goal") or {}).get("revision") or {}
    status = context.get("status") or {}
    attention = status.get("attention") or []
    lines = [
        "# PRIME Project Context Export", "", "## PROJECT",
        f"- Name: {project.get('name', 'UNKNOWN')}", f"- Project ID: {project.get('project_id', 'UNKNOWN')}",
        f"- Node: {repository.get('node_name', 'UNKNOWN')}", f"- Repository: {repository.get('canonical_path', 'UNKNOWN')}",
        f"- Canonical revision: {git.get('canonical_revision', 'UNKNOWN')}", f"- Branch: {git.get('branch', 'UNKNOWN')}",
        "", "## GOAL", f"- Revision: {goal.get('revision_number', 'UNKNOWN')} ({goal.get('status', 'UNKNOWN')})",
        f"- Source hash: {goal.get('content_hash', 'UNKNOWN')}", f"- Approved goal: {goal.get('content', 'UNKNOWN')}",
        "", "## CURRENT STATUS", f"- Progress: {(status.get('progress') or {}).get('progress_percent', 'UNKNOWN')}",
        f"- Confidence: {(status.get('progress') or {}).get('confidence', 'UNKNOWN')}", f"- Alignment: {status.get('alignment', 'UNKNOWN')}",
        f"- Attention: {len(attention)} item(s)", "", "## BLOCKERS / ATTENTION",
    ]
    lines.extend([f"- {item.get('severity', 'UNKNOWN')}: {item.get('code', 'UNKNOWN')} - {item.get('message', 'UNKNOWN')}" for item in attention] or ["- NONE REPORTED"])
    lines.extend(["", "## PROVENANCE", *[f"- {item.get('claim', 'UNKNOWN')}: {item.get('source_class', 'UNKNOWN')} / {item.get('reference', 'UNKNOWN')} / revision {item.get('revision', 'UNKNOWN')}" for item in (context.get('provenance') or [])], "", "## AUTHORITY", f"- Validation: {(context.get('authority') or {}).get('latest', {}).get('validation_status', 'UNKNOWN') if (context.get('authority') or {}).get('latest') else 'UNKNOWN'}", "- Credential material: OMITTED", "", "## MEMORY / EVIDENCE / ACTIVITY", f"- Durable memory entries exported: {len(context.get('memory') or [])}", f"- Evidence references exported: {len(context.get('evidence') or [])}", f"- Meaningful activity events exported: {len(context.get('activity') or [])}", "", "## FRESHNESS", f"- Generated at: {context.get('generated_at', 'UNKNOWN')}", f"- Project freshness: {(context.get('freshness') or {}).get('project', 'UNKNOWN')}", f"- Canonical repository revision: {(context.get('freshness') or {}).get('repository', 'UNKNOWN')}", f"- Redaction: credentials, tokens, authorization headers, and chain of thought omitted."])
    return "\n".join(lines) + "\n"


@app.get("/v1/projects/{project_id}/context-export")
def context_export(project_id: str, request: Request, format: str = "json", prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        context = _project_context(project_id)
    except KeyError:
        return error("PROJECT_NOT_FOUND", "project not found", request_id(request), status_code=404)
    if format.lower() in {"md", "markdown"}:
        return Response(content=_context_markdown(context), media_type="text/markdown", headers={"Cache-Control": "no-store", "Content-Disposition": f'attachment; filename="prime-{project_id}-context.md"'})
    if format.lower() != "json":
        return error("EXPORT_FORMAT_UNSUPPORTED", "format must be json or markdown", request_id(request), status_code=400)
    return Response(content=json.dumps(context, default=str, ensure_ascii=False, indent=2), media_type="application/json", headers={"Cache-Control": "no-store", "Content-Disposition": f'attachment; filename="prime-{project_id}-context.json"'})


@app.get("/v1/projects/{project_id}/repository/state")
def repository_state(project_id: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    if not project_exists(project_id):
        return error("PROJECT_NOT_FOUND", "project not found", request_id(request), status_code=404)
    return _git_state(project_id)


@app.get("/v1/projects/{project_id}/repository/tree")
def repository_tree(project_id: str, request: Request, path: str = "", prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        root, candidate = _safe_repository_path(project_id, path)
        if not candidate.is_dir():
            return error("REPOSITORY_PATH_NOT_DIRECTORY", "requested repository path is not a directory", request_id(request), status_code=400)
        entries = []
        for entry in sorted(candidate.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))[:200]:
            if entry.name == ".git":
                continue
            relative = entry.relative_to(root).as_posix()
            item = {"name": entry.name, "path": relative, "kind": "directory" if entry.is_dir() else "file"}
            if entry.is_file():
                item["size_bytes"] = entry.stat().st_size
            entries.append(item)
        return {"project_id": project_id, "path": candidate.relative_to(root).as_posix() if candidate != root else "", "root": str(root), "entries": entries, "source_revision": _git(root, "rev-parse", "HEAD")}
    except KeyError:
        return error("PROJECT_NOT_FOUND", "project not found or repository is unbound", request_id(request), status_code=404)
    except (OSError, ValueError) as exc:
        return error("REPOSITORY_PATH_REJECTED", str(exc), request_id(request), status_code=400)


@app.get("/v1/projects/{project_id}/repository/file")
def repository_file(project_id: str, path: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        root, candidate = _safe_repository_path(project_id, path)
        if not candidate.is_file():
            return error("REPOSITORY_FILE_NOT_FOUND", "requested repository file was not found", request_id(request), status_code=404)
        size = candidate.stat().st_size
        if size > 120_000:
            return {"project_id": project_id, "path": candidate.relative_to(root).as_posix(), "availability": "UNAVAILABLE", "reason": "file exceeds bounded viewer limit", "size_bytes": size, "source_revision": _git(root, "rev-parse", "HEAD")}
        data = candidate.read_bytes()
        if b"\x00" in data[:8192]:
            return {"project_id": project_id, "path": candidate.relative_to(root).as_posix(), "availability": "UNAVAILABLE", "reason": "binary file", "size_bytes": size, "source_revision": _git(root, "rev-parse", "HEAD")}
        content = data.decode("utf-8", errors="replace")
        return {"project_id": project_id, "path": candidate.relative_to(root).as_posix(), "availability": "EXACT", "content": content, "content_hash": hashlib.sha256(data).hexdigest(), "size_bytes": size, "source_revision": _git(root, "rev-parse", "HEAD")}
    except KeyError:
        return error("PROJECT_NOT_FOUND", "project not found or repository is unbound", request_id(request), status_code=404)
    except (OSError, ValueError) as exc:
        return error("REPOSITORY_FILE_REJECTED", str(exc), request_id(request), status_code=400)


@app.get("/v1/projects/{project_id}/authority")
def authority_view(project_id: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        context = _project_context(project_id)
    except KeyError:
        return error("PROJECT_NOT_FOUND", "project not found", request_id(request), status_code=404)
    authority = context.get("authority") or {}
    return {"project_id": project_id, "health": (authority.get("latest") or {}).get("validation_status", "UNKNOWN"), "contract": (authority.get("latest") or {}).get("contract_version", "UNKNOWN"), "latest": authority.get("latest"), "history": authority.get("history", []), "files": {name: {"sha256": value.get("sha256"), "content": value.get("content")} for name, value in (authority.get("files") or {}).items()}}


def _project_snapshot(project_id: str) -> dict[str, Any]:
    """Return the bounded, read-only product snapshot used by the operator UI."""
    with connect(settings) as db:
        project = db.execute("SELECT * FROM prime_core.projects WHERE project_id=%s", (project_id,)).fetchone()
        if not project:
            raise KeyError("project not found")
        binding = db.execute(
            "SELECT b.binding_status,b.canonical_revision,r.repository_id,r.canonical_path,r.identity_fingerprint,r.last_observed_at,n.node_id,n.name AS node_name,n.platform,n.status AS node_status "
            "FROM prime_core.project_bindings b JOIN prime_core.repositories r ON r.repository_id=b.repository_id "
            "JOIN prime_core.nodes n ON n.node_id=b.node_id WHERE b.project_id=%s",
            (project_id,),
        ).fetchone()
        goal = db.execute("SELECT goal_revision_id,revision_number,content,content_hash,status,created_at,approved_at FROM prime_core.goal_revisions WHERE project_id=%s ORDER BY revision_number DESC LIMIT 1", (project_id,)).fetchone()
        goal_items = db.execute("SELECT goal_item_id,title,description,weight,required,acceptance_expectations FROM prime_core.goal_items WHERE project_id=%s AND goal_revision_id=%s ORDER BY goal_item_id", (project_id, goal["goal_revision_id"] if goal else "")).fetchall()
        progress = db.execute("SELECT assessment_id,goal_revision_id,repository_revision,progress_percent,confidence,freshness_state,summary,evidence_refs,created_at FROM prime_core.progress_assessments WHERE project_id=%s ORDER BY created_at DESC LIMIT 1", (project_id,)).fetchone()
        authority = db.execute("SELECT authority_revision_id,source_path,source_hash,contract_version,validation_status,observed_at FROM prime_core.authority_revisions WHERE project_id=%s ORDER BY observed_at DESC LIMIT 1", (project_id,)).fetchone()
        notion = db.execute("SELECT project_id,page_id,page_url,connection_status,managed_content_hash,last_synced_at FROM prime_core.notion_projects WHERE project_id=%s", (project_id,)).fetchone()
        evidence = db.execute("SELECT COUNT(*) AS total, COUNT(*) FILTER (WHERE retracted_at IS NULL AND purged_at IS NULL) AS current, COUNT(*) FILTER (WHERE parser_status='FAILED' OR index_status='FAILED') AS failed FROM prime_core.evidence_records WHERE project_id=%s", (project_id,)).fetchone()
        memory = db.execute("SELECT COUNT(*) AS total, MAX(created_at) AS last_created FROM prime_core.memory_records WHERE project_id=%s AND status NOT IN ('TOMBSTONED','SUPERSEDED')", (project_id,)).fetchone()
        events = [dict(row) for row in db.execute("SELECT event_id,event_type,project_sequence,observed_at,payload,source_revision FROM prime_core.events WHERE project_id=%s ORDER BY observed_at DESC LIMIT 20", (project_id,)).fetchall()]
        files = db.execute("SELECT COUNT(*) AS total, MAX(observed_at) AS last_observed, MAX(source_revision) AS source_revision FROM prime_core.repository_files WHERE project_id=%s", (project_id,)).fetchone()
        checkpoint = db.execute("SELECT last_seen_event_sequence,updated_at FROM prime_core.activity_checkpoints WHERE project_id=%s", (project_id,)).fetchone()
    attention: list[dict[str, Any]] = []
    project_dict = dict(project)
    if not binding:
        attention.append({"code": "REPOSITORY_UNBOUND", "severity": "HIGH", "message": "Bind one verified repository before treating this project as operational."})
    if not goal or goal["status"] != "APPROVED":
        attention.append({"code": "GOAL_NOT_APPROVED", "severity": "HIGH", "message": "An approved PROJECT_GOAL.md revision is not visible in Core."})
    if project_dict.get("freshness_state") in {"STALE", "UNKNOWN"}:
        attention.append({"code": "PROJECT_STALE", "severity": "MEDIUM", "message": f"Project freshness is {project_dict.get('freshness_state')}."})
    if project_dict.get("work_condition") in {"BLOCKED", "CONFLICT", "INVALID_AUTHORITY", "REVIEW_REQUIRED"}:
        attention.append({"code": "WORK_CONDITION", "severity": "HIGH", "message": f"Project work condition is {project_dict.get('work_condition')}; inspect the owning source before continuing."})
    if binding and binding.get("node_status") in {"OFFLINE", "DEGRADED"}:
        attention.append({"code": "NODE_DEGRADED", "severity": "HIGH", "message": f"Bound repository node is {binding.get('node_status')}."})
    if evidence and int(evidence["failed"] or 0):
        attention.append({"code": "EVIDENCE_DEGRADED", "severity": "MEDIUM", "message": "One or more Evidence parser/index operations failed."})
    return {
        "project": project_dict,
        "binding": dict(binding) if binding else None,
        "goal": dict(goal) if goal else None,
        "goal_items": [dict(row) for row in goal_items],
        "progress": dict(progress) if progress else None,
        "authority": dict(authority) if authority else None,
        "notion": dict(notion) if notion else {"connection_status": "DISCONNECTED"},
        "evidence": dict(evidence) if evidence else {"total": 0, "current": 0, "failed": 0},
        "memory": dict(memory) if memory else {"total": 0},
        "files": dict(files) if files else {"total": 0},
        "events": events,
        "checkpoint": dict(checkpoint) if checkpoint else {"last_seen_event_sequence": 0},
        "attention": attention,
        "brain": {"availability": "DERIVED_ON_REQUEST"},
    }


@app.get("/v1/projects/{project_id}/agent-chain")
def agent_chain(project_id: str, request: Request, path: str = "", prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return service.agent_instruction_chain(project_id, path)
    except KeyError:
        return error("PROJECT_NOT_FOUND", "project or repository not found", request_id(request), status_code=404)
    except (PermissionError, ValueError, OSError) as exc:
        return error("AGENT_CHAIN_REJECTED", str(exc), request_id(request), status_code=400)


@app.get("/v1/projects/{project_id}/snapshot")
def project_snapshot(project_id: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return _project_snapshot(project_id)
    except KeyError:
        return error("PROJECT_NOT_FOUND", "project not found", request_id(request), status_code=404)


@app.get("/v1/projects/{project_id}/since-you-were-here")
def since_you_were_here(project_id: str, request: Request, advance: bool = False, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    if not project_exists(project_id):
        return error("PROJECT_NOT_FOUND", "project not found", request_id(request), status_code=404)
    return intelligence.since_last_seen(project_id, advance=advance)


@app.get("/v1/projects/{project_id}/activity")
def project_activity(project_id: str, request: Request, event_type: str | None = None, source_revision: str | None = None, limit: int = 50, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    if not project_exists(project_id):
        return error("PROJECT_NOT_FOUND", "project not found", request_id(request), status_code=404)
    clauses = ["project_id=%s"]
    params: list[Any] = [project_id]
    if event_type:
        clauses.append("event_type=%s")
        params.append(event_type)
    if source_revision:
        clauses.append("source_revision=%s")
        params.append(source_revision)
    params.append(min(max(limit, 1), 200))
    with connect(settings) as db:
        rows = db.execute(f"SELECT event_id,event_type,project_sequence,occurred_at,observed_at,source_revision,source_ref,payload FROM prime_core.events WHERE {' AND '.join(clauses)} ORDER BY observed_at DESC LIMIT %s", tuple(params)).fetchall()
    return {"project_id": project_id, "filters": {"event_type": event_type, "source_revision": source_revision}, "events": [dict(row) for row in rows]}


@app.post("/v1/projects/{project_id}/since-you-were-here/advance")
def advance_since_you_were_here(project_id: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    if not project_exists(project_id):
        return error("PROJECT_NOT_FOUND", "project not found", request_id(request), status_code=404)
    return intelligence.since_last_seen(project_id, advance=True)


@app.post("/v1/projects/{project_id}/ask")
def ask_project(project_id: str, question: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    if not project_exists(project_id):
        return error("PROJECT_NOT_FOUND", "project not found", request_id(request), status_code=404)
    try:
        return intelligence.ask(project_id, question)
    except (KeyError, ValueError) as exc:
        return error("ASK_REJECTED", str(exc), request_id(request), status_code=400)


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


@app.get("/v1/projects/{project_id}/brain")
def project_brain(project_id: str, request: Request, q: str | None = None, kind: list[str] | None = None, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    if not project_exists(project_id):
        return error("PROJECT_NOT_FOUND", "project not found", request_id(request), status_code=404)
    return brain.build(project_id, query=q, kinds=kind)


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


@app.get("/v1/projects/{project_id}/ai/connections")
def list_ai_connections(project_id: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    if not project_exists(project_id):
        return error("PROJECT_NOT_FOUND", "project not found", request_id(request), status_code=404)
    profiles = ai.public_profiles()
    return {"project_id": project_id, "profiles": profiles, "grants": mcp.list_grants(project_id), "secrets": "NEVER_RETURNED_AFTER_ISSUANCE"}


@app.post("/v1/projects/{project_id}/ai/connections/{grant_id}/rotate")
def rotate_ai_connection(project_id: str, grant_id: str, body: GrantRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return {"project_id": project_id, "rotation": "REVOKED_AND_REISSUED", "grant": mcp.rotate_grant(project_id, grant_id, body.client_id), "secret_policy": "one_time_issue_only"}
    except KeyError as exc:
        return error("AI_CONNECTION_REJECTED", str(exc), request_id(request), status_code=404)


@app.delete("/v1/projects/{project_id}/ai/connections/{grant_id}")
def revoke_ai_connection(project_id: str, grant_id: str, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        mcp.revoke_grant(grant_id, project_id)
        return {"project_id": project_id, "grant_id": grant_id, "state": "REVOKED"}
    except KeyError as exc:
        return error("AI_CONNECTION_REJECTED", str(exc), request_id(request), status_code=404)


@app.post("/v1/projects/{project_id}/fork")
def fork_project(project_id: str, body: ForkRequest, request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    try:
        return service.fork_project(project_id, body.source_revision, body.destination_node_id, body.parent_path, body.repository_name, body.confirm)
    except KeyError as exc:
        return error("FORK_NOT_FOUND", str(exc), request_id(request), status_code=404)
    except (PermissionError, ValueError, FileNotFoundError, FileExistsError, OSError, subprocess.CalledProcessError) as exc:
        return error("FORK_REJECTED", str(exc), request_id(request), status_code=400)


@app.post("/v1/mcp/{tool}")
def mcp_tool(tool: str, body: dict[str, Any], authorization: str | None = Header(default=None)):
    token = authorization[7:] if authorization and authorization.startswith("Bearer ") else ""
    return mcp.call(token, tool, body)


@app.get("/v1/system/remote-access")
def remote_access_status(request: Request, prime_session: str | None = Cookie(default=None)):
    require_session(request, prime_session)
    return remote_access.reconcile()


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
    if step_up != "CONFIRM":
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
