# epics/ep_057_sql_to_pgsql/scenario_engine_v2/engine/core_ported.py — server-side port of the dashboard's client-side logic (extended copy of EP058 dashboard_engine.py).
#
# VERSION HISTORY
# v2.2.0 · 2026-10-17 · js_to_fixed (Number.toFixed rounds an exact tie up, Python's format rounds it to even): the DAILY TARGET texts now match the page on a .5 P&L.
# v2.1.0 · 2026-10-16 · Adds the assigned overlay-rule path (overlay_rule_candidate, overlay_rule_metric_value, as_of_correlation, apply_assigned_overlay_trade_results, assigned_rule_target, time_of_day_minutes, curve_point_at_or_before, source_trade_flip_results, RuleContext) to both rotation functions; generic path unchanged. The rule path assumes the page's eligibility filter falls through (eligible_fallthrough=True); the page as written returns false there.
# v2.0.0 · 2026-10-16 · Rewrites leader_rotation and multi_split_rotation to follow page v2.65.24's generic (non-rule) path: time-based point lookup, selected-time eligibility, negative-return override, rank hold, exposure de-duplication; adds point_at_or_before and selected_time_*; extra metric keys; color fields. Behaviour change (breaking). Overlay-rule mode still raises NotImplementedError.
# v1.1.0 · 2026-10-16 · Copied unchanged from EP058 dashboard_engine.py (sha256 8ead6261...) as the base of the extended engine; EP058's file is not modified. Still ported from page v2.30.0; the drift check reports the gap to the current page.
# v1.0.0 · 2026-09-26 · Python port of top10_5min_equity_curves.html v2.30.0 functions: getMetricKeys, getBasePoint, getReplayHeadPoint,
#   getScenarioCandidates/getEligibleModels, updateRibbon aggregates, computeTradeOverlaySignals, pairOverlayTrades,
#   computeSplitTargetSignal, computeLeaderRotation, computeMultiSplitRotation. Keep in step with the page by hand.
"""Pure functions over model dicts shaped like build_live_day() output ({model, product, series:[{time,net,buy,sell,alt_*}]})."""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal


def js_to_fixed(value, digits: int = 0) -> str:
    """Number.prototype.toFixed(digits): the exact binary value rounded to `digits` decimals, an exact tie going to the larger magnitude (Python's format() would round it to even:
    (504.5).toFixed(0) is '505', f'{504.5:.0f}' is '504')."""
    v = float(value)
    if v != v:
        return "NaN"
    if abs(v) == float("inf"):
        return "Infinity" if v > 0 else "-Infinity"
    if abs(v) >= 1e21:
        return repr(v)
    if v < 0:
        return "-" + js_to_fixed(-v, digits)
    return format(Decimal(v).quantize(Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP), "f")


def metric_keys(return_type: str = "NET") -> dict[str, str]:
    alt = str(return_type).upper() == "ALT"
    return {"netKey": "alt_net" if alt else "net", "buyKey": "alt_buy" if alt else "buy",
            "sellKey": "alt_sell" if alt else "sell", "cumNetKey": "cum_alt_net" if alt else "cum_net",
            "winRateKey": "alt_win_rate" if alt else "win_rate",
            "buyNetKey": "buy_alt_net" if alt else "buy_net", "sellNetKey": "sell_alt_net" if alt else "sell_net",
            "winsKey": "alt_wins" if alt else "wins"}


def strategy_family_of(model: dict) -> str:
    name = str(model.get("strategy") or "").strip().lower()
    for family in ("breakout_r_rev", "breakout_rev", "breakout_r", "breakout"):
        if name == family or name.startswith(family + "_"):
            return family
    return "unknown"


def base_point(series: list[dict], baseline_index: int = 0) -> dict:
    """getBasePoint: index 0 is the session-start zero, not the first snapshot."""
    if not series:
        return {"net": 0, "buy": 0, "sell": 0, "time": "00:00"}
    if baseline_index == 0:
        return {"time": "00:00", "net": 0, "buy": 0, "sell": 0, "alt_net": 0, "alt_buy": 0, "alt_sell": 0, "open": 0, "trades": 0}
    return series[min(baseline_index, len(series) - 1)]


def head_point(series: list[dict], frame_index: int = -1) -> dict:
    """getReplayHeadPoint: -1 means end of series."""
    if not series:
        return {"net": 0, "buy": 0, "sell": 0, "time": "00:00"}
    i = len(series) - 1 if frame_index < 0 else max(0, min(frame_index, len(series) - 1))
    return series[i]


def resolve_baseline_index(models: list[dict], baseline_index: int | None, baseline_time: str | None) -> int:
    if baseline_time and models:
        longest = max(models, key=lambda m: len(m["series"]))["series"]
        for i, p in enumerate(longest):
            if p["time"] >= baseline_time:
                return i
        return len(longest) - 1
    return baseline_index or 0


def _v(point: dict, key: str, fallback: str) -> float:
    return float(point[key] if point.get(key) is not None else point.get(fallback, 0) or 0)


def scenario_candidates(models: list[dict], *, return_type="NET", min_win_rate=0.0, product_type="all",
                        product="all", strategy_family="all", dedicated_family_scenario=False) -> list[dict]:
    """getScenarioCandidates: win-rate / product / family filter, sorted by active return desc then model id."""
    keys = metric_keys(return_type)

    def active_return(m):
        v = m.get(keys["cumNetKey"])
        if v is not None:
            return float(v)
        last = (m.get("series") or [{}])[-1]
        return float(last.get(keys["netKey"]) or 0)

    out = [m for m in models
           if float(m.get(keys["winRateKey"]) or m.get("win_rate") or 0) >= min_win_rate
           and (product_type == "all" or str(m.get("product_type") or "").lower() == product_type)
           and (product == "all" or str(m.get("product") or "").lower() == product)
           and (dedicated_family_scenario or strategy_family == "all" or strategy_family_of(m) == strategy_family)]
    return sorted(out, key=lambda m: (-active_return(m), str(m["model"])))


