# epics/ep_055_strategy_directory_chart/app/backdrop_server.py
# Read-only aggregation API for the EP055 Strategy Landscape historical backdrop.
#
# VERSION HISTORY
# v2.3.0 · 2026-09-15 · Add /api/intraday_series for the time-playback scrubber:
#   per-strategy cumulative net_return/alt_net_return at real trade-close resolution
#   (COALESCE(g_close_time, last_update, created), same convention api_server_sql
#   already uses), not the day-granularity snapshot series /api/breakout_backdrop
#   returns.
# v2.2.2 · 2026-09-12 · Exclude unrecognised model IDs; Non-DNA is exactly six digits starting with 1.
# v2.2.1 · 2026-09-12 · Filter trade signal before backdrop aggregation and isolate direction caches.
# v2.2.0 · 2026-09-09 · [V20260909_1555] Serves strategy_landscape_live.html and static UI
#   directly on port 8065 via Uvicorn, unifying the backend backdrop API and the frontend.
# v2.1.0 · 2026-09-08 · REVERTED v2.0.0's regrouping - that was a misreading of the
#   request. The user asked for a FILTER to show DNA or Non-DNA strategies within the
#   existing breakout-family landscape, not for DNA/Non-DNA to replace the breakout
#   families as the primary grouping/layout. Back to strategy_name LIKE 'breakout%'
#   scoping the whole dataset, family_of() grouping by breakout_*/breakout_r_*/etc, and
#   no product_forex join. The "group" field is DNA/Non-DNA is still returned (from the
#   model prefix) so the frontend can offer a same-landscape filter, but it plays no
#   part in positioning/grouping.
# v2.0.0 · 2026-09-07 · Regrouping requirement changed: the landscape's primary grouping
#   is now DNA vs Non-DNA (by the model column's "DNA_" prefix - the same convention
#   api_server_sql already uses in trade_summary_live's "model NOT LIKE 'DNA_%'"), not
#   the breakout_*/strategy_name families. Real DNA-model rows turned out to mostly
#   carry non-breakout strategy_names (TIME-/BRK-/BUCKET-/EVENT- schemes), so filtering
#   to strategy_name LIKE 'breakout%' would have made "Non-DNA" come back empty and
#   wasn't the right scope anyway once DNA/Non-DNA became the grouping itself. The
#   strategy_name filter is dropped entirely - every closed/open strategy in the
#   trailing window is now included, grouped by model prefix instead.
# v1.3.0 · 2026-09-07 · Narrows the GROUP BY key to model+date (strategy_name/product
#   recovered via MIN() since they're constant per model) and bounds the scan to the
#   trailing 90 days, both to shrink the query's memory grant - the SQL Server instance
#   was observed under RESOURCE_SEMAPHORE memory pressure alongside unrelated production
#   queries, so reducing this query's footprint helps regardless of the root cause.
# v1.2.0 · 2026-09-07 · Caches the aggregate in memory (TTL below) and serves stale data
#   immediately while refreshing in the background. The underlying query's cost varies
#   wildly on this DB (observed 4s to 135s for the same query - likely contention with
#   the live trading writers) so blocking every page load on a live query is unusable;
#   only the first request per process ever blocks.
# v1.1.0 · 2026-09-07 · Aggregates alt_net_return alongside net_return so the landscape
#   can switch return basis without a second round trip.
# v1.0.0 · 2026-09-07 · Initial version. Aggregates dbo.combined_trades_closed (historical)
#   and dbo.combined_trades_open (current unrealized) for the four breakout strategy
#   families, scoped by strategy_name prefix. Runs as its own read-only process on a
#   separate port so the landscape never touches the live trading API server
#   (api_server_sql, port 8001) - no risk to execute_trade/ or any write path there.
#
# Real data only: every strategy, family and net_return value returned here comes
# directly from SQL Server. Nothing in this file fabricates or simulates data.

import os
import re
import logging
import threading
import time
from collections import defaultdict
from datetime import date

import pyodbc
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# [V20260909_1555] 2026-09-09: Unify static HTML and backdrop API under uvicorn port 8065
APP_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(APP_DIR, "strategy_landscape_live.html")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

