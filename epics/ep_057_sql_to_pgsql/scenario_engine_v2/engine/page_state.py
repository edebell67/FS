# epics/ep_057_sql_to_pgsql/scenario_engine_v2/engine/page_state.py — the page's global state as one object, defined once in a table that also generates the JS code used to test it.
#
# VERSION HISTORY
# v1.5.0 · 2026-10-20 · search_resolved_query / search_resolved_message (page v2.65.36: what the last Find model search concluded, shown while nothing matched).
# v1.5.0 · 2026-10-18 · view_args: arguments of view calls (index of the ['view', name] effect -> args), for the browser copy.
# v1.4.0 · 2026-10-17 · hourly-cohort history state (pit_hours, pit_history_at, status text, viewport / panel flags).
# v1.3.0 · 2026-10-17 · model_search_status (the model-search status line).
# v1.2.0 · 2026-10-17 · editing_rule_id / pending_rule_config (the overlay-rule editor's state).
# v1.1.0 · 2026-10-17 · pit_status / auto_status_text labels, portfolio refresh flags.
# v1.0.0 · 2026-10-17 · Initial version: FIELDS table (python attribute <-> page global <-> kind), PageState, snapshot / from_snapshot, JS set / get code generator.
"""Kinds: val (plain JSON value), set (JS Set, compared sorted), oset (JS Set whose insertion order matters), map (JS Map -> list of
[key, value] pairs), odict (JS object whose key order matters -> list of pairs), valueobj (a DOM control: only its .value is state)."""
from __future__ import annotations

import copy
from collections import OrderedDict

FIELDS = [
    # --- portfolios ---
    ("portfolios", "portfolios", "odict", dict),
    ("portfolio_criteria", "portfolioCriteria", "val", dict),
    ("portfolio_scenario_configs", "portfolioScenarioConfigs", "val", dict),
    ("portfolio_view_configs", "portfolioViewConfigs", "val", dict),
    ("merge_selection", "portfolioMergeSelection", "oset", list),
    ("active_portfolio", "activePortfolioName", "val", None),
    ("main_criteria", "mainScenarioCriteria", "val", "top_net"),
    ("main_view_config", "mainScenarioViewConfig", "val", None),
    ("similar_payload", "similarStrategyPayload", "val", None),
    ("live_store", "livePortfolioStore", "val", lambda: {"events": [], "states": {}, "configs": {}}),
    # --- view / filters ---
    ("current_date", "currentDate", "val", ""),
    ("current_criteria", "currentCriteria", "val", "top_net"),
    ("return_type", "currentReturnType", "val", "NET"),
    ("product_type", "currentProductType", "val", "all"),
    ("product", "currentProduct", "val", "all"),
    ("strategy_family", "currentStrategyFamily", "val", "all"),
    ("model_limit", "modelLimit", "val", 10),
    ("min_win_rate", "minWinRate", "val", 0),
    ("split_mode", "splitMode", "val", "ALL_NET"),
    ("chart_locked", "chartLocked", "val", False),
    ("chart_lock_before_live", "liveModePriorChartLock", "val", None),
    ("use_assigned_rule", "useAssignedOverlayRule", "val", False),
    ("editing_rule_id", "editingNamedOverlayRuleId", "val", None),
    ("pending_rule_config", "pendingNamedOverlayRuleConfig", "val", None),
    # --- DOM controls whose value is state ---
    ("rank_select_value", "selectedTimeRankSelect", "valueobj", "1"),
    ("selected_time_input", "selectedTimeInput", "valueobj", ""),
    ("auto_direction_select", "autoRefreshTop1DirectionSelect", "valueobj", "top"),
    ("auto_rank_select", "autoRefreshTop1RankSelect", "valueobj", "1"),
    ("model_search_input", "modelSearchInput", "valueobj", ""),
    # --- auto-add (auto top 1) ---
    ("auto_enabled", "autoRefreshTop1Enabled", "val", False),
    ("auto_direction", "autoRefreshTop1Direction", "val", "top"),
    ("auto_rank", "autoRefreshTop1Rank", "val", 1),
    ("auto_minutes", "autoRefreshTop1Minutes", "val", 15),
    ("auto_last_minute", "autoRefreshTop1LastMinute", "val", None),
    ("auto_next_minute", "autoRefreshTop1NextMinute", "val", None),
    ("auto_context", "autoRefreshTop1Context", "val", ""),
    ("auto_request_at", "autoRefreshTop1RequestAt", "val", None),
    ("pending_explicit_time", "pendingExplicitTop1Time", "val", None),
    ("explicit_refresh", "selectedTimeExplicitRefresh", "val", False),
    # --- point in time ---
    ("pit_mode", "pointInTimeMode", "val", False),
    ("pit_models", "pointInTimeModels", "val", None),
    ("pit_requested_key", "pointInTimeRequestedKey", "val", ""),
    ("pit_request_sequence", "pointInTimeRequestSequence", "val", 0),
    ("pit_history_key", "pointInTimeHistoryKey", "val", ""),
    ("pit_history_sequence", "pointInTimeHistorySequence", "val", 0),
    ("pit_hours", "pointInTimeHours", "val", list),
    ("pit_history_at", "pointInTimeHistoryAt", "val", ""),
    ("pit_history_status_text", "pointInTimeHistoryStatus", "textobj", ""),
    ("pit_history_near_viewport", "pointInTimeHistoryNearViewport", "val", True),
    ("pit_history_panel_hidden", "pointInTimeHistoryPanelHidden", "val", False),
    ("pit_timeline_models", "pointInTimeTimelineModels", "val", list),
    ("pit_selection_preference", "pointInTimeSelectionPreference", "val", True),
    ("history", "selectedTimeLeaderHistory", "map", list),
    ("history_context", "selectedTimeLeaderHistoryContext", "val", ""),
    ("scenario_removed", "scenarioRemovedModels", "set", list),
    ("top1_prev_mode", "top1AtTimePreviousPointInTimeMode", "val", None),
    # --- models on screen ---
    ("search_loaded", "modelSearchLoadedModels", "val", list),
    ("search_sequence", "modelSearchRequestSequence", "val", 0),
    ("search_resolved_query", "modelSearchResolvedQuery", "val", None),
    ("search_resolved_message", "modelSearchResolvedMessage", "val", ""),
    ("pinned", "pinnedComparisonModels", "map", list),
    ("deep_link_only", "deepLinkModelsOnly", "val", False),
    ("portfolio_models", "portfolioModels", "val", list),
    ("visible", "visibleModels", "set", list),
    ("selected_model_index", "selectedModelIndex", "val", 0),
    # --- replay ---
    ("frame", "currentFrameIndex", "val", -1),
    ("baseline", "baselineFrameIndex", "val", 0),
    ("is_playing", "isPlaying", "val", False),
    ("replay_interval", "replayInterval", "val", None),
    ("date_switch_sequence", "dateSwitchSequence", "val", 0),
    ("live_refresh_sequence", "liveRefreshSequence", "val", 0),
    ("available_dates", "availableDates", "val", list),
    ("live_date", "LIVE_DATE", "val", ""),
    # --- status labels (text the page shows; observable state) ---
    ("pit_status", "pointInTimeStatus", "statusobj", lambda: ["", ""]),
    ("model_search_status", "modelSearchStatus", "textobj", ""),
    ("auto_status_text", "autoRefreshTop1Status", "textobj", ""),
    ("live_refresh_in_flight", "portfolioViewRefreshInFlight", "val", False),
    ("portfolio_refresh_timer", "portfolioViewRefreshTimer", "val", None),
]
BY_PY = {f[0]: f for f in FIELDS}


