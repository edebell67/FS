# epics/ep_057_sql_to_pgsql/scenario_engine_v2/engine/data_client.py — headless data layer: the page's fetchers (live day, portfolio day, model search, deep links, catalogue, rules, source trades, historical curves) over an injectable transport.
#
# VERSION HISTORY
# v1.x · 2026-10-19 · load_model_search follows page v2.65.35 (strategy names via /api/strategy_catalog, first 100 matches).
# v1.5.0 · 2026-10-18 · `ops`: every write to the page-owned view caches (viewSet / viewTouch / viewDelete / persist / remember) is recorded in order so a browser copy can replay it on its own caches.
# v1.4.1 · 2026-10-17 · records the persistPortfolioView view call (browser copy replays it).
# v1.4.0 · 2026-10-17 · send(): PUT / POST through an injectable write transport (refused when none is set); HeadlessWriteRefused.
# v1.3.2 · 2026-10-17 · Pending.shared: a caller that joins an in-flight request resumes after the original awaiter.
# v1.3.1 · 2026-10-17 · One in-flight portfolio request per cache key (PORTFOLIO_VIEW_REQUESTS): a second caller shares it.
# v1.3.0 · 2026-10-17 · Pending.issued / seq (responses apply in issue order); fetch_guard / on_fetched / on_timeout hooks: a fetched portfolio is shown only if it is still the wanted one, and stale-cache revalidation is a timer.
# v1.2.1 · 2026-10-17 · on_effect hook (rememberPortfolioView writes an index to localStorage).
# v1.2.0 · 2026-10-17 · Pending (issue now, apply later) for live data, portfolio data and the rule library; the page's in-memory last-portfolio-view cache (remember / get); load_portfolio_data takes the portfolio name.
# v1.1.0 · 2026-10-17 · http_transport (urllib) for production use.
# v1.0.2 · 2026-10-17 · refresh_live_data returns tp_sl_ids (the page's TP / SL card order).
# v1.0.1 · 2026-10-17 · portfolio_models tracks the refreshed set after a background revalidation; overlay-rule assignments accept any non-null object (a list too), as the page does.
# v1.0.0 · 2026-10-17 · Initial version: DataClient mirroring refreshLiveData / fetchPortfolioData / loadPortfolioData / loadModelSearchFromDatabase / loadDeepLinkModelsFromDatabase / loadStrategyCatalogue / loadOverlayRuleLibrary / ensureAssignedOverlayTradeData / ensureHistoricalDataLoaded; URL builders for the hourly report and point-in-time endpoints.
"""No network code lives here: `transport(url) -> (http_status, parsed_json)` is supplied by the caller (urllib in production,
a fixture dict in tests). Browser-only concerns (localStorage caches, DOM updates, stale-response sequence guards,
duplicate in-flight request tracking) are intentionally absent; a headless run is sequential."""
from __future__ import annotations

import math
import re
import time
from collections import OrderedDict
from datetime import datetime
from typing import Any, Callable
from urllib.parse import quote, urljoin

from . import page_utils as pu

PORTFOLIO_VIEW_CACHE_MAX = 32
PORTFOLIO_VIEW_REFRESH_MS = 5 * 60 * 1000
DATE_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
MODEL_ID_RE = re.compile(r"[A-Za-z0-9._-]+")
LINKED_COLORS = ["#f59e0b", "#e879f9", "#34d399", "#fb7185", "#a78bfa", "#f97316", "#38bdf8", "#facc15", "#2dd4bf", "#c084fc"]

Transport = Callable[[str], "tuple[int, Any]"]


class HeadlessWriteRefused(Exception):
    """A write (POST / PUT) was attempted without a write transport: headless races never change shared server data by default."""


class FetchError(Exception):
    pass


_SEQ = __import__("itertools").count()


class Pending:
    """A request that has been issued but whose result the page applies later (JavaScript's `void fetch(...)` / un-awaited promise).
    finish() applies the result once and returns it. `issued` = a network request is in flight; `seq` orders issue times, because
    responses are applied in the order the requests were made."""

    def __init__(self, apply, issued=False):
        self._apply, self.done, self.result, self.issued, self.seq = apply, False, None, issued, next(_SEQ)
        self.failed = False  # a failed live-day request (see begin_refresh_live_data)
        self.shared = False  # True if this only waits on a request another caller already made
        self.root = None     # ...and that request (a joiner resumes once it is done, after its original awaiter)

    def finish(self):
        if not self.done:
            self.done, self.result = True, self._apply()
        return self.result


