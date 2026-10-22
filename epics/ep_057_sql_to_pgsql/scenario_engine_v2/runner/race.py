# epics/ep_057_sql_to_pgsql/scenario_engine_v2/runner/race.py — one virtual strategy race: start from a strategy, add competitors, replay the day frame by frame on its own isolated Engine.
#
# VERSION HISTORY
# v1.4.0 · 2026-10-18 · the held leader comes from the engine's own leader rotation (the page's Top X hold rank + exit threshold): lead_changes counts its switches, raw_lead_changes keeps the every-#1-flip count, and each board frame carries held / held_rank once the race has finished.
# v1.3.0 · 2026-10-18 · self.board: every frame's leaderboard is published as it is computed, so a race can be watched live and replayed from frame 0.
# v1.2.0 · 2026-10-18 · add_scenario_top picks the top N leaders with DISTINCT final net (a leader whose net equals one already in the field is skipped and the next one is used); skipped ids are reported.
# v1.1.0 · 2026-10-17 · add_scenario_top: the competition can be built from configuration (named strategies + the top N leaders of a scenario).
# v1.0.1 · 2026-10-17 · the race's data client uses the race date as its live date (the scenario-leaders path needs one).
# v1.0.0 · 2026-10-17 · Initial version: RaceConfig, Race.run (load via the data client, replay every frame, per-frame leaderboard, final engine outputs), cancel + progress hooks; virtual only.
"""A race is read-only and virtual: it loads curves through the data client (GET only), replays them on a private Engine and reports. It never places orders, never writes to
PostgreSQL or the rule library (no write transport is ever set), and refuses live portfolios."""
from __future__ import annotations

import threading
import time
import uuid
from dataclasses import asdict, dataclass, field, replace

from engine import core_ported as core
from engine import data_client as dc
from engine.instance import Engine, EngineSpec, HeadlessLiveModeError

LIVE_PORTFOLIOS = ("LIVE", "LIVE_ALT")


class RaceCancelled(Exception):
    pass


@dataclass(frozen=True)
class RaceConfig:
    name: str = "race"
    start_model: str | None = None            # the strategy the race starts from (a DNA_… id)
    add_models: tuple = ()                    # strategies added to compete with it
    add_scenario_top: int = 0                 # ...plus the top N leaders of `scenario` on `date` (the competition is built from configuration)
    scenario: str = "top_net"                 # used when no models are named: the scenario's leaders for the date
    date: str = ""
    product_type: str = "all"
    product: str = "all"
    strategy_family: str = "all"
    return_type: str = "NET"
    limit: int = 10
    split_mode: str = "ALL_NET"
    baseline_index: int = 0
    exit_threshold: float = 0.0
    daily_target: float = 500.0
    hold_rank: int = 1
    overlay_rule_id: str | None = None        # an existing named overlay rule (read from the library, never written)
    max_frames: int | None = None             # stop early (None = the whole day)
    api_base: str = "http://127.0.0.1:8765"

    def models(self) -> tuple:
        ids = [m for m in ([self.start_model] if self.start_model else []) + list(self.add_models) if m]
        return tuple(dict.fromkeys(ids))

    def validate(self) -> None:
        if not self.date:
            raise ValueError("date is required")
        if any(str(m).upper() in LIVE_PORTFOLIOS for m in self.models()):
            raise HeadlessLiveModeError("live portfolios are not available to virtual races")
        if self.limit not in (10, 20, 30):
            raise ValueError("limit must be 10, 20 or 30 (what the data service serves)")
        if len(self.models()) > 20:
            raise ValueError("a race holds at most 20 strategies")
        if self.add_scenario_top < 0 or self.add_scenario_top > 19:
            raise ValueError("add_scenario_top must be 0..19")


@dataclass
class RaceProgress:
    state: str = "queued"           # queued | running | completed | failed | cancelled
    frame: int = 0
    frames: int = 0
    error: str | None = None
    started_at: float | None = None
    finished_at: float | None = None


