# epics/ep_057_sql_to_pgsql/scenario_engine_v2/engine/intelligence.py — strategy intelligence for agents: top performers, correlated groups, spread widening / collapsing, as of a point in time.
#
# VERSION HISTORY
# v1.0.0 · 2026-10-17 · Initial version: report(models, as_of_index) = top N with drawdown / momentum, correlation clusters, pair spread signals (z-score, trend, half-life), confidence and caveats; no look-ahead.
"""Pure functions over model dicts ({model, series:[{time, net, buy, sell, alt_net...}]}). Everything is computed from points at or before `as_of_index` only, and the report states the
snapshot time it used, so an agent can see exactly what it knew. The numbers are evidence for a decision, not a recommendation: every section carries its sample size and caveats."""
from __future__ import annotations

import math

from . import core_ported as core


def _net_series(model: dict, return_type: str) -> list[float]:
    key = core.metric_keys(return_type)["netKey"]
    out = []
    for p in model.get("series") or []:
        v = p.get(key, p.get("net"))
        out.append(float(v) if v is not None else 0.0)
    return out


def _pearson(a: list[float], b: list[float]) -> float | None:
    n = min(len(a), len(b))
    if n < 3:
        return None
    a, b = a[-n:], b[-n:]
    ma, mb = sum(a) / n, sum(b) / n
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((y - mb) ** 2 for y in b)
    if va <= 0 or vb <= 0:
        return None
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / math.sqrt(va * vb)


def _increments(vals: list[float]) -> list[float]:
    return [b - a for a, b in zip(vals, vals[1:])]


def _max_drawdown(vals: list[float]) -> float:
    peak, worst = float("-inf"), 0.0
    for v in vals:
        peak = max(peak, v)
        worst = min(worst, v - peak)
    return worst


def top_performers(curves: dict[str, list[float]], times: dict[str, str], n: int = 3, momentum_window: int = 12) -> list[dict]:
    rows = []
    for mid, vals in curves.items():
        if not vals:
            continue
        look = vals[-1 - momentum_window] if len(vals) > momentum_window else vals[0]
        rows.append({"model": mid, "net": vals[-1], "momentum": vals[-1] - look, "max_drawdown": _max_drawdown(vals), "points": len(vals), "as_of": times.get(mid)})
    rows.sort(key=lambda r: (-r["net"], r["model"]))
    for i, r in enumerate(rows[:n]):
        r["rank"] = i + 1
    return rows[:n]


def correlation_clusters(curves: dict[str, list[float]], window: int = 48, threshold: float = 0.7) -> list[dict]:
    ids = sorted(curves)
    inc = {m: _increments(curves[m])[-window:] for m in ids}
    corr, parent = {}, {m: m for m in ids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            c = _pearson(inc[a], inc[b])
            if c is not None:
                corr[(a, b)] = c
                if c >= threshold:
                    parent[find(a)] = find(b)
    groups: dict[str, list[str]] = {}
    for m in ids:
        groups.setdefault(find(m), []).append(m)
    out = []
    for members in groups.values():
        if len(members) < 2:
            continue
        cs = [corr[(a, b)] for i, a in enumerate(members) for b in members[i + 1:] if (a, b) in corr]
        out.append({"members": members, "avg_correlation": round(sum(cs) / len(cs), 4) if cs else None, "min_correlation": round(min(cs), 4) if cs else None, "window": window})
    out.sort(key=lambda g: (-(g["avg_correlation"] or 0), g["members"]))
    return out


def spread_signal(a: str, b: str, va: list[float], vb: list[float], window: int = 48, z_hi: float = 1.5) -> dict | None:
    n = min(len(va), len(vb))
    if n < 8:
        return None
    spread = [x - y for x, y in zip(va[-n:], vb[-n:])][-window:]
    m = sum(spread) / len(spread)
    sd = math.sqrt(sum((s - m) ** 2 for s in spread) / len(spread))
    if sd <= 0:
        return None
    z = (spread[-1] - m) / sd
    z_prev = (spread[-4] - m) / sd if len(spread) > 4 else z
    # AR(1) on the spread: phi < 1 means it pulls back; half-life = ln 0.5 / ln phi
    x, y = spread[:-1], spread[1:]
    mx, my = sum(x) / len(x), sum(y) / len(y)
    denom = sum((u - mx) ** 2 for u in x)
    phi = sum((u - mx) * (w - my) for u, w in zip(x, y)) / denom if denom > 0 else None
    half_life = round(math.log(0.5) / math.log(phi), 2) if phi is not None and 0 < phi < 1 else None
    if abs(z) >= z_hi and abs(z) > abs(z_prev) + 0.05:
        state = "widening"
    elif abs(z_prev) >= z_hi and abs(z) < abs(z_prev) - 0.05:
        state = "collapsing"
    elif abs(z) >= z_hi:
        state = "stretched"
    else:
        state = "normal"
    return {"pair": [a, b], "spread": round(spread[-1], 4), "z": round(z, 3), "z_3_ago": round(z_prev, 3), "state": state, "half_life_points": half_life,
            "ar1": None if phi is None else round(phi, 3), "window": len(spread), "leader": a if spread[-1] > 0 else b}


def report(models: list[dict], *, return_type: str = "NET", as_of_index: int | None = None, top_n: int = 3, window: int = 48, corr_threshold: float = 0.7, z_hi: float = 1.5) -> dict:
    curves, times = {}, {}
    for m in models:
        vals = _net_series(m, return_type)
        if as_of_index is not None:
            vals = vals[:as_of_index + 1]
        pts = (m.get("series") or [])[:len(vals)]
        curves[m["model"]] = vals
        times[m["model"]] = pts[-1].get("time") if pts else None
    clusters = correlation_clusters(curves, window, corr_threshold)
    signals = []
    for c in clusters:
        mem = c["members"]
        for i, a in enumerate(mem):
            for b in mem[i + 1:]:
                s = spread_signal(a, b, curves[a], curves[b], window, z_hi)
                if s:
                    s["cluster_correlation"] = c["avg_correlation"]
                    signals.append(s)
    signals.sort(key=lambda s: -abs(s["z"]))
    sample = min((len(v) for v in curves.values()), default=0)
    caveats = []
    if sample < window:
        caveats.append(f"only {sample} points available (window {window}): statistics are weak")
    if len(curves) < 3:
        caveats.append("fewer than three strategies: rankings and clusters are thin")
    caveats.append("past curves only: correlation and spread behaviour can change; this is evidence, not advice")
    return {"as_of": max((t for t in times.values() if t), default=None), "as_of_index": as_of_index, "return_type": return_type, "strategies": len(curves), "sample_points": sample,
            "top": top_performers(curves, times, top_n), "clusters": clusters, "spread_signals": signals,
            "confidence": "low" if sample < window else ("medium" if sample < 3 * window else "high"), "caveats": caveats}
