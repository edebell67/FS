"""Fail-closed first-run migration gate for the shared Render PostgreSQL instance."""
from __future__ import annotations

import os
from pathlib import Path

import psycopg

MIGRATIONS = Path(__file__).resolve().parents[1] / "migrations"
STATE_TABLE = "ep051_migration_state"


def preflight_database(connection) -> None:
    """Reject unsafe shared-DB conditions before any EP051 migration runs."""
    collisions = connection.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema='public' "
        "AND (table_name LIKE 'directory_%' OR table_name LIKE 'intelligence_%') "
        "ORDER BY table_name"
    ).fetchall()
    if collisions:
        names = ", ".join(str(row[0]) for row in collisions)
        raise RuntimeError(f"EP051 migration blocked by existing table(s): {names}")
    can_create_role = connection.execute(
        "SELECT rolcreaterole FROM pg_roles WHERE rolname=current_user"
    ).fetchone()[0]
    if not can_create_role:
        raise RuntimeError("EP051 migration blocked: database role lacks CREATEROLE")


def is_complete(connection) -> bool:
    connection.execute(
        f"CREATE TABLE IF NOT EXISTS {STATE_TABLE} "
        "(singleton boolean PRIMARY KEY DEFAULT true, completed_at timestamptz NOT NULL DEFAULT now())"
    )
    return connection.execute(f"SELECT EXISTS (SELECT 1 FROM {STATE_TABLE} WHERE singleton)").fetchone()[0]


def run() -> None:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required")
    with psycopg.connect(database_url, autocommit=True) as connection:
        if is_complete(connection):
            return
        preflight_database(connection)
        for path in sorted(MIGRATIONS.glob("0*.sql")):
            connection.execute(path.read_text(encoding="utf-8"))
        connection.execute(f"INSERT INTO {STATE_TABLE} (singleton) VALUES (true)")


if __name__ == "__main__":
    run()
