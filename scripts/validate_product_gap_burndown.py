from __future__ import annotations
from collections import Counter
from pathlib import Path
import yaml
ROOT = Path(__file__).parents[1]
AUDIT = ROOT / "docs" / "v1-product-goal-alignment-audit.yaml"
BURNDOWN = ROOT / "docs" / "v1-product-gap-burndown.yaml"
REQUIRED = {"dod_id", "current_status", "acceptance_kind", "product_area", "owner_phase", "mapped_r_requirements", "exact_missing_behavior", "work_class", "requires_code", "requires_browser", "requires_native_linux", "requires_windows", "requires_tailscale", "requires_second_device", "requires_hindsight", "requires_external_at", "requires_live_notion", "requires_privilege", "requires_packaging", "requires_clean_install", "next_action", "evidence_already_available", "qualification_needed", "blocked_by", "depends_on"}
ACCEPTANCE_KINDS = {"ARCHITECTURAL_INVARIANT", "OPERATOR_WORKFLOW", "MIXED", "EXTERNAL_DEPENDENCY", "AGGREGATE_RELEASE_GATE"}
WORK_CLASSES = {"LOCAL_CODE", "LOCAL_BROWSER_QUALIFICATION", "LOCAL_NATIVE_QUALIFICATION", "EVIDENCE_RECONCILIATION", "EXTERNAL_ENVIRONMENT", "AGGREGATE_RELEASE_GATE"}
COMPLETE_STATUSES = {"USER_USABLE_VERIFIED", "PRODUCT_VERIFIED"}
STATUS_VOCABULARY = COMPLETE_STATUSES | {"IMPLEMENTED_NOT_PRODUCT_QUALIFIED", "BACKEND_ONLY", "UI_SHELL_ONLY", "PARTIAL", "MISSING", "BLOCKED_BY_ENVIRONMENT"}


def validate_documents(audit_path: Path = AUDIT, burndown_path: Path = BURNDOWN) -> dict[str, object]:
    audit = yaml.safe_load(audit_path.read_text(encoding="utf-8"))
    burndown = yaml.safe_load(burndown_path.read_text(encoding="utf-8"))
    audit_items = audit["items"]
    audit_kinds_ok = all(item.get("acceptance_kind") in ACCEPTANCE_KINDS for item in audit_items)
    audit_ids = [item.get("dod_id") for item in audit_items]
    duplicate_audit_ids = sorted({item for item in audit_ids if item and audit_ids.count(item) > 1})
    complete = [item for item in audit_items if item["status"] in COMPLETE_STATUSES]
    open_items = burndown["items"]
    audit_open = {item["dod_id"]: item for item in audit_items if item["status"] not in COMPLETE_STATUSES}
    burndown_ids = [item.get("dod_id") for item in open_items]
    burndown_map = {item["dod_id"]: item for item in open_items if item.get("dod_id")}
    duplicate_burndown_ids = sorted({item for item in burndown_ids if item and burndown_ids.count(item) > 1})
    expected_open_ids = set(audit_open)
    burndown_id_set = set(burndown_map)
    ids_ok = not duplicate_audit_ids and not duplicate_burndown_ids and expected_open_ids == burndown_id_set
    fields_ok = all(REQUIRED <= set(item) for item in open_items)
    statuses_ok = all(item["current_status"] == audit_open[item["dod_id"]]["status"] for item in open_items if item.get("dod_id") in audit_open)
    acceptance_kinds_ok = all(item["acceptance_kind"] == audit_open[item["dod_id"]]["acceptance_kind"] for item in open_items if item.get("dod_id") in audit_open)
    classes_ok = all(item["work_class"] in WORK_CLASSES for item in open_items)
    concrete_ok = all(item["exact_missing_behavior"] != "SEE_AUDIT" and item["next_action"] != "SEE_AUDIT" for item in open_items)
    architectural_ui_gap_ids = [item["dod_id"] for item in open_items if item["acceptance_kind"] == "ARCHITECTURAL_INVARIANT" and any(token in (item["exact_missing_behavior"] + " " + item["next_action"] + " " + item["qualification_needed"]).lower() for token in ("operator screen", "dedicated screen", "operator workflow"))]
    architectural_semantics_ok = not architectural_ui_gap_ids
    status_counts = Counter(item.get("status") for item in audit_items)
    computed_status_counts = {status: status_counts.get(status, 0) for status in sorted(STATUS_VOCABULARY)}
    declared_status_counts = audit.get("declared_status_counts")
    normalized_declared_counts = ({str(status): int(count) for status, count in declared_status_counts.items()} if declared_status_counts is not None else None)
    status_counts_ok = normalized_declared_counts is None or normalized_declared_counts == computed_status_counts
    status_vocabulary_ok = all(item.get("status") in STATUS_VOCABULARY for item in audit_items)
    audit_total_ok = len(audit_items) == 81
    status_sum_ok = sum(status_counts.values()) == len(audit_items)
    burndown_count_ok = len(open_items) == sum(item["status"] not in COMPLETE_STATUSES for item in audit_items)
    open_missing = sorted(expected_open_ids - burndown_id_set)
    complete_in_burndown = sorted(set(burndown_id_set) & {item["dod_id"] for item in complete})
    complete_absent_ok = not complete_in_burndown
    expected_work_class_totals = {work_class: Counter(item.get("work_class") for item in open_items).get(work_class, 0) for work_class in sorted(WORK_CLASSES)}
    declared_work_class_totals = {work_class: burndown.get("totals_by_work_class", {}).get(work_class, 0) for work_class in sorted(WORK_CLASSES)}
    work_class_totals_ok = declared_work_class_totals == expected_work_class_totals
    work_class_sum_ok = sum(expected_work_class_totals.values()) == len(open_items)
    total_ok = audit_total_ok and burndown_count_ok and len(complete) + len(open_items) == len(audit_items)
    return locals()


