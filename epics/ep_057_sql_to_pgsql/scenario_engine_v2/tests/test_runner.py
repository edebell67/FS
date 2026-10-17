# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_runner.py — the virtual race runner: cap (default 5, configurable), queueing, isolation, cancel, failure, no writes, live refusal.
#
# VERSION HISTORY
# v1.1.0 · 2026-10-17 · cap 8 by configuration alone, no look-ahead, live / order refusal.
# v1.0.0 · 2026-10-17 · Initial version.
import os
import sys
import threading
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine.instance import HeadlessLiveModeError  # noqa: E402
from runner import RaceConfig, RaceManager  # noqa: E402
from runner.manager import DEFAULT_MAX_CONCURRENT, HARD_LIMIT  # noqa: E402


def toy(model, nets, product="gbp"):
    return {"model": model, "product": product, "product_type": "forex", "strategy": "breakout", "color": "#112233", "win_rate": 50,
            "cum_net": nets[-1], "cum_alt_net": nets[-1],
            "series": [{"time": f"{h:02d}:00", "net": n, "buy": n, "sell": 0, "alt_net": n, "alt_buy": n, "alt_sell": 0} for h, n in enumerate(nets)]}


CURVES = {"DNA_1": [0, 10, 20, 30, 40], "DNA_2": [0, -5, 5, 25, 60], "DNA_3": [0, 15, 12, 18, 30], "DNA_4": [0, 1, 2, 3, 4]}


class FakeClient:
    """Stands in for the data client: no network. `gate` (an Event) holds a race at load time so tests can hold races open; `calls` records every method used."""

    def __init__(self, gate=None, fail=False):
        self.gate, self.fail, self.calls = gate, fail, []
        self.portfolio_models, self.criteria_data, self.trade_cache = [], {}, {}
        self.write_transport = None

    def fetch_portfolio_data(self, cache_key, date, key, background=False, portfolio_name=None):
        self.calls.append("fetch_portfolio_data")
        if self.gate is not None:
            assert self.gate.wait(30), "gate never opened"
        if self.fail:
            raise RuntimeError("data service unavailable")
        self.portfolio_models = [toy(m, CURVES[m]) for m in key.split(",") if m in CURVES]
        return {"models": self.portfolio_models}

    def refresh_live_data(self, target_date, **kw):
        """The scenario's leaders for the day (server order): DNA_3, DNA_4, DNA_1, DNA_2."""
        self.calls.append("refresh_live_data")
        if self.fail:
            raise RuntimeError("data service unavailable")
        scenario = f"{kw.get('criteria', 'top_net')}"
        self.criteria_data[scenario] = {target_date: [toy(m, CURVES[m]) for m in ("DNA_3", "DNA_4", "DNA_1", "DNA_2")]}
        return {"ok": True, "scenario": scenario, "url": "fake://live_day"}

    def send(self, *a, **k):  # pragma: no cover - must never be reached
        self.calls.append("SEND")
        raise AssertionError("a race must never write")


def cfg(name="r", models=("DNA_1", "DNA_2"), **kw):
    return RaceConfig(name=name, start_model=models[0], add_models=tuple(models[1:]), date="2026-10-14", **kw)


def test_default_cap_is_five_and_configurable(monkeypatch):
    monkeypatch.delenv("EP057_MAX_RACES", raising=False)
    assert DEFAULT_MAX_CONCURRENT == 5 and RaceManager().max_concurrent == 5
    monkeypatch.setenv("EP057_MAX_RACES", "9")
    assert RaceManager().max_concurrent == 9
    assert RaceManager(max_concurrent=3).max_concurrent == 3
    m = RaceManager()
    assert m.set_max_concurrent(12) == 12 and m.max_concurrent == 12
    with pytest.raises(ValueError):
        m.set_max_concurrent(0)
    assert m.set_max_concurrent(10_000) == HARD_LIMIT
    monkeypatch.setenv("EP057_MAX_RACES", "not-a-number")
    assert RaceManager().max_concurrent == 5


def test_never_more_than_the_cap_run_at_once_and_the_rest_queue():
    gate = threading.Event()
    clients = []

    def factory(config):
        c = FakeClient(gate)
        clients.append(c)
        return c

    mgr = RaceManager(max_concurrent=5, client_factory=factory)
    races = [mgr.submit(cfg(f"r{i}")) for i in range(8)]
    deadline = time.time() + 10
    while mgr.counts()["running"] < 5 and time.time() < deadline:
        time.sleep(0.02)
    c = mgr.counts()
    assert c["running"] == 5 and c["queued"] == 3, c
    gate.set()
    assert mgr.wait(30)
    assert [r.progress.state for r in races] == ["completed"] * 8
    assert mgr.counts()["completed"] == 8


