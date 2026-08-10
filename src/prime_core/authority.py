from __future__ import annotations

import hashlib
import shutil
from pathlib import Path


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

