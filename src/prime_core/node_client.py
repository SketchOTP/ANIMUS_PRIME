from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


class NodeClientError(RuntimeError):
    pass


@dataclass(frozen=True)
class NodeClientSettings:
    base_url: str
    node_id: str
    credential: str
    protocol_version: str = "node-control-v1"
    ca_file: Path | None = None
    client_cert: Path | None = None
    client_key: Path | None = None
    timeout_seconds: int = 10


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

    def read_file(self, path: str) -> dict[str, Any]:
        return self._request("POST", "/v1/files/read", {"path": path})

    def _request(self, method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        request = urllib.request.Request(
            self.settings.base_url.rstrip("/") + path,
            method=method,
            headers={
                "Authorization": f"Bearer {self.settings.credential}",
                "X-Prime-Node-Id": self.settings.node_id,
                "X-Prime-Protocol": self.settings.protocol_version,
                "Content-Type": "application/json",
            },
            data=json.dumps(body).encode() if body is not None else None,
        )
        context = self._tls_context()
        try:
            with self._opener(request, timeout=self.settings.timeout_seconds, context=context) as response:
                result = json.loads(response.read().decode())
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise NodeClientError("Node control-plane request failed") from exc
        if not isinstance(result, dict):
            raise NodeClientError("Node returned an invalid response")
        return result

    def _tls_context(self) -> ssl.SSLContext:
        context = ssl.create_default_context(cafile=str(self.settings.ca_file) if self.settings.ca_file else None)
        if self.settings.client_cert or self.settings.client_key:
            if not self.settings.client_cert or not self.settings.client_key:
                raise NodeClientError("client certificate and key must be configured together")
            context.load_cert_chain(str(self.settings.client_cert), str(self.settings.client_key))
        return context
