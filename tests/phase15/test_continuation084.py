from pathlib import Path


ROOT = Path(__file__).parents[2]


def test_terminal_completion_is_exposed_as_the_existing_protected_lifecycle_action():
    web = (ROOT / "apps" / "web" / "index.html").read_text(encoding="utf-8")
    lifecycle = (ROOT / "src" / "prime_core" / "lifecycle_service.py").read_text(encoding="utf-8")

    assert 'data-workflow-action="REQUEST_COMPLETION"' in web
    assert 'id="bootstrap-authority"' in web
    assert "/authority/bootstrap" in web
    assert '"REQUEST_COMPLETION": "COMPLETED"' in lifecycle
    assert '"REQUEST_COMPLETION"' in lifecycle
