# epics/ep_057_sql_to_pgsql/scenario_engine_v2/engine/twophase.py — begin / finish commands for page controllers that fetch (the browser copy does the fetching).
#
# VERSION HISTORY
# v1.0.0 · 2026-10-18 · Initial version: refresh_live_data (one live-day request, then the optional portfolio load as extra rounds).
"""Why two phases: the original awaits a fetch in the middle of the controller and its stale-response guards compare the page's state before and after the await,
so one synchronous call would remove the await and block the page. Protocol:

  begin : {"method": "refresh_live_data", "phase": "begin", "args": [...], "state": snapshot, ...}
          -> {"requests": [url], "ctx": {...}, "state": new snapshot (sequence bumped), "effects": [...]}
  finish: {"method": ..., "phase": "finish", "ctx": ctx, "responses": {url: [status, payload] | {"error": "..."}}, "state": CURRENT snapshot, ...}
          -> {"need": [urls]}                       (the controller wants more data: fetch and call finish again with the larger `responses`; nothing was applied)
          or {"done": true, "ret", "state", "effects"}

Finish re-runs from the state it is given each round (nothing is applied until it completes), so a round that needs more data is simply repeated."""
from __future__ import annotations

from .data_client import DataClient, Pending
from .page import Page
from .page_state import PageState


class NeedFetch(BaseException):
    """Raised by the finish transport for a URL the page has not fetched yet (BaseException: the data client turns ordinary exceptions into 'offline')."""

    def __init__(self, url):
        super().__init__(url)
        self.url = url


class _Begin:
    def __init__(self):
        self.urls = []

    def __call__(self, url):
        self.urls.append(url)
        return 200, {}   # placeholder: begin never applies the answer


class _Replay:
    def __init__(self, responses):
        self.responses = responses
        self.missing = []

    def __call__(self, url):
        if url not in self.responses:
            raise NeedFetch(url)
        r = self.responses[url]
        if isinstance(r, dict) and "error" in r:
            raise ConnectionError(str(r["error"]))
        return r[0], r[1]


def _page(req, transport):
    state = PageState.from_snapshot(req["state"])
    client = DataClient(transport, req.get("api", ""), live_date=state.live_date)
    client.criteria_data = req.get("criteriaData") or {}
    client.overlay_rule_library = req.get("library") or {"rules": [], "assignments": {}}
    hooks = req.get("hooks")   # test seam, as in command.py
    extra = {}
    if hooks:
        extra = dict(max_frames=lambda: hooks["maxFrames"], head_time=lambda: hooks["head"], eligible=lambda: hooks["eligible"], candidates=lambda: hooks["candidates"])
    return state, client, Page(state, client, scenario_names=req.get("scenarioNames") or {}, **extra)


def run(req: dict) -> dict:
    method, phase = req.get("method"), req.get("phase")
    if method != "refresh_live_data":
        raise ValueError(f"{method!r} has no two-phase form yet")
    args = req.get("args") or []
    if phase == "begin":
        rec = _Begin()
        state, client, page = _page(req, rec)
        s = state
        page.begin_refresh_live_data(*args)     # issues the request (the placeholder answer is never applied)
        ctx = {"seq": s.live_refresh_sequence, "req": [s.product_type, s.product, s.strategy_family, s.model_limit, s.return_type, s.current_criteria],
               "target_date": args[0] if args and args[0] is not None else s.live_date, "skip": bool(args[1]) if len(args) > 1 else False}
        return {"requests": rec.urls, "ctx": ctx, "state": state.snapshot(), "effects": state.effects}
    if phase == "finish":
        ctx = req["ctx"]
        replay = _Replay(req.get("responses") or {})
        state, client, page = _page(req, replay)
        product_type, product, family, limit, return_type, criteria = ctx["req"]
        try:
            pending = client.begin_refresh_live_data(ctx["target_date"], product_type=product_type, product=product, strategy_family=family, limit=limit,
                                                     criteria=criteria, return_type=return_type)
            ret = page._await(Pending(lambda: page._apply_live(ctx, pending), issued=pending.issued))
            page.settle()
        except NeedFetch as need:
            return {"need": [need.url]}
        return {"done": True, "ret": ret, "state": state.snapshot(), "effects": state.effects}
    raise ValueError(f"unknown phase {phase!r}")
