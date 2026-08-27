# VERSION HISTORY
# v1.2.0 · 2026-08-24 · Adds timestamp alignment and classified-cohort safety coverage.
# v1.1.0 · 2026-08-24 · Adds comparison API contract coverage.
# v1.0.0 · 2026-08-24 · Composite-score, percentile, correlation and similarity golden tests.
from fastapi.testclient import TestClient
from app.config import Settings
from app.main import create_app
from app.intelligence.comparative import SCORE_SPEC,cohort_percentiles,correlation,correlation_matrix,percentile,related_strategies,rolling_correlation,score_profile,similarity


def profile(confidence=.8):
    names=("annualized_return","profit_factor","max_drawdown","volatility","sharpe","sortino")
    values=(1000,1.5,-500,900,1.2,1.8)
    return {"metrics":{n:{"value":v} for n,v in zip(names,values)},"evidence":{"confidence":confidence}}


def test_score_is_explainable_bounded_and_evidence_sensitive():
    high=score_profile(profile(.9)); low=score_profile(profile(.2))
    assert 0<=high["quality_score"]<=100
    assert high["quality_score"]>low["quality_score"]
    assert low["rank_eligible"] is False and low["quality_band"]=="insufficient evidence"
    assert SCORE_SPEC["range"]==[0,100] and set(high["components"])==set(high["weights"])
    assert abs(sum(high["weights"].values())-1)<1e-9
    assert len(high["explanation"])==5


def test_relationship_services_are_symmetric_rolling_and_explainable():
    a=[{"timestamp":f"2026-01-{day:02d}","return":day} for day in range(1,6)];b=[{"timestamp":f"2026-01-{day:02d}","return":day*2} for day in range(1,6)]
    matrix=correlation_matrix({"A":a,"B":b});assert matrix["cells"][-1]["value"]==1
    assert len(rolling_correlation(a,b,window=3))==3
    target={"strategy_id":"A","quality_score":80,"win_rate":.6,"profit_factor":1.5,"max_drawdown":-5};candidates=[{"strategy_id":"B","quality_score":79,"win_rate":.59,"profit_factor":1.45,"max_drawdown":-5.2},{"strategy_id":"C","quality_score":10,"win_rate":.1,"profit_factor":.2,"max_drawdown":-50}]
    related=related_strategies(target,candidates);assert related[0]["strategy_id"]=="B" and related[0]["reasons"]


def test_percentile_uses_midrank_and_requires_cohort():
    assert percentile(20,[10,20,20,30])==50
    assert percentile(1,[1]) is None


def test_correlation_reports_overlap_and_insufficient_evidence():
    assert correlation([1,2,3],[2,4,6])["value"]==1
    assert correlation([1,2],[2,4])["confidence"]=="insufficient"


def test_correlation_aligns_by_timestamp_not_array_position():
    left=[{"timestamp":"2026-01-02","return":2},{"timestamp":"2026-01-01","return":1},{"timestamp":"2026-01-03","return":3}]
    right=[{"timestamp":"2026-01-03","return":6},{"timestamp":"2026-01-01","return":2},{"timestamp":"2026-01-02","return":4}]
    result=correlation(left,right)
    assert result["value"]==1 and result["timestamp_aligned"] is True and result["overlap"]==3


def test_classified_cohorts_suppress_small_peer_groups():
    rows=[{"strategy_id":f"DNA_{n}","quality":n,"family":"trend" if n<5 else "range","asset_class":"FX"} for n in range(6)]
    result=cohort_percentiles(rows,"quality",minimum_size=5)
    assert result["DNA_2"]["family"]["state"]=="VALID"
    assert result["DNA_5"]["family"]["state"]=="INSUFFICIENT_COHORT"
    assert result["DNA_5"]["family"]["percentile"] is None


def test_similarity_exposes_feature_contributions():
    result=similarity({"quality_score":90,"win_rate":.6},{"quality_score":85,"win_rate":.55})
    assert result["similarity"]>90
    assert set(result["contributions"])=={"quality_score","win_rate"}


def test_compare_api_returns_profiles_scores_and_relationships(monkeypatch):
    import app.main as module
    monkeypatch.setattr(module,"local_strategies",lambda settings,start,end,strategy_id:[{"strategy_id":strategy_id,"descriptive_name":None,"product_name":"EURUSD","market":"FX"}])
    monkeypatch.setattr(module,"local_equity_curve",lambda settings,strategy_id,*args:[
      {"closed_at":"2024-01-01T00:00:00+00:00","net_return":1},{"closed_at":"2024-02-01T00:00:00+00:00","net_return":2},{"closed_at":"2024-03-01T00:00:00+00:00","net_return":3}])
    client=TestClient(create_app(settings=Settings(data_backend="sqlserver",db_server="x",db_user="x",db_pass="x",local_intelligence_cache_path="runtime/__missing_compare_cache__.json",allow_synchronous_local_fallback=True)))
    response=client.get("/api/intelligence/compare?strategy_ids=DNA_1,DNA_2")
    assert response.status_code==200
    assert set(response.json()["profiles"])=={"DNA_1","DNA_2"}
    assert response.json()["relationships"][0]["correlation"]["value"]==1


def test_ascending_rank_keeps_evidence_eligible_profiles_first():
    from app.intelligence.discovery import StrategyQuery,retrieve
    base={"classification":{"asset_class":"FX","instruments":[]},"metrics":{},"evidence":{},"regimes":{}}
    eligible={**base,"identity":{"strategy_id":"DNA_ELIGIBLE"},"score":{"quality_score":80,"rank_eligible":True}}
    collecting={**base,"identity":{"strategy_id":"DNA_COLLECTING"},"score":{"quality_score":10,"rank_eligible":False}}
    rows=retrieve([collecting,eligible],StrategyQuery(direction="asc"))
    assert [row["profile"]["identity"]["strategy_id"] for row in rows]==["DNA_ELIGIBLE","DNA_COLLECTING"]
