from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_warm_start_has_explicit_project_scoped_preview_and_execute_contract():
    source = (ROOT / "apps/core/main.py").read_text(encoding="utf-8")
    service = (ROOT / "src/prime_core/warm_start_service.py").read_text(encoding="utf-8")
    web = (ROOT / "apps/web/index.html").read_text(encoding="utf-8")

    assert '"/v1/projects/{project_id}/warm-start/preview"' in source
    assert '"/v1/projects/{project_id}/warm-start"' in source
    assert "selected_only" in service
    assert "repository_bulk_ingestion" in service
    assert "git_history_ingestion" in service
    assert "notion_bulk_ingestion" in service
    assert "content_hash" in service
    assert "WARM_START_MEMORY_ADMISSION" in service
    assert 'id="warm-start-preview"' in web
    assert 'id="warm-start-run"' in web


def test_warm_start_authority_allowlist_excludes_unbounded_repository_context():
    source = (ROOT / "src/prime_core/warm_start_service.py").read_text(encoding="utf-8")
    assert "AUTHORITY_PATHS" in source
    assert "PROJECT_GOAL.md" in source
    assert "DIRECTIVES.md" in source
    assert "whole repository" not in source.lower()
