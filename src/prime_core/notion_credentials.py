from __future__ import annotations

"""Secret-safe reuse of an existing MyAssistant Notion authorization.

Only a reference to the runtime secret source is durable.  The secret itself is
resolved on demand and is never returned by this module or written to the
database, logs, evidence, or state snapshots.
"""

import json
import os
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .notion_api import NotionApiClient, NotionApiSettings


MYASSISTANT_ENV = "NOTION_READONLY_KEY"
MYASSISTANT_REFERENCE = "env/myassistant/notion-readonly"
KNOWN_GRANTED_PAGE = "3b3833cb-27ff-8039-bf9e-f4f731df0633"


@dataclass(frozen=True)
class CredentialImport:
    status: str
    credential_reference: str | None
    source_environment: str
    source_present: bool
    changed: bool
    reason: str | None = None

    def public(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "credential_reference": self.credential_reference,
            "source_environment": self.source_environment,
            "source_present": self.source_present,
            "changed": self.changed,
            "reason": self.reason,
        }


class NotionCredentialRegistry:
    """Durable reference metadata plus an environment-backed secret resolver."""

    def __init__(self, state_path: Path | None = None, environ: dict[str, str] | None = None):
        self.state_path = state_path
        self.environ = environ if environ is not None else os.environ
        self.state: dict[str, Any] = self._load()

    def _load(self) -> dict[str, Any]:
        if not self.state_path or not self.state_path.is_file():
            return {}
        try:
            value = json.loads(self.state_path.read_text(encoding="utf-8"))
            return value if isinstance(value, dict) else {}
        except (OSError, ValueError, TypeError):
            return {"status": "DEGRADED", "reason": "credential metadata snapshot unreadable"}

    def _persist(self) -> None:
        if not self.state_path:
            return
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.state_path.with_name(self.state_path.name + ".tmp")
        temporary.write_text(json.dumps(self.state, sort_keys=True), encoding="utf-8")
        os.replace(temporary, self.state_path)

    def import_myassistant(self, existing_reference: str | None = None) -> CredentialImport:
        present = bool(self.environ.get(MYASSISTANT_ENV))
        current = existing_reference or self.state.get("credential_reference")
        if current and current != MYASSISTANT_REFERENCE:
            return CredentialImport(
                "CONFLICT",
                current,
                MYASSISTANT_ENV,
                present,
                False,
                "an existing deliberate PRIME credential reference was preserved",
            )
        if not present:
            return CredentialImport(
                "SOURCE_ABSENT",
                current,
                MYASSISTANT_ENV,
                False,
                False,
                "MyAssistant runtime authorization is not present in this process",
            )
        already_imported = current == MYASSISTANT_REFERENCE
        self.state = {
            **self.state,
            "credential_reference": MYASSISTANT_REFERENCE,
            "source_kind": "MYASSISTANT_RUNTIME_ENVIRONMENT",
            "source_environment": MYASSISTANT_ENV,
            "migration_status": "NOOP" if already_imported else "IMPORTED",
            "import_id": self.state.get("import_id") or f"notion-credential-{uuid.uuid4().hex}",
            "updated_at": self.state.get("updated_at") or "runtime-import",
        }
        self._persist()
        return CredentialImport(
            "NOOP" if already_imported else "IMPORTED",
            MYASSISTANT_REFERENCE,
            MYASSISTANT_ENV,
            True,
            not already_imported,
        )

    def public_status(self) -> dict[str, Any]:
        reference = self.state.get("credential_reference")
        return {
            "status": self.state.get("migration_status", self.state.get("status", "UNCONFIGURED")),
            "credential_reference": reference,
            "source_kind": self.state.get("source_kind"),
            "source_environment": self.state.get("source_environment", MYASSISTANT_ENV),
            "source_present": bool(self.environ.get(MYASSISTANT_ENV)),
            "known_granted_page": KNOWN_GRANTED_PAGE,
            "capabilities": self.state.get("capabilities", {}),
        }

    def resolve_token(self) -> str:
        if self.state.get("credential_reference") != MYASSISTANT_REFERENCE:
            raise LookupError("Notion credential reference is not configured")
        token = self.environ.get(MYASSISTANT_ENV)
        if not token:
            raise LookupError("Notion credential source is unavailable")
        return token

    def client(self) -> NotionApiClient:
        return NotionApiClient(NotionApiSettings(token=self.resolve_token()))

    def record_capabilities(self, capabilities: dict[str, Any]) -> dict[str, Any]:
        self.state = {**self.state, "capabilities": capabilities}
        self._persist()
        return self.public_status()
