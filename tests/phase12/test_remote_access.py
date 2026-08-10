from __future__ import annotations

import json
import subprocess

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
