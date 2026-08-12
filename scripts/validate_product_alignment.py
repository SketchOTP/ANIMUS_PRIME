from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).parents[1]
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


def main() -> int:
    path = ROOT / "docs" / "v1-product-goal-alignment-audit.yaml"
    audit = yaml.safe_load(path.read_text(encoding="utf-8"))
    items = audit.get("items", [])
    statuses = Counter(item.get("status") for item in items)
    ids = [item.get("dod_id") for item in items]
    valid = (
        len(items) == 81
        and ids == [f"DOD-{number:03d}" for number in range(1, 82)]
        and all(item.get("status") in ALLOWED for item in items)
        and all(REQUIRED <= set(item) for item in items)
        and audit.get("release_gate") == "V1_PRODUCT_GOAL_ALIGNMENT"
        and audit.get("release_gate_status") in {"PASS", "FAIL", "BLOCKED"}
    )
    print(f"§26 items: {len(items)}")
    print("status counts: " + ", ".join(f"{key}={statuses.get(key, 0)}" for key in sorted(ALLOWED)))
    print("V1_PRODUCT_GOAL_ALIGNMENT: " + str(audit.get("release_gate_status")))
    print("PRODUCT_ALIGNMENT_AUDIT: " + ("PASS" if valid else "FAIL"))
    return 0 if valid else 1


if __name__ == "__main__":
    sys.exit(main())
