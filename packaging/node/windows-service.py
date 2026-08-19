from __future__ import annotations

import ctypes
import asyncio
import os
import sys
import traceback
from ctypes import wintypes
from pathlib import Path

if os.name == "nt":
    import winreg


SERVICE_WIN32_OWN_PROCESS = 0x00000010
SERVICE_START_PENDING = 0x00000002
SERVICE_STOP_PENDING = 0x00000003
SERVICE_RUNNING = 0x00000004
SERVICE_STOPPED = 0x00000001
SERVICE_ACCEPT_STOP = 0x00000001
SERVICE_ACCEPT_SHUTDOWN = 0x00000004
SERVICE_CONTROL_STOP = 0x00000001
SERVICE_CONTROL_SHUTDOWN = 0x00000005
NO_ERROR = 0


class ServiceStatus(ctypes.Structure):
    _fields_ = [
        ("service_type", wintypes.DWORD),
        ("current_state", wintypes.DWORD),
        ("controls_accepted", wintypes.DWORD),
        ("win32_exit_code", wintypes.DWORD),
        ("service_specific_exit_code", wintypes.DWORD),
        ("check_point", wintypes.DWORD),
        ("wait_hint", wintypes.DWORD),
    ]


ServiceMainFunction = ctypes.WINFUNCTYPE(None, wintypes.DWORD, ctypes.POINTER(wintypes.LPWSTR))
HandlerFunction = ctypes.WINFUNCTYPE(
    wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID
)


class ServiceTableEntry(ctypes.Structure):
    _fields_ = [("service_name", wintypes.LPWSTR), ("service_main", ServiceMainFunction)]


_MACHINE_SETTING_NAMES = (
    "PRIME_NODE_WINDOWS_SERVICE_NAME",
    "PRIME_NODE_ALLOWED_ROOTS",
    "PRIME_NODE_STATE_FILE",
    "PRIME_NODE_NAME",
    "PRIME_NODE_ID",
    "PRIME_NODE_BIND_HOST",
    "PRIME_NODE_PORT",
    "PRIME_NODE_TLS_CERT_FILE",
    "PRIME_NODE_TLS_KEY_FILE",
    "PRIME_NODE_TLS_CA_FILE",
    "PRIME_NODE_BOOTSTRAP_PUBLIC_KEY_FILE",
)


def _load_machine_settings() -> None:
    if os.name != "nt":
        return
    key_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
        for name in _MACHINE_SETTING_NAMES:
            try:
                value, _ = winreg.QueryValueEx(key, name)
            except FileNotFoundError:
                continue
            if isinstance(value, str) and value:
                os.environ[name] = value


_load_machine_settings()
_advapi32 = ctypes.WinDLL("advapi32", use_last_error=True) if os.name == "nt" else None
_service_name = os.getenv("PRIME_NODE_WINDOWS_SERVICE_NAME", "AnimusPrimeNode")
_status_handle: int | None = None
_server = None


def _set_status(state: int, *, exit_code: int = NO_ERROR, wait_hint: int = 0) -> None:
    if not _status_handle or _advapi32 is None:
        return
    accepted = SERVICE_ACCEPT_STOP | SERVICE_ACCEPT_SHUTDOWN if state == SERVICE_RUNNING else 0
    status = ServiceStatus(
        SERVICE_WIN32_OWN_PROCESS,
        state,
        accepted,
        exit_code,
        0,
        0,
        wait_hint,
    )
    if not _advapi32.SetServiceStatus(_status_handle, ctypes.byref(status)):
        raise ctypes.WinError(ctypes.get_last_error())


@HandlerFunction
def _control_handler(control: int, event_type: int, event_data, context) -> int:
    del event_type, event_data, context
    global _server
    if control in {SERVICE_CONTROL_STOP, SERVICE_CONTROL_SHUTDOWN}:
        _set_status(SERVICE_STOP_PENDING, wait_hint=20_000)
        if _server is not None:
            _server.should_exit = True
    return NO_ERROR


def _record_start_failure() -> None:
    log_dir = Path(__file__).resolve().parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    (log_dir / "service-start-error.log").write_text(traceback.format_exc(), encoding="utf-8")


@ServiceMainFunction
def _service_main(argc: int, argv) -> None:
    del argc, argv
    global _status_handle, _server
    assert _advapi32 is not None
    _status_handle = _advapi32.RegisterServiceCtrlHandlerExW(
        _service_name, _control_handler, None
    )
    if not _status_handle:
        return
    try:
        _set_status(SERVICE_START_PENDING, wait_hint=30_000)
        app_root = Path(__file__).resolve().parent / "app"
        sys.path.insert(0, str(app_root))
        import uvicorn

        from apps.node.main import app, settings

        settings.validate()
        config = uvicorn.Config(app, log_level="info", **settings.uvicorn_kwargs())
        _server = uvicorn.Server(config)
        _set_status(SERVICE_RUNNING)
        loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(_server.serve())
        finally:
            loop.close()
        _set_status(SERVICE_STOPPED)
    except BaseException:
        _record_start_failure()
        _set_status(SERVICE_STOPPED, exit_code=1)


def main() -> None:
    if os.name != "nt" or _advapi32 is None:
        raise SystemExit("The ANIMUS PRIME Windows service wrapper requires Windows")
    _advapi32.RegisterServiceCtrlHandlerExW.restype = wintypes.HANDLE
    _advapi32.RegisterServiceCtrlHandlerExW.argtypes = [
        wintypes.LPCWSTR,
        HandlerFunction,
        wintypes.LPVOID,
    ]
    _advapi32.SetServiceStatus.argtypes = [wintypes.HANDLE, ctypes.POINTER(ServiceStatus)]
    _advapi32.SetServiceStatus.restype = wintypes.BOOL
    _advapi32.StartServiceCtrlDispatcherW.argtypes = [ctypes.POINTER(ServiceTableEntry)]
    _advapi32.StartServiceCtrlDispatcherW.restype = wintypes.BOOL
    table = (ServiceTableEntry * 2)(
        ServiceTableEntry(_service_name, _service_main),
        ServiceTableEntry(None, ServiceMainFunction()),
    )
    if not _advapi32.StartServiceCtrlDispatcherW(table):
        raise ctypes.WinError(ctypes.get_last_error())


if __name__ == "__main__":
    main()
