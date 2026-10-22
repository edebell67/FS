"""Promote sampled local intelligence evidence into the hosted contract and reconcile outputs."""
from __future__ import annotations
from datetime import datetime,timezone
import json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from app.contracts import IntelligenceReturnPoint,Snapshot,Strategy,snapshot_hash
from app.intelligence.models import StrategyIntelligenceProfile
from app.repository import MemoryRepository,rebase_equity_rows


def main():
    local=json.loads((ROOT/"runtime"/"intelligence_profiles.json").read_text(encoding="utf-8"));by_id={item["identity"]["strategy_id"]:item for item in local["profiles"]};sample=sorted(by_id)[:3]
    items=[];profiles=[];series=[]
    for strategy_id in sample:
        profile=by_id[strategy_id];curve=local["curves"][strategy_id];values=[float(row["net_return"]) for row in curve];wins=sum(value>0 for value in values);losses=sum(value<0 for value in values);breakevens=len(values)-wins-losses;gross_profit=sum(value for value in values if value>0);gross_loss=abs(sum(value for value in values if value<0));instrument=(profile["classification"].get("instruments") or [None])[0]
        items.append(Strategy(strategy_id=strategy_id,descriptive_name=profile["identity"].get("name"),product_name=instrument,market=profile["classification"]["asset_class"],total_trades=len(values),wins=wins,losses=losses,breakevens=breakevens,total_net_return=sum(values),win_rate=wins/len(values),profit_factor=None if gross_loss==0 else gross_profit/gross_loss,max_drawdown_money=min(float(row["drawdown"]) for row in curve),evidence_start=min(row.get("opened_at") or row["closed_at"] for row in curve),evidence_end=max(row["closed_at"] for row in curve),quality_state=profile["evidence"]["quality_state"] if profile["evidence"]["quality_state"] in {"VALID","COLLECTING","STALE"} else "COLLECTING"));profiles.append(profile)
        for row in curve:series.append(IntelligenceReturnPoint(strategy_id=strategy_id,trade_id=f"{strategy_id}:{int(row['trade_number']):08d}",trade_number=row["trade_number"],opened_at=row.get("opened_at"),observed_at=row["closed_at"],net_return=row["net_return"],cumulative_net_return=row["equity"],drawdown=row["drawdown"]))
    now=datetime.now(timezone.utc);snap=Snapshot(snapshot_id="parity-proof-v1",source_watermark=now,generated_at=now,item_count=len(items),sha256=snapshot_hash(items,profiles,series),items=items,intelligence_profiles=profiles,return_series=series);repo=MemoryRepository();repo.promote(snap)
    def curve_signature(rows):return [{"trade_number":row["trade_number"],"closed_at":datetime.fromisoformat(str(row["closed_at"]).replace("Z","+00:00")).isoformat(),"net_return":round(float(row["net_return"]),8),"equity":round(float(row["equity"]),8),"drawdown":round(float(row["drawdown"]),8)} for row in rows]
    checks=[]
    for strategy_id in sample:
        local_profile=by_id[strategy_id];hosted_profile=next(item for item in repo.current_profiles() if item["identity"]["strategy_id"]==strategy_id);curve=local["curves"][strategy_id];start=datetime.fromisoformat(curve[-min(5,len(curve))]["closed_at"].replace("Z","+00:00"));hosted_period=repo.current_equity_curve(strategy_id,start,None);local_period=rebase_equity_rows([row for row in curve if datetime.fromisoformat(row["closed_at"].replace("Z","+00:00"))>=start]);profile_equal=StrategyIntelligenceProfile.model_validate(hosted_profile).model_dump(mode="json")==StrategyIntelligenceProfile.model_validate(local_profile).model_dump(mode="json");checks.append({"strategy_id":strategy_id,"profile_equal":profile_equal,"period_curve_equal":curve_signature(hosted_period)==curve_signature(local_period),"points":len(hosted_period)})
    passed=all(item["profile_equal"] and item["period_curve_equal"] for item in checks)
    report={"schema_version":"1.0.0","generated_at":now.isoformat(),"passed":passed,"sample_size":len(sample),"sample_strategy_ids":sample,"snapshot_digest":snap.sha256,"checks":checks,"basis":"The same content-addressed local profile/series payload was promoted through the hosted Snapshot and repository contract; sampled period curves were independently rebased before comparison."}
    target=ROOT/"evidence"/"hosted_local_parity_report.json";target.write_text(json.dumps(report,indent=2),encoding="utf-8");print(json.dumps(report))


if __name__=="__main__":main()
