from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).parents[1]
TRACEABILITY_PATH = ROOT / "docs" / "requirements-traceability.yaml"
AUDIT_PATH = ROOT / "docs" / "v1-product-goal-alignment-audit.yaml"
BURNDOWN_PATH = ROOT / "docs" / "v1-product-gap-burndown.yaml"
MATRIX_PATH = ROOT / "docs" / "phase15-remediation-matrix.yaml"
LEDGER_PATH = ROOT / "docs" / "phase15-remediation-qualification-ledger.yaml"
COMPLETE_DOD_STATUSES = {"USER_USABLE_VERIFIED", "PRODUCT_VERIFIED"}
TERMINAL_REQUIREMENT_STATUSES = {"VERIFIED", "FUTURE_ONLY_BY_SPEC"}
ALLOWED = {
    "USER_USABLE_VERIFIED",
    "PRODUCT_VERIFIED",
    "IMPLEMENTED_NOT_PRODUCT_QUALIFIED",
    "BACKEND_ONLY",
    "UI_SHELL_ONLY",
    "PARTIAL",
    "MISSING",
    "BLOCKED_BY_ENVIRONMENT",
}
REQUIRED = {
    "dod_id", "spec_section", "exact_requirement_summary", "product_area", "status",
    "owner_phase", "mapped_requirements", "backend_evidence", "api_evidence", "ui_evidence",
    "browser_evidence", "qualification_evidence", "user_can_actually_use_it", "user_path",
    "missing_behavior", "environment_blocker", "reopen_required", "reopen_targets", "evidence_paths",
}


def validate_release_consistency(
    audit_path: Path = AUDIT_PATH,
    traceability_path: Path = TRACEABILITY_PATH,
    burndown_path: Path = BURNDOWN_PATH,
    matrix_path: Path = MATRIX_PATH,
    ledger_path: Path = LEDGER_PATH,
) -> dict[str, object]:
    audit = yaml.safe_load(audit_path.read_text(encoding="utf-8"))
    traceability = yaml.safe_load(traceability_path.read_text(encoding="utf-8"))
    burndown = yaml.safe_load(burndown_path.read_text(encoding="utf-8"))
    matrix = yaml.safe_load(matrix_path.read_text(encoding="utf-8"))
    ledger = yaml.safe_load(ledger_path.read_text(encoding="utf-8"))

    audit_items = audit.get("items", [])
    complete_count = sum(item.get("status") in COMPLETE_DOD_STATUSES for item in audit_items)
    v1_rows = [
        row for row in traceability.get("requirements", [])
        if 1 <= int(row.get("id", "R-000")[2:]) <= 29
    ]
    unresolved = [
        row.get("id") for row in v1_rows
        if row.get("status") not in TERMINAL_REQUIREMENT_STATUSES
    ]
    reopened = [
        row.get("id") for row in v1_rows
        if row.get("phase_status", {}).get(15) == "REOPENED"
    ]
    matrix_status = {
        row.get("requirement_id"): (row.get("current_status"), row.get("final_status"))
        for row in matrix.get("requirements", [])
    }
    ledger_status = {
        row.get("requirement_id"): (row.get("current_status"), row.get("final_status"))
        for row in ledger.get("records", [])
    }

    return {
        "audit_pass": audit.get("release_gate_status") == "PASS",
        "audit_81_complete": len(audit_items) == 81 and complete_count == 81,
        "traceability_pass": traceability.get("product_alignment_status") == "PASS",
        "traceability_counts": (
            traceability.get("product_alignment_item_count") == 81
            and traceability.get("product_alignment_complete_count") == 81
            and traceability.get("product_alignment_open_count") == 0
            and traceability.get("unresolved_v1_requirement_count") == 0
        ),
        "traceability_phase_complete": (
            traceability.get("phase15_status") == "COMPLETE"
            and traceability.get("v1_status") == "QUALIFIED_FOR_PRIVATE_PRODUCTION_USE"
        ),
        "traceability_terminal": len(v1_rows) == 29 and not unresolved and not reopened,
        "burndown_empty": len(burndown.get("items", [])) == 0,
        "matrix_pass": (
            matrix.get("product_alignment_status") == "PASS"
            and matrix_status.get("R-045") == ("VERIFIED", "VERIFIED")
            and matrix_status.get("R-056") == ("VERIFIED", "VERIFIED")
        ),
        "ledger_pass": (
            ledger.get("product_alignment_status") == "PASS"
            and ledger_status.get("R-045") == ("VERIFIED", "VERIFIED")
            and ledger_status.get("R-056") == ("VERIFIED", "VERIFIED")
        ),
        "unresolved_v1_rows": unresolved,
        "reopened_v1_rows": reopened,
    }


def main() -> int:
    path = AUDIT_PATH
    audit = yaml.safe_load(path.read_text(encoding="utf-8"))
    items = audit.get("items", [])
    statuses = Counter(item.get("status") for item in items)
    ids = [item.get("dod_id") for item in items]
    release = validate_release_consistency()
    release_checks = [value for key, value in release.items() if not key.endswith("_rows")]
    valid = (
        len(items) == 81
        and ids == [f"DOD-{number:03d}" for number in range(1, 82)]
        and all(item.get("status") in ALLOWED for item in items)
        and all(REQUIRED <= set(item) for item in items)
        and audit.get("release_gate") == "V1_PRODUCT_GOAL_ALIGNMENT"
        and audit.get("release_gate_status") in {"PASS", "FAIL", "BLOCKED"}
        and all(release_checks)
    )
    print(f"§26 items: {len(items)}")
    print("status counts: " + ", ".join(f"{key}={statuses.get(key, 0)}" for key in sorted(ALLOWED)))
    print("V1_PRODUCT_GOAL_ALIGNMENT: " + str(audit.get("release_gate_status")))
    print("REQUIREMENTS_TRACEABILITY: " + ("PASS" if release["traceability_terminal"] else "FAIL"))
    print("RELEASE_CROSS_VIEW_CONSISTENCY: " + ("PASS" if all(release_checks) else "FAIL"))
    print("PRODUCT_ALIGNMENT_AUDIT: " + ("PASS" if valid else "FAIL"))
    return 0 if valid else 1


if __name__ == "__main__":
    sys.exit(main())