def _default(d):
    return d() if callable(d) else d


class PageState:
    """Attributes are the python names in FIELDS; `effects` logs side effects (persistence, timers, UI hooks) in call order."""

    def __init__(self, **init):
        for py, _js, kind, default in FIELDS:
            v = _default(default)
            if kind == "map":
                v = OrderedDict(v)
            setattr(self, py, v)
        self.effects: list = []
        self.view_args: dict = {}   # arguments of view calls: index of the ['view', name] effect -> [args]
        self.timer_ops: list = []   # named timer operations tied to the setTimeout / clearTimeout effect at index `at`: {op, timer, ms, call, args, at}
        self.update(init)

    def update(self, init: dict) -> "PageState":
        for k, v in init.items():
            assert k in BY_PY, k
            setattr(self, k, copy.deepcopy(v))
        return self

    @classmethod
    def from_snapshot(cls, snap: dict) -> "PageState":
        s = cls()
        for py, _js, kind, _d in FIELDS:
            if py not in snap:
                continue
            v = copy.deepcopy(snap[py])
            if kind == "map":
                v = OrderedDict((k, x) for k, x in v)
            elif kind == "odict":
                v = {k: x for k, x in v}
            elif kind in ("set", "oset"):
                v = set(v) if kind == "set" else list(v)
            setattr(s, py, v)
        return s

    def snapshot(self) -> dict:
        out = {}
        for py, _js, kind, _d in FIELDS:
            v = getattr(self, py)
            if kind == "map":
                v = [[k, x] for k, x in v.items()]
            elif kind == "odict":
                v = [[k, x] for k, x in v.items()]
            elif kind == "set":
                v = sorted(str(x) for x in v)
            elif kind == "oset":
                v = list(v)
            out[py] = copy.deepcopy(v)
        return out


def js_state_code() -> str:
    """JS that restores every field from a snapshot dict `c` and reads them back, generated from FIELDS."""
    sets, gets = [], []
    for py, js, kind, _d in FIELDS:
        if kind == "val":
            sets.append(f"globalThis.{js} = c.{py};")
            gets.append(f"{py}: globalThis.{js}")
        elif kind == "set":
            sets.append(f"globalThis.{js} = new Set(c.{py});")
            gets.append(f"{py}: [...globalThis.{js}].map(String).sort()")
        elif kind == "oset":
            sets.append(f"globalThis.{js} = new Set(c.{py});")
            gets.append(f"{py}: [...globalThis.{js}]")
        elif kind == "map":
            sets.append(f"globalThis.{js} = new Map(c.{py});")
            gets.append(f"{py}: [...globalThis.{js}.entries()]")
        elif kind == "odict":
            sets.append(f"globalThis.{js} = Object.fromEntries(c.{py});")
            gets.append(f"{py}: Object.entries(globalThis.{js})")
        elif kind == "valueobj":
            sets.append(f"globalThis.{js} = {{ value: c.{py} }};")
            gets.append(f"{py}: globalThis.{js} ? globalThis.{js}.value : null")
        elif kind == "textobj":
            sets.append(f"globalThis.{js} = {{ textContent: c.{py} }};")
            gets.append(f"{py}: globalThis.{js} ? globalThis.{js}.textContent : null")
        elif kind == "statusobj":
            sets.append(f"globalThis.{js} = {{ textContent: c.{py}[0], className: c.{py}[1] }};")
            gets.append(f"{py}: [globalThis.{js}.textContent, globalThis.{js}.className]")
    return ("function __ps_set(c){ " + " ".join(sets) + " }\n"
            "function __ps_get(){ return { " + ", ".join(gets) + " }; }\n")
