from __future__ import annotations

import os
from dataclasses import dataclass, field
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
    bind_host: str = field(default_factory=lambda: os.getenv("PRIME_NODE_BIND_HOST", "127.0.0.1"))
    port: int = field(default_factory=lambda: int(os.getenv("PRIME_NODE_PORT", "18001")))
    tls_cert_file: Path | None = field(default_factory=lambda: Path(os.environ["PRIME_NODE_TLS_CERT_FILE"]).resolve() if os.getenv("PRIME_NODE_TLS_CERT_FILE") else None)
    tls_key_file: Path | None = field(default_factory=lambda: Path(os.environ["PRIME_NODE_TLS_KEY_FILE"]).resolve() if os.getenv("PRIME_NODE_TLS_KEY_FILE") else None)
    tls_ca_file: Path | None = field(default_factory=lambda: Path(os.environ["PRIME_NODE_TLS_CA_FILE"]).resolve() if os.getenv("PRIME_NODE_TLS_CA_FILE") else None)
    allow_insecure_http: bool = field(default_factory=lambda: os.getenv("PRIME_NODE_ALLOW_INSECURE_HTTP", "0").lower() in {"1", "true", "yes"})

    def uvicorn_kwargs(self) -> dict[str, object]:
        tls_files = (self.tls_cert_file, self.tls_key_file, self.tls_ca_file)
        if any(tls_files) and not all(tls_files):
            raise ValueError("Node TLS requires certificate, key, and CA files together")
        if not all(tls_files) and not self.allow_insecure_http:
            raise ValueError("Node service mode requires TLS/mTLS; set PRIME_NODE_ALLOW_INSECURE_HTTP only for disposable local qualification")
        values: dict[str, object] = {"host": self.bind_host, "port": self.port}
        if all(tls_files):
            values.update(
                {
                    "ssl_certfile": str(self.tls_cert_file),
                    "ssl_keyfile": str(self.tls_key_file),
                    "ssl_ca_certs": str(self.tls_ca_file),
                    "ssl_cert_reqs": 2,
                }
            )
        return values
