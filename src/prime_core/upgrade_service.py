from __future__ import annotations

from typing import Any
import uuid

from .build_info import build_info
from .db import connect, transaction, schema_version


def _version(value: str) -> tuple[int, ...]:
    parts = value.lstrip("v").split(".")
    try:
        return tuple(int(part) for part in parts)
    except ValueError:
        return ()


class UpgradeService:
    """Preflight-only upgrade boundary; it never mutates the installation."""

    def __init__(self, settings: Any):
        self.settings = settings

    def status(self, startup_schema: str | None) -> dict[str, Any]:
        with connect(self.settings) as db:
            rows = db.execute(
                "SELECT preflight_id,target_version,target_schema,compatibility,migration_required,backup_required,backup_available,status,recovery_guidance,created_at "
                "FROM prime_core.upgrade_preflights ORDER BY created_at DESC LIMIT 20"
            ).fetchall()
        return {"build": build_info(startup_schema), "preflights": [dict(row) for row in rows]}

    def preflight(self, target_version: str, target_schema: str | None, backup_available: bool, simulate: str = "NONE") -> dict[str, Any]:
        current = build_info(schema_version(self.settings))
        current_version = _version(current["service_version"])
        target = _version(target_version)
        current_schema = current["schema_version"]
        migration_required = bool(target_schema and target_schema != current_schema)
        compatibility = "COMPATIBLE"
        status = "READY"
        guidance = "No installation changes were made. Apply only through the approved release procedure after this preflight."
        if target and current_version and target < current_version:
            compatibility, status, guidance = "UNSUPPORTED_DOWNGRADE", "REFUSED", "Downgrade is refused; restore a compatible encrypted continuity backup through the guarded recovery path."
            migration_required = False
        elif target_schema and target_schema != current_schema and not target_schema.startswith("0039"):
            compatibility, status, guidance = "SCHEMA_INCOMPATIBLE", "REFUSED", "Target schema is not present in the installed migration set; no migration was attempted."
        elif migration_required and not backup_available:
            compatibility, status, guidance = "BACKUP_REQUIRED", "REFUSED", "Create and verify an encrypted continuity backup before any schema-changing release."
        elif simulate == "INTERRUPTED":
            compatibility, status, guidance = "RECOVERY_REQUIRED", "RECOVERY_REQUIRED", "Interrupted migration requires guarded recovery from the verified continuity backup; no partial migration was applied by this preflight."
        elif simulate == "FAILED":
            compatibility, status, guidance = "MIGRATION_FAILED", "RECOVERY_REQUIRED", "Migration failure requires review of the immutable preflight record and guarded recovery; no release was applied."
        elif not migration_required:
            compatibility = "NO_OP"
        row = {
            "preflight_id": "upgrade_preflight_" + uuid.uuid4().hex,
            "target_version": target_version,
            "target_schema": target_schema,
            "compatibility": compatibility,
            "migration_required": migration_required,
            "backup_required": migration_required,
            "backup_available": backup_available,
            "status": status,
            "recovery_guidance": guidance,
        }
        with transaction(self.settings) as db:
            db.execute(
                "INSERT INTO prime_core.upgrade_preflights(preflight_id,target_version,target_schema,compatibility,migration_required,backup_required,backup_available,status,recovery_guidance) "
                "VALUES (%(preflight_id)s,%(target_version)s,%(target_schema)s,%(compatibility)s,%(migration_required)s,%(backup_required)s,%(backup_available)s,%(status)s,%(recovery_guidance)s)",
                row,
            )
        return row | {"current_build": current}
