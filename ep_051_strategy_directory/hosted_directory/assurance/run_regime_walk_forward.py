"""Leakage-safe walk-forward evaluation on canonical strategy returns and ECB features."""
from __future__ import annotations

from collections import defaultdict
from bisect import bisect_right
from datetime import datetime,timedelta,timezone
import json,math
from pathlib import Path
import statistics
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from app.intelligence.regime import classify


def at(value):
    parsed=datetime.fromisoformat(str(value).replace("Z","+00:00"));return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def evaluate(train_days=14,test_days=5,minimum_samples=2,selection_size=10):
    market=json.loads((ROOT/"runtime"/"market_features.json").read_text(encoding="utf-8"));cache=json.loads((ROOT/"runtime"/"intelligence_profiles.json").read_text(encoding="utf-8"))
    labels=sorted((at(row["as_of"]),classify(row["features"])["state"]) for row in market["features"]);label_times=[row[0] for row in labels];trades=[]
    for strategy_id,points in cache["curves"].items():
        for point in points:
            timestamp=at(point["closed_at"]);label_index=bisect_right(label_times,timestamp)-1
            if label_index>=0:trades.append({"strategy_id":strategy_id,"at":timestamp,"day":timestamp.date(),"regime":labels[label_index][1],"return":float(point["net_return"])})
    days=sorted({trade["day"] for trade in trades});folds=[]
    for offset in range(train_days,len(days)-test_days+1,test_days):
        training_days=set(days[offset-train_days:offset]);testing_days=set(days[offset:offset+test_days]);training=[row for row in trades if row["day"] in training_days];testing=[row for row in trades if row["day"] in testing_days]
        scores=defaultdict(list)
        for row in training:scores[(row["regime"],row["strategy_id"])].append(row["return"])
        selected={}
        for regime in {row["regime"] for row in testing}:
            ranked=[(statistics.mean(values),strategy_id) for (state,strategy_id),values in scores.items() if state==regime and len(values)>=minimum_samples];selected[regime]={strategy_id for _,strategy_id in sorted(ranked,reverse=True)[:selection_size]}
        by_day=defaultdict(list);candidate_day=defaultdict(list)
        for row in testing:
            by_day[row["day"]].append(row["return"])
            if row["strategy_id"] in selected.get(row["regime"],set()):candidate_day[row["day"]].append(row["return"])
        baseline=sum(statistics.mean(values) for values in by_day.values());candidate=sum(statistics.mean(candidate_day[day]) if candidate_day[day] else 0 for day in sorted(testing_days))
        folds.append({"trained_from":min(training_days).isoformat(),"trained_through":max(training_days).isoformat(),"evaluated_from":min(testing_days).isoformat(),"evaluated_through":max(testing_days).isoformat(),"candidate_return":candidate,"baseline_return":baseline,"candidate_days":sum(bool(candidate_day[day]) for day in testing_days),"test_days":len(testing_days)})
    calibration=folds[:-2];holdout=folds[-2:];candidate=sum(row["candidate_return"] for row in holdout);baseline=sum(row["baseline_return"] for row in holdout);lift=candidate-baseline
    return {"generated_at":datetime.now(timezone.utc).isoformat(),"schema_version":"1.0.0","market_source":market["source"],"market_source_version":market["source_version"],"strategy_source":"sanitized combined_trades_closed intelligence cache","methodology":{"train_days":train_days,"test_days":test_days,"minimum_samples_per_regime":minimum_samples,"selection_size":selection_size,"selection":"top training-period mean net return within the point-in-time regime","baseline":"daily equal-weight mean across all strategies with closed trades","outcome":"signed net_return; costs and commission included","holdout":"last two chronological folds; calibration folds are reported but excluded from the release decision"},"calibration_folds":calibration,"holdout_folds":holdout,"folds":folds,"candidate_return":candidate,"baseline_return":baseline,"lift":lift,"positive_lift_folds":sum(row["candidate_return"]>row["baseline_return"] for row in holdout),"passed":len(holdout)==2 and lift>0 and all(row["trained_through"]<row["evaluated_from"] for row in folds),"limitations":["ECB reference rates are daily informational rates, not executable prices.","The available strategy cache bounds each model to its latest 1,000 closed trades.","A positive lift may mean a smaller loss than baseline; it is not necessarily a positive absolute return.","Results are decision-support evaluation, not a promise of future performance."]}


if __name__=="__main__":
    result=evaluate();target=ROOT/"evidence"/"regime_walk_forward_report.json";target.write_text(json.dumps(result,indent=2),encoding="utf-8");print(json.dumps({key:result[key] for key in ("passed","lift","candidate_return","baseline_return","positive_lift_folds")}|{"folds":len(result["folds"])}))
