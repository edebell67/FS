# VERSION HISTORY
# v1.0.0 · 2026-08-24 · Point-in-time immutability, freshness and leakage tests.
import hashlib,json
import pytest
from app.intelligence.market import MarketFeatureStore,join_regimes_without_lookahead,validate_market_cache


def test_feature_snapshots_are_idempotent_and_immutable():
    store=MarketFeatureStore();digest=store.ingest("FX","2026-01-01T00:00:00Z",{"trend":.1},"feed-1")
    assert store.ingest("FX","2026-01-01T00:00:00Z",{"trend":.1},"feed-1")==digest
    with pytest.raises(ValueError):store.ingest("FX","2026-01-01T00:00:00Z",{"trend":.2},"feed-1")


def test_as_of_lookup_and_freshness_never_use_future_features():
    store=MarketFeatureStore();store.ingest("FX","2026-01-01T10:00:00Z",{"trend":.1},"feed-1")
    store.ingest("FX","2026-01-01T12:00:00Z",{"trend":.2},"feed-1")
    assert store.as_of("FX","2026-01-01T11:00:00Z")["features"]["trend"]==.1
    assert store.current("FX","2026-01-01T12:30:00Z",3600)["fresh"] is True
    assert store.current("FX","2026-01-01T14:00:00Z",3600)["state"]=="STALE"


def test_regime_join_has_no_lookahead():
    returns=[{"timestamp":"2026-01-01T10:30:00Z","return":1},{"timestamp":"2026-01-01T12:30:00Z","return":2}]
    regimes=[{"as_of":"2026-01-01T10:00:00Z","state":"bull"},{"as_of":"2026-01-01T12:00:00Z","state":"bear"}]
    joined=join_regimes_without_lookahead(returns,regimes)
    assert [row["regime"] for row in joined]==["bull","bear"]


def test_market_cache_is_content_addressed_and_validated_before_ingestion():
    payload={"schema_version":"1.0.0","generated_at":"2026-01-01T12:00:00Z","market":"FX","source":"test","source_url":"https://example.test","source_version":"feed-1","features":[{"market":"FX","as_of":"2026-01-01T10:00:00Z","features":{"trend":.1},"source_version":"feed-1"}]}
    payload["sha256"]=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()
    assert validate_market_cache(payload,now="2026-01-01T12:00:00Z") is payload
    payload["features"][0]["features"]["trend"]=.2
    with pytest.raises(ValueError,match="digest mismatch"):validate_market_cache(payload,now="2026-01-01T12:00:00Z")


def test_market_cache_rejects_future_or_duplicate_rows():
    def signed(rows):
        value={"schema_version":"1.0.0","features":rows};value["sha256"]=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest();return value
    row={"market":"FX","as_of":"2026-01-02T10:00:00Z","features":{"trend":.1},"source_version":"feed-1"}
    with pytest.raises(ValueError,match="future"):validate_market_cache(signed([row]),now="2026-01-01T12:00:00Z")
    row["as_of"]="2026-01-01T10:00:00Z"
    with pytest.raises(ValueError,match="duplicate"):validate_market_cache(signed([row,row]),now="2026-01-01T12:00:00Z")
