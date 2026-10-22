-- workstreams/WF-101/migrations/001_strategy_registry.sql — PostgreSQL registry for immutable DNA definitions and source aliases.
--
-- VERSION HISTORY
-- v1.0.0 · 2026-08-23 · Initial version: creates canonical strategy, definition-lineage, alias, and immutability controls for WF-101.

CREATE SCHEMA IF NOT EXISTS dna_directory;

CREATE TABLE IF NOT EXISTS dna_directory.dna_strategy (
    strategy_id text PRIMARY KEY CHECK (strategy_id ~ '^DNA_[0-9]+$'),
    descriptive_name text,
    definition_hash char(64) NOT NULL,
    definition_version integer NOT NULL CHECK (definition_version > 0),
    parent_strategy_id text REFERENCES dna_directory.dna_strategy(strategy_id),
    market text NOT NULL DEFAULT 'FX',
    product_type text NOT NULL DEFAULT 'SPOT_FX',
    status text NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT','COLLECTING','ELIGIBLE','ACTIVE','PAUSED','RETIRED','QUARANTINED')),
    visibility text NOT NULL DEFAULT 'private' CHECK (visibility IN ('private','internal','public')),
    methodology_version text NOT NULL,
    generated_at timestamptz NOT NULL,
    eligible_at timestamptz,
    retired_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (definition_hash),
    UNIQUE (strategy_id, definition_version)
);

CREATE TABLE IF NOT EXISTS dna_directory.dna_strategy_definition (
    strategy_id text NOT NULL REFERENCES dna_directory.dna_strategy(strategy_id),
    definition_version integer NOT NULL,
    definition_hash char(64) NOT NULL,
    definition_json jsonb NOT NULL,
    supersedes_strategy_id text REFERENCES dna_directory.dna_strategy(strategy_id),
    recorded_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (strategy_id, definition_version),
    UNIQUE (definition_hash),
    CHECK (definition_hash = encode(digest(convert_to(definition_json::text, 'UTF8'), 'sha256'), 'hex'))
);

CREATE TABLE IF NOT EXISTS dna_directory.dna_strategy_source_alias (
    source_model text PRIMARY KEY,
    strategy_id text NOT NULL REFERENCES dna_directory.dna_strategy(strategy_id),
    first_seen_at timestamptz NOT NULL,
    last_seen_at timestamptz NOT NULL,
    CHECK (last_seen_at >= first_seen_at)
);

CREATE OR REPLACE FUNCTION dna_directory.prevent_definition_identity_mutation()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.strategy_id <> OLD.strategy_id
       OR NEW.definition_hash <> OLD.definition_hash
       OR NEW.definition_version <> OLD.definition_version
       OR NEW.parent_strategy_id IS DISTINCT FROM OLD.parent_strategy_id
       OR NEW.generated_at <> OLD.generated_at THEN
        RAISE EXCEPTION 'DNA strategy identity and definition fields are immutable; create a new strategy/version';
    END IF;
    NEW.updated_at := now();
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_dna_strategy_immutable_definition ON dna_directory.dna_strategy;
CREATE TRIGGER trg_dna_strategy_immutable_definition
BEFORE UPDATE ON dna_directory.dna_strategy
FOR EACH ROW EXECUTE FUNCTION dna_directory.prevent_definition_identity_mutation();

CREATE INDEX IF NOT EXISTS idx_dna_strategy_discovery
ON dna_directory.dna_strategy (visibility, status, market, updated_at DESC);

