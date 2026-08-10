from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class BackupError(RuntimeError):
    pass


class BackupCoordinator:
    """Build and preflight encrypted PRIME continuity bundles.

    The bundle is deliberately metadata-oriented: repositories and external
    Notion pages remain authoritative outside PRIME. Sensitive bundle bytes are
    encrypted with the host OpenSSL implementation; plaintext credentials are
    rejected before packaging.
    """

    def __init__(self, openssl: str = "openssl"):
        self.openssl = openssl

    def build_bundle(self, destination: Path, components: dict[str, Any], passphrase: str) -> dict[str, Any]:
        if not passphrase:
            raise BackupError("backup encryption passphrase is required")
        self._reject_secrets(components)
        destination.parent.mkdir(parents=True, exist_ok=True)
        captured_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        manifest = {
            "format": "prime-continuity/v1",
            "captured_at": captured_at,
            "components": sorted(components),
            "high_water_marks": {name: value.get("revision") for name, value in components.items() if isinstance(value, dict)},
        }
        manifest_bytes = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
        with tempfile.TemporaryDirectory(prefix="prime-backup-") as temp_dir:
            plain = Path(temp_dir) / "bundle.zip"
            with zipfile.ZipFile(plain, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("manifest.json", manifest_bytes)
                for name, value in sorted(components.items()):
                    archive.writestr(f"components/{name}.json", json.dumps(value, sort_keys=True).encode())
            self._crypt(plain, destination, passphrase, decrypt=False)
        digest = hashlib.sha256(destination.read_bytes()).hexdigest()
        return {"locator": str(destination), "content_hash": digest, "manifest": manifest, "status": "VERIFIED"}

    def preflight_restore(self, bundle: Path, passphrase: str) -> dict[str, Any]:
        if not bundle.is_file():
            raise BackupError("backup bundle does not exist")
        with tempfile.TemporaryDirectory(prefix="prime-restore-") as temp_dir:
            encrypted = bundle
            plain = Path(temp_dir) / "bundle.zip"
            self._crypt(encrypted, plain, passphrase, decrypt=True)
            try:
                with zipfile.ZipFile(plain) as archive:
                    manifest = json.loads(archive.read("manifest.json"))
                    names = sorted(name.removeprefix("components/").removesuffix(".json") for name in archive.namelist() if name.startswith("components/"))
            except (OSError, KeyError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
                raise BackupError("backup manifest is invalid or incompatible") from exc
        if manifest.get("format") != "prime-continuity/v1" or names != manifest.get("components"):
            raise BackupError("backup manifest/component set is inconsistent")
        return {"status": "READY", "manifest": manifest, "components": names}

    def _crypt(self, source: Path, destination: Path, passphrase: str, *, decrypt: bool) -> None:
        operation = "-d" if decrypt else "-e"
        command = [self.openssl, "enc", "-aes-256-cbc", "-pbkdf2", "-iter", "600000", "-salt", operation, "-in", str(source), "-out", str(destination), "-pass", "stdin"]
        result = subprocess.run(command, input=passphrase.encode(), capture_output=True, check=False)
        if result.returncode != 0:
            raise BackupError(result.stderr.decode(errors="replace").strip() or "backup encryption failed")

    @staticmethod
    def _reject_secrets(value: Any, path: str = "root") -> None:
        secret_names = {"password", "passphrase", "secret", "token", "api_key", "private_key", "credential"}
        if isinstance(value, dict):
            for key, child in value.items():
                if str(key).lower() in secret_names:
                    raise BackupError(f"plaintext credential field is not allowed in backup: {path}.{key}")
                BackupCoordinator._reject_secrets(child, f"{path}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                BackupCoordinator._reject_secrets(child, f"{path}[{index}]")
