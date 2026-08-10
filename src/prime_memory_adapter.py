"""Small Phase 0 Hindsight adapter probe with project-bound bank identity."""

from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class AdapterResult:
    status: str
    payload: dict
    reason: str | None = None


class PrimeMemoryAdapter:
    """Keep Hindsight behind a PRIME-owned, project-bound contract."""

    def __init__(self, base_url: str, project_id: str) -> None:
        if not project_id or "/" in project_id or project_id.startswith("."):
            raise ValueError("invalid project_id")
        self.base_url = base_url.rstrip("/")
        self.project_id = project_id
        self.bank_id = f"prime-{project_id}"

    def _request(self, method: str, path: str, body: dict | None = None) -> dict:
        data = None if body is None else json.dumps(body).encode()
        request = Request(
            f"{self.base_url}{path}",
            data=data,
            method=method,
            headers={"content-type": "application/json"},
        )
        try:
            with urlopen(request, timeout=10) as response:
                return json.loads(response.read() or b"{}")
        except (HTTPError, URLError, TimeoutError) as exc:
            raise RuntimeError("hindsight unavailable") from exc

    def health(self) -> AdapterResult:
        try:
            return AdapterResult("CURRENT", self._request("GET", "/health"))
        except RuntimeError as exc:
            return AdapterResult("UNAVAILABLE", {}, str(exc))

    def create_bank(self) -> AdapterResult:
        try:
            return AdapterResult(
                "CURRENT",
                self._request("PUT", f"/v1/default/banks/{self.bank_id}", {"name": self.project_id, "enable_observations": False}),
            )
        except RuntimeError as exc:
            return AdapterResult("UNAVAILABLE", {}, str(exc))

    def retain_verified(self, content: str, document_id: str) -> AdapterResult:
        try:
            payload = self._request(
                "POST",
                f"/v1/default/banks/{self.bank_id}/memories",
                {"items": [{"content": content, "document_id": document_id}], "async": False},
            )
            recalled = self._request(
                "POST",
                f"/v1/default/banks/{self.bank_id}/memories/recall",
                {"query": content},
            )
        except RuntimeError as exc:
            return AdapterResult("UNAVAILABLE", {}, str(exc))
        if not recalled.get("results"):
            return AdapterResult("DEGRADED", payload, "Hindsight acknowledged retain without a durable recallable result")
        return AdapterResult("CURRENT", {"retain": payload, "recall": recalled})

    def recall(self, query: str) -> AdapterResult:
        try:
            return AdapterResult("CURRENT", self._request("POST", f"/v1/default/banks/{self.bank_id}/memories/recall", {"query": query}))
        except RuntimeError as exc:
            return AdapterResult("UNAVAILABLE", {}, str(exc))

    def reflect(self, query: str) -> AdapterResult:
        try:
            return AdapterResult("CURRENT", self._request("POST", f"/v1/default/banks/{self.bank_id}/reflect", {"query": query, "budget": "low", "max_tokens": 256}))
        except RuntimeError as exc:
            return AdapterResult("UNAVAILABLE", {}, str(exc))

    def export_template(self) -> AdapterResult:
        try:
            return AdapterResult("CURRENT", self._request("GET", f"/v1/default/banks/{self.bank_id}/export"))
        except RuntimeError as exc:
            return AdapterResult("UNAVAILABLE", {}, str(exc))

    def import_template(self, manifest: dict) -> AdapterResult:
        try:
            return AdapterResult("CURRENT", self._request("POST", f"/v1/default/banks/{self.bank_id}/import", manifest))
        except RuntimeError as exc:
            return AdapterResult("UNAVAILABLE", {}, str(exc))

    def delete_bank(self) -> AdapterResult:
        try:
            return AdapterResult("CURRENT", self._request("DELETE", f"/v1/default/banks/{self.bank_id}"))
        except RuntimeError as exc:
            return AdapterResult("UNAVAILABLE", {}, str(exc))
