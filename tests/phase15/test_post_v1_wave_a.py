from __future__ import annotations

import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "apps" / "web" / "index.html"


class _IdentityParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key == "id" and value:
                self.ids.append(value)


def _html() -> str:
    return WEB.read_text(encoding="utf-8")


def test_wave_a_shell_and_home_contract() -> None:
    html = _html()

    for token in ("--canvas: #050505", "--cyan: #00f5ff", "--pink: #ff2a6d", "--radius: 10px"):
        assert token in html

    global_nav = re.search(r'<nav class="nav-group global-nav".*?</nav>', html, re.DOTALL)
    assert global_nav is not None
    labels = re.findall(r"</svg>([^<]+)</a>", global_nav.group(0))
    assert labels == ["Home", "Projects", "Attention", "Activity", "System"]

    for identity in (
        'id="selected-project"',
        'class="project-tabs"',
        'id="project-subnav"',
        'id="home-health-strip"',
        'id="home-attention-preview"',
        'id="home-resume"',
        'id="home-recent-projects"',
    ):
        assert identity in html


def test_wave_a_routes_are_single_surface_and_deep_link_safe() -> None:
    html = _html()

    assert ".workspace > section { display: none" in html
    assert "#project-workspace > .surface-grid > article { display: none" in html
    assert "'timelens':'time-lens', 'lifecycle':'project-settings'" in html
    assert "'diagnostics':'global-settings'" in html
    assert "const legacyWarmStart=document.querySelector('#workspace > #warm-start')" in html
    assert "if (!valid) { route='home'" in html
    assert "if (PROJECT_ROUTES.has(route) && !state.activeProjectId)" in html
    assert "history.replaceState(null,'','#home')" in html
    assert "window.addEventListener('hashchange',()=>activateRoute(currentRoute(),true))" in html


def test_wave_a_preserves_product_boundaries_and_accessibility() -> None:
    html = _html()

    for endpoint in (
        "/v1/operator/state",
        "/v1/projects/${encodeURIComponent(projectId)}/snapshot",
        "/v1/projects/${encodeURIComponent(projectId)}/context-export?format=json",
    ):
        assert endpoint in html

    assert "min-height: 44px" in html
    assert "@media (prefers-reduced-motion: reduce)" in html
    assert "@media (max-width: 340px)" in html
    assert 'aria-label="Open navigation"' in html
    assert 'aria-label="Refresh state"' in html
    assert 'aria-label="Sign out"' in html
    assert "summary.textContent=project.description" in html
    assert "project.name || project.project_id" in html
    assert "body.dataset.entryMode='auth'" in html
    assert "body.dataset.entryMode='product'" in html


def test_wave_a_html_ids_and_inline_javascript_are_valid() -> None:
    html = _html()
    parser = _IdentityParser()
    parser.feed(html)
    assert len(parser.ids) == len(set(parser.ids))

    match = re.search(r"<script>(.*)</script>", html, re.DOTALL)
    assert match is not None
    result = subprocess.run(
        ["node", "--check", "-"],
        input=match.group(1),
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
