-- Version history: 1.0.0 (2026-08-24) Complete hosted intelligence, private-object and regime persistence schema.
BEGIN;

CREATE TABLE IF NOT EXISTS intelligence_source_evidence (
  evidence_id uuid PRIMARY KEY, source_type text NOT NULL CHECK (source_type IN ('strategy_definition','backtest','live_result','market_series','closed_trade')),
  source_key text NOT NULL, source_version text NOT NULL, source_watermark timestamptz NOT NULL,
  sha256 char(64) NOT NULL, payload jsonb NOT NULL, state text NOT NULL CHECK (state IN ('current','quarantined','superseded')),
  received_at timestamptz NOT NULL DEFAULT now(), UNIQUE(source_type,source_key,source_version,sha256)
);

CREATE TABLE IF NOT EXISTS intelligence_profile (
  strategy_id text NOT NULL, definition_version text NOT NULL, methodology_version text NOT NULL,
  evidence_watermark timestamptz NOT NULL, profile jsonb NOT NULL, generated_at timestamptz NOT NULL,
  is_current boolean NOT NULL DEFAULT false, PRIMARY KEY(strategy_id,definition_version,methodology_version,evidence_watermark)
);
CREATE UNIQUE INDEX IF NOT EXISTS intelligence_profile_one_current ON intelligence_profile(strategy_id) WHERE is_current;

CREATE TABLE IF NOT EXISTS intelligence_return_series (
  strategy_id text NOT NULL, observed_at timestamptz NOT NULL, trade_id text NOT NULL,
  net_return numeric(28,8) NOT NULL, cumulative_net_return numeric(28,8) NOT NULL, drawdown numeric(28,8) NOT NULL,
  evidence_watermark timestamptz NOT NULL, methodology_version text NOT NULL,
  PRIMARY KEY(strategy_id,observed_at,trade_id,methodology_version)
);
CREATE INDEX IF NOT EXISTS intelligence_return_series_period ON intelligence_return_series(strategy_id,observed_at DESC);

CREATE TABLE IF NOT EXISTS intelligence_period_metric (
  strategy_id text NOT NULL, period_kind text NOT NULL CHECK(period_kind IN ('day','week','month','year','rolling')),
  period_start timestamptz NOT NULL, period_end timestamptz NOT NULL, methodology_version text NOT NULL,
  metrics jsonb NOT NULL, evidence_state text NOT NULL, generated_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY(strategy_id,period_kind,period_start,period_end,methodology_version)
);

