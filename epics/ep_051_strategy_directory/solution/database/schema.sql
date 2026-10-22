-- EP051 canonical bootstrap schema. Version 1.0.0 (2026-08-23).
BEGIN;
CREATE SCHEMA IF NOT EXISTS ep051;
CREATE TABLE IF NOT EXISTS ep051.schema_migrations (
    migration_id text PRIMARY KEY,
    sha256 text NOT NULL,
    applied_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMIT;

-- Feature schemas are applied in the exact order declared by migrations/manifest.txt.
