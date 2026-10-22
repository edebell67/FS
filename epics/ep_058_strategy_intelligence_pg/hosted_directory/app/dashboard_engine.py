# epics/ep_058_strategy_intelligence_pg/hosted_directory/app/dashboard_engine.py — server-side port of the dashboard's client-side logic.
#
# VERSION HISTORY
# v1.0.0 · 2026-09-26 · Python port of top10_5min_equity_curves.html v2.30.0 functions: getMetricKeys, getBasePoint, getReplayHeadPoint,
#   getScenarioCandidates/getEligibleModels, updateRibbon aggregates, computeTradeOverlaySignals, pairOverlayTrades,
#   computeSplitTargetSignal, computeLeaderRotation, computeMultiSplitRotation. Keep in step with the page by hand.
"""Pure functions over model dicts shaped like build_live_day() output ({model, product, series:[{time,net,buy,sell,alt_*}]})."""
from __future__ import annotations


def metric_keys(return_type: str = "NET") -> dict[str, str]:
    alt = str(return_type).upper() == "ALT"
    return {"netKey": "alt_net" if alt else "net", "buyKey": "alt_buy" if alt else "buy",
            "sellKey": "alt_sell" if alt else "sell", "cumNetKey": "cum_alt_net" if alt else "cum_net",
            "winRateKey": "alt_win_rate" if alt else "win_rate"}


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
                    "text": f"DAILY TARGET ${daily_target:.0f} HIT · {side.upper()} overlay P&L ${cum:.0f}"}
    return None


def _at(series, idx):
    return series[min(idx, len(series) - 1)] if series else None


def leader_rotation(models: list[dict], metric_key: str, up_to_idx: int, *, baseline_index=0, exit_threshold=0.0,
                    daily_target=500.0) -> dict:
    """computeLeaderRotation (Total Net strategy rotation)."""
    signals, trades = [], []
    threshold = abs(exit_threshold)
    start = min(baseline_index, up_to_idx)
    bases = {m["model"]: base_point(m["series"], baseline_index) for m in models}
    state = {"pos": None, "realised": 0.0, "target": None}

    def delta(m, idx):
        p, b = _at(m["series"], idx), bases.get(m["model"])
        if not p or not b:
            return None
        pv = p.get(metric_key) if p.get(metric_key) is not None else p.get("net", 0)
        bv = b.get(metric_key) if b.get(metric_key) is not None else b.get("net", 0)
        return pv - bv

    def close(idx, time, switch):
        pos = state["pos"]
        if not pos:
            return
        ev = delta(pos["model"], idx)
        if ev is None:
            return
        pnl = ev - pos["entryVal"]
        trades.append({"side": "strategy", "label": pos["model"]["model"], "model": pos["model"]["model"],
                       "color": pos["model"].get("color"), "entryIdx": pos["entryIdx"], "entryTime": pos["entryTime"],
                       "entryVal": pos["entryVal"], "exitIdx": idx, "exitTime": time, "exitVal": ev, "pnl": pnl, "isOpen": False})
        state["realised"] += pnl
        signals.append({"idx": idx, "time": time, "type": "X", "model": pos["model"]["model"], "val": ev, "pnl": pnl,
                        "text": f"{'ROTATE OUT' if switch else 'EXIT'} {pos['model']['model']}"})
        state["pos"] = None

    def enter(leader, idx, time):
        state["pos"] = {"model": leader["model"], "entryIdx": idx, "entryTime": time, "entryVal": leader["delta"]}
        signals.append({"idx": idx, "time": time, "type": "B", "model": leader["model"]["model"], "val": leader["delta"],
                        "text": f"ENTER LEADER {leader['model']['model']}"})

    def mark_target(idx, time):
        if state["target"] or daily_target <= 0:
            return
        pos = state["pos"]
        held = delta(pos["model"], idx) if pos else None
        cum = state["realised"] + ((held - pos["entryVal"]) if pos and held is not None else 0)
        if cum < daily_target:
            return
        state["target"] = {"idx": idx, "time": time, "type": "T", "model": pos["model"]["model"] if pos else "",
                           "val": held or 0, "cumulativePnl": cum,
                           "text": f"DAILY TARGET ${daily_target:.0f} HIT · overlay P&L ${cum:.0f}"}
        signals.append(state["target"])

    for idx in range(start, up_to_idx + 1):
        ranked = sorted(({"model": m, "delta": d} for m in models if (d := delta(m, idx)) is not None),
                        key=lambda r: -r["delta"])
        leader = ranked[0] if ranked else None
        time = (_at(leader["model"]["series"], idx) or {}).get("time", "") if leader else ""
        pos = state["pos"]
        if not pos:
            if leader and leader["delta"] > threshold:
                enter(leader, idx, time)
            mark_target(idx, time)
            continue
        held = delta(pos["model"], idx)
        if not leader or leader["delta"] <= 0:
            if held <= exit_threshold:
                close(idx, time, False)
            mark_target(idx, time)
            continue
        if leader["model"]["model"] != pos["model"]["model"] and leader["delta"] - held > threshold:
            close(idx, time, True)
            enter(leader, idx, time)
        mark_target(idx, time)
    pos = state["pos"]
    if pos:
        ev = delta(pos["model"], up_to_idx)
        trades.append({"side": "strategy", "label": pos["model"]["model"], "model": pos["model"]["model"],
                       "color": pos["model"].get("color"), "entryIdx": pos["entryIdx"], "entryTime": pos["entryTime"],
                       "entryVal": pos["entryVal"], "exitIdx": up_to_idx,
                       "exitTime": (_at(pos["model"]["series"], up_to_idx) or {}).get("time", ""), "exitVal": ev,
                       "pnl": ev - pos["entryVal"], "isOpen": True})
    return {"signals": signals, "trades": trades, "threshold": threshold, "targetSignal": state["target"]}


