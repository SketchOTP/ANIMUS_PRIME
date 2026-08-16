from pathlib import Path


def test_web_shell_is_accessible_and_non_caching():
    html = Path("apps/web/index.html").read_text(encoding="utf-8")
    assert '<html lang="en">' in html
    assert 'meta name="viewport"' in html
    assert 'Cache-Control" content="no-store"' in html
    assert 'aria-live="polite"' in html
    assert 'prefers-reduced-motion' in html
    assert 'href="#projects"' in html
    assert 'data.build?.build_commit' in html
    assert 'overflow-wrap: anywhere' in html
    for surface in ("setup", "nodes", "notion", "remote", "backup", "progress", "integrity", "ask", "search", "memory", "brain", "evidence", "timelens", "lifecycle"):
        assert f'id="{surface}"' in html
    assert 'id="time-lens-form"' in html
    assert 'id="time-lens-boundary"' in html
    assert 'id="time-lens-now"' in html
    assert "Authentication required" in html
    assert "Funnel/public exposure" in html
    assert 'notion-reconcile' in html
    assert 'notion-sync' in html
    assert 'notion-history' in html
    assert 'notion-attach-source' in html
    assert 'notion-detach-source' in html
    assert 'Detach this read-only source and retract it from current retrieval' in html
