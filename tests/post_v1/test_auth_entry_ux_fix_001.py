from __future__ import annotations

import re
from types import SimpleNamespace
from pathlib import Path

import pytest

from src.prime_core import service as service_module
from src.prime_core.service import CoreService


ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "apps" / "web" / "index.html"
MAIN = ROOT / "apps" / "core" / "main.py"


def _html() -> str:
    return WEB.read_text(encoding="utf-8")


def _section(source: str, section_id: str) -> str:
    match = re.search(rf'<section id="{re.escape(section_id)}".*?</section>', source, re.DOTALL)
    assert match is not None
    return match.group(0)


class _InitializationDb:
    def __init__(self, initialized: bool) -> None:
        self.initialized = initialized

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def execute(self, query: str):
        assert query == "SELECT 1 FROM prime_core.operators LIMIT 1"
        return self

    def fetchone(self):
        return {"?column?": 1} if self.initialized else None


@pytest.mark.parametrize("initialized", [True, False])
def test_initialization_state_uses_only_operator_existence(monkeypatch, initialized: bool) -> None:
    monkeypatch.setattr(service_module, "connect", lambda _settings: _InitializationDb(initialized))
    service = object.__new__(CoreService)
    service.settings = object()

    assert service.initialized() is initialized


def test_public_auth_state_is_minimal_and_does_not_require_session(monkeypatch) -> None:
    from apps.core import main

    monkeypatch.setattr(main, "service", SimpleNamespace(initialized=lambda: True))
    assert main.auth_state() == {"initialized": True}
    route = MAIN.read_text(encoding="utf-8").split('@app.get("/v1/auth/state")', 1)[1].split('@app.post("/v1/auth/bootstrap")', 1)[0]
    assert "require_session" not in route
    assert "operator" not in route.replace("operator-bootstrap", "")
    assert "project" not in route


def test_initialized_unauthenticated_routes_to_compact_sign_in() -> None:
    html = _html()
    assert "if (bootstrapState.initialized === true) renderEntryState('initialized')" in html
    assert "activateRoute('auth-entry')" in html
    assert "PRIME is online and ready." in _section(html, "auth-entry")


def test_uninitialized_unauthenticated_routes_to_first_run() -> None:
    html = _html()
    assert "else if (bootstrapState.initialized === false) renderEntryState('uninitialized')" in html
    assert "activateRoute('setup')" in html
    assert "Bring PRIME online" in _section(html, "setup")


def test_authenticated_state_enters_product_without_entry_surface() -> None:
    html = _html()
    assert "state.authenticated = true; state.initialized = true; document.body.dataset.entryMode='product'" in html
    assert "$('#auth-entry').hidden=true; $('#setup').hidden=true" in html


def test_invalid_or_expired_session_resolves_bootstrap_state_without_protected_payload() -> None:
    html = _html()
    refresh = html.split("async function refresh()", 1)[1].split("$('#refresh-state')", 1)[0]
    assert "await api('/v1/operator/state')" in refresh
    assert "await resolveProtectedEntry(error)" in refresh
    resolver = html.split("async function resolveProtectedEntry", 1)[1].split("function renderSetup", 1)[0]
    assert "await api('/v1/auth/state')" in resolver
    assert "/v1/operator/state" not in resolver


def test_trusted_host_is_primary_and_password_is_secondary() -> None:
    auth = _section(_html(), "auth-entry")
    assert auth.index('id="local-identity-sign-in-button"') < auth.index('id="login-form"')
    assert "Continue with trusted PRIME host" in auth
    assert "/v1/auth/local-identity/challenge" in _html()
    assert "/v1/auth/login" in _html()


def test_recovery_is_collapsed_progressive_disclosure() -> None:
    auth = _section(_html(), "auth-entry")
    assert '<details id="recovery-disclosure"' in auth
    assert "<summary>Recovery options</summary>" in auth
    assert '<form id="recovery-form">' in auth
    assert "recovery.open=false" in _html()


def test_initialized_sign_in_does_not_render_initialization_or_setup_controls() -> None:
    auth = _section(_html(), "auth-entry")
    for forbidden in (
        "Initialize new PRIME",
        "Bring PRIME online",
        "PostgreSQL",
        "Hindsight",
        "Notion",
        "Tailscale",
        "Node enrollment",
    ):
        assert forbidden not in auth
    assert "if (bootstrap) [...bootstrap.elements].forEach(control=>{ control.disabled=!uninitialized; })" in _html()


def test_clean_install_preserves_bootstrap_and_setup_checklist() -> None:
    setup = _section(_html(), "setup")
    assert '<form id="bootstrap-form">' in setup
    assert "Initialize new PRIME" in setup
    assert "PostgreSQL, Hindsight, and privacy policy" in setup
    assert "Enroll a Node and bind a repository" in setup
    assert "state.initialized !== false" in _html()


def test_unknown_initialization_state_fails_closed_without_bootstrap_action() -> None:
    html = _html()
    assert "renderEntryState('error'" in html
    assert "No protected data or initialization action is available." in html
    assert "control.disabled=!uninitialized" in html


def test_logout_refresh_and_restart_keep_existing_session_contract() -> None:
    html = _html()
    assert "await api('/v1/auth/logout', {method:'POST'})" in html
    assert "location.reload()" in html
    assert "fetch(path, { cache: 'no-store', credentials: 'same-origin'" in html
    assert "await api('/v1/operator/state')" in html
