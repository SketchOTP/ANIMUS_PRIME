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


def route(endpoint: str, target: str, *, funnel: bool = False) -> dict[str, object]:
    return {
        "Web": {endpoint: {"Handlers": {"/": {"Proxy": target}}}},
        "AllowFunnel": {endpoint: True} if funnel else {},
    }


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
        ("funnel", "status", "--json"): (0, json.dumps(route("prime.tail", "http://127.0.0.1:8000", funnel=True)), ""),
    }
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/tailscale")
    service = TailscaleService(runner=fake_runner(outputs))
    with pytest.raises(PermissionError):
        service.configure_serve()


def test_no_routes_are_reported_as_prime_disabled(monkeypatch):
    outputs = {
        ("status", "--json"): (0, json.dumps({"Self": {"DNSName": "prime.tail"}}), ""),
        ("serve", "status", "--json"): (0, "{}", ""),
        ("funnel", "status", "--json"): (0, "{}", ""),
    }
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/tailscale")
    status = TailscaleService(runner=fake_runner(outputs)).status()
    assert status["prime_serve"] == "DISABLED"
    assert status["unrelated_serve"] == []
    assert status["unrelated_funnel"] == []


def test_prime_only_route_is_owned_when_persisted(tmp_path: Path, monkeypatch):
    outputs = {
        ("status", "--json"): (0, json.dumps({"Self": {"DNSName": "prime.tail"}}), ""),
        ("serve", "status", "--json"): (0, json.dumps(route("prime.tail", "http://127.0.0.1:8000")), ""),
        ("funnel", "status", "--json"): (0, json.dumps(route("prime.tail", "http://127.0.0.1:8000")), ""),
    }
    (tmp_path / "remote.json").write_text(json.dumps({"desired": "ACTIVE", "owned_target": "http://127.0.0.1:8000", "owned_endpoint": "443"}), encoding="utf-8")
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/tailscale")
    status = TailscaleService(RemoteAccessSettings(state_path=tmp_path / "remote.json"), fake_runner(outputs)).status()
    assert status["prime_serve"] == "CONFIGURED"
    assert status["route_ownership"] == "OWNED"


def test_unrelated_serve_and_prime_route_are_separated(tmp_path: Path, monkeypatch):
    outputs = {
        ("status", "--json"): (0, json.dumps({"Self": {"DNSName": "prime.tail"}}), ""),
        ("serve", "status", "--json"): (0, json.dumps({"Web": {
            "prime.tail:10000": {"Handlers": {"/": {"Proxy": "http://127.0.0.1:4117"}}},
            "prime.tail": {"Handlers": {"/": {"Proxy": "http://127.0.0.1:8000"}}},
        }}), ""),
        ("funnel", "status", "--json"): (0, json.dumps({"Web": {
            "prime.tail:10000": {"Handlers": {"/": {"Proxy": "http://127.0.0.1:4117"}}},
            "prime.tail": {"Handlers": {"/": {"Proxy": "http://127.0.0.1:8000"}}},
        }}), ""),
    }
    (tmp_path / "remote.json").write_text(json.dumps({"desired": "ACTIVE", "owned_target": "http://127.0.0.1:8000", "owned_endpoint": "443"}), encoding="utf-8")
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/tailscale")
    status = TailscaleService(RemoteAccessSettings(state_path=tmp_path / "remote.json"), fake_runner(outputs)).status()
    assert status["prime_serve"] == "CONFIGURED"
    assert status["unrelated_serve"] == ["prime.tail:10000"]


def test_unrelated_funnel_does_not_block_prime(tmp_path: Path, monkeypatch):
    serve = {"Web": {
        "prime.tail:10000": {"Handlers": {"/": {"Proxy": "http://127.0.0.1:4117"}}},
        "prime.tail": {"Handlers": {"/": {"Proxy": "http://127.0.0.1:8000"}}},
    }, "AllowFunnel": {"prime.tail:10000": True}}
    outputs = {
        ("status", "--json"): (0, json.dumps({"Self": {"DNSName": "prime.tail"}}), ""),
        ("serve", "status", "--json"): (0, json.dumps(serve), ""),
        ("funnel", "status", "--json"): (0, json.dumps(serve), ""),
    }
    (tmp_path / "remote.json").write_text(json.dumps({"desired": "ACTIVE", "owned_target": "http://127.0.0.1:8000", "owned_endpoint": "443"}), encoding="utf-8")
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/tailscale")
    status = TailscaleService(RemoteAccessSettings(state_path=tmp_path / "remote.json"), fake_runner(outputs)).status()
    assert status["funnel"] == "NOT_DETECTED"
    assert status["unrelated_funnel"] == ["prime.tail:10000"]


