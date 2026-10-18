# epics/ep_057_sql_to_pgsql/scenario_engine_v2/engine/command.py — run a page controller in the engine on a state snapshot sent by the browser copy; returns the new state and the ordered effects.
#
# VERSION HISTORY
# v1.5.0 · 2026-10-18 · spawn_mode: un-awaited lookups come back as `spawns` for the page to run; no controller answers needsNetwork for a lookup any more.
# v1.4.0 · 2026-10-18 · answers carry viewArgs; requests may carry `flags` (page facts) and a stage given by name.
# v1.3.0 · 2026-10-18 · staged controllers (page.STAGES): {"stage": N, "ctx", "result"} resumes a controller after the page awaited a page async function; the answer carries {"await": {fn, args}, "ctx", "stage"} while one is outstanding.
# v1.2.0 · 2026-10-17 · a controller that wants the network answers {needsNetwork: true} (the page then runs its own copy); timers: named timer operations tied to effect indexes.
# v1.1.0 · 2026-10-17 · stage 2 (no fetch): apply_chart_lock, reset_automatic_rank_schedule.
# v1.0.1 · 2026-10-17 · optional `hooks` test seam.
# v1.0.0 · 2026-10-17 · Initial version: stage 1 controllers that need no network (movePortfolio, markPortfolioFixed, capturePortfolioScenario, persistPortfolioViewConfig, startReplay, pauseReplay, syncPortfolioViewRefresh, updateAutoRefreshTop1Status).
"""A command request: {"method": <Page method>, "args": [...], "state": <PageState.snapshot() of the page>, "criteriaData": {key: {date: [models]}} (only what the page's current view reads),
"library": <overlay rule library>, "scenarioNames": {id: name}}. The answer: {"ret", "state", "effects"} where effects are the ordered persistence / timer / view calls the page must make
(['view', name], ['savePortfolios'], ['localStorage.setItem', key], ['setInterval', ms], ...). The page is the authority for its own state: it sends the whole snapshot each time and applies the answer."""
from __future__ import annotations

from .data_client import DataClient
from .page import STAGES, LivePortfolioRefused, Page
from .page_state import PageState

# controllers the browser copy may delegate (stage 1: none of them touches the network or starts a timer callback the engine would have to own)
STAGE1 = ("move_portfolio", "mark_portfolio_fixed", "capture_portfolio_scenario", "persist_portfolio_view_config", "start_replay", "pause_replay",
          "sync_portfolio_view_refresh", "update_auto_refresh_status",
          "apply_chart_lock", "reset_automatic_rank_schedule",
          "unique_portfolio_name", "current_portfolio_view_config", "apply_portfolio_view_config", "get_merged_portfolio_models", "auto_pin_live_portfolio_strategies",
          "schedule_point_in_time_selection", "schedule_automatic_top1_refresh", "apply_selected_time", "trigger_selected_time_refresh",   # last two: stage 2, no fetch
          *STAGES)   # staged: the page awaits a page async function between the stages


class CommandError(ValueError):
    pass


class NeedsNetwork(Exception):
    """The controller wants to fetch data; the engine session does not own the data layer yet, so the page runs its own copy for this call."""


def _no_network_for(wanted: list):
    def transport(url):   # the page's own try/catch blocks swallow errors, so remember that the network was wanted
        wanted.append(url)
        raise NeedsNetwork(url)
    return transport


_CRITERIA_CACHE: dict = {}   # criteriaHash -> criteriaData (the engine never mutates it)


def run(req: dict) -> dict:
    method = req.get("method")
    if method not in STAGE1:
        raise CommandError(f"controller {method!r} is not delegated to the engine yet")
    state = PageState.from_snapshot(req["state"])
    wanted: list = []
    client = DataClient(_no_network_for(wanted), "", live_date=state.live_date)
    criteria = req.get("criteriaData")
    chash = req.get("criteriaHash")
    if chash is not None:   # the page sends the (large) scenario data once per content hash, then only the hash
        if criteria is None:
            criteria = _CRITERIA_CACHE.get(chash)
            if criteria is None:
                return {"needCriteria": True}
        else:
            _CRITERIA_CACHE[chash] = criteria
            while len(_CRITERIA_CACHE) > 4:
                _CRITERIA_CACHE.pop(next(iter(_CRITERIA_CACHE)))
    client.criteria_data = {k: dict(v) for k, v in (criteria or {}).items()}   # outer two levels copied: the client files results into them
    client.overlay_rule_library = req.get("library") or {"rules": [], "assignments": {}}
    hooks = req.get("hooks")   # test seam only (the differential tests pin the replay head / frame count); the page never sends it
    extra = {}
    if hooks:
        extra = dict(max_frames=lambda: hooks["maxFrames"], head_time=lambda: hooks["head"], eligible=lambda: hooks["eligible"], candidates=lambda: hooks["candidates"])
    page = Page(state, client, scenario_names=req.get("scenarioNames") or {}, flags=req.get("flags"), **extra)
    page.spawn_mode = True
    pending_await, calls = None, []
    try:
        if method in STAGES:   # one stage: the page performs the awaited function and calls again with {stage, ctx, result}
            stage = req.get("stage") or 0
            stage = stage if isinstance(stage, str) else int(stage)
            ret, pending_await, calls = page.run_stage(method, stage, req.get("args"), req.get("ctx"), req.get("result"))
        else:
            ret = getattr(page, method)(*(req.get("args") or []))
            page.settle()
    except NeedsNetwork:
        wanted.append("raised")
    except LivePortfolioRefused:   # the engine does not run live portfolios (orders): the page runs its own copy
        wanted.append("live")
    if wanted:
        return {"needsNetwork": True}
    if pending_await is not None:
        nxt = pending_await.next if pending_await.next else int(req.get("stage") or 0) + 1
        return {"await": {"fn": pending_await.fn, "args": pending_await.args, "catch": pending_await.catch, "fire": pending_await.fire, "sync": pending_await.sync, "handle": pending_await.handle, "attach": pending_await.attach}, "ctx": pending_await.ctx, "stage": nxt,
                "state": state.snapshot(), "effects": state.effects, "timers": state.timer_ops, "calls": calls, "viewArgs": state.view_args, "spawns": page._spawns}
    out = {"ret": ret, "state": state.snapshot(), "effects": state.effects, "timers": state.timer_ops, "viewArgs": state.view_args, "spawns": page._spawns}
    if method in STAGES:
        out["calls"] = calls
    return out