def multi_split_rotation(models: list[dict], keys: dict, up_to_idx: int, *, baseline_index=0, exit_threshold=0.0,
                         daily_target=500.0) -> dict:
    """computeMultiSplitRotation: every model's Buy and Sell side is a candidate; de-duplicated by product+direction exposure."""
    signals, trades = [], []
    threshold = abs(exit_threshold)
    start = min(baseline_index, up_to_idx)
    bases = {m["model"]: base_point(m["series"], baseline_index) for m in models}
    state = {"pos": None, "realised": 0.0, "target": None}

    def product_for(m):
        p = str(m.get("product") or "").strip().upper()
        return p or f"MODEL:{m.get('model', '')}"

    def key_for(m, side):
        pref = keys["buyKey"] if side == "buy" else keys["sellKey"]
        return pref if m["series"] and pref in m["series"][0] else side

    def delta(m, side, idx):
        p, b, k = _at(m["series"], idx), bases.get(m["model"]), key_for(m, side)
        if not p or not b:
            return None
        return float(p.get(k) or 0) - float(b.get(k) or 0)

    def active(m, side, idx):
        if idx <= start:
            return True
        k = key_for(m, side)
        now, prev = _at(m["series"], idx), _at(m["series"], idx - 1)
        return bool(now and prev and float(now.get(k) or 0) != float(prev.get(k) or 0))

    def trade_row(pos, idx, exit_val, time, is_open):
        fs = "sell" if pos["side"] == "buy" else "buy"
        fe, fx = delta(pos["model"], fs, pos["entryIdx"]), delta(pos["model"], fs, idx)
        return {"side": pos["side"], "product": product_for(pos["model"]),
                "label": f"{product_for(pos['model'])} · {pos['side'].upper()}",
                "model": pos["model"]["model"], "color": pos["model"].get("color"), "entryIdx": pos["entryIdx"],
                "entryTime": pos["entryTime"], "entryVal": pos["entryVal"], "exitIdx": idx, "exitTime": time,
                "exitVal": exit_val, "pnl": exit_val - pos["entryVal"], "flipSide": fs, "flipEntryVal": fe,
                "flipExitVal": fx, "flipPnl": None if fe is None or fx is None else fx - fe, "isOpen": is_open}

    def close(idx, time, switch):
        pos = state["pos"]
        if not pos:
            return
        ev = delta(pos["model"], pos["side"], idx)
        if ev is None:
            return
        t = trade_row(pos, idx, ev, time, False)
        trades.append(t)
        state["realised"] += t["pnl"]
        signals.append({"idx": idx, "time": time, "type": "X", "side": pos["side"], "model": pos["model"]["model"],
                        "val": ev, "pnl": t["pnl"],
                        "text": f"{'ROTATE OUT' if switch else 'EXIT'} {pos['model']['model']} {pos['side'].upper()}"})
        state["pos"] = None

    def enter(c, idx, time):
        state["pos"] = {"model": c["model"], "side": c["side"], "entryIdx": idx, "entryTime": time, "entryVal": c["delta"]}
        signals.append({"idx": idx, "time": time, "type": "B" if c["side"] == "buy" else "S", "side": c["side"],
                        "model": c["model"]["model"], "val": c["delta"],
                        "buy": c["delta"] if c["side"] == "buy" else None,
                        "sell": c["delta"] if c["side"] == "sell" else None,
                        "text": f"ENTER {c['model']['model']} {c['side'].upper()}"})

    def mark_target(idx, time):
        if state["target"] or daily_target <= 0:
            return
        pos = state["pos"]
        held = delta(pos["model"], pos["side"], idx) if pos else None
        cum = state["realised"] + ((held - pos["entryVal"]) if pos and held is not None else 0)
        if cum < daily_target:
            return
        state["target"] = {"idx": idx, "time": time, "type": "T", "side": pos["side"] if pos else "closed",
                           "model": pos["model"]["model"] if pos else "", "val": held or 0, "cumulativePnl": cum,
                           "text": f"DAILY TARGET ${daily_target:.0f} HIT · overlay P&L ${cum:.0f}"}
        signals.append(state["target"])

    for idx in range(start, up_to_idx + 1):
        ranked = sorted(({"model": m, "side": s, "delta": d} for m in models for s in ("buy", "sell")
                         if (d := delta(m, s, idx)) is not None and active(m, s, idx)), key=lambda r: -r["delta"])
        leader = ranked[0] if ranked else None
        pos = state["pos"]
        time = ((_at(leader["model"]["series"], idx) or {}).get("time") if leader else None) \
            or ((_at(pos["model"]["series"], idx) or {}).get("time") if pos else "") or ""
        if not pos:
            if leader and leader["delta"] > threshold:
                enter(leader, idx, time)
            mark_target(idx, time)
            continue
        held = delta(pos["model"], pos["side"], idx)
        if not leader or leader["delta"] <= 0:
            if held <= exit_threshold:
                close(idx, time, False)
            mark_target(idx, time)
            continue
        same_cand = leader["model"]["model"] == pos["model"]["model"] and leader["side"] == pos["side"]
        same_exp = (product_for(leader["model"]), leader["side"]) == (product_for(pos["model"]), pos["side"])
        if not same_cand and not same_exp and leader["delta"] - held > threshold:
            close(idx, time, True)
            enter(leader, idx, time)
        mark_target(idx, time)
    pos = state["pos"]
    if pos:
        ev = delta(pos["model"], pos["side"], up_to_idx)
        trades.append(trade_row(pos, up_to_idx, ev,
                                (_at(pos["model"]["series"], up_to_idx) or {}).get("time", ""), True))
    return {"signals": signals, "trades": trades, "threshold": threshold, "targetSignal": state["target"]}
