from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import psycopg
from psycopg.rows import dict_row

from .config import Settings

MIGRATION_DIR = Path(__file__).parents[2] / "migrations" / "prime"


def connect(settings: Settings) -> psycopg.Connection:
    return psycopg.connect(settings.database_url, row_factory=dict_row)


@contextmanager
def transaction(settings: Settings) -> Iterator[psycopg.Connection]:
    connection = connect(settings)
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def migrate(settings: Settings) -> list[str]:
    applied: list[str] = []
    with transaction(settings) as connection:
        connection.execute("CREATE SCHEMA IF NOT EXISTS prime_core")
        connection.execute(
            "CREATE TABLE IF NOT EXISTS prime_core.schema_migrations "
            "(version TEXT PRIMARY KEY, applied_at TIMESTAMPTZ NOT NULL DEFAULT now())"
        )
        for path in sorted(MIGRATION_DIR.glob("*.sql")):
            version = path.name
            exists = connection.execute(
                "SELECT 1 FROM prime_core.schema_migrations WHERE version = %s", (version,)
            ).fetchone()
            if exists:
                continue
            connection.execute(path.read_text(encoding="utf-8"))
            connection.execute(
                "INSERT INTO prime_core.schema_migrations(version) VALUES (%s)", (version,)
            )
            applied.append(version)
    return applied


def schema_version(settings: Settings) -> str:
    with connect(settings) as connection:
        row = connection.execute(
            "SELECT version FROM prime_core.schema_migrations ORDER BY version DESC LIMIT 1"
        ).fetchone()
        return row["version"] if row else "NONE"

