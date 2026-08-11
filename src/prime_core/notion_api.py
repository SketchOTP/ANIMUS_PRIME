from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable


class NotionApiError(RuntimeError):
    def __init__(self, status: int, message: str, retryable: bool = False):
        super().__init__(message)
        self.status = status
        self.retryable = retryable


@dataclass(frozen=True)
class NotionApiSettings:
    token: str
    api_version: str = "2026-03-11"
    base_url: str = "https://api.notion.com/v1"
    timeout_seconds: int = 15
    max_retries: int = 3


class NotionApiClient:
    """Small server-side Notion client with bounded retry and no credential logging."""

    def __init__(self, settings: NotionApiSettings, opener: Callable[..., Any] | None = None, sleeper: Callable[[float], None] | None = None):
        if not settings.token:
            raise ValueError("Notion token is required")
        self.settings = settings
        self._opener = opener or urllib.request.urlopen
        self._sleep = sleeper or time.sleep

    def retrieve_page(self, page_id: str) -> dict[str, Any]:
        return self._request("GET", f"/pages/{page_id}")

    def test_connection(self) -> dict[str, Any]:
        """Return provider identity/capabilities without exposing the token."""
        payload = self._request("GET", "/users/me")
        return {
            "status": "CONNECTED",
            "workspace_id": payload.get("bot", {}).get("workspace_name") or payload.get("workspace_id"),
            "actor_id": payload.get("id"),
            "capabilities": ["page_read", "page_write", "block_read", "block_write"],
        }

    def provider_health(self) -> dict[str, Any]:
        try:
            return self.test_connection()
        except NotionApiError as exc:
            if exc.status in {401, 403}:
                return {"status": "REAUTH_REQUIRED" if exc.status == 401 else "ACCESS_LOST", "error_code": f"HTTP_{exc.status}"}
            return {"status": "DEGRADED", "retryable": exc.retryable, "error_code": f"HTTP_{exc.status}"}

    def retrieve_children(self, block_id: str, start_cursor: str | None = None) -> dict[str, Any]:
        suffix = f"?start_cursor={start_cursor}" if start_cursor else ""
        return self._request("GET", f"/blocks/{block_id}/children{suffix}")

    def retrieve_block(self, block_id: str) -> dict[str, Any]:
        return self._request("GET", f"/blocks/{block_id}")

    def create_page(self, parent: dict[str, Any], properties: dict[str, Any], children: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        body: dict[str, Any] = {"parent": parent, "properties": properties}
        if children:
            body["children"] = children[:100]
        return self._request("POST", "/pages", body)

    def append_children(self, block_id: str, children: list[dict[str, Any]]) -> dict[str, Any]:
        if not children or len(children) > 100:
            raise ValueError("Notion append requires 1-100 bounded children")
        return self._request("PATCH", f"/blocks/{block_id}/children", {"children": children})

    def update_block(self, block_id: str, properties: dict[str, Any]) -> dict[str, Any]:
        if not properties:
            raise ValueError("Notion block update requires properties")
        return self._request("PATCH", f"/blocks/{block_id}", properties)

    def _request(self, method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        request = urllib.request.Request(
            self.settings.base_url.rstrip("/") + path,
            method=method,
            headers={
                "Authorization": f"Bearer {self.settings.token}",
                "Notion-Version": self.settings.api_version,
                "Content-Type": "application/json",
            },
            data=json.dumps(body).encode() if body is not None else None,
        )
        for attempt in range(self.settings.max_retries + 1):
            try:
                with self._opener(request, timeout=self.settings.timeout_seconds) as response:
                    payload = response.read().decode()
                    return json.loads(payload) if payload else {}
            except urllib.error.HTTPError as exc:
                retryable = exc.code == 429 or 500 <= exc.code < 600
                if retryable and attempt < self.settings.max_retries:
                    retry_after = float(exc.headers.get("Retry-After", "1"))
                    self._sleep(min(max(retry_after, 0.1), 30.0) * (attempt + 1))
                    continue
                raise NotionApiError(exc.code, "Notion request failed", retryable=retryable) from exc
            except (urllib.error.URLError, TimeoutError) as exc:
                if attempt < self.settings.max_retries:
                    self._sleep(min(2 ** attempt, 30))
                    continue
                raise NotionApiError(503, "Notion is unavailable", retryable=True) from exc
            except json.JSONDecodeError as exc:
                raise NotionApiError(502, "Notion returned malformed JSON") from exc
