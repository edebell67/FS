# Skill Update: Turning-Point Pattern Database Design

## Purpose

Extend the price-frequency cluster interpretation skill into a database-backed pattern engine.

The goal is to store frequency-count behaviour around confirmed tops and bottoms, normalise those patterns, and make future quantitative comparison straightforward.

The system should support:

```text
1. Storing raw bid/ask frequency snapshots.
2. Detecting and storing confirmed tops and bottoms.
3. Extracting pattern windows around each turning point.
4. Normalising price levels relative to the turning price.
5. Creating comparable feature vectors.
6. Comparing live patterns against historical bottom/top libraries.
7. Comparing behaviour across multiple products.
8. Detecting same-direction, inverse, and lead/lag relationships.
```

Target output:

```text
GBP live pattern is 78% similar to prior GBP bottom patterns.
EUR showed a similar bottom pattern 5 minutes earlier.
Historically, this combination led to GBP rising over the next 10 minutes 72% of the time.
```

---

## Core Principle

Do not compare absolute prices.

Compare:

```text
- frequency shape
- accepted-zone migration
- cluster width
- skew
- magnet shift
- failed probes
- vanishing prior zones
- rebuild behaviour
- lead/lag behaviour across products
```

Every stored turning-point pattern must be aligned to a relative coordinate system:

```text
turning price = 0
1 pip above = +1
1 pip below = -1
```

This allows a bottom at 1.3000 and a bottom at 1.2760 to be compared by shape.

---

## Recommended Database Approach

Use PostgreSQL first.

Recommended stack:

```text
PostgreSQL
+ TimescaleDB extension if snapshot volume is high
+ pgvector extension for similarity search
```

Why:

```text
PostgreSQL handles structured trade/time-series metadata well.
TimescaleDB helps if snapshot volume becomes large.
pgvector allows fast similarity search over numeric pattern vectors.
```

Do not rely only on flat files if the system needs to support many products, many snapshots, and historical pattern comparison.

---

## Main Tables

### products

Stores each instrument/product being monitored.

