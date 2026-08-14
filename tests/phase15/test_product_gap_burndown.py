from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import yaml

from scripts.validate_product_gap_burndown import validate_documents


ROOT = Path(__file__).parents[2]


def _copies(tmp_path: Path) -> tuple[Path, Path]:
    audit = tmp_path / "audit.yaml"
    burndown = tmp_path / "burndown.yaml"
    audit.write_text((ROOT / "docs" / "v1-product-goal-alignment-audit.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    burndown.write_text((ROOT / "docs" / "v1-product-gap-burndown.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    return audit, burndown


def test_burndown_is_derived_and_totals_match() -> None:
    result = validate_documents()

    assert result["audit_total_ok"]
    assert result["status_sum_ok"]
    assert result["burndown_count_ok"]
    assert result["ids_ok"]
    assert result["complete_absent_ok"]
    assert result["work_class_totals_ok"]
    assert result["work_class_sum_ok"]


def test_stale_work_class_header_fails(tmp_path: Path) -> None:
    audit_path, burndown_path = _copies(tmp_path)
    burndown = yaml.safe_load(burndown_path.read_text(encoding="utf-8"))
    burndown["totals_by_work_class"]["LOCAL_CODE"] += 1
    burndown_path.write_text(yaml.safe_dump(burndown, sort_keys=False), encoding="utf-8")

    result = validate_documents(audit_path, burndown_path)

    assert not result["work_class_totals_ok"]


def test_duplicate_or_complete_burndown_row_fails(tmp_path: Path) -> None:
    audit_path, burndown_path = _copies(tmp_path)
    audit = yaml.safe_load(audit_path.read_text(encoding="utf-8"))
    burndown = yaml.safe_load(burndown_path.read_text(encoding="utf-8"))
    burndown["items"].append(deepcopy(burndown["items"][0]))
    completed_id = next(item["dod_id"] for item in audit["items"] if item["status"] == "PRODUCT_VERIFIED")
    completed_row = deepcopy(burndown["items"][0])
    completed_row["dod_id"] = completed_id
    completed_row["current_status"] = next(item["status"] for item in audit["items"] if item["dod_id"] == completed_id)
    completed_row["acceptance_kind"] = next(item["acceptance_kind"] for item in audit["items"] if item["dod_id"] == completed_id)
    burndown["items"].append(completed_row)
    burndown_path.write_text(yaml.safe_dump(burndown, sort_keys=False), encoding="utf-8")

    result = validate_documents(audit_path, burndown_path)

    assert result["duplicate_burndown_ids"]
    assert result["complete_in_burndown"]
    assert not result["ids_ok"]
    assert not result["complete_absent_ok"]


def test_status_counts_are_derived_and_declared_summary_is_checked(tmp_path: Path) -> None:
    audit_path, burndown_path = _copies(tmp_path)
    audit = yaml.safe_load(audit_path.read_text(encoding="utf-8"))
    burndown = yaml.safe_load(burndown_path.read_text(encoding="utf-8"))
    starting_product_verified = sum(item["status"] == "PRODUCT_VERIFIED" for item in audit["items"])
    starting_backend_only = sum(item["status"] == "BACKEND_ONLY" for item in audit["items"])
    starting_complete = sum(item["status"] in {"USER_USABLE_VERIFIED", "PRODUCT_VERIFIED"} for item in audit["items"])
    promoted = next(item for item in audit["items"] if item["status"] == "BACKEND_ONLY")
    old_status = promoted["status"]
    promoted["status"] = "PRODUCT_VERIFIED"
    audit["declared_status_counts"][old_status] -= 1
    audit["declared_status_counts"]["PRODUCT_VERIFIED"] += 1
    burndown["items"] = [item for item in burndown["items"] if item["dod_id"] != promoted["dod_id"]]
    audit_path.write_text(yaml.safe_dump(audit, sort_keys=False), encoding="utf-8")
    burndown_path.write_text(yaml.safe_dump(burndown, sort_keys=False), encoding="utf-8")
    result = validate_documents(audit_path, burndown_path)
    assert result["status_counts"]["PRODUCT_VERIFIED"] == starting_product_verified + 1
    assert result["status_counts"]["BACKEND_ONLY"] == starting_backend_only - 1
    assert result["status_counts_ok"]
    assert result["status_vocabulary_ok"]
    assert len(result["complete"]) == starting_complete + 1


def test_stale_declared_status_summary_fails(tmp_path: Path) -> None:
    audit_path, burndown_path = _copies(tmp_path)
    audit = yaml.safe_load(audit_path.read_text(encoding="utf-8"))
    audit["declared_status_counts"]["PRODUCT_VERIFIED"] += 1
    audit_path.write_text(yaml.safe_dump(audit, sort_keys=False), encoding="utf-8")
    result = validate_documents(audit_path, burndown_path)
    assert not result["status_counts_ok"]
