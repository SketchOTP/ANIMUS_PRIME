from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from src.prime_node.config import NodeSettings
from src.prime_node.service import NodeService

settings = NodeSettings()
service = NodeService(settings)
app = FastAPI(title="ANIMUS PRIME Node", version="1.0.0-phase2")


class EnrollRequest(BaseModel):
    credential: str = Field(min_length=1, max_length=256)


class PathRequest(BaseModel):
    path: str = Field(min_length=1, max_length=4096)


def require_node(authorization: str | None) -> None:
    if not authorization or not authorization.startswith("Bearer ") or not service.authenticate(authorization[7:]):
        raise HTTPException(status_code=401, detail="node authentication required")


@app.get("/health/live")
def live():
    return {"status": "live", "service": "prime-node"}


@app.post("/v1/enroll")
def enroll(body: EnrollRequest):
    try:
        node_id, token = service.enroll(body.credential)
        return {"node_id": node_id, "node_credential": token, "warning": "store outside the repository"}
    except PermissionError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.post("/v1/repositories/inspect")
def inspect(body: PathRequest, authorization: str | None = Header(default=None)):
    require_node(authorization)
    try:
        return service.inspect_repository(body.path)
    except (PermissionError, ValueError, FileNotFoundError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/v1/files/read")
def read_file(body: PathRequest, authorization: str | None = Header(default=None)):
    require_node(authorization)
    try:
        return service.read_file(body.path)
    except (PermissionError, ValueError, FileNotFoundError, IsADirectoryError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/v1/revoke")
def revoke(authorization: str | None = Header(default=None)):
    require_node(authorization)
    service.revoke()
    return {"status": "REVOKED"}

