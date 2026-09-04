# VERSION HISTORY
# v1.0.0 · 2026-08-24 · Golden, evaluation, monitoring and release-gate tests.
from app.intelligence.assurance import (OperationsMonitor,ReleaseGate,discovery_evaluation,
    ReleaseManager,metric_tolerance_report,rank_invariants,walk_forward_lift)
from app.intelligence.discovery import interpret


def test_metric_gate_fails_any_out_of_tolerance_value():
    assert metric_tolerance_report({"a":1.001},{"a":1},{"a":.01})["passed"] is True
    assert metric_tolerance_report({"a":1.1},{"a":1},{"a":.01})["passed"] is False


def test_discovery_exactness_and_rank_invariants_are_repeatable():
    cases=[{"id":"fx-win","query":"FX with win rate over 60%","expected":{"asset_class":"FX","min_win_rate":.6,"sort":"quality_score","direction":"desc","return_basis":"net_return"}}]
    assert discovery_evaluation(cases,interpret)["passed"] is True
    assert rank_invariants([{"suitability_score":90},{"suitability_score":80}])=={"descending":True,"bounded":True,"count":2}


def test_walk_forward_gate_rejects_leakage_and_requires_lift():
    leak=[{"trained_through":"2026-02-01","evaluated_from":"2026-01-01","candidate_return":2,"baseline_return":1}]
    clean=[{"trained_through":"2025-12-31","evaluated_from":"2026-01-01","candidate_return":2,"baseline_return":1}]
    assert walk_forward_lift(leak)["reason"]=="LEAKAGE"
    assert walk_forward_lift(clean)["passed"] is True


def test_operations_and_release_fail_closed_until_every_gate_passes():
    monitor=OperationsMonitor();monitor.observe(100);monitor.data_state("profiles",10,60);monitor.drift_state("quality",.51,.5,.05)
    assert monitor.report()["healthy"] is True
    gate=ReleaseGate();assert gate.decide({})["promote"] is False
    evidence={name:{"passed":True} for name in gate.REQUIRED};assert gate.decide(evidence)["promote"] is True
    evidence["security"]={"passed":False};assert gate.decide(evidence)["promote"] is False


def test_canary_requires_every_gate_and_rollback_restores_previous_version():
    manager=ReleaseManager();evidence={name:{"passed":True} for name in ReleaseGate.REQUIRED}
    manager.stage("v1",evidence,"canary");manager.promote("v1");manager.stage("v2",evidence,"canary");manager.promote("v2")
    assert manager.status()["active"]=="v2" and manager.rollback()["active"]=="v1"
    manager.stage("bad",{"metrics":{"passed":True}},"canary")
    try:manager.promote("bad")
    except ValueError:pass
    else:raise AssertionError("incomplete release evidence promoted")
