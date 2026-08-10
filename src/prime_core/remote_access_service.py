from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from typing import Callable, Sequence


@dataclass(frozen=True)
class RemoteAccessSettings:
    web_port: int = 8000
    binary: str = "tailscale"
    timeout_seconds: int = 10


class TailscaleService:
    """Fixed-command Tailscale Serve controller.

    The browser/model supplies no command text. All invocations are assembled
    here as argv lists, and Funnel is checked before Serve is configured.
    """

    def __init__(self, settings: RemoteAccessSettings | None = None, runner: Callable[..., subprocess.CompletedProcess[str]] | None = None):
        self.settings = settings or RemoteAccessSettings()
        self._runner = runner or subprocess.run

    def _run(self, args: Sequence[str]) -> subprocess.CompletedProcess[str]:
        return self._runner(
            [self.settings.binary, *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=self.settings.timeout_seconds,
        )

    def status(self) -> dict[str, object]:
        if shutil.which(self.settings.binary) is None:
            return {"status": "NOT_INSTALLED", "serve": "DISABLED", "funnel": "UNKNOWN"}
        tailnet = self._json(["status", "--json"])
        serve = self._json(["serve", "status", "--json"])
        funnel = self._json(["funnel", "status", "--json"])
        funnel_active = bool(funnel and funnel.get("Web", funnel.get("web")))
        dns_name = tailnet.get("Self", {}).get("DNSName") if tailnet else None
        return {
            "status": "ONLINE" if tailnet else "DEGRADED",
            "tailnet_dns_name": dns_name,
            "serve": "FUNNEL_EXPOSED" if funnel_active else ("CONFIGURED" if serve else "DISABLED"),
            "funnel": "REFUSED" if funnel_active else "NOT_DETECTED",
            "private_only": not funnel_active,
        }

    def configure_serve(self) -> dict[str, object]:
        current = self.status()
        if current.get("funnel") == "REFUSED":
            raise PermissionError("refusing to configure PRIME while Tailscale Funnel is exposed")
        result = self._run(["serve", "--bg", "--https=443", f"http://127.0.0.1:{self.settings.web_port}"])
        if result.returncode != 0:
            return {"status": "DEGRADED", "error": result.stderr.strip() or "tailscale serve failed"}
        return {"status": "CONFIGURED", "private_only": True, "output": result.stdout.strip()}

    def disable(self) -> dict[str, object]:
        result = self._run(["serve", "reset", "--yes"])
        return {"status": "DISABLED" if result.returncode == 0 else "DEGRADED", "error": result.stderr.strip() or None}

    def _json(self, args: Sequence[str]) -> dict[str, object]:
        result = self._run(args)
        if result.returncode != 0:
            return {}
        try:
            value = json.loads(result.stdout)
        except json.JSONDecodeError:
            return {}
        return value if isinstance(value, dict) else {}
