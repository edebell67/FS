# epics/ep_057_sql_to_pgsql/scenario_engine_v2/engine/replay_models.py · which models are on screen and how long the replay is: getScenarioCandidates, getEligibleModels, getReplayTimelineModels, pointInTimeAtReplayHead, getMaxFrames.
#
# VERSION HISTORY
# v1.2.0 · 2026-10-19 · get_eligible_models follows page v2.65.35: the query's whitespace counts as '_' and whatever a search loaded is the search result (strategy-name matches as well as model IDs).
# v1.1.1 · 2026-10-17 · toFixed is core.js_to_fixed.
# v1.1.0 · 2026-10-17 · update_ribbon: the ribbon's numbers, labels and colours (TRI_SPLIT selected model or the visible models' totals).
# v1.0.0 · 2026-10-17 · Initial version: faithful ports over PageState + the client's scenario data (replaces the simplified Engine.eligible / max_frames / replay_head_time); differential-tested against the page's own functions.
"""These read the page's state (point-in-time mode, search results, pinned models, the active portfolio, cached scenario buckets), so they take a
PageState and the DataClient. The one DOM write, the model-search status line, is kept as `state.model_search_status`."""
from __future__ import annotations

import math
import re

from . import core_ported as core
from . import page_utils as pu
from .selected_time import js_truthy

_UNDEF = object()

# String.prototype.localeCompare on ASCII (ICU root collation, punctuation not ignored): this is the order Node/ICU 76 produces for the printable characters.
_ASCII_ORDER = " _-,;:!?.'\"()[]{}@*/\\&#%`^+<=>|~$0123456789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ"
_PRIMARY = {}
for _i, _c in enumerate(_ASCII_ORDER):
    _PRIMARY.setdefault(_c.lower(), len(_PRIMARY))


def locale_compare(a: str, b: str) -> int:
    """a.localeCompare(b) for ASCII text: compare by base character first (case-insensitive), then lowercase before uppercase."""
    ka = [_PRIMARY.get(c.lower(), 1000 + ord(c)) for c in a]
    kb = [_PRIMARY.get(c.lower(), 1000 + ord(c)) for c in b]
    if ka != kb:
        return -1 if ka < kb else 1
    for x, y in zip(a, b):
        if x != y:
            return -1 if x.islower() else 1  # same base letter, different case: lowercase sorts first
    return 0


def _num(v) -> float:
    """JS Number(v): missing -> NaN, null -> 0."""
    if v is _UNDEF:
        return float("nan")
    if v is None:
        return 0.0
    return pu._number(v)


def _get(m, key):
    return m.get(key, _UNDEF) if isinstance(m, dict) else _UNDEF


def _or(a, b):
    """JS `a || b`."""
    return a if (a is not _UNDEF and js_truthy(a)) else b


def _gte(a, b) -> bool:
    return _num(a) >= _num(b)


def js_round(x: float) -> float:
    return math.floor(x + 0.5) if x == x and abs(x) != float("inf") else x


def _s(v) -> str:
    return "" if v is None or v is _UNDEF else pu.js_str(v)


def _has_series(m) -> bool:
    """`m?.series?.length` (truthy): a non-empty series."""
    series = m.get("series") if isinstance(m, dict) else None
    return bool(series) and hasattr(series, "__len__") and len(series) > 0


def _lower(v) -> str:
    return _s(v).lower()


def _active_return_total(s, model) -> float:
    v = _num(_get(model, "cum_alt_net" if s.return_type == "ALT" else "cum_net"))
    return v if (v == v and v != 0) else 0.0


# ---- getScenarioCandidates ----
def get_scenario_candidates(s, client, criteria=None, product_type_filter=None) -> list[dict]:
    criteria = s.current_criteria if criteria is None else criteria
    aware = pu.is_metric_aware_criteria(criteria)
    key = f"{criteria}_{'alt' if s.return_type == 'ALT' else 'net'}" if aware else criteria
    dataset = client.criteria_data.get(key) or {}
    all_models = dataset.get(s.current_date) or []
    visible_product_type = product_type_filter if js_truthy(product_type_filter) else s.product_type
    dedicated = criteria.startswith("top5_")
    keys = core.metric_keys(s.return_type)

    def active_return(m) -> float:
        total_key = "cum_alt_net" if s.return_type == "ALT" else "cum_net"
        series_key = "alt_net" if s.return_type == "ALT" else "net"
        t = _num(_get(m, total_key))
        if t == t and abs(t) != float("inf"):
            return t
        series = m.get("series") if isinstance(m, dict) else None
        last = series[-1] if js_truthy(series) and series else None
        v = _num(_get(last, series_key)) if last is not None else float("nan")
        return v if (v == v and v != 0) else 0.0

    eligible = [m for m in all_models
                if _gte(_or(_get(m, keys["winRateKey"]), _get(m, "win_rate")), s.min_win_rate)
                and (visible_product_type == "all" or _lower(m.get("product_type")) == visible_product_type)
                and (s.product == "all" or _lower(m.get("product")) == s.product)
                and (dedicated or s.strategy_family == "all" or core.strategy_family_of(m) == s.strategy_family)]
    seen, out = set(), []
    for m in eligible:
        perf = js_round(active_return(m) * 100) / 100
        k = "NaN" if perf != perf else perf
        if k in seen:
            continue
        seen.add(k)
        out.append(m)
    return out


