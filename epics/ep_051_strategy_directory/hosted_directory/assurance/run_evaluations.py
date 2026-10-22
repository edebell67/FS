"""Generate the repeatable EP051 intelligence assurance evidence bundle."""
from __future__ import annotations
from datetime import datetime,timezone
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from app.intelligence.assurance import ReleaseGate,discovery_evaluation,metric_tolerance_report,walk_forward_lift
from app.intelligence.discovery import interpret
from app.intelligence.metrics import calculate

def main():
    corpus=json.loads((ROOT/"assurance"/"discovery_corpus.json").read_text(encoding="utf-8"));discovery=discovery_evaluation(corpus,interpret);variance=json.loads((ROOT/"evidence"/"discovery_ranking_variance_report.json").read_text(encoding="utf-8"));discovery["variance_and_protected_slices_passed"]=variance["passed"];discovery["passed"]=discovery["passed"] and variance["passed"]
    metrics=metric_tolerance_report(calculate([10,-5,20]),{"total_return":25,"win_rate":2/3,"profit_factor":6},{"total_return":1e-12,"win_rate":1e-12,"profit_factor":1e-12})
    regime_report=json.loads((ROOT/"evidence"/"regime_walk_forward_report.json").read_text(encoding="utf-8"));calibration_report=json.loads((ROOT/"evidence"/"regime_confidence_calibration_report.json").read_text(encoding="utf-8"));regime={"passed":regime_report["passed"] and calibration_report["passed"],"lift":regime_report["lift"],"candidate":regime_report["candidate_return"],"baseline":regime_report["baseline_return"],"periods":len(regime_report["holdout_folds"]),"calibration_error":calibration_report["holdout_mean_absolute_calibration_error"],"basis":"chronological walk-forward and confidence holdouts"}
    security_findings=json.loads((ROOT/"evidence"/"security_scan"/"findings.json").read_text(encoding="utf-8"));security_manifest=json.loads((ROOT/"evidence"/"security_scan"/"scan-manifest.json").read_text(encoding="utf-8"));security={"passed":len(security_findings.get("findings",[]))==0,"scan_id":security_manifest["scan"]["id"],"finding_count":len(security_findings.get("findings",[]))}
    operations_report=json.loads((ROOT/"evidence"/"operations_observability_report.json").read_text(encoding="utf-8"));operations={"passed":operations_report["passed"],"p95_ms":operations_report["load"]["p95_ms"],"requests":operations_report["load"]["requests"]}
    release_report=json.loads((ROOT/"evidence"/"release_canary_rollback_report.json").read_text(encoding="utf-8"));restore={"passed":release_report["checks"]["rollback_restored_predecessor"],"basis":"shadow/canary/promotion/rollback drill"}
    browser_report=json.loads((ROOT/"evidence"/"browser_acceptance_report.json").read_text(encoding="utf-8"));acceptance={"passed":browser_report["passed"],"pages":len(browser_report["pages"]),"console_errors":len(browser_report["console_errors"])}
    evidence={"metrics":metrics,"discovery":discovery,"regime":regime,"security":security,"operations":operations,"restore":restore,"acceptance":acceptance};decision=ReleaseGate().decide(evidence)
    report={"generated_at":datetime.now(timezone.utc).isoformat(),"schema_version":"1.0.0","evidence":evidence,"release_decision":decision}
    target=ROOT/"evidence"/"intelligence_assurance_report.json";target.parent.mkdir(exist_ok=True);target.write_text(json.dumps(report,indent=2),encoding="utf-8");print(json.dumps({"report":str(target),"promote":decision["promote"],"discovery_exact_match":discovery["exact_match"]}))


if __name__=="__main__":main()