SERVER = os.getenv("DB_SERVER", "tcp:EDS,1433")
USERNAME = os.getenv("DB_USER", "sqlaccessfromapi")
PASSWORD = os.getenv("DB_PASS", "apiaccess@4321")


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return FileResponse(HTML_FILE)

@app.get("/strategy_landscape_live.html")
def landscape_page():
    return FileResponse(HTML_FILE)


def connect_to_db(database_name: str = "tradedb"):
    try:
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={SERVER};DATABASE={database_name};"
            f"UID={USERNAME};PWD={PASSWORD}"
        )
        return pyodbc.connect(conn_str, timeout=10)
    except Exception as e:
        logger.error("Database connection error: %s", e)
        return None


def is_dna(model: str) -> bool:
    return bool(re.fullmatch(r"DNA_[12][0-9]+", model or "", re.IGNORECASE))


def is_nondna(model: str) -> bool:
    return bool(re.fullmatch(r"1[0-9]{5}", model or ""))


# Longest-prefix-first so "breakout_r_rev" is never mis-matched as "breakout_r".
FAMILY_PREFIXES = ["breakout_r_rev", "breakout_rev", "breakout_r", "breakout"]


def family_of(strategy_name: str | None) -> str | None:
    name = (strategy_name or "").lower()
    for prefix in FAMILY_PREFIXES:
        if name.startswith(prefix):
            return prefix
    return None


@app.get("/healthz")
def health():
    return {"status": "ok"}


# Non-DNA open trades mostly have strategy_name = NULL (confirmed: 38 of 43 open
# non-DNA trades right now), so they can never match the breakout%/tp-sl regex the
# way DNA strategy_names do. This gives them an equivalent label sourced the same
# real way DNA's is - just from product_forex's target_profit/target_loss instead of
# a name string - as "tp{target_profit}_sl{target_loss}", with no "breakout_N_"
# prefix since there is no DNA-style variant number for these. Small, mostly-static
# table (bounded to non-DNA rows) so a long TTL is fine.
_TPSL_CACHE_TTL_SECONDS = 3600
_tpsl_cache_lock = threading.Lock()
_tpsl_cache: dict[str, dict] = {}  # db -> {"payload": {...}, "fetched_at": float}


@app.get("/api/nondna_tpsl_lookup")
def nondna_tpsl_lookup(db: str = Query("tradedb")):
    with _tpsl_cache_lock:
        entry = _tpsl_cache.get(db)
    if entry is not None and time.time() - entry["fetched_at"] < _TPSL_CACHE_TTL_SECONDS:
        return entry["payload"]

    conn = connect_to_db(db)
    if not conn:
        if entry is not None:
            return entry["payload"]  # serve stale rather than fail outright
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT model, product, target_profit, target_loss
            FROM dbo.product_forex WITH (NOLOCK)
            WHERE model LIKE '1[0-9][0-9][0-9][0-9][0-9]' AND LEN(model) = 6 AND target_profit IS NOT NULL AND target_loss IS NOT NULL
            """
        )
        rows = cur.fetchall()
    except Exception as e:
        conn.close()
        if entry is not None:
            return entry["payload"]
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")
    conn.close()

    lookup = {f"{model}:{(product or '').upper()}": {"tp": tp, "sl": sl} for model, product, tp, sl in rows}
    payload = {"lookup": lookup, "total": len(lookup)}
    with _tpsl_cache_lock:
        _tpsl_cache[db] = {"payload": payload, "fetched_at": time.time()}
    return payload


# [V20260908_1710] Dedicated fast endpoints for live open trades (DNA + Non-DNA)
# Uses OPTION (MAXDOP 1) and a short TTL cache with background refresh so requests never hang.
_NONDNA_OPEN_TTL_SECONDS = 3
_nondna_open_cache_lock = threading.Lock()
_nondna_open_cache: dict[str, dict] = {}  # db -> {"payload": {...}, "fetched_at": float}
_nondna_open_refresh_in_progress: set[str] = set()

_LIVE_OPEN_TTL_SECONDS = 3
_live_open_cache_lock = threading.Lock()
_live_open_cache: dict[str, dict] = {}  # db -> {"payload": {...}, "fetched_at": float}
_live_open_refresh_in_progress: set[str] = set()


def _fetch_live_open_trades(db: str) -> list[dict]:
    conn = connect_to_db(db)
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT guid, model, product, strategy_name, signal, net_return, alt_net_return,
                   entry_price, latest_price, created
            FROM dbo.combined_trades_open WITH (NOLOCK)
            WHERE net_return IS NOT NULL
              AND (model LIKE 'DNA[_]1%' OR model LIKE 'DNA[_]2%' OR
                   (model LIKE '1[0-9][0-9][0-9][0-9][0-9]' AND LEN(model) = 6))
            OPTION (MAXDOP 1)
            """
        )
        cols = [c[0] for c in cur.description]
        trades = []
        for row in cur.fetchall():
            d = dict(zip(cols, row))
            for k, v in d.items():
                if hasattr(v, "isoformat"):
                    d[k] = v.isoformat()
                elif hasattr(v, "__float__"):
                    d[k] = float(v)
            trades.append(d)
        return trades
    except Exception as e:
        logger.error("Failed to query live open trades for db=%s: %s", db, e)
        return []
    finally:
        conn.close()


