-- Turning-Point Pattern Database Schema V1
-- Date: 2026-05-02
-- Version: V20260502_1505

-- Core Tables
CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    product_code TEXT NOT NULL UNIQUE,
    product_type TEXT,
    quote_currency TEXT,
    base_currency TEXT,
    pip_size NUMERIC(12, 8) NOT NULL DEFAULT 0.0001,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS frequency_snapshots (
    snapshot_id BIGSERIAL PRIMARY KEY,
    product_id INT NOT NULL REFERENCES products(product_id),
    snapshot_time TIMESTAMP NOT NULL,
    window_start_time TIMESTAMP,
    window_end_time TIMESTAMP,
    source_run_id TEXT,
    source_name TEXT,
    source_timestamp TIMESTAMP,
    market_mode TEXT,
    bucket_label TEXT,
    quote_count INT NOT NULL DEFAULT 0,
    window_seconds INT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    UNIQUE(product_id, snapshot_time)
);

ALTER TABLE frequency_snapshots
    ADD COLUMN IF NOT EXISTS window_start_time TIMESTAMP,
    ADD COLUMN IF NOT EXISTS window_end_time TIMESTAMP,
    ADD COLUMN IF NOT EXISTS source_name TEXT,
    ADD COLUMN IF NOT EXISTS source_timestamp TIMESTAMP,
    ADD COLUMN IF NOT EXISTS market_mode TEXT,
    ADD COLUMN IF NOT EXISTS bucket_label TEXT,
    ADD COLUMN IF NOT EXISTS quote_count INT NOT NULL DEFAULT 0;

UPDATE frequency_snapshots
SET
    window_start_time = COALESCE(window_start_time, snapshot_time),
    window_end_time = COALESCE(window_end_time, snapshot_time + make_interval(secs => COALESCE(window_seconds, 0))),
    source_name = COALESCE(source_name, 'legacy'),
    source_timestamp = COALESCE(source_timestamp, snapshot_time),
    market_mode = COALESCE(market_mode, 'SIM'),
    bucket_label = COALESCE(bucket_label, TO_CHAR(snapshot_time, 'YYYY-MM-DD HH24:MI')),
    quote_count = COALESCE(quote_count, 0)
WHERE
    window_start_time IS NULL
    OR window_end_time IS NULL
    OR source_name IS NULL
    OR source_timestamp IS NULL
    OR market_mode IS NULL
    OR bucket_label IS NULL;

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'frequency_snapshots_product_id_snapshot_time_key'
    ) THEN
        ALTER TABLE frequency_snapshots
            DROP CONSTRAINT frequency_snapshots_product_id_snapshot_time_key;
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'frequency_snapshots_product_window_key'
    ) THEN
        ALTER TABLE frequency_snapshots
            ADD CONSTRAINT frequency_snapshots_product_window_key
            UNIQUE (product_id, window_start_time, window_seconds);
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_frequency_snapshots_window_start
    ON frequency_snapshots(window_start_time);
CREATE INDEX IF NOT EXISTS idx_frequency_snapshots_bucket_label
    ON frequency_snapshots(bucket_label);

