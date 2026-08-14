from __future__ import annotations

from typing import Any


STEP_STATUSES = {
    "PENDING",
    "RUNNING",
    "SUCCEEDED",
    "FAILED_RETRYABLE",
    "FAILED_FINAL",
    "REPAIR_REQUIRED",
    "COMPENSATED",
}
REPLAY_POLICIES = {"PURE_OR_DB_TRANSACTION", "IDEMPOTENT_EXTERNAL", "NON_IDEMPOTENT_EXTERNAL"}


def step_resume_decision(status: str, replay_policy: str) -> str:
    if status in {"SUCCEEDED", "COMPENSATED"}:
        return "SKIP_COMPLETED"
    if status == "RUNNING":
        return "REPAIR_REQUIRED" if replay_policy == "NON_IDEMPOTENT_EXTERNAL" else "RETRY"
    if status == "FAILED_RETRYABLE":
        return "RETRY"
    if status in {"PENDING", "FAILED_FINAL", "REPAIR_REQUIRED"}:
        return "REPAIR_REQUIRED" if status != "PENDING" else "START"
    return "UNKNOWN"


def resume_plan_payload(workflow: dict[str, Any], steps: list[dict[str, Any]], resources: list[dict[str, Any]]) -> dict[str, Any]:
    ordered = sorted(steps, key=lambda item: item.get("step_order", 0))
    incomplete = next((step for step in ordered if step.get("status") not in {"SUCCEEDED", "COMPENSATED"}), None)
    ambiguities = [
        {"step_key": step.get("step_key"), "reason": "NON_IDEMPOTENT_EXTERNAL_OUTCOME"}
        for step in ordered
        if step.get("status") == "REPAIR_REQUIRED"
        or (step.get("status") == "RUNNING" and step.get("replay_policy") == "NON_IDEMPOTENT_EXTERNAL")
    ]
    next_action = "COMPLETE" if incomplete is None else step_resume_decision(incomplete.get("status", "UNKNOWN"), incomplete.get("replay_policy", ""))
    return {
        "workflow_id": workflow.get("workflow_id"),
        "workflow_status": workflow.get("status"),
        "completed_steps": [step.get("step_key") for step in ordered if step.get("status") in {"SUCCEEDED", "COMPENSATED"}],
        "current_incomplete_step": incomplete.get("step_key") if incomplete else None,
        "retryability": "RETRYABLE" if incomplete and next_action in {"START", "RETRY"} else "NOT_RETRYABLE",
        "recorded_resource_refs": resources,
        "ambiguities": ambiguities,
        "required_reconciliation": bool(ambiguities),
        "next_safe_action": next_action,
    }
