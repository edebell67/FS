-- workstreams/WF-202/migrations/001_period_stats.sql — Versioned daily, weekly, monthly, and rolling strategy statistics.
--
-- VERSION HISTORY
-- v1.0.0 · 2026-08-23 · Initial version: defines timezone-aware complete/incomplete period evidence.

CREATE TABLE IF NOT EXISTS dna_directory.dna_strategy_period_stats (
 strategy_id text NOT NULL, period_type text NOT NULL CHECK (period_type IN ('DAY','WEEK','MONTH','ROLLING')),
 period_start timestamptz NOT NULL, period_end timestamptz NOT NULL,
 methodology_version text NOT NULL, timezone text NOT NULL,
 trades integer NOT NULL, winners integer NOT NULL, losers integer NOT NULL, breakevens integer NOT NULL,
 net_return numeric(28,8) NOT NULL, mean_trade numeric(28,8), median_trade numeric(28,8),
 win_rate numeric(12,10), max_drawdown numeric(28,8), active boolean NOT NULL,
 completeness text NOT NULL CHECK (completeness IN ('COMPLETE','INCOMPLETE')),
 PRIMARY KEY(strategy_id, period_type, period_start, methodology_version)
);
