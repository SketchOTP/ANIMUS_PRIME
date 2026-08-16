from __future__ import annotations

import pytest

from src.prime_core.notion_service import (
    InMemoryNotionProvider,
    NotionLifecycleService,
    NotionProviderError,
)


def configured(history_limit: int = 2):
    provider = InMemoryNotionProvider()
    service = NotionLifecycleService(provider, history_limit=history_limit)
    assert service.configure("project-a", "notion-credential-ref")['status'] == "CONNECTED"
    return provider, service


def bind(service: NotionLifecycleService):
    result = service.create_project_record("project-a", "approved-parent", "Project A")
    assert result["status"] == "BOUND"
    return result["page_id"]


def test_project_record_create_retry_after_lost_response_is_idempotent():
    provider, service = configured()
    provider.lost_response_once = True
    result = service.create_project_record("project-a", "parent", "A")
    assert result["status"] == "BOUND"
    assert len(provider.pages) == 1
    again = service.create_project_record("project-a", "parent", "A")
    assert again["idempotent"] is True


def test_existing_page_binding_preserves_user_content_and_targeted_updates():
    provider, service = configured()
    page_id = bind(service)
    page = provider.pages[page_id]
    page.content = "User introduction\n\n" + page.content + "\n\nUser notes\nUser checklist"
    assert service.configure("project-b", "notion-credential-ref")["status"] == "CONNECTED"
    assert service.bind_existing("project-b", page_id)["status"] == "BOUND"
    result = service.document("project-b", {"CURRENT_STATUS": "ONLINE", "PROGRESS": "25%"}, "commit-b", source_rank=2)
    assert result["status"] == "SYNCED"
    assert "User introduction" in page.content and "User notes" in page.content and "User checklist" in page.content
    assert "ONLINE" in page.content


def test_manual_managed_edit_is_a_conflict_and_old_job_cannot_overwrite_newer():
    provider, service = configured()
    page_id = bind(service)
    assert service.document("project-a", {"CURRENT_STATUS": "A"}, "commit-a", source_rank=1)["status"] == "SYNCED"
    page = provider.pages[page_id]
    page.content = page.content.replace("A", "operator edit")
    conflict = service.document("project-a", {"CURRENT_STATUS": "B"}, "commit-b", source_rank=2)
    assert conflict["status"] == "CONFLICT"
    assert service.document("project-a", {"CURRENT_STATUS": "old"}, "commit-old", source_rank=1)["status"] == "STALE_JOB_REJECTED"


def test_privacy_redaction_and_self_write_metadata():
    _, service = configured()
    bind(service)
    result = service.document("project-a", {"CURRENT_STATUS": "token=do-not-send password=hunter2"}, "commit-a", source_rank=1, documentation_run_id="run-a")
    assert result["status"] == "SYNCED"
    page = service.provider.pages[service.projects["project-a"].page_id]
    assert "do-not-send" not in page.content and "hunter2" not in page.content
    assert result["projection"]["self_write_id"].startswith("PRIME-WRITE/")


def test_knowledge_source_is_project_scoped_and_detach_retracts_and_reviews_memory():
    provider, service = configured()
    page = provider._new_page("parent", "Research", "operator research")
    service.configure("project-b", "notion-credential-ref")
    a = service.attach_source("project-a", "source-a", page.page_id)
    b = service.attach_source("project-b", "source-b", page.page_id)
    assert a["page_id"] == b["page_id"]
    service.admit_memory_reference("project-a", "memory-a", "source-a")
    detached = service.detach_source("project-a", "source-a")
    assert detached["retrieval"] == "RETRACTED"
    assert service.projects["project-a"].admitted_memory["memory-a"]["reconciliation_status"] == "REVIEW_REQUIRED"
    assert service.refresh_source("project-a", "source-a")["status"] == "DETACHED"
    assert service.refresh_source("project-a", "source-a")["retrieval"] == "RETRACTED"
    assert service.reconcile("project-a")["results"][-1]["retrieval"] == "RETRACTED"
    assert service.refresh_source("project-b", "source-b")["retrieval"] == "CURRENT"


def test_provider_failure_reconciliation_page_deletion_and_access_loss():
    provider, service = configured()
    bind(service)
    provider.fail_mode = "timeout"
    degraded = service.reconcile("project-a")
    assert degraded["status"] == "DEGRADED"
    provider.fail_mode = None
    provider.pages[service.projects["project-a"].page_id].archived = True
    missing = service.reconcile("project-a")
    assert missing["status"] == "PAGE_MISSING"


def test_binding_projection_and_source_metadata_survive_restart(tmp_path):
    provider = InMemoryNotionProvider()
    state_path = tmp_path / "notion-state.json"
    service = NotionLifecycleService(provider, state_path=state_path)
    service.configure("project-a", "notion-credential-ref")
    page_id = service.create_project_record("project-a", "parent", "A")["page_id"]
    service.document("project-a", {"CURRENT_STATUS": "persisted"}, "commit-a", source_rank=1)
    restarted = NotionLifecycleService(provider, state_path=state_path)
    assert restarted.health("project-a")["status"] == "BOUND"
    assert restarted.projects["project-a"].page_id == page_id
    assert restarted.projects["project-a"].latest_source_revision == "commit-a"


def test_history_rollover_is_idempotent_and_backup_excludes_raw_secret():
    _, service = configured()
    bind(service)
    first = service.rollover_history("project-a", "2026-08", "managed history", "a", "b")
    second = service.rollover_history("project-a", "2026-08", "managed history", "a", "b")
    assert second["idempotent"] is True
    backup = service.backup_metadata("project-a")
    assert backup["credential_state"] == "REPROVISION_REQUIRED"
    assert "token" not in json_safe(backup)


def json_safe(value):
    import json
    return json.dumps(value)
