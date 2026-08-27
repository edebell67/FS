# Version history:
# 2026-08-23 v1.0.0 Codex - Infrastructure-free structural checks for PostgreSQL schema.

from pathlib import Path


MIGRATION = (
    Path(__file__).resolve().parents[1]
    / "migrations"
    / "001_hosted_snapshot_schema.sql"
)


def test_migration_supports_immutable_snapshots_and_atomic_pointer():
    sql = MIGRATION.read_text(encoding="utf-8").lower()
    assert "begin;" in sql and "commit;" in sql
    assert "create table if not exists directory_snapshot" in sql
    assert "create table if not exists directory_strategy" in sql
    assert "create table if not exists directory_current" in sql
    assert "payload jsonb not null" in sql
    assert "singleton boolean primary key" in sql
    assert "on delete restrict" in sql
    assert "source_watermark" in sql
    assert "sha256" in sql
    assert "combined_trades" not in sql  # hosted storage contains aggregates only