@dataclass
class Race:
    config: RaceConfig
    race_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    progress: RaceProgress = field(default_factory=RaceProgress)
    result: dict | None = None
    created_at: float = field(default_factory=time.time)
    cancel_event: threading.Event = field(default_factory=threading.Event, repr=False)

    def summary(self) -> dict:
        p = self.progress
        return {"race_id": self.race_id, "name": self.config.name, "state": p.state, "frame": p.frame, "frames": p.frames,
                "pct": (round(100.0 * p.frame / p.frames, 1) if p.frames else 0.0), "error": p.error, "created_at": self.created_at,
                "started_at": p.started_at, "finished_at": p.finished_at, "config": asdict(self.config),
                "leader": (self.result or {}).get("final", {}).get("leader")}

    def cancel(self) -> None:
        self.cancel_event.set()

    def run(self, client_factory=None) -> dict:
        p = self.progress
        p.state, p.started_at = "running", time.time()
        try:
            self.config.validate()
            self.result = self._run(client_factory)
            p.state = "completed"
        except RaceCancelled:
            p.state = "cancelled"
        except Exception as e:  # noqa: BLE001 - reported on the race, never raised into the manager
            p.state, p.error = "failed", f"{type(e).__name__}: {e}"
        finally:
            p.finished_at = time.time()
        return self.summary()

    # ---- the race itself ----
    def _competitors(self, client) -> tuple:
        """The named strategies, then the scenario's top N leaders (server order) with DISTINCT final net, de-duplicated by id and capped at 20.
        A leader whose final net equals one already in the field is a duplicate outcome: it is skipped (and listed in self.skipped_duplicates) and the next leader takes its place.
        The start strategy counts as one of the N when it is itself a leader."""
        c = self.config
        ids = list(c.models())
        self.skipped_duplicates = []
        if c.add_scenario_top:
            res = client.refresh_live_data(c.date, product_type=c.product_type, product=c.product, strategy_family=c.strategy_family, limit=30,
                                           criteria=c.scenario, return_type=c.return_type)
            if not res.get("ok"):
                raise RuntimeError(f"scenario leaders unavailable: {res.get('url')}")
            leaders = client.criteria_data.get(res["scenario"], {}).get(c.date, [])
            net_key = core.metric_keys(c.return_type)["netKey"]
            seen, taken = set(), 0
            for m in leaders:
                if taken >= c.add_scenario_top:
                    break
                series = m.get("series") or []
                last = series[-1] if series else {}
                net = round(_num(last.get(net_key, last.get("net"))), 2)
                if net in seen:
                    self.skipped_duplicates.append({"model": m["model"], "net": net})
                    continue
                seen.add(net)
                taken += 1
                ids.append(m["model"])
        return tuple(dict.fromkeys(ids))[:20]

    def _run(self, client_factory) -> dict:
        c = self.config
        client = client_factory(c) if client_factory else dc.DataClient(dc.http_transport(), c.api_base, live_date=c.date)  # the live-day endpoint serves any date
        models = self._competitors(client)
        spec = EngineSpec(product_type=c.product_type, product=c.product, scenario=c.scenario, date=c.date, models=models,
                          models_only=bool(models), return_type=c.return_type, split_mode=c.split_mode, baseline_index=c.baseline_index,
                          exit_threshold=c.exit_threshold, daily_target=c.daily_target, hold_rank=c.hold_rank, strategy_family=c.strategy_family)
        if c.overlay_rule_id:
            library = client.load_overlay_rule_library()
            rule = next((r for r in library.get("rules", []) if r.get("id") == c.overlay_rule_id), None)
            if rule is None:
                raise ValueError(f"overlay rule {c.overlay_rule_id!r} not found")
            spec = replace(spec, overlay_rule=rule)
        engine = Engine(spec).load_from_client(client, limit=c.limit)
        total = engine.max_frames()
        frames = total if c.max_frames is None else max(1, min(total, int(c.max_frames)))
        self.progress.frames = frames
        board = self.board = []   # published frame by frame: the board endpoint serves it while the race runs
        keys = core.metric_keys(c.return_type)
        models = engine.eligible()
        longest = max(models, key=lambda m: len(m.get("series") or []), default={"series": []})["series"] if models else []
        for frame in range(frames):
            if self.cancel_event.is_set():
                raise RaceCancelled()
            rows = []
            for m in models:
                series = m.get("series") or []
                pt = series[min(frame, len(series) - 1)] if series else {}
                rows.append({"model": m["model"], "net": _num(pt.get(keys["netKey"], pt.get("net")))})
            rows.sort(key=lambda r: (-r["net"], r["model"]))
            board.append({"frame": frame, "time": longest[min(frame, len(longest) - 1)].get("time") if longest else None, "leaders": rows})
            self.progress.frame = frame + 1
        engine.configure(frame_index=frames - 1 if c.max_frames is not None else -1)
        outputs = engine.outputs()
        lead_changes = _apply_held_leader(board, outputs)
        final = board[-1]["leaders"] if board else []
        raw_lead_changes = sum(1 for a, b in zip(board, board[1:]) if a["leaders"] and b["leaders"] and a["leaders"][0]["model"] != b["leaders"][0]["model"])
        return {"race_id": self.race_id, "frames": frames, "board": board, "outputs": outputs,
                "skipped_duplicates": list(getattr(self, "skipped_duplicates", [])),
                "final": {"leader": final[0]["model"] if final else None, "standings": final, "lead_changes": lead_changes, "raw_lead_changes": raw_lead_changes,
                          "rotation_net": _rotation_net(outputs)}}


def _apply_held_leader(board: list, outputs: dict) -> int:
    """Mark every frame with the leader the page's own rotation logic is holding (held while within the hold rank, replaced by the net #1 once it drops out), and
    return the number of switches. Frames before the rotation's first entry have no held leader; the board frames are mutated in place."""
    trades = (outputs.get("rotation", {}).get("leader") or {}).get("trades") or []
    for fr in board:
        t = next((t for t in trades if t["entryIdx"] <= fr["frame"] and (t.get("isOpen") or fr["frame"] < t["exitIdx"])), None)
        held = t["model"] if t else None
        fr["held"] = held
        fr["held_rank"] = next((i + 1 for i, r in enumerate(fr["leaders"]) if r["model"] == held), None) if held else None
    return max(0, len(trades) - 1)


def _num(v) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def _rotation_net(outputs: dict):
    """Net result of the leader-rotation simulation (sum of its paired trades), None when the engine produced none."""
    trades = (outputs.get("rotation", {}).get("leader") or {}).get("trades") or []
    total = 0.0
    seen = False
    for t in trades:
        for k in ("net", "pnl", "result"):
            if isinstance(t, dict) and t.get(k) is not None:
                total += _num(t[k])
                seen = True
                break
    return round(total, 4) if seen else None
