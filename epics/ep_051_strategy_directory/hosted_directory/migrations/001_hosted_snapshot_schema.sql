-- Version history:
-- 2026-08-23 v1.0.0 Codex - Initial immutable snapshot schema and atomic promotion contract.

BEGIN;

CREATE TABLE IF NOT EXISTS directory_snapshot (
    snapshot_id varchar(128) PRIMARY KEY CHECK (snapshot_id ~ '^dna-[A-Za-z0-9:TZ+._-]+-[0-9a-f]{12}$'),
    schema_version varchar(32) NOT NULL,
    methodology_version varchar(64) NOT NULL,
    source_watermark timestamptz NOT NULL,
    generated_at timestamptz NOT NULL,
    item_count integer NOT NULL CHECK (item_count >= 0),
    sha256 char(64) NOT NULL CHECK (sha256 ~ '^[0-9a-f]{64}$'),
    status varchar(16) NOT NULL DEFAULT 'staged'
        CHECK (status IN ('staged', 'current', 'retained', 'rejected')),
    promoted_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (source_watermark, sha256),
    CHECK ((status = 'current' AND promoted_at IS NOT NULL) OR status <> 'current')
);

CREATE TABLE IF NOT EXISTS directory_strategy (
    snapshot_id varchar(128) NOT NULL REFERENCES directory_snapshot(snapshot_id) ON DELETE RESTRICT,
    strategy_id varchar(64) NOT NULL CHECK (strategy_id ~ '^DNA_[A-Za-z0-9]+$'),
    payload jsonb NOT NULL CHECK (payload->>'strategy_id' = strategy_id),
    PRIMARY KEY (snapshot_id, strategy_id)
);

CREATE TABLE IF NOT EXISTS directory_current (
    singleton boolean PRIMARY KEY DEFAULT true CHECK (singleton),
    snapshot_id varchar(128) NOT NULL UNIQUE REFERENCES directory_snapshot(snapshot_id) ON DELETE RESTRICT,
    changed_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_directory_strategy_snapshot_market
    ON directory_strategy(snapshot_id, (payload->>'market'));
CREATE INDEX IF NOT EXISTS idx_directory_strategy_snapshot_return
    ON directory_strategy(snapshot_id, ((payload->>'total_net_return')::numeric) DESC);
CREATE INDEX IF NOT EXISTS idx_directory_snapshot_watermark
    ON directory_snapshot(source_watermark DESC);

-- The application promotes a snapshot in one transaction by locking the
-- singleton row, superseding the previous snapshot, marking the new snapshot
-- current, and upserting this pointer. Immutable strategy rows remain available
-- for audit and rollback.

COMMIT;
