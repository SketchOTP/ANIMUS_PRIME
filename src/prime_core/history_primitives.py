from __future__ import annotations

import json
import uuid
from datetime import datetime
from typing import Any


def reconstruction_status(statuses: dict[str, str]) -> str:
    """Combine per-source historical coverage without inventing missing state."""
    values = list(statuses.values())
    if not values or all(value == "UNAVAILABLE" for value in values):
        return "UNAVAILABLE"
    if all(value == "EXACT" for value in values):
        return "EXACT"
    return "PARTIAL"


def record_historical_snapshot(db: Any, project_id: str, artifact_type: str, artifact_id: str,
                              source_revision: str | None, snapshot: dict[str, Any],
                              observed_at: datetime, content_hash: str | None = None,
                              availability_status: str = "EXACT") -> None:
    """Write-once historical input used by Time Lens reconstruction."""
    db.execute(
        "INSERT INTO prime_core.historical_revisions(historical_revision_id,project_id,artifact_type,artifact_id,source_revision,content_hash,snapshot,availability_status,observed_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
        (f"hist_{uuid.uuid4().hex}", project_id, artifact_type, artifact_id, source_revision, content_hash, json.dumps(snapshot), availability_status, observed_at),
    )
