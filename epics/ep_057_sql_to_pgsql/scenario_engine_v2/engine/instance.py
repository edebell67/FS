# epics/ep_057_sql_to_pgsql/scenario_engine_v2/engine/instance.py — isolated, headless Engine instance over the ported page logic.
#
# VERSION HISTORY
# v1.9.1 · 2026-10-17 · rotation(kind, visible): the overlay candidates are the visible models, like drawChart's activeModels.
# v1.9.0 · 2026-10-17 · pit_mode: after refresh_selected_time the engine shows the selected-time cohort (pointInTimeMode), like the page's default view of a past date.
# v1.8.0 · 2026-10-17 · eligible / max_frames / replay_head_time are the page's own getEligibleModels / getMaxFrames / pointInTimeAtReplayHead (replay_models, differential-tested); `models` without models_only are pinned comparison models; ribbon_view().
# v1.7.0 · 2026-10-17 · refresh_selected_time (selected-time cohort via the data layer); Engine.selected state.
# v1.6.0 · 2026-10-17 · load_from_client (live_day / portfolio_day / source trades via the data layer).
# v1.5.0 · 2026-10-17 · auto_top1 state, finish_auto_top1_refresh, exact_search_model.
# v1.4.0 · 2026-10-17 · max_frames, replay_head_time, step, seek_to_pct, set_split_mode, set_return_type (over page_utils).
# v1.3.0 · 2026-10-16 · Assigned overlay rules: EngineSpec.overlay_rule / rule_eligible_fallthrough / live_date / now_ms, Engine.load_trade_cache; rotation passes a RuleContext.
# v1.2.0 · 2026-10-16 · PORTED_FROM_PAGE_VERSION now means last-verified version (v2.65.27) for the ported subset, after the differential test passed on v2.65.24 and v2.65.27.
# v1.1.0 · 2026-10-16 · EngineSpec.hold_rank; rotation passes the longest series as replay series (matches the page's call), using the page-faithful rotation functions.
# v1.0.0 · 2026-10-16 · Initial version: EngineSpec + Engine (load models, eligibility, ribbon, overlay signals/trades, rotation, outputs) over core_ported; live mode is refused for headless instances.
"""One Engine = one isolated race/view. No DOM, no network, no database: data is handed in via load_models()."""
from __future__ import annotations

import copy
import types
import uuid
from collections import OrderedDict
from dataclasses import asdict, dataclass, field, replace

from . import core_ported as core
from . import page_utils as pu
from . import replay_models as rm
from . import selected_time as stm
from .page_state import PageState

# Page version the ported functions were last VERIFIED against by tools/diff_js_vs_py.py (only the functions marked ported / ported_partial
# in engine_map.json; most of the page is still unported). check_drift.py compares this with the page header.
PORTED_FROM_PAGE_VERSION = "v2.65.32"


class HeadlessLiveModeError(RuntimeError):
    """Raised when a headless instance is asked to place orders or enter live mode."""


@dataclass(frozen=True)
class EngineSpec:
    """Mirror of the page's URL/state parameters that drive computation."""
    product_type: str = "all"
    product: str = "all"
    scenario: str = "top_net"
    date: str = ""
    models: tuple[str, ...] = ()
    models_only: bool = False
    return_type: str = "NET"
    split_mode: str = "ALL_NET"
    min_win_rate: float = 0.0
    strategy_family: str = "all"
    baseline_index: int = 0
    baseline_time: str | None = None
    frame_index: int = -1
    exit_threshold: float = 0.0
    daily_target: float = 500.0
    hold_rank: int = 1  # page overlayTopX
    overlay_rule: dict | None = None  # assigned overlay rule record {id, name, config}; None = generic rotation
    rule_eligible_fallthrough: bool = True  # see core_ported.RuleContext: the page as written has its rule eligibility filter return false
    live_date: str = ""  # the page's LIVE_DATE; trade-cache entries older than 5 min are stale only on this date
    now_ms: float = 0


