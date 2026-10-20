# epics/ep_057_sql_to_pgsql/scenario_engine_v2/engine/page.py — the page's state transitions (portfolios, scenario / date navigation, replay, auto-add scheduling, live data and point-in-time refresh) as a headless controller.
#
# VERSION HISTORY
# v1.12.0 · 2026-10-20 · the model search follows page v2.65.36: it records what it concluded (search_resolved_query / _message) and redraws the date label, ribbon, cards and chart when nothing matched.
# v1.11.1 · 2026-10-19 · switch_date re-runs the model search for 3+ characters of any ID or strategy-name text (page v2.65.35).
# v1.11.0 · 2026-10-19 · load_model_search_from_database follows page v2.65.35: a search that is not a model ID looks up strategy names in /api/strategy_catalog (new stage _msearch_cat), first 100 matches; activate_portfolio follows v2.65.34.
# v1.10.0 · 2026-10-18 · _fire_pit: an un-awaited refreshPointInTimeSelection. One-go it is begin_ + _fire; for the browser copy (spawn_mode) the engine does the part before the request in place and hands the page a spawn (fetch + the resume stage), so no controller needs the network any more.
# v1.9.0 · 2026-10-18 · refresh_point_in_time_selection and refresh_point_in_time_history in stages for the browser copy (the page fetches; the engine plans before and merges after, on the page's current state).
# v1.8.1 · 2026-10-18 · stages hand applyPortfolioViewConfig to the page (it may want the network: the page runs its own fallback); create_similar_portfolio returns nothing, like the page.
# v1.8.0 · 2026-10-18 · activate_portfolio and create_similar_portfolio in stages for the browser copy (Await.handle / Await.attach: a started page promise gets a continuation that runs later as its own stage); a live portfolio is refused so the page runs its own copy.
# v1.7.0 · 2026-10-18 · set_ranking_criteria in stages (its one-go form is the stages driven in Python: fired refreshes, paintLiveChartCache, schedulePointInTimeSelection resolved by _resolve_await).
# v1.6.0 · 2026-10-18 · staged remove_portfolios, switch_date, refresh_active_portfolio_view (Await.fire: start a page async function without waiting for it).
# v1.5.1 · 2026-10-18 · FIX: a failing portfolio load inside refresh_live_data is caught (the page's try / catch wraps the await), it no longer escapes the controller; found by failing /api/portfolio_day fixtures.
# v1.5.0 · 2026-10-18 · refresh_live_data in stages for the browser copy (the page fetches and files the live-day payload, the engine decides); Await.next / catch; view_with (view calls with arguments); page flags.
# v1.4.0 · 2026-10-18 · staged controllers: a controller that awaits a page async function is split at the await (Await + STAGES + run_staged); the one-go method is the stages driven in Python, the browser copy drives them across the real await.
# v1.3.0 · 2026-10-17 · refresh_point_in_time_history (hourly cohorts).
# v1.2.0 · 2026-10-17 · max frames / replay head / eligible models / candidates default to replay_models (the page's own logic); injected hooks still win (the differential tests).
# v1.1.0 · 2026-10-17 · Responses are applied in issue order (outstanding Pendings; joiners of a shared request resume after its original awaiter); fetch_guard / on_fetched / on_timeout wiring; Page.rule_editor (overlay-rule editor).
# v1.0.0 · 2026-10-17 · Initial version: view config + persistence, replay, auto-add scheduling, selected-time apply, live-data refresh, portfolio store operations, activatePortfolio (non-live), switchDate, setRankingCriteria.
"""Everything here is a port of page functions that mix state changes with DOM updates and timers. Only the state changes are kept. What a
browser would do on screen is dropped; what it would persist or schedule is recorded in `state.effects` so callers (and the tests)
can see it: ["savePortfolios"], ["saveCriteriaWorkspaces"], ["localStorage.setItem", key], ["setTimeout", ms], ["clearTimeout"],
["setInterval", ms], ["clearInterval"], ["startPlaybackLoop"], ["renderPortfolioList"], ["refreshPointInTimeHistory"].

Live portfolios (LIVE / LIVE_ALT) place orders and are refused headless. Un-awaited calls (`void fetch...`) are issued at once and applied
after the caller's synchronous code, like JavaScript microtasks; timers are recorded but only run when run_timers() is called."""
from __future__ import annotations

import copy
import re

from . import page_utils as pu
from . import replay_models as rm
from . import selected_time as stm
from .core_ported import time_of_day_minutes
from .data_client import DATE_RE, LINKED_COLORS, MODEL_ID_RE, FetchError, Pending, _is_ok, _message, resolved, url_search_params
from .page_state import PageState

_ACTIVE = object()
MOMENTUM_SCENARIO_IDS = {"top3_momentum_net", "top3_momentum_alt"}
LIVE_PORTFOLIOS = ("LIVE", "LIVE_ALT")


class LivePortfolioRefused(RuntimeError):
    pass


def _clamp_num(value, lo, hi, fallback):
    n = pu._number(value)
    n = fallback if (n != n or n == 0) else n
    return max(lo, min(hi, n))


def _truthy(v) -> bool:
    return stm.js_truthy(v)


class Await:
    """A stage's request to the host: 'await this page async function, then resume me with its result'. `ctx` is what the stage wants back on resume (what the page's closure captured)."""

    def __init__(self, fn: str, args=None, ctx=None, next=None, catch=False, fire=False, sync=False, handle=None, attach=None):
        self.fn, self.args, self.ctx = fn, list(args or []), ctx or {}
        self.fire = fire      # start the page function and carry on without waiting for it (the page logs a failure)
        self.handle = handle  # with fire: keep the started promise under this name
        self.attach = attach  # run stage `attach` when the promise kept under args[0] settles (a detached .then); the call itself does not wait
        self.sync = sync      # a synchronous page function: call it and resume in the same turn (an await would let other async work slip in between)
        self.next = next      # name of the stage method to resume with (default: the next entry of STAGES[name])
        self.catch = catch    # the page reports a failure of the awaited function as {"error": msg} instead of letting it propagate


# controller name -> its stage methods; stage 0 takes the call's arguments, stage N takes (ctx, result of the awaited function)
STAGES = {
    "remove_model_from_portfolio": ("_remove_model_0", "_remove_model_1"),
    "add_catalogue_model": ("_add_catalogue_0", "_add_catalogue_1"),
    "move_model_between_portfolios": ("_move_model_0", "_move_model_1"),
    "repopulate_active_portfolio_from_criteria": ("_repopulate_0", "_repopulate_1"),
    # refresh_live_data is staged only for the browser copy; its one-go form (begin_refresh_live_data / _apply_live) keeps the event-loop model the headless races use
    "refresh_point_in_time_selection": ("_pit_sel_0", "_pit_sel_1"),
    "refresh_point_in_time_history": ("_pit_hist_0", "_pit_hist_1"),
    "load_model_search_from_database": ("_msearch_0", "_msearch_cat", "_msearch_1"),
    "load_deep_link_models_from_database": ("_deeplink_0", "_deeplink_1"),
    "activate_portfolio": ("_act_0", "_act_1", "_act_1b", "_act_2", "_act_3", "_act_4", "_act_load_done", "_act_rules_done"),
    "create_similar_portfolio": ("_similar_0", "_similar_1"),
    "set_ranking_criteria": ("_rank_0", "_rank_portfolio_1", "_rank_main_1", "_rank_main_2", "_rank_main_3", "_rank_done"),
    "remove_portfolios": ("_remove_portfolios_0", "_remove_portfolios_0b", "_remove_portfolios_1", "_remove_portfolios_2"),
    "switch_date": ("_switch_0", "_switch_1", "_switch_2", "_switch_3", "_switch_4"),
    "refresh_active_portfolio_view": ("_refresh_view_0", "_refresh_view_1"),
    "refresh_live_data": ("_refresh_live_0", "_refresh_live_1", "_refresh_live_after_data", "_refresh_live_after_sync", "_refresh_live_after_load"),
}
STAGE_METHODS = {fn for names in STAGES.values() for fn in names}   # the only methods a browser may ask to resume


