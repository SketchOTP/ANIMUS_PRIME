from pathlib import Path


def test_web_shell_is_accessible_and_non_caching():
    html = Path("apps/web/index.html").read_text(encoding="utf-8")
    assert '<html lang="en">' in html
    assert 'meta name="viewport"' in html
    assert 'Cache-Control" content="no-store"' in html
    assert 'aria-live="polite"' in html
    assert 'prefers-reduced-motion' in html
    assert 'href="#projects"' in html
