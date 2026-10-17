# epics/ep_057_sql_to_pgsql/scenario_engine_v2/engine/page_utils.py — small pure helpers ported from the page (replay clock, search terms, point-in-time request options, selected-time leaders, frame stepping).
#
# VERSION HISTORY
# v1.1.0 · 2026-10-17 · AutoTop1State + finish_automatic_top1_refresh, exact_search_model (differential-tested against the page JS).
# v1.0.0 · 2026-10-17 · Initial version: clock/replay-time helpers, rule summary, scenario criteria helpers, point-in-time request options and context key, retainSelectedTimeLeaders, trade date range, frame step/seek, split-mode and return-type rules. Each is differential-tested against the page's JS except available_dates (unit test only).
"""Every function names the page function it ports. They take the page state they read as arguments (no globals)."""
from __future__ import annotations

import copy
import math
import re
from dataclasses import dataclass
from datetime import datetime, timedelta

SPLIT_MODES = ("ALL_NET", "BUY_NET", "SELL_NET", "TRI_SPLIT", "MULTI_SPLIT")
HISTORY_PALETTE = ["#f59e0b", "#a78bfa", "#34d399", "#fb7185", "#f97316", "#38bdf8", "#e879f9"]


def _number(value):
    """JS Number(value) for the inputs that occur: numeric strings and numbers; anything else -> NaN."""
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if value is None:
        return float("nan")
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip()
    if s == "":
        return 0.0
    try:
        return float(s)
    except ValueError:
        return float("nan")


def _or(value, fallback):
    """JS `value || fallback` for numbers (NaN and 0 are falsy)."""
    return fallback if (value != value or value == 0) else value


