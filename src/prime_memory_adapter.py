"""Small Phase 0 Hindsight adapter probe with project-bound bank identity."""

from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class AdapterResult:
    status: str
    payload: dict
    reason: str | None = None


class PrimeMemoryAdapter:
    """Keep Hindsight behind a PRIME-owned, project-bound contract."""

    def __init__(self, base_url: str, project_id: str, timeout_seconds: float = 30.0) -> None:
        if not project_id or "/" in project_id or project_id.startswith("."):
            raise ValueError("invalid project_id")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
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
            with urlopen(request, timeout=self.timeout_seconds) as response:
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

    def list_mental_models(self) -> AdapterResult:
        try:
            path = f"/v1/default/banks/{self.bank_id}/mental-models?{urlencode({'detail': 'full', 'limit': 1000})}"
            return AdapterResult("CURRENT", self._request("GET", path))
        except RuntimeError as exc:
            return AdapterResult("UNAVAILABLE", {}, str(exc))

    def create_mental_model(
        self,
        name: str,
        source_query: str,
        model_id: str | None = None,
        max_tokens: int = 2048,
    ) -> AdapterResult:
        body: dict[str, object] = {
            "name": name,
            "source_query": source_query,
            "max_tokens": max_tokens,
            "trigger": {"refresh_after_consolidation": False},
        }
        if model_id:
            body["id"] = model_id
        try:
            return AdapterResult(
                "CURRENT",
                self._request("POST", f"/v1/default/banks/{self.bank_id}/mental-models", body),
            )
        except RuntimeError as exc:
            return AdapterResult("UNAVAILABLE", {}, str(exc))

    def mental_model_operation(self, operation_id: str) -> AdapterResult:
        if not operation_id or "/" in operation_id:
            raise ValueError("invalid operation_id")
        try:
            return AdapterResult(
                "CURRENT",
                self._request(
                    "GET",
                    f"/v1/default/banks/{self.bank_id}/operations/{operation_id}",
                ),
            )
        except RuntimeError as exc:
            return AdapterResult("UNAVAILABLE", {}, str(exc))

    def get_mental_model(self, model_id: str) -> AdapterResult:
        if not model_id or "/" in model_id:
            raise ValueError("invalid mental_model_id")
        try:
            path = f"/v1/default/banks/{self.bank_id}/mental-models/{model_id}?{urlencode({'detail': 'full'})}"
            return AdapterResult("CURRENT", self._request("GET", path))
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
