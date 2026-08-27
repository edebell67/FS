"""Fail-closed first-run migration gate for the shared Render PostgreSQL instance."""
from __future__ import annotations

import os
from pathlib import Path

import psycopg

MIGRATIONS = Path(__file__).resolve().parents[1] / "migrations"
STATE_TABLE = "ep051_migration_state"
KNOWN_EP051_TABLES = frozenset({
    "directory_current", "directory_intelligence_profile", "directory_return_series",
    "directory_snapshot", "directory_strategy", "intelligence_cohort_percentile",
    "intelligence_collection", "intelligence_collection_strategy", "intelligence_correlation",
    "intelligence_market_feature", "intelligence_period_metric", "intelligence_preference",
    "intelligence_privacy_audit", "intelligence_profile", "intelligence_recommendation_run",
    "intelligence_regime_label", "intelligence_return_series", "intelligence_saved_search",
    "intelligence_similarity", "intelligence_source_evidence", "intelligence_strategy_regime_profile",
    "intelligence_strategy_score", "intelligence_user_consent", "intelligence_user_history",
    "intelligence_watchlist",
})


def existing_ep051_tables(connection) -> set[str]:
    rows = connection.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema='public' "
        "AND (table_name LIKE 'directory_%' OR table_name LIKE 'intelligence_%') "
        "ORDER BY table_name"
    ).fetchall()
    return {str(row[0]) for row in rows}


def preflight_database(connection) -> bool:
    """Reject unknown shared-DB table names; return retention-role capability."""
    tables = existing_ep051_tables(connection)
    unexpected = tables - KNOWN_EP051_TABLES
    if unexpected:
        raise RuntimeError(f"EP051 migration blocked by existing table(s): {', '.join(sorted(unexpected))}")
    return connection.execute(
        "SELECT rolbypassrls FROM pg_roles WHERE rolname=current_user"
    ).fetchone()[0]


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
        can_create_retention_owner = preflight_database(connection)
        tables = existing_ep051_tables(connection)
        if tables and tables != KNOWN_EP051_TABLES:
            raise RuntimeError("EP051 migration blocked: incomplete prior migration state")
        if not tables:
            for path in sorted(MIGRATIONS.glob("00[1-6]_*.sql")):
                connection.execute(path.read_text(encoding="utf-8"))
        # Private routes are fail-closed unless an identity token is configured. Only a
        # BYPASSRLS operator may install their retention-owner function (migration 007).
        if can_create_retention_owner:
            connection.execute((MIGRATIONS / "007_retention_security_definer.sql").read_text(encoding="utf-8"))
        connection.execute(f"INSERT INTO {STATE_TABLE} (singleton) VALUES (true)")


if __name__ == "__main__":
    run()
