from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv(
        "PRIME_DATABASE_URL",
        "postgresql://prime:phase1-local-only@127.0.0.1:15432/prime",
    )
    session_ttl_seconds: int = int(os.getenv("PRIME_SESSION_TTL_SECONDS", "28800"))
    cookie_secure: bool = os.getenv("PRIME_COOKIE_SECURE", "0") == "1"
    hindsight_base_url: str = field(default_factory=lambda: os.getenv("PRIME_HINDSIGHT_BASE_URL", "http://127.0.0.1:8888").rstrip("/"))
    hindsight_timeout_seconds: float = field(default_factory=lambda: float(os.getenv("PRIME_HINDSIGHT_TIMEOUT_SECONDS", "30")))
    allowed_origins: tuple[str, ...] = tuple(
        value.strip()
        for value in os.getenv(
            "PRIME_ALLOWED_ORIGINS",
            "http://127.0.0.1:8000,http://localhost:8000",
        ).split(",")
        if value.strip()
    )
    schema: str = "prime_core"
    notion_credential_state_path: str = os.getenv("PRIME_NOTION_CREDENTIAL_STATE_PATH", "var/notion-credential-reference.json")
    notion_granted_page_id: str = os.getenv("PRIME_NOTION_GRANTED_PAGE_ID", "3b3833cb-27ff-8039-bf9e-f4f731df0633")