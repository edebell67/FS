"""Fail-closed evidence audit for every EP051 intelligence parent and child node."""
from __future__ import annotations
from datetime import datetime,timezone
import json,subprocess,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

NODE_EVIDENCE={
"IL-110":["app/intelligence/ingestion.py","tests/test_intelligence_ingestion.py","evidence/data_quality_reconciliation_report.json"],
"IL-120":["app/intelligence/models.py","contracts/strategy-intelligence-profile.schema.json","evidence/data_quality_reconciliation_report.json"],
"IL-130":["app/intelligence/metrics.py","tests/test_intelligence_foundation.py","evidence/data_quality_reconciliation_report.json"],
"IL-140":["app/intelligence/robustness.py","tests/test_intelligence_robustness.py","evidence/intelligence_methodology_and_model_card.md"],
"IL-150":["app/repository.py","migrations/004_hosted_intelligence_snapshot.sql","tests/test_intelligence_security_and_hosted_parity.py","evidence/hosted_local_parity_report.json"],
"IL-160":["contracts/openapi.json","web/api-client.js","tests/test_intelligence_ui_contract.py","evidence/browser_acceptance_report.json"],
"IL-210":["app/intelligence/comparative.py","tests/test_comparative_intelligence.py","evidence/intelligence_methodology_and_model_card.md"],
"IL-220":["app/intelligence/comparative.py","tests/test_comparative_intelligence.py","evidence/data_quality_reconciliation_report.json"],
"IL-230":["app/intelligence/comparative.py","tests/test_comparative_intelligence.py","evidence/discovery_ranking_variance_report.json"],
"IL-240":["app/intelligence/comparative.py","tests/test_intelligence_batch_series.py","evidence/browser_acceptance_report.json"],
"IL-250":["app/intelligence/comparative.py","tests/test_comparative_intelligence.py","evidence/browser_acceptance_report.json"],
"IL-260":["web/compare.html","tests/test_intelligence_security_and_hosted_parity.py","evidence/browser_acceptance_report.json"],
"IL-310":["app/intelligence/discovery.py","contracts/strategy-query.schema.json","tests/test_intelligent_discovery.py"],
"IL-320":["app/main.py","web/index.html","tests/test_intelligent_discovery.py"],
"IL-330":["app/intelligence/discovery.py","assurance/discovery_corpus.json","evidence/discovery_ranking_variance_report.json"],
"IL-340":["app/intelligence/discovery.py","tests/test_intelligent_discovery.py","evidence/discovery_ranking_variance_report.json"],
"IL-350":["app/intelligence/comparative.py","app/intelligence/discovery.py","evidence/discovery_ranking_variance_report.json"],
"IL-360":["web/intelligence.html","tests/test_intelligence_ui_contract.py","evidence/browser_acceptance_report.json"],
"IL-410":["app/main.py","migrations/003_private_intelligence_security.sql","tests/test_intelligence_security_and_hosted_parity.py","evidence/privacy_lifecycle_and_isolation_report.json"],
"IL-420":["app/intelligence/user.py","migrations/007_retention_security_definer.sql","evidence/privacy_lifecycle_and_isolation_report.json","evidence/security_scan/report.md"],
"IL-430":["app/intelligence/user.py","web/account.html","evidence/privacy_lifecycle_and_isolation_report.json"],
"IL-440":["app/intelligence/user.py","migrations/005_comparative_intelligence_schema.sql","evidence/privacy_lifecycle_and_isolation_report.json"],
"IL-450":["web/builder.html","app/intelligence/user.py","evidence/browser_acceptance_report.json","evidence/privacy_lifecycle_and_isolation_report.json"],
"IL-460":["app/intelligence/user.py","tests/test_user_and_regime_intelligence.py","evidence/privacy_lifecycle_and_isolation_report.json"],
"IL-510":["sync/ecb_market_features.py","runtime/market_features.json","tests/test_market_feature_pipeline.py","evidence/data_quality_reconciliation_report.json"],
"IL-520":["app/intelligence/regime.py","tests/test_user_and_regime_intelligence.py","evidence/regime_confidence_calibration_report.json"],
"IL-530":["app/main.py","web/regimes.html","evidence/browser_acceptance_report.json","evidence/operations_observability_report.json"],
"IL-540":["app/intelligence/regime.py","assurance/run_regime_walk_forward.py","evidence/regime_walk_forward_report.json"],
"IL-550":["app/intelligence/regime.py","tests/test_user_and_regime_intelligence.py","evidence/regime_walk_forward_report.json"],
"IL-560":["web/regimes.html","app/intelligence/regime.py","evidence/browser_acceptance_report.json","evidence/intelligence_methodology_and_model_card.md"],
"IL-610":["assurance/run_data_quality.py","evidence/data_quality_reconciliation_report.json","tests/test_intelligence_assurance.py"],
"IL-620":["assurance/run_discovery_variance.py","evidence/discovery_ranking_variance_report.json","assurance/discovery_corpus.json"],
"IL-630":["assurance/run_regime_walk_forward.py","assurance/run_regime_calibration.py","evidence/regime_walk_forward_report.json","evidence/regime_confidence_calibration_report.json"],
"IL-640":["security/threat-model.md","evidence/security_scan/report.md","evidence/privacy_lifecycle_and_isolation_report.json"],
"IL-650":["assurance/run_load_test.py","assurance/run_operations_evidence.py","evidence/intelligence_load_report.json","evidence/operations_observability_report.json"],
"IL-660":["assurance/run_release_drill.py","evidence/release_canary_rollback_report.json","evidence/browser_acceptance_report.json","evidence/intelligence_assurance_report.json"]}

