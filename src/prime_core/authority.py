from __future__ import annotations

import hashlib
import shutil
from pathlib import Path
from typing import Mapping


REQUIRED_AUTHORITY_FILES = (
    "AGENTS.md", "CLAUDE.md", "COMMANDMENTS_OF_THE_CODE.md", "GEMINI.md",
    ".agent/PROJECT_GOAL.md", ".agent/PROJECT_PROFILE.md", ".agent/CURRENT.md",
    ".agent/DIRECTIVES.md", ".agent/OUTCOMES.md", ".agent/LEARNINGS.md",
    ".agent/RECORD.md", ".agent/REPO_MAP.md",
)


def content_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_authority(root: Path) -> dict[str, object]:
    missing = [relative for relative in REQUIRED_AUTHORITY_FILES if not (root / relative).is_file()]
    files = {relative: content_hash(root / relative) for relative in REQUIRED_AUTHORITY_FILES if (root / relative).is_file()}
    return {"valid": not missing, "missing": missing, "files": files, "contract_version": "authority-file-contract-v1"}


def classify_authority_snapshot(files: Mapping[str, str]) -> str:
    """Classify an authority snapshot without mutating the source files."""
    present = set(files)
    if set(REQUIRED_AUTHORITY_FILES) <= present:
        legacy_markers = (
            "LEGACY-V1", "legacy-v1", "D-PRIME-PHASE15-V1-NATIVE-ATLAS-CLOSURE-042",
            "O-PRIME-042", "L-PRIME-CONTINUATION-043",
        )
        if any(marker in "\n".join(files.values()) for marker in legacy_markers):
            return "LEGACY"
        return "CURRENT"
    core_files = {".agent/PROJECT_GOAL.md", ".agent/PROJECT_PROFILE.md", ".agent/CURRENT.md", ".agent/DIRECTIVES.md", ".agent/OUTCOMES.md", ".agent/LEARNINGS.md", ".agent/RECORD.md", ".agent/REPO_MAP.md"}
    if core_files <= present and any(marker in "\n".join(files.values()) for marker in ("LEGACY-V1", "legacy-v1", "Date:", "Objective:")):
        return "LEGACY"
    return "CONFLICT" if present else "NONE"


def authority_migration_plan(files: Mapping[str, str]) -> dict[str, object]:
    state = classify_authority_snapshot(files)
    if state == "CURRENT":
        return {"state": state, "decision": "NOOP", "rewrite": "NONE", "affected_files": []}
    if state == "LEGACY":
        missing = [relative for relative in REQUIRED_AUTHORITY_FILES if relative not in files]
        return {"state": state, "decision": "MIGRATE_REQUIRED", "rewrite": "NONE_UNTIL_CONFIRMED", "affected_files": missing, "preserve_original": True}
    return {"state": state, "decision": "REVIEW_REQUIRED", "rewrite": "NONE", "affected_files": sorted(files)}


def migrate_authority(template: Path, target: Path, files: Mapping[str, str], confirm: bool = False) -> dict[str, object]:
    plan = authority_migration_plan(files)
    if plan["state"] != "LEGACY":
        raise ValueError("only a recognized legacy authority can be migrated")
    if not confirm:
        raise ValueError("explicit MIGRATE confirmation is required")
    copied: list[str] = []
    for relative in plan["affected_files"]:
        source = template / relative
        if not source.is_file():
            raise FileNotFoundError(relative)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied.append(relative)
    return {"decision": "MIGRATE", "rewrite": "MISSING_FILES_ONLY", "copied_files": copied, "preserved_source": True}


def provision_authority(template: Path, target: Path, overwrite: bool = False) -> dict[str, object]:
    target.mkdir(parents=True, exist_ok=True)
    existing = [relative for relative in REQUIRED_AUTHORITY_FILES if (target / relative).exists()]
    if existing and not overwrite:
        raise FileExistsError("authority provisioning would overwrite existing authority")
    for relative in REQUIRED_AUTHORITY_FILES:
        source = template / relative
        if not source.is_file():
            raise FileNotFoundError(relative)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    return validate_authority(target)
