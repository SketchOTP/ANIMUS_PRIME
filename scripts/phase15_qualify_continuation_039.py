"""Continuation 039 reusable production-path qualification fixture builder.

The fixture is intentionally built through PRIME's Core, repository indexer,
history, progress, memory, and MCP services.  Browser qualification consumes
the resulting disposable projects; it does not insert browser-only rows.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

from src.prime_core.authority import validate_authority
from src.prime_core.brain_service import BrainService
from src.prime_core.config import Settings
from src.prime_core.db import migrate
from src.prime_core.history_service import HistoryService
from src.prime_core.indexer import RepositoryIndexer
from src.prime_core.memory_service import MemoryService
from src.prime_core.mcp_service import MCPService
from src.prime_core.progress_service import ProgressService
from src.prime_core.service import CoreService
from src.prime_memory_adapter import PrimeMemoryAdapter


ROOT = Path(os.environ.get("PRIME039_FIXTURE_ROOT", "/qualification")).resolve()


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


def make_repo(name: str, marker: str, goal: str) -> tuple[Path, str, str]:
    repo = ROOT / name
    shutil.rmtree(repo, ignore_errors=True)
    repo.mkdir(parents=True)
    git(repo, "init", "-q", "--initial-branch=main")
    git(repo, "config", "user.email", "qualification@example.invalid")
    git(repo, "config", "user.name", "Continuation 039")
    template = Path("authority-template/v1").resolve()
    for relative in (
        "AGENTS.md", "CLAUDE.md", "COMMANDMENTS_OF_THE_CODE.md", "GEMINI.md",
        ".agent/PROJECT_GOAL.md", ".agent/PROJECT_PROFILE.md", ".agent/CURRENT.md",
        ".agent/DIRECTIVES.md", ".agent/OUTCOMES.md", ".agent/LEARNINGS.md",
        ".agent/RECORD.md", ".agent/REPO_MAP.md",
    ):
        target = repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(template / relative, target)
    (repo / ".agent" / "PROJECT_GOAL.md").write_text(goal, encoding="utf-8")
    with (repo / ".agent" / "LEARNINGS.md").open("a", encoding="utf-8") as handle:
        handle.write(f"\n- {marker}: authority/search fixture marker for Continuation 039.\n")
    (repo / f"{name}-repository-marker.txt").write_text(f"{marker}\n", encoding="utf-8")
    (repo / "src" / "brain-marker.txt").parent.mkdir(parents=True)
    (repo / "src" / "brain-marker.txt").write_text(f"{marker}-BRAIN\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", f"{name} A1")
    a1 = git(repo, "rev-parse", "HEAD")
    (repo / f"{name}-A2-marker.txt").write_text(f"{marker}-A2\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", f"{name} A2")
    a2 = git(repo, "rev-parse", "HEAD")
    return repo, a1, a2


def build_project(core: CoreService, indexer: RepositoryIndexer, memory: MemoryService, progress: ProgressService, history: HistoryService, mcp: MCPService, name: str, marker: str) -> dict:
    goal_text = f"Continuation 039 qualified fixture goal for {name}. Marker {marker}."
    repo, a1, a2 = make_repo(name.lower().replace(" ", "-"), marker, goal_text)
    project = core.create_project(name, f"Independent Continuation 039 fixture {marker}")
    node_id = f"node-c039-{name.split()[-1].lower()}"
    core.register_node(node_id, f"Continuation 039 {name} Node", "linux", hashlib.sha256(node_id.encode()).hexdigest(), [str(ROOT)], {"repository": True, "brain": True})
    inspection = core.inspect_repository_for_onboarding(project["project_id"], node_id, str(repo))
    binding = core.bind_verified_repository(inspection, confirm=True)
    adopted = core.review_or_adopt_project_authority(project["project_id"], "ADOPT", confirm=True)
    goal = core.create_goal_revision(project["project_id"], goal_text, approve=True)
    baseline = progress.propose_baseline(project["project_id"], goal["goal_revision_id"], [
        {"title": "repository", "weight": 0.35, "required": True, "acceptance_expectations": ["repository evidence"]},
        {"title": "brain", "weight": 0.35, "required": True, "acceptance_expectations": ["brain evidence"]},
        {"title": "memory", "weight": 0.30, "required": False},
    ])
    progress.approve_baseline(baseline["review_id"])
    indexed = indexer.build(project["project_id"])
    brain = BrainService(core.settings).build(project["project_id"], source_revision=a2)
    evidence = history.record_evidence(project["project_id"], "UPLOAD", f"local://continuation-039/{marker}.txt", f"{marker}-EVIDENCE\n".encode(), source_revision=a2)
    assessment = progress.assess(project["project_id"], goal["goal_revision_id"], [
        {"title": "repository", "completion": 1.0, "confidence": 0.95},
        {"title": "brain", "completion": 1.0, "confidence": 0.9},
        {"title": "memory", "completion": 1.0, "confidence": 0.85},
    ], repository_revision=a2, summary=f"Current assessment for {marker}.", evidence_refs=[evidence["source_reference_id"]])
    memory_fact = memory.store(project["project_id"], f"{marker} durable native fact", "DECISION", source_revision=a2, source_reference_id=evidence["source_reference_id"])
    correction_seed = memory.store(project["project_id"], f"{marker} correction seed", "DECISION", source_revision=a2)
    correction = memory.store(project["project_id"], f"{marker} corrected durable fact", "DECISION", source_revision=a2, supersedes_memory_id=correction_seed["memory_id"], correction_reason="fixture correction")
    memory.tombstone(project["project_id"], correction["memory_id"], "fixture tombstone")
    durable_anchor = memory.store(project["project_id"], f"{marker} durable recall anchor", "DECISION", source_revision=a2, source_reference_id=evidence["source_reference_id"])
    durable_recall = memory.recall(project["project_id"], marker)
    for _ in range(40):
        if durable_recall["results"]:
            break
        time.sleep(3)
        durable_recall = memory.recall(project["project_id"], marker)
    adapter = PrimeMemoryAdapter(core.settings.hindsight_base_url, project["project_id"], core.settings.hindsight_timeout_seconds)
    bank = adapter.bank_id
    for event_type, source_ref in (("GIT_COMMIT", f"git:{a2}"), ("AUTHORITY_OBSERVED", ".agent"), ("GOAL_REVISION", goal["goal_revision_id"]), ("PROGRESS_ASSESSMENT", assessment["assessment_id"]), ("EVIDENCE_CAPTURED", evidence["source_reference_id"]), ("AI_RUN", "ai-run-c039")):
        core.emit_event(event_type, {"marker": marker, "source": source_ref}, project_id=project["project_id"], source_revision=a2, source_ref=source_ref)
    grant = mcp.issue_grant(project["project_id"], f"continuation-039-{name.split()[-1].lower()}")
    checkpoint_root = ROOT / "checkpoints" / name.split()[-1].lower()
    checkpoint_root.mkdir(parents=True, exist_ok=True)
    checkpoint = history.add_git_checkpoint(project["project_id"], str(repo), a1, str(checkpoint_root))
    authority = validate_authority(repo)
    assert authority["valid"] and indexed["source_revision"] == a2
    assert brain["source_revision"] == a2 and len(brain["nodes"]) > 0 and len(brain["edges"]) > 0
    assert durable_recall["results"], f"{name} Hindsight recall did not return a PRIME-owned fact: {durable_recall}"
    assert git(repo, "status", "--porcelain") == ""
    return {"project": project, "project_id": project["project_id"], "node_id": node_id, "repo": str(repo), "a1": a1, "a2": a2, "binding": binding, "authority": authority, "adopted": adopted, "goal": goal, "assessment": assessment, "evidence": {"evidence_id": evidence["evidence_id"], "source_reference_id": evidence["source_reference_id"]}, "brain": {"availability": "CURRENT", "source_revision": brain["source_revision"], "nodes": len(brain["nodes"]), "edges": len(brain["edges"])}, "memory": {"bank_id": bank, "durable_memory_id": durable_anchor["memory_id"], "recall_results": len(durable_recall["results"]), "correction_id": correction["memory_id"]}, "mcp_grant": grant, "checkpoint": checkpoint}


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    settings = Settings()
    migrate(settings)
    core = CoreService(settings)
    # The disposable database may have been left after a setup retry.  The
    # fixed password is only used for this disposable browser session.
    password = "continuation-039-fixture-password"
    try:
        core.login(password)
    except PermissionError:
        core.bootstrap(password)
    indexer = RepositoryIndexer(core)
    memory = MemoryService(settings)
    progress = ProgressService(settings)
    history = HistoryService(settings)
    mcp = MCPService(settings, memory)
    project_a = build_project(core, indexer, memory, progress, history, mcp, "Continuation 039 Project A", "ALPHA-039")
    project_b = build_project(core, indexer, memory, progress, history, mcp, "Continuation 039 Project B", "BETA-039")
    assert project_a["project_id"] != project_b["project_id"]
    assert project_a["memory"]["bank_id"] != project_b["memory"]["bank_id"]
    metadata = {"continuation": "039", "fixture_root": str(ROOT), "project_a": project_a, "project_b": project_b}
    Path(os.environ.get("PRIME039_FIXTURE_METADATA", str(ROOT / "fixture.json"))).write_text(json.dumps(metadata, indent=2, default=str), encoding="utf-8")
    print(json.dumps(metadata, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
