from pathlib import Path

from src.prime_core.upgrade_service import _version
from src.prime_core.usage_limits import UsagePolicyService


ROOT = Path(__file__).parents[2]


def test_usage_policy_enforces_project_scoped_limit_before_provider_call():
    service = UsagePolicyService(object())
    service.snapshot = lambda project_id: [{
        "limit_id": "limit_test",
        "capability": "ASK_PRIME",
        "period": "DAILY",
        "max_units": 10,
        "consumed_units": 9,
        "remaining_units": 1,
        "enabled": True,
        "status": "KNOWN",
    }]

    decision = service.check("qualification-project", "ASK_PRIME", 2)

    assert decision["allowed"] is False
    assert decision["status"] == "EXCEEDED"
    assert decision["limit_id"] == "limit_test"


def test_upgrade_version_comparison_and_persistent_contract_are_declared():
    assert _version("1.0.0") < _version("1.1.0")
    migration = (ROOT / "migrations/prime/0039_usage_limits_and_upgrade_preflights.sql").read_text(encoding="utf-8")
    assert "prime_core.usage_limits" in migration
    assert "prime_core.upgrade_preflights" in migration
    core = (ROOT / "apps/core/main.py").read_text(encoding="utf-8")
    assert "/v1/system/upgrade/preflight" in core
    assert "/v1/projects/{project_id}/usage/limits" in core


def test_operator_surfaces_expose_usage_and_upgrade_controls():
    web = (ROOT / "apps/web/index.html").read_text(encoding="utf-8")
    assert "usage-limit-form" in web
    assert "upgrade-preflight-form" in web
    assert "Show interrupted recovery state" in web