def test_raising_the_cap_lets_queued_races_start():
    gate = threading.Event()
    mgr = RaceManager(max_concurrent=1, client_factory=lambda c: FakeClient(gate))
    for i in range(4):
        mgr.submit(cfg(f"r{i}"))
    time.sleep(0.2)
    assert mgr.counts()["running"] == 1
    mgr.set_max_concurrent(4)
    deadline = time.time() + 10
    while mgr.counts()["running"] < 4 and time.time() < deadline:
        time.sleep(0.02)
    assert mgr.counts()["running"] == 4
    gate.set()
    assert mgr.wait(30)


def test_parallel_results_equal_sequential_results():
    configs = [cfg("a", ("DNA_1", "DNA_2")), cfg("b", ("DNA_2", "DNA_3", "DNA_4")), cfg("c", ("DNA_3", "DNA_1")), cfg("d", ("DNA_4", "DNA_2", "DNA_1")),
               cfg("e", ("DNA_1",), return_type="ALT"), cfg("f", ("DNA_2", "DNA_4"), split_mode="TRI_SPLIT")]
    seq = []
    for c in configs:
        m = RaceManager(max_concurrent=1, client_factory=lambda cc: FakeClient())
        r = m.submit(c)
        assert m.wait(30)
        seq.append(r.result)
    par_mgr = RaceManager(max_concurrent=6, client_factory=lambda cc: FakeClient())
    par = [par_mgr.submit(c) for c in configs]
    assert par_mgr.wait(30)
    for s, p in zip(seq, par):
        assert p.progress.state == "completed"
        strip = lambda r: {k: v for k, v in r.items() if k != "race_id"}  # noqa: E731
        s2, p2 = strip(s), strip(p.result)
        s2["outputs"] = {k: v for k, v in s2["outputs"].items() if k != "instance_id"}
        p2["outputs"] = {k: v for k, v in p2["outputs"].items() if k != "instance_id"}
        assert s2 == p2


def test_race_content():
    mgr = RaceManager(client_factory=lambda c: FakeClient())
    r = mgr.submit(cfg("content", ("DNA_1", "DNA_2", "DNA_3")))
    assert mgr.wait(30)
    res = r.result
    assert res["frames"] == 5 and len(res["board"]) == 5
    assert res["board"][0]["leaders"][0]["model"] == "DNA_1"            # frame 0: everyone is at 0, ties break by id
    assert res["board"][1]["leaders"][0]["model"] == "DNA_3"            # frame 1: 10 / -5 / 15
    assert res["final"]["leader"] == "DNA_2" and res["final"]["standings"][0]["net"] == 60.0
    assert [x["model"] for x in res["final"]["standings"]] == ["DNA_2", "DNA_1", "DNA_3"]
    assert res["final"]["lead_changes"] == 3                            # leaders by frame: DNA_1, DNA_3, DNA_1, DNA_1, DNA_2
    assert [b["leaders"][0]["model"] for b in res["board"]] == ["DNA_1", "DNA_3", "DNA_1", "DNA_1", "DNA_2"]
    assert r.progress.frame == r.progress.frames == 5


def test_failure_is_reported_and_isolated():
    def factory(config):
        return FakeClient(fail=(config.name == "bad"))

    mgr = RaceManager(client_factory=factory)
    good, bad, good2 = mgr.submit(cfg("g1")), mgr.submit(cfg("bad")), mgr.submit(cfg("g2"))
    assert mgr.wait(30)
    assert [good.progress.state, bad.progress.state, good2.progress.state] == ["completed", "failed", "completed"]
    assert "data service unavailable" in bad.progress.error


def test_cancel_running_and_queued():
    gate = threading.Event()
    mgr = RaceManager(max_concurrent=1, client_factory=lambda c: FakeClient(gate))
    running, queued = mgr.submit(cfg("run")), mgr.submit(cfg("wait"))
    deadline = time.time() + 5
    while running.progress.state != "running" and time.time() < deadline:
        time.sleep(0.02)
    assert mgr.cancel(queued.race_id) is True and queued.progress.state == "cancelled"
    assert mgr.cancel(running.race_id) is True
    gate.set()
    assert mgr.wait(30)
    assert running.progress.state == "cancelled"
    assert mgr.cancel("nope") is False and mgr.cancel(running.race_id) is False


