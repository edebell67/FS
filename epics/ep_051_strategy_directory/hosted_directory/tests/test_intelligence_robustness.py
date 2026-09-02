# VERSION HISTORY
# v1.0.0 · 2026-08-24 · Behaviour, sensitivity, walk-forward and live divergence eligibility.
from app.intelligence.robustness import divergence_split_from_points,live_backtest_divergence,parameter_sensitivity,trade_behaviour,walk_forward,walk_forward_folds_from_points


def test_trade_behaviour_merges_overlapping_exposure_intervals():
    rows=[{"opened_at":f"2026-01-01T0{n}:00:00Z","closed_at":f"2026-01-01T0{n+2}:00:00Z"} for n in range(5)]
    result=trade_behaviour(rows)
    assert result["state"]=="VALID" and result["median_hold_minutes"]==120 and 0<result["exposure_fraction"]<=1


def test_robustness_metrics_never_present_valid_below_sample_minimum():
    assert parameter_sensitivity([{"score":1}])["state"]=="COLLECTING"
    assert live_backtest_divergence([1],[1])["state"]=="COLLECTING"
    assert walk_forward([{"train_end":"2026-01-02","test_start":"2026-01-01","test_return":1}])["state"]=="INVALID"


def test_parameter_and_walk_forward_valid_states_are_explainable():
    sensitivity=parameter_sensitivity([{"score":x} for x in (10,10.5,9.5,10.2,9.8)])
    folds=[{"train_end":f"2025-0{n}-28","test_start":f"2025-0{n+1}-01","test_return":n} for n in (1,2,3)]
    result=walk_forward(folds)
    assert sensitivity["state"]=="VALID" and sensitivity["stable"] is True
    assert result["state"]=="VALID" and result["positive_fold_rate"]==1


def test_walk_forward_folds_from_points_derives_chronological_leakage_free_folds():
    points=[{"closed_at":f"2026-01-{day:02d}T00:00:00Z","net_return":10 if day%2==0 else -1} for day in range(1,25)]
    folds=walk_forward_folds_from_points(points,folds=4)
    assert len(folds)==3
    for previous,current in zip(folds,folds[1:]):
        assert previous["test_start"]<current["test_start"]
    result=walk_forward(folds)
    assert result["state"]=="VALID"


def test_walk_forward_folds_from_points_collects_below_minimum():
    assert walk_forward_folds_from_points([{"closed_at":"2026-01-01T00:00:00Z","net_return":1}],folds=4)==[]


def test_divergence_split_from_points_halves_chronologically():
    points=[{"closed_at":f"2026-01-{day:02d}T00:00:00Z","net_return":-1} for day in range(1,21)]+[{"closed_at":f"2026-02-{day:02d}T00:00:00Z","net_return":5} for day in range(1,21)]
    backtest,live=divergence_split_from_points(points)
    assert len(backtest)==20 and len(live)==20
    result=live_backtest_divergence(backtest,live)
    assert result["state"]=="VALID" and result["alert"] is True


def test_divergence_split_from_points_collects_below_minimum():
    assert divergence_split_from_points([{"closed_at":"2026-01-01T00:00:00Z","net_return":1}]*10)==([],[])