def js_str(value) -> str:
    """String(value) as JS prints array-join elements: null/undefined -> '', integral floats without '.0'."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if value != value:
            return "NaN"
        if value.is_integer():
            return str(int(value))
        return repr(value)
    return str(value)


def clock_minutes(value) -> int | None:
    """clockMinutes: 'HH:MM' -> minutes since midnight, else None."""
    m = re.fullmatch(r"([0-9]{2}):([0-9]{2})", str(value or ""))
    if not m:
        return None
    h, mi = int(m.group(1)), int(m.group(2))
    return h * 60 + mi if h <= 23 and mi <= 59 else None


def replay_clock_time(value) -> str:
    """replayClockTime: minutes -> 'HH:MM' (wrapped into one day)."""
    n = _number(value)
    n = 0.0 if n != n else n
    minute = int(math.floor(n)) % 1440
    return f"{minute // 60:02d}:{minute % 60:02d}"


def next_automatic_top1_minute(minute, interval, include_current=True) -> int:
    """nextAutomaticTop1Minute: next scheduled minute on an `interval` grid."""
    mi = _number(minute)
    iv = _number(interval)
    current = max(0, int(math.floor(0.0 if mi != mi else mi)))
    every = max(1, int(math.floor(1.0 if (iv != iv or iv == 0) else iv)))
    remainder = current % every
    if remainder == 0 and include_current:
        return current
    return current + ((every - remainder) or every)


def selected_time_point_eligible(model: dict, point: dict | None, join_at) -> bool:
    """selectedTimePointEligible; `join_at` = core_ported.selected_time_join_at(model)."""
    return (not join_at) or str((point or {}).get("time") or "") >= join_at


def model_search_terms(value) -> list[str]:
    """modelSearchTerms: unique comma/semicolon/space separated terms, in order."""
    out: list[str] = []
    for term in re.split(r"[,;\s]+", str(value or "")):
        term = term.strip()
        if term and term not in out:
            out.append(term)
    return out


_RULE_LABELS = {
    "ranked_top": "overall top", "ranked_bottom": "overall bottom",
    "similar_higher_net": "similar correlation + higher net", "similar_lower_net": "similar correlation + lower net",
    "opposite_top": "opposite correlation + top", "opposite_bottom": "opposite correlation + bottom",
    "better_win_rate": "better win rate", "higher_loss_rate": "higher loss rate",
    "ranked": "overall top", "similar": "similar correlation", "opposite": "opposite correlation", "win_rate": "win rate",
}


def overlay_rule_summary(rule: dict | None) -> str:
    """overlayRuleSummary."""
    if not rule:
        return "No replay overlay rule assigned"
    config = rule.get("config") or {}
    parts = []
    for item in config.get("rules") or []:
        group = item.get("group") or "group"
        labels = dict(_RULE_LABELS, group_ranked_top=f"top in {group}", group_ranked_bottom=f"bottom in {group}",
                      group_ranked=f"top in {group}")
        parts.append(labels.get(item.get("type")) or item.get("type"))
    criteria = " → ".join(js_str(p) for p in parts)
    interval = js_str(_or(_number(config.get("interval_minutes")), 30))
    hold = js_str(_or(_number(config.get("hold_rank")), 1))
    side = str(config.get("trade_side") or "both").upper()
    return f"{rule.get('name')} · every {interval}m · {criteria or 'no criteria'} · hold top #{hold} · {side}"


def is_metric_aware_criteria(criteria: str) -> bool:
    """isMetricAwareCriteria."""
    return criteria == "family_leaders" or criteria.startswith("top5_") or criteria.startswith("top3_tp")


def short_strategy_description(model_id, strategy_catalogue: list[dict], portfolio_models: list[dict]) -> str:
    """shortStrategyDescription: strip the breakout_ prefix and normalise the R_Rev_/Rev_ prefixes."""
    item = next((c for c in strategy_catalogue if c.get("model") == model_id), None) \
        or next((c for c in portfolio_models if c.get("model") == model_id), None)
    if not item or not item.get("strategy"):
        return ""
    s = re.sub(r"^breakout_", "", item["strategy"], flags=re.I)
    s = re.sub(r"^R_Rev_", "R_rev_", s, flags=re.I)
    return re.sub(r"^Rev_", "rev_", s, flags=re.I)


def selected_time_note_entries(model: dict | None) -> list[dict]:
    """getSelectedTimeNoteEntries."""
    model = model or {}
    if model.get("selectedAtEntries"):
        return model["selectedAtEntries"]
    m = re.match(r"^selected-time #([0-9]+)", str(model.get("comparisonRole") or ""))
    rank = (m.group(1) if m else None) or model.get("selectedRank") or 1
    if model.get("selectedAtTimes"):
        times = model["selectedAtTimes"]
    else:
        times = [model["selectedAt"]] if model.get("selectedAt") else []
    return [{"time": t, "rank": rank} for t in times]


def selected_time_rank_count(select_value) -> float:
    """selectedTimeRankCount: the rank <select> value clamped to 1..10 (default 1)."""
    n = _number(select_value)
    return max(1, min(10, 1 if (n != n or n == 0) else n))


def point_in_time_request_options(state: dict) -> dict:
    """pointInTimeRequestOptions. state keys: active_portfolio, portfolio_scenario_configs, portfolio_criteria, current_criteria,
    current_return_type, current_product_type, current_product, current_strategy_family, model_limit, min_win_rate, rank_select_value."""
    active = state.get("active_portfolio")
    source = (state.get("portfolio_scenario_configs") or {}).get(active) if active else None
    source = source or None
    cur = state["current_criteria"]
    if active:
        crit = (source or {}).get("criteria") or (state.get("portfolio_criteria") or {}).get(active) or cur
    else:
        crit = cur
    ret = (source or {}).get("returnType") or state["current_return_type"]
    scenario = (("top_alt_net" if ret == "ALT" else "top_net") if crit == "top1_at_time" else crit)
    limit_src = (source or {}).get("limit") or state["model_limit"]
    mwr = (source or {}).get("minWinRate")
    return {
        "scenario": scenario,
        "return_type": ret,
        "product_type": (source or {}).get("productType") or state["current_product_type"],
        "product": (source or {}).get("product") or state["current_product"],
        "strategy_family": (source or {}).get("strategyFamily") or state["current_strategy_family"],
        "limit": max(limit_src, selected_time_rank_count(state.get("rank_select_value"))),
        "min_win_rate": mwr if mwr is not None else state["min_win_rate"],
    }


def point_in_time_context_key(state: dict) -> str:
    """pointInTimeContextKey. Adds current_date, auto_refresh_enabled, auto_refresh_direction, auto_refresh_rank to the state."""
    opts = point_in_time_request_options(state)
    enabled = bool(state.get("auto_refresh_enabled"))
    parts = [state.get("current_date"), *opts.values(), state.get("active_portfolio") or "scenario",
             state.get("auto_refresh_direction") if enabled else "", state.get("auto_refresh_rank") if enabled else ""]
    return "|".join(js_str(p) for p in parts)


def retain_selected_time_leaders(history: dict, pinned: list[dict], search_loaded: list[dict], leaders: list[dict], selected_at) -> dict:
    """retainSelectedTimeLeaders: remember each selected-time leader with a stable colour, join time and selection history.
    `history` (model id -> record, insertion ordered) is updated in place and returned."""
    if not isinstance(leaders, list) or not selected_at:
        return history
    used = {str(m.get("color") or "").lower() for m in [*pinned, *search_loaded]}
    used |= {str(m.get("color") or "").lower() for m in history.values()}
    for rank_index, leader in enumerate(leaders):
        if not leader or not leader.get("series"):
            continue
        model_id = str(leader["model"])
        prev = history.get(model_id)
        if prev is not None and prev.get("selectedAtEntries") is not None:
            raw = prev["selectedAtEntries"]
        else:
            raw = [{"time": t, "rank": (prev or {}).get("selectedRank") or 1} for t in ((prev or {}).get("selectedAtTimes") or [])]
        entries = {e["time"]: e["rank"] for e in raw}
        rank = _number(leader.get("selectedRank"))
        selected_rank = rank_index + 1 if (rank != rank or rank == 0) else rank
        entries[selected_at] = selected_rank
        times = list(entries.keys())
        color = (prev or {}).get("color") or next((c for c in HISTORY_PALETTE if c.lower() not in used), None) \
            or HISTORY_PALETTE[len(history) % len(HISTORY_PALETTE)]
        used.add(color.lower())
        history[model_id] = {**copy.deepcopy(leader), "color": color, "selectedAt": selected_at, "selectedAtTimes": times,
                             "joined_at": (prev or {}).get("joined_at") or leader.get("joined_at") or selected_at,
                             "selectedAtEntries": [{"time": t, "rank": r} for t, r in entries.items()],
                             "selectedRank": selected_rank}
    return history


def trade_date_range(current_date: str, available_ids: list[str]) -> list:
    """tradeDateRange (note: the page hard-codes an upper bound of 2026-09-18 for the 'Full Week' view)."""
    if current_date == "WEEK_OVERALL":
        days = sorted(i for i in available_ids if re.match(r"^[0-9]{4}-", i) and i <= "2026-09-18")
        return [days[0] if days else None, days[-1] if days else None]
    return [current_date, current_date]


def available_dates(now: datetime) -> list[dict]:
    """availableDates: 'Full Week' plus the last seven calendar days ending today (en-GB short weekday + day)."""
    now = now.replace(hour=12, minute=0, second=0, microsecond=0)
    out = [{"id": "WEEK_OVERALL", "label": "Full Week"}]
    cursor = now - timedelta(days=6)
    names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    while cursor <= now:
        out.append({"id": cursor.strftime("%Y-%m-%d"), "label": f"{names[cursor.weekday()]} {cursor.day}"})
        cursor += timedelta(days=1)
    return out


def frame_after_step(current: int, delta: int, max_frames: int) -> int:
    """step(): new replay frame, clamped to the timeline (the page adds delta to the raw index, -1 included)."""
    return max(0, min(max_frames - 1, current + delta))


def frame_for_pct(pct: float, max_frames: int) -> int:
    """seekToPct(): frame for a 0..1 position, rounded half up like Math.round (not clamped, as on the page)."""
    return int(math.floor(pct * (max_frames - 1) + 0.5))


def valid_split_mode(mode) -> bool:
    """setSplitMode(): only these modes are accepted; anything else is ignored."""
    return mode in SPLIT_MODES


def swap_scenario_for_return_type(current_type: str, criteria: str, new_type: str) -> dict:
    """setReturnType() scenario rule: NET moves top_alt_net back to top_net, ALT moves top_net to top_alt_net;
    switching to the current type changes nothing. Persistence / refetch / UI are outside the engine."""
    if current_type == new_type:
        return {"currentReturnType": current_type, "currentCriteria": criteria}
    if new_type == "NET":
        criteria = "top_net" if criteria == "top_alt_net" else criteria
    else:
        criteria = "top_alt_net" if criteria == "top_net" else criteria
    return {"currentReturnType": new_type, "currentCriteria": criteria}


def _tpl(value) -> str:
    """How a JS template literal prints a value: null -> 'null', booleans lower-case, integral floats without '.0'."""
    if value is None:
        return "null"
    return js_str(value)


@dataclass
class AutoTop1State:
    """The page's 'auto-refresh top 1' bookkeeping (autoRefreshTop1*, pendingExplicitTop1Time, selectedTimeExplicitRefresh)."""
    request_at: str | None = None            # autoRefreshTop1RequestAt: the lookup time currently in flight
    pending_explicit_time: str | None = None  # pendingExplicitTop1Time
    explicit_refresh: bool = False            # selectedTimeExplicitRefresh
    next_minute: float | None = None          # autoRefreshTop1NextMinute
    interval_minutes: float = 15              # autoRefreshTop1Minutes
    enabled: bool = False                     # autoRefreshTop1Enabled


