from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone


class RedactedJsonFormatter(logging.Formatter):
    """Small structured formatter that never serializes request bodies or secrets."""

    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }, separators=(",", ":"))


def configure() -> None:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(RedactedJsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(logging.INFO)

