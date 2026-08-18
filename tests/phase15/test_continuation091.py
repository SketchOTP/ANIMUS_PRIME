from __future__ import annotations

import os
import hashlib
import subprocess
from pathlib import Path

import pytest

from src.prime_core.workflow_primitives import (
    QualificationInterruption,
    qualification_interrupt,
    resume_plan_payload,
)


def test_qualification_interrupt_is_exact_and_disabled_by_default(monkeypatch):
    monkeypatch.delenv("PRIME_QUALIFICATION_INTERRUPT", raising=False)
    qualification_interrupt("FORK_PROJECT", "REPOSITORY_CLONED", "BEFORE_EXTERNAL_CALL")
    monkeypatch.setenv("PRIME_QUALIFICATION_INTERRUPT", "FORK_PROJECT:REPOSITORY_CLONED:BEFORE_EXTERNAL_CALL")
    with pytest.raises(QualificationInterruption):
        qualification_interrupt("FORK_PROJECT", "REPOSITORY_CLONED", "BEFORE_EXTERNAL_CALL")
    qualification_interrupt("FORK_PROJECT", "REPOSITORY_CLONED", "EXTERNAL_SUCCESS_BEFORE_PERSIST")


def test_resume_plan_exposes_expected_created_and_reconciliation_resources():
    plan = resume_plan_payload(
        {"workflow_id": "workflow-091", "status": "REPAIR_REQUIRED"},
        [
            {"step_key": "EXPECTED", "step_order": 0, "status": "SUCCEEDED", "replay_policy": "PURE_OR_DB_TRANSACTION"},
            {"step_key": "CREATED", "step_order": 1, "status": "RUNNING", "replay_policy": "NON_IDEMPOTENT_EXTERNAL"},
        ],
        [
            {"resource_type": "REPOSITORY", "resource_key": "child", "status": "EXPECTED"},
            {"resource_type": "NOTION_PAGE", "resource_key": "record", "status": "RECONCILIATION_REQUIRED"},
        ],
    )
    assert plan["required_reconciliation"] is True
    assert plan["next_safe_action"] == "REPAIR_REQUIRED"
    assert {item["status"] for item in plan["recorded_resource_refs"]} == {"EXPECTED", "RECONCILIATION_REQUIRED"}


def test_all_converted_boundaries_declare_durable_steps_and_diagnostics():
    root = Path(__file__).parents[2]
    core = (root / "src/prime_core/service.py").read_text(encoding="utf-8")
    notion = (root / "src/prime_core/notion_service.py").read_text(encoding="utf-8")
    memory = (root / "src/prime_core/memory_service.py").read_text(encoding="utf-8")
    backup = (root / "src/prime_core/backup_service.py").read_text(encoding="utf-8")
    api = (root / "apps/core/main.py").read_text(encoding="utf-8")
    for step in ("REPOSITORY_CLONED", "AUTHORITY_PROVISIONED", "MCP_SCOPE_ISSUED", "HINDSIGHT_BOUND", "FINALIZED"):
        assert step in core
    for step in ("PAGE_EXPECTED", "PAGE_CREATED", "PAGE_BOUND"):
        assert step in notion
    for step in ("BANK_EXPECTED", "BANK_CREATED", "BANK_BOUND"):
        assert step in memory
    for step in ("INPUT_VALIDATED", "CANONICAL_STATE_APPLIED", "POST_RESTORE_VERIFIED"):
        assert step in backup
    assert "/v1/workflows/reconciliation" in api
    assert "not notion_state.page_id" in api


@pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for durable workflow integration")
def test_persistent_repair_plan_and_orphan_visibility_survive_service_instance(monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.service import CoreService

    settings = Settings()
    migrate(settings)
    first = CoreService(settings)
    project = first.create_project("Continuation 091 workflow persistence")
    workflow = first.start_or_get_workflow("QUALIFICATION_091", f"qualification-091:{project['project_id']}", project["project_id"], [
        {"step_key": "EXTERNAL", "replay_policy": "NON_IDEMPOTENT_EXTERNAL"},
    ])
    first.record_workflow_resource(workflow["workflow_id"], "QUALIFICATION_RESOURCE", "resource-a", "qualification://resource-a", {"purpose": "DOD-004"}, "EXPECTED")
    assert first.begin_step(workflow["workflow_id"], "EXTERNAL")["decision"] == "START"

    restarted = CoreService(Settings())
    assert restarted.begin_step(workflow["workflow_id"], "EXTERNAL")["decision"] == "REPAIR_REQUIRED"
    plan = restarted.workflow_resume_plan(workflow["workflow_id"])
    assert plan["required_reconciliation"] is True
    assert plan["recorded_resource_refs"][0]["status"] == "EXPECTED"
    report = restarted.workflow_reconciliation_report(project["project_id"])
    assert report["status"] == "ACTION_REQUIRED"
    assert report["operator_action_required"] is True


@pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for durable workflow integration")
def test_hindsight_stable_put_replays_without_duplicate_bank(monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.memory_service import MemoryService
    from src.prime_core.service import CoreService
    from src.prime_memory_adapter import AdapterResult

    class StableBank:
        calls = 0

        def create_bank(self):
            self.calls += 1
            return AdapterResult("CURRENT", {"id": "stable-bank"})

    settings = Settings()
    migrate(settings)
    project = CoreService(settings).create_project("Continuation 091 Hindsight bank")
    adapter = StableBank()
    service = MemoryService(settings, lambda _project_id: adapter)
    first = service.ensure_bank(project["project_id"])
    second = MemoryService(settings, lambda _project_id: adapter).ensure_bank(project["project_id"])
    assert first["bank_id"] == second["bank_id"] == f"prime-{project['project_id']}"
    assert adapter.calls == 1
    assert CoreService(settings).workflow_resume_plan(first["workflow_id"])["next_safe_action"] == "COMPLETE"


@pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for durable workflow integration")
def test_notion_response_checkpoint_reconciles_one_provider_page_across_service_restart(tmp_path, monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.notion_service import InMemoryNotionProvider, NotionLifecycleService
    from src.prime_core.service import CoreService

    settings = Settings()
    migrate(settings)
    project = CoreService(settings).create_project("Continuation 091 Notion resource")
    provider = InMemoryNotionProvider()
    state_path = tmp_path / "notion-state.json"
    first = NotionLifecycleService(provider, state_path=state_path, settings=settings)
    first.configure(project["project_id"], "secure/ref/notion")
    monkeypatch.setenv("PRIME_QUALIFICATION_INTERRUPT", "CREATE_NOTION_PROJECT_RECORD:PAGE_CREATED:EXTERNAL_SUCCESS_BEFORE_PERSIST")
    with pytest.raises(QualificationInterruption):
        first.create_project_record(project["project_id"], "qualification-parent", "Continuation 091")
    assert len(provider.pages) == 1
    monkeypatch.delenv("PRIME_QUALIFICATION_INTERRUPT")

    restarted = NotionLifecycleService(provider, state_path=state_path, settings=Settings())
    restarted.configure(project["project_id"], "secure/ref/notion")
    result = restarted.create_project_record(project["project_id"], "qualification-parent", "Continuation 091")
    repeated = NotionLifecycleService(provider, state_path=state_path, settings=Settings()).create_project_record(project["project_id"], "qualification-parent", "Continuation 091")
    assert result["page_id"] == repeated["page_id"]
    assert len(provider.pages) == 1
    report = CoreService(settings).workflow_reconciliation_report(project["project_id"])
    assert report["status"] == "CLEAR"


@pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for durable workflow integration")
def test_supported_compensation_and_resource_release_are_durable(monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.service import CoreService

    settings = Settings()
    migrate(settings)
    core = CoreService(settings)
    project = core.create_project("Continuation 091 compensation")
    workflow = core.start_or_get_workflow("QUALIFICATION_COMPENSATION", f"compensate:{project['project_id']}", project["project_id"], [{"step_key": "REVERSIBLE", "replay_policy": "IDEMPOTENT_EXTERNAL"}])
    core.begin_step(workflow["workflow_id"], "REVERSIBLE")
    core.record_workflow_resource(workflow["workflow_id"], "QUALIFICATION_RESOURCE", "reversible", "qualification://reversible", {}, "CREATED")
    core.compensate_step(workflow["workflow_id"], "REVERSIBLE", {"compensation": "SUPPORTED_REVERSE_COMPLETED"})
    core.record_workflow_resource(workflow["workflow_id"], "QUALIFICATION_RESOURCE", "reversible", "qualification://reversible", {"compensation": "SUPPORTED_REVERSE_COMPLETED"}, "RELEASED")
    core.complete_workflow(workflow["workflow_id"], "REVERSIBLE")
    plan = CoreService(Settings()).workflow_resume_plan(workflow["workflow_id"])
    assert plan["next_safe_action"] == "COMPLETE"
    assert plan["recorded_resource_refs"][0]["status"] == "RELEASED"


@pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for durable workflow integration")
def test_fork_adopts_clone_after_interruption_without_duplicate_project_or_repository(tmp_path, monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings
    from src.prime_core.db import connect, migrate
    from src.prime_core.notion_service import InMemoryNotionProvider, NotionLifecycleService
    from src.prime_core.progress_service import ProgressService
    from src.prime_core.service import CoreService

    def git(root: Path, *args: str) -> str:
        return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout.strip()

    settings = Settings()
    migrate(settings)
    source = tmp_path / "source"
    source.mkdir()
    git(source, "init", "-q")
    git(source, "config", "user.email", "qualification@example.invalid")
    git(source, "config", "user.name", "Qualification")
    (source / "README.md").write_text("Continuation 091 durable Fork\n", encoding="utf-8")
    git(source, "add", ".")
    git(source, "commit", "-qm", "qualification source")
    revision = git(source, "rev-parse", "HEAD")

    core = CoreService(settings)
    class LocalNode:
        def inspect_repository(self, path: str):
            root = Path(path).resolve()
            return {
                "canonical_path": str(root),
                "git_common_dir": str(root / ".git"),
                "identity_fingerprint": hashlib.sha256(str(root).encode()).hexdigest(),
                "is_bare": False,
                "branch": git(root, "branch", "--show-current") or "DETACHED",
                "authority_state": "PROVISIONED",
            }

        def write_project_goal(self, path: str, content: str, content_hash: str):
            target = Path(path) / "PROJECT_GOAL.md"
            target.write_text(content, encoding="utf-8")
            return {"status": "CURRENT", "content_hash": content_hash}

    monkeypatch.setattr(CoreService, "_node_client", lambda self, node: LocalNode())
    source_project = core.create_project("Continuation 091 Fork source")
    node_id = f"node-091-{source_project['project_id']}"
    core.register_node(node_id, "Continuation 091 local Node", "linux", source_project["project_id"].replace("project_", "")[:64], [str(tmp_path)], {})
    core.bind_repository(source_project["project_id"], node_id, f"identity-{source_project['project_id']}", str(source))
    goal_content = """# Project Goal
What and why: preserve a durable qualification fork.
Target user and operator: the PRIME operator.
Desired end state and outcome: an isolated child project.
Functional requirements: clone the selected revision.
Constraints and non-functional requirements: no shared mutable state.
Success and acceptance: child resources are independently identified.
Validation and evidence: verify identities and restart recovery.
Non-goals and out of scope: no external device qualification.
Failure and stop rules: stop on ambiguous external state.
"""
    goal = core.create_goal_revision(source_project["project_id"], goal_content, approve=True)
    baseline_items = [{"title": "isolated child", "description": "Verify child isolation", "weight": 1.0, "required": True, "acceptance_expectations": ["identity evidence"]}]
    review = ProgressService(settings).propose_baseline(source_project["project_id"], goal["goal_revision_id"], baseline_items)
    ProgressService(settings).approve_baseline(review["review_id"])
    notion = NotionLifecycleService(InMemoryNotionProvider(), settings=settings)
    request = dict(source_project_id=source_project["project_id"], source_revision=revision, destination_node_id=node_id, parent_path=str(tmp_path), repository_name="child", project_name="Continuation 091 child", remote_action="CLEAR", notion_parent_id="qualification-parent", progress_items=baseline_items)
    preflight = core.fork_preflight(**request)
    invoke = lambda instance: instance.fork_project(**request, preflight_fingerprint=preflight["preflight_fingerprint"], approve_child_goal=True, approve_progress_baseline=True, notion_lifecycle=notion, confirm=True)

    monkeypatch.setenv("PRIME_QUALIFICATION_INTERRUPT", "FORK_PROJECT:REPOSITORY_CLONED:EXTERNAL_SUCCESS_BEFORE_PERSIST")
    with pytest.raises(QualificationInterruption):
        invoke(core)
    assert (tmp_path / "child" / ".git").is_dir()
    monkeypatch.delenv("PRIME_QUALIFICATION_INTERRUPT")

    resumed = invoke(CoreService(Settings()))
    repeated = invoke(CoreService(Settings()))
    assert resumed["workflow_id"] == repeated["workflow_id"]
    assert resumed["project"]["project_id"] == repeated["project"]["project_id"]
    assert resumed["destination_revision"] == revision
    with connect(settings) as db:
        project_count = db.execute("SELECT count(*) AS count FROM prime_core.projects WHERE project_id=%s", (resumed["project"]["project_id"],)).fetchone()["count"]
        repository_count = db.execute("SELECT count(*) AS count FROM prime_core.repositories WHERE project_id=%s", (resumed["project"]["project_id"],)).fetchone()["count"]
    assert project_count == repository_count == 1
    plan = CoreService(settings).workflow_resume_plan(resumed["workflow_id"])
    assert plan["next_safe_action"] == "COMPLETE"
    assert not [resource for resource in plan["recorded_resource_refs"] if resource["status"] in {"EXPECTED", "RECONCILIATION_REQUIRED"}]