def main() -> int:
    result = validate_documents()
    audit_items = result["audit_items"]
    complete = result["complete"]
    open_items = result["open_items"]
    ids_ok = result["ids_ok"]
    fields_ok = result["fields_ok"]
    statuses_ok = result["statuses_ok"]
    audit_kinds_ok = result["audit_kinds_ok"]
    acceptance_kinds_ok = result["acceptance_kinds_ok"]
    classes_ok = result["classes_ok"]
    concrete_ok = result["concrete_ok"]
    architectural_semantics_ok = result["architectural_semantics_ok"]
    audit_total_ok = result["audit_total_ok"]
    status_sum_ok = result["status_sum_ok"]
    status_counts_ok = result["status_counts_ok"]
    status_vocabulary_ok = result["status_vocabulary_ok"]
    burndown_count_ok = result["burndown_count_ok"]
    complete_absent_ok = result["complete_absent_ok"]
    work_class_totals_ok = result["work_class_totals_ok"]
    work_class_sum_ok = result["work_class_sum_ok"]
    total_ok = result["total_ok"]
    print(f"audit_total={len(audit_items)}")
    print(f"complete={len(complete)}")
    print(f"burndown={len(open_items)}")
    print(f"complete_plus_burndown={len(complete) + len(open_items)}")
    print(f"audit_total_ok={audit_total_ok}")
    print(f"status_sum_ok={status_sum_ok}")
    print(f"status_counts_ok={status_counts_ok}")
    print(f"status_vocabulary_ok={status_vocabulary_ok}")
    print("declared_status_counts=" + str(result["declared_status_counts"]))
    print("status_counts=" + str(result["computed_status_counts"]))
    print(f"burndown_count_ok={burndown_count_ok}")
    print(f"ids_match={ids_ok}")
    print(f"open_missing={','.join(result['open_missing']) or 'NONE'}")
    print(f"complete_in_burndown={','.join(result['complete_in_burndown']) or 'NONE'}")
    print(f"duplicate_audit_ids={','.join(result['duplicate_audit_ids']) or 'NONE'}")
    print(f"duplicate_burndown_ids={','.join(result['duplicate_burndown_ids']) or 'NONE'}")
    print(f"fields_complete={fields_ok}")
    print(f"statuses_match={statuses_ok}")
    print(f"audit_acceptance_kinds_valid={audit_kinds_ok}")
    print(f"acceptance_kinds_match={acceptance_kinds_ok}")
    print(f"work_classes_valid={classes_ok}")
    print(f"concrete_actions={concrete_ok}")
    print(f"architectural_semantics={architectural_semantics_ok}")
    print(f"complete_absent={complete_absent_ok}")
    print(f"work_class_totals_match={work_class_totals_ok}")
    print(f"work_class_sum={work_class_sum_ok}")
    if result["architectural_ui_gap_ids"]:
        print("architectural_ui_gap_ids=" + ",".join(result["architectural_ui_gap_ids"]))
    print("work_class_totals=" + str(dict(Counter(item["work_class"] for item in open_items))))
    return 0 if all((audit_total_ok, status_sum_ok, status_counts_ok, status_vocabulary_ok, burndown_count_ok, ids_ok, fields_ok, statuses_ok, audit_kinds_ok, acceptance_kinds_ok, classes_ok, concrete_ok, architectural_semantics_ok, complete_absent_ok, work_class_totals_ok, work_class_sum_ok, total_ok)) else 1
if __name__ == "__main__":
    raise SystemExit(main())
