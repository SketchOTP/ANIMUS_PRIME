from pathlib import Path

ROOT = Path(__file__).parents[2]


def test_continuation_059_safe_product_surfaces_are_data_backed():
    core = (ROOT / "apps" / "core" / "main.py").read_text(encoding="utf-8")
    web = (ROOT / "apps" / "web" / "index.html").read_text(encoding="utf-8")
    reliability = (ROOT / "src" / "prime_core" / "reliability_service.py").read_text(encoding="utf-8")

    assert '@app.get("/v1/projects/{project_id}/usage")' in core
    assert 'policies = usage_limits.snapshot(project_id)' in core
    assert '"limits": {"status": "KNOWN", "policies": policies}' in core
    assert 'id="usage-detail"' in web
    assert 'id="backup-detail"' in web
    assert 'id="project-metadata-form"' in web
    assert 'backup_status' in reliability
    assert 'No verified continuity backup is currently recorded.' in reliability


def test_continuation_059_mobile_navigation_has_no_desktop_min_width():
    web = (ROOT / "apps" / "web" / "index.html").read_text(encoding="utf-8")
    assert "@media (max-width: 560px) { .nav-group { display: block; min-width: 0;" in web
    assert "a:focus-visible" in web