# ---- getEligibleModels ----
def get_eligible_models(s, client) -> list[dict]:
    keys = core.metric_keys(s.return_type)
    if s.deep_link_only:
        scenario_models = []
    elif s.pit_mode:
        scenario_models = s.pit_models if js_truthy(s.pit_models) or s.pit_models == [] else []
    elif not s.active_portfolio:
        scenario_models = get_scenario_candidates(s, client, s.current_criteria)
    else:
        def passes(m):
            wr = _get(m, keys["winRateKey"])
            if wr is _UNDEF or wr is None:
                wr = _get(m, "win_rate")
            if wr is _UNDEF or wr is None:
                wr = 0
            return (_gte(wr, s.min_win_rate)
                    and (s.product_type == "all" or _lower(m.get("product_type")) == s.product_type)
                    and (s.product == "all" or _lower(m.get("product")) == s.product)
                    and (s.strategy_family == "all" or core.strategy_family_of(m) == s.strategy_family))
        import functools
        picked = [m for m in s.portfolio_models if passes(m)]
        picked.sort(key=functools.cmp_to_key(lambda a, b: (
            (-1 if _active_return_total(s, b) - _active_return_total(s, a) < 0 else 1) if _active_return_total(s, b) - _active_return_total(s, a) != 0
            else locale_compare(_s(a.get("model")), _s(b.get("model"))))))
        scenario_models = picked
    query = re.sub(r"\s+", "_", str(s.model_search_input or "").strip().lower()) if s.model_search_input is not None else None   # v2.65.35: spaces count as '_' (strategy names)
    terms = pu.model_search_terms(query)
    direct = list(s.search_loaded) if query else []   # v2.65.35: what a search loaded (model IDs or strategy-name matches) is the search result
    models = scenario_models
    pinned = s.pinned
    if s.pit_mode:
        for m in direct:
            if not any(_s(e.get("model")) == _s(m.get("model")) for e in models):
                models = [*models, {**m, "color": "#e879f9", "comparisonRole": "searched model"}]
    elif direct:
        if pinned:
            for m in direct:
                if not any(_s(e.get("model")) == _s(m.get("model")) for e in models):
                    models = [*models, m]
        else:
            models = direct
    elif query and len(terms) == 1 and not pinned:
        models = [m for m in scenario_models if query in _lower(m.get("model"))]
    for model_id, pm in pinned.items():
        index = next((i for i, m in enumerate(models) if _s(m.get("model")) == model_id), -1)
        if index < 0:
            models = [*models, pm]
        elif _has_series(pm) and not _has_series(models[index]):
            models = [pm if i == index else m for i, m in enumerate(models)]
    n = len(pinned)
    plural = lambda c, one, many: one if c == 1 else many  # noqa: E731
    if s.deep_link_only:
        s.model_search_status = (f"Showing {n} selected strateg{plural(n, 'y', 'ies')} only · choose a scenario to add scenario leaders"
                                 if n else "Loading selected strategies…")
    elif s.pit_mode:
        count = len([m for m in scenario_models if _re_time_leader(_s(m.get("comparisonRole")))])
        s.model_search_status = (f"{count} time-selected strateg{plural(count, 'y', 'ies')}"
                                 + (f" · {len(direct)} searched model{plural(len(direct), '', 's')}" if direct else "")
                                 + (f" · {n} pinned" if n else ""))
    elif n:
        s.model_search_status = f"{n} pinned for comparison · {', '.join(pinned.keys())} · {len(scenario_models)} scenario leaders"
    elif not query:
        s.model_search_status = ""
    elif len(terms) > 1:
        s.model_search_status = f"{len(direct)} of {len(terms)} requested models loaded" + (f" · {n} pinned" if n else "")
    elif not models:
        s.model_search_status = "No match in current selection"
    elif len(models) == 1:
        s.model_search_status = "1 match · single-model chart"
    else:
        s.model_search_status = f"{len(models)} matches · showing first; select a card to switch"
    return models if s.active_portfolio else [m for m in models if _s(m.get("model")) not in s.scenario_removed]