```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_code TEXT NOT NULL UNIQUE,
    product_type TEXT,
    quote_currency TEXT,
    base_currency TEXT,
    pip_size NUMERIC(12, 8) NOT NULL DEFAULT 0.0001,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

### frequency_snapshots

Stores one snapshot event per product and timestamp.

```sql
CREATE TABLE frequency_snapshots (
    snapshot_id BIGSERIAL PRIMARY KEY,
    product_id INT NOT NULL REFERENCES products(product_id),
    snapshot_time TIMESTAMP NOT NULL,
    source_run_id TEXT,
    window_seconds INT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    UNIQUE(product_id, snapshot_time)
);
```

---

### frequency_levels

Stores the actual bid/ask price-frequency counts for each snapshot.

```sql
CREATE TABLE frequency_levels (
    level_id BIGSERIAL PRIMARY KEY,
    snapshot_id BIGINT NOT NULL REFERENCES frequency_snapshots(snapshot_id) ON DELETE CASCADE,
    side TEXT NOT NULL CHECK (side IN ('BID', 'ASK')),
    price NUMERIC(18, 8) NOT NULL,
    frequency_count INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_frequency_levels_snapshot_side 
ON frequency_levels(snapshot_id, side);

CREATE INDEX idx_frequency_levels_price 
ON frequency_levels(price);
```

---

## Turning-Point Storage

### turning_points

Stores confirmed tops and bottoms.

```sql
CREATE TABLE turning_points (
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

    outcome_5m_pips NUMERIC(12, 4),
    outcome_10m_pips NUMERIC(12, 4),
    outcome_15m_pips NUMERIC(12, 4),
    outcome_30m_pips NUMERIC(12, 4),

    max_favourable_10m_pips NUMERIC(12, 4),
    max_adverse_10m_pips NUMERIC(12, 4),

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    UNIQUE(product_id, turn_time, turn_type)
);
```

Confirmed turn examples:

```text
BOTTOM:
The lowest price in a local window where subsequent snapshots migrate upward by at least X pips or X accepted-zone shift.

TOP:
The highest price in a local window where subsequent snapshots migrate downward by at least X pips or X accepted-zone shift.
```

---

### turning_point_windows

Stores which snapshots belong to each turning-point pattern.

```sql
CREATE TABLE turning_point_windows (
    window_id BIGSERIAL PRIMARY KEY,
    turn_id BIGINT NOT NULL REFERENCES turning_points(turn_id) ON DELETE CASCADE,
    snapshot_id BIGINT NOT NULL REFERENCES frequency_snapshots(snapshot_id),
    relative_time_index INT NOT NULL,

    -- T-3 = -3
    -- T-2 = -2
    -- T-1 = -1
    -- T   = 0
    -- T+1 = 1
    -- T+2 = 2
    -- T+3 = 3

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    UNIQUE(turn_id, snapshot_id)
);
```

---

## Normalised Pattern Storage

### normalised_pattern_levels

Stores the aligned pattern levels for each turning point.

This is one of the most important tables.

```sql
CREATE TABLE normalised_pattern_levels (
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

CREATE INDEX idx_normalised_pattern_lookup
ON normalised_pattern_levels(turn_type, relative_time_index, side, relative_pips);

CREATE INDEX idx_normalised_pattern_turn
ON normalised_pattern_levels(turn_id);
```

Example:

```text
turn_price = 1.3000

raw_price = 1.3003
relative_pips = +3

raw_price = 1.2998
relative_pips = -2
```

This table allows many tops/bottoms to be overlaid directly.

---

## Feature Vector Storage

The comparison engine should not only compare raw matrices. It should also compare feature vectors.

### pattern_features

Stores calculated features for each turning-point pattern.

```sql
CREATE TABLE pattern_features (
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
```

---

### pattern_vectors

Stores the vector representation for similarity search.

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE pattern_vectors (
    vector_id BIGSERIAL PRIMARY KEY,
    turn_id BIGINT NOT NULL REFERENCES turning_points(turn_id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES products(product_id),
    turn_type TEXT NOT NULL CHECK (turn_type IN ('TOP', 'BOTTOM')),

    vector_model_version TEXT NOT NULL,
    vector_dimensions INT NOT NULL,
    feature_vector VECTOR(128),

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_pattern_vectors_vector
ON pattern_vectors
USING ivfflat (feature_vector vector_cosine_ops);
```

Start simple:

```text
Use a deterministic numeric vector, not an LLM embedding.
```

Example vector construction:

```text
For each relative_time_index from -3 to +3:
For each relative_pips from -10 to +10:
- store normalised bid frequency
- store normalised ask frequency
Then append engineered features.
```

---

## Live Pattern Storage

### live_pattern_windows

Stores rolling live candidate windows.

```sql
CREATE TABLE live_pattern_windows (
    live_pattern_id BIGSERIAL PRIMARY KEY,
    product_id INT NOT NULL REFERENCES products(product_id),
    latest_snapshot_time TIMESTAMP NOT NULL,

    candidate_type TEXT CHECK (candidate_type IN ('TOP', 'BOTTOM', 'UNKNOWN')),
    candidate_turn_price NUMERIC(18, 8),

    pre_window_snapshots INT NOT NULL,
    post_window_snapshots INT DEFAULT 0,

    current_state TEXT,
    direction_bias TEXT CHECK (direction_bias IN ('UP', 'DOWN', 'NEUTRAL', 'UNCLEAR')),

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

### live_pattern_vectors

Stores vectorised live windows for comparison against historical patterns.

```sql
CREATE TABLE live_pattern_vectors (
    live_vector_id BIGSERIAL PRIMARY KEY,
    live_pattern_id BIGINT NOT NULL REFERENCES live_pattern_windows(live_pattern_id) ON DELETE CASCADE,

    vector_model_version TEXT NOT NULL,
    vector_dimensions INT NOT NULL,
    feature_vector VECTOR(128),

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

## Similarity Match Storage

### pattern_similarity_matches

Stores live-vs-historical pattern comparisons.

```sql
CREATE TABLE pattern_similarity_matches (
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
```

Example derived read:

```text
Live GBP pattern matched 64 prior bottom patterns.
Average similarity = 0.78.
Next 10m up-rate = 72%.
```

---

## Aggregated Pattern Profiles

### pattern_library_profiles

Stores aggregate top/bottom signatures by product or across products.

```sql
CREATE TABLE pattern_library_profiles (
    profile_id BIGSERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id),
    turn_type TEXT NOT NULL CHECK (turn_type IN ('TOP', 'BOTTOM')),
    profile_scope TEXT NOT NULL CHECK (profile_scope IN ('PRODUCT_ONLY', 'PRODUCT_TYPE', 'GLOBAL')),

    sample_count INT NOT NULL,
    vector_model_version TEXT NOT NULL,
    average_vector VECTOR(128),

    avg_outcome_5m_pips NUMERIC(12, 4),
    avg_outcome_10m_pips NUMERIC(12, 4),
    avg_outcome_15m_pips NUMERIC(12, 4),

    success_rate_5m NUMERIC(12, 8),
    success_rate_10m NUMERIC(12, 8),
    success_rate_15m NUMERIC(12, 8),

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

Use this for comparing live GBP against:

```text
GBP bottom profile
GBP top profile
FX bottom profiles
FX top profiles
global bottom profile
global top profile
```

---

## Cross-Product Relationship Storage

### product_relationships

Stores discovered relationships between products.

```sql
CREATE TABLE product_relationships (
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
```

---

### cross_product_pattern_events

Stores multi-product events at a given time.

```sql
CREATE TABLE cross_product_pattern_events (
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
```

---

### cross_product_event_members

Stores the products participating in a cross-product event.

```sql
CREATE TABLE cross_product_event_members (
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
```

---

## Pattern Comparison Method

### Single-Product Similarity

For each live product window:

```text
1. Build live candidate pattern.
2. Choose candidate turn price.
3. Convert raw prices to relative_pips.
4. Build normalised frequency matrix.
5. Build feature vector.
6. Compare to historical TOP vectors.
7. Compare to historical BOTTOM vectors.
8. Return nearest matches and aggregate outcomes.
```

Example decision:

```text
bottom_similarity = average similarity to nearest 50 bottom patterns
top_similarity = average similarity to nearest 50 top patterns

direction_bias = UP if bottom_similarity materially exceeds top_similarity
direction_bias = DOWN if top_similarity materially exceeds bottom_similarity
```

---

### Cross-Product Similarity

For each product pair:

```text
1. Compare live pattern states across products.
2. Check whether similar or inverse patterns appeared within lag windows.
3. Test lags such as -15, -10, -5, 0, +5, +10, +15 minutes.
4. Store best historical lag relationship.
5. Use that relationship to boost or reduce confidence.
```

Example:

```text
EUR bottom-like pattern appears at 15:00.
GBP bottom-like pattern appears at 15:05.
Historically this EUR -> GBP sequence leads to GBP upward continuation 69% of the time.
```

---

## Recommended Similarity Metrics

Use multiple scores, not just one.

```text
1. Cosine similarity over normalised vectors.
2. Euclidean distance over engineered feature vectors.
3. Dynamic time warping for magnet path sequence.
4. Correlation of relative frequency distribution.
5. Separate same-side and inverse-side comparisons.
```

Start with:

```text
cosine similarity + feature distance
```

Add dynamic time warping later.

---

## Feature Engineering Details

### Frequency Shape Features

```text
peak_frequency
total_frequency
cluster_width_pips
frequency_above_turn
frequency_below_turn
above_below_ratio
frequency_skew
frequency_kurtosis
normalised_peak_location
```

### Magnet Movement Features

```text
magnet_path = [T-3, T-2, T-1, T, T+1, T+2, T+3]
magnet_shift_pre_turn
magnet_shift_post_turn
magnet_acceleration
magnet_reversal_distance
```

### Probe Features

```text
failed_probe_pips
failed_probe_frequency
failed_probe_duration_snapshots
probe_vanish_score
```

### Acceptance Features

```text
accepted_zone_width
accepted_zone_midpoint
accepted_zone_shift
rebuild_score
zone_persistence_score
prior_zone_vanish_score
```

### Outcome Features

```text
outcome_5m_pips
outcome_10m_pips
outcome_15m_pips
direction_success_5m
direction_success_10m
direction_success_15m
max_favourable_excursion
max_adverse_excursion
```

---

## Live Direction Output

The database should support this output:

```json
{
  "product": "GBP",
  "latest_time": "15:05",
  "candidate_turn_type": "BOTTOM",
  "current_state": "THIN_UPWARD_ROTATION",
  "bottom_similarity": 0.78,
  "top_similarity": 0.12,
  "nearest_match_count": 64,
  "historical_next_5m_up_rate": 0.69,
  "historical_next_10m_up_rate": 0.74,
  "historical_avg_10m_move_pips": 4.8,
  "cross_product_confirmation": {
    "leader_product": "EUR",
    "lag_minutes": 5,
    "relationship": "LEADER_FOLLOWER",
    "historical_follow_rate": 0.71
  },
  "final_direction_bias": "UP",
  "confidence": "MEDIUM_HIGH",
  "continuation_trigger": "frequency builds above 1.3003",
  "failure_trigger": "frequency rebuilds below 1.2998"
}
```

---

## Practical Implementation Flow

### Phase 1: Raw Storage

```text
Store products.
Store snapshots.
Store bid/ask frequency levels.
```

Minimum tables:

```text
products
frequency_snapshots
frequency_levels
```

### Phase 2: Turning-Point Labelling

```text
Detect confirmed tops and bottoms.
Store turning_points.
Store turning_point_windows.
```

Minimum new tables:

```text
turning_points
turning_point_windows
```

### Phase 3: Normalisation

```text
Convert raw prices to relative_pips around the turn price.
Store normalised_pattern_levels.
```

Minimum new table:

```text
normalised_pattern_levels
```

### Phase 4: Feature Generation

```text
Calculate numeric features for every turn.
Build deterministic feature vectors.
```

Minimum new tables:

```text
pattern_features
pattern_vectors
```

### Phase 5: Similarity Search

```text
Create live rolling pattern windows.
Vectorise live windows.
Compare against historical vectors.
Store similarity matches.
```

Minimum new tables:

```text
live_pattern_windows
live_pattern_vectors
pattern_similarity_matches
```

### Phase 6: Cross-Product Engine

```text
Calculate product relationships.
Detect leader/follower patterns.
Detect inverse confirmation.
Detect basket turns.
```

Minimum new tables:

```text
product_relationships
cross_product_pattern_events
cross_product_event_members
```

---

## Important Design Rules

### Rule 1: Store Raw Data First

Never only store derived features.

Raw frequency snapshots must be retained so features can be recalculated later.

### Rule 2: Use Relative Prices For Pattern Matching

Absolute prices are not comparable.

Always convert to:

```text
relative_pips_from_turn_price
```

### Rule 3: Version The Feature Model

Every vector should have:

```text
vector_model_version
```

This allows the feature design to evolve without corrupting old results.

### Rule 4: Store Outcomes Separately From Pattern Shape

Do not leak future information into the pattern vector.

Future outcomes should be stored only as labels/results.

### Rule 5: Compare Product-Specific And Global Profiles

For live GBP, compare against:

```text
GBP bottom patterns
GBP top patterns
FX bottom patterns
FX top patterns
global bottom patterns
global top patterns
```

### Rule 6: Treat Thin Patterns Differently

Thin latest snapshots should not be given the same confidence as dense accepted zones.

Store:

```text
thin_snapshot_score
pattern_quality_score
```

### Rule 7: Store Failed Patterns Too

Do not only store successful tops and bottoms.

Also store failed bottom-like and failed top-like events.

Optional table:

```sql
CREATE TABLE failed_pattern_events (
    failed_event_id BIGSERIAL PRIMARY KEY,
    product_id INT NOT NULL REFERENCES products(product_id),
    event_time TIMESTAMP NOT NULL,
    failed_type TEXT CHECK (failed_type IN ('FAILED_BOTTOM_LIKE', 'FAILED_TOP_LIKE')),
    reason TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

## Minimum Viable Database

Start with these tables:

```text
products
frequency_snapshots
frequency_levels
turning_points
turning_point_windows
normalised_pattern_levels
pattern_features
pattern_vectors
live_pattern_windows
live_pattern_vectors
pattern_similarity_matches
```

Add cross-product tables after the single-product pattern matching works.

---

## Expected End State

The system should be able to answer:

```text
Is the current GBP pattern similar to prior GBP bottoms?
Is it more similar to tops or bottoms?
What happened next historically?
Is another product showing the same pattern earlier?
Is another product showing the inverse pattern?
Does cross-product behaviour improve confidence?
What level confirms or invalidates the live signal?
```

Final system output example:

```text
GBP is forming a bottom-like pattern.
Similarity to prior GBP bottoms: 78%.
Similarity to GBP tops: 12%.
Nearest historical matches: 64.
Next 10-minute upward follow-through rate: 74%.
EUR showed the same pattern 5 minutes earlier.
AUD is showing inverse confirmation.
Final bias: UP.
Confidence: MEDIUM_HIGH.
```
