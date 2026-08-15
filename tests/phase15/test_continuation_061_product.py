from pathlib import Path

ROOT = Path(__file__).parents[2]


def test_notifications_lifecycle_is_additive_and_user_visible():
    migration = (ROOT / "migrations" / "prime" / "0035_notifications_lifecycle.sql").read_text(encoding="utf-8")
    source = (ROOT / "src" / "prime_core" / "notification_service.py").read_text(encoding="utf-8")
    web = (ROOT / "apps" / "web" / "index.html").read_text(encoding="utf-8")
    main = (ROOT / "apps" / "core" / "main.py").read_text(encoding="utf-8")
    for field in ("category", "dedupe_key", "source_type", "source_ref", "first_seen_at", "last_seen_at", "dismissed_at", "metadata"):
        assert "ADD COLUMN IF NOT EXISTS " + field in migration
    assert "notifications_open_dedupe_idx" in migration
    assert "def sync(" in source
    assert "def dismiss(" in source
    assert 'id="notifications"' in web
    assert "Dismiss notification" in web
    assert '@app.get("/notifications")' in main
    assert '@app.post("/notifications/{notification_id}/dismiss")' in main


def test_alignment_is_derived_from_goal_items_and_has_stable_milestones():
    progress = (ROOT / "src" / "prime_core" / "progress_service.py").read_text(encoding="utf-8")
    main = (ROOT / "apps" / "core" / "main.py").read_text(encoding="utf-8")
    web = (ROOT / "apps" / "web" / "index.html").read_text(encoding="utf-8")
    assert "def alignment(" in progress
    assert "milestone_" in progress
    assert '"alignment": alignment_detail' in main
    assert "alignment_detail" in main
    assert "snapshotAlignment.milestones" in web


def test_backup_controls_are_real_and_guarded():
    web = (ROOT / "apps" / "web" / "index.html").read_text(encoding="utf-8")
    assert 'id="backup-form"' in web
    assert "Create verified backup" in web
    assert "Run restore preflight" in web
    assert "/v1/backups/preflight" in web
    assert "explicit confirmation" in web

def test_project_snapshot_preserves_progress_service_for_alignment():
    main = (ROOT / "apps" / "core" / "main.py").read_text(encoding="utf-8")
    assert "progress_row = db.execute" in main
    assert '"progress": dict(progress_row) if progress_row else None' in main
    assert "alignment_detail = progress.alignment(project_id)" in main
