from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from src.prime_core.remote_access_service import RemoteAccessSettings, TailscaleService


def fake_runner(outputs: dict[tuple[str, ...], tuple[int, str, str]]):
    def run(argv, **kwargs):
        key = tuple(argv[1:])
        code, stdout, stderr = outputs.get(key, (1, "", "missing fixture"))
        return subprocess.CompletedProcess(argv, code, stdout, stderr)

    return run


def test_serve_uses_fixed_private_loopback_command(monkeypatch):
    outputs = {
        ("status", "--json"): (0, json.dumps({"Self": {"DNSName": "prime.tail"}}), ""),
        ("serve", "status", "--json"): (0, "{}", ""),
        ("funnel", "status", "--json"): (0, "{}", ""),
        ("serve", "--bg", "--https=443", "http://127.0.0.1:18000"): (0, "ok", ""),
    }
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/tailscale")
    service = TailscaleService(RemoteAccessSettings(web_port=18000), fake_runner(outputs))
    result = service.configure_serve()
    assert result["status"] == "CONFIGURED"


def test_funnel_is_a_hard_refusal(monkeypatch):
    outputs = {
        ("status", "--json"): (0, json.dumps({"Self": {"DNSName": "prime.tail"}}), ""),
        ("serve", "status", "--json"): (0, "{}", ""),
        ("funnel", "status", "--json"): (0, json.dumps({"Web": {"https://public": {}}}), ""),
    }
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/tailscale")
    service = TailscaleService(runner=fake_runner(outputs))
    with pytest.raises(PermissionError):
        service.configure_serve()


def test_status_distinguishes_signed_out_and_serve_disabled(monkeypatch):
    outputs = {
        ("status", "--json"): (0, json.dumps({"BackendState": "NeedsLogin", "Self": {}}), ""),
        ("serve", "status", "--json"): (0, "{}", ""),
        ("funnel", "status", "--json"): (0, "{}", ""),
    }
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/tailscale")
    service = TailscaleService(runner=fake_runner(outputs))
    assert service.status()["actual_state"] == "SIGNED_OUT"


def test_public_bind_and_ambiguous_serve_fail_closed(monkeypatch):
    outputs = {
        ("status", "--json"): (0, json.dumps({"Self": {"DNSName": "prime.tail"}}), ""),
        ("serve", "status", "--json"): (0, json.dumps({"Web": {"https://prime.tail": {"handler": "http://127.0.0.1:9999"}}}), ""),
        ("funnel", "status", "--json"): (0, "{}", ""),
    }
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/tailscale")
    unsafe = TailscaleService(RemoteAccessSettings(web_host="0.0.0.0"), fake_runner(outputs))
    with pytest.raises(PermissionError):
        unsafe.configure_serve()
    ambiguous = TailscaleService(RemoteAccessSettings(web_port=18000), fake_runner(outputs))
    with pytest.raises(PermissionError):
        ambiguous.configure_serve()


def test_disable_refuses_unowned_serve_and_reconcile_reports_degraded(tmp_path: Path, monkeypatch):
    outputs = {
        ("status", "--json"): (0, json.dumps({"Self": {"DNSName": "prime.tail"}}), ""),
        ("serve", "status", "--json"): (0, json.dumps({"Web": {"handler": "http://127.0.0.1:18000"}}), ""),
        ("funnel", "status", "--json"): (0, "{}", ""),
    }
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/tailscale")
    service = TailscaleService(RemoteAccessSettings(web_port=18000, state_path=tmp_path / "remote.json"), fake_runner(outputs))
    assert service.disable()["status"] == "DEGRADED"
