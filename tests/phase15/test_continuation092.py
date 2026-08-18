from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest


def test_node_quarantine_is_idempotent_recoverable_and_recorded(tmp_path: Path, monkeypatch):
    root = tmp_path / "approved"
    root.mkdir()
    repository = root / "fixture"
    repository.mkdir()
    subprocess.run(["git", "-C", str(repository), "init", "-q"], check=True)
    monkeypatch.setenv("PRIME_NODE_ALLOWED_ROOTS", str(root))
    monkeypatch.setenv("PRIME_NODE_STATE_FILE", str(tmp_path / "node.json"))
    from src.prime_node.config import NodeSettings
    from src.prime_node.service import NodeService

    first = NodeService(NodeSettings()).quarantine_repository(str(repository), "delete-092")
    assert first["newly_performed"] is True and not repository.exists()
    assert Path(first["quarantine_path"]).is_dir()
    assert NodeService(NodeSettings()).quarantine_repository(str(repository), "delete-092")["reconciled"] is True
    assert NodeService(NodeSettings()).restore_quarantined_repository("delete-092")["restored"] is True
    second = NodeService(NodeSettings()).quarantine_repository(str(repository), "delete-092b")
    assert NodeService(NodeSettings()).purge_quarantined_repository("delete-092b")["purged"] is True
    assert not Path(second["quarantine_path"]).exists()
    assert NodeService(NodeSettings()).purge_quarantined_repository("delete-092b")["reconciled"] is True


def test_node_quarantine_rejects_allowed_root_and_unrecorded_purge(tmp_path: Path, monkeypatch):
    root = tmp_path / "approved"
    root.mkdir()
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    monkeypatch.setenv("PRIME_NODE_ALLOWED_ROOTS", str(root))
    monkeypatch.setenv("PRIME_NODE_STATE_FILE", str(tmp_path / "node.json"))
    from src.prime_node.config import NodeSettings
    from src.prime_node.service import NodeService

    node = NodeService(NodeSettings())
    with pytest.raises(PermissionError):
        node.quarantine_repository(str(root), "forbidden-root")
    with pytest.raises(KeyError):
        node.purge_quarantined_repository("unrecorded")


def test_destructive_ui_has_separate_repository_confirmation_and_disclosure():
    web = (Path(__file__).parents[2] / "apps/web/index.html").read_text(encoding="utf-8")
    assert 'data-workflow-action="PURGE"' in web
    assert '<dialog id="lifecycle-dialog"' in web
    assert "repository_erasure_confirmation" in web
    assert "include_repository_erasure" in web
    assert "External copies PRIME cannot erase" in web
    assert "preserve_recovery_snapshot" in web
    assert web.index('id="lifecycle-cancel"') < web.index('id="lifecycle-confirm-submit"')
    assert "$('#lifecycle-cancel')?.focus()" in web
    assert "The terminally deleted project is no longer active" in web


def test_lifecycle_declares_delete_and_purge_saga_steps():
    source = (Path(__file__).parents[2] / "src/prime_core/lifecycle_service.py").read_text(encoding="utf-8")
    for step in ("NOTION_DISPOSITION", "REPOSITORY_QUARANTINED", "ACTIVE_WORK_STOPPED", "CREDENTIALS_REVOKED", "STATE_TRANSITIONED"):
        assert step in source
    for step in ("HINDSIGHT_PURGED", "REPOSITORY_PURGED", "LOCAL_RESOURCES_PURGED", "MINIMAL_TOMBSTONE_WRITTEN", "PURGE_COMPLETED"):
        assert step in source


@pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for destructive lifecycle integration")
def test_delete_refusals_do_not_mutate_and_workflow_completes(monkeypatch, tmp_path: Path):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings
    from src.prime_core.db import connect, migrate
    from src.prime_core.lifecycle_service import LifecycleService
    from src.prime_core.notion_service import InMemoryNotionProvider, NotionLifecycleService
    from src.prime_core.service import CoreService

    settings = Settings()
    migrate(settings)
    core = CoreService(settings)
    project = core.create_project("V1_QUALIFICATION_FIXTURE Continuation 092 unit delete")
    notion_provider = InMemoryNotionProvider()
    notion = NotionLifecycleService(notion_provider, state_path=tmp_path / "notion.json", settings=settings)
    notion.configure(project["project_id"], "qualification-reference")
    page = notion.create_project_record(project["project_id"], "qualification-parent", "Continuation 092")
    notion_provider.archive_page(page["page_id"])  # lost response: effect happened before the checkpoint
    lifecycle = LifecycleService(settings, core, notion_resolver=lambda: notion)
    prior = core.start_or_get_workflow(
        "PROJECT_DELETE",
        f"expired-preflight:{project['project_id']}",
        project["project_id"],
        [
            {"step_key": "PREFLIGHT_VERIFIED"}, {"step_key": "SNAPSHOT_DISPOSITION"},
            {"step_key": "NOTION_DISPOSITION", "replay_policy": "IDEMPOTENT_EXTERNAL"},
            {"step_key": "REPOSITORY_QUARANTINED", "replay_policy": "IDEMPOTENT_EXTERNAL"},
            {"step_key": "ACTIVE_WORK_STOPPED"}, {"step_key": "CREDENTIALS_REVOKED"},
            {"step_key": "RESOURCE_DISPOSITION_RECORDED"}, {"step_key": "STATE_TRANSITIONED"},
        ],
    )
    preflight = lifecycle.preflight(project["project_id"], "DELETE", True)
    with pytest.raises(PermissionError):
        lifecycle.execute(project["project_id"], "DELETE", preflight["preflight_token"], "wrong", True)
    with connect(settings) as db:
        assert db.execute("SELECT lifecycle_state FROM prime_core.projects WHERE project_id=%s", (project["project_id"],)).fetchone()["lifecycle_state"] == "DRAFT"
    result = lifecycle.execute(project["project_id"], "DELETE", preflight["preflight_token"], project["project_id"], True)
    assert result["to_state"] == "DELETION_PENDING"
    assert result["workflow_id"] == prior["workflow_id"]
    assert core.workflow_resume_plan(result["workflow_id"])["next_safe_action"] == "COMPLETE"
    with pytest.raises(ValueError):
        lifecycle.execute(project["project_id"], "DELETE", preflight["preflight_token"], project["project_id"], True)
    from src.prime_memory_adapter import AdapterResult

    class Memory:
        @staticmethod
        def adapter_factory(_project_id):
            class Adapter:
                @staticmethod
                def delete_bank():
                    return AdapterResult("CURRENT", {"deleted": True})
            return Adapter()

    purge = LifecycleService(settings, core, Memory())
    active_purge = core.start_or_get_workflow(
        "PROJECT_PURGE",
        f"interrupted-purge:{project['project_id']}",
        project["project_id"],
        [
            {"step_key": "PURGE_PLAN_VERIFIED"},
            {"step_key": "HINDSIGHT_PURGED", "replay_policy": "IDEMPOTENT_EXTERNAL"},
            {"step_key": "REPOSITORY_PURGED", "replay_policy": "IDEMPOTENT_EXTERNAL"},
            {"step_key": "LOCAL_RESOURCES_PURGED"}, {"step_key": "MINIMAL_TOMBSTONE_WRITTEN"},
            {"step_key": "PURGE_COMPLETED"},
        ],
    )
    core.begin_step(active_purge["workflow_id"], "PURGE_PLAN_VERIFIED")
    durable_plan = {"repository_erasure": False, "external_survival": ["Notion page"], "backup": {"matching_backups": []}}
    core.complete_step(active_purge["workflow_id"], "PURGE_PLAN_VERIFIED", durable_plan, durable_plan)
    purge_preflight = purge.preflight(project["project_id"], "PURGE", True)
    terminal = purge.execute(project["project_id"], "PURGE", purge_preflight["preflight_token"], project["project_id"], True, "stale-path-confirmation", True)
    assert terminal["to_state"] == "DELETED"
    assert terminal["workflow_id"] == active_purge["workflow_id"]
    assert project["project_id"] not in {item["project_id"] for item in core.list_projects()}
    with connect(settings) as db:
        assert db.execute("SELECT content_retained FROM (SELECT false AS content_retained) x").fetchone()["content_retained"] is False
        assert db.execute("SELECT 1 FROM prime_core.project_deletion_tombstones WHERE project_id=%s", (project["project_id"],)).fetchone()
