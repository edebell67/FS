# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_engine_basic.py — skeleton tests: import without DOM/network, isolation, live-mode refusal.
#
# VERSION HISTORY
# v1.6.0 · 2026-10-17 · the no-DOM / no-network import check runs in a fresh interpreter.
# v1.5.0 · 2026-10-17 · eligible() keeps the server's order like the page (no cum_net sort); the earlier expectation was wrong.
# v1.4.0 · 2026-10-17 · Selected-time cohort through the Engine.
# v1.3.0 · 2026-10-17 · DataClient URL builders (hourly / point-in-time) and Engine.load_from_client.
# v1.2.0 · 2026-10-17 · auto-top1 refresh and exact search unit test.
# v1.1.0 · 2026-10-17 · Replay controls, split-mode / return-type rules and available_dates (unit tests; available_dates is not differential-tested).
# v1.0.0 · 2026-10-16 · Initial version: 5 tests for the engine skeleton (task engine_core step 1).
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from engine import Engine, EngineSpec, HeadlessLiveModeError


def toy(model, nets, product="EURUSD"):
    series = [{"time": f"00:{i*5:02d}", "net": n, "buy": n, "sell": 0, "alt_net": n, "alt_buy": n, "alt_sell": 0,
               "open": 0, "trades": i, "wins": 0, "losses": 0, "win_rate": 50, "loss_rate": 50}
              for i, n in enumerate(nets)]
    return {"model": model, "product": product, "product_type": "forex", "strategy": "breakout", "color": "#fff",
            "cum_net": nets[-1], "buy_net": nets[-1], "sell_net": 0, "cum_alt_net": nets[-1], "win_rate": 50,
            "series": series}


DATA = [toy("DNA_1", [0, 10, 20, 30, 40]), toy("DNA_2", [0, -5, 5, 25, 60], product="GBPUSD")]


def test_imports_without_dom_or_network():
    """Checked in a fresh interpreter: the engine package must not pull in a browser, HTTP client or DOM library (other tests import the runner's web stack)."""
    import subprocess
    code = ("import sys; sys.path.insert(0, %r); import engine, engine.instance, engine.page, engine.rpc, engine.replay_models; "
            "bad = [m for m in ('js', 'pyodide', 'selenium', 'playwright', 'requests', 'httpx', 'fastapi') if m in sys.modules]; print(bad)" % str(ROOT))
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, encoding="utf-8")
    assert out.returncode == 0 and out.stdout.strip() == "[]", out.stdout + out.stderr


def test_eligible_and_ribbon():
    e = Engine(EngineSpec(date="2026-10-14")).load_models(DATA)
    # the page keeps the server's order (getScenarioCandidates does not re-sort; its own comment says so) - the old expectation of a cum_net sort was a port bug
    assert [m["model"] for m in e.eligible()] == ["DNA_1", "DNA_2"]
    r = e.ribbon()
    assert r["count"] == 2 and r["total"]["net"] == 100


def test_models_only_filter():
    e = Engine(EngineSpec(models=("DNA_1",), models_only=True)).load_models(DATA)
    assert [m["model"] for m in e.eligible()] == ["DNA_1"]


def test_instances_are_isolated():
    a = Engine(EngineSpec(models=("DNA_1",), models_only=True)).load_models(DATA)
    b = Engine(EngineSpec(models=("DNA_2",), models_only=True)).load_models(DATA)
    alone = Engine(EngineSpec(models=("DNA_1",), models_only=True)).load_models(DATA).outputs()
    b.outputs()
    a_out = a.outputs()
    for k in ("eligible", "ribbon", "overlay", "rotation"):
        assert a_out[k] == alone[k]
    a._models[0]["series"][0]["net"] = 999  # mutating one instance's data must not leak
    assert DATA[0]["series"][0]["net"] == 0
    assert b._models[0]["series"][0]["net"] != 999


def test_live_mode_refused():
    e = Engine().load_models(DATA)
    with pytest.raises(HeadlessLiveModeError):
        e.activate_live()
    with pytest.raises(HeadlessLiveModeError):
        e.place_order()


def test_replay_controls():
    e = Engine(EngineSpec(date="2026-10-14")).load_models(DATA)
    assert e.max_frames() == 5 and e.replay_head_time() == "00:20"
    assert e.step(1).spec.frame_index == 0            # the page adds delta to the raw -1 end-marker
    assert e.step(2).spec.frame_index == 2 and e.replay_head_time() == "00:10"
    assert e.step(100).spec.frame_index == 4          # clamped to the last frame
    assert e.step(-100).spec.frame_index == 0
    assert e.seek_to_pct(0.5).spec.frame_index == 2
    assert e.seek_to_pct(0.125).spec.frame_index == 1  # 0.5 rounds half up like Math.round
    assert Engine().max_frames() == 1 and Engine().replay_head_time() is None


def test_split_mode_and_return_type_rules():
    e = Engine(EngineSpec(scenario="top_net"))
    assert e.set_split_mode("TRI_SPLIT").spec.split_mode == "TRI_SPLIT"
    assert e.set_split_mode("BOGUS").spec.split_mode == "TRI_SPLIT"       # invalid modes are ignored
    e.set_return_type("ALT")
    assert (e.spec.return_type, e.spec.scenario) == ("ALT", "top_alt_net")
    e.set_return_type("NET")
    assert (e.spec.return_type, e.spec.scenario) == ("NET", "top_net")
    e.configure(scenario="top_win").set_return_type("ALT")
    assert e.spec.scenario == "top_win"                                   # only top_net / top_alt_net swap


