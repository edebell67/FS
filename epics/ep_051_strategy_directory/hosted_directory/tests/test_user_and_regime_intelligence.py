# VERSION HISTORY
# v1.0.0 · 2026-08-24 · Tenant isolation, privacy lifecycle, regime and recommendation tests.
from app.intelligence.user import UserIntelligenceStore,preference_trace
from app.intelligence.regime import classify,recommend,strategy_regime_profile


def test_user_objects_are_tenant_isolated_exportable_and_deletable():
    store=UserIntelligenceStore();store.watch("a","DNA_1");store.watch("b","DNA_2")
    search=store.save_search("a","quality",{"min_sharpe":1.5});collection=store.create_collection("a","core",["DNA_1"])
    assert store.export("a")["watchlist"]==["DNA_1"] and store.export("b")["watchlist"]==["DNA_2"]
    assert search in store.export("a")["searches"] and collection in store.export("a")["collections"]
    store.delete("a");assert store.export("a")["watchlist"]==[]


def test_history_requires_consent_and_preferences_are_traceable():
    store=UserIntelligenceStore();store.record("u",{"market":"FX"},consented=False);assert store.export("u")["history"]==[]
    trace=preference_trace({"risk":"low"},[{"market":"FX"},{"market":"FX"}]);assert trace["explicit"]["risk"]=="low" and trace["inferred_market_counts"]["FX"]==2


def test_regime_classifier_fails_closed_and_classifies_point_in_time():
    assert classify({"trend":None})["state"]=="UNKNOWN"
    result=classify({"trend":.04,"volatility_z":1.1,"drawdown":-.03});assert result["state"]=="bull / high volatility" and result["confidence"]>=.5
    assert abs(sum(result["probabilities"].values())-1)<1e-12 and result["calibration_version"].startswith("ecb-next-day-direction")


def test_strategy_profiles_gate_samples_and_recommendations_explain():
    observations=[{"regime":"bull / high volatility","return":x} for x in (1,2,1,3,2)]
    profile=strategy_regime_profile(observations,minimum=5);assert profile["bull / high volatility"]["confidence"]=="VALID"
    current=classify({"trend":.04,"volatility_z":1.1,"drawdown":-.03})
    results=recommend(current,[{"strategy_id":"DNA_1","quality_score":80,"max_drawdown":-.1,"regimes":profile}],risk_limit=.2)
    assert results[0]["strategy_id"]=="DNA_1" and len(results[0]["why"])==3