def finish_automatic_top1_refresh(state: AutoTop1State, at, message="", head_time=None) -> dict:
    """finishAutomaticTop1Refresh: close the in-flight lookup for `at`, schedule the next check one interval later, build the
    status text, and report whether the replay head should be evaluated again (a scheduled time may have been crossed meanwhile).
    Mutates `state`. Returns the same fields the page leaves behind plus `status` (None if the lookup was not the in-flight one)
    and `sched` (the head time to re-evaluate, or None). The scheduler itself (scheduleAutomaticTop1Refresh) is not ported."""
    if state.request_at != at:
        return {"status": None, "sched": None, "requestAt": state.request_at, "pending": state.pending_explicit_time,
                "explicit": state.explicit_refresh, "nextMinute": state.next_minute}
    state.request_at = None
    if state.pending_explicit_time == at:
        state.pending_explicit_time = None
        state.explicit_refresh = False
    checked = clock_minutes(at)
    if checked is not None:
        state.next_minute = checked + state.interval_minutes
    next_label = "" if state.next_minute is None else f" · next at {replay_clock_time(state.next_minute)}"
    status = f"{message}{next_label}" if message else f"On · checked {_tpl(at)}{next_label}"
    return {"status": status, "sched": head_time if (state.enabled and head_time) else None, "requestAt": state.request_at,
            "pending": state.pending_explicit_time, "explicit": state.explicit_refresh, "nextMinute": state.next_minute}


def exact_search_model(search_text, loaded_models: list[dict], available_models: list[dict]):
    """getExactSearchModel: with exactly one search term, the model whose id equals it (case-insensitive), looking first in the
    models loaded by search and then in `available_models` (the caller supplies what the page picks: portfolio models,
    point-in-time models, or the scenario candidates). None when there are several terms or no match."""
    terms = [t.lower() for t in model_search_terms(search_text)]
    if len(terms) != 1:
        return None
    q = terms[0]
    found = next((m for m in loaded_models if str(m.get("model") or "").lower() == q), None)
    if found:
        return found
    return next((m for m in available_models if str(m.get("model") or "").lower() == q), None)
