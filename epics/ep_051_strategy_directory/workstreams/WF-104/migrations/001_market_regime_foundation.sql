-- workstreams/WF-104/migrations/001_market_regime_foundation.sql — Instrument, calendar, market-bar, and objective regime observation schema.
--
-- VERSION HISTORY
-- v1.0.0 · 2026-08-23 · Initial version: creates versioned leakage-resistant market and regime foundations.

CREATE TABLE IF NOT EXISTS dna_directory.instrument_master (
    instrument_id text PRIMARY KEY,
    market text NOT NULL,
    product_type text NOT NULL,
    base_currency char(3), quote_currency char(3),
    timezone text NOT NULL,
    calendar_id text NOT NULL,
    price_scale integer NOT NULL CHECK (price_scale BETWEEN 0 AND 12),
    active boolean NOT NULL DEFAULT true
);

CREATE TABLE IF NOT EXISTS dna_directory.market_bar (
    instrument_id text NOT NULL REFERENCES dna_directory.instrument_master(instrument_id),
    interval text NOT NULL,
    bucket_start timestamptz NOT NULL,
    bucket_end timestamptz NOT NULL,
    available_at timestamptz NOT NULL CHECK (available_at >= bucket_end),
    open numeric(24,10) NOT NULL, high numeric(24,10) NOT NULL,
    low numeric(24,10) NOT NULL, close numeric(24,10) NOT NULL,
    provider_version text NOT NULL,
    quality_state text NOT NULL CHECK (quality_state IN ('VALID','STALE','INVALID')),
    PRIMARY KEY (instrument_id, interval, bucket_start, provider_version),
    CHECK (high >= low AND high >= open AND high >= close AND low <= open AND low <= close)
);

CREATE TABLE IF NOT EXISTS dna_directory.market_regime_observation (
    instrument_id text NOT NULL REFERENCES dna_directory.instrument_master(instrument_id),
    interval_start timestamptz NOT NULL,
    interval_end timestamptz NOT NULL,
    available_at timestamptz NOT NULL,
    directional_state text NOT NULL CHECK (directional_state IN ('TREND_UP','TREND_DOWN','SIDEWAYS','UNKNOWN')),
    volatility_state text NOT NULL CHECK (volatility_state IN ('HIGH_VOLATILITY','NORMAL_VOLATILITY','LOW_VOLATILITY','UNKNOWN')),
    feature_values jsonb NOT NULL,
    thresholds jsonb NOT NULL,
    definition_version text NOT NULL,
    source_watermark timestamptz NOT NULL,
    quality_state text NOT NULL,
    confidence numeric(5,4),
    PRIMARY KEY (instrument_id, interval_start, definition_version),
    CHECK (available_at > interval_end AND source_watermark <= available_at)
);

