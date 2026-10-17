# epics/ep_057_sql_to_pgsql/scenario_engine_v2/engine/selected_time.py — selected-time ("point in time") cohort: the request and the merge of leaders, history, pinned and searched models (port of refreshPointInTimeSelection).
#
# VERSION HISTORY
# v1.4.0 · 2026-10-17 · events: the ordered view calls / effects of a lookup (replaces render_history).
# v1.3.0 · 2026-10-17 · render_history flag (the page re-renders the hourly-cohort list after a lookup).
# v1.2.1 · 2026-10-17 · the point-in-time Pending is marked issued (a request is in flight), so responses apply in issue order.
# v1.2.0 · 2026-10-17 · request_sequence (pointInTimeRequestSequence) is incremented per request and checked on completion: 'context changed' and 'lookup canceled' outcomes.
# v1.1.0 · 2026-10-17 · begin_point_in_time_selection (issue the request now, apply later) for fire-and-forget callers; refresh_point_in_time_selection = begin + finish.
# v1.0.0 · 2026-10-17 · Initial version: SelectedTimeState + refresh_point_in_time_selection, differential-tested against the page's own function on a recording fetch stub.
"""The page keeps this state in globals; here it lives in a SelectedTimeState that the caller owns. UI work (re-rendering, button
classes, chart painting) and the concurrency guards (request sequence numbers, 'context changed while loading') are not modelled:
a headless run is sequential. Status text and CSS class are kept because they are observable page state."""
from __future__ import annotations

import math
from collections import OrderedDict
from dataclasses import dataclass, field

from . import page_utils as pu
from .data_client import DATE_RE, DataClient, FetchError, Pending, resolved

PALETTE = pu.HISTORY_PALETTE


def js_truthy(v) -> bool:
    if v is None:
        return False
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v != 0 and v == v
    if isinstance(v, str):
        return len(v) > 0
    return True  # lists and objects are truthy in JS even when empty


def js_or(*vals):
    """a || b || c  with JS truthiness (the last operand is returned if none is truthy)."""
    for v in vals[:-1]:
        if js_truthy(v):
            return v
    return vals[-1]


@dataclass
class SelectedTimeState:
    point_in_time_mode: bool = True
    current_date: str = ""
    current_criteria: str = "top_net"
    active_portfolio: str | None = None
    auto: pu.AutoTop1State = field(default_factory=pu.AutoTop1State)
    auto_direction: str | None = None        # autoRefreshTop1DirectionSelect.value
    auto_rank_value: object = None           # autoRefreshTop1RankSelect.value
    models: list = field(default_factory=list)            # pointInTimeModels
    timeline_models: list = field(default_factory=list)   # pointInTimeTimelineModels
    requested_key: str = ""                  # pointInTimeRequestedKey
    pinned: "OrderedDict[str, dict]" = field(default_factory=OrderedDict)   # pinnedComparisonModels
    search_loaded: list = field(default_factory=list)                        # modelSearchLoadedModels
    history: "OrderedDict[str, dict]" = field(default_factory=OrderedDict)  # selectedTimeLeaderHistory
    history_context: str = ""
    scenario_removed: set = field(default_factory=set)
    scenario_names: dict = field(default_factory=dict)    # SCENARIOS_CATALOGUE id -> name
    status: str = ""
    status_class: str = ""
    history_at: str = ""
    events: list = field(default_factory=list)   # ordered view calls / effects the page makes during a lookup: ("view", name) or ("fx", name); the caller replays and clears them
    visible: set = field(default_factory=set)
    frame_index: int = -1
    selected_time_input: str | None = None
    selected_model_index: int = 0
    request_sequence: int = 0                # pointInTimeRequestSequence
    auto_status: str | None = None           # last status finishAutomaticTop1Refresh produced
    sched: str | None = None                 # head time finishAutomaticTop1Refresh asked to re-evaluate


def _index(lst, x):
    """lst[x] the way JS reads it: only an integral in-range index finds an element."""
    if isinstance(x, float) and x != int(x):
        return None
    i = int(x)
    return lst[i] if 0 <= i < len(lst) else None


def _same(a, b) -> bool:
    return str(a.get("model")) == str(b.get("model"))


