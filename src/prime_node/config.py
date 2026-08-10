from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class NodeSettings:
    bootstrap_credential: str = os.getenv("PRIME_NODE_BOOTSTRAP_CREDENTIAL", "phase2-bootstrap-change-me")
    state_file: Path = Path(os.getenv("PRIME_NODE_STATE_FILE", ".prime-node-state.json"))
    allowed_roots: tuple[Path, ...] = tuple(
        Path(item).resolve()
        for item in os.getenv("PRIME_NODE_ALLOWED_ROOTS", "").split(os.pathsep)
        if item
    )
    max_read_bytes: int = int(os.getenv("PRIME_NODE_MAX_READ_BYTES", str(5 * 1024 * 1024)))
    node_name: str = os.getenv("PRIME_NODE_NAME", "prime-node")
    protocol_version: str = os.getenv("PRIME_NODE_PROTOCOL_VERSION", "node-control-v1")
    capabilities: tuple[str, ...] = tuple(
        value.strip()
        for value in os.getenv(
            "PRIME_NODE_CAPABILITIES",
            "repository.inspect,files.read,git.read,health,heartbeat",
        ).split(",")
        if value.strip()
    )
