"""Unit tests for the server-side port of the Top10 dashboard's client logic (parity was also checked against the page's own JS in node)."""
from app import dashboard_engine as eng


def _series(buys, sells):
    return [{"time": f"00:{5 * (i + 1):02d}", "net": b + s, "buy": b, "sell": s} for i, (b, s) in enumerate(zip(buys, sells))]


def test_base_point_zero_is_session_start():
    s = _series([50, 60], [0, 0])
    assert eng.base_point(s, 0)["buy"] == 0
    assert eng.base_point(s, 1)["buy"] == 60


def test_overlay_enters_buy_when_sell_flat_then_exits_below_threshold():
    s = _series([10, 30, 30, 5], [0, 0, 0, 0])
    base = eng.base_point(s, 0)
    sigs = eng.overlay_signals(s, base, exit_threshold=10)
    assert [x["type"] for x in sigs] == ["B", "X"]
    trades = eng.pair_overlay_trades(sigs, s, base)
    assert len(trades) == 1 and trades[0]["pnl"] == 5 - 10 and not trades[0]["isOpen"]


def test_target_signal_fires_when_open_pnl_reaches_target():
    s = _series([10, 700], [0, 0])
    base = eng.base_point(s, 0)
    sigs = eng.overlay_signals(s, base)
    hit = eng.split_target_signal(sigs, s, base, daily_target=500)
    assert hit and hit["idx"] == 1


def test_leader_rotation_switches_only_beyond_threshold():
    a = {"model": "A", "series": _series([10, 20, 21], [0, 0, 0])}
    b = {"model": "B", "series": _series([5, 15, 40], [0, 0, 0])}
    out = eng.leader_rotation([a, b], "net", 2, exit_threshold=10)
    assert [s["type"] for s in out["signals"]] == ["B", "X", "B"]
    assert out["trades"][-1]["model"] == "B" and out["trades"][-1]["isOpen"]


def test_scenario_candidates_filters_and_sorts():
    ms = [{"model": "a", "win_rate": 60, "cum_net": 5, "product_type": "forex", "product": "GBP", "strategy": "breakout_R_3"},
          {"model": "b", "win_rate": 40, "cum_net": 9, "product_type": "forex", "product": "GBP", "strategy": "breakout_3"},
          {"model": "c", "win_rate": 90, "cum_net": 7, "product_type": "crypto", "product": "BTC", "strategy": "breakout_3"}]
    assert [m["model"] for m in eng.scenario_candidates(ms, min_win_rate=50)] == ["c", "a"]
    assert [m["model"] for m in eng.scenario_candidates(ms, product_type="forex")] == ["b", "a"]
    assert [m["model"] for m in eng.scenario_candidates(ms, strategy_family="breakout_r")] == ["a"]
