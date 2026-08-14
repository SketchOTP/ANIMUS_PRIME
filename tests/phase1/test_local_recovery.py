from __future__ import annotations

from starlette.requests import Request

from apps.core import main


def request_from(client_host: str, credential: str | None = None) -> Request:
    headers = [] if credential is None else [(b"x-prime-local-recovery", credential.encode())]
    return Request({"type": "http", "method": "POST", "path": "/v1/auth/local-recovery", "headers": headers, "client": (client_host, 1)})


def test_local_recovery_route_rejects_non_loopback_callers():
    response = main.local_recover(main.LocalRecovery(new_password="a sufficiently long password"), request_from("10.0.0.4"))
    assert response.status_code == 403


def test_local_recovery_route_returns_one_time_rotations_without_new_identity(monkeypatch):
    class FakeService:
        def recover_local(self, credential: str, new_password: str) -> tuple[str, str]:
            assert credential == "platform-secret"
            assert new_password == "a sufficiently long password"
            return "replacement-recovery", "replacement-local"

    monkeypatch.setattr(main, "service", FakeService())
    request = request_from("127.0.0.1", "platform-secret")
    result = main.local_recover(main.LocalRecovery(new_password="a sufficiently long password"), request)
    assert result["recovery_credential"] == "replacement-recovery"
    assert result["local_recovery_credential"] == "replacement-local"
    assert "single" in result["warning"] or "once" in result["warning"]
