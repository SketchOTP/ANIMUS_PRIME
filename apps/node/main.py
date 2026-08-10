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


def require_node(authorization: str | None, node_id: str | None = None, protocol: str | None = None) -> None:
    if not authorization or not authorization.startswith("Bearer ") or not service.authenticate(authorization[7:]):
        raise HTTPException(status_code=401, detail="node authentication required")
    if node_id != service.state.get("node_id"):
        raise HTTPException(status_code=401, detail="node identity mismatch")
    if protocol != settings.protocol_version:
        raise HTTPException(status_code=426, detail="incompatible node control protocol")


@app.get("/health/live")
def live():
    return {"status": "live", **service.status()}


@app.post("/v1/enroll")
def enroll(body: EnrollRequest):
    try:
        node_id, token = service.enroll(body.credential)
        return {"node_id": node_id, "node_credential": token, "warning": "store outside the repository"}
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
    return {"status": "ONLINE", "node_id": service.state["node_id"], "protocol_version": settings.protocol_version}


@app.post("/v1/credentials/rotate")
def rotate(authorization: str | None = Header(default=None), x_prime_node_id: str | None = Header(default=None), x_prime_protocol: str | None = Header(default=None)):
    require_node(authorization, x_prime_node_id, x_prime_protocol)
    return {"node_credential": service.rotate(authorization[7:]), "warning": "store outside the repository"}


@app.post("/v1/re-enroll")
def re_enroll(body: EnrollRequest):
    try:
        node_id, token = service.enroll(body.credential)
        return {"node_id": node_id, "node_credential": token, "warning": "store outside the repository"}
    except PermissionError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.post("/v1/repositories/inspect")
def inspect(body: PathRequest, authorization: str | None = Header(default=None), x_prime_node_id: str | None = Header(default=None), x_prime_protocol: str | None = Header(default=None)):
    require_node(authorization, x_prime_node_id, x_prime_protocol)
    try:
        return service.inspect_repository(body.path)
    except (PermissionError, ValueError, FileNotFoundError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/v1/files/read")
def read_file(body: PathRequest, authorization: str | None = Header(default=None), x_prime_node_id: str | None = Header(default=None), x_prime_protocol: str | None = Header(default=None)):
    require_node(authorization, x_prime_node_id, x_prime_protocol)
    try:
        return service.read_file(body.path)
    except (PermissionError, ValueError, FileNotFoundError, IsADirectoryError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/v1/revoke")
def revoke(authorization: str | None = Header(default=None), x_prime_node_id: str | None = Header(default=None), x_prime_protocol: str | None = Header(default=None)):
    require_node(authorization, x_prime_node_id, x_prime_protocol)
    return {"status": "REVOKED", "re_enrollment_credential": service.revoke()}


def run() -> None:
    """Run the packaged Node with mandatory TLS/mTLS service configuration."""
    import uvicorn

    uvicorn.run(app, **settings.uvicorn_kwargs())


if __name__ == "__main__":
    run()
