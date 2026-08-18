from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from typing import Any

from src.prime_node.config import NodeSettings
from src.prime_node.service import NodeService

settings = NodeSettings()
service = NodeService(settings)
app = FastAPI(title="ANIMUS PRIME Node", version="1.0.0")


class EnrollRequest(BaseModel):
    credential: str = Field(min_length=1, max_length=4096)
    node_id: str = Field(min_length=1, max_length=160)
    csr_pem: str = Field(min_length=100, max_length=20000)


class PathRequest(BaseModel):
    path: str = Field(min_length=1, max_length=4096)


class RepositoryCreateRequest(BaseModel):
    parent_path: str = Field(min_length=1, max_length=4096)
    repository_name: str = Field(min_length=1, max_length=160)
    operation_id: str = Field(min_length=1, max_length=200)


class AuthorityBootstrapRequest(BaseModel):
    repository_path: str = Field(min_length=1, max_length=4096)
    files: dict[str, str]
    operation_id: str = Field(min_length=1, max_length=200)


class ProjectGoalWriteRequest(BaseModel):
    repository_path: str = Field(min_length=1, max_length=4096)
    content: str = Field(min_length=20, max_length=200000)
    content_hash: str = Field(min_length=64, max_length=64)


class ApprovalRequest(BaseModel):
    certificate_pem: str = Field(min_length=100, max_length=20000)
    token: str = Field(min_length=32, max_length=512)
    metadata: dict[str, Any] = Field(default_factory=dict)


def require_node(authorization: str | None, node_id: str | None = None, protocol: str | None = None) -> None:
    if not authorization or not authorization.startswith("Bearer ") or not service.authenticate(authorization[7:]):
        raise HTTPException(status_code=401, detail="node authentication required")
    if node_id != service.state.get("node_id"):
        raise HTTPException(status_code=401, detail="node identity mismatch")
    if protocol != settings.protocol_version:
        raise HTTPException(status_code=426, detail="incompatible node control protocol")
    if node_id != service.state.get("node_id"):
        raise HTTPException(status_code=401, detail="authenticated Node identity mismatch")


@app.get("/health/live")
def live():
    return {"status": "live", **service.status()}


@app.post("/v1/enroll")
def enroll(body: EnrollRequest):
    try:
        return service.enroll(body.credential, body.node_id, body.csr_pem)
    except PermissionError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.get("/v1/status")
def status(authorization: str | None = Header(default=None), x_prime_node_id: str | None = Header(default=None), x_prime_protocol: str | None = Header(default=None)):
    require_node(authorization, x_prime_node_id, x_prime_protocol)
    return service.status()


@app.post("/v1/heartbeat")
def heartbeat(authorization: str | None = Header(default=None), x_prime_node_id: str | None = Header(default=None), x_prime_protocol: str | None = Header(default=None)):
    require_node(authorization, x_prime_node_id, x_prime_protocol)
    try:
        return service.heartbeat(x_prime_protocol or "")
    except ValueError as exc:
        raise HTTPException(status_code=426, detail=str(exc)) from exc


@app.post("/v1/credentials/rotate")
def rotate(authorization: str | None = Header(default=None), x_prime_node_id: str | None = Header(default=None), x_prime_protocol: str | None = Header(default=None)):
    require_node(authorization, x_prime_node_id, x_prime_protocol)
    return {"node_credential": service.rotate(authorization[7:]), "warning": "store outside the repository"}


@app.post("/v1/re-enroll")
def re_enroll(body: EnrollRequest):
    return enroll(body)


@app.post("/v1/enrollment/approve")
def approve_enrollment(body: ApprovalRequest):
    try:
        return service.approve(body.certificate_pem, body.token, body.metadata)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.post("/v1/enrollment/reject")
def reject_enrollment():
    service.reject()
    return {"status": "REJECTED"}


@app.post("/v1/repositories/inspect")
def inspect(body: PathRequest, authorization: str | None = Header(default=None), x_prime_node_id: str | None = Header(default=None), x_prime_protocol: str | None = Header(default=None)):
    require_node(authorization, x_prime_node_id, x_prime_protocol)
    try:
        return service.inspect_repository(body.path)
    except (PermissionError, ValueError, FileNotFoundError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/v1/repositories/create")
def create_repository(body: RepositoryCreateRequest, authorization: str | None = Header(default=None), x_prime_node_id: str | None = Header(default=None), x_prime_protocol: str | None = Header(default=None)):
    require_node(authorization, x_prime_node_id, x_prime_protocol)
    try:
        return service.create_repository(body.parent_path, body.repository_name, body.operation_id)
    except (PermissionError, ValueError, FileNotFoundError, FileExistsError, NotADirectoryError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/v1/repositories/authority/bootstrap")
def bootstrap_authority(body: AuthorityBootstrapRequest, authorization: str | None = Header(default=None), x_prime_node_id: str | None = Header(default=None), x_prime_protocol: str | None = Header(default=None)):
    require_node(authorization, x_prime_node_id, x_prime_protocol)
    try:
        return service.bootstrap_authority(body.repository_path, body.files, body.operation_id)
    except (PermissionError, ValueError, FileNotFoundError, FileExistsError, NotADirectoryError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/v1/repositories/goal")
def write_project_goal(body: ProjectGoalWriteRequest, authorization: str | None = Header(default=None), x_prime_node_id: str | None = Header(default=None), x_prime_protocol: str | None = Header(default=None)):
    require_node(authorization, x_prime_node_id, x_prime_protocol)
    try:
        return service.write_project_goal(body.repository_path, body.content, body.content_hash)
    except (PermissionError, ValueError, FileNotFoundError, NotADirectoryError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/v1/files/read")
def read_file(body: PathRequest, authorization: str | None = Header(default=None), x_prime_node_id: str | None = Header(default=None), x_prime_protocol: str | None = Header(default=None)):
    require_node(authorization, x_prime_node_id, x_prime_protocol)
    try:
        return service.read_file(body.path)
    except (PermissionError, ValueError, FileNotFoundError, IsADirectoryError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/v1/files/list")
def list_files(body: PathRequest, authorization: str | None = Header(default=None), x_prime_node_id: str | None = Header(default=None), x_prime_protocol: str | None = Header(default=None)):
    require_node(authorization, x_prime_node_id, x_prime_protocol)
    try:
        return service.list_directory(body.path)
    except (PermissionError, ValueError, FileNotFoundError, NotADirectoryError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/v1/revoke")
def revoke(authorization: str | None = Header(default=None), x_prime_node_id: str | None = Header(default=None), x_prime_protocol: str | None = Header(default=None)):
    require_node(authorization, x_prime_node_id, x_prime_protocol)
    return {"status": service.revoke()}


@app.get("/v1/diagnostics")
def diagnostics(authorization: str | None = Header(default=None), x_prime_node_id: str | None = Header(default=None), x_prime_protocol: str | None = Header(default=None)):
    require_node(authorization, x_prime_node_id, x_prime_protocol)
    return service.diagnostics()


@app.post("/v1/repositories/snapshot")
def snapshot(body: PathRequest, authorization: str | None = Header(default=None), x_prime_node_id: str | None = Header(default=None), x_prime_protocol: str | None = Header(default=None)):
    require_node(authorization, x_prime_node_id, x_prime_protocol)
    try:
        return service.repository_snapshot(body.path)
    except (PermissionError, ValueError, FileNotFoundError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def run() -> None:
    """Run the packaged Node with mandatory TLS/mTLS service configuration."""
    import uvicorn

    settings.validate()
    uvicorn.run(app, **settings.uvicorn_kwargs())


if __name__ == "__main__":
    run()
