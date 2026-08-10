#!/usr/bin/env python3
"""Dependency-free Phase 0 source-lock and contract qualification."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_HANDOFF = "48306047cbd84df583bca6530f25d3dd3c1674d490d11a6e621add0238f36ec9"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*([^\n]+)$", text, re.MULTILINE)
    if not match:
        raise AssertionError(f"missing baseline key: {key}")
    return match.group(1).strip().strip('"')


def check_source_lock() -> list[str]:
    baseline_path = ROOT / "baseline/implementation-baseline.yaml"
    baseline = baseline_path.read_text(encoding="utf-8")
    spec = ROOT / value(baseline, "spec_export_artifact")
    handoff = ROOT / value(baseline, "handoff_record_artifact")
    authority_manifest = ROOT / value(baseline, "authority_template_manifest")
    assert value(baseline, "spec_revision") == "PRIME-SPEC-V1.0.0"
    assert value(baseline, "freeze_timestamp_utc") == "2026-08-10T15:41:00Z"
    assert value(baseline, "operator_approval") == "APPROVED"
    assert value(baseline, "handoff_manifest_sha256") == EXPECTED_HANDOFF
    assert digest(spec) == value(baseline, "spec_content_sha256")
    assert digest(authority_manifest) == value(baseline, "authority_template_sha256")
    assert digest(handoff) == value(baseline, "handoff_record_sha256")
    with tempfile.NamedTemporaryFile() as mutated:
        mutated.write(spec.read_bytes() + b"\nphase0-mismatch-test\n")
        mutated.flush()
        assert digest(Path(mutated.name)) != value(baseline, "spec_content_sha256")
    subprocess.run(
        ["sha256sum", "-c", "MANIFEST.sha256"],
        cwd=authority_manifest.parent,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return ["source export hash", "authority manifest hash", "deliberate mismatch failure", "authority file hashes"]


def check_contracts() -> list[str]:
    required = [
        "contracts/authority-file-contract-v1.md",
        "contracts/shared-domain-contracts-v1.yaml",
        "contracts/project-isolation-v1.md",
        "contracts/storage-architecture-v1.md",
        "contracts/privacy-egress-v1.md",
        "threat-model/PRIME-V1.md",
        "docs/requirements-traceability.yaml",
        "dependencies/pins.yaml",
        "dependencies/SBOM.cdx.json",
    ]
    for relative in required:
        assert (ROOT / relative).is_file(), relative
    ledger = (ROOT / "docs/requirements-traceability.yaml").read_text(encoding="utf-8")
    assert not re.search(r"status:\s*UNASSIGNED", ledger)
    assert len(re.findall(r"- \{id: R-", ledger)) >= 30
    json.loads((ROOT / "dependencies/SBOM.cdx.json").read_text(encoding="utf-8"))
    return ["contract inventory", "zero unassigned requirements", "SBOM JSON"]


def check_git() -> list[str]:
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    assert head
    baseline = (ROOT / "baseline/implementation-baseline.yaml").read_text(encoding="utf-8")
    assert value(baseline, "phase0_start_commit") not in {"TO_BE_CREATED_BEFORE_PHASE_0_QUALIFICATION", "TO_BE_RECORDED"}
    return [f"governed Git HEAD {head}"]


def main() -> int:
    checks = check_source_lock() + check_contracts() + check_git()
    print("PHASE 0 QUALIFICATION: PASS")
    for item in checks:
        print(f"PASS: {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