def test_available_dates_unit():
    from datetime import datetime
    from engine import page_utils as pu
    d = pu.available_dates(datetime(2026, 10, 14, 9, 30))
    assert d[0] == {"id": "WEEK_OVERALL", "label": "Full Week"}
    assert [x["id"] for x in d[1:]] == ["2026-10-08", "2026-10-09", "2026-10-10", "2026-10-11", "2026-10-12", "2026-10-13", "2026-10-14"]
    assert d[1]["label"] == "Thu 8" and d[-1]["label"] == "Wed 14"


def test_auto_top1_refresh_and_exact_search():
    e = Engine(EngineSpec(date="2026-10-14")).load_models(DATA)
    e.auto_top1.request_at, e.auto_top1.enabled, e.auto_top1.interval_minutes = "00:10", True, 15
    out = e.finish_auto_top1_refresh("00:10")
    assert out["status"] == "On · checked 00:10 · next at 00:25" and out["sched"] == "00:20" and out["requestAt"] is None
    assert e.finish_auto_top1_refresh("00:10")["status"] is None          # nothing in flight any more
    assert e.exact_search_model("dna_2")["model"] == "DNA_2"
    assert e.exact_search_model("dna_1, dna_2") is None and e.exact_search_model("nope") is None


def test_data_client_url_builders_and_engine_loader():
    from engine import data_client as dc

    class T:
        def __init__(self, fx):
            self.fx, self.calls = fx, []

        def __call__(self, url):
            self.calls.append(url)
            return self.fx.get(url, (404, {"error": "nf"}))

    cl = dc.DataClient(None, "http://api", live_date="2026-10-17")
    # URL shapes taken from the page's source (hourly report, point-in-time, hours)
    assert cl.hourly_report_url("2026-10-14", "forex", "all", "breakout", 60) == \
        "http://api/api/hourly_family_report?date=2026-10-14&product_type=forex&product=all&family=breakout&interval_minutes=60"
    opts = {"scenario": "top_net", "return_type": "NET", "product_type": "forex", "product": "all", "strategy_family": "all", "limit": 10, "min_win_rate": 0}
    assert cl.point_in_time_url("2026-10-14", "23:55", opts) == \
        "http://api/api/point_in_time_scenario?date=2026-10-14&at=23%3A55&scenario=top_net&return_type=NET&product_type=forex&product=all&strategy_family=all&limit=10&min_win_rate=0&rank_direction=top"
    assert cl.point_in_time_url("2026-10-14", "23:55", opts, "bottom", 2).endswith("&rank_direction=bottom&rank_position=2")
    assert cl.point_in_time_hours_url("2026-10-14", opts) == \
        "http://api/api/point_in_time_scenario_hours?date=2026-10-14&scenario=top_net&return_type=NET&product_type=forex&product=all&strategy_family=all&limit=10&min_win_rate=0"
    # the Engine loads a day through the data layer
    day = {"top_net": DATA, "products": ["eurusd", "gbpusd"]}
    tr = T({cl.live_day_url("2026-10-14", "forex", "all", "all", 10, "top_net", "NET"): (200, day)})
    e = Engine(EngineSpec(date="2026-10-14", product_type="forex")).load_from_client(dc.DataClient(tr, "http://api", live_date="2026-10-17"))
    assert [m["model"] for m in e.eligible()] == ["DNA_1", "DNA_2"] and len(tr.calls) == 1
    tr2 = T({f"http://api/api/portfolio_day?date=2026-10-14&models=DNA_1": (200, {"models": [DATA[0]], "generated_at": "2026-10-14T10:00:00"})})
    e2 = Engine(EngineSpec(date="2026-10-14", models=("DNA_1",), models_only=True)).load_from_client(dc.DataClient(tr2, "http://api"))
    assert [m["model"] for m in e2.eligible()] == ["DNA_1"]


def test_selected_time_cohort_through_the_engine():
    from engine import data_client as dc

    class T:
        def __init__(self, fx):
            self.fx, self.calls = fx, []

        def __call__(self, url):
            self.calls.append(url)
            return self.fx.get(url, (404, {"error": "nf"}))

    e = Engine(EngineSpec(date="2026-10-14", product_type="forex", scenario="top_net")).load_models(DATA)
    probe = dc.DataClient(None, "http://api")
    opts = {"scenario": "top_net", "return_type": "NET", "product_type": "forex", "product": "all", "strategy_family": "all", "limit": 10, "min_win_rate": 0}
    url = probe.point_in_time_url("2026-10-14", "00:20", opts)
    ranked = [{**DATA[1], "color": "#111111"}, {**DATA[0], "color": "#222222"}]
    tr = T({url: (200, {"models": ranked, "at_time": "00:20"})})
    out = e.refresh_selected_time(dc.DataClient(tr, "http://api"), rank_count=2)
    assert out["ran"] and tr.calls == [url]
    assert [m["model"] for m in e.selected.models] == ["DNA_2", "DNA_1"]
    assert e.selected.models[0]["comparisonRole"] == "as-of #1" and e.selected.status == "00:20 · 2 selected"
    assert e.refresh_selected_time(dc.DataClient(tr, "http://api"), rank_count=2)["ran"] is False  # identical request is skipped
    e.auto_top1.request_at = "00:20"   # automatic add of the top-1: retained in the chart history
    e.selected.requested_key = ""
    url2 = probe.point_in_time_url("2026-10-14", "00:20", opts, "top", 1)
    tr2 = T({url2: (200, {"models": ranked, "at_time": "00:20"})})
    e.refresh_selected_time(dc.DataClient(tr2, "http://api"))
    assert e.selected.models[0]["comparisonRole"] == "selected-time #1" and "DNA_2" in e.selected.history
