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
    first = migrate(settings)
    with connect(settings) as db:
        tables = {row["tablename"] for row in db.execute("SELECT tablename FROM pg_tables WHERE schemaname='prime_core'").fetchall()}
    checks = [("node migration", "0002_nodes.sql" in first or {"nodes", "repositories"} <= tables)]
    for name, passed in checks:
        print(("PASS" if passed else "FAIL") + ": " + name)
    if not all(passed for _, passed in checks):
        print("PHASE 2 QUALIFICATION: FAIL")
        return 1
    print("PHASE 2 QUALIFICATION: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
