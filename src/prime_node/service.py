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
from src.prime_core.authority import REQUIRED_AUTHORITY_FILES
from src.prime_core.node_trust import csr_fingerprint, verify_bootstrap


class NodeService:
    def __init__(self, settings: NodeSettings):
        self.settings = settings
        self.state = self._load()

    def _load(self) -> dict[str, Any]:
        if not self.settings.state_file.exists():
            return {"node_id": self.settings.node_id, "token_hash": None, "revoked": False, "bootstrap_consumed": False, "approval_state": "UNENROLLED", "last_heartbeat": None, "allowed_roots": [str(root) for root in self.settings.allowed_roots], "consumed_bootstrap_digests": []}
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

    def enroll(self, credential: str, node_id: str, csr_pem: str) -> dict[str, Any]:
        if not self.settings.bootstrap_public_key_file:
            raise PermissionError("Node bootstrap verification is not configured")
        proof = verify_bootstrap(credential, self.settings.bootstrap_public_key_file)
        if proof.get("node_id") != self.settings.node_id or node_id != self.settings.node_id:
            raise PermissionError("Node identity does not match the governed enrollment")
        credential_digest = self.digest(credential)
        if credential_digest in set(self.state.get("consumed_bootstrap_digests") or []):
            raise PermissionError("node bootstrap proof was already consumed")
        if self.state.get("approval_state") in {"APPROVED", "ACTIVE"} and not self.state.get("revoked"):
            raise ValueError("node is already enrolled")
        fingerprint = csr_fingerprint(csr_pem)
        self.state.update({
            "node_id": self.settings.node_id,
            "token_hash": None,
            "revoked": False,
            "bootstrap_consumed": True,
            "consumed_bootstrap_digests": [*(self.state.get("consumed_bootstrap_digests") or []), credential_digest][-32:],
            "challenge_id": proof["challenge_id"],
            "csr_pem": csr_pem,
            "csr_fingerprint": fingerprint,
            "approval_state": "PENDING_OPERATOR_APPROVAL",
            "trust_state": "BOOTSTRAP_PROOF_RECEIVED",
            "last_heartbeat": None,
        })
        self._record_audit("NODE_PROOF_RECEIVED")
        self._save()
        return {"challenge_id": proof["challenge_id"], "node_id": self.settings.node_id, "csr_fingerprint": fingerprint, "approval_state": "PENDING_OPERATOR_APPROVAL"}

    def approve(self, certificate_pem: str, token: str, metadata: dict[str, Any]) -> dict[str, Any]:
        if self.state.get("approval_state") != "PENDING_OPERATOR_APPROVAL":
            raise ValueError("Node is not pending operator approval")
        target = self.settings.tls_cert_file
        if not target:
            raise ValueError("Node TLS certificate path is not configured")
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(".new")
        temporary.write_text(certificate_pem, encoding="ascii")
        os.chmod(temporary, 0o600)
        temporary.replace(target)
        self.state.update({"token_hash": self.digest(token), "approval_state": "APPROVED", "trust_state": "ACTIVE_CREDENTIAL_PENDING_RESTART", "revoked": False, "certificate": metadata, "csr_pem": None})
        self._record_audit("OPERATOR_APPROVED")
        self._save()
        return {"node_id": self.state.get("node_id"), "approval_state": self.state.get("approval_state"), "certificate": metadata}

    def reject(self) -> None:
        self.state.update({"approval_state": "REJECTED", "trust_state": "REVOKED", "revoked": True, "csr_pem": None})
        self._record_audit("OPERATOR_REJECTED")
        self._save()

    def authenticate(self, token: str) -> bool:
        return bool(self.state.get("node_id") and self.state.get("approval_state") in {"APPROVED", "ACTIVE"} and not self.state.get("revoked") and secrets.compare_digest(self.digest(token), self.state.get("token_hash", "")))

    def revoke(self) -> str:
        self.state["revoked"] = True
        self.state["approval_state"] = "REVOKED"
        self.state["trust_state"] = "REVOKED"
        self.state["token_hash"] = None
        self._record_audit("REVOKED")
        self._save()
        return "REVOKED"

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
            "health": "PENDING" if self.state.get("approval_state") == "PENDING_OPERATOR_APPROVAL" else health,
            "node_version": self.settings.node_version,
            "protocol_versions": list(self.settings.supported_protocols),
            "service": "prime-node",
        }

    def heartbeat(self, protocol_version: str) -> dict[str, Any]:
        if protocol_version not in self.settings.supported_protocols:
            raise ValueError("incompatible node control protocol")
        if self.state.get("approval_state") not in {"APPROVED", "ACTIVE"} or self.state.get("revoked"):
            raise PermissionError("Node is not approved")
        self.state["last_heartbeat"] = time.time()
        self.state["approval_state"] = "ACTIVE"
        self.state["trust_state"] = "ACTIVE"
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

    def list_directory(self, requested: str) -> dict[str, Any]:
        path = self.safe_path(requested)
        if not path.is_dir():
            raise NotADirectoryError("requested path is not a directory")
        entries = []
        for entry in sorted(path.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))[:200]:
            if entry.name == ".git":
                continue
            item = {"name": entry.name, "path": str(entry), "kind": "directory" if entry.is_dir() else "file"}
            if entry.is_file():
                item["size_bytes"] = entry.stat().st_size
            entries.append(item)
        return {"path": str(path), "entries": entries}

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

    def create_repository(self, parent_path: str, repository_name: str, operation_id: str) -> dict[str, Any]:
        if not repository_name or repository_name in {".", ".."} or Path(repository_name).name != repository_name:
            raise ValueError("repository name must be one directory name")
        operations = dict(self.state.get("repository_operations") or {})
        existing = operations.get(operation_id)
        if existing:
            return {**existing, "idempotent_replay": True}
        parent = self.safe_path(parent_path)
        if not parent.is_dir():
            raise NotADirectoryError("repository parent is not a directory")
        target = parent / repository_name
        if target.exists() or target.is_symlink():
            raise FileExistsError("repository target already exists")
        try:
            target.mkdir()
            subprocess.run(
                ["git", "-C", str(target), "init", "--initial-branch=main"],
                check=True,
                capture_output=True,
                text=True,
                timeout=10,
            )
            result = self.inspect_repository(str(target))
        except Exception:
            if target.is_dir() and not any(target.iterdir()):
                target.rmdir()
            raise
        result = {**result, "operation_id": operation_id, "created": True, "idempotent_replay": False}
        operations[operation_id] = result
        self.state["repository_operations"] = dict(list(operations.items())[-128:])
        self._record_audit("REPOSITORY_CREATED")
        self._save()
        return result

    def bootstrap_authority(self, repository_path: str, files: dict[str, str], operation_id: str) -> dict[str, Any]:
        if set(files) != set(REQUIRED_AUTHORITY_FILES):
            raise ValueError("authority bootstrap must contain the exact authority-file-contract-v1 file set")
        if sum(len(content.encode("utf-8")) for content in files.values()) > 1024 * 1024:
            raise ValueError("authority bootstrap exceeds the bounded payload size")
        repository = self.safe_path(repository_path)
        self.inspect_repository(str(repository))
        operations = dict(self.state.get("authority_operations") or {})
        if operation_id in operations:
            return {**operations[operation_id], "idempotent_replay": True}
        mismatched = []
        for relative, content in files.items():
            target = repository / relative
            if target.exists() and (not target.is_file() or target.read_text(encoding="utf-8") != content):
                mismatched.append(relative)
        if mismatched:
            raise FileExistsError("authority provisioning would overwrite existing authority")
        written = []
        for relative, content in files.items():
            target = repository / relative
            if target.exists():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_suffix(target.suffix + ".prime-new")
            temporary.write_text(content, encoding="utf-8")
            os.chmod(temporary, 0o644)
            temporary.replace(target)
            written.append(relative)
        hashes = {relative: hashlib.sha256((repository / relative).read_bytes()).hexdigest() for relative in REQUIRED_AUTHORITY_FILES}
        result = {
            "repository_path": str(repository),
            "contract_version": "authority-file-contract-v1",
            "valid": True,
            "files": hashes,
            "written_files": written,
            "operation_id": operation_id,
            "idempotent_replay": False,
        }
        operations[operation_id] = result
        self.state["authority_operations"] = dict(list(operations.items())[-128:])
        self._record_audit("AUTHORITY_BOOTSTRAPPED")
        self._save()
        return result

    def write_project_goal(self, repository_path: str, content: str, content_hash: str) -> dict[str, Any]:
        if hashlib.sha256(content.encode("utf-8")).hexdigest() != content_hash:
            raise ValueError("PROJECT_GOAL.md content hash mismatch")
        repository = self.safe_path(repository_path)
        self.inspect_repository(str(repository))
        goal_path = repository / ".agent" / "PROJECT_GOAL.md"
        if not goal_path.parent.is_dir():
            raise FileNotFoundError("authority must be provisioned before PROJECT_GOAL.md approval")
        temporary = goal_path.with_suffix(".md.prime-new")
        temporary.write_text(content, encoding="utf-8")
        os.chmod(temporary, 0o644)
        temporary.replace(goal_path)
        self._record_audit("PROJECT_GOAL_APPROVED")
        self._save()
        return {"path": str(goal_path), "content_hash": content_hash, "written": True}

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
