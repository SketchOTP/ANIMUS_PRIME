from __future__ import annotations

import hashlib
import json
import os
import secrets
import subprocess
import uuid
import time
from pathlib import Path
from typing import Any

from .config import NodeSettings


class NodeService:
    def __init__(self, settings: NodeSettings):
        self.settings = settings
        self.state = self._load()

    def _load(self) -> dict[str, Any]:
        if not self.settings.state_file.exists():
            return {"node_id": None, "token_hash": None, "revoked": False, "enrollment_hash": None, "bootstrap_consumed": False, "approval_state": "UNENROLLED", "last_heartbeat": None, "allowed_roots": []}
        try:
            return json.loads(self.settings.state_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"node_id": None, "token_hash": None, "revoked": True, "enrollment_hash": None, "bootstrap_consumed": True, "approval_state": "REVOKED"}

    def _save(self) -> None:
        self.settings.state_file.parent.mkdir(parents=True, exist_ok=True)
        temp = self.settings.state_file.with_suffix(".tmp")
        temp.write_text(json.dumps(self.state, sort_keys=True), encoding="utf-8")
        os.chmod(temp, 0o600)
        temp.replace(self.settings.state_file)

    def enroll(self, credential: str) -> tuple[str, str]:
        accepted = not self.state.get("bootstrap_consumed") and secrets.compare_digest(credential, self.settings.bootstrap_credential)
        if self.state.get("revoked") and self.state.get("enrollment_hash"):
            accepted = accepted or secrets.compare_digest(self.digest(credential), self.state["enrollment_hash"])
        if not accepted:
            raise PermissionError("invalid node bootstrap credential")
        if self.state.get("node_id") and not self.state.get("revoked"):
            raise ValueError("node is already enrolled")
        node_id = f"node_{uuid.uuid4().hex}"
        token = secrets.token_urlsafe(32)
        prior_audit = list(self.state.get("audit") or [])
        self.state = {
            "node_id": node_id,
            "token_hash": self.digest(token),
            "enrollment_hash": None,
            "bootstrap_consumed": True,
            "revoked": False,
            "name": self.settings.node_name,
            "protocol_version": self.settings.protocol_version,
            "capabilities": list(self.settings.capabilities),
            "approval_state": "APPROVED",
            "last_heartbeat": None,
            "allowed_roots": [str(root) for root in self.settings.allowed_roots],
            "audit": prior_audit,
        }
        self._record_audit("REENROLLED" if prior_audit else "ENROLLED")
        self._save()
        return node_id, token

    def authenticate(self, token: str) -> bool:
        return bool(self.state.get("node_id") and not self.state.get("revoked") and secrets.compare_digest(self.digest(token), self.state.get("token_hash", "")))

    def revoke(self) -> str:
        self.state["revoked"] = True
        self.state["approval_state"] = "REVOKED"
        replacement = secrets.token_urlsafe(32)
        self.state["enrollment_hash"] = self.digest(replacement)
        self._record_audit("REVOKED")
        self._save()
        return replacement

    def rotate(self, token: str) -> str:
        if not self.authenticate(token):
            raise PermissionError("node authentication required")
        replacement = secrets.token_urlsafe(32)
        self.state["token_hash"] = self.digest(replacement)
        self._record_audit("ROTATED")
        self._save()
        return replacement

    def status(self) -> dict[str, Any]:
        last = self.state.get("last_heartbeat")
        health = "OFFLINE" if self.state.get("revoked") else "ONLINE"
        if last and time.time() - float(last) > self.settings.heartbeat_stale_seconds:
            health = "STALE"
        return {
            "node_id": self.state.get("node_id"),
            "name": self.state.get("name", self.settings.node_name),
            "protocol_version": self.state.get("protocol_version", self.settings.protocol_version),
            "capabilities": self.state.get("capabilities", list(self.settings.capabilities)),
            "allowed_roots": list(self.state.get("allowed_roots") or [str(root) for root in self.settings.allowed_roots]),
            "revoked": bool(self.state.get("revoked")),
            "approval_state": self.state.get("approval_state", "UNENROLLED"),
            "health": health,
            "node_version": self.settings.node_version,
            "protocol_versions": list(self.settings.supported_protocols),
            "service": "prime-node",
        }

    def heartbeat(self, protocol_version: str) -> dict[str, Any]:
        if protocol_version not in self.settings.supported_protocols:
            raise ValueError("incompatible node control protocol")
        self.state["last_heartbeat"] = time.time()
        self._save()
        return {"status": "ONLINE", "node_id": self.state.get("node_id"), "protocol_version": self.settings.protocol_version, "node_version": self.settings.node_version, "capabilities": self.state.get("capabilities", [])}

    def set_allowed_roots(self, roots: list[str]) -> list[str]:
        normalized = []
        for raw in roots:
            root = Path(raw).expanduser().resolve(strict=True)
            if not root.is_dir():
                raise NotADirectoryError(str(root))
            if str(root) not in normalized:
                normalized.append(str(root))
        self.state["allowed_roots"] = normalized
        self._save()
        return normalized

    def diagnostics(self) -> dict[str, Any]:
        result = self.status()
        result["state_file"] = str(self.settings.state_file)
        result["credential_present"] = bool(self.state.get("token_hash"))
        result["audit_events"] = len(self.state.get("audit") or [])
        return result

    def _record_audit(self, event: str) -> None:
        audit = list(self.state.get("audit") or [])
        audit.append({"event": event, "node_id": self.state.get("node_id"), "at": time.time()})
        self.state["audit"] = audit[-128:]

    def repository_snapshot(self, requested: str) -> dict[str, Any]:
        path = self.safe_path(requested)
        result = self.inspect_repository(str(path))
        result["head"] = self._git(path, ["rev-parse", "HEAD"], allow_failure=True) or None
        result["status"] = self._git(path, ["status", "--porcelain"], allow_failure=True)
        return result

    def safe_path(self, requested: str) -> Path:
        candidate = Path(requested).expanduser().resolve(strict=True)
        roots = tuple(Path(item).resolve() for item in (self.state.get("allowed_roots") or [str(root) for root in self.settings.allowed_roots]))
        if not any(candidate == root or root in candidate.parents for root in roots):
            raise PermissionError("path is outside configured Node roots")
        return candidate

    def read_file(self, requested: str) -> dict[str, Any]:
        path = self.safe_path(requested)
        if not path.is_file():
            raise IsADirectoryError("requested path is not a regular file")
        if path.stat().st_size > self.settings.max_read_bytes:
            raise ValueError("file exceeds Node read limit")
        data = path.read_bytes()
        if b"\x00" in data:
            raise ValueError("binary files are not readable through the text endpoint")
        return {"path": str(path), "content": data.decode("utf-8"), "content_hash": hashlib.sha256(data).hexdigest()}

    def inspect_repository(self, requested: str) -> dict[str, Any]:
        path = self.safe_path(requested)
        values = self._git(path, ["rev-parse", "--show-toplevel", "--git-common-dir", "--is-bare-repository"]).splitlines()
        if len(values) < 3:
            raise ValueError("Git returned an incomplete repository identity")
        top = Path(values[0]).resolve()
        common = Path(values[1])
        if not common.is_absolute():
            common = (path / common).resolve()
        is_bare = values[2].strip().lower() == "true"
        if is_bare:
            raise ValueError("bare repositories are not supported")
        fingerprint = hashlib.sha256(str(common).encode("utf-8")).hexdigest()
        branch = self._git(path, ["symbolic-ref", "--short", "HEAD"], allow_failure=True) or "UNBORN"
        return {"canonical_path": str(top), "git_common_dir": str(common), "is_bare": False, "branch": branch, "identity_fingerprint": fingerprint}

    @staticmethod
    def _git(path: Path, args: list[str], allow_failure: bool = False) -> str:
        try:
            completed = subprocess.run(["git", "-C", str(path), *args], check=True, capture_output=True, text=True, timeout=5)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            if allow_failure:
                return ""
            raise ValueError("path is not a readable Git working repository") from exc
        return completed.stdout.strip()

    @staticmethod
    def digest(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()