def ribbon(models: list[dict], *, return_type="NET", baseline_index=0, frame_index=-1) -> dict:
    """updateRibbon aggregate: summed delta net/buy/sell from baseline to replay head, plus per-model deltas."""
    keys = metric_keys(return_type)
    per, tot = [], {"net": 0.0, "buy": 0.0, "sell": 0.0}
    for m in models:
        b, h = base_point(m["series"], baseline_index), head_point(m["series"], frame_index)
        d = {"model": m["model"],
             "net": _v(h, keys["netKey"], "net") - _v(b, keys["netKey"], "net"),
             "buy": _v(h, keys["buyKey"], "buy") - _v(b, keys["buyKey"], "buy"),
             "sell": _v(h, keys["sellKey"], "sell") - _v(b, keys["sellKey"], "sell")}
        per.append(d)
        for k in tot:
            tot[k] += d[k]
    longest = max(models, key=lambda m: len(m["series"]))["series"] if models else []
    return {"total": tot, "models": per, "count": len(models),
            "base_time": longest[min(baseline_index, len(longest) - 1)]["time"] if longest else None,
            "head_time": head_point(longest, frame_index)["time"] if longest else None}


def mapped_series(model: dict, return_type="NET") -> list[dict]:
    keys = metric_keys(return_type)
    return [{"time": p["time"], "net": _v(p, keys["netKey"], "net"), "buy": _v(p, keys["buyKey"], "buy"),
             "sell": _v(p, keys["sellKey"], "sell")} for p in model["series"]]


def overlay_signals(series: list[dict], base: dict, exit_threshold: float = 0.0) -> list[dict]:
    """computeTradeOverlaySignals over a series slice (already mapped to net/buy/sell)."""
    signals, state = [], "FLAT"
    for i, pt in enumerate(series):
        prev = series[i - 1] if i > 0 else pt
        bd, sd = pt["buy"] - base["buy"], pt["sell"] - base["sell"]
        buy_flat = i > 0 and pt["buy"] == prev["buy"]
        sell_flat = i > 0 and pt["sell"] == prev["sell"]
        can_buy, can_sell = not buy_flat, not sell_flat

        def sig(t, switch, val, text):
            signals.append({"idx": i, "time": pt["time"], "type": t, "isSwitch": switch, "val": val,
                            "buy": bd, "sell": sd, "text": text})

        if state == "SELL":
            if sd < exit_threshold:
                state = "FLAT"
                sig("X", False, sd, "EXIT SELL")
            elif can_buy and bd > 0 and (sell_flat or bd > sd):
                state = "BUY"
                sig("X", True, sd, "EXIT SELL (BUY ENTERED)")
                sig("B", True, bd, "SWITCH BUY")
        elif state == "BUY":
            if bd < exit_threshold:
                state = "FLAT"
                sig("X", False, bd, "EXIT BUY")
            elif can_sell and sd > 0 and (buy_flat or sd > bd):
                state = "SELL"
                sig("X", True, bd, "EXIT BUY (SELL ENTERED)")
                sig("S", True, sd, "SWITCH SELL")
        else:
            if buy_flat and can_sell and sd > 0:
                state = "SELL"
                sig("S", False, sd, "SELL")
            elif sell_flat and can_buy and bd > 0:
                state = "BUY"
                sig("B", False, bd, "BUY")
            elif can_buy and bd > 0 and bd >= sd:
                state = "BUY"
                sig("B", False, bd, "BUY")
            elif can_sell and sd > 0 and sd > bd:
                state = "SELL"
                sig("S", False, sd, "SELL")
    return signals


def pair_overlay_trades(signals: list[dict], series: list[dict], base: dict) -> list[dict]:
    """pairOverlayTrades: entry (B/S) -> X on the same side; an unclosed trade is valued at the last point."""
    trades, open_ = [], None

    def flip(side, e, x):
        fs = "sell" if side == "buy" else "buy"
        if not series:
            return {}
        ep, xp = series[min(e, len(series) - 1)], series[min(x, len(series) - 1)]
        fe, fx = ep[fs] - base[fs], xp[fs] - base[fs]
        return {"flipSide": fs, "flipEntryVal": fe, "flipExitVal": fx, "flipPnl": fx - fe}

    for sig in signals:
        if sig["type"] == "X":
            if open_:
                pnl = sig["val"] - open_["entryVal"]
                trades.append({**open_, "exitIdx": sig["idx"], "exitTime": sig["time"], "exitVal": sig["val"], "pnl": pnl,
                               **flip(open_["side"], open_["entryIdx"], sig["idx"]), "isOpen": False})
                sig["pnl"], sig["entryTime"] = pnl, open_["entryTime"]
                open_ = None
        else:
            side = "buy" if sig["type"] == "B" else "sell"
            open_ = {"side": side, "entryIdx": sig["idx"], "entryTime": sig["time"], "entryVal": sig[side]}
    if open_ and series:
        last = len(series) - 1
        lv = series[last][open_["side"]] - base[open_["side"]]
        trades.append({**open_, "exitIdx": last, "exitTime": series[last]["time"], "exitVal": lv, "pnl": lv - open_["entryVal"],
                       **flip(open_["side"], open_["entryIdx"], last), "isOpen": True})
    return trades


def split_target_signal(signals: list[dict], series: list[dict], base: dict, daily_target: float = 500.0) -> dict | None:
    """computeSplitTargetSignal: first point where realised + open overlay P&L reaches the daily target."""
    if daily_target <= 0 or not series:
        return None
    by_idx: dict[int, list[dict]] = {}
    for s in signals:
        by_idx.setdefault(s["idx"], []).append(s)
    realised, open_, last_exit = 0.0, None, 0.0
    for idx, pt in enumerate(series):
        for s in by_idx.get(idx, []):
            if s["type"] == "X":
                if open_:
                    realised += s["val"] - open_["entryVal"]
                last_exit, open_ = s["val"], None
            elif s["type"] in ("B", "S"):
                side = "buy" if s["type"] == "B" else "sell"
                open_ = {"side": side, "entryVal": s[side]}
        cur = pt[open_["side"]] - base[open_["side"]] if open_ else last_exit
        cum = realised + ((cur - open_["entryVal"]) if open_ else 0)
        if cum >= daily_target:
            side = open_["side"] if open_ else "closed"
            return {"idx": idx, "time": pt["time"], "type": "T", "side": side, "val": cur, "cumulativePnl": cum,
                    "color": "#39ff14",
                    "text": f"DAILY TARGET ${js_to_fixed(daily_target)} HIT · {side.upper()} overlay P&L ${js_to_fixed(cum)}"}
    return None