def test_virtual_only_no_writes_no_live():
    clients = []

    def factory(config):
        c = FakeClient()
        clients.append(c)
        return c

    mgr = RaceManager(client_factory=factory)
    mgr.submit(cfg("clean"))
    assert mgr.wait(30)
    assert all("SEND" not in c.calls and c.write_transport is None for c in clients)
    with pytest.raises(HeadlessLiveModeError):
        mgr.submit(RaceConfig(start_model="LIVE", date="2026-10-14"))
    with pytest.raises(HeadlessLiveModeError):
        mgr.submit(RaceConfig(start_model="DNA_1", add_models=("live_alt",), date="2026-10-14"))
    with pytest.raises(ValueError):
        mgr.submit(RaceConfig(start_model="DNA_1"))  # no date
    assert os.environ.get("EP057_ALLOW_LIVE") is None


def test_eight_run_at_once_by_configuration_alone(monkeypatch):
    """Plan step 2: raising the cap to 8 needs no code change (environment variable or set_max_concurrent)."""
    monkeypatch.setenv("EP057_MAX_RACES", "8")
    gate = threading.Event()
    mgr = RaceManager(client_factory=lambda c: FakeClient(gate))
    for i in range(10):
        mgr.submit(cfg(f"r{i}"))
    deadline = time.time() + 10
    while mgr.counts()["running"] < 8 and time.time() < deadline:
        time.sleep(0.02)
    assert mgr.counts()["running"] == 8 and mgr.counts()["queued"] == 2
    gate.set()
    assert mgr.wait(30)


def test_no_look_ahead_each_frame_uses_only_data_up_to_that_frame():
    """A race stopped at frame 3 reports exactly what the full race reported for frames 0..2 (nothing later can have leaked in)."""
    full_mgr = RaceManager(client_factory=lambda c: FakeClient())
    full = full_mgr.submit(cfg("full", ("DNA_1", "DNA_2", "DNA_3")))
    short_mgr = RaceManager(client_factory=lambda c: FakeClient())
    short = short_mgr.submit(cfg("short", ("DNA_1", "DNA_2", "DNA_3"), max_frames=3))
    assert full_mgr.wait(30) and short_mgr.wait(30)
    assert short.result["board"] == full.result["board"][:3]
    assert [b["time"] for b in short.result["board"]] == ["00:00", "01:00", "02:00"]  # the snapshot time of every decision is recorded


def test_headless_engine_refuses_live_activation_and_orders():
    from engine.instance import Engine, EngineSpec
    e = Engine(EngineSpec(date="2026-10-14"))
    with pytest.raises(HeadlessLiveModeError):
        e.activate_live("LIVE")
    with pytest.raises(HeadlessLiveModeError):
        e.place_order("BUY", 1)


def test_a_race_holds_at_most_twenty_strategies():
    mgr = RaceManager(client_factory=lambda c: FakeClient())
    twenty = tuple(f"DNA_{i}" for i in range(1, 21))
    mgr.submit(RaceConfig(start_model=twenty[0], add_models=twenty[1:], date="2026-10-14"))
    assert mgr.wait(30)
    with pytest.raises(ValueError, match="at most 20"):
        mgr.submit(RaceConfig(start_model="DNA_0", add_models=twenty, date="2026-10-14"))


def test_the_competition_can_be_built_from_configuration():
    """Start from one strategy and add the scenario's top N leaders: the race holds the start strategy first, then the leaders in server order, no duplicates."""
    mgr = RaceManager(client_factory=lambda c: FakeClient())
    r = mgr.submit(cfg("built", ("DNA_1",), add_scenario_top=3))
    assert mgr.wait(30)
    assert r.progress.state == "completed", r.progress.error
    # named DNA_1, then the top 3 leaders DNA_3, DNA_4, DNA_1 (a duplicate): the race holds DNA_1, DNA_3, DNA_4 in that order
    assert list(r.result["outputs"]["spec"]["models"]) == ["DNA_1", "DNA_3", "DNA_4"]
    assert [m["model"] for m in r.result["final"]["standings"]] == ["DNA_1", "DNA_3", "DNA_4"]   # final nets 40 / 30 / 4


def test_scenario_leaders_that_cannot_be_loaded_fail_the_race_only():
    mgr = RaceManager(client_factory=lambda c: FakeClient(fail=True))
    r = mgr.submit(cfg("broken", ("DNA_1",), add_scenario_top=2))
    assert mgr.wait(30) and r.progress.state == "failed"
    with pytest.raises(ValueError):
        mgr.submit(cfg("bad", ("DNA_1",), add_scenario_top=25))


def test_limit_must_be_a_value_the_data_service_serves():
    mgr = RaceManager(client_factory=lambda c: FakeClient())
    for bad in (1, 5, 15, 50):
        with pytest.raises(ValueError, match="10, 20 or 30"):
            mgr.submit(cfg("bad", limit=bad))
    mgr.submit(cfg("ok", limit=20))
    assert mgr.wait(30)