def _re_time_leader(role: str) -> bool:
    import re
    return re.match(r"^selected-time #\d+", role) is not None


# ---- getReplayTimelineModels / pointInTimeAtReplayHead / getMaxFrames ----
def get_replay_timeline_models(s, client) -> list[dict]:
    query = str(s.model_search_input or "").strip().lower() if s.model_search_input is not None else None
    if s.pit_mode:
        active = get_eligible_models(s, client) if s.pit_models else []
        if active:
            return active
        if s.pit_timeline_models:
            return s.pit_timeline_models
    if s.pinned:
        return get_eligible_models(s, client)
    terms = [t.lower() for t in pu.model_search_terms(query)]
    loaded_ids = {_lower(m.get("model")) for m in s.search_loaded}
    if terms and all(t in loaded_ids for t in terms):
        return s.search_loaded
    if s.active_portfolio:
        return s.portfolio_models
    aware = pu.is_metric_aware_criteria(s.current_criteria)
    key = f"{s.current_criteria}_{'alt' if s.return_type == 'ALT' else 'net'}" if aware else s.current_criteria
    selected = (client.criteria_data.get(key) or {}).get(s.current_date)
    if isinstance(selected, list) and selected:
        return selected
    fallback = (client.criteria_data.get("top_net") or {}).get(s.current_date)
    return fallback if isinstance(fallback, list) and fallback else get_scenario_candidates(s, client, s.current_criteria)


def point_in_time_at_replay_head(s, client):
    timeline = get_replay_timeline_models(s, client)
    if not timeline:
        return None
    longest = timeline[0]
    for m in timeline:
        if len(m.get("series") or []) > len(longest.get("series") or []):
            longest = m
    series = longest.get("series") or []
    if not series:
        return None
    index = len(series) - 1 if s.frame < 0 else max(0, min(len(series) - 1, s.frame))
    return series[index].get("time") or None


def get_max_frames(s, client) -> int:
    eligible = get_replay_timeline_models(s, client)
    if not eligible:
        return 1
    return max(len(m["series"]) for m in eligible)


# ---- updateRibbon (the numbers and labels the ribbon shows) ----
_RIBBON_FIELDS = ("model_name", "product", "strategy", "tot_net", "buy_net", "sell_net", "tot_class", "buy_class", "sell_class",
                  "total_label", "buy_label", "sell_label", "indicator")


def new_ribbon_state() -> dict:
    return {k: "" for k in _RIBBON_FIELDS}


def _dom_text(v) -> str:
    """textContent = v on a DOM node: null / undefined -> ''."""
    return "" if v is None or v is _UNDEF else pu.js_str(v)


def _tpl(v) -> str:
    return "undefined" if v is _UNDEF else ("null" if v is None else pu.js_str(v))


def _fmt(v: float) -> str:
    return ("+$" if v >= 0 else "-$") + core.js_to_fixed(abs(v), 2)


def _point(series, baseline: int):
    if not series:
        return {"net": 0, "buy": 0, "sell": 0, "time": "00:00"}
    if baseline == 0:
        return {"time": "00:00", "net": 0, "buy": 0, "sell": 0, "alt_net": 0, "alt_buy": 0, "alt_sell": 0, "open": 0, "trades": 0}
    return series[min(baseline, len(series) - 1)]


def _head(series, frame: int):
    if not series:
        return {"net": 0, "buy": 0, "sell": 0, "time": "00:00"}
    return series[len(series) - 1 if frame < 0 else max(0, min(frame, len(series) - 1))]


def _metric(pt, key, fallback) -> float:
    v = _get(pt, key)
    return _num(v if v is not _UNDEF else _get(pt, fallback))


