"""Create the bounded, explicitly marked Continuation-088 qualification appliances.

This helper only owns PRIME qualification containers under the authorized lab.
It never touches the canonical project database, canonical project records, or
unrelated containers. Runtime credentials remain in the existing Atlas env file
and are never printed.
"""
from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path("/home/sketch/ANIMUS_PRIME_V1_QUALIFICATION_LAB/088")
ENV_FILE = Path("/home/sketch/.config/animus-prime/core.env")
IMAGE = "animus-prime-core:continuation-086-warm-start-notion"


def run(*args: str, capture: bool = False) -> str:
    result = subprocess.run(args, check=True, text=True, capture_output=capture)
    return result.stdout.strip() if capture else ""


def env_value(name: str) -> str:
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        if line.startswith(f"{name}="):
            return line.split("=", 1)[1]
    raise RuntimeError(f"missing required runtime configuration: {name}")


def database_url(database: str) -> str:
    value = env_value("PRIME_DATABASE_URL")
    return value.rsplit("/", 1)[0] + "/" + database


def appliance(name: str, database: str, port: int) -> None:
    container = f"prime-qual-088-{name}"
    state = ROOT / name / "state"
    evidence = ROOT / name / "evidence"
    state.mkdir(parents=True, exist_ok=True)
    evidence.mkdir(parents=True, exist_ok=True)
    inspect = subprocess.run(
        ["docker", "inspect", "--type=container", container],
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if inspect.returncode == 0:
        raise RuntimeError(f"refusing to replace existing qualification container: {container}")
    run(
        "docker",
        "run",
        "--detach",
        "--name",
        container,
        "--network",
        "host",
        "--label",
        "animus.prime.qualification=V1_QUALIFICATION_FIXTURE",
        "--label",
        "animus.prime.continuation=088",
        "--env-file",
        str(ENV_FILE),
        "--env",
        f"PRIME_DATABASE_URL={database_url(database)}",
        "--env",
        f"PRIME_STATE_DIR=/var/lib/prime-qualification/{name}/state",
        "--env",
        f"PRIME_EVIDENCE_ROOT=/var/lib/prime-qualification/{name}/evidence",
        "--env",
        f"PRIME_NOTION_CREDENTIAL_STATE_PATH=/var/lib/prime-qualification/{name}/state/notion-credential-reference.json",
        "--env",
        "PRIME_COOKIE_SECURE=0",
        "--env",
        f"PRIME_ALLOWED_ORIGINS=http://127.0.0.1:{port},http://localhost:{port}",
        "--mount",
        f"type=bind,src={state},dst=/var/lib/prime-qualification/{name}/state",
        "--mount",
        f"type=bind,src={evidence},dst=/var/lib/prime-qualification/{name}/evidence",
        IMAGE,
        "uvicorn",
        "apps.core.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        str(port),
    )
    print(f"{container}: V1_QUALIFICATION_FIXTURE database={database} port={port}")


def main() -> None:
    if not ENV_FILE.is_file():
        raise SystemExit(f"missing secure Atlas env file: {ENV_FILE}")
    ROOT.mkdir(parents=True, exist_ok=True)
    appliance("a-clean", "prime088_a", 18100)
    appliance("b-restore", "prime088_b", 18200)


if __name__ == "__main__":
    main()
