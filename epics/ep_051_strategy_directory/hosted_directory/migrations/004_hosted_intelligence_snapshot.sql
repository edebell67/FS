-- Version history: 1.0.0 (2026-08-24) Atomically publish sanitized profiles and bounded return series with each directory snapshot.
BEGIN;
CREATE TABLE IF NOT EXISTS directory_intelligence_profile (
  snapshot_id text NOT NULL REFERENCES directory_snapshot(snapshot_id) ON DELETE CASCADE,
  strategy_id text NOT NULL,
  payload jsonb NOT NULL,
  PRIMARY KEY(snapshot_id,strategy_id)
);
CREATE TABLE IF NOT EXISTS directory_return_series (
  snapshot_id text NOT NULL REFERENCES directory_snapshot(snapshot_id) ON DELETE CASCADE,
  strategy_id text NOT NULL,
  observed_at timestamptz NOT NULL,
  trade_id text NOT NULL,
  payload jsonb NOT NULL,
  PRIMARY KEY(snapshot_id,strategy_id,observed_at,trade_id)
);
CREATE INDEX IF NOT EXISTS directory_return_series_lookup ON directory_return_series(snapshot_id,strategy_id,observed_at);
COMMIT;