def resolved(value) -> "Pending":
    p = Pending(lambda: value)
    p.finish()
    return p


def encode_uri_component(value) -> str:
    """JS encodeURIComponent."""
    return quote(str(value), safe="-_.!~*'()")


def url_search_params(items) -> str:
    """JS URLSearchParams(...).toString(): application/x-www-form-urlencoded (space -> '+', only * - . _ and alphanumerics kept)."""
    pairs = items.items() if isinstance(items, dict) else items
    out = []
    for k, v in pairs:
        enc = lambda s: quote(str(s), safe="*").replace("~", "%7E").replace("%20", "+")  # noqa: E731
        out.append(f"{enc(k)}={enc(v)}")
    return "&".join(out)


def js_date_parse_ms(value) -> float:
    """Date.parse for the ISO strings the API returns: date-only is UTC, date-time without an offset is LOCAL time."""
    s = str(value or "")
    try:
        if re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", s):
            return datetime.fromisoformat(s + "T00:00:00+00:00").timestamp() * 1000
        return math.floor(datetime.fromisoformat(s).timestamp() * 1000)
    except ValueError:
        return float("nan")


def _is_ok(status) -> bool:
    return 200 <= int(status) < 300


def _message(payload, status):
    """payload.detail || payload.error || status  (how the page words HTTP failures)."""
    if isinstance(payload, dict):
        return payload.get("detail") or payload.get("error") or status
    return status