def _at(series, idx):
    return series[min(idx, len(series) - 1)] if series else None


def point_at_or_before(model: dict, time) -> dict | None:
    """modelPointAtOrBeforeTime: binary search of the model's series by time string (<=)."""
    series = model.get("series") or []
    if not series or not time:
        return None
    lo, hi, found = 0, len(series) - 1, -1
    while lo <= hi:
        mid = (lo + hi) >> 1
        if str(series[mid].get("time") or "") <= str(time):
            found, lo = mid, mid + 1
        else:
            hi = mid - 1
    return series[found] if found >= 0 else None


def selected_time_join_at(model: dict) -> str:
    """selectedTimeJoinAt: HH:MM a selected-time rank joined, or '' for ordinary models."""
    if not re.match(r"^selected-time #\d+", str(model.get("comparisonRole") or "")):
        return ""
    return str(model.get("joined_at") or model.get("selectedAt") or "")[:5]


def selected_time_eligible_at(model: dict, time) -> bool:
    """selectedTimeModelEligibleAt."""
    joined = selected_time_join_at(model)
    return (not joined) or str(time or "")[:5] >= joined


def _replay_time_fn(models: list[dict], replay_series):
    """replayTimeAt: time of the replay series at idx, else the first model's series."""
    def at(idx: int) -> str:
        if replay_series:
            t = replay_series[min(idx, len(replay_series) - 1)].get("time")
            if t:
                return t
        s = (models[0].get("series") or []) if models else []
        if s:
            return s[min(idx, len(s) - 1)].get("time") or ""
        return ""
    return at


def _bases(models: list[dict], baseline_index: int, start: int, time_at) -> dict:
    baseline_time = time_at(start)
    out = {}
    for m in models:
        if baseline_index == 0:
            out[m["model"]] = base_point(m["series"], 0)
        else:
            out[m["model"]] = point_at_or_before(m, baseline_time) or base_point(m["series"], baseline_index)
    return out


def _metric(point: dict, key: str):
    """point[key] ?? point.net ?? 0"""
    v = point.get(key)
    if v is None:
        v = point.get("net")
    return 0 if v is None else v


@dataclass
class RuleContext:
    """Page state the assigned-rule path reads that is not part of the models: the per-model source-trade cache
    (assignedOverlayTradeCache), the date/product keys, the live-date staleness rule and the replay head.
    eligible_fallthrough: the page's overlayRuleCandidate eligibility filter currently ends with an unconditional
    'return false' (v2.65.24-v2.65.27, assigned rules select nothing). True = behave as the filter is evidently
    meant to (fall through to eligible); False = replicate the page as written."""
    trade_cache: dict = field(default_factory=dict)  # key "date|product_type|product|model" -> {"rows": [...], "cachedAt": ms}
    current_date: str = ""
    product_type: str = "forex"
    product: str = "all"
    live_date: str = ""
    now_ms: float = 0
    refresh_ms: float = 5 * 60 * 1000
    current_frame_index: int = -1
    max_frames: int | None = None
    return_type: str = "NET"
    eligible_fallthrough: bool = True

    def cache_key(self, model_id: str) -> str:
        return "|".join([self.current_date, self.product_type, self.product, model_id])


def _num(v, default=0.0):
    """Number(v) with JS semantics for the cases that occur here: None/'' -> 0, non-numeric -> NaN."""
    if v is None or v == "":
        return default
    try:
        return float(v)
    except (TypeError, ValueError):
        return float("nan")


