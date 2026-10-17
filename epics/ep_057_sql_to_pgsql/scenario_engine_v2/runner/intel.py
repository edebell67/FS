# epics/ep_057_sql_to_pgsql/scenario_engine_v2/runner/intel.py — intelligence service for agents: on-demand reports and rule-based watches that queue events (proactive delivery).
#
# VERSION HISTORY
# v1.0.0 · 2026-10-17 · Initial version: build_report (data client -> engine.intelligence), WatchRegistry (top-N change, spread z threshold), event queue per agent, evaluate_all().
"""Lightweight on purpose: rules, not models. A watch re-reads the day's curves, builds the same report an agent could request, and queues an event when its trigger holds
(top-N membership changed, a pair's spread |z| crossed a threshold while widening or stretched). Agents pull their events and can answer by launching a race through /api/races."""
from __future__ import annotations

import threading
import time
import uuid
from collections import defaultdict, deque

from engine import data_client as dc
from engine import intelligence as intel

MAX_WATCHES_PER_AGENT = 20
MAX_EVENTS_PER_AGENT = 200


def load_models(client, *, date, models=(), scenario="top_net", return_type="NET", limit=10, product_type="all", product="all", strategy_family="all") -> list[dict]:
    if models:
        key = ",".join(models)
        client.fetch_portfolio_data(f"{date}|{key}", date, key, False)
        return list(client.portfolio_models)
    res = client.refresh_live_data(date, product_type=product_type, product=product, strategy_family=strategy_family, limit=limit, criteria=scenario, return_type=return_type)
    if not res.get("ok"):
        raise RuntimeError(f"live day unavailable: {res.get('url')}")
    return list(client.criteria_data.get(res["scenario"], {}).get(date, []))


def build_report(client_factory, spec: dict) -> dict:
    client = client_factory(spec)
    models = load_models(client, date=spec["date"], models=tuple(spec.get("models") or ()), scenario=spec.get("scenario", "top_net"), return_type=spec.get("return_type", "NET"),
                         limit=int(spec.get("limit", 10)))
    as_of = None
    if spec.get("as_of_time") and models:   # last snapshot at or before the requested time, never after
        times = [p["time"] for p in max(models, key=lambda m: len(m["series"]))["series"]]
        idx = [i for i, t in enumerate(times) if t <= spec["as_of_time"]]
        as_of = idx[-1] if idx else 0
    return intel.report(models, return_type=spec.get("return_type", "NET"), as_of_index=as_of, top_n=int(spec.get("top_n", 3)), window=int(spec.get("window", 48)),
                        corr_threshold=float(spec.get("corr_threshold", 0.7)), z_hi=float(spec.get("z_hi", 1.5)))


def default_factory(api_base: str):
    return lambda spec: dc.DataClient(dc.http_transport(), api_base, live_date=spec["date"])


class WatchRegistry:
    def __init__(self, client_factory, interval_s: float = 60.0):
        self.client_factory = client_factory
        self.watches: dict[str, dict] = {}
        self.events = defaultdict(lambda: deque(maxlen=MAX_EVENTS_PER_AGENT))
        self.interval_s = interval_s
        self._lock = threading.RLock()
        self._stop = threading.Event()
        self._thread = None

    def add(self, agent: str, spec: dict, triggers: dict) -> dict:
        with self._lock:
            if sum(1 for w in self.watches.values() if w["agent"] == agent) >= MAX_WATCHES_PER_AGENT:
                raise ValueError(f"at most {MAX_WATCHES_PER_AGENT} watches per agent")
            w = {"watch_id": uuid.uuid4().hex[:12], "agent": agent, "spec": spec, "triggers": triggers, "state": {"top": None}, "created_at": time.time()}
            self.watches[w["watch_id"]] = w
            return {k: v for k, v in w.items() if k != "state"}

    def remove(self, watch_id: str) -> bool:
        with self._lock:
            return self.watches.pop(watch_id, None) is not None

    def pull(self, agent: str, clear: bool = True) -> list[dict]:
        with self._lock:
            out = list(self.events[agent])
            if clear:
                self.events[agent].clear()
            return out

    def evaluate(self, watch_id: str) -> list[dict]:
        w = self.watches[watch_id]
        report = build_report(self.client_factory, w["spec"])
        t, st, new = w["triggers"], w["state"], []

        def event(kind, summary, evidence):
            new.append({"event_id": uuid.uuid4().hex[:12], "watch_id": watch_id, "kind": kind, "summary": summary, "as_of": report["as_of"], "confidence": report["confidence"],
                        "evidence": evidence, "caveats": report["caveats"], "created_at": time.time()})
        top_now = [r["model"] for r in report["top"]]
        if t.get("top_change") and st["top"] is not None and set(top_now) != set(st["top"]):
            event("top_change", f"top {len(top_now)} changed: {st['top']} -> {top_now}", {"before": st["top"], "after": top_now, "top": report["top"]})
        st["top"] = top_now
        z_min = t.get("spread_z")
        seen = st.setdefault("flagged", [])
        flagged_now = []
        for s in report["spread_signals"]:
            key = "|".join(s["pair"])
            hot = z_min is not None and abs(s["z"]) >= z_min and s["state"] in ("widening", "stretched")
            if hot:
                flagged_now.append(key)
                if key not in seen:
                    event("spread", f"{s['pair'][0]}/{s['pair'][1]} spread z={s['z']} ({s['state']})", s)
        st["flagged"] = flagged_now
        with self._lock:
            self.events[w["agent"]].extend(new)
        return new

    def evaluate_all(self) -> int:
        n = 0
        for wid in list(self.watches):
            try:
                n += len(self.evaluate(wid))
            except Exception:  # noqa: BLE001 - a broken watch must not stop the others
                continue
        return n

    def start(self):
        if self._thread:
            return

        def loop():
            while not self._stop.wait(self.interval_s):
                self.evaluate_all()
        self._thread = threading.Thread(target=loop, name="intel-watch", daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
