from __future__ import annotations

from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).parents[1]
AUDIT = ROOT / "docs" / "v1-product-goal-alignment-audit.yaml"
BURNDOWN = ROOT / "docs" / "v1-product-gap-burndown.yaml"
REQUIRED = {
    "dod_id",
    "current_status",
    "acceptance_kind",
    "product_area",
    "owner_phase",
    "mapped_r_requirements",
    "exact_missing_behavior",
    "work_class",
    "requires_code",
    "requires_browser",
    "requires_native_linux",
    "requires_windows",
    "requires_tailscale",
    "requires_second_device",
    "requires_hindsight",
    "requires_external_at",
    "requires_live_notion",
    "requires_privilege",
    "requires_packaging",
    "requires_clean_install",
    "next_action",
    "evidence_already_available",
    "qualification_needed",
    "blocked_by",
    "depends_on",
}
ACCEPTANCE_KINDS = {"ARCHITECTURAL_INVARIANT", "OPERATOR_WORKFLOW", "MIXED", "EXTERNAL_DEPENDENCY", "AGGREGATE_RELEASE_GATE"}

WORK_CLASSES = {
    "LOCAL_CODE",
    "LOCAL_BROWSER_QUALIFICATION",
    "LOCAL_NATIVE_QUALIFICATION",
    "EVIDENCE_RECONCILIATION",
    "EXTERNAL_ENVIRONMENT",
    "AGGREGATE_RELEASE_GATE",
}


def main() -> int:
    audit = yaml.safe_load(AUDIT.read_text(encoding="utf-8"))
    burndown = yaml.safe_load(BURNDOWN.read_text(encoding="utf-8"))
    audit_items = audit["items"]
    audit_kinds_ok = all(item.get("acceptance_kind") in ACCEPTANCE_KINDS for item in audit_items)
    complete = [item for item in audit_items if item["status"] in {"USER_USABLE_VERIFIED", "PRODUCT_VERIFIED"}]
    open_items = burndown["items"]
    audit_open = {item["dod_id"]: item for item in audit_items if item["status"] not in {"USER_USABLE_VERIFIED", "PRODUCT_VERIFIED"}}
    burndown_map = {item["dod_id"]: item for item in open_items}
    ids_ok = set(audit_open) == set(burndown_map)
    fields_ok = all(REQUIRED <= set(item) for item in open_items)
    statuses_ok = all(item["current_status"] == audit_open[item["dod_id"]]["status"] for item in open_items if item["dod_id"] in audit_open)
    acceptance_kinds_ok = all(item["acceptance_kind"] == audit_open[item["dod_id"]]["acceptance_kind"] for item in open_items if item["dod_id"] in audit_open)
    classes_ok = all(item["work_class"] in WORK_CLASSES for item in open_items)
    concrete_ok = all(item["exact_missing_behavior"] != "SEE_AUDIT" and item["next_action"] != "SEE_AUDIT" for item in open_items)
    total_ok = len(complete) + len(open_items) == 81
    print(f"audit_total={len(audit_items)}")
    print(f"complete={len(complete)}")
    print(f"burndown={len(open_items)}")
    print(f"complete_plus_burndown={len(complete) + len(open_items)}")
    print(f"ids_match={ids_ok}")
    print(f"fields_complete={fields_ok}")
    print(f"statuses_match={statuses_ok}")
    print(f"audit_acceptance_kinds_valid={audit_kinds_ok}")
    print(f"acceptance_kinds_match={acceptance_kinds_ok}")
    print(f"work_classes_valid={classes_ok}")
    print(f"concrete_actions={concrete_ok}")
    print("work_class_totals=" + str(dict(Counter(item["work_class"] for item in open_items))))
    return 0 if all((ids_ok, fields_ok, statuses_ok, audit_kinds_ok, acceptance_kinds_ok, classes_ok, concrete_ok, total_ok)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
