-- workstreams/WF-403/relationship_schema.sql — Canonical pairwise relationship evidence.
-- VERSION HISTORY
-- v1.0.0 · 2026-08-23 · Initial version: stores correlation, downside, loss/drawdown overlap, stability and quality.
CREATE TABLE IF NOT EXISTS dna_directory.dna_strategy_relationship (
 strategy_id_a text NOT NULL, strategy_id_b text NOT NULL, window_start date NOT NULL, window_end date NOT NULL,
 frequency text NOT NULL, alignment_method text NOT NULL, methodology_version text NOT NULL,
 return_correlation numeric(12,10), downside_correlation numeric(12,10), joint_loss_ratio numeric(12,10),
 drawdown_overlap_ratio numeric(12,10), joint_drawdown_severity numeric(28,8), stability_score numeric(12,10),
 sample_count integer NOT NULL, quality_state text NOT NULL, calculated_at timestamptz NOT NULL,
 PRIMARY KEY(strategy_id_a,strategy_id_b,window_start,window_end,methodology_version), CHECK(strategy_id_a<strategy_id_b)
);