def update_ribbon(s, client, ribbon: dict, scenario_names: dict | None = None) -> dict:
    """updateRibbon: fills `ribbon` (see new_ribbon_state) exactly as the page sets its ribbon elements; fields it does not touch keep their value."""
    eligible = get_eligible_models(s, client)
    if not eligible:
        ribbon["model_name"] = "Loading Selected Models" if s.deep_link_only else "No Models Matching Filter"
        ribbon["tot_net"] = ribbon["buy_net"] = ribbon["sell_net"] = "$0.00"
        return ribbon
    longest = eligible[0]
    for m in eligible:
        if len(m["series"]) > len(longest["series"]):
            longest = m
    series = longest["series"]
    base_time = series[min(s.baseline, len(series) - 1)]["time"]
    head_time = _head(series, s.frame)["time"]
    if s.baseline == 0:
        ribbon["total_label"] = f"Total Net ({_tpl(head_time)})"
        ribbon["buy_label"] = "Cum Buy Net"
        ribbon["sell_label"] = "Cum Sell Net"
    else:
        ribbon["total_label"] = f"\u0394 Net ({_tpl(base_time)} \u2192 {_tpl(head_time)})"
        ribbon["buy_label"] = f"\u0394 Buy since {_tpl(base_time)}"
        ribbon["sell_label"] = f"\u0394 Sell since {_tpl(base_time)}"
    keys = core.metric_keys(s.return_type)
    if s.split_mode == "TRI_SPLIT":
        idx = s.selected_model_index
        m = eligible[idx] if (isinstance(idx, int) and 0 <= idx < len(eligible)) else eligible[0]
        base_pt, head_pt = _point(m["series"], s.baseline), _head(m["series"], s.frame)
        d_net = _metric(head_pt, keys["netKey"], "net") - _metric(base_pt, keys["netKey"], "net")
        d_buy = _metric(head_pt, keys["buyKey"], "buy") - _metric(base_pt, keys["buyKey"], "buy")
        d_sell = _metric(head_pt, keys["sellKey"], "sell") - _metric(base_pt, keys["sellKey"], "sell")
        ribbon["model_name"] = f"#{_tpl(_get(m, 'rank'))} {_tpl(_get(m, 'model'))}"
        ribbon["product"] = _dom_text(_get(m, "product"))
        ribbon["strategy"] = _dom_text(_get(m, "strategy"))
        ribbon["indicator"] = _dom_text(_get(m, "color"))
        tot, buy, sell = d_net, d_buy, d_sell
        ribbon["tot_class"] = f"text-base sm:text-lg font-black {'text-sky-400' if d_net >= 0 else 'text-sky-300'}"
        ribbon["buy_class"] = f"text-xs sm:text-sm font-bold {'text-emerald-400' if d_buy >= 0 else 'text-emerald-300'}"
        ribbon["sell_class"] = f"text-xs sm:text-sm font-bold {'text-rose-400' if d_sell >= 0 else 'text-rose-300'}"
    else:
        tot = buy = sell = 0.0
        active = [m for m in eligible if m.get("model") in s.visible]
        for m in active:
            base_pt, head_pt = _point(m["series"], s.baseline), _head(m["series"], s.frame)
            tot += _metric(head_pt, keys["netKey"], "net") - _metric(base_pt, keys["netKey"], "net")
            buy += _metric(head_pt, keys["buyKey"], "buy") - _metric(base_pt, keys["buyKey"], "buy")
            sell += _metric(head_pt, keys["sellKey"], "sell") - _metric(base_pt, keys["sellKey"], "sell")
        names = scenario_names or {}
        sc_name = names[s.current_criteria] if s.current_criteria in names else s.current_criteria  # an entry without a name -> undefined
        crit_label = "Selected Models" if s.deep_link_only else (s.active_portfolio or _tpl(sc_name))
        ribbon["model_name"] = f"{crit_label} ({len(active)} of {len(eligible)})"
        ribbon["product"] = "PORTFOLIO" if s.active_portfolio else "ALL"
        ribbon["strategy"] = {"ALL_NET": "Mode: Total Net Curves", "BUY_NET": "Mode: Cum Buy Net (Longs)",
                              "SELL_NET": "Mode: Cum Sell Net (Shorts)"}.get(s.split_mode, "Mode: Multi-Strategy Buy/Sell Split")
        ribbon["indicator"] = "#38bdf8" if s.current_criteria == "NET_RETURN" else "#34d399"
        ribbon["tot_class"] = f"text-base sm:text-lg font-black {'text-sky-400' if tot >= 0 else 'text-sky-300'}"
        ribbon["buy_class"] = f"text-xs sm:text-sm font-bold {'text-emerald-400' if buy >= 0 else 'text-emerald-300'}"
        ribbon["sell_class"] = f"text-xs sm:text-sm font-bold {'text-rose-400' if sell >= 0 else 'text-rose-300'}"
    ribbon["tot_net"], ribbon["buy_net"], ribbon["sell_net"] = _fmt(tot), _fmt(buy), _fmt(sell)
    return ribbon
