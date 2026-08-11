from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence


@dataclass(frozen=True)
class RemoteAccessSettings:
    web_port: int = 8000
    web_host: str = "127.0.0.1"
    binary: str = "tailscale"
    timeout_seconds: int = 10
    state_path: Path | None = None


class TailscaleService:
    """Bounded, PRIME-owned Tailscale Serve lifecycle adapter.

    This class deliberately has no generic command escape hatch.  Tailnet
    membership is only network provenance; PRIME's normal session middleware
    remains responsible for operator authentication.
    """

    _allowed = {
        ("version",),
        ("status", "--json"),
        ("serve", "status", "--json"),
        ("funnel", "status", "--json"),
        ("serve", "--bg", "--https=443"),
        ("serve", "reset", "--yes"),
    }

    def __init__(self, settings: RemoteAccessSettings | None = None, runner: Callable[..., subprocess.CompletedProcess[str]] | None = None):
        self.settings = settings or RemoteAccessSettings()
        self._runner = runner or subprocess.run
        self._state: dict[str, object] = self._load_state()

    def _load_state(self) -> dict[str, object]:
        if not self.settings.state_path:
            return {"desired": "DISABLED"}
        try:
            value = json.loads(self.settings.state_path.read_text(encoding="utf-8"))
            return value if isinstance(value, dict) else {"desired": "DISABLED"}
        except (FileNotFoundError, OSError, json.JSONDecodeError):
            return {"desired": "DISABLED"}

    def _save_state(self) -> None:
        if not self.settings.state_path:
            return
        path = self.settings.state_path
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(json.dumps(self._state, sort_keys=True), encoding="utf-8")
        temporary.replace(path)

    def _run(self, args: Sequence[str]) -> subprocess.CompletedProcess[str]:
        command = tuple(args)
        if command not in self._allowed and not (command[:3] == ("serve", "--bg", "--https=443") and len(command) == 4):
            raise ValueError("unsupported Tailscale operation")
        return self._runner(
            [self.settings.binary, *args], check=False, capture_output=True,
            text=True, timeout=self.settings.timeout_seconds,
        )

    def _json(self, args: Sequence[str]) -> dict[str, object] | None:
        result = self._run(args)
        if result.returncode != 0:
            return None
        try:
            value = json.loads(result.stdout)
        except json.JSONDecodeError:
            return None
        return value if isinstance(value, dict) else None

    @staticmethod
    def _funnel_active(value: dict[str, object] | None) -> bool:
        if not value:
            return False
        return bool(value.get("Web") or value.get("web") or value.get("AllowFunnel"))

    @staticmethod
    def _serve_target(value: dict[str, object] | None) -> str | None:
        if not value:
            return None
        text = json.dumps(value, sort_keys=True)
        marker = "http://127.0.0.1:"
        start = text.find(marker)
        if start < 0:
            return None
        end = text.find('"', start)
        return text[start:end] if end > start else text[start:]

    def _local_bind(self) -> tuple[str, str | None]:
        if self.settings.web_host not in {"127.0.0.1", "localhost", "::1"}:
            return "LOCAL_BIND_UNSAFE", "PRIME Web must remain loopback-bound for Tailscale Serve"
        if not 1 <= self.settings.web_port <= 65535:
            return "LOCAL_BIND_UNSAFE", "invalid PRIME Web port"
        return "LOCAL_BIND_SAFE", None

    def status(self) -> dict[str, object]:
        bind_state, bind_error = self._local_bind()
        if shutil.which(self.settings.binary) is None:
            return {"status": "NOT_INSTALLED", "actual_state": "NOT_INSTALLED", "desired_state": self._state.get("desired", "DISABLED"), "serve": "DISABLED", "funnel": "UNKNOWN", "local_bind": bind_state, "error": bind_error}
        tailnet = self._json(["status", "--json"])
        if tailnet is None:
            return {"status": "ERROR", "actual_state": "ERROR", "desired_state": self._state.get("desired", "DISABLED"), "serve": "DISABLED", "funnel": "UNKNOWN", "local_bind": bind_state, "error": "Tailscale status unavailable"}
        backend = str(tailnet.get("BackendState", "")).upper().replace("_", "")
        serve = self._json(["serve", "status", "--json"])
        funnel = self._json(["funnel", "status", "--json"])
        funnel_active = self._funnel_active(funnel)
        serve_target = self._serve_target(serve)
        signed_out = backend in {"NOSTATE", "NEEDSLOGIN", "STOPPED"}
        connecting = backend in {"STARTING", "NONETWORK"}
        if signed_out:
            state = "SIGNED_OUT"
        elif connecting:
            state = "CONNECTING"
        elif funnel_active or bind_state != "LOCAL_BIND_SAFE":
            state = "DEGRADED"
        elif serve_target:
            state = "SERVE_ACTIVE"
        elif serve is not None:
            state = "SERVE_DISABLED"
        else:
            state = "DEGRADED"
        dns_name = (tailnet.get("Self") or {}).get("DNSName") if isinstance(tailnet.get("Self"), dict) else None
        return {
            "status": state, "actual_state": state, "desired_state": self._state.get("desired", "DISABLED"),
            "tailnet_dns_name": dns_name, "remote_url": f"https://{dns_name}/" if state == "SERVE_ACTIVE" and dns_name else None,
            "serve": "FUNNEL_EXPOSED" if funnel_active else ("CONFIGURED" if serve_target else "DISABLED"),
            "serve_target": serve_target, "funnel": "REFUSED" if funnel_active else "NOT_DETECTED",
            "private_only": not funnel_active and bind_state == "LOCAL_BIND_SAFE", "local_bind": bind_state, "error": bind_error,
        }

    def configure_serve(self) -> dict[str, object]:
        bind_state, bind_error = self._local_bind()
        if bind_state != "LOCAL_BIND_SAFE":
            raise PermissionError(bind_error or "unsafe PRIME Web bind")
        current = self.status()
        if current.get("status") in {"NOT_INSTALLED", "SIGNED_OUT", "CONNECTING", "ERROR"}:
            return {"status": current["status"], "actual_state": current["actual_state"], "error": current.get("error")}
        if current.get("funnel") == "REFUSED":
            raise PermissionError("REMOTE_ACCESS_UNSAFE: PRIME remote access requires private Tailscale Serve; public Funnel exposure is unsupported and must be removed")
        target = f"http://127.0.0.1:{self.settings.web_port}"
        existing = current.get("serve_target")
        if existing and existing != target:
            raise PermissionError("ambiguous existing Serve configuration; PRIME will not reset unrelated services")
        result = self._run(["serve", "--bg", "--https=443", target])
        if result.returncode != 0:
            return {"status": "DEGRADED", "actual_state": "DEGRADED", "error": result.stderr.strip() or "tailscale serve failed"}
        self._state.update({"desired": "ACTIVE", "owned_target": target})
        self._save_state()
        return {"status": "CONFIGURED", "actual_state": "SERVE_ACTIVE", "desired_state": "ACTIVE", "private_only": True, "output": result.stdout.strip()}

    def disable(self) -> dict[str, object]:
        current = self.status()
        owned = self._state.get("owned_target")
        if current.get("serve_target") and owned != current.get("serve_target"):
            return {"status": "DEGRADED", "actual_state": current.get("actual_state"), "error": "PRIME-owned Serve configuration is not identifiable; refusing unrelated reset"}
        result = self._run(["serve", "reset", "--yes"])
        if result.returncode == 0:
            self._state.update({"desired": "DISABLED", "owned_target": None})
            self._save_state()
        return {"status": "DISABLED" if result.returncode == 0 else "DEGRADED", "desired_state": self._state.get("desired"), "error": result.stderr.strip() or None}

    def reconcile(self) -> dict[str, object]:
        current = self.status()
        if self._state.get("desired") == "ACTIVE" and current.get("actual_state") != "SERVE_ACTIVE":
            current["status"] = "DEGRADED" if current.get("actual_state") not in {"NOT_INSTALLED", "SIGNED_OUT"} else current["actual_state"]
        return current
