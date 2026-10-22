-- workstreams/WF-201/migrations/001_strategy_stats.sql — Versioned evidence-aware headline strategy snapshots.
--
-- VERSION HISTORY
-- v1.0.0 · 2026-08-23 · Initial version: defines monetary, outcome, risk, behavior, excursion and quality fields without unsupported percentages.

CREATE TABLE IF NOT EXISTS dna_directory.dna_strategy_stats (
    strategy_id text NOT NULL REFERENCES dna_directory.dna_strategy(strategy_id),
    methodology_version text NOT NULL,
    calculated_at timestamptz NOT NULL,
    evidence_start timestamptz, evidence_end timestamptz,
    source_watermark timestamptz NOT NULL,
    currency char(3) NOT NULL,
    total_trades integer NOT NULL,
    wins integer NOT NULL, losses integer NOT NULL, breakevens integer NOT NULL,
    total_net_return numeric(28,8) NOT NULL,
    mean_trade numeric(28,8), median_trade numeric(28,8), return_stddev numeric(28,8),
    gross_profit numeric(28,8) NOT NULL, gross_loss numeric(28,8) NOT NULL,
    win_rate numeric(12,10), profit_factor numeric(28,10), payoff_ratio numeric(28,10), expectancy numeric(28,8),
    max_drawdown_money numeric(28,8), max_drawdown_percent numeric(18,10),
    mean_holding_minutes numeric(28,8), median_holding_minutes numeric(28,8),
    mean_mfe numeric(28,8), mean_mae numeric(28,8),
    sample_sufficiency text NOT NULL, quality_state text NOT NULL,
    PRIMARY KEY (strategy_id, methodology_version, calculated_at),
    CHECK (total_trades = wins + losses + breakevens),
    CHECK (max_drawdown_percent IS NULL OR max_drawdown_percent <= 0)
);
