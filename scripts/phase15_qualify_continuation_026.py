"""Create a disposable production-state A/B/C/D fixture for Continuation 026."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.prime_memory_adapter import AdapterResult
from src.prime_core.brain_service import BrainService
from src.prime_core.config import Settings
from src.prime_core.db import connect, migrate
from src.prime_core.history_service import HistoryService
from src.prime_core.indexer import RepositoryIndexer
from src.prime_core.memory_service import MemoryService
from src.prime_core.notion_service import NotionProjectionService
from src.prime_core.progress_service import ProgressService
from src.prime_core.service import CoreService


class QualificationMemory:
    def retain_verified(self, content: str, document_id: str) -> AdapterResult:
        return AdapterResult("CURRENT", {"document_id": document_id})

    def recall(self, query: str) -> AdapterResult:
        return AdapterResult("CURRENT", {"results": []})


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)
    return result.stdout.strip()


def main() -> None:
    settings = Settings(database_url=os.getenv("PRIME_PHASE1_DB_URL", "postgresql://prime:phase1-local-only@127.0.0.1:15432/prime"))
    migrate(settings)
    repo = Path(tempfile.mkdtemp(prefix="prime-c026-history-"))
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "qualification@example.invalid")
    git(repo, "config", "user.name", "Continuation 026 Qualification")

    core = CoreService(settings)
    project = core.create_project("C026 real historical A B C D")
    project_id = project["project_id"]
    node_id = "node-c026-" + os.urandom(4).hex()
    core.register_node(node_id, "Continuation 026 Node", "linux", hashlib.sha256(node_id.encode()).hexdigest(), [str(repo)], {})
    core.bind_repository(project_id, node_id, hashlib.sha256(str(repo).encode()).hexdigest(), str(repo))

    history = HistoryService(settings)
    memory = MemoryService(settings, adapter_factory=lambda _project_id: QualificationMemory())
    notion = NotionProjectionService(settings)
    progress = ProgressService(settings)
    brain = BrainService(settings)
    indexer = RepositoryIndexer(core)
    checkpoint_root = repo.parent / (repo.name + "-checkpoints")
    revisions: dict[str, str] = {}
    cutoffs: dict[str, str] = {}
    evidence_paths: dict[str, str] = {}
    p1_a_memory_id: str | None = None
    p1_b_memory_id: str | None = None
    goal_revision_id: str | None = None

    states = {
        "A": ("Authority v1", "VALID", 20, "P1: the approved goal remains valid (recorded at A)", "Evidence A supports P1"),
        "B": ("Authority v2", "VALID", 45, "P1: the approved goal remains valid (reaffirmed at B)", "Evidence B supports P1"),
        "C": ("Authority v2 with failed validation", "INVALID", 35, "P2: validation disproves P1 (correction at C)", "Evidence C disproves P1"),
        "D": ("Authority v2 corrected", "VALID", 75, "P2: validation correction is current (confirmed at D)", "Evidence D confirms P2"),
    }

    for label, (authority_text, authority_status, progress_value, memory_text, evidence_text) in states.items():
        (repo / "state.txt").write_text(f"STATE {label}\n{authority_text}\n{evidence_text}\n", encoding="utf-8")
        git(repo, "add", "state.txt")
        git(repo, "commit", "-qm", f"State {label}")
        revision = git(repo, "rev-parse", "HEAD")
        revisions[label] = revision
        indexer.build(project_id)
        core.record_authority_revision(project_id, f".agent/state-{label}.md", revision, authority_status, canonical_commit=revision)
        evidence = history.store_uploaded_evidence(project_id, f"evidence-{label}.txt", evidence_text.encode(), "text/plain", source_revision=revision)
        evidence_paths[label] = evidence["storage_path"]
        if label == "A":
            goal = core.create_goal_revision(project_id, "Goal v1: preserve truthful project continuity", approve=True)
            goal_revision_id = goal["goal_revision_id"]
            review = progress.propose_baseline(project_id, goal_revision_id, [{"title": "continuity", "weight": 1.0, "completion": 0.0}])
            progress.approve_baseline(review["review_id"])
        progress.assess(project_id, goal_revision_id, [{"title": "continuity", "weight": 1.0, "completion": progress_value / 100, "confidence": 1.0}], repository_revision=revision, summary=f"Progress {progress_value}")
        stored = memory.store(project_id, memory_text, "FACT", source_revision=revision, source_reference_id=evidence["source_reference_id"], supersedes_memory_id=p1_a_memory_id if label == "C" else None, correction_reason="Evidence C disproves P1" if label == "C" else None)
        if label == "A":
            p1_a_memory_id = stored.get("memory_id")
        elif label == "B":
            p1_b_memory_id = stored.get("memory_id")
        elif label == "C" and p1_b_memory_id:
            memory.tombstone(project_id, p1_b_memory_id, "P2 correction supersedes the B affirmation", correction_type="SUPERSEDE")
        notion._record(project_id, evidence["content_hash"], "SYNCED", {"source_revision": revision}, f"State {label} / {evidence['source_reference_id']}")
        history.add_git_checkpoint(project_id, str(repo), revision, str(checkpoint_root))
        brain.build(project_id, revision)
        time.sleep(0.08)
        cutoffs[label] = datetime.now(timezone.utc).isoformat()

    with connect(settings) as db:
        rows = db.execute("SELECT memory_id,content,status,source_revision FROM prime_core.memory_records WHERE project_id=%s ORDER BY created_at", (project_id,)).fetchall()
        correction_rows = db.execute("SELECT memory_id,correction_type,reason FROM prime_core.memory_corrections WHERE project_id=%s", (project_id,)).fetchall()

    print(json.dumps({
        "status": "READY",
        "project_id": project_id,
        "project_name": project["name"],
        "repository": str(repo),
        "checkpoint_root": str(checkpoint_root),
        "revisions": revisions,
        "cutoffs": cutoffs,
        "evidence_paths": evidence_paths,
        "current_memory": [dict(row) for row in rows],
        "corrections": [dict(row) for row in correction_rows],
        "goal_revision_id": goal_revision_id,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