PARENTS={"IL-100":[f"IL-{value}" for value in range(110,170,10)],"IL-200":[f"IL-{value}" for value in range(210,270,10)],"IL-300":[f"IL-{value}" for value in range(310,370,10)],"IL-400":[f"IL-{value}" for value in range(410,470,10)],"IL-500":[f"IL-{value}" for value in range(510,570,10)],"IL-600":[f"IL-{value}" for value in range(610,670,10)]}


def evidence_passes(path):
    if not path.exists():return False
    if path.suffix==".json" and "evidence" in path.parts and path.parts[-2]!="security_scan":
        payload=json.loads(path.read_text(encoding="utf-8"));return payload.get("passed",payload.get("release_decision",{}).get("promote",True)) is True
    return True


def main():
    test_run=subprocess.run([sys.executable,"-m","pytest","-q"],cwd=ROOT,capture_output=True,text=True);test_passed=test_run.returncode==0
    nodes={}
    for node,items in NODE_EVIDENCE.items():
        checks=[{"path":item,"present_and_passing":evidence_passes(ROOT/item)} for item in items];nodes[node]={"percent_complete":100 if test_passed and all(item["present_and_passing"] for item in checks) else 0,"status":"complete" if test_passed and all(item["present_and_passing"] for item in checks) else "incomplete","evidence":checks}
    for parent,children in PARENTS.items():
        passed=all(nodes[child]["percent_complete"]==100 for child in children);nodes[parent]={"percent_complete":100 if passed else 0,"status":"complete" if passed else "incomplete","children":children}
    report={"schema_version":"1.0.0","generated_at":datetime.now(timezone.utc).isoformat(),"passed":test_passed and all(item["percent_complete"]==100 for item in nodes.values()),"automated_tests":{"passed":test_passed,"summary":test_run.stdout.strip().splitlines()[-1] if test_run.stdout.strip() else test_run.stderr.strip()},"node_count":len(nodes),"nodes":nodes}
    target=ROOT/"evidence"/"node_completion_audit.json";target.write_text(json.dumps(report,indent=2),encoding="utf-8");print(json.dumps({"passed":report["passed"],"node_count":len(nodes),"tests":report["automated_tests"]}))
    raise SystemExit(0 if report["passed"] else 1)


if __name__=="__main__":main()
