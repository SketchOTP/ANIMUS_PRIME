from __future__ import annotations

import json
import hashlib
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse


class NodeClientError(RuntimeError):
    pass


@dataclass(frozen=True)
class NodeClientSettings:
    base_url: str
    node_id: str
    credential: str | None = None
    protocol_version: str = "node-control-v1"
    ca_file: Path | None = None
    client_cert: Path | None = None
    client_key: Path | None = None
    timeout_seconds: int = 10
    max_response_bytes: int = 256 * 1024


class NodeClient:
    """Core-side bounded client for the private Node control plane."""

    def __init__(self, settings: NodeClientSettings, opener: Callable[..., Any] | None = None):
        self.settings = settings
        self._opener = opener or urllib.request.urlopen

    def heartbeat(self) -> dict[str, Any]:
        return self._request("POST", "/v1/heartbeat")

    def status(self) -> dict[str, Any]:
        return self._request("GET", "/v1/status")

    def inspect_repository(self, path: str) -> dict[str, Any]:
        return self._request("POST", "/v1/repositories/inspect", {"path": path})

    def create_repository(self, parent_path: str, repository_name: str, operation_id: str) -> dict[str, Any]:
        return self._request(
            "POST",
            "/v1/repositories/create",
            {"parent_path": parent_path, "repository_name": repository_name, "operation_id": operation_id},
        )

    def quarantine_repository(self, repository_path: str, operation_id: str) -> dict[str, Any]:
        return self._request("POST", "/v1/repositories/quarantine", {"repository_path": repository_path, "operation_id": operation_id})

    def restore_quarantined_repository(self, operation_id: str) -> dict[str, Any]:
        return self._request("POST", "/v1/repositories/quarantine/restore", {"operation_id": operation_id})

    def purge_quarantined_repository(self, operation_id: str) -> dict[str, Any]:
        return self._request("POST", "/v1/repositories/quarantine/purge", {"operation_id": operation_id})

    def bootstrap_authority(self, repository_path: str, files: dict[str, str], operation_id: str) -> dict[str, Any]:
        return self._request(
            "POST",
            "/v1/repositories/authority/bootstrap",
            {"repository_path": repository_path, "files": files, "operation_id": operation_id},
        )

    def write_project_goal(self, repository_path: str, content: str, content_hash: str) -> dict[str, Any]:
        return self._request(
            "POST",
            "/v1/repositories/goal",
            {"repository_path": repository_path, "content": content, "content_hash": content_hash},
        )

    def read_file(self, path: str) -> dict[str, Any]:
        return self._request("POST", "/v1/files/read", {"path": path})

    def list_directory(self, path: str) -> dict[str, Any]:
        return self._request("POST", "/v1/files/list", {"path": path})

    def diagnostics(self) -> dict[str, Any]:
        return self._request("GET", "/v1/diagnostics")

    def repository_snapshot(self, path: str) -> dict[str, Any]:
        return self._request("POST", "/v1/repositories/snapshot", {"path": path})

    def enroll(self, credential: str, csr_pem: str) -> dict[str, Any]:
        return self._request("POST", "/v1/enroll", {"credential": credential, "node_id": self.settings.node_id, "csr_pem": csr_pem})

    def approve(self, certificate_pem: str, token: str, metadata: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/v1/enrollment/approve", {"certificate_pem": certificate_pem, "token": token, "metadata": metadata})

    def reject(self) -> dict[str, Any]:
        return self._request("POST", "/v1/enrollment/reject", {})

    def rotate(self) -> dict[str, Any]:
        return self._request("POST", "/v1/credentials/rotate", {})

    def revoke(self) -> dict[str, Any]:
        return self._request("POST", "/v1/revoke", {})

    def _request(self, method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        request = urllib.request.Request(
            self.settings.base_url.rstrip("/") + path,
            method=method,
            headers={
                "X-Prime-Node-Id": self.settings.node_id,
                "X-Prime-Protocol": self.settings.protocol_version,
                "Content-Type": "application/json",
            },
            data=json.dumps(body).encode() if body is not None else None,
        )
        if self.settings.credential:
            request.add_header("Authorization", f"Bearer {self.settings.credential}")
        context = self._tls_context()
        try:
            with self._opener(request, timeout=self.settings.timeout_seconds, context=context) as response:
                try:
                    payload = response.read(self.settings.max_response_bytes + 1)
                except TypeError:  # small test doubles and legacy urllib wrappers
                    payload = response.read()
                if len(payload) > self.settings.max_response_bytes:
                    raise NodeClientError("Node response exceeded bound")
                result = json.loads(payload.decode())
        except urllib.error.HTTPError as exc:
            try:
                detail = exc.read(4096).decode("utf-8", errors="replace")
            except Exception:
                detail = ""
            raise NodeClientError(f"Node control-plane HTTP {exc.code}: {detail[:512]}") from exc
        except urllib.error.URLError as exc:
            reason = getattr(exc, "reason", None)
            detail = str(reason)[:256] if reason else ""
            raise NodeClientError(f"Node control-plane request failed: {type(reason).__name__ if reason else type(exc).__name__}: {detail}") from exc
        except (TimeoutError, json.JSONDecodeError) as exc:
            raise NodeClientError(f"Node control-plane request failed: {type(exc).__name__}") from exc
        if not isinstance(result, dict):
            raise NodeClientError("Node returned an invalid response")
        return result

    @staticmethod
    def idempotency_key(operation: str, request_body: dict[str, Any] | None = None) -> str:
        return hashlib.sha256(json.dumps([operation, request_body or {}], sort_keys=True).encode()).hexdigest()

    def _tls_context(self) -> ssl.SSLContext:
        context = ssl.create_default_context(cafile=str(self.settings.ca_file) if self.settings.ca_file else None)
        # The canonical Atlas Node is deliberately loopback-bound.  Its certificate
        # is still chain-verified and client-authenticated; loopback transport has no
        # DNS identity to validate, so the application-level canonical Node ID is the
        # stable endpoint identity for this private control plane.
        if urlparse(self.settings.base_url).hostname in {"127.0.0.1", "::1"}:
            context.check_hostname = False
        if self.settings.client_cert or self.settings.client_key:
            if not self.settings.client_cert or not self.settings.client_key:
                raise NodeClientError("client certificate and key must be configured together")
            context.load_cert_chain(str(self.settings.client_cert), str(self.settings.client_key))
        return context
