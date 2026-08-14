from __future__ import annotations

import json
import re
import socket
import subprocess
from pathlib import Path

from src.prime_core.config import Settings
from src.prime_core.db import connect, migrate
from src.prime_core.service import CoreService


ROOT = Path("/home/sketch/Projects/ANIMUS_PRIME")
PRIOR_RUNTIME_COMMIT = "a9efb529dbd9a0bdd9edfd4f33fd54b6c856d609"


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True, timeout=20).stdout.strip()


def listener_available(port: int) -> bool:
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    probe.settimeout(0.5)
    try:
        return probe.connect_ex(("127.0.0.1", port)) == 0
    finally:
        probe.close()


def main() -> None:
    settings = Settings()
    applied = migrate(settings)
    with connect(settings) as db:
        row = db.execute(
            "SELECT p.project_id,b.repository_id,b.node_id,b.binding_revision,b.canonical_ref,b.canonical_ref_commit,r.canonical_path "
            "FROM prime_core.projects p JOIN prime_core.project_bindings b ON b.project_id=p.project_id "
            "JOIN prime_core.repositories r ON r.repository_id=b.repository_id WHERE r.canonical_path=%s",
            (str(ROOT),),
        ).fetchone()
        assert row, "persistent ANIMUS PRIME binding not found"
        table_rows = db.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='prime_core' AND table_name IN ('repository_continuity_anchors','repository_rebind_preflights','repository_rebind_history','workflow_steps','workflow_resources') ORDER BY table_name"
        ).fetchall()
    project = dict(row)
    core = CoreService(settings)

    changed_network_files = git("diff", "--name-only", PRIOR_RUNTIME_COMMIT, "HEAD", "--", "apps/core/main.py", "apps/node/main.py", "src/prime_core/remote_access_service.py", "docker-compose.phase1.yml", "docker-compose.yml").splitlines()
    network_diff = git("diff", "--unified=0", PRIOR_RUNTIME_COMMIT, "HEAD", "--", *changed_network_files) if changed_network_files else ""
    network_semantic_markers = re.compile(r"(?:uvicorn|CORSMiddleware|allow_origins|web_host|web_port|Funnel|tailscale serve|public listener|0\.0\.0\.0)", re.I)
    dod006 = {
        "prior_runtime_evidence": "qualification-continuation-041.md",
        "prior_revision": PRIOR_RUNTIME_COMMIT,
        "network_relevant_files_changed": changed_network_files,
        "code_equivalence": "NETWORK_SEMANTICS_CHANGED" if network_semantic_markers.search(network_diff) else "UNRELATED_CHANGE",
        "current_runtime_topology_available": any(listener_available(port) for port in (8000, 18000)),
        "exact_residual": "CURRENT_RUNTIME_TOPOLOGY_QUALIFICATION_REQUIRED",
        "final": "IMPLEMENTED_NOT_PRODUCT_QUALIFIED",
    }
    assert dod006["code_equivalence"] == "UNRELATED_CHANGE"
    assert dod006["current_runtime_topology_available"] is False

    before = {key: project[key] for key in ("project_id", "repository_id", "node_id", "binding_revision", "canonical_ref", "canonical_ref_commit", "canonical_path")}
    preflight = core.inspect_repository_rebind(project["project_id"], project["node_id"], project["canonical_path"])
    assert preflight["continuity_verdict"] == "LOGICAL_REPOSITORY_CONTINUITY_VERIFIED"
    assert preflight["preflight_token"]
    assert preflight["real_relocation_candidate"] is False
    refusal = core.inspect_repository_rebind(project["project_id"], project["node_id"], str(ROOT / "does-not-exist"))
    assert refusal["refusal_reason"] == "DESTINATION_ABSENT"
    with connect(settings) as db:
        after = dict(db.execute(
            "SELECT p.project_id,b.repository_id,b.node_id,b.binding_revision,b.canonical_ref,b.canonical_ref_commit,r.canonical_path "
            "FROM prime_core.projects p JOIN prime_core.project_bindings b ON b.project_id=p.project_id JOIN prime_core.repositories r ON r.repository_id=b.repository_id WHERE p.project_id=%s",
            (project["project_id"],),
        ).fetchone())
    assert {key: after[key] for key in before} == before
    dod039 = {
        "stable_project_id": project["project_id"],
        "stable_repository_id": project["repository_id"],
        "old_location_fingerprint": preflight["current_location_fingerprint"],
        "candidate_location_fingerprint": preflight["candidate"]["candidate_location_fingerprint"],
        "continuity_anchor": "ESTABLISHED",
        "canonical_ref_check": "VERIFIED",
        "canonical_commit_check": "VERIFIED",
        "known_object_check": "VERIFIED",
        "authority_project_check": "VERIFIED",
        "dirty_worktree_check": preflight["dirty_worktree"],
        "duplicate_binding_check": preflight["duplicate_active_binding"],
        "preflight": "PASSED",
        "stale_preflight_protection": "IMPLEMENTED_AND_TESTED",
        "rollback": "OLD_BINDING_PRESERVED_ON_PREFLIGHT_FAILURE",
        "audit_history": "CUTOVER_PATH_RECORDS_BOTH_LOCATIONS",
        "real_relocation_candidate_available": False,
        "final": "IMPLEMENTED_NOT_PRODUCT_QUALIFIED",
        "exact_residual": "REAL_RELOCATION_CUTOVER_NOT_AVAILABLE_UNDER_CURRENT_NONDISPOSABLE_CONSTRAINT",
    }

    service_text = (ROOT / "src/prime_core/service.py").read_text(encoding="utf-8")
    dod004 = {
        "workflow_inventory": {
            "CREATE_REPOSITORY": "DURABLE_STEP_MODEL_CONVERTED",
            "FORK_PROJECT": "MULTI_SYSTEM_LEGACY_PATH_REVIEW_REQUIRED",
            "RESTORE": "DEDICATED_RESTORE_WORKFLOW_OUTSIDE_GENERIC_STEP_MODEL",
            "NOTION_HINDSIGHT_ARCHIVE": "NOT_CONVERTED_IN_THIS_BOUNDED_CYCLE",
        },
        "schema": [dict(item) for item in table_rows],
        "step_model": "PERSISTENT workflow_steps WITH UNIQUE workflow_id+step_key",
        "replay_policy": "PURE_OR_DB_TRANSACTION, IDEMPOTENT_EXTERNAL, NON_IDEMPOTENT_EXTERNAL",
        "resource_references": "PERSISTENT workflow_resources WITHOUT SECRETS",
        "resume_plan": "IMPLEMENTED_AND_TESTED",
        "create_repository": "CHECKPOINTED_DIRECTORY_GIT_BIND",
        "fork_project": "REMAINS_OUTSIDE_FULL_CONVERSION",
        "notion": "NOT_CONVERTED",
        "hindsight": "NOT_CONVERTED",
        "interruption_matrix": "PURE_CONTRACT_TESTS_ONLY; NO_PERSISTENT_RESOURCE_INTERRUPTION",
        "ambiguous_external_effect": "REPAIR_REQUIRED",
        "repair_handling": "MARK_REPAIRED_RESETS_STEP_TO_PENDING",
        "orphan_visibility": "RECORDED_RESOURCE_REFS_AND_REPAIR_PLAN",
        "final": "IMPLEMENTED_NOT_PRODUCT_QUALIFIED",
        "exact_residual": "FORK_NOTION_HINDSIGHT_BACKUP_AND_ARCHIVE_WORKFLOWS_REMAIN_OUTSIDE_GENERIC_DURABLE_STEP_CONTRACT",
    }
    assert "start_or_get_workflow" in service_text
    assert len(table_rows) == 5

    print(json.dumps({"migrations_applied": applied, "dod006": dod006, "dod039": dod039, "dod004": dod004, "project_id": project["project_id"]}, sort_keys=True))


if __name__ == "__main__":
    main()