def test_prime_funnel_is_refused(monkeypatch):
    outputs = {
        ("status", "--json"): (0, json.dumps({"Self": {"DNSName": "prime.tail"}}), ""),
        ("serve", "status", "--json"): (0, json.dumps(route("prime.tail", "http://127.0.0.1:8000", funnel=True)), ""),
        ("funnel", "status", "--json"): (0, json.dumps(route("prime.tail", "http://127.0.0.1:8000", funnel=True)), ""),
    }
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/tailscale")
    with pytest.raises(PermissionError, match="public Funnel"):
        TailscaleService(runner=fake_runner(outputs)).configure_serve()


def test_conflicting_prime_endpoint_refuses_overwrite(monkeypatch):
    outputs = {
        ("status", "--json"): (0, json.dumps({"Self": {"DNSName": "prime.tail"}}), ""),
        ("serve", "status", "--json"): (0, json.dumps(route("prime.tail", "http://127.0.0.1:9000")), ""),
        ("funnel", "status", "--json"): (0, json.dumps(route("prime.tail", "http://127.0.0.1:9000")), ""),
    }
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/tailscale")
    with pytest.raises(PermissionError, match="overwrite"):
        TailscaleService(runner=fake_runner(outputs)).configure_serve()


def test_disable_clears_only_owned_prime_endpoint(tmp_path: Path, monkeypatch):
    calls: list[tuple[str, ...]] = []
    serve = {"Web": {
        "prime.tail:10000": {"Handlers": {"/": {"Proxy": "http://127.0.0.1:4117"}}},
        "prime.tail": {"Handlers": {"/": {"Proxy": "http://127.0.0.1:8000"}}},
    }}
    outputs = {
        ("status", "--json"): (0, json.dumps({"Self": {"DNSName": "prime.tail"}}), ""),
        ("serve", "status", "--json"): (0, json.dumps(serve), ""),
        ("funnel", "status", "--json"): (0, json.dumps(serve), ""),
        ("serve", "clear", "443"): (0, "cleared", ""),
    }
    def runner(argv, **kwargs):
        calls.append(tuple(argv[1:]))
        return fake_runner(outputs)(argv, **kwargs)
    (tmp_path / "remote.json").write_text(json.dumps({"desired": "ACTIVE", "owned_target": "http://127.0.0.1:8000", "owned_endpoint": "443"}), encoding="utf-8")
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/tailscale")
    result = TailscaleService(RemoteAccessSettings(state_path=tmp_path / "remote.json"), runner=runner).disable()
    assert result["status"] == "DISABLED"
    assert ("serve", "clear", "443") in calls
    assert not any(call[:2] == ("serve", "reset") for call in calls)


def test_unknown_prime_ownership_refuses_disable(monkeypatch):
    outputs = {
        ("status", "--json"): (0, json.dumps({"Self": {"DNSName": "prime.tail"}}), ""),
        ("serve", "status", "--json"): (0, json.dumps(route("prime.tail", "http://127.0.0.1:8000")), ""),
        ("funnel", "status", "--json"): (0, json.dumps(route("prime.tail", "http://127.0.0.1:8000")), ""),
    }
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/tailscale")
    result = TailscaleService(runner=fake_runner(outputs)).disable()
    assert result["status"] == "DEGRADED"
    assert "not identifiable" in result["error"]


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
        ("serve", "status", "--json"): (0, json.dumps({"Web": {"prime.tail": {"handler": "http://127.0.0.1:18000"}}}), ""),
        ("funnel", "status", "--json"): (0, "{}", ""),
    }
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/tailscale")
    service = TailscaleService(RemoteAccessSettings(web_port=18000, state_path=tmp_path / "remote.json"), fake_runner(outputs))
    assert service.disable()["status"] == "DEGRADED"