class Page:
    def __init__(self, state: PageState, client, *, max_frames=None, head_time=None, eligible=None, candidates=None,
                 scenario_names=None, flags=None):
        self.s, self.client = state, client
        self.flags = flags or {}   # facts only the page knows (e.g. liveArmed)
        self._max_frames = max_frames or (lambda: rm.get_max_frames(self.s, self.client))
        self._head_time = head_time or (lambda: rm.point_in_time_at_replay_head(self.s, self.client))
        self._eligible = eligible or (lambda: rm.get_eligible_models(self.s, self.client))
        self._candidates = candidates or (lambda: rm.get_scenario_candidates(self.s, self.client))
        self.scenario_names = scenario_names or {}
        self._micro: list = []
        self._timers: list = []
        self._outstanding: list = []   # fire-and-forget Pendings, applied in issue order
        self._calls: list = []         # page functions a stage asks the host to call once it returns (staged controllers)
        self._spawns: list = []        # un-awaited page work a command asks the host to start (fetch + the stage to resume with its answer)
        self.spawn_mode = False        # the browser copy: un-awaited lookups are handed to the page instead of run here
        client.on_effect = self.fx  # persistence the client does on the page's behalf (rememberPortfolioView)
        client.on_timeout = lambda fn, delay: self._timeout(fn, delay)
        client.fetch_guard = lambda name, date, key: (self.s.active_portfolio == name and self.s.current_date == date
                                                      and ",".join(self.s.portfolios.get(name) or []) == key)
        client.on_fetched = self._on_fetched
        from .rule_editor import RuleEditor  # local import: rule_editor uses Page helpers
        self.rule_editor = RuleEditor(self)

    # ------------------------------------------------------------------ infrastructure
    def fx(self, *a):
        self.s.effects.append(list(a))

    def dom(self, element, op, *args):
        """A write the page makes to one of its elements (the browser copy replays it): ['dom', element, op, args]; op is 'set' (args: property, value), 'classList.add' / 'classList.remove' /
        'classList.toggle', 'setAttribute' or 'removeAttribute'. Fields the page mirrors from the DOM (selected time, search box, status texts) travel in the state snapshot instead."""
        self.fx("dom", element, op, list(args))

    def pending_button(self, on):
        """applySelectedTimeBtn's busy look while a selected-time lookup is out."""
        b = "applySelectedTimeBtn"
        if on:
            self.dom(b, "classList.add", "click-feedback-pending")
            self.dom(b, "setAttribute", "aria-busy", "true")
        else:
            self.dom(b, "classList.remove", "click-feedback-pending")
            self.dom(b, "removeAttribute", "aria-busy")

    def view_with(self, name, *args):
        """A view call that takes arguments (['view', name] as before; the browser copy passes `args`)."""
        self.fx("view", name)
        self.s.view_args[len(self.s.effects) - 1] = list(args)

    def view(self, *names):
        """The page calls a view function here (recorded as ['view', name]; the browser copy replays it)."""
        for n in names:
            self.fx("view", n)

    def render_all(self):
        self.view("updateDateLabelAndTitle", "updateScrubberUI", "updateRibbon", "renderCards", "drawChart")

    def defer(self, fn, wait=None):
        """Queue a continuation; with `wait`, it is runnable only once that request has been answered."""
        self._micro.append((fn, wait))

    def tick(self):
        while True:
            ready = next((e for e in self._micro if e[1] is None or e[1].done), None)
            if ready is None:
                return
            self._micro.remove(ready)
            ready[0]()

    def settle(self):
        """Let un-awaited work finish (what the event loop does after the caller returns), oldest request first."""
        while self._outstanding or self._micro:
            self.tick()
            if not self._outstanding and self._micro:
                self._micro[0] = (self._micro[0][0], None)  # nothing left to wait for
            if self._outstanding:
                self._outstanding.sort(key=lambda p: p.seq)
                self._outstanding.pop(0).finish()

    def run_staged(self, name, *args):
        """The one-go form of a staged controller: run each stage, resolving every Await the way the page would (in Python), then let un-awaited work finish."""
        stages = STAGES[name]
        out = getattr(self, stages[0])(*args)
        self._flush_calls()
        i = 0
        while isinstance(out, Await):
            i += 1
            result = self._resolve_await(out)
            out = getattr(self, out.next or stages[i])(out.ctx, result)
            self._flush_calls()
        self.settle()
        return out

    def run_stage(self, name, stage, args=None, ctx=None, result=None):
        """One stage of a staged controller (what a browser copy asks for): returns (ret, Await | None, page calls to make afterwards)."""
        if isinstance(stage, str):
            if stage not in STAGE_METHODS:
                raise ValueError(f"not a stage method: {stage!r}")
            fn, first = getattr(self, stage), False
        else:
            fn, first = getattr(self, STAGES[name][stage]), stage == 0
        out = fn(*(args or [])) if first else fn(ctx or {}, result)
        calls, self._calls = self._calls, []
        return (None, out, calls) if isinstance(out, Await) else (out, None, calls)

    def _call(self, fn, *args):
        """Ask the host to call a page function at the end of this stage (the page's own, possibly delegated, copy runs it)."""
        self._calls.append([fn, list(args)])

    def _flush_calls(self):
        """The one-go form of those calls: run the engine's own implementation, in order."""
        calls, self._calls = self._calls, []
        for fn, args in calls:
            if fn == "schedulePointInTimeSelection":
                self.schedule_point_in_time_selection(*args)
            elif fn.startswith("__"):
                pass   # page-only DOM / URL code the engine does not model
            else:
                raise ValueError(f"no engine implementation for page call {fn!r}")

    def _resolve_await(self, aw):
        if aw.fn == "loadPortfolioData":
            return self._await(self.begin_load_portfolio_data(*aw.args))
        if aw.fn == "refreshLiveData" and aw.fire:   # started, not waited for: the request goes out now, the answer is applied after the caller
            skip = bool(aw.args[1]) if len(aw.args) > 1 else False
            self._fire(self.begin_refresh_live_data(aw.args[0], skip))
            return None
        if aw.fn == "applyPortfolioViewConfig":
            self.apply_portfolio_view_config(*aw.args)
            return None
        if aw.fn == "activatePortfolio":
            self.activate_portfolio(*aw.args)
            return None
        if aw.fn == "paintLiveChartCache":   # a browser cache: nothing to paint headless (the page's stub says 'not painted')
            self.view("paintLiveChartCache")
            return False
        if aw.fn == "schedulePointInTimeSelection":
            self.schedule_point_in_time_selection()
            return None
        if aw.fn == "fetchStrategyCatalog":   # the page's fetch of /api/strategy_catalog (a failing answer throws; reported as {"error"} when the stage asks to catch)
            try:
                status, payload = self.client._get(f"{self.client.api}/api/strategy_catalog?{url_search_params({'date': aw.args[0]})}")
                if not _is_ok(status):
                    raise FetchError(_message(payload, f"HTTP {status}"))
                return {"ok": (payload.get("models") if isinstance(payload, dict) else None) or []}
            except Exception as error:  # noqa: BLE001
                return {"error": str(error)}
        if aw.fn == "fetchPortfolioDayBatches":   # the page's Promise.all over the batches; a non-2xx answer throws (reported as {"error"} when the stage asks to catch)
            try:
                answers = [self.client._get(f"{self.client.api}/api/portfolio_day?{url_search_params({'models': ','.join(batch), 'date': aw.args[1]})}")
                           for batch in aw.args[0]]   # every request goes out before the first answer is looked at (Promise.all)
                out = []
                for status, payload in answers:
                    if not _is_ok(status):
                        raise FetchError(_message(payload, f"HTTP {status}"))
                    models = payload.get("models") if isinstance(payload, dict) else None
                    out.append(models if isinstance(models, list) else [])
                return {"ok": out}
            except Exception as error:  # noqa: BLE001
                return {"error": str(error)}
        raise ValueError(f"no engine implementation for awaited page function {aw.fn!r}")

    def _on_fetched(self, background):
        s = self.s
        self._pull_models()
        self.auto_pin_live_portfolio_strategies()
        if background:
            s.visible = {m.get("model") for m in s.portfolio_models}
            self.render_all()

    def _timeout(self, fn, delay, name=None, call=None, args=None):
        """Record a page timer. `name`/`call`/`args` name the callback (the page's own timer variable and the controller it fires) so a browser copy can re-create the timer."""
        self.fx("setTimeout", delay)
        if name:
            self.s.timer_ops.append({"op": "set", "timer": name, "ms": delay, "call": call, "args": list(args or []), "at": len(self.s.effects) - 1})
        self._timers.append(fn)

    def _clear_timer(self, name):
        self.fx("clearTimeout")
        self.s.timer_ops.append({"op": "clear", "timer": name, "at": len(self.s.effects) - 1})

    def _timer_op(self, effect, op, name, **extra):
        """An interval start / stop: the effect (what the original page calls) plus the named operation the browser copy replays on its own timer variable."""
        if effect == "setInterval":
            self.fx(effect, extra["ms"])
        else:
            self.fx(effect)
        self.s.timer_ops.append({"op": op, "timer": name, "at": len(self.s.effects) - 1, **extra})

    def run_timers(self):
        """Run the timer callbacks recorded so far (the page's debounces); they may record more."""
        while self._timers:
            self._timers.pop(0)()
            self.tick()

    def _await(self, pending):
        """`await pending`: requests issued earlier have been answered by then (oldest first); a purely local await lets only
        already-resolved continuations run."""
        self.tick()
        self._outstanding.sort(key=lambda p: p.seq)
        while self._outstanding and (self._outstanding[0].seq < pending.seq if pending.issued else not self._outstanding[0].issued):
            self._outstanding.pop(0).finish()
            self.tick()  # continuations queued by that response run before the next response is applied
        return pending.finish()

    # models the engine decides on
    def max_frames(self):
        return self._max_frames()

    def _pull_models(self):
        self.s.portfolio_models = self.client.portfolio_models

    def _push_models(self):
        self.client.portfolio_models = self.s.portfolio_models

    def _opt_state(self) -> dict:
        s = self.s
        return {"active_portfolio": s.active_portfolio, "portfolio_scenario_configs": s.portfolio_scenario_configs,
                "portfolio_criteria": s.portfolio_criteria, "current_criteria": s.current_criteria, "current_return_type": s.return_type,
                "current_product_type": s.product_type, "current_product": s.product, "current_strategy_family": s.strategy_family,
                "model_limit": s.model_limit, "min_win_rate": s.min_win_rate, "rank_select_value": s.rank_select_value,
                "current_date": s.current_date, "auto_refresh_enabled": s.auto_enabled, "auto_refresh_direction": s.auto_direction,
                "auto_refresh_rank": s.auto_rank}

    # ------------------------------------------------------------------ overlay rule lookups
    def assigned_portfolio_overlay_rule(self, portfolio=_ACTIVE):
        portfolio = self.s.active_portfolio if portfolio is _ACTIVE else portfolio
        if not portfolio:
            return None
        lib = self.client.overlay_rule_library
        assignments = lib.get("assignments")
        rule_id = assignments.get(portfolio) if isinstance(assignments, dict) else None
        if rule_id is None:
            return None
        return next((r for r in lib.get("rules", []) if r.get("id") == rule_id), None)

    def active_portfolio_overlay_rule(self):
        if not self.s.active_portfolio or not self.s.use_assigned_rule:
            return None
        return self.assigned_portfolio_overlay_rule()

    # ------------------------------------------------------------------ view config
    def current_portfolio_view_config(self) -> dict:
        s = self.s
        return {"date": s.current_date, "selectedTopCount": pu.selected_time_rank_count(s.rank_select_value),
                "selectedAtTime": str(s.selected_time_input or "").strip(), "replayHeadTime": self._head_time() or "",
                "criteria": s.current_criteria, "returnType": s.return_type, "productType": s.product_type, "product": s.product,
                "strategyFamily": s.strategy_family, "limit": s.model_limit, "minWinRate": s.min_win_rate, "splitMode": s.split_mode,
                "chartLocked": s.chart_locked, "chartLockBeforeLive": s.chart_lock_before_live,
                "useAssignedOverlayRule": s.use_assigned_rule, "autoAddEnabled": s.auto_enabled, "autoAddDirection": s.auto_direction,
                "autoAddRank": s.auto_rank, "autoAddMinutes": s.auto_minutes}

    def persist_portfolio_view_config(self, name=_ACTIVE):
        s = self.s
        name = s.active_portfolio if name is _ACTIVE else name
        if name:
            s.portfolio_view_configs[name] = self.current_portfolio_view_config()
            self.fx("localStorage.setItem", "strategyDirectoryPortfolioViewV1")
        else:
            s.main_view_config = self.current_portfolio_view_config()
            self.fx("localStorage.setItem", "strategyDirectoryMainViewV1")

    def update_auto_refresh_status(self, message=""):
        s = self.s
        s.auto_status_text = message or (f"On · {s.auto_direction} #{pu.js_str(s.auto_rank)} · every {pu.js_str(s.auto_minutes)}m at clock times"
                                         if s.auto_enabled else "Off")

    def apply_chart_lock(self, locked, persist=True):
        s = self.s
        # (a live portfolio with armed live mode would force the lock on; live mode is refused headless)
        s.chart_locked = bool(locked)
        if persist:
            self.persist_portfolio_view_config()
        on = s.chart_locked
        self.dom("chartLockBtn", "setAttribute", "aria-pressed", "true" if on else "false")
        self.dom("chartLockIcon", "set", "textContent", "🔒" if on else "🔓")
        self.dom("chartLockLabel", "set", "textContent", "Chart locked" if on else "Chart unlocked")
        self.view("updateChartLockControlState")
        self.dom("chartLockBtn", "set", "className", "px-2.5 py-1 rounded-lg border border-lime-400/60 bg-lime-500 text-slate-950 text-xs font-black transition shadow shadow-lime-500/20"
                 if on else "px-2.5 py-1 rounded-lg border border-slate-700 bg-slate-900 text-slate-300 hover:text-white text-xs font-bold transition")
        for control in ("playBtn", "stepBackBtn", "stepFwdBtn", "restartBtn", "setBaseAtHeadBtn", "resetBaselineBtn"):
            self.dom(control, "set", "disabled", on)
            self.dom(control, "classList.toggle", "opacity-40", on)
            self.dom(control, "classList.toggle", "cursor-not-allowed", on)
        self.dom("scrubberTrack", "setAttribute", "aria-disabled", "true" if on else "false")
        self.dom("scrubberTrack", "classList.toggle", "cursor-not-allowed", on)
        self.dom("scrubberTrack", "set", "title", "Chart locked — unlock to scrub or reposition the baseline" if on else "Scrub replay head")
        if s.chart_locked:
            self.pause_replay()
            s.frame = max(0, self.max_frames() - 1)
            self.view("updateScrubberUI", "updateRibbon", "renderCards", "drawChart")
            self.schedule_point_in_time_selection()

    def apply_portfolio_view_config(self, config):
        s = self.s
        if not config:
            return
        s.return_type = "ALT" if config.get("returnType") == "ALT" else "NET"
        s.product_type = config.get("productType") if config.get("productType") in ("all", "forex", "crypto") else "all"
        s.product = str(pu.js_str(stm.js_or(config.get("product"), "all"))).lower()
        s.strategy_family = str(pu.js_str(stm.js_or(config.get("strategyFamily"), "all"))).lower()
        lim = pu._number(config.get("limit"))
        s.model_limit = int(lim) if lim in (10, 20, 30) else 10
        top = _clamp_num(config.get("selectedTopCount"), 1, 10, 1)
        s.rank_select_value = pu.js_str(top)
        at = str(pu.js_str(stm.js_or(config.get("selectedAtTime"), "")))
        s.selected_time_input = at if re.fullmatch(r"[0-9]{2}:[0-9]{2}", at) else ""
        self.dom("applySelectedTimeBtn", "set", "textContent", "Refresh & Add #1" + (f"–#{pu.js_str(top)}" if top > 1 else ""))
        s.min_win_rate = _clamp_num(config.get("minWinRate"), 0, 100, 0)
        if config.get("splitMode") in pu.SPLIT_MODES:
            s.split_mode = config["splitMode"]
        if config.get("criteria"):
            s.current_criteria = config["criteria"]
        if isinstance(config.get("useAssignedOverlayRule"), bool):
            s.use_assigned_rule = config["useAssignedOverlayRule"]
        else:
            s.use_assigned_rule = bool(s.active_portfolio and self.assigned_portfolio_overlay_rule())
        s.auto_enabled = bool(config.get("autoAddEnabled"))
        s.auto_direction = "bottom" if config.get("autoAddDirection") == "bottom" else "top"
        s.auto_rank = _clamp_num(config.get("autoAddRank"), 1, 5, 1)
        m = pu._number(config.get("autoAddMinutes"))
        s.auto_minutes = int(m) if m in (1, 5, 15, 30, 60, 120) else 15
        s.auto_direction_select = s.auto_direction
        s.auto_rank_select = pu.js_str(s.auto_rank)
        self.dom("autoRefreshTop1Toggle", "set", "checked", s.auto_enabled)
        self.dom("autoRefreshTop1Interval", "set", "value", pu.js_str(s.auto_minutes))
        self.update_auto_refresh_status()
        self.reset_automatic_rank_schedule()
        s.chart_lock_before_live = config["chartLockBeforeLive"] if isinstance(config.get("chartLockBeforeLive"), bool) else None
        if isinstance(config.get("chartLocked"), bool):
            self.apply_chart_lock(config["chartLocked"], False)
        self.view("syncAssignedOverlayRuleUI")
        net = s.return_type == "NET"
        self.dom("returnTypeNetBtn", "set", "className", "px-2.5 py-1 font-bold rounded bg-indigo-600 text-white transition flex items-center gap-1 shadow" if net
                 else "px-2.5 py-1 font-bold rounded text-slate-400 hover:text-white transition flex items-center gap-1")
        self.dom("returnTypeAltBtn", "set", "className", "px-2.5 py-1 font-bold rounded bg-amber-600 text-white transition flex items-center gap-1 shadow" if not net
                 else "px-2.5 py-1 font-bold rounded text-slate-400 hover:text-white transition flex items-center gap-1")
        self.dom("productTypeFilter", "set", "value", s.product_type)
        self.dom("modelLimitFilter", "set", "value", pu.js_str(s.model_limit))
        self.dom("winRateSlider", "set", "value", pu.js_str(s.min_win_rate))
        self.dom("winRateValBadge", "set", "textContent", f"≥ {pu.js_str(s.min_win_rate)}%")
        self.dom("winRateDisplayBadge", "set", "textContent", "All Win Rates (≥0%)" if s.min_win_rate == 0 else f"Win Rate ≥ {pu.js_str(s.min_win_rate)}%")
        self.view("updateStrategyFamilyOptions")
        self.dom("productFilter", "ensureOption", s.product)
        self.dom("productFilter", "set", "value", s.product)
        self.view("syncSplitModeControls", "updateScenarioUI")

    # ------------------------------------------------------------------ replay
    def start_replay(self):
        s = self.s
        max_f = self.max_frames()
        if s.frame >= max_f - 1 or s.frame < s.baseline:
            s.frame = s.baseline
        s.is_playing = True
        self.dom("playIcon", "set", "textContent", "⏸")
        self.dom("playBtnText", "set", "textContent", "Pause")
        self.dom("playBtn", "classList.remove", "bg-sky-600", "hover:bg-sky-500")
        self.dom("playBtn", "classList.add", "bg-amber-600", "hover:bg-amber-500")
        s.replay_interval = 1  # startPlaybackLoop() installs the playback timer
        self.fx("startPlaybackLoop")

    def pause_replay(self):
        s = self.s
        s.is_playing = False
        self.dom("playIcon", "set", "textContent", "▶")
        self.dom("playBtnText", "set", "textContent", "Play from Base" if s.baseline > 0 else "Play")
        self.dom("playBtn", "classList.add", "bg-sky-600", "hover:bg-sky-500")
        self.dom("playBtn", "classList.remove", "bg-amber-600", "hover:bg-amber-500")
        if s.replay_interval:
            self._timer_op("clearInterval", "clear", "replayInterval")
            s.replay_interval = None

    # ------------------------------------------------------------------ auto-add scheduling
    def reset_automatic_rank_schedule(self):
        s = self.s
        s.auto_direction = "bottom" if s.auto_direction_select == "bottom" else "top"
        s.auto_rank = _clamp_num(s.auto_rank_select, 1, 5, 1)
        if s.auto_request_at is not None:
            s.auto_request_at = None
            s.pending_explicit_time = None
            s.explicit_refresh = False
            s.pit_request_sequence += 1
            s.pit_requested_key = ""
            self.pending_button(False)
        s.auto_context = pu.point_in_time_context_key(self._opt_state())
        head = self._head_time()
        head_minute = pu.clock_minutes(head) if head else None
        s.auto_last_minute = head_minute
        s.auto_next_minute = None if head_minute is None else pu.next_automatic_top1_minute(head_minute, s.auto_minutes, True)
        self.update_auto_refresh_status(f"On · {s.auto_direction} #{pu.js_str(s.auto_rank)} · every {pu.js_str(s.auto_minutes)}m at clock times"
                                        if s.auto_enabled else "Off")
        self.persist_portfolio_view_config()
        if s.auto_enabled and head:
            self.schedule_automatic_top1_refresh(head)

    def schedule_automatic_top1_refresh(self, at):
        s = self.s
        if not s.auto_enabled:
            return
        minute = pu.clock_minutes(at)
        if minute is None:
            return
        context = pu.point_in_time_context_key(self._opt_state())
        if s.auto_context != context:
            if s.auto_request_at is not None:
                s.auto_request_at = None
                s.pending_explicit_time = None
                s.explicit_refresh = False
                s.pit_request_sequence += 1
                s.pit_requested_key = ""
                self.pending_button(False)
            s.auto_context = context
            s.auto_last_minute = minute
            s.auto_next_minute = pu.next_automatic_top1_minute(minute, s.auto_minutes, True)
            self.update_auto_refresh_status(f"On · next at {pu.replay_clock_time(s.auto_next_minute)}")
        if s.auto_last_minute is None or s.auto_next_minute is None:
            s.auto_last_minute = minute
            s.auto_next_minute = pu.next_automatic_top1_minute(minute, s.auto_minutes, True)
        if minute < s.auto_last_minute:
            s.auto_last_minute = minute
            s.auto_next_minute = pu.next_automatic_top1_minute(minute, s.auto_minutes, True)
            self.update_auto_refresh_status(f"On · replay rewound · next at {pu.replay_clock_time(s.auto_next_minute)}")
        s.auto_last_minute = minute
        if minute < s.auto_next_minute or s.auto_request_at is not None or s.explicit_refresh:
            return
        scheduled = pu.replay_clock_time(s.auto_next_minute)
        s.auto_request_at = scheduled
        s.pending_explicit_time = scheduled
        s.explicit_refresh = True
        s.pit_requested_key = ""
        self._clear_timer("pointInTimeDebounceTimer")
        self.pending_button(True)
        self.update_auto_refresh_status(f"Checking {s.auto_direction} #{pu.js_str(s.auto_rank)} at {scheduled}…")
        self._fire_pit(scheduled)

    def schedule_point_in_time_selection(self):
        s = self.s
        at = self._head_time()
        if at:
            self.schedule_automatic_top1_refresh(at)
        if not s.pit_mode:
            return
        self.fx("refreshPointInTimeHistory")
        if at:
            o = pu.point_in_time_request_options(self._opt_state())
            next_key = "|".join(pu.js_str(p) for p in [s.current_date, at, o["scenario"], o["return_type"], o["product_type"], o["product"],
                                                       o["strategy_family"], o["limit"], o["min_win_rate"], s.active_portfolio or "scenario"])
            if not s.explicit_refresh and s.pit_requested_key and s.pit_requested_key != next_key:
                s.pit_request_sequence += 1
                s.pit_requested_key = ""
                self.pending_button(False)
        if not s.explicit_refresh and s.is_playing and at and not re.search(r":00$", at):
            self._clear_timer("pointInTimeDebounceTimer")
            return
        self._clear_timer("pointInTimeDebounceTimer")
        if not s.explicit_refresh:
            self._timeout(lambda: self._fire(self.begin_refresh_point_in_time_selection(at)), 180, "pointInTimeDebounceTimer", "refreshPointInTimeSelection", [at])

    def apply_selected_time(self):
        s = self.s
        before = list(s.pit_models) if (s.pit_mode and isinstance(s.pit_models, list)) else list(self._eligible())
        if not s.pit_mode:
            s.pit_mode = True
            s.pit_models = before
            self.view("updatePointInTimeToggleUI")
        requested_at = s.selected_time_input
        if pu.clock_minutes(requested_at) is None:
            self.pending_button(False)
            s.pit_status = ["Choose a valid time in HH:MM format", "text-[10px] font-bold text-rose-300"]
            return
        self.pause_replay()
        self._clear_timer("pointInTimeDebounceTimer")
        s.search_sequence += 1
        self._clear_timer("modelSearchTimer")
        s.search_loaded = []
        s.model_search_input = ""
        self.view("updateScrubberUI", "updateRibbon", "renderCards", "drawChart")
        s.selected_time_input = requested_at
        s.pending_explicit_time = requested_at
        s.explicit_refresh = True
        s.pit_requested_key = ""
        s.pit_request_sequence += 1
        self._fire_pit(requested_at)

    def trigger_selected_time_refresh(self):
        s = self.s
        if s.deep_link_only:
            s.deep_link_only = False
            self.view("updateScenarioUI")
        self.dom("applySelectedTimeBtn", "classList.add", "click-feedback-selected", "click-feedback-pending")
        self.dom("applySelectedTimeBtn", "setAttribute", "aria-busy", "true")
        self.apply_selected_time()
        self.settle()

    # ------------------------------------------------------------------ point-in-time refresh (selected_time) and live data
    def _fire(self, pending):
        """An un-awaited async call: the request is already issued; the result is applied when a later request is awaited or the
        caller finishes."""
        self._outstanding.append(pending)

    def _pit_state(self) -> stm.SelectedTimeState:
        s = self.s
        st = stm.SelectedTimeState(
            point_in_time_mode=s.pit_mode, current_date=s.current_date, current_criteria=s.current_criteria, active_portfolio=s.active_portfolio,
            auto=pu.AutoTop1State(request_at=s.auto_request_at, pending_explicit_time=s.pending_explicit_time, explicit_refresh=s.explicit_refresh,
                                  next_minute=s.auto_next_minute, interval_minutes=s.auto_minutes, enabled=s.auto_enabled),
            auto_direction=s.auto_direction_select, auto_rank_value=s.auto_rank_select, models=s.pit_models, timeline_models=s.pit_timeline_models,
            requested_key=s.pit_requested_key, pinned=s.pinned, search_loaded=s.search_loaded, history=s.history,
            history_context=s.history_context, scenario_removed=s.scenario_removed, scenario_names=self.scenario_names,
            status=s.pit_status[0], status_class=s.pit_status[1], frame_index=s.frame, selected_time_input=None,
            selected_model_index=s.selected_model_index, visible=set(s.visible), request_sequence=s.pit_request_sequence,
            history_at=s.pit_history_at)
        return st

    def _pit_commit(self, st: stm.SelectedTimeState):
        s = self.s
        s.auto_request_at, s.pending_explicit_time, s.explicit_refresh = st.auto.request_at, st.auto.pending_explicit_time, st.auto.explicit_refresh
        s.auto_next_minute = st.auto.next_minute
        s.pit_models, s.pit_timeline_models, s.pit_requested_key = st.models, st.timeline_models, st.requested_key
        s.history_context, s.pit_status = st.history_context, [st.status, st.status_class]
        s.frame, s.selected_model_index, s.visible = st.frame_index, st.selected_model_index, set(st.visible)
        s.pit_request_sequence = st.request_sequence
        s.pit_history_at = st.history_at
        for kind, name in st.events:
            if kind == "pending_off":
                self.pending_button(False)
            else:
                (self.fx if kind == "fx" else self.view)(name)
        st.events = []
        if st.selected_time_input is not None:
            s.selected_time_input = st.selected_time_input

    def _pit_sync(self, st: stm.SelectedTimeState):
        """Bring a lookup's working copy up to date with the page before its result is applied (the page may have changed meanwhile)."""
        s = self.s
        st.current_date, st.current_criteria, st.active_portfolio = s.current_date, s.current_criteria, s.active_portfolio
        st.point_in_time_mode, st.requested_key, st.request_sequence = s.pit_mode, s.pit_requested_key, s.pit_request_sequence
        st.models, st.timeline_models = s.pit_models, s.pit_timeline_models
        st.auto.request_at, st.auto.pending_explicit_time, st.auto.explicit_refresh = s.auto_request_at, s.pending_explicit_time, s.explicit_refresh
        st.auto.next_minute, st.auto.interval_minutes, st.auto.enabled = s.auto_next_minute, s.auto_minutes, s.auto_enabled
        st.frame_index, st.selected_model_index, st.visible = s.frame, s.selected_model_index, set(s.visible)
        st.status, st.status_class = s.pit_status[0], s.pit_status[1]
        st.history_context, st.selected_time_input = s.history_context, None
        st.history_at = s.pit_history_at

    def begin_refresh_point_in_time_selection(self, at_override=None) -> Pending:
        """refreshPointInTimeSelection: the request goes out now; the cohort is merged when the Pending finishes."""
        st = self._pit_state()
        pending = stm.begin_point_in_time_selection(st, self.client, self._opt_state(), head_time=self._head_time(), max_frames=self.max_frames(),
                                                    eligible_models=self._eligible(), at_override=at_override)
        self._pit_commit(st)  # the part before the request (flags, the "Loading…" label, the request counter) is visible at once
        if pending.done:
            return pending

        def finish():
            self._pit_sync(st)
            r = pending.finish()
            if st.auto_status is not None:
                self.update_auto_refresh_status(st.auto_status)
            if st.sched is not None:
                head = st.sched
                self._timeout(lambda: self.schedule_automatic_top1_refresh(head), 0)
            self._pit_commit(st)
            return r
        return Pending(finish, issued=pending.issued)

    def begin_refresh_point_in_time_history(self) -> Pending:
        """refreshPointInTimeHistory: the hourly cohorts for the current selection (the request goes out now; the result is applied when the Pending finishes)."""
        s = self.s
        if (s.current_criteria == "top1_at_time" or not s.pit_mode or not s.pit_history_near_viewport or s.pit_history_panel_hidden
                or not DATE_RE.fullmatch(s.current_date or "")):
            return resolved(None)
        key = pu.point_in_time_context_key(self._opt_state())
        if key == s.pit_history_key:
            return resolved(None)
        s.pit_history_key = key
        s.pit_history_at = ""
        s.pit_history_sequence += 1
        seq = s.pit_history_sequence
        s.pit_history_status_text = "Building hourly cohorts\u2026"
        url = self.client.point_in_time_hours_url(s.current_date, pu.point_in_time_request_options(self._opt_state()))
        try:
            resp, err = self.client._get(url), None
        except Exception as e:  # noqa: BLE001
            resp, err = None, e

        def apply():
            try:
                if err is not None:
                    raise err
                status, payload = resp
                if not (200 <= int(status) < 300):
                    raise FetchError(pu.js_str(stm.js_or(payload.get("error") if isinstance(payload, dict) else None, status)))
                if seq != s.pit_history_sequence or key != s.pit_history_key:
                    return None
                hours = payload.get("hours") if isinstance(payload, dict) else None
                s.pit_hours = hours if isinstance(hours, list) else []
                s.pit_history_status_text = f"{len(s.pit_hours)} hourly cohorts \u00b7 select an hour to inspect its strategies"
                self.fx("renderPointInTimeHistory")
            except Exception as error:  # noqa: BLE001
                if seq != s.pit_history_sequence:
                    return None
                s.pit_history_status_text = f"Hourly cohorts unavailable: {error}"
                s.pit_history_key = ""
            return None
        return Pending(apply, issued=True)

    # ---- the two point-in-time lookups in stages (browser copy): the page fetches, the engine plans before and merges after
    def _pit_plan(self, at_override=None):
        """The part of refreshPointInTimeSelection before the request, in place: returns the context the merge needs, or None when nothing is requested."""
        st = self._pit_state()
        result, ctx = stm.plan_point_in_time_selection(st, self.client, self._opt_state(), head_time=self._head_time(), max_frames=self.max_frames(),
                                                       eligible_models=self._eligible(), at_override=at_override)
        self._pit_commit(st)   # the part before the request (flags, the "Loading…" label, the request counter) is visible at once
        return ctx

    def _fire_pit(self, at):
        """An un-awaited refreshPointInTimeSelection(at). One-go: the request goes out now and the merge runs when it is answered. Browser copy: the part before the request
        runs here, in its place in the controller, and the page is handed a spawn (the fetch, and the stage that merges the answer into the page's current state)."""
        if not self.spawn_mode:
            self._fire(self.begin_refresh_point_in_time_selection(at))
            return
        ctx = self._pit_plan(at)
        if ctx is not None:
            self._spawns.append({"method": "refresh_point_in_time_selection", "fn": "fetchPointInTime", "args": [ctx["url"]], "ctx": ctx, "stage": "_pit_sel_1"})

    def _pit_sel_0(self, at_override=None):
        ctx = self._pit_plan(at_override)
        if ctx is None:
            return None
        return Await("fetchPointInTime", [ctx["url"]], ctx, next="_pit_sel_1", catch=True)

    def _pit_sel_1(self, ctx, result):
        st = self._pit_state()   # the page may have changed while the lookup was out: merge into its CURRENT state
        if "error" in (result or {}):
            resp, err = None, FetchError(result["error"])
        else:
            got = (result or {}).get("ok") or {}
            resp, err = (got.get("status"), got.get("payload")), None
        stm.apply_point_in_time_selection(st, ctx, resp, err, self._eligible())
        if st.auto_status is not None:
            self.update_auto_refresh_status(st.auto_status)
        if st.sched is not None:
            head = st.sched
            self._timeout(lambda: None, 0, "anonymousTimer", "scheduleAutomaticTop1Refresh", [head])
        self._pit_commit(st)
        return None

    def _pit_hist_0(self):
        s = self.s
        if (s.current_criteria == "top1_at_time" or not s.pit_mode or not s.pit_history_near_viewport or s.pit_history_panel_hidden
                or not DATE_RE.fullmatch(s.current_date or "")):
            return None
        key = pu.point_in_time_context_key(self._opt_state())
        if key == s.pit_history_key:
            return None
        s.pit_history_key = key
        s.pit_history_at = ""
        s.pit_history_sequence += 1
        s.pit_history_status_text = "Building hourly cohorts\u2026"
        url = self.client.point_in_time_hours_url(s.current_date, pu.point_in_time_request_options(self._opt_state()))
        return Await("fetchPointInTimeHours", [url], {"seq": s.pit_history_sequence, "key": key}, next="_pit_hist_1", catch=True)

    def _pit_hist_1(self, ctx, result):
        s = self.s
        seq, key = ctx["seq"], ctx["key"]
        try:
            if "error" in (result or {}):
                raise FetchError(result["error"])
            got = (result or {}).get("ok") or {}
            status, payload = got.get("status"), got.get("payload")
            if not (200 <= int(status) < 300):
                raise FetchError(pu.js_str(stm.js_or(payload.get("error") if isinstance(payload, dict) else None, status)))
            if seq != s.pit_history_sequence or key != s.pit_history_key:
                return None
            hours = payload.get("hours") if isinstance(payload, dict) else None
            s.pit_hours = hours if isinstance(hours, list) else []
            s.pit_history_status_text = f"{len(s.pit_hours)} hourly cohorts \u00b7 select an hour to inspect its strategies"
            self.fx("renderPointInTimeHistory")
        except Exception as error:  # noqa: BLE001
            if seq != s.pit_history_sequence:
                return None
            s.pit_history_status_text = f"Hourly cohorts unavailable: {error}"
            s.pit_history_key = ""
        return None

    def refresh_point_in_time_history(self):
        self._await(self.begin_refresh_point_in_time_history())
        self.settle()

    # ---- loadModelSearchFromDatabase / loadDeepLinkModelsFromDatabase in stages: the page fetches /api/portfolio_day, the engine validates before and merges after (on the page's current state)
    def load_model_search_from_database(self, search_term):
        return self.run_staged("load_model_search_from_database", search_term)

    def _msearch_0(self, search_term):
        s = self.s
        s.search_sequence += 1
        seq, date = s.search_sequence, s.current_date
        terms = pu.model_search_terms(search_term)
        query = re.sub(r"\s+", "_", str(search_term or "").strip().lower())
        s.search_resolved_query, s.search_resolved_message = None, ""
        is_list = len(terms) > 1 and all(re.fullmatch(r"(?:dna_)?\d+", m, re.I) for m in terms)
        is_direct = is_list or (len(terms) == 1 and re.fullmatch(r"(?:dna_)?\d{5,}", terms[0], re.I) is not None)
        requested = terms if is_direct else [query]
        if not search_term or len(search_term) > 100 or (is_list and any(not MODEL_ID_RE.fullmatch(m) for m in requested)):
            s.model_search_status = "Search by one strategy name, or enter model IDs separated by commas or spaces"
            return None
        if not DATE_RE.fullmatch(date or ""):
            s.model_search_status = "Choose a single date to search PostgreSQL"
            return None
        n = len(requested)
        s.model_search_status = ("Searching model IDs and strategy names in PostgreSQL\u2026" if n == 1 else f"Searching {n} model IDs in PostgreSQL\u2026")
        ctx = {"seq": seq, "date": date, "query": query, "search_term": str(search_term)}
        if not is_direct:   # a strategy name: the catalogue says which models match
            return Await("fetchStrategyCatalog", [date], ctx, next="_msearch_cat", catch=True)
        return self._msearch_fetch(requested, ctx | {"direct": True, "truncated": False})

    def _msearch_fetch(self, model_ids, ctx):
        batches = [model_ids[i:i + 10] for i in range(0, len(model_ids), 10)]   # the day endpoint accepts at most ten ids
        return Await("fetchPortfolioDayBatches", [batches, ctx["date"]], ctx | {"model_ids": list(model_ids)}, next="_msearch_1", catch=True)

    def _msearch_conclude(self, query, message):
        s = self.s
        s.search_resolved_query, s.search_resolved_message = query, message
        s.model_search_status = message

    def _msearch_current(self, ctx):
        s = self.s
        return ctx["seq"] == s.search_sequence and ctx["query"] == re.sub(r"\s+", "_", str(s.model_search_input or "").strip().lower()) and ctx["date"] == s.current_date

    def _msearch_cat(self, ctx, result):
        s = self.s
        if "error" in (result or {}):
            if ctx["seq"] == s.search_sequence:
                self._msearch_conclude(ctx["query"], f"Database search failed: {result['error']}")
            return None
        query = ctx["query"]
        matches = [m for m in (result or {}).get("ok") or [] if query in str(m.get("model") or "").lower() or query in str(m.get("strategy") or "").lower()]
        if not self._msearch_current(ctx):
            return None
        if not matches:
            s.search_loaded = []
            s.search_resolved_query = query
            s.search_resolved_message = f"No model ID or strategy name matches \u201c{ctx['search_term']}\u201d for {ctx['date']}"
            self.view("updateDateLabelAndTitle", "updateRibbon", "renderCards", "drawChart")
            s.model_search_status = s.search_resolved_message
            return None
        return self._msearch_fetch([str(m.get("model")) for m in matches[:100]], ctx | {"direct": False, "truncated": len(matches) > 100})

    def _msearch_1(self, ctx, result):
        s = self.s
        seq, date, requested = ctx["seq"], ctx["date"], ctx["model_ids"]
        if "error" in (result or {}):
            if seq == s.search_sequence:
                self._msearch_conclude(ctx["query"], f"Database search failed: {result['error']}")
            return None
        if not self._msearch_current(ctx):
            return None
        by_id = {str(m.get("model") or "").lower(): m for r in (result or {}).get("ok") or [] for m in r}
        s.search_loaded = [by_id[m.lower()] for m in requested if m.lower() in by_id]
        for m in s.search_loaded:
            s.scenario_removed.discard(pu.js_str(m.get("model")))
        missing = [m for m in requested if m.lower() not in by_id]
        if not s.search_loaded:
            s.search_resolved_query = ctx["query"]
            s.search_resolved_message = f"No model data found for {date}{': ' + ', '.join(missing) if missing else ''}"
            self.view("updateDateLabelAndTitle", "updateRibbon", "renderCards", "drawChart")
            s.model_search_status = s.search_resolved_message
            return None
        s.search_resolved_query = ctx["query"]
        s.frame = -1
        requested_ids = {pu.js_str(m.get("model")).lower() for m in s.search_loaded}
        s.visible = {m.get("model") for m in self._eligible() if pu.js_str(m.get("model")).lower() in requested_ids}
        s.selected_model_index = 0
        self.view("updateDateLabelAndTitle", "updateScrubberUI", "updateRibbon", "renderCards", "drawChart")
        c = len(s.search_loaded)
        plural = "" if c == 1 else "s"
        if ctx.get("direct"):
            s.model_search_status = f"{c} model{plural} loaded{' \u00b7 not found: ' + ', '.join(missing) if missing else ''}"
        else:
            s.model_search_status = f"{c} model{plural} match \u201c{ctx['search_term']}\u201d{' \u00b7 showing first 100 matches' if ctx.get('truncated') else ''}"
        if s.pit_mode:   # deep-linked data may arrive after the load: once its series defines the replay head, run the selected-time lookup
            self.schedule_point_in_time_selection()
        return None

    def load_deep_link_models_from_database(self, model_ids):
        return self.run_staged("load_deep_link_models_from_database", model_ids)

    def _deeplink_0(self, model_ids):
        s = self.s
        ids = []
        for raw in model_ids or []:
            i = pu.js_str(raw).strip()
            if MODEL_ID_RE.fullmatch(i) and i not in ids:
                ids.append(i)
        ids = ids[:10]
        if not ids:
            return None
        date = s.current_date
        if not DATE_RE.fullmatch(date or ""):
            s.model_search_status = "Choose a single date to load linked comparison models"
            return None
        n = len(ids)
        s.model_search_status = f"Loading {n} linked comparison strateg{'y' if n == 1 else 'ies'}\u2026"
        return Await("fetchPortfolioDayBatches", [[ids], date], {"ids": ids, "date": date}, next="_deeplink_1", catch=True)

    def _deeplink_1(self, ctx, result):
        s = self.s
        ids, date = ctx["ids"], ctx["date"]
        if "error" in (result or {}):
            s.model_search_status = f"Could not load linked models: {result['error']}"
            return None
        if s.current_date != date:
            return None
        loaded = ((result or {}).get("ok") or [[]])[0]
        for index, model in enumerate(loaded):
            mid = str(model.get("model") or "")
            if not mid:
                continue
            s.pinned[mid] = {**model, "color": model.get("color") or LINKED_COLORS[index % len(LINKED_COLORS)], "comparisonRole": "pinned comparison"}
        loaded_ids = {pu.js_str(m.get("model")) for m in loaded}
        missing = [i for i in ids if i not in loaded_ids]
        s.selected_model_index = 0
        s.visible = {m.get("model") for m in self._eligible()}
        self.view("updateDateLabelAndTitle", "updateScrubberUI", "updateRibbon", "renderCards", "drawChart")
        c = len(loaded)
        word = f"strateg{'y' if c == 1 else 'ies'}"
        miss = f" \u00b7 no data found for {', '.join(missing)}" if missing else ""
        s.model_search_status = (f"Showing {c} selected {word} only{miss} \u00b7 choose a scenario to add scenario leaders" if s.deep_link_only
                                 else f"{c} linked comparison {word} added{miss} \u00b7 change scenario to compare")
        if s.pit_mode:
            s.pit_requested_key = ""
            self._fire_pit(None)
        return None

    def refresh_point_in_time_selection(self, at_override=None):
        p = self.begin_refresh_point_in_time_selection(at_override)
        r = self._await(p)
        self.settle()
        return r

    def begin_refresh_live_data(self, target_date=None, skip_portfolio_refresh=False) -> Pending:
        """refreshLiveData: request now, apply (with the guards, the re-render bookkeeping and the portfolio refresh) later."""
        s = self.s
        if not s.live_date:
            return resolved(None)
        target_date = s.live_date if target_date is None else target_date
        s.live_refresh_sequence += 1
        seq = s.live_refresh_sequence
        req = (s.product_type, s.product, s.strategy_family, s.model_limit, s.return_type, s.current_criteria)
        pending = self.client.begin_refresh_live_data(target_date, product_type=s.product_type, product=s.product,
                                                      strategy_family=s.strategy_family, limit=s.model_limit,
                                                      criteria=s.current_criteria, return_type=s.return_type)
        ctx = {"seq": seq, "req": list(req), "target_date": target_date, "skip": bool(skip_portfolio_refresh)}
        return Pending(lambda: self._apply_live(ctx, pending), issued=pending.issued)

    def _apply_live(self, ctx, pending):
        """The half of refreshLiveData that runs once the answer is in. `ctx` is what the page's closure captured when the request went out
        (so a browser copy can carry it across the fetch: see command.py begin / finish)."""
        seq, req, target_date, skip_portfolio_refresh = ctx["seq"], tuple(ctx["req"]), ctx["target_date"], ctx["skip"]

        def apply():
            s = self.s
            if pending.failed:  # offline: only a newer request makes the answer irrelevant
                if seq == s.live_refresh_sequence:
                    self.view("setLiveBadge")
                return None
            # a newer request or a changed filter makes this response stale
            if seq != s.live_refresh_sequence or req != (s.product_type, s.product, s.strategy_family, s.model_limit, s.return_type,
                                                           s.current_criteria):
                return None
            on_target = s.current_date == target_date
            was_at_end = on_target and (s.frame < 0 or s.frame >= self.max_frames() - 1)
            prev_models = {m.get("model") for m in self._eligible()} if on_target else set()
            self.client.current_product = s.product
            res = pending.finish()
            if not res.get("ok"):
                return None
            self.view("cacheLiveChartResponse", "updateStrategyFamilyOptions", "setLiveBadge")
            s.product = self.client.current_product
            if not on_target or s.is_playing:
                return res
            if s.active_portfolio:
                if str(s.active_portfolio).upper() in LIVE_PORTFOLIOS:
                    raise LivePortfolioRefused(s.active_portfolio)
                if not skip_portfolio_refresh:
                    load = self.begin_load_portfolio_data()

                    def after_load():
                        try:
                            if not load.done:
                                load.finish()
                            s.visible = {m.get("model") for m in s.portfolio_models}
                            # (armed live mode would jump to the newest frame here; live mode is refused headless)
                            self.render_all()
                        except Exception:  # noqa: BLE001 - the page shows 'Portfolio: unavailable'
                            self.view("setLiveBadge")
                    if load.shared:
                        self.defer(after_load, load.root)  # it waits on a request another caller made: that caller resumes first
                    else:
                        try:
                            if not load.done:
                                self._await(load)
                        except Exception:  # noqa: BLE001 - the page's try / catch wraps the await too: 'Portfolio: unavailable'
                            self.view_with("setLiveBadge", "Portfolio: unavailable", "err")
                            return res
                        after_load()
                    return res
            self._live_finish(prev_models, was_at_end)
            return res
        return apply()

    # ---- refreshLiveData in stages (browser copy). The page keeps the data layer (fetch, file the payload in ALL_CRITERIA_DATA, the product filter, the scenario cards, the
    # badges); the engine does the stale-response guards and everything that follows. The live-portfolio tail (orders) stays in the page.
    def _refresh_live_0(self, target_date=None, skip_portfolio_refresh=False):
        s = self.s
        if not s.live_date:
            return None
        target_date = s.live_date if target_date is None else target_date
        s.live_refresh_sequence += 1
        url = self.client.live_day_url(target_date, s.product_type, s.product, s.strategy_family, s.model_limit, s.current_criteria, s.return_type)
        ctx = {"seq": s.live_refresh_sequence, "req": [s.product_type, s.product, s.strategy_family, s.model_limit, s.return_type, s.current_criteria],
               "target_date": target_date, "skip": bool(skip_portfolio_refresh), "scenario": self.client.live_scenario(s.current_criteria, s.return_type)}
        return Await("fetchLiveDay", [url], ctx, next="_refresh_live_1", catch=True)

    def _refresh_live_1(self, ctx, result):
        s = self.s
        if not (result or {}).get("ok"):   # offline: only a newer request makes the answer irrelevant
            if ctx["seq"] == s.live_refresh_sequence:
                self.view_with("setLiveBadge", "Live: offline", "err")
            return None
        if ctx["seq"] != s.live_refresh_sequence or tuple(ctx["req"]) != (s.product_type, s.product, s.strategy_family, s.model_limit, s.return_type, s.current_criteria):
            return None   # a newer request or a changed filter makes this response stale
        on_target = s.current_date == ctx["target_date"]
        was_at_end = on_target and (s.frame < 0 or s.frame >= self.max_frames() - 1)
        prev = sorted({m.get("model") for m in self._eligible()}) if on_target else []
        pt, p, fam, lim, rt, crit = ctx["req"]
        return Await("applyLivePayload", [ctx["target_date"], ctx["scenario"], pt, p, fam, lim, crit, rt],
                     {**ctx, "on_target": on_target, "was_at_end": was_at_end, "prev": prev}, next="_refresh_live_after_data")

    def _refresh_live_after_data(self, ctx, result):
        s = self.s
        if not ctx["on_target"] or s.is_playing:
            return None
        if s.active_portfolio:
            if str(s.active_portfolio).upper() in LIVE_PORTFOLIOS:   # the live-mode screen state (orders live there) stays in the page; the engine resumes after it
                return Await("syncLivePortfolioScreenState", [ctx["target_date"]], ctx, next="_refresh_live_after_sync")
            if not ctx["skip"]:
                return Await("loadPortfolioData", [], ctx, next="_refresh_live_after_load", catch=True)
        self._live_finish(ctx["prev"], ctx["was_at_end"], staged=True)
        return None

    def _refresh_live_after_sync(self, ctx, result):
        s = self.s
        if s.active_portfolio and not ctx["skip"]:
            if not result:   # the sync did not already load a new model
                return Await("loadPortfolioData", [], ctx, next="_refresh_live_after_load", catch=True)
            return self._refresh_live_after_load(ctx, None)
        self._live_finish(ctx["prev"], ctx["was_at_end"], staged=True)
        return None

    def _refresh_live_after_load(self, ctx, result):
        s = self.s
        if (result or {}).get("error"):   # the page shows 'Portfolio: unavailable'
            self.view_with("setLiveBadge", "Portfolio: unavailable", "err")
            return None
        s.visible = {m.get("model") for m in s.portfolio_models}
        if self.flags.get("liveArmed") and ctx["target_date"] == s.live_date:
            s.frame = max(0, self.max_frames() - 1)
        self.render_all()
        return None

    def _live_finish(self, prev_models, was_at_end, staged=False):
        """The end of refreshLiveData when no portfolio refresh follows: new models become visible, the head and baseline are clamped, the view redraws."""
        s = self.s
        prev_models = set(prev_models)
        for m in self._eligible():
            if m.get("model") not in prev_models:
                s.visible.add(m.get("model"))
        max_f = self.max_frames()
        if was_at_end or s.frame > max_f - 1:
            s.frame = max_f - 1
        if s.baseline > max_f - 1:
            s.baseline = 0
        self.view("updateScrubberUI", "updateRibbon", "renderCards", "drawChart")
        if staged:
            self._call("schedulePointInTimeSelection")
        else:
            self.schedule_point_in_time_selection()

    def refresh_live_data(self, target_date=None, skip_portfolio_refresh=False):
        r = self._await(self.begin_refresh_live_data(target_date, skip_portfolio_refresh))
        self.settle()
        return r

    # ------------------------------------------------------------------ portfolio data
    def begin_load_portfolio_data(self, prefer_cache=True) -> Pending:
        """loadPortfolioData() for the active portfolio and the current date; resolves to True if it had to fetch."""
        s = self.s
        if not s.active_portfolio:
            return resolved(None)
        models = s.portfolios.get(s.active_portfolio) or []
        self._push_models()
        p = self.client.begin_load_portfolio_data(models, s.current_date, prefer_cache, s.active_portfolio)
        self._pull_models()
        for bg in self.client.background:  # a stale cache hit revalidates in the background
            self._fire(bg)
        self.client.background = []

        def apply():
            self._push_models()
            r = p.finish()
            self._pull_models()
            self.auto_pin_live_portfolio_strategies()
            return r["fetched"]
        out = Pending(apply, issued=p.issued)
        out.shared, out.root = p.shared, p.root
        return out

    def load_portfolio_data(self, prefer_cache=True):
        r = self._await(self.begin_load_portfolio_data(prefer_cache))
        self.settle()
        return r

    def auto_pin_live_portfolio_strategies(self):
        s = self.s
        if s.current_date != s.live_date or str(s.active_portfolio or "").upper() not in LIVE_PORTFOLIOS:
            return
        for model in s.portfolio_models:
            mid = str((model or {}).get("model") or "").strip()
            if not mid:
                continue
            s.pinned[mid] = {**model, "comparisonRole": "live trade strategy"}
        s.visible = {m.get("model") for m in self._eligible()}

    # ------------------------------------------------------------------ portfolio store
    def move_portfolio(self, name, offset) -> bool:
        s = self.s
        names = list(s.portfolios)
        frm = names.index(name) if name in names else -1
        off = pu._number(offset)
        to = frm + off
        if frm < 0 or to != to or to < 0 or to >= len(names) or to != int(to):
            return False
        to = int(to)
        names[frm], names[to] = names[to], names[frm]
        s.portfolios = {n: s.portfolios[n] for n in names}
        self.fx("savePortfolios")
        self.fx("renderPortfolioList")
        return True

    def unique_portfolio_name(self, base_name: str) -> str:
        s = self.s
        compact = base_name[:32]
        if not _truthy(s.portfolios.get(compact)):
            return compact
        suffix = 2
        while _truthy(s.portfolios.get(f"{compact[:28]} {suffix}")):
            suffix += 1
        return f"{compact[:28]} {suffix}"

    def mark_portfolio_fixed(self, name):
        s = self.s
        if not name or not _truthy(s.portfolio_scenario_configs.get(name)):
            return
        del s.portfolio_scenario_configs[name]
        self.fx("saveCriteriaWorkspaces")
        if s.active_portfolio == name and s.pit_mode:
            s.pit_mode = False
            s.pit_models = None
            s.pit_requested_key = ""
            s.pit_request_sequence += 1
            self.view("updatePointInTimeToggleUI")

    def capture_portfolio_scenario(self, name, criteria=None):
        s = self.s
        criteria = s.current_criteria if criteria is None else criteria
        s.portfolio_scenario_configs[name] = {"criteria": criteria, "returnType": s.return_type, "productType": s.product_type,
                                              "product": s.product, "strategyFamily": s.strategy_family, "limit": s.model_limit,
                                              "minWinRate": s.min_win_rate}
        s.portfolio_view_configs[name] = self.current_portfolio_view_config()
        self.fx("localStorage.setItem", "strategyDirectoryPortfolioViewV1")
        s.portfolio_criteria[name] = criteria
        self.fx("saveCriteriaWorkspaces")

    def get_merged_portfolio_models(self) -> list:
        out = []
        for name in self.s.merge_selection:
            for m in self.s.portfolios.get(name) or []:
                if m not in out:
                    out.append(m)
        return out

    def _reload_active_view(self, reset_index=False):
        self._await(self.begin_load_portfolio_data())
        self._reload_suffix(reset_index)

    def _reload_suffix(self, reset_index=False):
        s = self.s
        s.visible = {m.get("model") for m in s.portfolio_models}
        if reset_index:
            s.selected_model_index = 0
        s.frame = self.max_frames() - 1
        self.render_all()

    def remove_model_from_portfolio(self, name, model):
        return self.run_staged("remove_model_from_portfolio", name, model)

    def _remove_model_0(self, name, model):
        s = self.s
        if name not in s.portfolios:
            return None
        self.mark_portfolio_fixed(name)
        s.portfolios[name] = [i for i in s.portfolios[name] if i != model]
        self.fx("savePortfolios")
        if s.active_portfolio == name:
            return Await("loadPortfolioData")
        self.fx("renderPortfolioList")
        return None

    def _remove_model_1(self, ctx, result):
        self._reload_suffix(reset_index=True)
        self.fx("renderPortfolioList")

    def add_catalogue_model(self, name, model):
        return self.run_staged("add_catalogue_model", name, model)

    def _add_catalogue_0(self, name, model):
        s = self.s
        if not name or name not in s.portfolios:
            return None
        if model in s.portfolios[name]:
            return None
        if len(s.portfolios[name]) >= 10:
            return None  # the page alerts "already contains the maximum of 10 strategies"
        self.mark_portfolio_fixed(name)
        s.portfolios[name].append(model)
        self.fx("savePortfolios")
        self.view("populateCataloguePortfolioOptions")
        if s.active_portfolio == name:
            return Await("loadPortfolioData")
        self.fx("renderPortfolioList")
        self.view("renderStrategyCatalogue")
        return None

    def _add_catalogue_1(self, ctx, result):
        self._reload_suffix()
        self.fx("renderPortfolioList")
        self.view("renderStrategyCatalogue")

    def move_model_between_portfolios(self, src, dst, model):
        return self.run_staged("move_model_between_portfolios", src, dst, model)

    def _move_model_0(self, src, dst, model):
        s = self.s
        if not src or not dst or src == dst:
            return None
        if model not in (s.portfolios.get(src) or []) or dst not in s.portfolios:
            return None
        if model not in s.portfolios[dst] and len(s.portfolios[dst]) >= 10:
            self.fx("renderPortfolioList")  # (the page alerts first)
            return None
        s.portfolios[src] = [i for i in s.portfolios[src] if i != model]
        if model not in s.portfolios[dst]:
            s.portfolios[dst].append(model)
        self.mark_portfolio_fixed(src)
        self.mark_portfolio_fixed(dst)
        self.fx("savePortfolios")
        if s.active_portfolio in (src, dst):
            return Await("loadPortfolioData")
        self.fx("renderPortfolioList")
        return None

    def _move_model_1(self, ctx, result):
        self._reload_suffix(reset_index=True)
        self.fx("renderPortfolioList")

    def remove_portfolios(self, names):
        s = self.s
        was_active = s.active_portfolio in names
        for name in names:
            s.portfolios.pop(name, None)
            s.portfolio_criteria.pop(name, None)
            s.portfolio_scenario_configs.pop(name, None)
            s.portfolio_view_configs.pop(name, None)
            if name in s.merge_selection:
                s.merge_selection.remove(name)
        self.fx("localStorage.setItem", "strategyDirectoryPortfolioViewV1")
        if was_active:
            s.active_portfolio = None
            self.view("syncLiveAltReporting")
            s.portfolio_models = []
            self.apply_portfolio_view_config(s.main_view_config or {"criteria": s.main_criteria})
            s.main_criteria = s.current_criteria
        self.fx("saveCriteriaWorkspaces")
        self.fx("savePortfolios")
        if was_active:
            self.view("updateScenarioUI")
            self._await(self.begin_refresh_live_data(s.current_date))
            self.switch_date(s.current_date)
        self.fx("renderPortfolioList")
        self.settle()

    # staged form (browser copy): the two awaits are page async functions (refreshLiveData, switchDate)
    def _remove_portfolios_0(self, names):
        s = self.s
        was_active = s.active_portfolio in names
        for name in names:
            s.portfolios.pop(name, None)
            s.portfolio_criteria.pop(name, None)
            s.portfolio_scenario_configs.pop(name, None)
            s.portfolio_view_configs.pop(name, None)
            if name in s.merge_selection:
                s.merge_selection.remove(name)
        self.fx("localStorage.setItem", "strategyDirectoryPortfolioViewV1")
        if was_active:
            s.active_portfolio = None
            self.view("syncLiveAltReporting")
            s.portfolio_models = []
            return Await("applyPortfolioViewConfig", [s.main_view_config or {"criteria": s.main_criteria}], {"was_active": True}, next="_remove_portfolios_0b", sync=True)
        return self._remove_portfolios_0b({"was_active": False}, None)

    def _remove_portfolios_0b(self, ctx, result):
        s = self.s
        if ctx["was_active"]:
            s.main_criteria = s.current_criteria
        self.fx("saveCriteriaWorkspaces")
        self.fx("savePortfolios")
        if ctx["was_active"]:
            self.view("updateScenarioUI")
            return Await("refreshLiveData", [s.current_date], next="_remove_portfolios_1")
        self.fx("renderPortfolioList")
        return None

    def _remove_portfolios_1(self, ctx, result):
        return Await("switchDate", [self.s.current_date], next="_remove_portfolios_2")

    def _remove_portfolios_2(self, ctx, result):
        self.fx("renderPortfolioList")
        return None

    def delete_portfolio(self, name, confirmed=True):
        if name not in self.s.portfolios or not confirmed:
            return
        self.remove_portfolios([name])

    def delete_selected_portfolios(self, confirmed=True):
        names = [n for n in self.s.merge_selection if n in self.s.portfolios]
        if not names or not confirmed:
            return
        self.remove_portfolios(names)

    def repopulate_active_portfolio_from_criteria(self):
        return self.run_staged("repopulate_active_portfolio_from_criteria")

    def _repopulate_0(self):
        s = self.s
        if not s.active_portfolio:
            return None
        name = s.active_portfolio
        s.portfolios[name] = [m.get("model") for m in self._candidates()[:10]]
        self.capture_portfolio_scenario(name, s.current_criteria)
        self.fx("savePortfolios")
        return Await("loadPortfolioData")

    def _repopulate_1(self, ctx, result):
        s = self.s
        s.visible = {m.get("model") for m in s.portfolio_models}
        s.selected_model_index = 0
        s.frame = self.max_frames() - 1
        s.baseline = 0
        if s.pit_mode:
            self._call("schedulePointInTimeSelection")

    def create_similar_portfolio(self, dimension):
        return self.run_staged("create_similar_portfolio", dimension)

    def _similar_0(self, dimension):
        s = self.s
        payload = s.similar_payload or {}
        group = (payload.get("groups") or {}).get(dimension) or []
        reference = payload.get("reference")
        if not reference or not group:
            return None
        label = {"family": "Family", "window": "Window", "tp": "TP", "sl": "SL"}.get(dimension)
        win = "" if reference.get("window") is None else f" W{pu.js_str(reference['window'])}"
        name = self.unique_portfolio_name(f"{str(reference.get('product')).upper()} {label}{win} T{pu.js_str(reference.get('tp'))} S{pu.js_str(reference.get('sl'))}")
        s.portfolios[name] = [i.get("model") for i in group][:10]
        s.portfolio_scenario_configs.pop(name, None)
        s.portfolio_view_configs.pop(name, None)
        s.portfolio_criteria[name] = s.current_criteria
        self.fx("saveCriteriaWorkspaces")
        self.fx("savePortfolios")
        s.model_search_input = ""
        s.search_loaded = []
        s.pinned.clear()
        s.search_sequence += 1
        self._clear_timer("modelSearchTimer")
        s.portfolio_view_configs[name] = self.current_portfolio_view_config()
        self.dom("similarStrategyModal", "call", "close")
        return Await("activatePortfolio", [name], {"name": name}, next="_similar_1")

    def _similar_1(self, ctx, result):
        return None

    def livePortfolioModelsForDate(self, *a, **k):  # pragma: no cover - alias kept for readability when comparing with the page
        return self.live_portfolio_models_for_date(*a, **k)

    def live_portfolio_models_for_date(self, name, target_date, active_model=None) -> list:
        s = self.s
        pname = str(name or "").upper()
        seen, models = set(), []

        def add(m):
            i = str(m or "").strip()
            if i and i not in seen:
                seen.add(i)
                models.append(i)

        def local_date(value):
            from datetime import datetime
            try:
                v = str(value)
                d = datetime.fromisoformat(v)
                if d.tzinfo is not None:
                    d = d.astimezone()
                return f"{d.year:04d}-{d.month:02d}-{d.day:02d}"
            except (ValueError, TypeError):
                return ""

        store = s.live_store or {}
        events = [e for e in (store.get("events") or []) if str(e.get("portfolio") or "").upper() == pname
                  and local_date(stm.js_or(e.get("switched_at"), e.get("activated_at"), e.get("deactivated_at"))) == target_date]
        events.sort(key=lambda e: str(e.get("switched_at") or ""))
        for e in events:
            add(e.get("from_model"))
            add(e.get("to_model"))
        last = ((store.get("states") or {}).get(pname) or {}).get("last_switch")
        if last and local_date(stm.js_or(last.get("switched_at"), last.get("activated_at"), last.get("deactivated_at"))) == target_date:
            add(last.get("from_model"))
            add(last.get("to_model"))
        if target_date == s.live_date:
            add(stm.js_or(active_model, ((store.get("states") or {}).get(pname) or {}).get("active_model")))
        if not models:
            for m in s.portfolios.get(name) or []:
                add(m)
        return models

    def sync_portfolio_view_refresh(self):
        s = self.s
        if s.portfolio_refresh_timer is not None:
            self._timer_op("clearInterval", "clear", "portfolioViewRefreshTimer")
            s.portfolio_refresh_timer = None
        if not s.active_portfolio or s.current_date != s.live_date:
            return
        ms = pu.PORTFOLIO_VIEW_REFRESH_MS if hasattr(pu, "PORTFOLIO_VIEW_REFRESH_MS") else 300000
        self._timer_op("setInterval", "set", "portfolioViewRefreshTimer", ms=ms, call="refreshActivePortfolioView")
        s.portfolio_refresh_timer = 1

    def refresh_active_portfolio_view(self):
        s = self.s
        if s.live_refresh_in_flight or not s.active_portfolio or s.current_date != s.live_date:
            return
        name = s.active_portfolio
        if not (s.portfolios.get(name) or []):
            return
        was_latest = s.frame < 0 or s.frame >= self.max_frames() - 1
        s.live_refresh_in_flight = True
        try:
            self._await(self.begin_load_portfolio_data())
            if s.active_portfolio != name or s.current_date != s.live_date:
                return
            if was_latest:
                s.frame = self.max_frames() - 1
            s.visible = {m.get("model") for m in self._eligible()}
            self.render_all()
        except Exception:  # noqa: BLE001
            pass
        finally:
            s.live_refresh_in_flight = False
        self.settle()

    # staged form (browser copy) of refresh_active_portfolio_view
    def _refresh_view_0(self):
        s = self.s
        if s.live_refresh_in_flight or not s.active_portfolio or s.current_date != s.live_date:
            return None
        name = s.active_portfolio
        if not (s.portfolios.get(name) or []):
            return None
        was_latest = s.frame < 0 or s.frame >= self.max_frames() - 1
        s.live_refresh_in_flight = True
        return Await("loadPortfolioData", [], {"name": name, "was_latest": was_latest}, next="_refresh_view_1", catch=True)

    def _refresh_view_1(self, ctx, result):
        s = self.s
        try:
            if (result or {}).get("error"):   # the page only warns
                return None
            if s.active_portfolio != ctx["name"] or s.current_date != s.live_date:
                return None
            if ctx["was_latest"]:
                s.frame = self.max_frames() - 1
            s.visible = {m.get("model") for m in self._eligible()}
            self.render_all()
            return None
        finally:
            s.live_refresh_in_flight = False

    # ------------------------------------------------------------------ navigation
    def activate_portfolio(self, name):
        """activatePortfolio for an ordinary portfolio: the state transition and the first paint. Live portfolios are refused."""
        s = self.s
        if str(name).upper() in LIVE_PORTFOLIOS:
            raise LivePortfolioRefused(name)
        self.persist_portfolio_view_config(s.active_portfolio if s.active_portfolio else None)
        raw_saved = s.portfolio_view_configs.get(name)
        saved = raw_saved or {}
        saved_date = saved.get("date")
        saved_replay = str(pu.js_str(stm.js_or(saved.get("replayHeadTime"), "")))
        saved_selection = str(pu.js_str(stm.js_or(saved.get("selectedAtTime"), "")))
        if any(d.get("id") == saved_date for d in s.available_dates) and saved_date != s.current_date:  # v2.65.34: an unchanged date does not rebuild the tabs
            s.current_date = saved_date
            self.view("setupDateTabs")
        rules_ready = self.client.begin_load_overlay_rule_library()  # requested first, applied after the portfolio paints
        dynamic = s.portfolio_scenario_configs.get(name) or None
        s.pit_mode = bool(dynamic and s.pit_selection_preference)
        s.pit_models = [] if s.pit_mode else None
        s.pit_requested_key = ""
        s.pit_request_sequence += 1
        s.pending_explicit_time = None
        s.explicit_refresh = False
        s.auto_request_at = None
        s.auto_context = ""
        s.deep_link_only = False
        s.active_portfolio = name
        self.view("syncLiveModeUI", "syncLiveAltReporting")
        s.chart_lock_before_live = saved["chartLockBeforeLive"] if isinstance(saved.get("chartLockBeforeLive"), bool) else None
        saved_view = raw_saved if raw_saved is not None else (dynamic if dynamic else {
            "criteria": stm.js_or(s.portfolio_criteria.get(name), s.main_criteria), "returnType": "NET", "productType": "all", "product": "all",
            "strategyFamily": "all", "limit": 10, "minWinRate": 0, "chartLocked": False})
        self.apply_portfolio_view_config({
            **saved_view,
            "splitMode": saved_view.get("splitMode") if saved_view.get("splitMode") in pu.SPLIT_MODES else "ALL_NET",
            "chartLocked": saved["chartLocked"] if isinstance(saved.get("chartLocked"), bool) else False,
            "useAssignedOverlayRule": saved["useAssignedOverlayRule"] if isinstance(saved.get("useAssignedOverlayRule"), bool)
            else bool(self.assigned_portfolio_overlay_rule(name))})
        s.portfolio_view_configs[name] = self.current_portfolio_view_config()
        self.fx("localStorage.setItem", "strategyDirectoryPortfolioViewV1")
        self.view("updatePointInTimeToggleUI", "renderPortfolioTabs", "updateScenarioUI", "setLiveBadge")
        activation_date = s.current_date
        activation_key = ",".join(s.portfolios.get(name) or [])

        def render(data_settled=False):
            if s.active_portfolio != name or s.current_date != activation_date:
                return
            self.auto_pin_live_portfolio_strategies()
            s.visible = {m.get("model") for m in s.portfolio_models}
            s.selected_model_index = 0
            timeline = None
            for m in s.portfolio_models:
                if len(m.get("series") or []) > len((timeline or {}).get("series") or []):
                    timeline = m
            saved_minute = time_of_day_minutes(saved_replay)
            if timeline and timeline.get("series") and saved_minute is not None:
                idx = -1
                for i, pt in enumerate(timeline["series"]):
                    mn = time_of_day_minutes(pt.get("time"))
                    if mn is not None and mn <= saved_minute:
                        idx = i
                s.frame = idx if idx >= 0 else 0
            else:
                s.frame = max(0, self.max_frames() - 1)
            self.view("updateDateLabelAndTitle", "updateRibbon", "renderCards", "drawChart", "updateScrubberUI")
            if re.fullmatch(r"[0-9]{2}:[0-9]{2}", saved_selection):
                s.selected_time_input = saved_selection
            self.persist_portfolio_view_config(name)
            self.view("renderLivePortfolioTransition", "syncLiveModeUI")
            if s.portfolio_models or data_settled:
                self.view("setLiveBadge")
            if s.pit_mode:
                self.schedule_point_in_time_selection()

        load = self.begin_load_portfolio_data(True)
        render()

        def after_load():
            try:
                needs_final = load.finish()
            except Exception:  # noqa: BLE001 - 'Portfolio: unavailable'
                if s.active_portfolio == name and s.current_date == activation_date:
                    self.view("setLiveBadge")
                return None
            if not needs_final:
                return None
            if s.active_portfolio != name or s.current_date != activation_date or ",".join(s.portfolios.get(name) or []) != activation_key:
                return None
            render(True)
            return None
        self._fire(Pending(after_load, issued=load.issued))
        self._fire(rules_ready)
        if s.active_portfolio == name:   # reached before the (un-awaited) load answers
            self.view("syncAssignedOverlayRuleUI", "drawChart")
        self.settle()

    # ---- activatePortfolio in stages (browser copy), non-live portfolios. The page starts loadOverlayRuleLibrary and loadPortfolioData and keeps their promises; the continuations
    # (.then) run later as their own stages. A live portfolio is refused: the page runs its own copy of the original.
    def _act_0(self, name):
        s = self.s
        if str(name).upper() in LIVE_PORTFOLIOS:
            raise LivePortfolioRefused(name)
        self.persist_portfolio_view_config(s.active_portfolio if s.active_portfolio else None)
        raw_saved = s.portfolio_view_configs.get(name)
        saved = raw_saved or {}
        saved_date = saved.get("date")
        saved_replay = str(pu.js_str(stm.js_or(saved.get("replayHeadTime"), "")))
        saved_selection = str(pu.js_str(stm.js_or(saved.get("selectedAtTime"), "")))
        if any(d.get("id") == saved_date for d in s.available_dates) and saved_date != s.current_date:  # v2.65.34: an unchanged date does not rebuild the tabs
            s.current_date = saved_date
            self.view("setupDateTabs")
            if DATE_RE.fullmatch(s.current_date or ""):
                self._call("__switchDateUrl", s.current_date)
        ctx = {"name": name, "saved_replay": saved_replay, "saved_selection": saved_selection}
        return Await("loadOverlayRuleLibrary", [], ctx, next="_act_1", fire=True, handle="rules")

    def _act_1(self, ctx, result):
        s = self.s
        name = ctx["name"]
        raw_saved = s.portfolio_view_configs.get(name)
        saved = raw_saved or {}
        dynamic = s.portfolio_scenario_configs.get(name) or None
        s.pit_mode = bool(dynamic and s.pit_selection_preference)
        s.pit_models = [] if s.pit_mode else None
        s.pit_requested_key = ""
        s.pit_request_sequence += 1
        s.pending_explicit_time = None
        s.explicit_refresh = False
        s.auto_request_at = None
        s.auto_context = ""
        self.pending_button(False)
        s.deep_link_only = False
        s.active_portfolio = name
        self.view("syncLiveModeUI", "syncLiveAltReporting")
        s.chart_lock_before_live = saved["chartLockBeforeLive"] if isinstance(saved.get("chartLockBeforeLive"), bool) else None
        saved_view = raw_saved if raw_saved is not None else (dynamic if dynamic else {
            "criteria": stm.js_or(s.portfolio_criteria.get(name), s.main_criteria), "returnType": "NET", "productType": "all", "product": "all",
            "strategyFamily": "all", "limit": 10, "minWinRate": 0, "chartLocked": False})
        config = {
            **saved_view,
            "splitMode": saved_view.get("splitMode") if saved_view.get("splitMode") in pu.SPLIT_MODES else "ALL_NET",
            "chartLocked": saved["chartLocked"] if isinstance(saved.get("chartLocked"), bool) else False,
            "useAssignedOverlayRule": saved["useAssignedOverlayRule"] if isinstance(saved.get("useAssignedOverlayRule"), bool)
            else bool(self.assigned_portfolio_overlay_rule(name))}
        return Await("applyPortfolioViewConfig", [config], ctx, next="_act_1b", sync=True)   # the page's own (delegated, with its own fallback) function

    def _act_1b(self, ctx, result):
        s = self.s
        name = ctx["name"]
        s.portfolio_view_configs[name] = self.current_portfolio_view_config()
        self.fx("localStorage.setItem", "strategyDirectoryPortfolioViewV1")
        self.view("updatePointInTimeToggleUI", "renderPortfolioTabs", "updateScenarioUI")
        self.view_with("setLiveBadge", f"Loading portfolio {name}\u2026", "idle")
        ctx2 = {**ctx, "activation_date": s.current_date, "activation_key": ",".join(s.portfolios.get(name) or [])}
        return Await("loadPortfolioData", [{"preferCache": True}], ctx2, next="_act_2", fire=True, handle="load")

    def _act_2(self, ctx, result):
        self._act_render(ctx, False)   # the cached curves paint at once, before the load answers
        return Await("__attach", ["load"], ctx, next="_act_3", attach="_act_load_done")

    def _act_3(self, ctx, result):
        return Await("__attach", ["rules"], ctx, next="_act_4", attach="_act_rules_done")

    def _act_4(self, ctx, result):
        return None

    def _act_render(self, ctx, data_settled):
        s = self.s
        name = ctx["name"]
        if s.active_portfolio != name or s.current_date != ctx["activation_date"]:
            return
        self.auto_pin_live_portfolio_strategies()
        s.visible = {m.get("model") for m in s.portfolio_models}
        s.selected_model_index = 0
        timeline = None
        for m in s.portfolio_models:
            if len(m.get("series") or []) > len((timeline or {}).get("series") or []):
                timeline = m
        saved_minute = time_of_day_minutes(ctx["saved_replay"])
        if timeline and timeline.get("series") and saved_minute is not None:
            idx = -1
            for i, pt in enumerate(timeline["series"]):
                mn = time_of_day_minutes(pt.get("time"))
                if mn is not None and mn <= saved_minute:
                    idx = i
            s.frame = idx if idx >= 0 else 0
        else:
            s.frame = max(0, self.max_frames() - 1)
        self.view("updateDateLabelAndTitle", "updateRibbon", "renderCards", "drawChart", "updateScrubberUI")
        if re.fullmatch(r"[0-9]{2}:[0-9]{2}", ctx["saved_selection"]):
            s.selected_time_input = ctx["saved_selection"]
        self.persist_portfolio_view_config(name)
        self.view("renderLivePortfolioTransition", "syncLiveModeUI")
        if s.portfolio_models or data_settled:
            self.view_with("setLiveBadge", f"Portfolio \u00b7 {name}", "ok")
        if s.pit_mode:
            self._call("schedulePointInTimeSelection")

    def _act_load_done(self, ctx, result):
        s = self.s
        name = ctx["name"]
        if (result or {}).get("error"):   # 'Portfolio: unavailable'
            if s.active_portfolio == name and s.current_date == ctx["activation_date"]:
                self.view_with("setLiveBadge", "Portfolio: unavailable", "err")
            return None
        if not (result or {}).get("ok"):   # the load did not fetch: nothing new to paint
            return None
        if s.active_portfolio != name or s.current_date != ctx["activation_date"] or ",".join(s.portfolios.get(name) or []) != ctx["activation_key"]:
            return None
        self._act_render(ctx, True)
        return None

    def _act_rules_done(self, ctx, result):
        s = self.s
        if (result or {}).get("error") or s.active_portfolio != ctx["name"]:
            return None
        self.view("syncAssignedOverlayRuleUI", "drawChart")
        return None

    def switch_date(self, date_key, skip_portfolio_load=False, refresh_data=False):
        s = self.s
        s.date_switch_sequence += 1
        seq = s.date_switch_sequence
        date_data = self.begin_refresh_live_data(date_key) if (refresh_data and DATE_RE.fullmatch(date_key or "")) else None
        self.pause_replay()
        s.search_sequence += 1
        self._clear_timer("modelSearchTimer")
        s.search_loaded = []
        if date_key != s.current_date:
            s.pinned.clear()
            s.pit_timeline_models = []
        if s.current_criteria == "top1_at_time":
            s.pit_models = []
        s.current_date = date_key
        self.persist_portfolio_view_config()
        self.view("scheduleLiveChartCacheFallback")
        if date_key != s.live_date and not refresh_data:
            self.tick()
            try:
                self.client.ensure_historical_data(date_key)
            except Exception:  # noqa: BLE001 - 'Historical chart data load failed' is only warned about
                pass
            if seq != s.date_switch_sequence or s.current_date != date_key:
                return
        s.pit_requested_key = ""
        s.pit_request_sequence += 1
        self._clear_timer("pointInTimeDebounceTimer")
        if date_data is not None:
            self._fire(date_data)
        if not DATE_RE.fullmatch(s.current_date or "") and s.pit_mode:
            s.pit_mode = False
            s.pit_models = None
            s.pit_requested_key = ""
            s.pit_request_sequence += 1
            self.view("updatePointInTimeToggleUI")
        s.baseline = 0
        if s.active_portfolio and not skip_portfolio_load:
            try:
                self._await(self.begin_load_portfolio_data())
            except Exception:  # noqa: BLE001
                s.portfolio_models = []
        self.view("updateDateLabelAndTitle", "updateStrategyFamilyOptions")
        max_f = self.max_frames()
        s.frame = max_f - 1
        s.visible = {m.get("model") for m in self._eligible()}
        s.selected_model_index = 0
        self.view("updateScrubberUI")
        self.persist_portfolio_view_config()
        self.view("updateRibbon", "renderCards", "drawChart")
        self.schedule_point_in_time_selection()
        self.sync_portfolio_view_refresh()
        query = str(s.model_search_input or "").strip()
        deep = getattr(self, "deep_link_model", None)
        is_deep = bool(deep and query and str(deep).lower() == query.lower())
        if not is_deep and query and len(query) >= 3 and re.fullmatch(r"[a-z0-9._;,\s-]+", query, re.I):   # v2.65.35: strategy names (3+ characters, spaces and commas allowed)
            self._timeout(lambda: None, 350, "modelSearchTimer", "loadModelSearchFromDatabase", [query])
        self.settle()

    # ---- switchDate in stages (browser copy). Awaited page functions: refreshLiveData (started, not waited for), ensureHistoricalDataLoaded, loadPortfolioData,
    # schedulePointInTimeSelection (the page's own, delegated, copy). Page-only DOM (the URL, the date pills) is asked of the page by name.
    def _switch_0(self, date_key, skip_portfolio_load=False, refresh_data=False):
        s = self.s
        s.date_switch_sequence += 1
        ctx = {"seq": s.date_switch_sequence, "date": date_key, "skip": bool(skip_portfolio_load), "refresh": bool(refresh_data), "hist": False}
        if refresh_data and DATE_RE.fullmatch(date_key or ""):
            return Await("refreshLiveData", [date_key], ctx, next="_switch_1", fire=True)
        return self._switch_1(ctx, None)

    def _switch_1(self, ctx, result):
        s = self.s
        date_key = ctx["date"]
        self.pause_replay()
        s.search_sequence += 1
        self._clear_timer("modelSearchTimer")
        s.search_loaded = []
        if date_key != s.current_date:
            s.pinned.clear()
            s.pit_timeline_models = []
        if s.current_criteria == "top1_at_time":
            s.pit_models = []
        s.current_date = date_key
        self.persist_portfolio_view_config()
        self.view_with("scheduleLiveChartCacheFallback", date_key)
        if date_key != s.live_date and not ctx["refresh"]:
            return Await("ensureHistoricalDataLoaded", [date_key], {**ctx, "hist": True}, next="_switch_2", catch=True)
        return self._switch_2(ctx, None)

    def _switch_2(self, ctx, result):
        s = self.s
        date_key = ctx["date"]
        if ctx["hist"] and (ctx["seq"] != s.date_switch_sequence or s.current_date != date_key):
            return None
        if DATE_RE.fullmatch(date_key or ""):
            self._call("__switchDateUrl", date_key)
        s.pit_requested_key = ""
        s.pit_request_sequence += 1
        self._clear_timer("pointInTimeDebounceTimer")
        if not DATE_RE.fullmatch(s.current_date or "") and s.pit_mode:
            s.pit_mode = False
            s.pit_models = None
            s.pit_requested_key = ""
            s.pit_request_sequence += 1
            self.view("updatePointInTimeToggleUI")
        s.baseline = 0
        if s.active_portfolio and not ctx["skip"]:
            return Await("loadPortfolioData", [], ctx, next="_switch_3", catch=True)
        return self._switch_3(ctx, None)

    def _switch_3(self, ctx, result):
        s = self.s
        if (result or {}).get("error"):   # the page warns and shows no portfolio curves
            s.portfolio_models = []
        self.view("updateDateLabelAndTitle", "updateStrategyFamilyOptions")
        self._call("__switchDatePills")
        s.frame = self.max_frames() - 1
        s.visible = {m.get("model") for m in self._eligible()}
        s.selected_model_index = 0
        self.view("updateScrubberUI")
        self.persist_portfolio_view_config()
        self.view("updateRibbon", "renderCards", "drawChart")
        return Await("schedulePointInTimeSelection", [], ctx, next="_switch_4", sync=True)

    def _switch_4(self, ctx, result):
        s = self.s
        self.sync_portfolio_view_refresh()
        query = str(s.model_search_input or "").strip()
        deep = getattr(self, "deep_link_model", None)
        is_deep = bool(deep and query and str(deep).lower() == query.lower())
        if not is_deep and query and len(query) >= 3 and re.fullmatch(r"[a-z0-9._;,\s-]+", query, re.I):   # v2.65.35: strategy names (3+ characters, spaces and commas allowed)
            self._timeout(lambda: None, 350, "modelSearchTimer", "loadModelSearchFromDatabase", [query])
        return None

    def set_ranking_criteria(self, criteria):
        return self.run_staged("set_ranking_criteria", criteria)

    def _rank_0(self, criteria):
        s = self.s
        is_top1 = criteria == "top1_at_time"
        was_top1 = s.current_criteria == "top1_at_time"
        if (s.current_criteria == criteria and (not s.active_portfolio or s.portfolio_scenario_configs.get(s.active_portfolio))
                and not is_top1 and not s.deep_link_only):
            return None
        s.deep_link_only = False
        if criteria != s.current_criteria:
            s.pit_requested_key = ""
            s.pit_request_sequence += 1
            s.pending_explicit_time = None
            s.explicit_refresh = False
            self.pending_button(False)
        if criteria != s.current_criteria and s.pit_mode and not is_top1 and not was_top1:
            s.pit_requested_key = ""
            s.pit_request_sequence += 1
            s.pending_explicit_time = None
            s.explicit_refresh = False
            s.pit_models = []
            s.history.clear()
            s.history_context = ""
        if is_top1 and not was_top1:
            s.top1_prev_mode = s.pit_mode
            s.pit_mode = True
            s.pit_models = []
        elif not is_top1 and was_top1:
            s.pit_mode = bool(s.top1_prev_mode or s.auto_enabled)
            s.top1_prev_mode = None
            s.pit_models = [] if s.pit_mode else None
        if is_top1 or was_top1:
            s.pit_requested_key = ""
            s.pit_request_sequence += 1
            s.pit_history_key = ""
            s.pit_history_sequence += 1
            s.pending_explicit_time = None
            if was_top1 and not is_top1:
                s.history.clear()
                s.history_context = ""
                s.search_sequence += 1
                self._clear_timer("modelSearchTimer")
                s.search_loaded = []
                s.model_search_input = ""
        if criteria in MOMENTUM_SCENARIO_IDS and not s.active_portfolio:
            s.rank_select_value = "3"
            self.dom("applySelectedTimeBtn", "set", "textContent", "Refresh & Add #1–#3")
            s.pit_mode = True
            s.pit_models = []
            s.history.clear()
            s.history_context = ""
        if is_top1 and s.active_portfolio:
            s.active_portfolio = None
            self.view("syncLiveAltReporting", "renderPortfolioTabs")
            s.portfolio_models = []
        s.current_criteria = criteria
        self.view("updatePointInTimeToggleUI")
        ctx = {"criteria": criteria, "is_top1": is_top1}
        if s.active_portfolio:
            name = s.active_portfolio
            s.portfolio_criteria[name] = criteria
            self.fx("saveCriteriaWorkspaces")
            self.persist_portfolio_view_config(name)
            self.view_with("setLiveBadge", f"Portfolio · {name} · refreshing in background", "idle")
            return Await("refreshLiveData", [s.current_date, True], {**ctx, "name": name}, next="_rank_portfolio_1", fire=True)
        s.main_criteria = criteria
        self.fx("saveCriteriaWorkspaces")
        if not is_top1 and DATE_RE.fullmatch(s.current_date or ""):
            if not self._rank_ready(criteria):
                name = self.scenario_names.get(criteria) or criteria
                self.view_with("setLiveBadge", f"Loading {name} · keeping current chart visible", "idle")
                return Await("paintLiveChartCache", [s.current_date], ctx, next="_rank_main_1", sync=True)
            return Await("refreshLiveData", [s.current_date], {**ctx, "ready": True}, next="_rank_main_2", fire=True)
        return self._rank_main_2({**ctx, "ready": True}, None)

    def _rank_ready(self, criteria):
        """The scenario's data for the current date is already in the page."""
        s = self.s
        key = f"{criteria}_{'alt' if s.return_type == 'ALT' else 'net'}" if pu.is_metric_aware_criteria(criteria) else criteria
        bucket = self.client.criteria_data.get(key, {}).get(s.current_date)
        return isinstance(bucket, list) and len(bucket) > 0

    def _rank_portfolio_1(self, ctx, result):
        s = self.s
        s.visible = {m.get("model") for m in self._eligible()}
        s.selected_model_index = 0
        candidates = len(s.portfolio_models)
        self.view("updateScenarioUI", "updateDateLabelAndTitle", "updateScrubberUI", "updateRibbon", "renderCards", "drawChart")
        self.view_with("setLiveBadge", f"Portfolio · {ctx['name']} · {candidates} strategies", "ok")
        if s.pit_mode:
            return Await("schedulePointInTimeSelection", [], ctx, next="_rank_done", sync=True)
        return None

    def _rank_main_1(self, ctx, painted):
        """After paintLiveChartCache: the scenario is ready if the page painted a cached chart that holds the data."""
        ready = bool(painted) and self._rank_ready(ctx["criteria"])
        return Await("refreshLiveData", [self.s.current_date], {**ctx, "ready": ready}, next="_rank_main_2", fire=True)

    def _rank_main_2(self, ctx, result):
        s = self.s
        self.view("updateScenarioUI")
        if not ctx["ready"]:
            return None
        s.visible = {m.get("model") for m in self._eligible()}
        s.selected_model_index = 0
        max_f = self.max_frames()
        if s.frame >= max_f:
            s.frame = max_f - 1
        if s.baseline >= max_f:
            s.baseline = 0
        self.view("updateDateLabelAndTitle", "updateScrubberUI", "updateRibbon", "renderCards", "drawChart")
        return Await("schedulePointInTimeSelection", [], ctx, next="_rank_main_3", sync=True)

    def _rank_main_3(self, ctx, result):
        self.persist_portfolio_view_config(None)
        return None

    def _rank_done(self, ctx, result):
        return None
