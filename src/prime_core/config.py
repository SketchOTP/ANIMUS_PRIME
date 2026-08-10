from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv(
        "PRIME_DATABASE_URL",
        "postgresql://prime:phase1-local-only@127.0.0.1:15432/prime",
    )
    session_ttl_seconds: int = int(os.getenv("PRIME_SESSION_TTL_SECONDS", "28800"))
    cookie_secure: bool = os.getenv("PRIME_COOKIE_SECURE", "0") == "1"
    allowed_origins: tuple[str, ...] = tuple(
        value.strip()
        for value in os.getenv(
            "PRIME_ALLOWED_ORIGINS",
            "http://127.0.0.1:8000,http://localhost:8000",
        ).split(",")
        if value.strip()
    )
    schema: str = "prime_core"

