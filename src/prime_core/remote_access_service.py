from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence
from urllib.parse import urlparse


@dataclass(frozen=True)
class RemoteAccessSettings:
    web_port: int = 8000
    web_host: str = "127.0.0.1"
    serve_port: int = 443
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
        configure = (
            "serve", "--bg", f"--https={self.settings.serve_port}",
            f"http://127.0.0.1:{self.settings.web_port}",
        )
        clear = ("serve", f"--https={self.settings.serve_port}", "off")
        if command not in self._allowed and command not in {configure, clear}:
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
    def _endpoint_port(endpoint: str) -> int | None:
        try:
            parsed = urlparse(endpoint if "://" in endpoint else f"https://{endpoint}")
            return parsed.port or 443
        except ValueError:
            return None

    @classmethod
    def _route_targets(cls, value: object) -> list[str]:
        """Extract only configured proxy/handler targets from Serve JSON."""
        targets: list[str] = []
        if isinstance(value, str):
            if value.startswith(("http://", "https://")):
                targets.append(value)
        elif isinstance(value, dict):
            for key, child in value.items():
                if key.lower() in {"proxy", "handler", "target"} and isinstance(child, str):
                    if child.startswith(("http://", "https://")):
                        targets.append(child)
                else:
                    targets.extend(cls._route_targets(child))
        elif isinstance(value, list):
            for child in value:
                targets.extend(cls._route_targets(child))
        return targets

    def _route_snapshot(
        self,
        serve: dict[str, object] | None,
        funnel: dict[str, object] | None,
        dns_name: str | None,
    ) -> dict[str, object]:
        web = serve.get("Web") if isinstance(serve, dict) else None
        if not isinstance(web, dict) and isinstance(funnel, dict):
            web = funnel.get("Web")
        allow = funnel.get("AllowFunnel") if isinstance(funnel, dict) else None
        if not isinstance(allow, dict) and isinstance(serve, dict):
            allow = serve.get("AllowFunnel")
        allow = allow if isinstance(allow, dict) else {}
        routes: list[dict[str, object]] = []
        if isinstance(web, dict):
            for endpoint, route in web.items():
                if not isinstance(endpoint, str):
                    continue
                routes.append({
                    "endpoint": endpoint,
                    "port": self._endpoint_port(endpoint),
                    "targets": self._route_targets(route),
                    "funnel": bool(allow.get(endpoint)),
                })
        dns_host = (urlparse(f"https://{dns_name}").hostname.rstrip(".") if dns_name and urlparse(f"https://{dns_name}").hostname else None)
        prime_routes = [
            route for route in routes
            if route["port"] == self.settings.serve_port
            and (
                dns_host is None
                or (urlparse(str(route["endpoint"] if "://" in str(route["endpoint"]) else f"https://{route['endpoint']}")).hostname or "").rstrip(".") == dns_host
            )
        ]
        unrelated_routes = [route for route in routes if route not in prime_routes]
        prime_targets = sorted({
            target
            for route in prime_routes
            for target in route["targets"]
            if isinstance(target, str)
        })
        unrelated_funnel = [
            route["endpoint"] for route in unrelated_routes if route["funnel"]
        ]
        prime_funnel = any(bool(route["funnel"]) for route in prime_routes)
        owned_target = self._state.get("owned_target")
        owned_endpoint = str(self._state.get("owned_endpoint", self.settings.serve_port))
        owned = (
            len(prime_targets) == 1
            and prime_targets[0] == owned_target
            and owned_endpoint == str(self.settings.serve_port)
        )
        if not prime_targets:
            ownership = "NONE"
            prime_state = "DISABLED"
        elif owned:
            ownership = "OWNED"
            prime_state = "CONFIGURED"
        elif len(prime_targets) == 1 and prime_targets[0] != f"http://127.0.0.1:{self.settings.web_port}":
            ownership = "UNKNOWN"
            prime_state = "CONFLICT"
        else:
            ownership = "UNKNOWN"
            prime_state = "UNKNOWN"
        return {
            "prime_targets": prime_targets,
            "prime_target": prime_targets[0] if len(prime_targets) == 1 else None,
            "prime_funnel": prime_funnel,
            "prime_state": prime_state,
            "ownership": ownership,
            "unrelated_serve": [route["endpoint"] for route in unrelated_routes],
            "unrelated_funnel": unrelated_funnel,
        }

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
        dns_name = (tailnet.get("Self") or {}).get("DNSName") if isinstance(tailnet.get("Self"), dict) else None
        snapshot = self._route_snapshot(serve, funnel, dns_name if isinstance(dns_name, str) else None)
        prime_funnel = bool(snapshot["prime_funnel"])
        serve_target = snapshot["prime_target"]
        signed_out = backend in {"NOSTATE", "NEEDSLOGIN", "STOPPED"}
        connecting = backend in {"STARTING", "NONETWORK"}
        if signed_out:
            state = "SIGNED_OUT"
        elif connecting:
            state = "CONNECTING"
        elif prime_funnel or bind_state != "LOCAL_BIND_SAFE" or snapshot["prime_state"] in {"UNKNOWN", "CONFLICT"}:
            state = "DEGRADED"
        elif serve_target and snapshot["ownership"] == "OWNED":
            state = "SERVE_ACTIVE"
        elif serve is not None:
            state = "SERVE_DISABLED"
        else:
            state = "DEGRADED"
        return {
            "status": state, "actual_state": state, "desired_state": self._state.get("desired", "DISABLED"),
            "tailnet_dns_name": dns_name, "remote_url": f"https://{dns_name}/" if state == "SERVE_ACTIVE" and dns_name else None,
            "serve": "FUNNEL_EXPOSED" if prime_funnel else ("CONFIGURED" if serve_target and snapshot["ownership"] == "OWNED" else snapshot["prime_state"]),
            "serve_target": serve_target, "funnel": "REFUSED" if prime_funnel else "NOT_DETECTED",
            "prime_serve": snapshot["prime_state"], "prime_funnel": "EXPOSED" if prime_funnel else "NOT_DETECTED",
            "route_ownership": snapshot["ownership"], "unrelated_serve": snapshot["unrelated_serve"],
            "unrelated_funnel": snapshot["unrelated_funnel"],
            "private_only": not prime_funnel and bind_state == "LOCAL_BIND_SAFE", "local_bind": bind_state, "error": bind_error,
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
        if existing:
            if current.get("route_ownership") == "OWNED" and existing == target:
                return {"status": "CONFIGURED", "actual_state": "SERVE_ACTIVE", "desired_state": "ACTIVE", "private_only": True, "output": "already configured"}
            raise PermissionError("ambiguous existing PRIME endpoint; ownership is not identifiable and PRIME will not overwrite it")
        result = self._run(["serve", "--bg", f"--https={self.settings.serve_port}", target])
        if result.returncode != 0:
            return {"status": "DEGRADED", "actual_state": "DEGRADED", "error": result.stderr.strip() or "tailscale serve failed"}
        self._state.update({"desired": "ACTIVE", "owned_target": target, "owned_endpoint": str(self.settings.serve_port)})
        self._save_state()
        return {"status": "CONFIGURED", "actual_state": "SERVE_ACTIVE", "desired_state": "ACTIVE", "private_only": True, "output": result.stdout.strip()}

    def disable(self) -> dict[str, object]:
        current = self.status()
        owned = self._state.get("owned_target")
        if not current.get("serve_target"):
            self._state.update({"desired": "DISABLED"})
            self._save_state()
            return {"status": "DISABLED", "actual_state": current.get("actual_state"), "desired_state": "DISABLED", "error": None}
        if current.get("route_ownership") != "OWNED" or owned != current.get("serve_target"):
            return {"status": "DEGRADED", "actual_state": current.get("actual_state"), "error": "PRIME-owned Serve configuration is not identifiable; refusing unrelated endpoint clear"}
        result = self._run(["serve", f"--https={self.settings.serve_port}", "off"])
        if result.returncode == 0:
            self._state.update({"desired": "DISABLED", "owned_target": None})
            self._save_state()
        return {"status": "DISABLED" if result.returncode == 0 else "DEGRADED", "desired_state": self._state.get("desired"), "error": result.stderr.strip() or None}

    def reconcile(self) -> dict[str, object]:
        current = self.status()
        if self._state.get("desired") == "ACTIVE" and current.get("actual_state") != "SERVE_ACTIVE":
            current["status"] = "DEGRADED" if current.get("actual_state") not in {"NOT_INSTALLED", "SIGNED_OUT"} else current["actual_state"]
        return current
