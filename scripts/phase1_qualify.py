from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.prime_core.config import Settings
from src.prime_core.db import connect, migrate, schema_version


def main() -> int:
    url = os.getenv("PRIME_PHASE1_DB_URL") or os.getenv("PRIME_DATABASE_URL")
    if not url:
        print("BLOCKED: PRIME_PHASE1_DB_URL or PRIME_DATABASE_URL is required")
        return 2
    settings = Settings(database_url=url)
    first = migrate(settings)
    second = migrate(settings)
    with connect(settings) as db:
        tables = {
            row["tablename"]
            for row in db.execute(
                "SELECT tablename FROM pg_tables WHERE schemaname='prime_core'"
            ).fetchall()
        }
    required = {"operators", "sessions", "projects", "source_references", "events", "jobs", "workflows", "audit_events", "notifications", "usage_records", "settings"}
    checks = [
        ("migration applies", "0001_core.sql" in first or not first),
        ("migration idempotence", second == []),
        ("schema version", schema_version(settings) in {"0001_core.sql", "0002_nodes.sql"}),
        ("canonical tables", required <= tables),
    ]
    failed = [name for name, passed in checks if not passed]
    for name, passed in checks:
        print(("PASS" if passed else "FAIL") + ": " + name)
    if failed:
        print("PHASE 1 QUALIFICATION: FAIL")
        return 1
    print("PHASE 1 QUALIFICATION: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
