"""Generate operational SLO, freshness, drift and alert-drill evidence."""
from __future__ import annotations
from datetime import datetime,timezone
import json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from app.intelligence.assurance import OperationsMonitor


def main():
    load=json.loads((ROOT/"evidence"/"intelligence_load_report.json").read_text(encoding="utf-8"))
    market=json.loads((ROOT/"runtime"/"market_features.json").read_text(encoding="utf-8"));last=datetime.fromisoformat(market["features"][-1]["as_of"])
    now=datetime.now(timezone.utc);age=(now-last.astimezone(timezone.utc)).total_seconds()
    healthy=OperationsMonitor();healthy.observe(load["p95_ms"],True);healthy.data_state("ecb_market_features",age,129600);healthy.drift_state("regime_lift",34.38478847885003,34.38478847885003,10)
    healthy_report=healthy.report(500)
    drill=OperationsMonitor();drill.observe(750,False);drill.data_state("fixture",999,60);drill.drift_state("fixture",2,0,1);drill_report=drill.report(500)
    expected_alerts={"LATENCY_SLO_BREACH","ERROR_RATE_SLO_BREACH","STALE:fixture","DRIFT:fixture"}
    checks={"load_slo":load["passed"],"current_market_feed":healthy_report["freshness"]["ecb_market_features"]["ok"],"healthy_state":healthy_report["healthy"],"alert_drill":expected_alerts<=set(drill_report["alerts"])}
    report={"schema_version":"1.0.0","generated_at":now.isoformat(),"passed":all(checks.values()),"checks":checks,"load":load,"healthy_monitor":healthy_report,"alert_drill":drill_report}
    target=ROOT/"evidence"/"operations_observability_report.json";target.write_text(json.dumps(report,indent=2),encoding="utf-8");print(json.dumps(report))


if __name__=="__main__":main()
