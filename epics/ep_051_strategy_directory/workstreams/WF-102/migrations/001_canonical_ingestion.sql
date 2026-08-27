-- workstreams/WF-102/migrations/001_canonical_ingestion.sql — Canonical closed/open trade storage, watermarks, quarantine, and run manifests.
--
-- VERSION HISTORY
-- v1.0.0 · 2026-08-23 · Initial version: separates closed analytics from open state and supports idempotent incremental ingestion.

CREATE SCHEMA IF NOT EXISTS dna_directory;

CREATE TABLE IF NOT EXISTS dna_directory.canonical_closed_trade (
    guid text PRIMARY KEY,
    strategy_id text NOT NULL REFERENCES dna_directory.dna_strategy(strategy_id),
    source_model text NOT NULL,
    signal text NOT NULL CHECK (signal IN ('BUY','SELL')),
    created_at timestamptz NOT NULL,
    exit_at timestamptz NOT NULL CHECK (exit_at >= created_at),
    net_return numeric(24,8) NOT NULL,
    outcome text NOT NULL CHECK (outcome IN ('winner','loser','breakeven')),
    close_type text,
    source_updated_at timestamptz NOT NULL,
    source_checksum char(64) NOT NULL,
    ingested_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS dna_directory.canonical_open_trade (
    guid text PRIMARY KEY,
    strategy_id text NOT NULL REFERENCES dna_directory.dna_strategy(strategy_id),
    source_model text NOT NULL,
    signal text NOT NULL CHECK (signal IN ('BUY','SELL')),
    created_at timestamptz NOT NULL,
    last_update timestamptz NOT NULL CHECK (last_update >= created_at),
    unrealized_net_return numeric(24,8),
    source_checksum char(64) NOT NULL,
    ingested_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS dna_directory.ingestion_watermark (
    source_name text PRIMARY KEY CHECK (source_name IN ('combined_trades_closed','combined_trades_open')),
    watermark_at timestamptz NOT NULL,
    stable_id text NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS dna_directory.ingestion_quarantine (
    quarantine_id bigserial PRIMARY KEY,
    source_name text NOT NULL,
    stable_id text,
    run_id uuid NOT NULL,
    reason_code text NOT NULL,
    raw_payload jsonb NOT NULL,
    replay_state text NOT NULL DEFAULT 'pending' CHECK (replay_state IN ('pending','replayed','discarded')),
    quarantined_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS dna_directory.ingestion_run (
    run_id uuid PRIMARY KEY,
    source_name text NOT NULL,
    started_at timestamptz NOT NULL,
    completed_at timestamptz,
    input_count integer NOT NULL DEFAULT 0,
    accepted_count integer NOT NULL DEFAULT 0,
    unchanged_count integer NOT NULL DEFAULT 0,
    quarantined_count integer NOT NULL DEFAULT 0,
    input_checksum char(64),
    status text NOT NULL CHECK (status IN ('running','passed','failed')),
    failure_reason text
);

CREATE OR REPLACE VIEW dna_directory.closed_trade_analytics_source AS
SELECT * FROM dna_directory.canonical_closed_trade;

CREATE OR REPLACE VIEW dna_directory.current_open_trade_source AS
SELECT * FROM dna_directory.canonical_open_trade;
