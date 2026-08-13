"""Bounded direct qualification of the protected Fork/Clone contract."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

from src.prime_core.authority import validate_authority
from src.prime_core.config import Settings
from src.prime_core.db import connect
from src.prime_core.mcp_service import MCPService
from src.prime_core.memory_service import MemoryService
from src.prime_core.progress_service import ProgressService
from src.prime_core.service import CoreService
from src.prime_memory_adapter import PrimeMemoryAdapter


def git(path: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(path), *args], check=True, capture_output=True, text=True).stdout.strip()


def main() -> None:
    metadata_path = Path(os.environ.get("PRIME040_FIXTURE_METADATA", "/tmp/prime040-fixture/fixture.json"))
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    root = Path(metadata["fixture_root"])
    source = metadata["project_a"]
    settings = Settings()
    core = CoreService(settings)
    memory = MemoryService(settings)
    progress = ProgressService(settings)
    mcp = MCPService(settings, memory)
    source_root = Path(source["repo"])
    child_name = os.environ.get("PRIME040_FORK_CHILD_NAME", "c040-fork-a2")
    target = root / child_name
    if target.exists():
        raise RuntimeError(f"unexpected existing target: {target}")

    fork = core.fork_project(source["project_id"], source["a2"], source["node_id"], str(root), child_name, confirm=True)
    child = fork["project"]
    child_id = child["project_id"]
    child_root = Path(fork["binding"]["canonical_path"])

    with connect(settings) as db:
        draft = db.execute("SELECT goal_revision_id,status,content_hash FROM prime_core.goal_revisions WHERE project_id=%s ORDER BY revision_number DESC LIMIT 1", (child_id,)).fetchone()
        child_progress_before = db.execute("SELECT COUNT(*) AS count FROM prime_core.progress_assessments WHERE project_id=%s", (child_id,)).fetchone()["count"]
        source_progress = db.execute("SELECT COUNT(*) AS count FROM prime_core.progress_assessments WHERE project_id=%s", (source["project_id"],)).fetchone()["count"]
        child_memory_before = db.execute("SELECT COUNT(*) AS count FROM prime_core.memory_records WHERE project_id=%s", (child_id,)).fetchone()["count"]

    child_goal = core.create_goal_revision(child_id, "Independent Continuation 040 child goal. Operator-approved after Fork draft review.", approve=True)
    baseline = progress.propose_baseline(child_id, child_goal["goal_revision_id"], [{"title": "child repository", "weight": 1.0, "required": False}])
    baseline_approved = progress.approve_baseline(baseline["review_id"])
    assessment = progress.assess(child_id, child_goal["goal_revision_id"], [{"title": "child repository", "completion": 1.0, "confidence": 0.9}], repository_revision=source["a2"], summary="Independent child baseline after explicit operator approval.")

    child_memory = memory.store(child_id, "C040 child-only memory", "DECISION", source_revision=source["a2"])
    source_memory = memory.recall(source["project_id"], "C040 child-only memory")
    child_memory_rows = memory.recall(child_id, "C040 child-only memory")

    source_grant = source["mcp_grant"]
    child_grant = fork["mcp_grant"]
    source_scope = mcp.call(source_grant["token"], "prime_memory_timeline", {"project_id": child_id})
    child_scope = mcp.call(child_grant["token"], "prime_memory_timeline", {"project_id": source["project_id"]})

    dirty_marker = source_root / "continuation-040-dirty-refusal.tmp"
    dirty_marker.write_text("temporary qualification marker\n", encoding="utf-8")
    try:
        try:
            core.fork_project(source["project_id"], source["a2"], source["node_id"], str(root), "c040-dirty-refused", confirm=True)
        except ValueError as exc:
            dirty_refusal = str(exc)
        else:
            raise AssertionError("dirty source fork unexpectedly succeeded")
    finally:
        dirty_marker.unlink(missing_ok=True)

    child_authority = validate_authority(child_root)
    template_mismatches = []
    for relative in child_authority["files"]:
        if relative == ".agent/PROJECT_GOAL.md":
            continue
        template_hash = hashlib.sha256((Path("authority-template/v1") / relative).read_bytes()).hexdigest()
        child_hash = hashlib.sha256((child_root / relative).read_bytes()).hexdigest()
        if child_hash != template_hash:
            template_mismatches.append(relative)
    child_goal_differs_from_template = hashlib.sha256((child_root / ".agent/PROJECT_GOAL.md").read_bytes()).hexdigest() != hashlib.sha256((Path("authority-template/v1") / ".agent/PROJECT_GOAL.md").read_bytes()).hexdigest()
    result = {
        "source_project_id": source["project_id"],
        "child_project_id": child_id,
        "source_revision": source["a2"],
        "child_revision": git(child_root, "rev-parse", "HEAD"),
        "child_revision_matches_source": git(child_root, "rev-parse", "HEAD") == source["a2"],
        "source_history_count": int(git(source_root, "rev-list", "--count", "HEAD")),
        "child_history_count": int(git(child_root, "rev-list", "--count", "HEAD")),
        "child_remotes": git(child_root, "remote").splitlines(),
        "authority": {"valid": child_authority["valid"], "template_hashes_match_except_explicit_child_goal": not template_mismatches, "template_mismatches": template_mismatches, "child_goal_differs_from_template_after_approval": child_goal_differs_from_template, "provenance": fork["authority_provenance"]},
        "goal": {"fork_draft_status": draft["status"], "child_approved_goal_id": child_goal["goal_revision_id"], "baseline": baseline_approved, "assessment": assessment["assessment_id"], "source_progress_count": int(source_progress), "child_progress_before_approval": int(child_progress_before)},
        "memory": {"before": int(child_memory_before), "child_store_status": child_memory["status"], "source_recall_child_token_count": len(source_memory["results"]), "child_recall_child_token_count": len(child_memory_rows["results"]), "source_bank": f"prime-{source['project_id']}", "child_bank": f"prime-{child_id}"},
        "mcp": {"source_grant": source_grant["grant_id"], "child_grant": child_grant["grant_id"], "source_scope_project": source_scope.get("project_id"), "child_scope_project": child_scope.get("project_id")},
        "dirty_refusal": dirty_refusal,
        "notion": "NOT_CONFIGURED_IN_DISPOSABLE_FIXTURE",
        "hindsight": {"source_bank": PrimeMemoryAdapter(settings.hindsight_base_url, source["project_id"]).bank_id, "child_bank": PrimeMemoryAdapter(settings.hindsight_base_url, child_id).bank_id, "bank_ids_distinct": source["project_id"] != child_id, "retain_recall": "DEGRADED_IN_DISPOSABLE_PROVIDER"},
    }
    print(json.dumps(result, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
