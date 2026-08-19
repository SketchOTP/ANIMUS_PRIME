from __future__ import annotations

from pathlib import Path

import yaml

from scripts.validate_product_alignment import validate_release_consistency


ROOT = Path(__file__).parents[2]


def _copy(tmp_path: Path, name: str) -> Path:
    target = tmp_path / Path(name).name
    target.write_text((ROOT / name).read_text(encoding="utf-8"), encoding="utf-8")
    return target


def _paths(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path]:
    return tuple(
        _copy(tmp_path, name)
        for name in (
            "docs/v1-product-goal-alignment-audit.yaml",
            "docs/requirements-traceability.yaml",
            "docs/v1-product-gap-burndown.yaml",
            "docs/phase15-remediation-matrix.yaml",
            "docs/phase15-remediation-qualification-ledger.yaml",
        )
    )


def test_final_release_views_are_consistent() -> None:
    result = validate_release_consistency()
    assert all(value for key, value in result.items() if not key.endswith("_rows"))
    assert result["unresolved_v1_rows"] == []
    assert result["reopened_v1_rows"] == []


def test_traceability_fail_cannot_coexist_with_alignment_pass(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    traceability = yaml.safe_load(paths[1].read_text(encoding="utf-8"))
    traceability["product_alignment_status"] = "FAIL"
    paths[1].write_text(yaml.safe_dump(traceability, sort_keys=False), encoding="utf-8")
    result = validate_release_consistency(*paths)
    assert result["audit_pass"]
    assert not result["traceability_pass"]


def test_nonterminal_v1_requirement_fails_complete_release(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    traceability = yaml.safe_load(paths[1].read_text(encoding="utf-8"))
    traceability["requirements"][0]["status"] = "IMPLEMENTED"
    paths[1].write_text(yaml.safe_dump(traceability, sort_keys=False), encoding="utf-8")
    result = validate_release_consistency(*paths)
    assert not result["traceability_terminal"]
    assert result["unresolved_v1_rows"] == ["R-001"]


def test_alignment_count_disagreement_fails_complete_release(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    audit = yaml.safe_load(paths[0].read_text(encoding="utf-8"))
    audit["items"][0]["status"] = "PARTIAL"
    paths[0].write_text(yaml.safe_dump(audit, sort_keys=False), encoding="utf-8")
    result = validate_release_consistency(*paths)
    assert not result["audit_81_complete"]