def _kick_off_live_open_refresh(db: str):
    with _live_open_cache_lock:
        if db in _live_open_refresh_in_progress:
            return
        _live_open_refresh_in_progress.add(db)

    def worker():
        try:
            trades = _fetch_live_open_trades(db)
            with _live_open_cache_lock:
                _live_open_cache[db] = {"payload": {"data": trades}, "fetched_at": time.time()}
        except Exception as e:
            logger.error("Background live open refresh failed: %s", e)
        finally:
            with _live_open_cache_lock:
                _live_open_refresh_in_progress.discard(db)

    threading.Thread(target=worker, daemon=True).start()


@app.get("/api/live_open_trades")
def live_open_trades(db: str = Query("tradedb")):
    with _live_open_cache_lock:
        entry = _live_open_cache.get(db)

    if entry is None:
        trades = _fetch_live_open_trades(db)
        payload = {"data": trades}
        with _live_open_cache_lock:
            _live_open_cache[db] = {"payload": payload, "fetched_at": time.time()}
        return payload

    age = time.time() - entry["fetched_at"]
    if age > _LIVE_OPEN_TTL_SECONDS:
        _kick_off_live_open_refresh(db)
    return entry["payload"]


def _fetch_nondna_open_trades(db: str) -> list[dict]:
    conn = connect_to_db(db)
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT guid, model, product, strategy_name, signal, net_return, alt_net_return,
                   entry_price, latest_price, created
            FROM dbo.combined_trades_open WITH (NOLOCK)
            WHERE model LIKE '1[0-9][0-9][0-9][0-9][0-9]' AND LEN(model) = 6 AND net_return IS NOT NULL
            OPTION (MAXDOP 1)
            """
        )
        cols = [c[0] for c in cur.description]
        trades = []
        for row in cur.fetchall():
            d = dict(zip(cols, row))
            for k, v in d.items():
                if hasattr(v, "isoformat"):
                    d[k] = v.isoformat()
                elif hasattr(v, "__float__"):
                    d[k] = float(v)
            trades.append(d)
        return trades
    except Exception as e:
        logger.error("Failed to query nondna open trades for db=%s: %s", db, e)
        return []
    finally:
        conn.close()


def _kick_off_nondna_open_refresh(db: str):
    with _nondna_open_cache_lock:
        if db in _nondna_open_refresh_in_progress:
            return
        _nondna_open_refresh_in_progress.add(db)

    def worker():
        try:
            trades = _fetch_nondna_open_trades(db)
            with _nondna_open_cache_lock:
                _nondna_open_cache[db] = {"payload": {"data": trades}, "fetched_at": time.time()}
        except Exception as e:
            logger.error("Background nondna open refresh failed: %s", e)
        finally:
            with _nondna_open_cache_lock:
                _nondna_open_refresh_in_progress.discard(db)

    threading.Thread(target=worker, daemon=True).start()


@app.get("/api/nondna_open_trades")
def nondna_open_trades(db: str = Query("tradedb")):
    with _nondna_open_cache_lock:
        entry = _nondna_open_cache.get(db)

    if entry is None:
        trades = _fetch_nondna_open_trades(db)
        payload = {"data": trades}
        with _nondna_open_cache_lock:
            _nondna_open_cache[db] = {"payload": payload, "fetched_at": time.time()}
        return payload

    age = time.time() - entry["fetched_at"]
    if age > _NONDNA_OPEN_TTL_SECONDS:
        _kick_off_nondna_open_refresh(db)
    return entry["payload"]


_CACHE_TTL_SECONDS = 300
_cache_lock = threading.Lock()
_cache: dict[tuple[str, str], dict] = {}  # (db, signal) -> cached aggregate
_refresh_in_progress: set[tuple[str, str]] = set()


@app.get("/api/breakout_backdrop")
def breakout_backdrop(db: str = Query("tradedb"), signal: str = Query("both", pattern="^(both|buy|sell)$")):
    """Real historical + current-state aggregate for the breakout strategy families,
    served from a cache that refreshes in the background (see version history above
    for why: the underlying query's cost on this DB is too unpredictable to run
    synchronously on every request).
    """
    key = (db, signal)
    with _cache_lock:
        entry = _cache.get(key)

    if entry is None:
        # Nothing cached yet - this request has to pay the real query cost once.
        payload = _run_query(db, signal)
        with _cache_lock:
            _cache[key] = {"payload": payload, "fetched_at": time.time()}
        return payload

    age = time.time() - entry["fetched_at"]
    if age > _CACHE_TTL_SECONDS:
        _kick_off_refresh(db, signal)
    payload = dict(entry["payload"])
    payload["cache_age_seconds"] = round(age, 1)
    return payload


@app.get("/api/intraday_series")
def intraday_series(db: str = Query("tradedb"), trade_date: str = Query(..., description="YYYY-MM-DD"),
                     signal: str = Query("both", pattern="^(both|buy|sell)$")):
    """Per-strategy cumulative net_return/alt_net_return through the day, timestamped
    at real trade-close resolution (not day-granularity), for the time-playback
    scrubber. closed_at follows the same COALESCE(g_close_time, last_update, created)
    convention api_server_sql/main.py already uses to mean "when a trade actually
    closed" - no new/fabricated timestamp concept. Real data only; not cached (called
    once per date selection, not on every poll)."""
    if signal not in {"both", "buy", "sell"}:
        raise ValueError("Invalid trade signal filter")
    conn = connect_to_db(db)
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT model, strategy_name,
                   COALESCE(g_close_time, last_update, created) AS closed_at,
                   CAST(net_return AS float) AS net_return,
                   CAST(alt_net_return AS float) AS alt_net_return
            FROM dbo.combined_trades_closed WITH (NOLOCK)
            WHERE ((strategy_name LIKE 'breakout%' AND (model LIKE 'DNA[_]1%' OR model LIKE 'DNA[_]2%'))
                   OR (model LIKE '1[0-9][0-9][0-9][0-9][0-9]' AND LEN(model) = 6))
              AND CAST(COALESCE(g_close_time, last_update, created) AS DATE) = ?
              AND (? = 'both' OR UPPER(LTRIM(RTRIM(signal))) = ?)
            ORDER BY model, closed_at
            OPTION (MAXDOP 1)
            """, trade_date, signal, signal.upper()
        )
        rows = cur.fetchall()
    finally:
        conn.close()

    from datetime import datetime as _dt
    day_start = _dt.fromisoformat(trade_date)
    series: dict[str, list] = defaultdict(list)
    running: dict[str, dict] = {}
    for model, strategy_name, closed_at, net_return, alt_net_return in rows:
        if not (is_dna(model) or is_nondna(model)):
            continue
        family = "nondna" if is_nondna(model) else family_of(strategy_name)
        if not family:
            continue
        r = running.setdefault(model, {"net": 0.0, "alt": 0.0})
        r["net"] += float(net_return or 0)
        r["alt"] += float(alt_net_return or 0)
        ms = int((closed_at - day_start).total_seconds() * 1000)
        series[model].append({"ms": ms, "net_return": round(r["net"], 2), "alt_net_return": round(r["alt"], 2)})

    return {"trade_date": trade_date, "signal_filter": signal, "series": series}


