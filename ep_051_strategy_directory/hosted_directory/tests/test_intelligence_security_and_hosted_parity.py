"""Regression proof for intelligence trust boundaries and hosted/local API parity."""
from datetime import datetime,timezone

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.config import Settings
from app.contracts import Snapshot,Strategy,snapshot_hash
from app.intelligence.discovery import StrategyQuery
from app.intelligence.profile import build_profile
from app.main import create_app
from app.repository import MemoryRepository


def _point(strategy_id,number,value,equity,drawdown):
    return {"strategy_id":strategy_id,"trade_id":f"t{number}","trade_number":number,"opened_at":f"2026-08-{number:02d}T08:00:00Z","observed_at":f"2026-08-{number:02d}T09:00:00Z","net_return":value,"cumulative_net_return":equity,"drawdown":drawdown}


def test_unit_bearing_constraints_fail_closed_when_unit_is_missing():
    with pytest.raises(ValidationError):StrategyQuery(min_annualized_return=.1)
    with pytest.raises(ValidationError):StrategyQuery(max_drawdown=100)


def test_hosted_snapshot_serves_profile_series_and_comparison():
    strategies=[];profiles=[];series=[]
    for strategy_id,values in (("DNA_1",[2,-1,3]),("DNA_2",[1,-2,4])):
        equity=peak=0;maximum_drawdown=0
        for value in values:
            equity+=value;peak=max(peak,equity);maximum_drawdown=min(maximum_drawdown,equity-peak)
        summary=Strategy(strategy_id=strategy_id,total_trades=3,wins=2,losses=1,breakevens=0,total_net_return=sum(values),win_rate=2/3,profit_factor=sum(value for value in values if value>0)/abs(sum(value for value in values if value<0)),max_drawdown_money=maximum_drawdown,evidence_start="2026-08-01T08:00:00Z",evidence_end="2026-08-03T09:00:00Z",quality_state="COLLECTING")
        strategies.append(summary);equity=peak=0;curve=[]
        for number,value in enumerate(values,1):
            equity+=value;peak=max(peak,equity);item=_point(strategy_id,number,value,equity,equity-peak);series.append(item);curve.append({"trade_number":number,"opened_at":item["opened_at"],"closed_at":item["observed_at"],"net_return":value,"equity":equity,"drawdown":item["drawdown"]})
        profiles.append(build_profile(summary.model_dump(mode="json"),curve))
    digest=snapshot_hash(strategies,profiles,series);now=datetime.now(timezone.utc)
    snapshot=Snapshot(snapshot_id="dna-hosted-parity",source_watermark=now,generated_at=now,item_count=2,sha256=digest,items=strategies,intelligence_profiles=profiles,return_series=series)
    repository=MemoryRepository();repository.promote(snapshot)
    client=TestClient(create_app(repository=repository,settings=Settings(data_backend="memory")))
    assert client.get("/api/dna/strategies/DNA_1/equity-curve").json()["total_points"]==3
    assert client.get("/api/intelligence/strategies/DNA_1").status_code==200
    comparison=client.get("/api/intelligence/compare",params={"strategy_ids":"DNA_1,DNA_2"})
    assert comparison.status_code==200 and len(comparison.json()["relationships"])==1
    period=client.get("/api/dna/strategies/DNA_1/equity-curve",params={"date_from":"2026-08-02","date_to":"2026-08-03"}).json()["points"]
    assert [item["trade_number"] for item in period]==[1,2]
    assert [item["equity"] for item in period]==[-1,2] and [item["drawdown"] for item in period]==[-1,0]


def test_public_regime_contract_rejects_fabricated_and_nonfinite_evidence():
    client=TestClient(create_app(settings=Settings(data_backend="memory",sync_token="publisher")))
    assert client.post("/api/intelligence/regimes/classify",json={"market":"FX","features":{"trend":1}}).status_code==422
    result=client.post("/internal/intelligence/market-features",headers={"Authorization":"Bearer publisher"},json={"market":"FX","as_of":datetime.now(timezone.utc).isoformat(),"features":{"trend":"NaN"},"source_version":"feed-1"})
    assert result.status_code==422


def test_source_metadata_renderers_apply_output_encoding():
    for path in ("web/index.html","web/strategy.html","web/builder.html"):
        source=open(path,encoding="utf-8").read()
        assert "const esc" in source and "descriptive_name" in source
