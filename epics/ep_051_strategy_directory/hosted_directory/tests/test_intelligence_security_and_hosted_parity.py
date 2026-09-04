# Version history:
# 2026-09-04 v2.0.0 - The intelligence/regime/compare tests that lived here moved to
#   epics/ep_049_strategy_intelligence/hosted_directory/tests/test_intelligence_security_and_hosted_parity.py
#   per Ed's EP049 ownership decision (those routes no longer exist on this app).
#   Kept: the equity-curve half of test_hosted_snapshot_serves_profile_series_and_comparison
#   (still an EP051 route) and the static web-file assertion.
"""Regression proof for EP051's directory/equity-curve hosted parity."""
from datetime import datetime,timezone

from fastapi.testclient import TestClient

from app.config import Settings
from app.contracts import Snapshot,Strategy,snapshot_hash
from app.main import create_app
from app.repository import MemoryRepository


def _point(strategy_id,number,value,equity,drawdown):
    return {"strategy_id":strategy_id,"trade_id":f"t{number}","trade_number":number,"opened_at":f"2026-08-{number:02d}T08:00:00Z","observed_at":f"2026-08-{number:02d}T09:00:00Z","net_return":value,"cumulative_net_return":equity,"drawdown":drawdown}


def _snapshot_with_one_strategy():
    values=[2,-1,3];equity=peak=0;maximum_drawdown=0
    for value in values:
        equity+=value;peak=max(peak,equity);maximum_drawdown=min(maximum_drawdown,equity-peak)
    summary=Strategy(strategy_id="DNA_1",total_trades=3,wins=2,losses=1,breakevens=0,total_net_return=sum(values),win_rate=2/3,profit_factor=sum(value for value in values if value>0)/abs(sum(value for value in values if value<0)),max_drawdown_money=maximum_drawdown,evidence_start="2026-08-01T08:00:00Z",evidence_end="2026-08-03T09:00:00Z",quality_state="COLLECTING")
    equity=peak=0;series=[]
    for number,value in enumerate(values,1):
        equity+=value;peak=max(peak,equity);series.append(_point("DNA_1",number,value,equity,equity-peak))
    digest=snapshot_hash([summary],[],series);now=datetime.now(timezone.utc)
    return Snapshot(snapshot_id="dna-hosted-parity",source_watermark=now,generated_at=now,item_count=1,sha256=digest,items=[summary],intelligence_profiles=[],return_series=series)


def test_hosted_equity_curve_serves_period_scoped_points():
    repository=MemoryRepository();repository.promote(_snapshot_with_one_strategy())
    client=TestClient(create_app(repository=repository,settings=Settings(data_backend="memory")))
    assert client.get("/api/dna/strategies/DNA_1/equity-curve").json()["total_points"]==3
    period=client.get("/api/dna/strategies/DNA_1/equity-curve",params={"date_from":"2026-08-02","date_to":"2026-08-03"}).json()["points"]
    assert [item["trade_number"] for item in period]==[1,2]
    assert [item["equity"] for item in period]==[-1,2] and [item["drawdown"] for item in period]==[-1,0]


def test_source_metadata_renderers_apply_output_encoding():
    for path in ("web/index.html","web/strategy.html","web/builder.html"):
        source=open(path,encoding="utf-8").read()
        assert "const esc" in source and "descriptive_name" in source
