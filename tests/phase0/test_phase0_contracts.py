from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_source_lock_identity() -> None:
    manifest = (ROOT / "baseline/implementation-baseline.yaml").read_text()
    assert "PRIME-SPEC-V1.0.0" in manifest
    assert "2026-08-10T15:41:00Z" in manifest
    assert "APPROVED" in manifest


def test_required_phase0_contracts_exist() -> None:
    required = [
        "contracts/authority-file-contract-v1.md",
        "contracts/shared-domain-contracts-v1.yaml",
        "contracts/project-isolation-v1.md",
        "contracts/storage-architecture-v1.md",
        "contracts/privacy-egress-v1.md",
        "threat-model/PRIME-V1.md",
        "docs/requirements-traceability.yaml",
        "dependencies/pins.yaml",
    ]
    assert all((ROOT / path).is_file() for path in required)


def test_traceability_has_no_unassigned_status() -> None:
    ledger = (ROOT / "docs/requirements-traceability.yaml").read_text()
    assert "UNASSIGNED" in ledger
    assert "status: UNASSIGNED" not in ledger


def test_authority_manifest_is_present_and_nonempty() -> None:
    manifest = ROOT / "authority-template/v1/MANIFEST.sha256"
    assert manifest.is_file()
    assert manifest.read_text().strip()


def test_sbom_is_valid_json() -> None:
    json.loads((ROOT / "dependencies/SBOM.cdx.json").read_text())
