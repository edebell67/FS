# epics/ep_057_sql_to_pgsql/scenario_engine_v2/engine/rpc.py — the call contract between the browser copy of the page and the engine: overlay signals, trades, daily-target signal and both rotations.
#
# VERSION HISTORY
# v1.1.0 · 2026-10-17 · fn 'command': page controllers run in the engine (engine/command.py).
# v1.0.0 · 2026-10-17 · Initial version: dispatch(request) for computeTradeOverlaySignals, pairOverlayTrades, computeSplitTargetSignal, computeLeaderRotation, computeMultiSplitRotation (assigned-rule path included).
"""Arguments follow the page: computeLeaderRotation(models, metricKey, upToIdx, replaySeries), computeMultiSplitRotation(models, keys, upToIdx, replaySeries).
A request is JSON: {"fn": <page function name>, "args": [...the page's arguments...], "globals": {...the page state that function reads...}, "rule": <assigned overlay rule or null>,
"tradeCache": [[key, {rows, cachedAt}], ...], "now": <Date.now()>, "maxFrames": <getMaxFrames()>, "replayIndex": <index into args[0] whose series is the replay series, or null>}.
The page sends the arguments it was called with and the globals the function reads (listed in GLOBALS below, found by scanning the function bodies); the answer is exactly what the
page function returned, minus the `curveModel` object handle on trades (the browser re-attaches it from the model id)."""
from __future__ import annotations

from . import core_ported as core

# globals each page function reads (page v2.65.32; tools/build_thin_page.py re-checks this list against the page on every build)
GLOBALS = {
    "computeTradeOverlaySignals": ["exitThreshold"],
    "pairOverlayTrades": [],
    "computeSplitTargetSignal": ["dailyTarget"],
    "computeLeaderRotation": ["activePortfolioName", "baselineFrameIndex", "dailyTarget", "exitThreshold", "overlayTopX", "currentDate", "currentFrameIndex",
                              "currentReturnType", "currentProduct", "currentProductType", "LIVE_DATE"],
    "computeMultiSplitRotation": ["activePortfolioName", "baselineFrameIndex", "dailyTarget", "exitThreshold", "overlayTopX", "currentDate", "currentFrameIndex",
                                  "currentReturnType", "currentProduct", "currentProductType", "LIVE_DATE"],
}


class RpcError(ValueError):
    pass


def _g(req: dict, name: str):
    g = req.get("globals") or {}
    if name not in g:
        raise RpcError(f"missing global {name!r} for {req.get('fn')}")
    return g[name]


def _num(v, default=0.0):
    return default if v is None else float(v)


def _rule_context(req: dict) -> core.RuleContext:
    cache = {k: v for k, v in (req.get("tradeCache") or [])}
    return core.RuleContext(trade_cache=cache, current_date=_g(req, "currentDate"), product_type=_g(req, "currentProductType"), product=_g(req, "currentProduct"),
                            live_date=_g(req, "LIVE_DATE"), now_ms=_num(req.get("now")), current_frame_index=int(_g(req, "currentFrameIndex")),
                            max_frames=req.get("maxFrames"), return_type=_g(req, "currentReturnType"), eligible_fallthrough=True)


def _common(req: dict, models: list, replay) -> dict:
    return dict(baseline_index=_g(req, "baselineFrameIndex"), exit_threshold=_num(_g(req, "exitThreshold")), daily_target=_num(_g(req, "dailyTarget")),
                replay_series=replay, hold_rank=int(_g(req, "overlayTopX")), overlay_rule=req.get("rule") if _g(req, "activePortfolioName") else None,
                rule_context=_rule_context(req))


def _replay(req: dict, models: list):
    idx = req.get("replayIndex")
    if idx is not None:
        return models[idx]["series"]
    return req["args"][3] if len(req["args"]) > 3 else None


def _strip(result: dict) -> dict:
    return {"signals": result["signals"], "trades": [{k: v for k, v in t.items() if k != "curveModel"} for t in result["trades"]],
            "threshold": result["threshold"], "targetSignal": result["targetSignal"]}


def dispatch(req: dict):
    fn, args = req.get("fn"), req.get("args") or []
    if fn == "command":   # a page controller run in the engine (engine/command.py)
        from . import command
        try:
            return command.run(req)
        except command.CommandError as e:
            raise RpcError(str(e)) from e
    if fn == "computeTradeOverlaySignals":
        return core.overlay_signals(args[0], args[1], _num(_g(req, "exitThreshold")))
    if fn == "pairOverlayTrades":
        return core.pair_overlay_trades(args[0], args[1], args[2])
    if fn == "computeSplitTargetSignal":
        return core.split_target_signal(args[0], args[1], args[2], _num(_g(req, "dailyTarget")))
    if fn == "computeLeaderRotation":
        models = args[0]
        return _strip(core.leader_rotation(models, args[1], args[2], **_common(req, models, _replay(req, models))))
    if fn == "computeMultiSplitRotation":
        models = args[0]
        return _strip(core.multi_split_rotation(models, args[1], args[2], **_common(req, models, _replay(req, models))))
    raise RpcError(f"unknown function {fn!r}")