CREATE TABLE IF NOT EXISTS frequency_levels (
    level_id BIGSERIAL PRIMARY KEY,
    snapshot_id BIGINT NOT NULL REFERENCES frequency_snapshots(snapshot_id) ON DELETE CASCADE,
    side TEXT NOT NULL CHECK (side IN ('BID', 'ASK')),
    price NUMERIC(18, 8) NOT NULL,
    frequency_count INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_frequency_levels_snapshot_side ON frequency_levels(snapshot_id, side);
CREATE INDEX IF NOT EXISTS idx_frequency_levels_price ON frequency_levels(price);

-- Turning-Point Storage
CREATE TABLE IF NOT EXISTS turning_points (
    turn_id BIGSERIAL PRIMARY KEY,
    product_id INT NOT NULL REFERENCES products(product_id),
    turn_time TIMESTAMP NOT NULL,
    turn_type TEXT NOT NULL CHECK (turn_type IN ('TOP', 'BOTTOM')),
    turn_price NUMERIC(18, 8) NOT NULL,

    confirmation_method TEXT,
    confirmation_delay_snapshots INT,
    confirmation_delay_minutes INT,

    pre_window_snapshots INT NOT NULL DEFAULT 3,
    post_window_snapshots INT NOT NULL DEFAULT 3,

    move_into_turn_pips NUMERIC(12, 4),
    confirmation_move_pips NUMERIC(12, 4),
    local_window_range_pips NUMERIC(12, 4),

    outcome_5m_pips NUMERIC(12, 4),
    outcome_10m_pips NUMERIC(12, 4),
    outcome_15m_pips NUMERIC(12, 4),
    outcome_30m_pips NUMERIC(12, 4),

    max_favourable_10m_pips NUMERIC(12, 4),
    max_adverse_10m_pips NUMERIC(12, 4),
    is_normalized BOOLEAN NOT NULL DEFAULT FALSE,
    has_features BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    UNIQUE(product_id, turn_time, turn_type)
);

ALTER TABLE turning_points
    ADD COLUMN IF NOT EXISTS move_into_turn_pips NUMERIC(12, 4),
    ADD COLUMN IF NOT EXISTS confirmation_move_pips NUMERIC(12, 4),
    ADD COLUMN IF NOT EXISTS local_window_range_pips NUMERIC(12, 4),
    ADD COLUMN IF NOT EXISTS is_normalized BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS has_features BOOLEAN NOT NULL DEFAULT FALSE;

CREATE TABLE IF NOT EXISTS turning_point_windows (
    window_id BIGSERIAL PRIMARY KEY,
    turn_id BIGINT NOT NULL REFERENCES turning_points(turn_id) ON DELETE CASCADE,
    snapshot_id BIGINT NOT NULL REFERENCES frequency_snapshots(snapshot_id),
    relative_time_index INT NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    UNIQUE(turn_id, snapshot_id)
);

-- Normalised Pattern Storage
CREATE TABLE IF NOT EXISTS normalised_pattern_levels (
    pattern_level_id BIGSERIAL PRIMARY KEY,
    turn_id BIGINT NOT NULL REFERENCES turning_points(turn_id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES products(product_id),
    turn_type TEXT NOT NULL CHECK (turn_type IN ('TOP', 'BOTTOM')),

    relative_time_index INT NOT NULL,
    side TEXT NOT NULL CHECK (side IN ('BID', 'ASK')),

    relative_pips INT NOT NULL,
    raw_price NUMERIC(18, 8) NOT NULL,
    frequency_count INT NOT NULL,

    normalised_frequency NUMERIC(12, 8),
    zscore_frequency NUMERIC(12, 8),

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_normalised_pattern_lookup ON normalised_pattern_levels(turn_type, relative_time_index, side, relative_pips);
CREATE INDEX IF NOT EXISTS idx_normalised_pattern_turn ON normalised_pattern_levels(turn_id);

-- Feature Vector Storage
CREATE TABLE IF NOT EXISTS pattern_features (
    feature_id BIGSERIAL PRIMARY KEY,
    turn_id BIGINT NOT NULL REFERENCES turning_points(turn_id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES products(product_id),
    turn_type TEXT NOT NULL CHECK (turn_type IN ('TOP', 'BOTTOM')),

    peak_frequency INT,
    peak_relative_pips INT,

    total_frequency INT,
    total_frequency_above_turn INT,
    total_frequency_below_turn INT,
    above_below_ratio NUMERIC(18, 8),

    cluster_width_pips INT,
    cluster_skew NUMERIC(18, 8),

    magnet_relative_pips_t_minus_3 INT,
    magnet_relative_pips_t_minus_2 INT,
    magnet_relative_pips_t_minus_1 INT,
    magnet_relative_pips_t INT,
    magnet_relative_pips_t_plus_1 INT,
    magnet_relative_pips_t_plus_2 INT,
    magnet_relative_pips_t_plus_3 INT,

    magnet_shift_pre_turn_pips NUMERIC(12, 4),
    magnet_shift_post_turn_pips NUMERIC(12, 4),

    failed_probe_pips INT,
    failed_probe_frequency INT,

    prior_zone_vanish_score NUMERIC(12, 8),
    rebuild_score NUMERIC(12, 8),
    reversal_strength_score NUMERIC(12, 8),

    thin_snapshot_score NUMERIC(12, 8),
    pattern_quality_score NUMERIC(12, 8),

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pattern_vectors (
    vector_id BIGSERIAL PRIMARY KEY,
    turn_id BIGINT NOT NULL REFERENCES turning_points(turn_id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES products(product_id),
    turn_type TEXT NOT NULL CHECK (turn_type IN ('TOP', 'BOTTOM')),

    vector_model_version TEXT NOT NULL,
    vector_dimensions INT NOT NULL,
    feature_vector float8[],

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Live Pattern Storage
CREATE TABLE IF NOT EXISTS live_pattern_windows (
    live_pattern_id BIGSERIAL PRIMARY KEY,
    product_id INT NOT NULL REFERENCES products(product_id),
    latest_snapshot_time TIMESTAMP NOT NULL,

    candidate_type TEXT CHECK (candidate_type IN ('TOP', 'BOTTOM', 'UNKNOWN')),
    candidate_turn_price NUMERIC(18, 8),

    pre_window_snapshots INT NOT NULL,
    post_window_snapshots INT DEFAULT 0,

    current_state TEXT,
    direction_bias TEXT CHECK (direction_bias IN ('UP', 'DOWN', 'NEUTRAL', 'UNCLEAR')),
    bottom_similarity NUMERIC(12, 8),
    top_similarity NUMERIC(12, 8),
    nearest_match_count INT,
    historical_next_5m_bias_rate NUMERIC(12, 8),
    historical_next_10m_bias_rate NUMERIC(12, 8),
    historical_avg_10m_move_pips NUMERIC(12, 4),
    confidence_label TEXT,
    summary TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

ALTER TABLE live_pattern_windows
    ADD COLUMN IF NOT EXISTS bottom_similarity NUMERIC(12, 8),
    ADD COLUMN IF NOT EXISTS top_similarity NUMERIC(12, 8),
    ADD COLUMN IF NOT EXISTS nearest_match_count INT,
    ADD COLUMN IF NOT EXISTS historical_next_5m_bias_rate NUMERIC(12, 8),
    ADD COLUMN IF NOT EXISTS historical_next_10m_bias_rate NUMERIC(12, 8),
    ADD COLUMN IF NOT EXISTS historical_avg_10m_move_pips NUMERIC(12, 4),
    ADD COLUMN IF NOT EXISTS confidence_label TEXT,
    ADD COLUMN IF NOT EXISTS summary TEXT;

CREATE TABLE IF NOT EXISTS live_pattern_vectors (
    live_vector_id BIGSERIAL PRIMARY KEY,
    live_pattern_id BIGINT NOT NULL REFERENCES live_pattern_windows(live_pattern_id) ON DELETE CASCADE,

    vector_model_version TEXT NOT NULL,
    vector_dimensions INT NOT NULL,
    feature_vector float8[],

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pattern_similarity_matches (
    match_id BIGSERIAL PRIMARY KEY,
    live_pattern_id BIGINT NOT NULL REFERENCES live_pattern_windows(live_pattern_id) ON DELETE CASCADE,
    matched_turn_id BIGINT NOT NULL REFERENCES turning_points(turn_id),

    matched_product_id INT NOT NULL REFERENCES products(product_id),
    matched_turn_type TEXT NOT NULL CHECK (matched_turn_type IN ('TOP', 'BOTTOM')),

    similarity_score NUMERIC(12, 8) NOT NULL,
    distance_score NUMERIC(12, 8),

    matched_outcome_5m_pips NUMERIC(12, 4),
    matched_outcome_10m_pips NUMERIC(12, 4),
    matched_outcome_15m_pips NUMERIC(12, 4),

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pattern_library_profiles (
    profile_id BIGSERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id),
    turn_type TEXT NOT NULL CHECK (turn_type IN ('TOP', 'BOTTOM')),
    profile_scope TEXT NOT NULL CHECK (profile_scope IN ('PRODUCT_ONLY', 'PRODUCT_TYPE', 'GLOBAL')),

    sample_count INT NOT NULL,
    vector_model_version TEXT NOT NULL,
    average_vector float8[],

    avg_outcome_5m_pips NUMERIC(12, 4),
    avg_outcome_10m_pips NUMERIC(12, 4),
    avg_outcome_15m_pips NUMERIC(12, 4),

    success_rate_5m NUMERIC(12, 8),
    success_rate_10m NUMERIC(12, 8),
    success_rate_15m NUMERIC(12, 8),

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Cross-Product Relationship Storage
CREATE TABLE IF NOT EXISTS product_relationships (
    relationship_id BIGSERIAL PRIMARY KEY,

    product_a_id INT NOT NULL REFERENCES products(product_id),
    product_b_id INT NOT NULL REFERENCES products(product_id),

    relationship_type TEXT NOT NULL CHECK (
        relationship_type IN (
            'SAME_DIRECTION',
            'INVERSE_DIRECTION',
            'LEADER_FOLLOWER',
            'LAGGING_CONFIRMATION',
            'DIVERGENCE_WARNING',
            'BASKET_CONFIRMATION',
            'UNKNOWN'
        )
    ),

    best_lag_minutes INT,
    same_direction_rate NUMERIC(12, 8),
    inverse_direction_rate NUMERIC(12, 8),
    lead_lag_confidence NUMERIC(12, 8),

    sample_count INT NOT NULL,
    last_calculated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    UNIQUE(product_a_id, product_b_id, relationship_type, best_lag_minutes)
);

CREATE TABLE IF NOT EXISTS cross_product_pattern_events (
    event_id BIGSERIAL PRIMARY KEY,
    event_time TIMESTAMP NOT NULL,

    primary_product_id INT REFERENCES products(product_id),
    primary_live_pattern_id BIGINT REFERENCES live_pattern_windows(live_pattern_id),

    event_type TEXT NOT NULL CHECK (
        event_type IN (
            'SAME_DIRECTION_CONFIRMATION',
            'INVERSE_DIRECTION_CONFIRMATION',
            'LEADER_FOLLOWER_SIGNAL',
            'BASKET_TURN',
            'DIVERGENCE_WARNING',
            'ISOLATED_PRODUCT_SIGNAL'
        )
    ),

    event_confidence NUMERIC(12, 8),
    summary TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cross_product_event_members (
    event_member_id BIGSERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL REFERENCES cross_product_pattern_events(event_id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES products(product_id),

    live_pattern_id BIGINT REFERENCES live_pattern_windows(live_pattern_id),

    candidate_turn_type TEXT CHECK (candidate_turn_type IN ('TOP', 'BOTTOM', 'UNKNOWN')),
    bottom_similarity NUMERIC(12, 8),
    top_similarity NUMERIC(12, 8),

    direction_bias TEXT CHECK (direction_bias IN ('UP', 'DOWN', 'NEUTRAL', 'UNCLEAR')),
    lag_minutes_from_primary INT,

    role TEXT CHECK (role IN ('PRIMARY', 'CONFIRMER', 'LEADER', 'LAGGER', 'INVERSE_CONFIRMER', 'DIVERGENT')),

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Initial Data
INSERT INTO products (product_code, product_type, base_currency, quote_currency, pip_size)
VALUES 
('GBP', 'FX', 'GBP', 'USD', 0.0001),
('EUR', 'FX', 'EUR', 'USD', 0.0001),
('JPY', 'FX', 'USD', 'JPY', 0.01)
ON CONFLICT (product_code) DO NOTHING;
