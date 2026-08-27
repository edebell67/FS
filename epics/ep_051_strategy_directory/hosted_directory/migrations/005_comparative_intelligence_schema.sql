-- Version history: 1.0.0 (2026-08-24) Versioned comparative intelligence persistence.
BEGIN;

ALTER TABLE intelligence_saved_search ADD COLUMN IF NOT EXISTS last_result_ids jsonb NOT NULL DEFAULT '[]';
ALTER TABLE intelligence_saved_search ADD COLUMN IF NOT EXISTS last_replayed_at timestamptz;

CREATE TABLE IF NOT EXISTS intelligence_strategy_score (
  strategy_id text NOT NULL,
  score_version text NOT NULL,
  evidence_watermark timestamptz NOT NULL,
  quality_score numeric(8,4) NOT NULL CHECK(quality_score BETWEEN 0 AND 100),
  quality_band text NOT NULL,
  confidence numeric(8,6) NOT NULL CHECK(confidence BETWEEN 0 AND 1),
  rank_eligible boolean NOT NULL,
  components jsonb NOT NULL,
  contribution_trace jsonb NOT NULL,
  generated_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY(strategy_id,score_version,evidence_watermark)
);

CREATE TABLE IF NOT EXISTS intelligence_cohort_percentile (
  strategy_id text NOT NULL,
  metric_name text NOT NULL,
  cohort_kind text NOT NULL,
  cohort_value text NOT NULL,
  cohort_size integer NOT NULL CHECK(cohort_size>=0),
  percentile numeric(8,4) CHECK(percentile BETWEEN 0 AND 100),
  evidence_state text NOT NULL,
  methodology_version text NOT NULL,
  evidence_watermark timestamptz NOT NULL,
  PRIMARY KEY(strategy_id,metric_name,cohort_kind,cohort_value,methodology_version,evidence_watermark)
);

CREATE TABLE IF NOT EXISTS intelligence_correlation (
  left_strategy_id text NOT NULL,
  right_strategy_id text NOT NULL,
  period_start timestamptz NOT NULL,
  period_end timestamptz NOT NULL,
  observation_period text NOT NULL DEFAULT 'day',
  overlap integer NOT NULL CHECK(overlap>=0),
  correlation numeric(10,8) CHECK(correlation BETWEEN -1 AND 1),
  confidence text NOT NULL,
  methodology_version text NOT NULL,
  evidence_watermark timestamptz NOT NULL,
  CHECK(left_strategy_id<right_strategy_id),
  PRIMARY KEY(left_strategy_id,right_strategy_id,period_start,period_end,methodology_version,evidence_watermark)
);

CREATE TABLE IF NOT EXISTS intelligence_similarity (
  strategy_id text NOT NULL,
  related_strategy_id text NOT NULL,
  similarity numeric(8,4) NOT NULL CHECK(similarity BETWEEN 0 AND 100),
  feature_contributions jsonb NOT NULL,
  methodology_version text NOT NULL,
  evidence_watermark timestamptz NOT NULL,
  CHECK(strategy_id<>related_strategy_id),
  PRIMARY KEY(strategy_id,related_strategy_id,methodology_version,evidence_watermark)
);

CREATE INDEX IF NOT EXISTS intelligence_score_rank ON intelligence_strategy_score(score_version,rank_eligible,quality_score DESC);
CREATE INDEX IF NOT EXISTS intelligence_correlation_pair ON intelligence_correlation(left_strategy_id,right_strategy_id,period_end DESC);
CREATE INDEX IF NOT EXISTS intelligence_similarity_neighbours ON intelligence_similarity(strategy_id,similarity DESC);

COMMIT;
