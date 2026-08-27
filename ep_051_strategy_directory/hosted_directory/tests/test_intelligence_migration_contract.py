# VERSION HISTORY
# v1.0.0 · 2026-08-24 · Hosted intelligence schema and tenant-policy contract coverage.
from pathlib import Path


SQL=(Path(__file__).resolve().parents[1]/"migrations"/"002_intelligence_layer_schema.sql").read_text(encoding="utf-8").lower()


def test_hosted_schema_persists_all_intelligence_domains():
    for table in ("intelligence_source_evidence","intelligence_profile","intelligence_return_series","intelligence_period_metric",
                  "intelligence_watchlist","intelligence_saved_search","intelligence_collection","intelligence_preference",
                  "intelligence_market_feature","intelligence_regime_label","intelligence_strategy_regime_profile","intelligence_recommendation_run"):
        assert f"create table if not exists {table}" in SQL


def test_private_tables_enable_owner_row_level_security_and_deletion_cascades():
    for table in ("intelligence_user_consent","intelligence_watchlist","intelligence_saved_search","intelligence_collection",
                  "intelligence_collection_strategy","intelligence_preference","intelligence_user_history","intelligence_privacy_audit"):
        assert f"alter table {table} enable row level security" in SQL
    assert "owner_id=current_setting(''app.user_id'',true)" in SQL
    assert "on delete cascade" in SQL


def test_regime_schema_enforces_point_in_time_invariant():
    assert "check(feature_as_of<=as_of)" in SQL
    assert "intelligence_user_history_expiry" in SQL
