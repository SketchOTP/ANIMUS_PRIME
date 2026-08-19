from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_windows_installer_uses_real_scm_wrapper_and_idempotent_repair() -> None:
    script = (ROOT / "packaging/node/install-node.ps1").read_text(encoding="utf-8")
    assert "windows-service.py" in script
    assert "PositionalBinding = $false" in script
    assert "sc.exe config" in script
    assert "Copy-Item -Path $source -Destination $appRoot" in script
    assert "PRIME_NODE_BIND_HOST" in script
    assert "PRIME_NODE_WINDOWS_SERVICE_NAME" in script
    assert "PRIME_NODE_BOOTSTRAP_PUBLIC_KEY_FILE" in script
    assert "PRIME_NODE_BOOTSTRAP_CREDENTIAL" not in script.split("$machineSettings =", 1)[1].split("}", 1)[0]
    assert '"*S-1-5-18:(F)"' in script
    assert '"*S-1-5-32-544:(F)"' in script


def test_windows_service_wrapper_loads_installed_app_and_handles_stop() -> None:
    wrapper = (ROOT / "packaging/node/windows-service.py").read_text(encoding="utf-8")
    assert 'Path(__file__).resolve().parent / "app"' in wrapper
    assert "StartServiceCtrlDispatcherW" in wrapper
    assert "RegisterServiceCtrlHandlerExW" in wrapper
    assert "SERVICE_CONTROL_STOP" in wrapper
    assert "_server.should_exit = True" in wrapper
    assert "asyncio.SelectorEventLoop()" in wrapper
    assert "_load_machine_settings()" in wrapper
    assert "Session Manager\\Environment" in wrapper
    assert "loop.run_until_complete(_server.serve())" in wrapper
    assert "settings.validate()" in wrapper
