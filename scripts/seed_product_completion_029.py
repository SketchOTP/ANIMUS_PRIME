#!/usr/bin/env python3
"""Create a disposable, production-service-backed project fixture for Continuation 029."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

from src.prime_core.config import Settings
from src.prime_core.db import migrate, transaction
from src.prime_core.history_service import HistoryService
from src.prime_core.indexer import RepositoryIndexer
from src.prime_core.memory_service import MemoryService
from src.prime_core.service import CoreService, _id, now


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True)
    return result.stdout.strip()


def make_repo(root: Path, label: str) -> tuple[Path, str]:
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q")
    git(root, "config", "user.email", "prime-product-029@example.invalid")
    git(root, "config", "user.name", "PRIME Product Fixture")
    (root / "README.md").write_text(f"# {label}\n\nThis is a disposable PRIME handoff fixture.\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-qm", "fixture baseline")
    (root / "PROJECT_GOAL.md").write_text(
        "# Project Goal\n\nMake the managed project understandable and resumable for every coding agent.\n\n## Acceptance\n- A fresh agent can identify current work, blockers, and evidence.\n- Context export is bounded, project-scoped, and redacted.\n",
        encoding="utf-8",
    )
    agent = root / ".agent"
    agent.mkdir()
    (agent / "CURRENT.md").write_text("# Current State\n\nCurrent work: qualify the project handoff slice.\n\nBlocker: one external provider is unavailable.\n", encoding="utf-8")
    (agent / "DIRECTIVES.md").write_text("# Directives\n\n- Continue source-grounded product qualification.\n", encoding="utf-8")
    (agent / "OUTCOMES.md").write_text("# Outcomes\n\n- Prior attempt exposed a stale-job recovery failure.\n", encoding="utf-8")
    (agent / "LEARNINGS.md").write_text("# Learnings\n\n- Windows service aliases are not portable; use the active interpreter.\n", encoding="utf-8")
    (agent / "RECORD.md").write_text("# Record\n\n- Authority remains append-only and source-linked.\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-qm", "fixture authority and goal")
    branch = "fixture/experiment"
    git(root, "checkout", "-qb", branch)
    (root / "progress.txt").write_text("Progress changed after the experiment.\n", encoding="utf-8")
    git(root, "add", "progress.txt")
    git(root, "commit", "-qm", "fixture experiment progress")
    git(root, "checkout", "-q", "-B", "main")
    return root, git(root, "rev-parse", "HEAD")


def seed() -> dict[str, str]:
    settings = Settings()
    migrate(settings)
    temp_root = Path(tempfile.mkdtemp(prefix="prime-product-029-"))
    repo_a, revision_a = make_repo(temp_root / "project-a", "Project A")
    repo_b, revision_b = make_repo(temp_root / "project-b", "Project B")
    core = CoreService(settings)
    project_a = core.create_project("Continuity Handoff Fixture A")
    project_b = core.create_project("Isolation Fixture B")
    node_a = "node-product-029-a"
    node_b = "node-product-029-b"
    core.register_node(node_a, "Atlas Fixture Node A", "windows", hashlib.sha256(node_a.encode()).hexdigest(), [str(temp_root)], {"git": True, "repository_browser": True})
    core.register_node(node_b, "Atlas Fixture Node B", "windows", hashlib.sha256(node_b.encode()).hexdigest(), [str(temp_root)], {"git": True})
    core.bind_repository(project_a["project_id"], node_a, hashlib.sha256(str(repo_a).encode()).hexdigest(), str(repo_a))
    core.bind_repository(project_b["project_id"], node_b, hashlib.sha256(str(repo_b).encode()).hexdigest(), str(repo_b))
    goal_content = (repo_a / "PROJECT_GOAL.md").read_text(encoding="utf-8")
    goal = core.create_goal_revision(project_a["project_id"], goal_content, approve=True)
    core.create_goal_revision(project_b["project_id"], "# Project B\n\nKeep the isolation marker private.\n", approve=True)
    authority_content = (repo_a / ".agent/CURRENT.md").read_text(encoding="utf-8")
    core.record_authority_revision(project_a["project_id"], ".agent/CURRENT.md", hashlib.sha256(authority_content.encode()).hexdigest(), "VALID", {"fixture": "continuation-029", "source": "bound-repository"}, authority_content, revision_a)
    core.record_authority_revision(project_a["project_id"], ".agent/CURRENT.md", hashlib.sha256((authority_content + "\nrevision-2").encode()).hexdigest(), "VALID", {"fixture": "continuation-029", "revision": 2}, authority_content, revision_a)
    indexed = RepositoryIndexer(core).build(project_a["project_id"])
    history = HistoryService(settings)
    history.add_git_checkpoint(project_a["project_id"], str(repo_a), revision_a, str(temp_root / "history"))
    memory = MemoryService(settings)
    memory.store(project_a["project_id"], "A prior stale-job recovery attempt failed and required a durable repair state.", "FAILURE", revision_a, branch_context="main")
    memory.store(project_a["project_id"], "The Atlas Windows environment does not provide a python3 command alias.", "ENVIRONMENT", revision_a, branch_context="main")
    memory.store(project_a["project_id"], "Keep PRIME source records separate from Hindsight native availability.", "LEARNING", revision_a, branch_context="main")
    history.record_evidence(project_a["project_id"], "EXTERNAL_REFERENCE", "https://example.invalid/prime-product-029-evidence", source_revision=revision_a)
    core.emit_event("DIRECTIVE_STARTED", {"summary": "Continuation 029 project handoff work began", "category": "Authority"}, project_id=project_a["project_id"])
    core.emit_event("PRIOR_FAILURE_RECORDED", {"summary": "Stale-job recovery required repair", "category": "System"}, project_id=project_a["project_id"])
    core.emit_event("PROGRESS_CHANGED", {"summary": "Progress moved from 42 to 68 after evidence review", "category": "Progress"}, project_id=project_a["project_id"])
    core.emit_event("ENVIRONMENT_QUIRK", {"summary": "Hindsight retain is unavailable in this qualification environment", "category": "Node"}, project_id=project_a["project_id"])
    core.emit_event("PROJECT_B_PRIVATE_MARKER", {"summary": "This marker belongs only to Project B"}, project_id=project_b["project_id"])
    with transaction(settings) as db:
        item_a = _id("goalitem")
        item_b = _id("goalitem")
        db.execute("INSERT INTO prime_core.goal_items(goal_item_id,project_id,goal_revision_id,title,description,weight,required,acceptance_expectations) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (item_a, project_a["project_id"], goal["goal_revision_id"], "Understand current work", "A replacement agent can identify current work and blockers.", 0.6, True, json.dumps(["context export identifies source revisions", "overview shows current directive"])))
        db.execute("INSERT INTO prime_core.goal_items(goal_item_id,project_id,goal_revision_id,title,description,weight,required,acceptance_expectations) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (item_b, project_a["project_id"], goal["goal_revision_id"], "Preserve continuity", "Historical failures and environment quirks remain inspectable.", 0.4, True, json.dumps(["memory and activity contain prior failure", "authority files are readable"])))
        for offset, percent, confidence, summary in ((-1, 42, 0.62, "Initial assessment before evidence review."), (0, 68, 0.84, "Evidence review improved continuity confidence; one provider remains unavailable.")):
            db.execute("INSERT INTO prime_core.progress_assessments(assessment_id,project_id,goal_revision_id,repository_revision,progress_percent,confidence,freshness_state,summary,item_results,evidence_refs,created_at) VALUES (%s,%s,%s,%s,%s,%s,'CURRENT',%s,%s,%s,now() + (%s * interval '1 second'))", (_id("assessment"), project_a["project_id"], goal["goal_revision_id"], revision_a, percent, confidence, summary, json.dumps({item_a: percent >= 60, item_b: percent >= 60}), json.dumps([]), offset))
        db.execute("INSERT INTO prime_core.notion_projects(project_id,page_id,page_url,connection_status,managed_content_hash,last_synced_at,updated_at) VALUES (%s,%s,%s,'DEGRADED',%s,now(),now()) ON CONFLICT (project_id) DO UPDATE SET connection_status='DEGRADED',last_synced_at=now(),updated_at=now()", (project_a["project_id"], "fixture-page-029", "https://notion.example.invalid/fixture-page-029", hashlib.sha256(b"fixture-notion").hexdigest()))
        db.execute("INSERT INTO prime_core.ai_runs(run_id,project_id,function,provider,model,profile_revision,prompt_revision,schema_revision,retrieval_policy_revision,fixture_revision,privacy_mode,source_revision_set,created_at,status,error_class,result) VALUES (%s,%s,'ASK_PRIME','fixture-provider','fixture-model','profile-029','prompt-029','schema-029','retrieval-029','fixture-029','LOCAL_ONLY',%s,now(),'DEGRADED','PROVIDER_UNAVAILABLE',%s)", (_id("run"), project_a["project_id"], json.dumps([revision_a]), json.dumps({"answer": "UNKNOWN", "citations": []})))
        db.execute("UPDATE prime_core.projects SET lifecycle_state='ACTIVE',connectivity_state='ONLINE',freshness_state='CURRENT',work_condition='BLOCKED',updated_at=now() WHERE project_id=%s", (project_a["project_id"],))
    return {"project_id": project_a["project_id"], "project_b_id": project_b["project_id"], "repository_path": str(repo_a), "project_b_repository_path": str(repo_b), "canonical_revision": revision_a, "indexed_files": str(indexed["files_indexed"]), "fixture_root": str(temp_root)}


if __name__ == "__main__":
    print(json.dumps(seed(), sort_keys=True))