def _finite(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and v == v and v not in (float("inf"), float("-inf"))


def time_of_day_minutes(value) -> float | None:
    """timeOfDayMinutes: minutes since midnight from 'HH:MM[:SS]' (optionally after a 'T' or space)."""
    m = re.search(r"(?:T|\s|^)(\d{2}):(\d{2})(?::(\d{2}))?", str(value or ""))
    return None if not m else int(m.group(1)) * 60 + int(m.group(2)) + int(m.group(3) or 0) / 60


def curve_point_at_or_before(series, value) -> dict | None:
    """curvePointAtOrBefore: last point whose minute <= target (series[0] if none)."""
    target = time_of_day_minutes(value)
    if not isinstance(series, list) or not series or target is None:
        return None
    found = None
    for point in series:
        minute = time_of_day_minutes(point.get("time"))
        if minute is None or minute > target:
            break
        found = point
    return found or series[0]


def source_trade_flip_results(model: dict, row: dict, head_time) -> dict:
    """sourceTradeFlipResults: the opposite side's curve change over a source trade's life."""
    side = str(row.get("signal") or "").lower()
    if side not in ("buy", "sell"):
        return {}
    flip = "sell" if side == "buy" else "buy"
    entry = curve_point_at_or_before(model.get("series"), row.get("opened"))
    status = str(row.get("status") or "").lower()
    exit_ = curve_point_at_or_before(model.get("series"), head_time if status == "open" else row.get("last_update"))
    if not entry or not exit_:
        return {}

    def curve_delta(point, kind):
        cands = [f"{flip}_net", flip] if kind == "net" else [f"{flip}_alt_net", f"alt_{flip}"]
        key = next((c for c in cands if _finite(_num(point.get(c), float("nan")))), None)
        return float(point[key]) if key else None

    ne, nx, ae, ax = curve_delta(entry, "net"), curve_delta(exit_, "net"), curve_delta(entry, "alt"), curve_delta(exit_, "alt")
    return {"flipSide": flip, "flipNet": None if ne is None or nx is None else nx - ne,
            "flipAltNet": None if ae is None or ax is None else ax - ae}


def overlay_rule_metric_value(metric, point: dict, base: dict) -> float:
    """overlayRuleMetricValue."""
    key = str(metric or "cum_net").lower()
    if key == "win_rate":
        return _num(point["win_rate"] if point.get("win_rate") is not None else point.get("alt_win_rate"))
    if key == "loss_rate":
        return _num(point["loss_rate"] if point.get("loss_rate") is not None else point.get("alt_loss_rate"))
    aliases = {
        "cum_net": ["cum_net", "net"], "net": ["net", "cum_net"],
        "cum_alt_net": ["cum_alt_net", "alt_net"], "alt_net": ["alt_net", "cum_alt_net"],
        "cum_buy_net": ["cum_buy_net", "buy_net", "buy"], "buy_net": ["buy_net", "cum_buy_net", "buy"],
        "cum_sell_net": ["cum_sell_net", "sell_net", "sell"], "sell_net": ["sell_net", "cum_sell_net", "sell"],
        "cum_buy_alt_net": ["cum_buy_alt_net", "buy_alt_net", "alt_buy"],
        "cum_sell_alt_net": ["cum_sell_alt_net", "sell_alt_net", "alt_sell"],
    }
    fields = aliases.get(key) or [key, key[4:] if key.startswith("cum_") else f"cum_{key}"]
    current = next((point[f] for f in fields if point.get(f) is not None), None)
    initial = next((base[f] for f in fields if base.get(f) is not None), None)
    if key.startswith("cum_"):
        return _num(current)
    return _num(current) - _num(initial)


def as_of_correlation(a, b, idx: int, value_at, baseline_index: int):
    """asOfCorrelation: Pearson correlation of two curves from the baseline to idx; None if < 3 points or no variance."""
    av, bv = [], []
    for i in range(min(baseline_index, idx), idx + 1):
        x, y = value_at(a, i), value_at(b, i)
        if _finite(x) and _finite(y):
            av.append(x)
            bv.append(y)
    if len(av) < 3:
        return None
    am, bm = sum(av) / len(av), sum(bv) / len(bv)
    cov = va = vb = 0.0
    for x, y in zip(av, bv):
        da, db = x - am, y - bm
        cov += da * db
        va += da * da
        vb += db * db
    return cov / math.sqrt(va * vb) if va and vb else None


def overlay_rule_candidate(ranked: list[dict], position, idx: int, rule_record: dict, metric_value, correlation,
                           replay_series, *, baseline_index: int, eligible_fallthrough: bool = True, options=None):
    """overlayRuleCandidate: pick the strategy (or strategy+side) an assigned rule selects at idx, or None."""
    options = options or {}
    config = (rule_record or {}).get("config")
    if not config:
        return None
    sd = lambda item: item.get("side") or ""  # noqa: E731
    held_candidate = None
    if position:
        held_candidate = next((i for i in ranked if i["model"]["model"] == position["model"]["model"]
                               and sd(i) == (position.get("side") or "")), None)
    excluded = set(options.get("exclude") or [])
    held = None if options.get("ignoreHeld") else held_candidate
    reference = held_candidate
    clock_model = ranked[0]["model"] if ranked else (held["model"] if held else None)
    clock_series = replay_series if replay_series else ((clock_model or {}).get("series"))

    def clock_at(i, default):
        if not clock_series or i < 0 or i >= len(clock_series):
            return default
        return str(clock_series[i].get("time") or default)

    n = len(clock_series) if clock_series else 1
    time = clock_at(min(idx, n - 1), "00:00") if clock_series else "00:00"
    start_time = clock_at(min(baseline_index, n - 1), "00:00") if clock_series else "00:00"
    point = lambda item: point_at_or_before(item["model"], time) or {}  # noqa: E731
    base_pt = lambda item: point_at_or_before(item["model"], start_time) or base_point(item["model"]["series"], baseline_index)  # noqa: E731

    filters = config.get("eligibility_filters") or []

    def passes(item):
        if f"{item['model']['model']}:{sd(item)}" in excluded:
            return False
        p = point(item)
        cum = _num(p["cum_net"] if p.get("cum_net") is not None else p.get("net"))
        cum_alt = _num(p["cum_alt_net"] if p.get("cum_alt_net") is not None else p.get("alt_net"))
        if "cum_net_positive" in filters and cum <= 0:
            return False
        if "cum_net_negative" in filters and cum >= 0:
            return False
        if "cum_alt_net_positive" in filters and cum_alt <= 0:
            return False
        side = config.get("trade_side")
        if side == "buy" and item.get("side") and item["side"] != "buy":
            return False
        if side == "sell" and item.get("side") and item["side"] != "sell":
            return False
        return bool(eligible_fallthrough)

    eligible = [i for i in ranked if passes(i)]
    held_still = bool(held) and any(i["model"]["model"] == held["model"]["model"] and sd(i) == sd(held) for i in eligible)

    def hm(t):
        a = t.split(":")
        h = _num(a[0] if a else "")
        m = _num(a[1] if len(a) > 1 else "")
        return (h * 60 if _finite(h) else 0) + (m if _finite(m) else 0)

    elapsed = max(0, hm(time) - hm(start_time))
    interval = max(1, _num(config.get("interval_minutes")) or 30)
    prev_time = clock_at(max(baseline_index, idx - 1), start_time) if clock_series else start_time
    prev_elapsed = max(0, hm(prev_time) - hm(start_time))
    is_baseline = idx == baseline_index
    crossed = math.floor(elapsed / interval) > math.floor(prev_elapsed / interval)
    if not options.get("forceEvaluation") and not is_baseline and not crossed and (not position or held_still):
        return held if held_still else None

    def metric_for(item, rule):
        return metric_value(item, rule.get("metric") or "cum_net", point(item), base_pt(item))

    def sorted_(items, rule, desc=True):
        keyed = [(_num(metric_for(i, rule)), str(i["model"]["model"]), i) for i in items]
        keyed.sort(key=lambda t: (-t[0] if desc else t[0], t[1]))
        return [t[2] for t in keyed]

    def choose(items, rule, desc=True):
        o = sorted_(items, rule, desc)
        return o[0] if o else None

    def group_items(items, rule):
        group = str(rule.get("group") or "").strip().lower()
        if not group:
            return []
        kind, _, value = group.partition(":")
        out = []
        for item in items:
            if kind == "family":
                actual = strategy_family_of(item["model"])
            elif kind == "product":
                actual = str(item["model"].get("product") or "").lower()
            elif kind == "product_type":
                actual = str(item["model"].get("product_type") or "").lower()
            else:
                actual = ""
            if actual == value or (kind == "family" and actual.startswith(value)):
                out.append(item)
        return out

    for rule in config.get("rules") or []:
        t = rule.get("type")
        if t in ("ranked_top", "ranked", "better_win_rate", "higher_loss_rate"):
            metric = "win_rate" if t == "better_win_rate" else "loss_rate" if t == "higher_loss_rate" else rule.get("metric")
            current = metric_for(held, {**rule, "metric": metric}) if held else None
            if held and t in ("better_win_rate", "higher_loss_rate"):
                qualified = [i for i in eligible if _num(metric_for(i, {**rule, "metric": metric})) > _num(current)]
            else:
                qualified = eligible
            cand = choose(qualified, {**rule, "metric": metric}, True)
            if cand:
                return cand
        elif t in ("ranked_bottom", "group_ranked_bottom"):
            pool = group_items(eligible, rule) if t == "group_ranked_bottom" else eligible
            cand = choose(pool, rule, False)
            if cand:
                return cand
        elif t in ("group_ranked_top", "group_ranked"):
            cand = choose(group_items(eligible, rule), rule, True)
            if cand:
                return cand
        elif t in ("similar_higher_net", "similar_lower_net", "similar") and reference:
            pool = [i for i in eligible if i["model"]["model"] != reference["model"]["model"] or i.get("side") != reference.get("side")]
            pool = [i for i in pool if (lambda c: -1 if c is None else c)(correlation(i, reference, idx)) >= 0.5]
            ordered = sorted_(pool, {**rule, "metric": "cum_net"}, t != "similar_lower_net")
            cand = ordered[0] if ordered else None
            if cand:
                cn = _num(metric_for(cand, {**rule, "metric": "cum_net"}))
                rn = _num(metric_for(reference, {**rule, "metric": "cum_net"}))
                if (cn < rn) if t == "similar_lower_net" else (cn > rn):
                    return cand
        elif t in ("opposite_top", "opposite_bottom", "opposite") and reference:
            pool = [i for i in eligible if i["model"]["model"] != reference["model"]["model"] or i.get("side") != reference.get("side")]
            pool = [i for i in pool if (lambda c: 1 if c is None else c)(correlation(i, reference, idx)) <= -0.5]
            ordered = sorted_(pool, rule, t != "opposite_bottom")
            if ordered:
                return ordered[0]
    return held if held_still else None


def apply_assigned_overlay_trade_results(intervals: list[dict], up_to_idx: int, replay_series, ctx: RuleContext,
                                         split_side=None) -> list[dict]:
    """applyAssignedOverlayTradeResults (rule active): replace each overlay interval's P&L with the source trades
    actually opened/closed inside it (from ctx.trade_cache); 'loading' when the cache has no entry yet."""
    head_time = replay_series[min(up_to_idx, len(replay_series) - 1)].get("time") if replay_series else None
    head_minute = time_of_day_minutes(head_time)
    latest_head = ctx.current_frame_index < 0 or ctx.current_frame_index >= (ctx.max_frames or 1) - 1
    metric = "alt_net_return" if ctx.return_type == "ALT" else "net_return"
    out = []
    for interval in intervals:
        cache = ctx.trade_cache.get(ctx.cache_key(interval["model"]))
        if not cache or (ctx.current_date == ctx.live_date and ctx.now_ms - cache["cachedAt"] >= ctx.refresh_ms):
            out.append({**interval, "pnl": 0, "actualTradeCount": None, "resultSource": "loading"})
            continue
        rows = cache["rows"]
        start_m = time_of_day_minutes(interval.get("entryTime"))
        end_m = head_minute if interval.get("isOpen") else time_of_day_minutes(interval.get("exitTime"))
        if start_m is None or end_m is None or head_minute is None:
            out.append({**interval, "pnl": 0, "actualTradeCount": 0, "actualTradeRows": [], "resultSource": "model-trades"})
            continue
        expected = split_side or (interval.get("side") if interval.get("side") in ("buy", "sell") else None)

        def keep(row):
            opened = time_of_day_minutes(row.get("opened"))
            if opened is None or opened < start_m or opened >= end_m or opened > head_minute:
                return False
            if expected and str(row.get("signal") or "").lower() != expected:
                return False
            status = str(row.get("status") or "").lower()
            if status == "closed":
                closed = time_of_day_minutes(row.get("last_update"))
                return closed is not None and closed < end_m + 1 and closed <= head_minute
            updated = time_of_day_minutes(row.get("last_update"))
            return status == "open" and latest_head and updated is not None and updated <= head_minute

        matched = [r for r in rows if keep(r)]
        sum_field = lambda f: sum((lambda v: 0 if v != v else v)(_num(r.get(f))) for r in matched)  # noqa: E731
        run_net = run_alt = 0.0
        cum_by_id = {}
        for r in sorted(rows, key=lambda r: time_of_day_minutes(r.get("opened")) or 0):
            run_net += (lambda v: 0 if v != v else v)(_num(r.get("net_return")))
            run_alt += (lambda v: 0 if v != v else v)(_num(r.get("alt_net_return")))
            cum_by_id[id(r)] = {"cumNet": run_net, "cumAltNet": run_alt}
        detailed = [{**r, **source_trade_flip_results(interval.get("curveModel") or {}, r, head_time), **cum_by_id.get(id(r), {})}
                    for r in matched]

        def sum_opt(f):
            vals = [d[f] for d in detailed if _finite(d.get(f))]
            return sum(vals) if vals else None

        out.append({**interval, "pnl": sum_field(metric), "actualTradeCount": len(matched),
                    "actualTradeNet": sum_field("net_return"), "actualTradeAltNet": sum_field("alt_net_return"),
                    "actualTradeRows": detailed, "flipNet": sum_opt("flipNet"), "flipAltNet": sum_opt("flipAltNet"),
                    "flipSide": next((d["flipSide"] for d in detailed if d.get("flipSide")), None),
                    "flipPnl": sum_opt("flipAltNet") if ctx.return_type == "ALT" else sum_opt("flipNet"),
                    "resultSource": "model-trades"})
    return out


def assigned_rule_target(signals: list[dict], trades: list[dict], daily_target: float, rule_active: bool) -> dict:
    """assignedRuleTarget."""
    if not rule_active:
        return {"signals": signals, "targetSignal": next((s for s in signals if s.get("type") == "T"), None)}
    clean = [s for s in signals if s.get("type") != "T"]
    if any(t.get("resultSource") == "loading" for t in trades) or daily_target <= 0:
        return {"signals": clean, "targetSignal": None}
    cum = 0.0
    for t in trades:
        v = _num(t.get("pnl"))
        cum += 0 if v != v else v
        if cum < daily_target:
            continue
        target = {"idx": t["exitIdx"], "time": t["exitTime"], "type": "T", "model": t["model"], "color": "#39ff14",
                  "val": t["exitVal"], "cumulativePnl": cum,
                  "text": f"DAILY TARGET ${js_to_fixed(daily_target)} HIT · assigned-rule trade results ${js_to_fixed(cum)}"}
        clean.append(target)
        return {"signals": clean, "targetSignal": target}
    return {"signals": clean, "targetSignal": None}


def _rule_numbers(overlay_rule, exit_threshold, hold_rank):
    if overlay_rule:
        cfg = overlay_rule.get("config") or {}
        return float(cfg.get("exit_threshold") or 0), float(cfg.get("hold_rank") or 1)
    return exit_threshold, hold_rank


def _finish(signals, trades, threshold, overlay_rule, daily_target, replay_series, up_to_idx, ctx):
    """applyAssignedOverlayTradeResults + assignedRuleTarget, then drop the internal curveModel handle."""
    if overlay_rule is not None:
        trades = apply_assigned_overlay_trade_results(trades, up_to_idx, replay_series, ctx or RuleContext())
    tgt = assigned_rule_target(signals, trades, daily_target, overlay_rule is not None)
    trades = [{k: v for k, v in t.items() if k != "curveModel"} for t in trades]
    return {"signals": tgt["signals"], "trades": trades, "threshold": threshold, "targetSignal": tgt["targetSignal"]}


def leader_rotation(models: list[dict], metric_key: str, up_to_idx: int, *, baseline_index=0, exit_threshold=0.0,
                    daily_target=500.0, replay_series=None, hold_rank=1, overlay_rule=None,
                    rule_context: RuleContext | None = None) -> dict:
    """computeLeaderRotation (Total Net strategy rotation) of page v2.65.24-27, including the assigned overlay-rule path.
    overlay_rule: the rule record {"id","name","config"} assigned to the active portfolio, or None for the generic path."""
    ctx = rule_context or RuleContext()
    active_exit, active_hold = _rule_numbers(overlay_rule, exit_threshold, hold_rank)
    signals, trades = [], []
    threshold = abs(active_exit)
    start = min(baseline_index, up_to_idx)
    time_at = _replay_time_fn(models, replay_series)
    bases = _bases(models, baseline_index, start, time_at)
    st = {"pos": None, "realised": 0.0, "target": None}

    def delta(m, idx):
        p, b = point_at_or_before(m, time_at(idx)), bases.get(m["model"])
        if not p or not b:
            return None
        return _metric(p, metric_key) - _metric(b, metric_key)

    def close(idx, time, switch):
        pos = st["pos"]
        if not pos:
            return
        ev = delta(pos["model"], idx)
        if ev is None:
            return
        pnl = ev - pos["entryVal"]
        trades.append({"side": "strategy", "label": pos["model"]["model"], "model": pos["model"]["model"],
                       "curveModel": pos["model"], "color": pos["model"].get("color"), "entryIdx": pos["entryIdx"],
                       "entryTime": pos["entryTime"], "entryVal": pos["entryVal"], "exitIdx": idx, "exitTime": time,
                       "exitVal": ev, "pnl": pnl, "isOpen": False})
        st["realised"] += pnl
        signals.append({"idx": idx, "time": time, "type": "X", "model": pos["model"]["model"],
                        "color": pos["model"].get("color"), "val": ev, "pnl": pnl,
                        "text": f"{'ROTATE OUT' if switch else 'EXIT'} {pos['model']['model']}"})
        st["pos"] = None

    def enter(leader, idx, time, text="ENTER LEADER"):
        st["pos"] = {"model": leader["model"], "entryIdx": idx, "entryTime": time, "entryVal": leader["delta"]}
        signals.append({"idx": idx, "time": time, "type": "B", "model": leader["model"]["model"],
                        "color": leader["model"].get("color"), "val": leader["delta"],
                        "text": f"{text} {leader['model']['model']}"})

    def mark_target(idx, time):
        if st["target"] or daily_target <= 0:
            return
        pos = st["pos"]
        held = delta(pos["model"], idx) if pos else None
        cum = st["realised"] + ((held - pos["entryVal"]) if pos and held is not None else 0)
        if cum < daily_target:
            return
        st["target"] = {"idx": idx, "time": time, "type": "T", "model": pos["model"]["model"] if pos else "",
                        "color": "#f59e0b", "val": held if held is not None else 0, "cumulativePnl": cum,
                        "text": f"DAILY TARGET ${js_to_fixed(daily_target)} HIT · overlay P&L ${js_to_fixed(cum)}"}
        signals.append(st["target"])

    def corr_value(item, i):
        p = point_at_or_before(item["model"] if "model" in item else item, time_at(i)) or {}
        b = bases.get((item["model"] if "model" in item else item)["model"]) or {}
        return _num(p["cum_net"] if p.get("cum_net") is not None else p.get("net")) - \
            _num(b["cum_net"] if b.get("cum_net") is not None else b.get("net"))

    for idx in range(start, up_to_idx + 1):
        time = time_at(idx)
        ranked = sorted(({"model": m, "delta": d} for m in models
                         if selected_time_eligible_at(m, time) and (d := delta(m, idx)) is not None),
                        key=lambda r: -r["delta"])
        if overlay_rule is not None:
            leader = overlay_rule_candidate(
                ranked, st["pos"], idx, overlay_rule, lambda item, metric, point, base: overlay_rule_metric_value(metric, point, base),
                lambda cand, held, at: as_of_correlation(cand["model"], held["model"], at,
                                                         lambda m, i: corr_value({"model": m}, i), baseline_index),
                replay_series, baseline_index=baseline_index, eligible_fallthrough=ctx.eligible_fallthrough)
            if not st["pos"]:
                if leader:
                    enter(leader, idx, time, "ENTER RULE")
            elif not leader:
                close(idx, time, False)
            elif leader["model"]["model"] != st["pos"]["model"]["model"]:
                close(idx, time, True)
                enter(leader, idx, time, "ENTER RULE")
            mark_target(idx, time)
            continue
        leader = ranked[0] if ranked else None
        if not st["pos"]:
            if leader and leader["delta"] > threshold:
                enter(leader, idx, time)
            mark_target(idx, time)
            continue
        pos = st["pos"]
        held = delta(pos["model"], idx)
        held_n = 0 if held is None else held
        prev_held = delta(pos["model"], idx - 1) if idx > start else None
        if held_n < 0 and prev_held is not None and prev_held >= 0:
            held_id = pos["model"]["model"]
            close(idx, time, False)
            if leader and leader["model"]["model"] != held_id and leader["delta"] > threshold:
                enter(leader, idx, time)
            mark_target(idx, time)
            continue
        if not leader or leader["delta"] <= 0:
            if held_n <= active_exit:
                close(idx, time, False)
            mark_target(idx, time)
            continue
        held_rank_index = next((i for i, r in enumerate(ranked) if r["model"]["model"] == pos["model"]["model"]), -1)
        held_rank = float("inf") if held_rank_index < 0 else held_rank_index + 1
        if (leader["model"]["model"] != pos["model"]["model"] and held_rank > active_hold
                and leader["delta"] - held_n > threshold):
            close(idx, time, True)
            enter(leader, idx, time)
        mark_target(idx, time)
    pos = st["pos"]
    if pos:
        ev = delta(pos["model"], up_to_idx)
        ev = float("nan") if ev is None else ev
        trades.append({"side": "strategy", "label": pos["model"]["model"], "model": pos["model"]["model"],
                       "curveModel": pos["model"], "color": pos["model"].get("color"), "entryIdx": pos["entryIdx"],
                       "entryTime": pos["entryTime"], "entryVal": pos["entryVal"], "exitIdx": up_to_idx,
                       "exitTime": time_at(up_to_idx), "exitVal": ev, "pnl": ev - pos["entryVal"], "isOpen": True})
    return _finish(signals, trades, threshold, overlay_rule, daily_target, replay_series, up_to_idx, ctx)


def multi_split_rotation(models: list[dict], keys: dict, up_to_idx: int, *, baseline_index=0, exit_threshold=0.0,
                         daily_target=500.0, replay_series=None, hold_rank=1, overlay_rule=None,
                         rule_context: RuleContext | None = None) -> dict:
    """computeMultiSplitRotation of page v2.65.24-27, including the assigned overlay-rule path: every model's Buy and
    Sell side is a candidate; same product+direction exposure is de-duplicated."""
    ctx = rule_context or RuleContext()
    active_exit, active_hold = _rule_numbers(overlay_rule, exit_threshold, hold_rank)
    signals, trades = [], []
    threshold = abs(active_exit)
    start = min(baseline_index, up_to_idx)
    time_at = _replay_time_fn(models, replay_series)
    bases = _bases(models, baseline_index, start, time_at)
    st = {"pos": None, "realised": 0.0, "target": None}

    def product_for(m):
        p = str(m.get("product") or "").strip().upper()
        return p or f"MODEL:{m.get('model', '')}"

    def exposure(c):
        return (product_for(c["model"]), c["side"])

    def key_for(m, side):
        pref = keys["buyKey"] if side == "buy" else keys["sellKey"]
        return pref if m["series"] and pref in m["series"][0] else side

    def num(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return float("nan")

    def delta(m, side, idx):
        p, b, k = point_at_or_before(m, time_at(idx)), bases.get(m["model"]), key_for(m, side)
        if not p or not b:
            return None
        return (0 if p.get(k) is None else p[k]) - (0 if b.get(k) is None else b[k])

    def active(m, side, idx):
        if idx <= start:
            return True
        k = key_for(m, side)
        now, prev = point_at_or_before(m, time_at(idx)), point_at_or_before(m, time_at(idx - 1))
        return bool(now and prev and now.get("time") != prev.get("time") and num(now.get(k)) != num(prev.get(k)))

    def trade_row(pos, idx, exit_val, time, is_open):
        fs = "sell" if pos["side"] == "buy" else "buy"
        fe, fx = delta(pos["model"], fs, pos["entryIdx"]), delta(pos["model"], fs, idx)
        return {"side": pos["side"], "curveModel": pos["model"], "product": product_for(pos["model"]),
                "label": f"{product_for(pos['model'])} · {pos['side'].upper()}",
                "model": pos["model"]["model"], "color": pos["model"].get("color"), "entryIdx": pos["entryIdx"],
                "entryTime": pos["entryTime"], "entryVal": pos["entryVal"], "exitIdx": idx, "exitTime": time,
                "exitVal": exit_val, "pnl": exit_val - pos["entryVal"], "flipSide": fs, "flipEntryVal": fe,
                "flipExitVal": fx, "flipPnl": None if fe is None or fx is None else fx - fe, "isOpen": is_open}

    def close(idx, time, switch):
        pos = st["pos"]
        if not pos:
            return
        ev = delta(pos["model"], pos["side"], idx)
        if ev is None:
            return
        t = trade_row(pos, idx, ev, time, False)
        trades.append(t)
        st["realised"] += t["pnl"]
        signals.append({"idx": idx, "time": time, "type": "X", "side": pos["side"], "model": pos["model"]["model"],
                        "color": pos["model"].get("color"), "val": ev, "pnl": t["pnl"],
                        "text": f"{'ROTATE OUT' if switch else 'EXIT'} {pos['model']['model']} {pos['side'].upper()}"})
        st["pos"] = None

    def enter(c, idx, time):
        st["pos"] = {"model": c["model"], "side": c["side"], "entryIdx": idx, "entryTime": time, "entryVal": c["delta"]}
        signals.append({"idx": idx, "time": time, "type": "B" if c["side"] == "buy" else "S", "side": c["side"],
                        "model": c["model"]["model"], "color": c["model"].get("color"), "val": c["delta"],
                        "buy": c["delta"] if c["side"] == "buy" else None,
                        "sell": c["delta"] if c["side"] == "sell" else None,
                        "text": f"ENTER {c['model']['model']} {c['side'].upper()}"})

    def mark_target(idx, time):
        if st["target"] or daily_target <= 0:
            return
        pos = st["pos"]
        held = delta(pos["model"], pos["side"], idx) if pos else None
        cum = st["realised"] + ((held - pos["entryVal"]) if pos and held is not None else 0)
        if cum < daily_target:
            return
        name = pos["model"]["model"] if pos else "CLOSED"
        side = pos["side"].upper() if pos else ""
        st["target"] = {"idx": idx, "time": time, "type": "T", "side": pos["side"] if pos else "closed",
                        "model": pos["model"]["model"] if pos else "", "color": "#39ff14",
                        "val": held if held is not None else 0, "cumulativePnl": cum,
                        "text": f"DAILY TARGET ${js_to_fixed(daily_target)} HIT · {name} {side} · overlay P&L ${js_to_fixed(cum)}"}
        signals.append(st["target"])

    def corr_value(m, i):
        p = point_at_or_before(m, time_at(i)) or {}
        b = bases.get(m["model"]) or {}
        return _num(p["cum_net"] if p.get("cum_net") is not None else p.get("net")) - \
            _num(b["cum_net"] if b.get("cum_net") is not None else b.get("net"))

    for idx in range(start, up_to_idx + 1):
        time = time_at(idx)
        ranked = sorted(({"model": m, "side": s, "delta": d, "active": active(m, s, idx)} for m in models
                         if selected_time_eligible_at(m, time) for s in ("buy", "sell")
                         if (d := delta(m, s, idx)) is not None),
                        key=lambda r: -r["delta"])
        ranked = [r for r in ranked if overlay_rule is not None or r["active"]]
        if overlay_rule is not None:
            leader = overlay_rule_candidate(
                ranked, st["pos"], idx, overlay_rule, lambda item, metric, point, base: overlay_rule_metric_value(metric, point, base),
                lambda cand, held, at: as_of_correlation(cand["model"], held["model"], at, corr_value, baseline_index),
                replay_series, baseline_index=baseline_index, eligible_fallthrough=ctx.eligible_fallthrough)
            pos = st["pos"]
            if not pos:
                if leader:
                    enter(leader, idx, time)
            elif not leader:
                close(idx, time, False)
            elif leader["model"]["model"] != pos["model"]["model"] or leader["side"] != pos["side"]:
                close(idx, time, True)
                enter(leader, idx, time)
            mark_target(idx, time)
            continue
        leader = ranked[0] if ranked else None
        if not st["pos"]:
            if leader and leader["delta"] > threshold:
                enter(leader, idx, time)
            mark_target(idx, time)
            continue
        pos = st["pos"]
        held = delta(pos["model"], pos["side"], idx)
        held_n = 0 if held is None else held
        prev_held = delta(pos["model"], pos["side"], idx - 1) if idx > start else None
        if held_n < 0 and prev_held is not None and prev_held >= 0:
            held_exp = exposure(pos)
            close(idx, time, False)
            if leader and exposure(leader) != held_exp and leader["delta"] > threshold:
                enter(leader, idx, time)
            mark_target(idx, time)
            continue
        if not leader or leader["delta"] <= 0:
            if held_n <= active_exit:
                close(idx, time, False)
            mark_target(idx, time)
            continue
        hri = next((i for i, r in enumerate(ranked)
                    if r["model"]["model"] == pos["model"]["model"] and r["side"] == pos["side"]), -1)
        held_rank = float("inf") if hri < 0 else hri + 1
        same_cand = leader["model"]["model"] == pos["model"]["model"] and leader["side"] == pos["side"]
        same_exp = exposure(leader) == exposure(pos)
        if not same_cand and not same_exp and held_rank > active_hold and leader["delta"] - held_n > threshold:
            close(idx, time, True)
            enter(leader, idx, time)
        mark_target(idx, time)
    pos = st["pos"]
    if pos:
        ev = delta(pos["model"], pos["side"], up_to_idx)
        ev = float("nan") if ev is None else ev
        trades.append(trade_row(pos, up_to_idx, ev, time_at(up_to_idx), True))
    return _finish(signals, trades, threshold, overlay_rule, daily_target, replay_series, up_to_idx, ctx)