def begin_point_in_time_selection(st: SelectedTimeState, client: DataClient, opt_state: dict, *, head_time, max_frames: int,
                                  eligible_models: list, at_override=None) -> Pending:
    """refreshPointInTimeSelection. `opt_state` is the dict page_utils.point_in_time_request_options reads (the page's current
    portfolio / criteria / product filters). `head_time` is pointInTimeAtReplayHead(), `eligible_models` getEligibleModels().
    Returns {"ran": bool, "url": str|None}; all results are left in `st`."""
    if not st.point_in_time_mode or not DATE_RE.fullmatch(st.current_date or ""):
        return resolved({"ran": False, "url": None})
    was_at_latest = st.frame_index < 0 or st.frame_index >= max_frames - 1
    at = at_override or head_time
    if not at:
        return resolved({"ran": False, "url": None})
    auto = st.auto.request_at == at
    explicit = bool(not auto and st.auto.explicit_refresh and st.auto.pending_explicit_time == at)
    retain = explicit or auto
    retained = list(st.models) if (retain and isinstance(st.models, list)) else []
    opts = pu.point_in_time_request_options(opt_state)
    criteria_for_request = st.current_criteria
    req_dir = "bottom" if st.auto_direction == "bottom" else "top"
    rn = pu._number(st.auto_rank_value)
    req_rank = max(1, min(5, 1 if (rn != rn or rn == 0) else rn))
    key = "|".join(pu.js_str(p) for p in [st.current_date, at, opts["scenario"], opts["return_type"], opts["product_type"], opts["product"],
                                          opts["strategy_family"], opts["limit"], opts["min_win_rate"], st.active_portfolio or "scenario",
                                          req_dir if auto else "", req_rank if auto else ""])
    if key == st.requested_key:
        return resolved({"ran": False, "url": None})
    rank_count = req_rank if auto else pu.selected_time_rank_count(opt_state.get("rank_select_value"))
    st.requested_key = key
    st.status_class = "text-[10px] font-bold text-amber-300"
    if auto:
        st.status = f"Auto-add {req_dir} #{pu.js_str(req_rank)} at {at}…"
    elif explicit:
        st.status = f"Finding top {pu.js_str(pu.selected_time_rank_count(opt_state.get('rank_select_value')))} as of {at}…"
        st.events += [("view", "renderCards"), ("view", "drawChart")]
    else:
        st.status = f"Loading as of {at}…"
    st.request_sequence += 1
    my_seq, date_for_request, portfolio_for_request = st.request_sequence, st.current_date, st.active_portfolio
    url = client.point_in_time_url(st.current_date, at, opts, req_dir if auto else None, req_rank if auto else None)
    try:  # the request is issued now; the result is applied when the Pending finishes
        resp, err = client._get(url), None
    except Exception as e:  # noqa: BLE001
        resp, err = None, e

    def apply():
        try:
            if err is not None:
                raise err
            status, payload = resp
            if not (200 <= int(status) < 300):
                raise FetchError((payload.get("error") if isinstance(payload, dict) else None) or status)
            if (my_seq != st.request_sequence or key != st.requested_key or st.current_date != date_for_request
                    or st.current_criteria != criteria_for_request or st.active_portfolio != portfolio_for_request):
                fin = pu.finish_automatic_top1_refresh(st.auto, at, f"On · context changed at {at}", head_time)
                if fin["status"] is not None:
                    st.auto_status = fin["status"]
                if fin["sched"] is not None:
                    st.sched = fin["sched"]
                return {"ran": True, "url": url}
            fin = pu.finish_automatic_top1_refresh(st.auto, at, "", head_time)
            if fin["status"] is not None:
                st.auto_status = fin["status"]
            if fin["sched"] is not None:
                st.sched = fin["sched"]
            ranked = payload.get("models") if isinstance(payload.get("models"), list) else []
            at_time = js_or(payload.get("at_time"), at)
            if auto:
                pick = _index(ranked, req_rank - 1)
                leaders = [{**pick, "selectedRank": req_rank}] if js_truthy(pick) else []
            else:
                leaders = ranked[:int(math.floor(rank_count))]
            comparison = list(leaders)
            history_context = "|".join(pu.js_str(p) for p in [st.current_date, criteria_for_request, opts["product_type"], opts["product"],
                                                               opts["strategy_family"], opts["return_type"]])
            previously: set = set()
            if retain:
                if st.history_context != history_context:
                    st.history.clear()
                    st.history_context = history_context
                previously = {k for k in st.history if str(k) not in st.scenario_removed}
                pu.retain_selected_time_leaders(st.history, list(st.pinned.values()), st.search_loaded, leaders, at_time)
                if explicit:
                    st.auto.pending_explicit_time = None
                    st.auto.explicit_refresh = False
            if st.history_context == history_context:
                for hl in st.history.values():
                    if str(hl.get("model")) in st.scenario_removed:
                        continue
                    if not any(_same(m, hl) for m in comparison):
                        comparison.append({**hl, "comparisonRole": f"selected-time #{pu.js_str(js_or(hl.get('selectedRank'), 1))} history"})
            for pid, pm in st.pinned.items():
                if not any(str(m.get("model")) == pid for m in comparison):
                    comparison.append(pm)
            for sm in st.search_loaded:
                if not any(_same(m, sm) for m in comparison):
                    comparison.append(sm)
            if retain:
                for rm in retained:
                    if not any(_same(m, rm) for m in comparison):
                        comparison.append({**rm, "comparisonRole": js_or(rm.get("comparisonRole"), "retained chart")})
            leader_ids = {str(m.get("model")) for m in leaders}
            other_ids = set(st.pinned.keys()) | {str(m.get("model")) for m in st.search_loaded}
            pinned_colors = {str(m.get("color") or "").lower() for m in [*st.pinned.values(), *st.search_loaded]}
            assigned = set(pinned_colors)
            for m in leaders:
                st.scenario_removed.discard(str(m.get("model")))
            out = []
            for index, model in enumerate(comparison):
                mid = str(model.get("model"))
                is_leader = mid in leader_ids
                cur_rank = next((i for i, l in enumerate(leaders) if str(l.get("model")) == mid), -1) + 1
                hist = st.history.get(mid)
                is_pinned = mid in st.pinned
                is_searched = any(str(i.get("model")) == mid for i in st.search_loaded)
                is_retained = retain and any(str(i.get("model")) == mid for i in retained)
                color = js_or((hist or {}).get("color"), model.get("color"))
                if is_leader and not hist and any(i != mid for i in other_ids):
                    color = next((c for c in PALETTE if c.lower() != str(model.get("color") or "").lower() and c.lower() not in assigned), None) or model.get("color")
                if is_leader:
                    assigned.add(str(color or "").lower())
                if not is_leader and is_searched and not is_pinned:
                    color = "#e879f9"
                mr = pu._number(model.get("selectedRank"))
                base = (req_rank if (mr != mr or mr == 0) else mr) if (is_leader and auto) else cur_rank
                selected_rank = js_or(base, (hist or {}).get("selectedRank"), model.get("selectedRank"), 1)
                explicit_leader = retain or criteria_for_request == "top1_at_time"
                if is_leader:
                    role = f"{'selected-time' if explicit_leader else 'as-of'} #{pu.js_str(selected_rank)}"
                elif hist:
                    role = f"selected-time #{pu.js_str(selected_rank)} history"
                elif is_pinned:
                    role = "pinned comparison"
                elif is_searched:
                    role = "searched model"
                elif is_retained:
                    role = "retained chart"
                else:
                    role = "comparison"
                out.append({**model, "color": color, "rank": index + 1, "comparisonRole": role,
                            "joined_at": js_or((hist or {}).get("joined_at"), model.get("joined_at"), at_time if is_leader else None),
                            "selectedAt": at_time if is_leader else js_or((hist or {}).get("selectedAt"), model.get("selectedAt"),
                                                                           None if (retain and is_retained) else at_time),
                            "selectedRank": selected_rank,
                            "selectedAtTimes": js_or((hist or {}).get("selectedAtTimes"), model.get("selectedAtTimes"), [at_time] if is_leader else []),
                            "selectedAtEntries": js_or((hist or {}).get("selectedAtEntries"), model.get("selectedAtEntries"),
                                                       [{"time": at_time, "rank": selected_rank}] if is_leader else [])})
            st.models = out
            if any(m.get("series") for m in out):
                st.timeline_models = [m for m in out if m.get("series")]
            if retain:
                st.selected_model_index = 0
                st.visible = {m.get("model") for m in out}
                st.events.append(("view", "updatePointInTimeToggleUI"))
            st.visible = {m.get("model") for m in eligible_models}
            st.status_class = "text-[10px] text-cyan-300"
            if retain:
                if not leaders:
                    st.status = (f"No new strategies available at {at_time}; existing chart and overlay history retained ({len(retained)} strategies)"
                                 if retained else f"No strategies available at or before {at_time}")
                else:
                    if all(str(l.get("model")) in st.pinned for l in leaders):
                        pin_note = " · all already pinned"
                    elif st.pinned:
                        pin_note = f" · plus {len(st.pinned)} pinned"
                    else:
                        pin_note = ""
                    times = {t for m in st.history.values() for t in (m.get("selectedAtTimes") or [])}
                    scenario_name = js_or(st.active_portfolio, st.scenario_names.get(criteria_for_request), criteria_for_request)
                    new_leaders = [l for l in leaders if str(l.get("model")) not in previously]
                    retained_count = len(st.history) - len(new_leaders)
                    if not new_leaders:
                        already = ", ".join(
                            f"{l.get('model')}{' (already added at ' + ', '.join(pu.js_str(t) for t in ((st.history.get(str(l.get('model'))) or {}).get('selectedAtTimes') or [])) + ')' if (st.history.get(str(l.get('model'))) or {}).get('selectedAtTimes') else ''}"
                            for l in leaders)
                        head = f"Auto-add {req_dir} #{pu.js_str(req_rank)}" if auto else f"Top {len(leaders)}"
                        st.status = f"{at_time} · {head} from {scenario_name} already on chart: {already}; no duplicate curve added; overlay history retained{pin_note}"
                    else:
                        added = ", ".join(pu.js_str(l.get("model")) for l in new_leaders)
                        retained_note = f"; retaining {retained_count} earlier strategies" if retained_count else ""
                        head = f"Auto-added {req_dir} #{pu.js_str(req_rank)}" if auto else f"Added new top {len(leaders)}"
                        st.status = (f"{at_time} · {head} from {scenario_name}: {added}{retained_note}; existing chart and overlay history retained; "
                                     f"{len(st.history)} distinct strategies across {len(times)} selected times{pin_note}")
                    st.status_class = "text-[10px] font-bold text-emerald-300"
            else:
                st.status = f"{at_time} · {len(leaders)} selected"
            st.history_at = f"{str(at_time)[:2]}:00"
            st.events.append(("fx", "renderPointInTimeHistory"))
            if was_at_latest:
                st.frame_index = max(0, max_frames - 1)
            st.events += [("view", n) for n in ("updateDateLabelAndTitle", "updateScrubberUI", "updateRibbon", "renderCards", "drawChart")]
            if explicit:
                st.selected_time_input = at
            return {"ran": True, "url": url}
        except Exception as error:  # noqa: BLE001 - the page reports any failure of the lookup (or of merging its result) this way
            if my_seq != st.request_sequence:
                fin = pu.finish_automatic_top1_refresh(st.auto, at, f"On · lookup canceled at {at}", head_time)
                if fin["status"] is not None:
                    st.auto_status = fin["status"]
                if fin["sched"] is not None:
                    st.sched = fin["sched"]
                return {"ran": True, "url": url}
            fin = pu.finish_automatic_top1_refresh(st.auto, at, f"On · lookup failed at {at}", head_time)
            if fin["status"] is not None:
                st.auto_status = fin["status"]
            if fin["sched"] is not None:
                st.sched = fin["sched"]
            retained_models = list(st.models) if isinstance(st.models, list) else []
            for pm in st.pinned.values():
                if not any(_same(m, pm) for m in retained_models):
                    retained_models.append(pm)
            for sm in st.search_loaded:
                if not any(_same(m, sm) for m in retained_models):
                    retained_models.append(sm)
            st.models = retained_models
            if st.auto.pending_explicit_time == at:
                st.auto.pending_explicit_time = None
            st.auto.explicit_refresh = False
            st.requested_key = ""
            st.status = f"Lookup failed for {at}: {error}"
            st.status_class = "text-[10px] font-bold text-rose-300"
            st.events += [("view", n) for n in ("updateDateLabelAndTitle", "updateRibbon", "renderCards", "drawChart")]
            return {"ran": True, "url": url}

    return Pending(apply, issued=True)


def refresh_point_in_time_selection(st: SelectedTimeState, client: DataClient, opt_state: dict, *, head_time, max_frames: int,
                                    eligible_models: list, at_override=None) -> dict:
    return begin_point_in_time_selection(st, client, opt_state, head_time=head_time, max_frames=max_frames,
                                         eligible_models=eligible_models, at_override=at_override).finish()
