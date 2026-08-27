-- workstreams/WF-401/migrations/001_regime_stats.sql — Versioned strategy-by-regime evidence snapshots.
--
-- VERSION HISTORY
-- v1.0.0 · 2026-08-23 · Initial version: persists regime performance, lift, uncertainty, sufficiency, and lineage.

CREATE TABLE IF NOT EXISTS dna_directory.dna_strategy_regime_stats (
 strategy_id text NOT NULL, regime_dimension text NOT NULL, regime_value text NOT NULL,
 definition_version text NOT NULL, methodology_version text NOT NULL,
 evidence_start timestamptz, evidence_end timestamptz, exposure_minutes numeric(28,4),
 trades integer NOT NULL, net_return numeric(28,8) NOT NULL, mean_return numeric(28,8),
 median_return numeric(28,8), win_rate numeric(12,10), profit_factor numeric(28,10),
 max_drawdown numeric(28,8), downside_deviation numeric(28,8),
 baseline_mean numeric(28,8), comparative_lift numeric(28,8),
 confidence_low numeric(28,8), confidence_high numeric(28,8),
 sufficiency text NOT NULL CHECK (sufficiency IN ('COLLECTING','INSUFFICIENT','SUFFICIENT')),
 source_watermark timestamptz NOT NULL, calculated_at timestamptz NOT NULL,
 PRIMARY KEY(strategy_id, regime_dimension, regime_value, definition_version, methodology_version, calculated_at)
);