def _kick_off_refresh(db: str, signal: str = "both"):
    key = (db, signal)
    with _cache_lock:
        if key in _refresh_in_progress:
            return
        _refresh_in_progress.add(key)

    def worker():
        try:
            payload = _run_query(db, signal)
            with _cache_lock:
                _cache[key] = {"payload": payload, "fetched_at": time.time()}
        except Exception as e:
            logger.error("Background backdrop refresh failed for db=%s: %s", db, e)
        finally:
            with _cache_lock:
                _refresh_in_progress.discard(key)

    threading.Thread(target=worker, daemon=True).start()


def _run_query(db: str, signal: str = "both") -> dict:
    if signal not in {"both", "buy", "sell"}:
        raise ValueError("Invalid trade signal filter")
    conn = connect_to_db(db)
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cur = conn.cursor()

        # Grouping by model+date only (not also strategy_name/product, which are
        # constant per model) keeps the grouping key narrow - a bigint+date hash
        # needs far less workspace memory than one that also hashes two wide
        # nvarchar columns. strategy_name/product are recovered with MIN() since
        # they don't vary within a group. The trailing-90-day bound cuts the rows
        # entering the grouping operator (this backdrop only ever shows the last
        # handful of days anyway) - both changes shrink the memory grant SQL
        # Server requests, which matters because the instance is currently under
        # memory pressure (RESOURCE_SEMAPHORE waits observed across other
        # sessions too, not something this query alone can fix). MAXDOP 1 avoids
        # a parallel plan multiplying the grant across worker threads.
        cur.execute(
            """
            SELECT model, MIN(strategy_name) AS strategy_name, MIN(product) AS product,
                   CAST(created AS DATE) AS trade_date,
                   SUM(net_return) AS day_net,
                   SUM(alt_net_return) AS day_alt_net,
                   COUNT(*) AS day_count
            FROM dbo.combined_trades_closed WITH (NOLOCK)
            WHERE ((strategy_name LIKE 'breakout%' AND (model LIKE 'DNA[_]1%' OR model LIKE 'DNA[_]2%'))
                   OR (model LIKE '1[0-9][0-9][0-9][0-9][0-9]' AND LEN(model) = 6)) AND created >= DATEADD(day, -90, GETDATE())
              AND (? = 'both' OR UPPER(LTRIM(RTRIM(signal))) = ?)
            GROUP BY model, CAST(created AS DATE)
            ORDER BY trade_date
            OPTION (MAXDOP 1)
            """, signal, signal.upper()
        )
        closed_rows = cur.fetchall()

        cur.execute(
            """
            SELECT model, strategy_name, product, net_return, alt_net_return
            FROM dbo.combined_trades_open WITH (NOLOCK)
            WHERE ((strategy_name LIKE 'breakout%' AND (model LIKE 'DNA[_]1%' OR model LIKE 'DNA[_]2%'))
                   OR (model LIKE '1[0-9][0-9][0-9][0-9][0-9]' AND LEN(model) = 6)) AND net_return IS NOT NULL
              AND (? = 'both' OR UPPER(LTRIM(RTRIM(signal))) = ?)
            OPTION (MAXDOP 1)
            """, signal, signal.upper()
        )
        open_rows = cur.fetchall()
    finally:
        conn.close()

    lookup = nondna_tpsl_lookup(db)["lookup"]

    # strategy_id -> {strategy_name, family, group, product, daily: {date_str: {net_return, alt_net_return}}}
    strategies: dict[str, dict] = {}
    all_dates: set[str] = set()

    def new_entry(model, strategy_name, family, product):
        targets = lookup.get(f"{model}:{(product or '').upper()}", {}) if is_nondna(model) else {}
        return {
            "tp": targets.get("tp"), "sl": targets.get("sl"),
            "strategy_id": model, "strategy_name": strategy_name,
            "family": family, "group": "dna" if is_dna(model) else "nondna",
            "product": (product or "").upper(),
            "daily": defaultdict(lambda: {"net_return": 0.0, "alt_net_return": 0.0}), "trade_count": 0,
        }

    for model, strategy_name, product, trade_date, day_net, day_alt_net, day_count in closed_rows:
        if not (is_dna(model) or is_nondna(model)):
            continue
        family = "nondna" if is_nondna(model) else family_of(strategy_name)
        if not family:
            continue
        date_str = trade_date.isoformat()
        all_dates.add(date_str)
        entry = strategies.setdefault(model, new_entry(model, strategy_name, family, product))
        entry["daily"][date_str]["net_return"] += float(day_net or 0)
        entry["daily"][date_str]["alt_net_return"] += float(day_alt_net or 0)
        entry["trade_count"] += int(day_count or 0)

    open_by_strategy: dict[str, dict] = defaultdict(lambda: {"net_return": 0.0, "alt_net_return": 0.0})
    for model, strategy_name, product, net_return, alt_net_return in open_rows:
        if not (is_dna(model) or is_nondna(model)):
            continue
        family = "nondna" if is_nondna(model) else family_of(strategy_name)
        if not family:
            continue
        open_by_strategy[model]["net_return"] += float(net_return or 0)
        open_by_strategy[model]["alt_net_return"] += float(alt_net_return or 0)
        strategies.setdefault(model, new_entry(model, strategy_name, family, product))

    sorted_dates = sorted(all_dates)
    historical_snapshots = sorted_dates[-4:] if len(sorted_dates) >= 4 else sorted_dates
    today_str = date.today().isoformat()
    snapshot_dates = historical_snapshots + [today_str] if not historical_snapshots or historical_snapshots[-1] != today_str else historical_snapshots
    # Guarantee exactly the historical days plus a distinct trailing "now" snapshot.
    if snapshot_dates[-1] != today_str:
        snapshot_dates = snapshot_dates + [today_str]
    snapshot_dates = snapshot_dates[-5:]

    out_strategies = []
    for model, s in strategies.items():
        net_by_snapshot, alt_by_snapshot = [], []
        running_net, running_alt = 0.0, 0.0
        # cumulative = sum of every closed day up to and including each snapshot date
        daily = s["daily"]
        prior_dates_used = set()
        open_vals = open_by_strategy.get(model, {"net_return": 0.0, "alt_net_return": 0.0})
        for snap_date in snapshot_dates:
            for d, day_vals in daily.items():
                if d <= snap_date and d not in prior_dates_used:
                    running_net += day_vals["net_return"]
                    running_alt += day_vals["alt_net_return"]
                    prior_dates_used.add(d)
            net_val, alt_val = running_net, running_alt
            if snap_date == today_str:
                net_val += open_vals["net_return"]
                alt_val += open_vals["alt_net_return"]
            net_by_snapshot.append(round(net_val, 2))
            alt_by_snapshot.append(round(alt_val, 2))
        out_strategies.append({
            "strategy_id": s["strategy_id"],
            "strategy_name": s["strategy_name"],
            "tp": s["tp"], "sl": s["sl"],
            "family": s["family"],
            "group": s["group"],  # 'dna' | 'nondna' - for the Trade Group filter only, not layout
            "product": s["product"],
            "trade_count": s["trade_count"],
            "open_net_return": round(open_vals["net_return"], 2),
            "open_alt_net_return": round(open_vals["alt_net_return"], 2),
            "net_series": net_by_snapshot,
            "alt_net_series": alt_by_snapshot,
        })

    return {
        "generated_at": date.today().isoformat(),
        "signal_filter": signal,
        "snapshot_dates": snapshot_dates,
        "strategies": out_strategies,
        "total_strategies": len(out_strategies),
    }
