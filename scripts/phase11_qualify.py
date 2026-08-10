from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from src.prime_core.config import Settings
from src.prime_core.db import connect, migrate


def main() -> int:
    url = os.getenv("PRIME_PHASE1_DB_URL") or os.getenv("PRIME_DATABASE_URL")
    if not url:
        print("BLOCKED: database URL required")
        return 2
    settings = Settings(database_url=url)
    applied = migrate(settings)
    with connect(settings) as db:
        tables = {row["tablename"] for row in db.execute("SELECT tablename FROM pg_tables WHERE schemaname='prime_core'").fetchall()}
    passed = "0011_evidence_time_lens.sql" in applied or {"evidence_records", "time_lens_checkpoints", "project_forks"} <= tables
    print(("PASS" if passed else "FAIL") + ": evidence/Time Lens/fork migration")
    print("PHASE 11 QUALIFICATION: " + ("PASS" if passed else "FAIL"))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
