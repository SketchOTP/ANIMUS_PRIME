from __future__ import annotations

import base64
import hashlib
import json
import os
import tempfile
import uuid
import zipfile
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

class BackupError(RuntimeError):
    pass


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class BackupCoordinator:
    """Create and restore a coherent, encrypted PRIME continuity artifact.

    Repository source code remains an explicitly separate protection concern.
    The artifact contains canonical PRIME rows, managed Evidence bytes and
    PRIME-owned Git checkpoint bundles when present, plus truthful fidelity
    labels for rebuildable Hindsight/source-ledger state.
    """

    FORMAT = "prime-continuity/v2"
    SPEC_REVISION = "PRIME-SPEC-V1.0.0"
    PRIME_VERSION = "1.0.0"
    AAD = b"ANIMUS-PRIME-CONTINUITY-V2"
    PBKDF2_ITERATIONS = 600_000
    OMITTED_TABLES = {"schema_migrations", "operators", "sessions"}
    SECRET_NAMES = {"password", "passphrase", "secret", "token", "api_key", "private_key", "credential", "recovery"}

    def build_bundle(
        self,
        destination: Path,
        components: dict[str, Any],
        passphrase: str,
        *,
        destination_class: str | None = None,
        manifest_fields: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self._reject_secrets(components)
        if len(passphrase) < 12:
            raise BackupError("backup encryption passphrase is required")
        destination.parent.mkdir(parents=True, exist_ok=True)
        captured_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        component_bytes = {
            name: json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
            for name, value in sorted(components.items())
        }
        manifest: dict[str, Any] = {
            "format": self.FORMAT,
            "backup_id": _new_id("backup"),
            "created_at": captured_at,
            "prime_version": self.PRIME_VERSION,
            "spec_revision": self.SPEC_REVISION,
            "schema_revision": "unknown",
            "source_high_water_mark": captured_at,
            "continuity": False,
            "project_ids": [],
            "component_inventory": sorted(component_bytes),
            "component_versions": {name: "v1" for name in component_bytes},
            "encryption_version": "AES-256-GCM/PBKDF2-HMAC-SHA256",
            "destination": str(destination),
            "destination_class": destination_class or self._destination_class(destination),
            "content_hashes": {name: hashlib.sha256(value).hexdigest() for name, value in component_bytes.items()},
            "high_water_marks": {
                name: value.get("revision") if isinstance(value, dict) else None
                for name, value in components.items()
            },
        }
        if manifest_fields:
            manifest.update(self._safe_manifest_fields(manifest_fields))
        manifest["component_inventory"] = sorted(component_bytes)
        manifest_bytes = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")
        with tempfile.TemporaryDirectory(prefix="prime-backup-") as temp_dir:
            plain = Path(temp_dir) / "bundle.zip"
            with zipfile.ZipFile(plain, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("manifest.json", manifest_bytes)
                for name, value in component_bytes.items():
                    archive.writestr(f"components/{name}.json", value)
            self._encrypt(plain.read_bytes(), destination, passphrase)
        verified = self.preflight_restore(destination, passphrase)
        digest = hashlib.sha256(destination.read_bytes()).hexdigest()
        return {
            "backup_id": manifest["backup_id"],
            "locator": str(destination),
            "content_hash": digest,
            "manifest": verified["manifest"],
            "status": "VERIFIED",
        }

    def create_continuity_backup(
        self,
        settings: Any,
        destination: Path,
        passphrase: str,
        *,
        project_ids: list[str] | None = None,
        destination_class: str | None = None,
    ) -> dict[str, Any]:
        from .db import schema_version

        components = self.snapshot_components(settings, project_ids)
        projects = components["prime_postgresql"]["tables"].get("projects", [])
        ids = [row["project_id"] for row in projects if row.get("project_id")]
        high_water = self._high_water(components)
        manifest_fields = {
            "schema_revision": schema_version(settings),
            "project_ids": ids,
            "source_high_water_mark": high_water,
            "continuity": True,
            "component_inventory": sorted(components),
            "component_versions": {
                "prime_postgresql": schema_version(settings),
                "hindsight": "source-ledger/v1",
                "evidence": "evidence-lifecycle/v1",
                "historical_state": "historical-revisions/v1",
                "git_checkpoints": "git-bundle/v1",
                "configuration": "configuration-reference/v1",
                "repository_source_protection": "separate-concern/v1",
            },
        }
        result = self.build_bundle(
            destination,
            components,
            passphrase,
            destination_class=destination_class,
            manifest_fields=manifest_fields,
        )
        from .reliability_service import ReliabilityService

        ReliabilityService(settings).record_continuity_backup(result, ids)
        return result

    def snapshot_components(self, settings: Any, project_ids: list[str] | None = None) -> dict[str, Any]:
        from .db import connect, schema_version

        with connect(settings) as db:
            tables = [
                row["table_name"]
                for row in db.execute(
                    "SELECT table_name FROM information_schema.tables "
                    "WHERE table_schema='prime_core' AND table_type='BASE TABLE' ORDER BY table_name"
                ).fetchall()
                if row["table_name"] not in self.OMITTED_TABLES
            ]
            table_rows: dict[str, list[dict[str, Any]]] = {}
            column_types: dict[str, dict[str, str]] = {}
            for table in tables:
                column_info = db.execute(
                    "SELECT column_name,udt_name FROM information_schema.columns "
                    "WHERE table_schema='prime_core' AND table_name=%s ORDER BY ordinal_position",
                    (table,),
                ).fetchall()
                columns = [row["column_name"] for row in column_info]
                column_types[table] = {
                    row["column_name"]: row["udt_name"] for row in column_info
                }
                quoted_columns = ", ".join(self._quote_identifier(column) for column in columns)
                query = f"SELECT {quoted_columns} FROM prime_core.{self._quote_identifier(table)}"
                params: tuple[Any, ...] = ()
                if project_ids and "project_id" in columns:
                    query += " WHERE project_id = ANY(%s)"
                    params = (project_ids,)
                rows = db.execute(query, params).fetchall()
                table_rows[table] = [self._json_value(dict(row)) for row in rows]

        evidence_files: dict[str, str] = {}
        git_bundles: dict[str, str] = {}
        for row in table_rows.get("evidence_records", []):
            path = row.get("storage_path")
            if path and Path(path).is_file():
                evidence_files[row["evidence_id"]] = base64.b64encode(Path(path).read_bytes()).decode("ascii")
        for row in table_rows.get("git_history_checkpoints", []):
            path = row.get("bundle_locator")
            if path and Path(path).is_file():
                git_bundles[row["checkpoint_id"]] = base64.b64encode(Path(path).read_bytes()).decode("ascii")
        settings_rows = [row for row in table_rows.get("settings", []) if not row.get("secret_reference")]
        return {
            "prime_postgresql": {"revision": schema_version(settings), "fidelity": "EXACT", "tables": table_rows, "column_types": column_types},
            "hindsight": {
                "mode": "SOURCE_LEDGER_REBUILD",
                "fidelity": "REBUILDABLE_NOT_BIT_IDENTICAL",
                "ledger_tables": ["memory_records", "memory_corrections"],
            },
            "evidence": {
                "mode": "MANAGED_CONTENT_AND_REFERENCES",
                "fidelity": "EXACT_FOR_MANAGED_BYTES",
                "managed_files": evidence_files,
                "external_references": [
                    row for row in table_rows.get("evidence_records", [])
                    if row.get("storage_mode") != "MANAGED_COPY"
                ],
            },
            "historical_state": {
                "mode": "CANONICAL_POSTGRESQL_HISTORY",
                "fidelity": "EXACT",
                "tables": ["historical_revisions", "authority_revisions", "goal_revisions", "progress_assessments", "notion_projection_revisions", "source_references"],
            },
            "git_checkpoints": {
                "mode": "PRIME_OWNED_BUNDLE_WHEN_RETAINED",
                "fidelity": "EXACT_FOR_RETAINED_BUNDLES",
                "managed_bundles": git_bundles,
            },
            "configuration": {
                "mode": "NON_SECRET_CONFIGURATION_AND_REFERENCES",
                "fidelity": "EXACT_NON_SECRET_ONLY",
                "settings": settings_rows,
                "secrets": "REPROVISION_REQUIRED",
            },
            "repository_source_protection": {
                "mode": "SEPARATE_CONCERN",
                "protected": False,
                "limitations": ["uncommitted changes", "untracked files", "Git LFS content", "external submodules", "externally stored assets"],
            },
        }

    def preflight_restore(self, bundle: Path, passphrase: str) -> dict[str, Any]:
        payload = self._decrypt(bundle, passphrase)
        try:
            with zipfile.ZipFile(__import__("io").BytesIO(payload)) as archive:
                if archive.testzip() is not None:
                    raise BackupError("backup archive failed integrity test")
                names = set(archive.namelist())
                if "manifest.json" not in names or any(name.startswith("/") or ".." in Path(name).parts for name in names):
                    raise BackupError("backup manifest is invalid or unsafe")
                manifest = json.loads(archive.read("manifest.json"))
                if manifest.get("format") != self.FORMAT:
                    raise BackupError("backup format is incompatible")
                component_names = sorted(
                    name.removeprefix("components/").removesuffix(".json")
                    for name in names if name.startswith("components/") and name.endswith(".json")
                )
                if component_names != sorted(manifest.get("component_inventory", [])):
                    raise BackupError("backup manifest/component set is inconsistent")
                components = {}
                for name in component_names:
                    raw = archive.read(f"components/{name}.json")
                    expected = manifest.get("content_hashes", {}).get(name)
                    if expected != hashlib.sha256(raw).hexdigest():
                        raise BackupError(f"backup component hash mismatch: {name}")
                    components[name] = json.loads(raw)
        except BackupError:
            raise
        except (OSError, KeyError, json.JSONDecodeError, zipfile.BadZipFile, ValueError) as exc:
            raise BackupError("backup manifest is invalid or incompatible") from exc
        required = {"prime_postgresql", "hindsight", "evidence", "historical_state", "git_checkpoints", "configuration"}
        if manifest.get("continuity") and not required <= set(components):
            raise BackupError("backup is missing required continuity components")
        return {"status": "READY", "manifest": manifest, "components": components}

    def restore_bundle(
        self,
        settings: Any,
        bundle: Path,
        passphrase: str,
        *,
        replace: bool = False,
        safety_destination: Path | None = None,
        storage_root: Path | None = None,
        fail_after_tables: int | None = None,
    ) -> dict[str, Any]:
        preflight = self.preflight_restore(bundle, passphrase)
        components = preflight["components"]
        rows = components["prime_postgresql"]["tables"]
        column_types = components["prime_postgresql"].get("column_types", {})
        from .db import connect

        with connect(settings) as db:
            existing = db.execute("SELECT count(*) AS count FROM prime_core.projects").fetchone()["count"]
        if existing and not replace:
            raise BackupError("restore collision: target PRIME already contains projects")
        if replace:
            if safety_destination is None:
                raise BackupError("destructive restore requires a safety backup destination")
            self.create_continuity_backup(settings, safety_destination, passphrase, destination_class="same-host")
        from .db import transaction

        restore_id = _new_id("restore")
        with transaction(settings) as db:
            db.execute(
                "INSERT INTO prime_core.restore_workflows(restore_id,bundle_locator,status,current_step,started_at,updated_at) VALUES (%s,%s,'RUNNING','PREPARE',%s,%s)",
                (restore_id, str(bundle), _utcnow(), _utcnow()),
            )
        try:
            with transaction(settings) as db:
                if replace:
                    db.execute("TRUNCATE TABLE prime_core.projects CASCADE")
                    db.execute("TRUNCATE TABLE prime_core.nodes CASCADE")
                db.execute("SET session_replication_role = replica")
                processed_tables = 0
                for table, table_rows in rows.items():
                    if table in self.OMITTED_TABLES or not table_rows:
                        continue
                    columns = sorted(set(table_rows[0]))
                    quoted = ", ".join('"' + column.replace('"', '""') + '"' for column in columns)
                    table_name = '"' + table.replace('"', '""') + '"'
                    placeholders = ", ".join(["%s"] * len(columns))
                    for row in table_rows:
                        values = [
                            json.dumps(row.get(column)) if column_types.get(table, {}).get(column) in ("json", "jsonb") else row.get(column)
                            for column in columns
                        ]
                        db.execute(
                            f"INSERT INTO prime_core.{table_name} ({quoted}) VALUES ({placeholders}) ON CONFLICT DO NOTHING",
                            values,
                        )
                    processed_tables += 1
                    if fail_after_tables is not None and processed_tables >= fail_after_tables:
                        raise RuntimeError("deterministic qualification interruption")
                db.execute("SET session_replication_role = origin")
                restored_files = self._restore_managed_files(components, storage_root)
                for evidence_id, path in restored_files.get("evidence", {}).items():
                    db.execute("UPDATE prime_core.evidence_records SET storage_path=%s WHERE evidence_id=%s", (path, evidence_id))
                for checkpoint_id, path in restored_files.get("git_checkpoints", {}).items():
                    db.execute("UPDATE prime_core.git_history_checkpoints SET bundle_locator=%s WHERE checkpoint_id=%s", (path, checkpoint_id))
        except Exception as exc:
            with transaction(settings) as db:
                db.execute("UPDATE prime_core.restore_workflows SET status='REPAIR_REQUIRED',current_step='FAILED',error_code=%s,error_message=%s,updated_at=%s WHERE restore_id=%s", (type(exc).__name__, str(exc)[:500], _utcnow(), restore_id))
            raise BackupError("restore failed before completion") from exc
        with transaction(settings) as db:
            db.execute(
                "UPDATE prime_core.restore_workflows SET status='SUCCEEDED',current_step='COMPLETE',updated_at=%s,completed_at=%s WHERE restore_id=%s",
                (_utcnow(), _utcnow(), restore_id),
            )
        return {
            "status": "RESTORED",
            "restore_id": restore_id,
            "backup_id": preflight["manifest"]["backup_id"],
            "component_fidelity": {
                "prime_postgresql": "EXACT",
                "hindsight": "SOURCE_LEDGER_REBUILD",
                "evidence": "EXACT_FOR_MANAGED_BYTES",
                "historical_state": "EXACT",
                "git_checkpoints": "EXACT_FOR_RETAINED_BUNDLES",
                "configuration": "REPROVISION_REQUIRED_FOR_SECRETS",
            },
        }

    @staticmethod
    def _restore_managed_files(components: dict[str, Any], storage_root: Path | None) -> dict[str, dict[str, str]]:
        restored: dict[str, dict[str, str]] = {"evidence": {}, "git_checkpoints": {}}
        if storage_root is None:
            return restored
        storage_root.mkdir(parents=True, exist_ok=True)
        for evidence_id, encoded in components["evidence"].get("managed_files", {}).items():
            target = storage_root / f"{evidence_id}.evidence"
            target.write_bytes(base64.b64decode(encoded))
            restored["evidence"][evidence_id] = str(target)
        for checkpoint_id, encoded in components["git_checkpoints"].get("managed_bundles", {}).items():
            target = storage_root / f"{checkpoint_id}.bundle"
            target.write_bytes(base64.b64decode(encoded))
            restored["git_checkpoints"][checkpoint_id] = str(target)
        return restored

    def _encrypt(self, plaintext: bytes, destination: Path, passphrase: str) -> None:
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            from cryptography.hazmat.primitives.hashes import SHA256
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        except ImportError as exc:
            raise BackupError("authenticated backup encryption requires the pinned cryptography dependency") from exc
        salt = os.urandom(16)
        nonce = os.urandom(12)
        key = PBKDF2HMAC(algorithm=SHA256(), length=32, salt=salt, iterations=self.PBKDF2_ITERATIONS).derive(passphrase.encode())
        ciphertext = AESGCM(key).encrypt(nonce, plaintext, self.AAD)
        envelope = {
            "format": self.FORMAT,
            "encryption": "AES-256-GCM",
            "kdf": "PBKDF2-HMAC-SHA256",
            "iterations": self.PBKDF2_ITERATIONS,
            "salt": base64.b64encode(salt).decode("ascii"),
            "nonce": base64.b64encode(nonce).decode("ascii"),
            "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
        }
        destination.write_bytes(b"PRIMEBACKUP\x00" + json.dumps(envelope, sort_keys=True, separators=(",", ":")).encode("utf-8"))

    def _decrypt(self, bundle: Path, passphrase: str) -> bytes:
        if not bundle.is_file():
            raise BackupError("backup bundle does not exist")
        try:
            raw = bundle.read_bytes()
            if not raw.startswith(b"PRIMEBACKUP\x00"):
                raise BackupError("backup envelope is invalid")
            envelope = json.loads(raw[len(b"PRIMEBACKUP\x00"):])
            if envelope.get("format") != self.FORMAT or envelope.get("encryption") != "AES-256-GCM":
                raise BackupError("backup encryption format is incompatible")
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            from cryptography.hazmat.primitives.hashes import SHA256
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            salt = base64.b64decode(envelope["salt"], validate=True)
            nonce = base64.b64decode(envelope["nonce"], validate=True)
            ciphertext = base64.b64decode(envelope["ciphertext"], validate=True)
            key = PBKDF2HMAC(algorithm=SHA256(), length=32, salt=salt, iterations=int(envelope["iterations"])).derive(passphrase.encode())
            return AESGCM(key).decrypt(nonce, ciphertext, self.AAD)
        except BackupError:
            raise
        except Exception as exc:
            raise BackupError("backup authentication or decryption failed") from exc

    def _destination_class(self, destination: Path) -> str:
        try:
            target = destination.resolve()
            while not target.exists() and target != target.parent:
                target = target.parent
            return "off-machine" if os.stat(target).st_dev != os.stat(Path.cwd().resolve()).st_dev else "same-host"
        except OSError:
            return "operator-selected"

    @staticmethod
    def _quote_identifier(identifier: str) -> str:
        return '"' + identifier.replace('"', '""') + '"'

    def _high_water(self, components: dict[str, Any]) -> str:
        values = []
        for component in components.values():
            if isinstance(component, dict) and isinstance(component.get("tables"), dict):
                for rows in component["tables"].values():
                    for row in rows:
                        for key in ("updated_at", "observed_at", "created_at", "captured_at", "occurred_at"):
                            if row.get(key):
                                values.append(str(row[key]))
        return max(values) if values else _utcnow().isoformat()

    @classmethod
    def _json_value(cls, value: Any, key: str = "") -> Any:
        if isinstance(value, dict):
            return {str(k): cls._json_value(v, str(k)) for k, v in value.items() if not cls._is_secret_key(str(k))}
        if isinstance(value, list):
            return [cls._json_value(item, key) for item in value]
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        if isinstance(value, Decimal):
            return str(value)
        if isinstance(value, (bytes, bytearray, memoryview)):
            return {"base64": base64.b64encode(bytes(value)).decode("ascii")}
        if cls._is_secret_key(key):
            return None
        return value

    @classmethod
    def _is_secret_key(cls, key: str) -> bool:
        lowered = key.lower()
        return lowered in cls.SECRET_NAMES or any(token in lowered for token in ("api_key", "private_key", "access_token", "refresh_token"))

    @classmethod
    def _reject_secrets(cls, value: Any, path: str = "root") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if cls._is_secret_key(str(key)):
                    raise BackupError(f"plaintext credential field is not allowed in backup: {path}.{key}")
                cls._reject_secrets(child, f"{path}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                cls._reject_secrets(child, f"{path}[{index}]")

    @classmethod
    def _safe_manifest_fields(cls, values: dict[str, Any]) -> dict[str, Any]:
        return {key: cls._json_value(value, key) for key, value in values.items() if not cls._is_secret_key(key)}