CREATE TABLE IF NOT EXISTS intelligence_user_consent (
  owner_id text PRIMARY KEY, history_enabled boolean NOT NULL DEFAULT false, changed_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS intelligence_watchlist (
  owner_id text NOT NULL, strategy_id text NOT NULL, evidence_version text, created_at timestamptz NOT NULL DEFAULT now(), PRIMARY KEY(owner_id,strategy_id)
);
CREATE TABLE IF NOT EXISTS intelligence_saved_search (
  saved_search_id uuid PRIMARY KEY, owner_id text NOT NULL, name text NOT NULL, schema_version text NOT NULL,
  canonical_plan jsonb NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS intelligence_collection (
  collection_id uuid PRIMARY KEY, owner_id text NOT NULL, name text NOT NULL, notes text NOT NULL DEFAULT '',
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE(collection_id,owner_id)
);
CREATE TABLE IF NOT EXISTS intelligence_collection_strategy (
  collection_id uuid NOT NULL, owner_id text NOT NULL, strategy_id text NOT NULL, evidence_version text,
  PRIMARY KEY(collection_id,strategy_id),
  FOREIGN KEY(collection_id,owner_id) REFERENCES intelligence_collection(collection_id,owner_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS intelligence_preference (
  owner_id text PRIMARY KEY, explicit_preferences jsonb NOT NULL DEFAULT '{}', inferred_signals jsonb NOT NULL DEFAULT '{}',
  derivation_version text NOT NULL, updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS intelligence_user_history (
  event_id uuid PRIMARY KEY, owner_id text NOT NULL, event_type text NOT NULL, event_payload jsonb NOT NULL,
  occurred_at timestamptz NOT NULL DEFAULT now(), expires_at timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS intelligence_user_history_expiry ON intelligence_user_history(expires_at);
CREATE TABLE IF NOT EXISTS intelligence_privacy_audit (
  audit_id bigserial PRIMARY KEY, owner_id text NOT NULL, action text NOT NULL, occurred_at timestamptz NOT NULL DEFAULT now(), request_id text
);

CREATE TABLE IF NOT EXISTS intelligence_market_feature (
  market text NOT NULL, as_of timestamptz NOT NULL, source_version text NOT NULL, features jsonb NOT NULL, sha256 char(64) NOT NULL,
  received_at timestamptz NOT NULL DEFAULT now(), PRIMARY KEY(market,as_of,source_version)
);
CREATE TABLE IF NOT EXISTS intelligence_regime_label (
  market text NOT NULL, as_of timestamptz NOT NULL, classifier_version text NOT NULL, state text NOT NULL,
  probabilities jsonb NOT NULL, feature_as_of timestamptz NOT NULL, confidence numeric(8,6) NOT NULL,
  PRIMARY KEY(market,as_of,classifier_version), CHECK(feature_as_of<=as_of)
);
CREATE TABLE IF NOT EXISTS intelligence_strategy_regime_profile (
  strategy_id text NOT NULL, market text NOT NULL, regime text NOT NULL, methodology_version text NOT NULL,
  sample_count integer NOT NULL, metrics jsonb NOT NULL, confidence_interval jsonb, evidence_state text NOT NULL,
  evidence_watermark timestamptz NOT NULL, PRIMARY KEY(strategy_id,market,regime,methodology_version,evidence_watermark)
);
CREATE TABLE IF NOT EXISTS intelligence_recommendation_run (
  run_id uuid PRIMARY KEY, owner_id text, market text NOT NULL, regime_as_of timestamptz NOT NULL,
  methodology_version text NOT NULL, constraints jsonb NOT NULL, results jsonb NOT NULL, created_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE intelligence_user_consent ENABLE ROW LEVEL SECURITY;
ALTER TABLE intelligence_watchlist ENABLE ROW LEVEL SECURITY;
ALTER TABLE intelligence_saved_search ENABLE ROW LEVEL SECURITY;
ALTER TABLE intelligence_collection ENABLE ROW LEVEL SECURITY;
ALTER TABLE intelligence_collection_strategy ENABLE ROW LEVEL SECURITY;
ALTER TABLE intelligence_preference ENABLE ROW LEVEL SECURITY;
ALTER TABLE intelligence_user_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE intelligence_privacy_audit ENABLE ROW LEVEL SECURITY;

ALTER TABLE intelligence_user_consent FORCE ROW LEVEL SECURITY;
ALTER TABLE intelligence_watchlist FORCE ROW LEVEL SECURITY;
ALTER TABLE intelligence_saved_search FORCE ROW LEVEL SECURITY;
ALTER TABLE intelligence_collection FORCE ROW LEVEL SECURITY;
ALTER TABLE intelligence_collection_strategy FORCE ROW LEVEL SECURITY;
ALTER TABLE intelligence_preference FORCE ROW LEVEL SECURITY;
ALTER TABLE intelligence_user_history FORCE ROW LEVEL SECURITY;
ALTER TABLE intelligence_privacy_audit FORCE ROW LEVEL SECURITY;

DO $$ DECLARE table_name text; BEGIN
  FOREACH table_name IN ARRAY ARRAY['intelligence_user_consent','intelligence_watchlist','intelligence_saved_search','intelligence_collection','intelligence_collection_strategy','intelligence_preference','intelligence_user_history','intelligence_privacy_audit'] LOOP
    EXECUTE format('DROP POLICY IF EXISTS owner_isolation ON %I',table_name);
    EXECUTE format('CREATE POLICY owner_isolation ON %I USING (owner_id=current_setting(''app.user_id'',true)) WITH CHECK (owner_id=current_setting(''app.user_id'',true))',table_name);
  END LOOP;
END $$;

COMMIT;