@dataclass
class Engine:
    spec: EngineSpec = field(default_factory=EngineSpec)
    instance_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    _models: list[dict] = field(default_factory=list, repr=False)
    _trade_cache: dict = field(default_factory=dict, repr=False)
    auto_top1: pu.AutoTop1State = field(default_factory=pu.AutoTop1State, repr=False)
    selected: stm.SelectedTimeState = field(default_factory=stm.SelectedTimeState, repr=False)
    pit_mode: bool = False   # the page's pointInTimeMode: set by refresh_selected_time; eligible() then shows the selected-time cohort

    # ---- state ----
    def load_models(self, models: list[dict]) -> "Engine":
        """Deep copy so no instance can see or mutate another instance's (or the caller's) data."""
        self._models = copy.deepcopy(list(models))
        return self

    def load_from_client(self, client, *, limit: int = 10) -> "Engine":
        """Fill the engine's models from the API. models_only + models -> those strategies' day curves (portfolio_day);
        otherwise the scenario's cohort for the date (live_day). Source trades for an assigned rule are fetched too."""
        s = self.spec
        if s.models_only and s.models:
            key = ",".join(s.models)
            client.fetch_portfolio_data(f"{s.date}|{key}", s.date, key, False)
            self.load_models(client.portfolio_models)
        else:
            res = client.refresh_live_data(s.date, product_type=s.product_type, product=s.product, strategy_family=s.strategy_family,
                                           limit=limit, criteria=s.scenario, return_type=s.return_type)
            if not res.get("ok"):
                raise RuntimeError(f"live day unavailable: {res.get('url')}")
            self.load_models(client.criteria_data.get(res["scenario"], {}).get(s.date, []))
        if s.overlay_rule is not None:
            client.ensure_trade_data([m["model"] for m in self._models], s.date, s.product_type, s.product)
            self.load_trade_cache(client.trade_cache)
        return self

    def load_trade_cache(self, cache: dict) -> "Engine":
        """Per-model source trades for assigned-rule results: {"date|product_type|product|model": {"rows": [...], "cachedAt": ms}}."""
        self._trade_cache = copy.deepcopy(dict(cache))
        return self

    def configure(self, **changes) -> "Engine":
        self.spec = replace(self.spec, **changes)
        return self

    # ---- replay / view state (ports of step, seekToPct, setSplitMode, setReturnType, getMaxFrames, pointInTimeAtReplayHead) ----
    def _view(self):
        """The page state this engine instance stands for: (PageState, client-like with the scenario data)."""
        sp = self.spec
        deep = bool(sp.models_only and sp.models)
        st = PageState()
        sel = self.selected
        st.update({"current_date": sp.date, "current_criteria": sp.scenario, "return_type": sp.return_type, "min_win_rate": sp.min_win_rate,
                   "product_type": sp.product_type, "product": sp.product, "strategy_family": sp.strategy_family, "frame": sp.frame_index,
                   "baseline": sp.baseline_index, "split_mode": sp.split_mode, "deep_link_only": deep, "live_date": sp.live_date})
        if self.pit_mode:
            st.update({"pit_mode": True, "pit_models": list(sel.models), "pit_timeline_models": list(sel.timeline_models), "search_loaded": list(sel.search_loaded),
                       "scenario_removed": set(sel.scenario_removed)})
            st.pinned = OrderedDict(sel.pinned)
        if sp.models:
            wanted = set(sp.models)
            st.pinned = OrderedDict((m["model"], m) for m in self._models if m["model"] in wanted)
        key = f"{sp.scenario}_{'alt' if sp.return_type == 'ALT' else 'net'}" if pu.is_metric_aware_criteria(sp.scenario) else sp.scenario
        client = types.SimpleNamespace(criteria_data={key: {sp.date: self._models}})
        return st, client

    def max_frames(self) -> int:
        """getMaxFrames (replay_models)."""
        return rm.get_max_frames(*self._view())

    def replay_head_time(self):
        """pointInTimeAtReplayHead (replay_models)."""
        return rm.point_in_time_at_replay_head(*self._view())

    def step(self, delta: int) -> "Engine":
        return self.configure(frame_index=pu.frame_after_step(self.spec.frame_index, delta, self.max_frames()))

    def seek_to_pct(self, pct: float) -> "Engine":
        return self.configure(frame_index=pu.frame_for_pct(pct, self.max_frames()))

    def set_split_mode(self, mode) -> "Engine":
        return self.configure(split_mode=mode) if pu.valid_split_mode(mode) else self

    def set_return_type(self, return_type: str) -> "Engine":
        r = pu.swap_scenario_for_return_type(self.spec.return_type, self.spec.scenario, return_type)
        return self.configure(return_type=r["currentReturnType"], scenario=r["currentCriteria"])

    def __post_init__(self):
        self.selected.auto = self.auto_top1  # one auto-top1 bookkeeping object, as on the page

    def refresh_selected_time(self, client, *, at=None, rank_count: int = 1, limit: int = 10) -> dict:
        """refreshPointInTimeSelection: look up the strategies ranked at a time and merge them into the selected-time cohort
        (Engine.selected.models) alongside history, pinned and searched models. `at` defaults to the replay head."""
        s = self.spec
        self.pit_mode = True   # applying a selected time switches the page into point-in-time mode
        self.selected.current_date, self.selected.current_criteria = s.date, s.scenario
        self.selected.frame_index = s.frame_index
        opt_state = {"active_portfolio": None, "portfolio_scenario_configs": {}, "portfolio_criteria": {}, "current_criteria": s.scenario,
                     "current_return_type": s.return_type, "current_product_type": s.product_type, "current_product": s.product,
                     "current_strategy_family": s.strategy_family, "model_limit": limit, "min_win_rate": s.min_win_rate,
                     "rank_select_value": str(rank_count)}
        return stm.refresh_point_in_time_selection(self.selected, client, opt_state, head_time=self.replay_head_time(),
                                                   max_frames=self.max_frames(), eligible_models=self.eligible(), at_override=at)

    def finish_auto_top1_refresh(self, at, message="") -> dict:
        """finishAutomaticTop1Refresh over this engine's auto-top1 state; the head time comes from replay_head_time()."""
        return pu.finish_automatic_top1_refresh(self.auto_top1, at, message, self.replay_head_time())

    def exact_search_model(self, search_text, loaded_models=()):
        """getExactSearchModel: available models are the scenario candidates of the engine's own models."""
        s = self.spec
        available = core.scenario_candidates(self._models, return_type=s.return_type, min_win_rate=s.min_win_rate,
                                             product_type=s.product_type, product=s.product, strategy_family=s.strategy_family)
        return pu.exact_search_model(search_text, list(loaded_models), available)

    # ---- ported computations ----
    def eligible(self) -> list[dict]:
        """getEligibleModels (replay_models): the scenario's leaders for the date, or only the deep-linked models when models_only."""
        return rm.get_eligible_models(*self._view())

    def ribbon_view(self, visible=None, scenario_names=None) -> dict:
        """updateRibbon: the text and colours the page's ribbon shows (visible defaults to every eligible model)."""
        st, client = self._view()
        st.visible = {m["model"] for m in rm.get_eligible_models(st, client)} if visible is None else set(visible)
        return rm.update_ribbon(st, client, rm.new_ribbon_state(), scenario_names)

    def _baseline(self, models: list[dict]) -> int:
        return core.resolve_baseline_index(models, self.spec.baseline_index, self.spec.baseline_time)

    def ribbon(self) -> dict:
        m = self.eligible()
        return core.ribbon(m, return_type=self.spec.return_type, baseline_index=self._baseline(m),
                           frame_index=self.spec.frame_index)

    def overlay(self, model_id: str) -> dict:
        """B/S/X signals, paired trades and the daily-target signal for one model up to the replay head."""
        s = self.spec
        model = next((m for m in self.eligible() if m["model"] == model_id), None)
        if model is None:
            raise KeyError(model_id)
        series = core.mapped_series(model, s.return_type)
        head = len(series) - 1 if s.frame_index < 0 else min(s.frame_index, len(series) - 1)
        part = series[: head + 1]
        base = core.base_point(part, self._baseline([model]))
        signals = core.overlay_signals(part, base, s.exit_threshold)
        trades = core.pair_overlay_trades(signals, part, base)
        target = core.split_target_signal(signals, part, base, s.daily_target)
        return {"signals": signals, "trades": trades, "targetSignal": target}

    def rotation(self, kind: str = "leader", visible=None) -> dict:
        """Leader / multi-split rotation. drawChart feeds the rotation only the VISIBLE models (`activeModels`); pass the visible ids to match it."""
        s = self.spec
        models = self.eligible()
        if visible is not None:
            models = [m for m in models if m["model"] in set(visible)]
        if not models:
            return {"signals": [], "trades": [], "threshold": abs(s.exit_threshold), "targetSignal": None}
        replay = max(models, key=lambda m: len(m["series"]))["series"]
        longest = len(replay)
        up_to = longest - 1 if s.frame_index < 0 else min(s.frame_index, longest - 1)
        keys = core.metric_keys(s.return_type)
        ctx = core.RuleContext(trade_cache=self._trade_cache, current_date=s.date, product_type=s.product_type,
                               product=s.product, live_date=s.live_date, now_ms=s.now_ms,
                               current_frame_index=s.frame_index, max_frames=longest, return_type=s.return_type,
                               eligible_fallthrough=s.rule_eligible_fallthrough)
        common = dict(baseline_index=self._baseline(models), exit_threshold=s.exit_threshold,
                      daily_target=s.daily_target, replay_series=replay, hold_rank=s.hold_rank,
                      overlay_rule=s.overlay_rule, rule_context=ctx)
        if kind == "multi_split":
            return core.multi_split_rotation(models, keys, up_to, **common)
        return core.leader_rotation(models, keys["netKey"], up_to, **common)

    def outputs(self) -> dict:
        """Everything the parity harness compares, in one JSON-serialisable dict."""
        el = self.eligible()
        return {
            "instance_id": self.instance_id,
            "ported_from_page_version": PORTED_FROM_PAGE_VERSION,
            "spec": asdict(self.spec),
            "eligible": [m["model"] for m in el],
            "ribbon": self.ribbon(),
            "overlay": {m["model"]: self.overlay(m["model"]) for m in el},
            "rotation": {"leader": self.rotation("leader"), "multi_split": self.rotation("multi_split")},
        }

    # ---- live mode is never available headless ----
    def activate_live(self, *_a, **_k):
        raise HeadlessLiveModeError("headless instances are virtual only: no orders, no PostgreSQL writes, no live mode")

    place_order = activate_live
