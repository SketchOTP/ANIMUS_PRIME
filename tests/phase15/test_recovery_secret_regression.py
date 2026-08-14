from pathlib import Path


WEB = Path(__file__).parents[2] / "apps" / "web" / "index.html"


def test_web_console_does_not_render_or_persist_recovery_secrets():
    source = WEB.read_text(encoding="utf-8")
    assert "result.recovery_credential" not in source
    assert "result.local_recovery_credential" not in source
    assert "localStorage.setItem('recovery" not in source
    assert "sessionStorage.setItem('recovery" not in source
    assert "localStorage.setItem('password" not in source
    assert "sessionStorage.setItem('password" not in source