class DataClient:
    def __init__(self, transport: Transport, api_base: str = "", live_date: str = "", base_href: str = "",
                 now_ms: Callable[[], float] | None = None):
        self.transport = transport
        self.api = api_base.rstrip("/") if api_base else ""
        self.live_date = live_date
        self.base_href = base_href
        self.now_ms = now_ms or (lambda: time.time() * 1000)
        # state the page keeps in globals
        self.criteria_data: dict[str, dict[str, list]] = {}      # ALL_CRITERIA_DATA
        self.current_product = "all"
        self.live_badge: tuple[str, str] | None = None
        self.portfolio_view_cache: "OrderedDict[str, dict]" = OrderedDict()  # PORTFOLIO_VIEW_CACHE
        self.portfolio_models: list[dict] = []                       # portfolioModels: what the active portfolio currently shows
        self.strategy_catalogue: list[dict] = []
        self.strategy_catalogue_date: str | None = None
        self.strategy_catalogue_status = ""
        self.overlay_rule_library: dict = {"rules": [], "assignments": {}}
        self.trade_cache: dict[str, dict] = {}                     # assignedOverlayTradeCache
        self.historical_loads: set[str] = set()
        self.model_search_loaded: list[dict] = []
        self.model_search_status = ""
        self.pinned: "OrderedDict[str, dict]" = OrderedDict()      # pinnedComparisonModels
        self.deep_link_status = ""
        self.last_view: dict[str, dict] = {}                       # PORTFOLIO_LAST_VIEW_CACHE: "date|portfolio" -> {modelKey, entry}
        self.in_flight: dict[str, Pending] = {}                    # PORTFOLIO_VIEW_REQUESTS: one request per cache key at a time
        self.on_effect = lambda *a: None                           # Page sets this to record persistence calls
        self.on_timeout = None                                     # Page: schedule a callback (setTimeout) instead of running it inline
        self.fetch_guard = lambda name, date, key: True            # Page: is this fetch still wanted (same portfolio / date / members)?
        self.on_fetched = lambda background: None                  # Page: react to freshly fetched portfolio curves
        self.background: list[Pending] = []                        # fire-and-forget requests started by the last call
        self.ops: list = []                                        # ordered writes to the page-owned view caches, for a browser copy to replay
        self.write_transport = None                                # (method, url, body) -> (status, payload); None = writes refused

    # ---- helpers ----
    def _get(self, url: str):
        return self.transport(url)

    def send(self, method: str, url: str, body: dict):
        if self.write_transport is None:
            raise HeadlessWriteRefused(f"{method} {url}")
        return self.write_transport(method, url, body)

    # ---- refreshLiveData ----
    @staticmethod
    def live_scenario(criteria: str, return_type: str) -> str:
        if criteria == "top1_at_time":
            return "top_alt_net" if return_type == "ALT" else "top_net"
        if pu.is_metric_aware_criteria(criteria):
            return f"{criteria}_{'alt' if return_type == 'ALT' else 'net'}"
        return criteria

    def live_day_url(self, target_date, product_type, product, strategy_family, limit, criteria, return_type) -> str:
        scenario = self.live_scenario(criteria, return_type)
        metric = "alt" if return_type == "ALT" else "net"
        return (f"{self.api}/api/live_day?date={encode_uri_component(target_date)}&product_type={encode_uri_component(product_type)}"
                f"&product={encode_uri_component(product)}&strategy_family={encode_uri_component(strategy_family)}&limit={pu.js_str(limit)}"
                f"&scenario={encode_uri_component(scenario)}&display_metric={metric}")

    def begin_refresh_live_data(self, target_date, *, product_type="all", product="all", strategy_family="all", limit=10,
                                criteria="top_net", return_type="NET") -> Pending:
        """Issue the live-day request now; finish() files the scenario arrays under criteria_data."""
        if not self.live_date:
            return resolved({"ok": False, "reason": "no live date"})
        url = self.live_day_url(target_date, product_type, product, strategy_family, limit, criteria, return_type)
        try:
            resp, err = self._get(url), None
        except Exception as e:  # noqa: BLE001
            resp, err = None, e

        def apply():
            nonlocal product
            try:
                if err is not None:
                    raise err
                status, payload = resp
                if not _is_ok(status):
                    raise FetchError(_message(payload, status))
            except Exception:  # noqa: BLE001 - the page warns and shows an offline badge
                self.live_badge = ("Live: offline", "err")
                return {"ok": False, "url": url}
            products = payload.get("products") if isinstance(payload.get("products"), list) else []
            if product not in products:  # the page resets a product the server does not list (its dropdown is rebuilt from `products`)
                product = "all"
            self.current_product = product
            tp_sl_ids = self.sync_tp_sl_scenarios(payload.get("tp_sl_scenarios") if isinstance(payload.get("tp_sl_scenarios"), list) else [])
            for key, value in payload.items():
                if isinstance(value, list):
                    self.criteria_data.setdefault(key, {})[target_date] = value
            return {"ok": True, "url": url, "scenario": self.live_scenario(criteria, return_type), "products": products,
                    "product": product, "tp_sl_ids": tp_sl_ids}
        pend = Pending(apply, issued=True)
        pend.failed = err is not None or not _is_ok(resp[0])   # known as soon as the answer is in: a failed request changes nothing but the badge
        return pend

    def refresh_live_data(self, target_date, **kw) -> dict:
        """The data half of refreshLiveData: request the live-day payload and file every scenario array under criteria_data."""
        return self.begin_refresh_live_data(target_date, **kw).finish()

    def sync_tp_sl_scenarios(self, items: list) -> list[str]:
        """syncTpSlScenarios, data part only: make an empty NET and ALT bucket for every top3_tp<N>_sl<N> scenario the server lists.
        (Building the on-screen scenario cards stays in the page.) Returns the ids in the page's card order."""
        picked = [i for i in items if i and re.fullmatch(r"top3_tp[0-9]+_sl[0-9]+", str(i.get("id") or ""))]
        picked.sort(key=lambda i: (pu._number(i.get("tp")), pu._number(i.get("sl"))))
        ids = []
        for item in picked:
            sid = str(item["id"])
            ids.append(sid)
            self.criteria_data.setdefault(f"{sid}_net", {})
            self.criteria_data.setdefault(f"{sid}_alt", {})
        return ids

    # ---- fetchPortfolioData / loadPortfolioData ----
    def remember_portfolio_view(self, portfolio, date, model_key, entry) -> None:
        """rememberPortfolioView (in-memory part; the page also mirrors an index into localStorage)."""
        if not portfolio or not date or not entry:
            return
        self.last_view[f"{date}|{portfolio}"] = {"modelKey": model_key, "entry": entry}
        self.ops.append(["remember", portfolio, date, model_key, entry])
        self.on_effect("localStorage.setItem", "strategyDirectoryPortfolioLastViewV1")  # the page mirrors an index into localStorage

    def get_last_portfolio_view(self, portfolio, date):
        """getLastPortfolioView (in-memory part)."""
        remembered = self.last_view.get(f"{date}|{portfolio}")
        entry = (remembered or {}).get("entry")
        if isinstance(entry, dict) and entry.get("models") is not None:  # an empty list is truthy in JS
            return remembered
        return None

    def begin_fetch_portfolio_data(self, cache_key: str, date: str, model_key: str, background: bool = False,
                                   portfolio_name=None) -> Pending:
        existing = self.in_flight.get(cache_key)
        if existing is not None and not existing.done:
            sharer = Pending(existing.finish, issued=existing.issued)  # a second caller waits on the request already under way
            sharer.shared = True
            sharer.root = getattr(existing, "root", None) or existing  # the request this caller is waiting on
            return sharer
        ids = [m for m in model_key.split(",") if m]
        batches = [ids[i:i + 10] for i in range(0, len(ids), 10)]
        groups = [batches[g:g + 3] for g in range(0, len(batches), 3)]  # up to three requests in flight at a time
        holder: list = []

        def issue(group):
            out = []
            for batch in group:
                q = {"date": date, "models": ",".join(batch)}
                if background:
                    q["refresh"] = "1"
                out.append(self._get(f"{self.api}/api/portfolio_day?{url_search_params(q)}"))
            return out

        first = issue(groups[0]) if groups else None  # only the first group is requested up front

        def apply():
            post: list = []  # work to do once this request is no longer 'in flight' (JS: after the finally)
            try:
                entry = apply_inner(post)
            finally:
                if holder and self.in_flight.get(cache_key) is holder[0]:
                    del self.in_flight[cache_key]
            for fn in post:
                fn()
            return entry

        def apply_inner(post):
            payloads = []
            for gi, group in enumerate(groups):
                results = first if gi == 0 else issue(group)
                for status, payload in results:  # Promise.all: every request is issued, the first failure wins
                    if not _is_ok(status):
                        raise FetchError(_message(payload, status))
                payloads.extend(p for _, p in results)
            models = [m for p in payloads for m in (p.get("models") or [])]
            stamps = [t for t in (js_date_parse_ms(p.get("generated_at")) for p in payloads) if t == t and abs(t) != float("inf")]
            entry = {"models": models, "cachedAt": max(stamps) if stamps else self.now_ms()}
            self.portfolio_view_cache[cache_key] = entry
            self.ops.append(["viewSet", cache_key, entry])
            self.ops.append(["persist", cache_key, entry])
            self.on_effect("view", "persistPortfolioView")  # persistPortfolioView(cacheKey, entry)
            self.remember_portfolio_view(portfolio_name, date, model_key, entry)
            while len(self.portfolio_view_cache) > PORTFOLIO_VIEW_CACHE_MAX:
                self.ops.append(["viewDelete", next(iter(self.portfolio_view_cache))])
                self.portfolio_view_cache.popitem(last=False)
            # a response for a portfolio / date the user has since left is cached but not shown
            if self.fetch_guard(portfolio_name, date, model_key):
                self.portfolio_models = models
                self.on_fetched(background)
                if not background and date == self.live_date and self.now_ms() - entry["cachedAt"] >= PORTFOLIO_VIEW_REFRESH_MS:
                    def revalidate():  # the server may have served its own cached response: revalidate without delaying the first paint
                        if not self.fetch_guard(portfolio_name, date, model_key):
                            return
                        try:
                            self.begin_fetch_portfolio_data(cache_key, date, model_key, True, portfolio_name).finish()
                        except Exception:  # noqa: BLE001 - background refresh failures are only warned about
                            pass
                    if self.on_timeout:
                        self.on_timeout(revalidate, 0)
                    else:
                        post.append(revalidate)
            return entry
        pend = Pending(apply, issued=bool(groups))
        holder.append(pend)
        self.in_flight[cache_key] = pend
        return pend

    def fetch_portfolio_data(self, cache_key: str, date: str, model_key: str, background: bool = False, portfolio_name=None) -> dict:
        return self.begin_fetch_portfolio_data(cache_key, date, model_key, background, portfolio_name).finish()

    def begin_load_portfolio_data(self, models: list[str], date: str, prefer_cache: bool = True, portfolio_name=None) -> Pending:
        """loadPortfolioData up to its first await: cache check and 'paint what we have'; finish() returns {"models","fetched"}
        once any needed fetch has been applied. A stale live cache hit starts a background refresh (self.background)."""
        if not models or not DATE_RE.fullmatch(date or ""):
            self.portfolio_models = []
            return resolved({"models": [], "fetched": False})
        model_key = ",".join(models)
        cache_key = f"{date}|{model_key}"
        cached = self.portfolio_view_cache.get(cache_key)
        if prefer_cache and cached:
            self.portfolio_models = cached["models"]  # paint the cached curves at once
            self.remember_portfolio_view(portfolio_name, date, model_key, cached)
            self.portfolio_view_cache.pop(cache_key)
            self.portfolio_view_cache[cache_key] = cached
            self.ops.append(["viewTouch", cache_key, cached])
            if date == self.live_date and self.now_ms() - cached["cachedAt"] >= PORTFOLIO_VIEW_REFRESH_MS:
                self.background.append(self.begin_fetch_portfolio_data(cache_key, date, model_key, True, portfolio_name))
            return resolved({"models": self.portfolio_models, "fetched": False})
        last = self.get_last_portfolio_view(portfolio_name, date) if prefer_cache else None
        self.portfolio_models = last["entry"]["models"] if last else []  # keep this portfolio's most recent curves visible meanwhile
        fetch = self.begin_fetch_portfolio_data(cache_key, date, model_key, False, portfolio_name)

        def apply():
            fetch.finish()
            return {"models": self.portfolio_models, "fetched": True}
        pend = Pending(apply, issued=fetch.issued)
        pend.shared, pend.root = fetch.shared, fetch.root
        return pend

    def load_portfolio_data(self, models: list[str], date: str, prefer_cache: bool = True, portfolio_name=None) -> dict:
        """loadPortfolioData: models of one portfolio on one date, from the cache when allowed."""
        r = self.begin_load_portfolio_data(models, date, prefer_cache, portfolio_name).finish()
        for bg in self.background:  # a stale cache hit's background refresh: failures are only warned about
            try:
                bg.finish()
            except Exception:  # noqa: BLE001
                pass
        self.background = []
        return {"models": self.portfolio_models, "fetched": r["fetched"]}  # what the portfolio shows once any background refresh landed

    # ---- loadModelSearchFromDatabase ----
    def load_model_search(self, search_term, date: str) -> dict:
        terms = pu.model_search_terms(search_term)
        query = re.sub(r"\s+", "_", str(search_term or "").strip().lower())   # page v2.65.35: spaces count as '_'
        is_list = len(terms) > 1 and all(re.fullmatch(r"(?:dna_)?\d+", m, re.I) for m in terms)
        is_direct = is_list or (len(terms) == 1 and re.fullmatch(r"(?:dna_)?\d{5,}", terms[0], re.I) is not None)
        requested = terms if is_direct else [query]
        if not search_term or len(search_term) > 100 or (is_list and any(not MODEL_ID_RE.fullmatch(m) for m in requested)):
            self.model_search_status = "Search by one strategy name, or enter model IDs separated by commas or spaces"
            return {"loaded": [], "missing": []}
        if not DATE_RE.fullmatch(date or ""):
            self.model_search_status = "Choose a single date to search PostgreSQL"
            return {"loaded": [], "missing": []}
        n = len(requested)
        self.model_search_status = "Searching model IDs and strategy names in PostgreSQL\u2026" if n == 1 else f"Searching {n} model IDs in PostgreSQL\u2026"
        try:
            model_ids, truncated = requested, False
            if not is_direct:   # a strategy name: the catalogue says which models match (first 100)
                status, payload = self._get(f"{self.api}/api/strategy_catalog?{url_search_params({'date': date})}")
                if not _is_ok(status):
                    raise FetchError(_message(payload, f"HTTP {status}"))
                models = (payload.get("models") if isinstance(payload, dict) else None) or []
                matches = [m for m in models if query in str(m.get("model") or "").lower() or query in str(m.get("strategy") or "").lower()]
                if not matches:
                    self.model_search_loaded = []
                    self.model_search_status = f"No model ID or strategy name matches \u201c{search_term}\u201d for {date}"
                    return {"loaded": [], "missing": []}
                truncated = len(matches) > 100
                model_ids = [str(m.get("model")) for m in matches[:100]]
            batches = [model_ids[i:i + 10] for i in range(0, len(model_ids), 10)]
            results = [self._get(f"{self.api}/api/portfolio_day?{url_search_params({'models': ','.join(b), 'date': date})}") for b in batches]
            responses = []
            for status, payload in results:
                if not _is_ok(status):
                    raise FetchError(_message(payload, f"HTTP {status}"))
                responses.append(payload.get("models") if isinstance(payload.get("models"), list) else [])
        except Exception as error:  # noqa: BLE001
            self.model_search_status = f"Database search failed: {error}"
            return {"loaded": [], "missing": []}
        by_id = {str(m.get("model") or "").lower(): m for r in responses for m in r}
        self.model_search_loaded = [by_id[m.lower()] for m in model_ids if m.lower() in by_id]
        missing = [m for m in model_ids if m.lower() not in by_id]
        if not self.model_search_loaded:
            self.model_search_status = f"No model data found for {date}{': ' + ', '.join(missing) if missing else ''}"
            return {"loaded": [], "missing": missing}
        c = len(self.model_search_loaded)
        if is_direct:
            self.model_search_status = f"{c} model{'' if c == 1 else 's'} loaded{' \u00b7 not found: ' + ', '.join(missing) if missing else ''}"
        else:
            self.model_search_status = f"{c} model{'' if c == 1 else 's'} match \u201c{search_term}\u201d{' \u00b7 showing first 100 matches' if truncated else ''}"
        return {"loaded": self.model_search_loaded, "missing": missing}

    # ---- loadDeepLinkModelsFromDatabase ----
    def load_deep_link_models(self, model_ids, date: str, models_only: bool = False) -> dict:
        ids = []
        for raw in model_ids or []:
            i = str(raw).strip()
            if MODEL_ID_RE.fullmatch(i) and i not in ids:
                ids.append(i)
        ids = ids[:10]
        if not ids:
            return {"loaded": [], "missing": []}
        if not DATE_RE.fullmatch(date or ""):
            self.deep_link_status = "Choose a single date to load linked comparison models"
            return {"loaded": [], "missing": []}
        n = len(ids)
        self.deep_link_status = f"Loading {n} linked comparison strateg{'y' if n == 1 else 'ies'}…"
        try:
            status, payload = self._get(f"{self.api}/api/portfolio_day?{url_search_params({'models': ','.join(ids), 'date': date})}")
            if not _is_ok(status):
                raise FetchError(_message(payload, f"HTTP {status}"))
        except Exception as error:  # noqa: BLE001
            self.deep_link_status = f"Could not load linked models: {error}"
            return {"loaded": [], "missing": ids}
        loaded = payload.get("models") if isinstance(payload.get("models"), list) else []
        for index, model in enumerate(loaded):
            mid = str(model.get("model") or "")
            if not mid:
                continue
            self.pinned[mid] = {**model, "color": model.get("color") or LINKED_COLORS[index % len(LINKED_COLORS)],
                                "comparisonRole": "pinned comparison"}
        loaded_ids = {str(m.get("model")) for m in loaded}
        missing = [i for i in ids if i not in loaded_ids]
        c = len(loaded)
        word = f"strateg{'y' if c == 1 else 'ies'}"
        miss = f" · no data found for {', '.join(missing)}" if missing else ""
        self.deep_link_status = (f"Showing {c} selected {word} only{miss} · choose a scenario to add scenario leaders" if models_only
                                 else f"{c} linked comparison {word} added{miss} · change scenario to compare")
        return {"loaded": loaded, "missing": missing}

    # ---- loadStrategyCatalogue ----
    def load_strategy_catalogue(self, date: str) -> list[dict]:
        if self.strategy_catalogue_date == date and self.strategy_catalogue:
            return self.strategy_catalogue
        try:
            status, payload = self._get(f"{self.api}/api/strategy_catalog?date={encode_uri_component(date)}")
            if not _is_ok(status):
                raise FetchError(_message(payload, status))
            self.strategy_catalogue = payload.get("models") or []
            self.strategy_catalogue_date = date
            self.strategy_catalogue_status = ""
        except Exception as error:  # noqa: BLE001
            self.strategy_catalogue_status = f"Catalogue unavailable: {error}"
        return self.strategy_catalogue

    # ---- loadOverlayRuleLibrary ----
    def begin_load_overlay_rule_library(self) -> Pending:
        try:
            resp, err = self._get(f"{self.api}/api/overlay_rules"), None
        except Exception as e:  # noqa: BLE001
            resp, err = None, e

        def apply():
            try:
                if err is not None:
                    raise err
                status, payload = resp
                if not _is_ok(status):
                    raise FetchError(f"HTTP {status}")
                self.overlay_rule_library = {
                    "rules": payload["rules"] if isinstance(payload.get("rules"), list) else [],
                    "assignments": payload["assignments"] if isinstance(payload.get("assignments"), (dict, list)) else {}}
            except Exception:  # noqa: BLE001 - the page keeps the previous library and warns
                pass
            return self.overlay_rule_library
        return Pending(apply, issued=True)

    def load_overlay_rule_library(self) -> dict:
        return self.begin_load_overlay_rule_library().finish()

    # ---- ensureAssignedOverlayTradeData ----
    def ensure_trade_data(self, models: list[str], date: str, product_type: str, product: str) -> None:
        """Fill trade_cache for each model (key date|product_type|product|model); stale only on the live date."""
        if not DATE_RE.fullmatch(date or ""):
            return
        for model in models:
            key = "|".join([date, product_type, product, model])
            cached = self.trade_cache.get(key)
            if cached and (date != self.live_date or self.now_ms() - cached["cachedAt"] < PORTFOLIO_VIEW_REFRESH_MS):
                continue
            url = (f"{self.api}/api/model_trades?model={encode_uri_component(model)}&from={date}&to={date}"
                   f"&product_type={encode_uri_component(product_type)}&product={encode_uri_component(product)}")
            try:
                status, payload = self._get(url)
                if not _is_ok(status):
                    raise FetchError(_message(payload, status))
                self.trade_cache[key] = {"rows": payload.get("trades") or [], "cachedAt": self.now_ms()}
            except Exception:  # noqa: BLE001 - the page caches an empty list and warns
                self.trade_cache[key] = {"rows": [], "cachedAt": self.now_ms()}

    # ---- ensureHistoricalDataLoaded ----
    def ensure_historical_data(self, date_key: str) -> None:
        if date_key == self.live_date or any(isinstance(b.get(date_key), list) and b[date_key] for b in self.criteria_data.values()):
            return
        if not DATE_RE.fullmatch(date_key or "") and date_key != "WEEK_OVERALL":
            return
        if date_key in self.historical_loads:
            return
        url = urljoin(self.base_href, f"historical_curve_data/{encode_uri_component(date_key)}.json")
        status, daily = self._get(url)
        if not _is_ok(status):
            raise FetchError(f"Historical chart data unavailable ({status})")
        for scenario, models in daily.items():
            self.criteria_data.setdefault(scenario, {})[date_key] = models
        self.historical_loads.add(date_key)

    # ---- URL builders for the endpoints whose handlers are mostly UI ----
    def hourly_report_url(self, date, product_type, product, family, interval_minutes) -> str:
        q = url_search_params({"date": date, "product_type": product_type, "product": product, "family": family,
                               "interval_minutes": pu.js_str(interval_minutes)})
        return f"{self.api}/api/hourly_family_report?{q}"

    def point_in_time_url(self, date, at, options: dict, auto_direction=None, auto_rank=None) -> str:
        """The point_in_time_scenario request refreshPointInTimeSelection sends (options = page_utils.point_in_time_request_options)."""
        q = {"date": date, "at": at, "scenario": options["scenario"], "return_type": options["return_type"],
             "product_type": options["product_type"], "product": options["product"], "strategy_family": options["strategy_family"],
             "limit": pu.js_str(options["limit"]), "min_win_rate": pu.js_str(options["min_win_rate"]),
             "rank_direction": auto_direction if auto_direction else "top"}
        if auto_direction:
            q["rank_position"] = pu.js_str(auto_rank)
        return f"{self.api}/api/point_in_time_scenario?{url_search_params(q)}"

    def point_in_time_hours_url(self, date, options: dict) -> str:
        q = {"date": date, **{k: pu.js_str(v) for k, v in options.items()}}
        return f"{self.api}/api/point_in_time_scenario_hours?{url_search_params(q)}"


def http_transport(timeout: float = 60.0) -> Transport:
    """A transport over urllib for production use: returns (status, parsed JSON); HTTP errors still return their JSON body."""
    import json
    import urllib.error
    import urllib.request

    def get(url: str):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as err:
            try:
                return err.code, json.loads(err.read().decode("utf-8"))
            except ValueError:
                return err.code, {}
    return get
