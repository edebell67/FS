# epics/ep_057_sql_to_pgsql/dashboards_and_uis/top10_live_server.py — Live equity-curve API and static dashboard server.
#
# VERSION HISTORY
# v1.10.3 · 2026-10-05 · trade_log product filter is an exact match; adds /api/trade_log_products for the dropdown.
# v1.10.2 · 2026-10-05 · /api/trade_log accepts model, strategy, product (contains) and signal (buy|sell) filters.
# v1.10.1 · 2026-10-05 · /trading_log.html is served from epics/ep_063_Trading_log/.
# v1.10.0 · 2026-10-05 · Adds /api/trade_log (last 50 executions, open + closed, forex/crypto filter) for trading_log.html.
# v1.9.1 · 2026-09-28 · Fixes LAST_SNAP_SIDE_SQL (added in v1.9.0): a DISTINCT ON + model=ANY(huge-array) shape
#   forced a full parallel seq scan (~12.6s for 2258 forex models, most of a >60s live_day timeout on its own).
#   Rewritten as a per-model LATERAL index lookup (~0.7s for the same 2258 models).
# v1.9.0 · 2026-09-28 · Adds top_buy_sell_net scenario: ranks each model by its own dominant side
#   (GREATEST(cum_buy_net, cum_sell_net) at its last 5-min snapshot of the day), not total net_return.
# v1.8.0 · 2026-09-25 · Adds live hourly exit reporting by product type, product, family, and side.
# v1.7.0 · 2026-09-24 · Adds the filterable single-strategy portfolio catalogue.
# v1.6.0 · 2026-09-24 · Adds same-product strategy comparisons by family, window, TP, or SL.
# v1.5.0 · 2026-09-23 · _connect() honours DATABASE_URL (Render); PG* variables remain the local default.
# v1.4.0 · 2026-09-22 · Adds configurable 10/20/30 scenario limits and explicit portfolio model snapshots (maximum ten models).
# v1.3.0 · 2026-09-22 · Adds canonical breakout strategy-family filtering before scenario ranking.
# v1.2.0 · 2026-09-22 · Adds validated dependent product filtering and product metadata so every dashboard result can share the selected type/product scope.
# v1.1.0 · 2026-09-21 · Adds validated product-type filtering so callers can isolate forex or crypto models without changing the default all-products view.
# v1.0.0 · 2026-09-21 · Version history added; file predates this convention.
"""
EP057 Top10 5min Equity Curves - static + live data server (port 8765).

Serves this folder (so top10_5min_equity_curves.html loads as before) and adds:
    GET /api/live_day?date=YYYY-MM-DD
returning {"date", "generated_at", "top_net": [...], "top_alt_net": [...]}
in the same model-list shape as ALL_CRITERIA_DATA[scenario][date], built
with the same queries as scratch_and_tools/append_today_data_to_html.py.

DB settings come from PGHOST/PGPORT/PGDATABASE/PGUSER/PGPASSWORD (repo .env
is loaded if present), defaulting to the local tradedb used by the ep057 scripts.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import psycopg2

HERE = Path(__file__).resolve().parent
PORT = int(os.environ.get("EP057_LIVE_PORT", "8765"))

try:
    from dotenv import load_dotenv

    load_dotenv(HERE.parents[2] / ".env")
except ImportError:
    pass

COLORS = [
    "#38bdf8", "#34d399", "#f472b6", "#fbbf24", "#a78bfa",
    "#fb923c", "#2dd4bf", "#4ade80", "#e879f9", "#f87171",
]

# Per-model stats for one trading date; strategy/tp from the canonical model definition
STATS_SQL = """
    WITH bounds AS (SELECT %s::date AS day)
    SELECT c.model,
           ROUND(SUM(c.net_return)::numeric, 2) AS total_net,
           ROUND(SUM(c.alt_net_return)::numeric, 2) AS total_alt_net,
           COUNT(*) AS total_trades,
           COUNT(*) FILTER (WHERE c.net_return > 0) AS wins,
           COUNT(*) FILTER (WHERE c.net_return <= 0) AS losses,
           ROUND((COUNT(*) FILTER (WHERE c.net_return > 0)::numeric / COUNT(*)::numeric * 100), 1) AS win_rate,
           COUNT(*) FILTER (WHERE c.alt_net_return > 0) AS alt_wins,
           ROUND((COUNT(*) FILTER (WHERE c.alt_net_return > 0)::numeric / COUNT(*)::numeric * 100), 1) AS alt_win_rate,
           MAX(c.product) AS product,
           COALESCE(MAX(pf.strategy_name), MAX(c.strategy_name)) AS strategy,
           MAX(pf.target_profit) AS target_profit,
           MAX(c.product_type) AS product_type
    FROM combined_trades_closed c
    CROSS JOIN bounds b
    LEFT JOIN product_forex pf ON pf.model = c.model
    WHERE c.created >= b.day
      AND c.created < b.day + INTERVAL '1 day'
      AND (%s = 'all' OR c.product_type = %s)
      AND (%s = 'all' OR c.product = %s)
    GROUP BY c.model;
"""

# Portfolio loads already know the model ids. Pushing that restriction into SQL
# avoids aggregating every model for the day and then discarding almost all rows.
PORTFOLIO_STATS_SQL = STATS_SQL.replace(
    "GROUP BY c.model", "AND c.model = ANY(%s)\n    GROUP BY c.model"
)

PRODUCTS_SQL = """
    SELECT DISTINCT LOWER(TRIM(product)) AS product
    FROM product_forex
    WHERE product IS NOT NULL
      AND (%s = 'all' OR LOWER(TRIM(product_type)) = %s)
    ORDER BY product;
"""

SNAP_SQL = """
    WITH bounds AS (SELECT %s::date AS day)
    SELECT model,
           to_char(snapshot_timestamp, 'HH24:MI') AS time_str,
           ROUND(cum_net::numeric, 1), ROUND(cum_buy_net::numeric, 1), ROUND(cum_sell_net::numeric, 1),
           ROUND(cum_alt_net::numeric, 1), ROUND(cum_buy_alt_net::numeric, 1), ROUND(cum_sell_alt_net::numeric, 1),
           open_trade_count, closed_trade_count
    FROM tbl_dna_model_summary_snapshots_5min s
    CROSS JOIN bounds b
    WHERE snapshot_timestamp >= b.day
      AND snapshot_timestamp < b.day + INTERVAL '1 day'
      AND model = ANY(%s)
    ORDER BY snapshot_timestamp;
"""

TOUCHED_RANK_ONE_SQL = """
    WITH bounds AS (SELECT %s::date AS day), ranked AS (
        SELECT model, snapshot_timestamp,
               DENSE_RANK() OVER (
                   PARTITION BY snapshot_timestamp
                   ORDER BY cum_net DESC
               ) AS position
        FROM tbl_dna_model_summary_snapshots_5min s
        CROSS JOIN bounds b
        WHERE snapshot_timestamp >= b.day
          AND snapshot_timestamp < b.day + INTERVAL '1 day'
          AND model = ANY(%s)
    )
    SELECT DISTINCT model
    FROM ranked
    WHERE position = 1;
"""

# Each model's own dominant side for the day: whichever of cum_buy_net/cum_sell_net is larger
# at its last 5-min snapshot. Drives the top_buy_sell_net scenario (rank by GREATEST(buy, sell),
# not total net_return) - a model with a strong buy leg and a weak/negative sell leg still ranks
# on its buy leg's strength, and vice versa.
# A DISTINCT ON (model) ... WHERE model = ANY(%s) shape here forces Postgres into a full parallel
# seq scan + sort over the whole day's snapshot rows once the model list gets into the thousands
# (measured ~12.6s for 2258 forex models - the majority of a >60s live_day timeout on its own).
# This LATERAL form does one indexed lookup per model instead (ix_dna_summary_5min_model_ts),
# ~0.7s for the same 2258 models - a ~17x reduction.
LAST_SNAP_SIDE_SQL = """
    SELECT m.model, snap.cum_buy_net, snap.cum_sell_net
    FROM unnest(%s::text[]) AS m(model)
    CROSS JOIN LATERAL (
        SELECT cum_buy_net, cum_sell_net
        FROM tbl_dna_model_summary_snapshots_5min s
        WHERE s.model = m.model
          AND s.snapshot_timestamp >= %s::date
          AND s.snapshot_timestamp < %s::date + INTERVAL '1 day'
        ORDER BY s.snapshot_timestamp DESC
        LIMIT 1
    ) snap;
"""


def _f(v) -> float:
    return float(v) if v is not None else 0.0


def _connect():
    if os.environ.get("DATABASE_URL"):
        return psycopg2.connect(os.environ["DATABASE_URL"], connect_timeout=5)
    return psycopg2.connect(
        host=os.environ.get("PGHOST", "localhost"),
        port=int(os.environ.get("PGPORT", "5432")),
        dbname=os.environ.get("PGDATABASE", "tradedb"),
        user=os.environ.get("PGUSER", "postgres"),
        password=os.environ.get("PGPASSWORD"),
        connect_timeout=5,
    )


STAT_COLS = ["model", "net", "alt", "trades", "wins", "losses", "win_rate",
             "alt_wins", "alt_win_rate", "product", "strategy", "target_profit", "product_type"]
MIN_SCENARIO_MODELS = 2  # fewer qualifying models -> scenario falls back to top_net


def _family_leaders(stats: list[dict], metric: str) -> list[dict]:
    """Return the best strategy in each canonical family for the chosen metric."""
    win_metric = "alt_win_rate" if metric == "alt" else "win_rate"
    winners: dict[str, dict] = {}
    for stat in stats:
        family = strategy_family(stat.get("strategy"))
        if family == "unknown":
            continue
        incumbent = winners.get(family)
        rank_key = (-stat[metric], -stat[win_metric], stat["model"])
        if incumbent is None or rank_key < (-incumbent[metric], -incumbent[win_metric], incumbent["model"]):
            winners[family] = stat
    family_order = ("breakout", "breakout_r", "breakout_rev", "breakout_r_rev")
    return [winners[family] for family in family_order if family in winners]


def _top_family(stats: list[dict], family: str, metric: str, limit: int = 5) -> list[dict]:
    """Return the strongest models in one family for the selected return metric."""
    win_metric = "alt_win_rate" if metric == "alt" else "win_rate"
    return sorted(
        (stat for stat in stats if strategy_family(stat.get("strategy")) == family),
        key=lambda stat: (-stat[metric], -stat[win_metric], stat["model"]),
    )[:limit]


TP_SL_RE = re.compile(r"(?:^|_)tp(?P<tp>\d+)_sl(?P<sl>\d+)(?:_|$)", re.IGNORECASE)
STRATEGY_SHAPE_RE = re.compile(
    r"^(?P<family>breakout(?:_r_rev|_rev|_r)?)_(?P<window>\d+)_tp(?P<tp>\d+)_sl(?P<sl>\d+)$",
    re.IGNORECASE,
)
CRYPTO_STRATEGY_SHAPE_RE = re.compile(
    r"^(?P<family>dna\d+_crypto)_tp(?P<tp>\d+)_sl(?P<sl>\d+)$",
    re.IGNORECASE,
)


def strategy_tp_sl(strategy: str | None) -> tuple[int, int] | None:
    """Extract the configured take-profit and stop-loss pair from a strategy name."""
    match = TP_SL_RE.search(strategy or "")
    return (int(match.group("tp")), int(match.group("sl"))) if match else None


def strategy_shape(strategy: str | None) -> dict | None:
    """Parse canonical Forex or Crypto family/window/TP/SL strategy names."""
    value = (strategy or "").strip()
    match = STRATEGY_SHAPE_RE.fullmatch(value)
    if match:
        return {
            "family": match.group("family").lower(),
            "window": int(match.group("window")),
            "tp": int(match.group("tp")),
            "sl": int(match.group("sl")),
        }
    match = CRYPTO_STRATEGY_SHAPE_RE.fullmatch(value)
    if not match:
        return None
    return {
        "family": match.group("family").lower(),
        "window": None,
        "tp": int(match.group("tp")),
        "sl": int(match.group("sl")),
    }


def _top_tp_sl(stats: list[dict], tp: int, sl: int, metric: str, limit: int = 3) -> list[dict]:
    """Return the strongest models for one exact TP/SL combination."""
    win_metric = "alt_win_rate" if metric == "alt" else "win_rate"
    return sorted(
        (stat for stat in stats if strategy_tp_sl(stat.get("strategy")) == (tp, sl)),
        key=lambda stat: (-stat[metric], -stat[win_metric], stat["model"]),
    )[:limit]


def _scenario_ids(stats: list[dict], snaps: dict[str, list[dict]], limit: int = 10,
                  touched_rank_one_ids: set[str] | None = None,
                  family_stats: list[dict] | None = None,
                  buy_sell_rank: list[str] | None = None) -> dict[str, list[str]]:
    """Scenario model lists for one trading date.

    Rules reproduce the stored 14-18 Sep lists: each scenario filters the day's pool
    (Top 10 Net Return + Top 10 Win Rate) and falls back to Top 10 Net Return when fewer
    than MIN_SCENARIO_MODELS qualify. weakening_selection follows its catalogue text
    (high-volume pool models below their intraday peak) - the original rule is unknown.
    """
    by_net = sorted(stats, key=lambda s: (-s["net"], -s["win_rate"], s["model"]))
    top_net = by_net[:limit]
    top_alt = sorted(stats, key=lambda s: (-s["alt"], s["model"]))[:limit]
    top_win = sorted((s for s in stats if s["win_rate"] >= 50),
                     key=lambda s: (-s["win_rate"], -s["net"], s["model"]))[:limit]
    pool, seen = [], set()
    for s in top_net + top_win:
        if s["model"] not in seen:
            seen.add(s["model"])
            pool.append(s)

    def tp_pips(s):
        return (s["target_profit"] or 0) / 10

    def drawdown(s):
        series = snaps.get(s["model"]) or []
        return (max(p["net"] for p in series) - series[-1]["net"]) if series else 0.0

    def pick(models, pick_limit=None):
        models = list(models)[:pick_limit or limit]
        return models if len(models) >= MIN_SCENARIO_MODELS else top_net

    family_stats = family_stats if family_stats is not None else stats
    lists = {
        "top_net": top_net,
        "top_alt_net": top_alt,
        "family_leaders_net": _family_leaders(stats, "net"),
        "family_leaders_alt": _family_leaders(stats, "alt"),
        "top_win": top_win or top_net,
        "strongest_three": sorted(pool, key=lambda s: -s["net"])[:3],
        "strengthening_cluster": pick(s for s in pool if (s["strategy"] or "").startswith("breakout_R_")),
        "relative_value": pick(sorted((s for s in pool if s["win_rate"] >= 85), key=lambda s: -s["win_rate"])),
        "market_move": pick(s for s in pool if tp_pips(s) >= 10),
        "opposite_cluster": pick(s for s in pool if 3 <= tp_pips(s) <= 5),
        "weakening_selection": pick(sorted((s for s in pool if drawdown(s) > 0),
                                           key=lambda s: (-s["trades"], -drawdown(s)))),
        "repair_negative": pick(s for s in pool if s["win_rate"] == 100 and s["net"] > 0),
        # Every strategy that held the highest cumulative net at one or more
        # five-minute snapshots. Ties at #1 are deliberately included.
        "touched_rank_one": sorted(
            (s for s in stats if s["model"] in (touched_rank_one_ids or set())),
            key=lambda s: (-s["net"], -s["win_rate"], s["model"]),
        )[:limit],
    }
    for family in ("breakout", "breakout_r", "breakout_rev", "breakout_r_rev"):
        lists[f"top5_{family}_net"] = _top_family(family_stats, family, "net")
        lists[f"top5_{family}_alt"] = _top_family(family_stats, family, "alt")
    for tp, sl in sorted({pair for stat in stats if (pair := strategy_tp_sl(stat.get("strategy")))}):
        scenario_id = f"top3_tp{tp}_sl{sl}"
        lists[f"{scenario_id}_net"] = _top_tp_sl(stats, tp, sl, "net")
        lists[f"{scenario_id}_alt"] = _top_tp_sl(stats, tp, sl, "alt")
    lists["NET_RETURN"] = lists["top_net"]
    lists["WIN_RATE"] = lists["top_win"]
    result = {k: [s["model"] for s in v] for k, v in lists.items()}
    # Ranked by each model's own dominant side (GREATEST(cum_buy_net, cum_sell_net)), not total
    # net_return - see LAST_SNAP_SIDE_SQL. Empty when the caller doesn't have day-snapshot access
    # (e.g. the point-in-time replay path), so it simply won't appear in that payload.
    result["top_buy_sell_net"] = (buy_sell_rank or [])[:limit]
    return result


def build_point_in_time_scenario(date_str: str, at_time: str, scenario: str = "top_net",
                                 return_type: str = "NET", product_type: str = "all",
                                 product: str = "all", strategy_family_filter: str = "all",
                                 limit: int = 10, min_win_rate: float = 0.0) -> dict:
    """Re-evaluate a scenario from the full strategy universe at one snapshot time.

    Selection uses only the latest 5-minute snapshot and closed-trade evidence
    available on or before the requested time. Returned curves extend through
    the rest of the day so the captured cohort can be assessed afterwards.
    """
    product_type = normalize_product_type(product_type)
    product = normalize_product(product)
    strategy_family_filter = normalize_strategy_family(strategy_family_filter)
    limit = normalize_model_limit(limit)
    return_type = str(return_type or "NET").upper()
    if return_type not in {"NET", "ALT"}:
        raise ValueError("return_type must be NET or ALT")
    if not re.fullmatch(r"\d{2}:\d{2}", str(at_time)):
        raise ValueError("at_time must be HH:MM")
    hour, minute = map(int, at_time.split(":"))
    if hour > 23 or minute > 59:
        raise ValueError("at_time must be a valid HH:MM time")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", str(scenario)):
        raise ValueError("scenario contains unsupported characters")
    if not 0 <= float(min_win_rate) <= 100:
        raise ValueError("min_win_rate must be between 0 and 100")

    metric = "alt" if return_type == "ALT" else "net"
    scenario_key = scenario
    if scenario == "family_leaders" or scenario.startswith("top5_") or scenario.startswith("top3_tp"):
        scenario_key = f"{scenario}_{metric}"

    point_sql = """
        WITH bounds AS (
          SELECT %s::date AS day,
                 (%s::date + %s::time) AS cutoff
        ), model_meta AS (
          SELECT TRIM(model) AS model, MAX(LOWER(TRIM(product))) AS product,
                 MAX(TRIM(strategy_name)) AS strategy, MAX(target_profit) AS target_profit,
                 MAX(LOWER(TRIM(product_type))) AS product_type
          FROM product_forex
          WHERE product IS NOT NULL
            AND (%s = 'all' OR LOWER(TRIM(product_type)) = %s)
            AND (%s = 'all' OR LOWER(TRIM(product)) = %s)
          GROUP BY TRIM(model)
        ), asof_snap AS (
          SELECT DISTINCT ON (s.model) s.model, s.snapshot_timestamp,
                 s.cum_net, s.cum_alt_net, s.open_trade_count, s.closed_trade_count
          FROM tbl_dna_model_summary_snapshots_5min s CROSS JOIN bounds b
          WHERE s.snapshot_timestamp >= b.day AND s.snapshot_timestamp <= b.cutoff
          ORDER BY s.model, s.snapshot_timestamp DESC
        ), asof_trades AS (
          SELECT c.model, COUNT(*) AS trades,
                 COUNT(*) FILTER (WHERE c.net_return > 0) AS wins,
                 COUNT(*) FILTER (WHERE c.net_return <= 0) AS losses,
                 COUNT(*) FILTER (WHERE c.alt_net_return > 0) AS alt_wins
          FROM combined_trades_closed c CROSS JOIN bounds b
          WHERE c.created >= b.day AND c.created < b.day + INTERVAL '1 day'
            AND c.last_update <= b.cutoff
            AND (%s = 'all' OR LOWER(TRIM(c.product_type)) = %s)
            AND (%s = 'all' OR LOWER(TRIM(c.product)) = %s)
          GROUP BY c.model
        )
        SELECT m.model, m.product, m.strategy, m.target_profit, m.product_type,
               p.snapshot_timestamp, p.cum_net, p.cum_alt_net,
               p.open_trade_count, p.closed_trade_count,
               COALESCE(t.trades, 0), COALESCE(t.wins, 0), COALESCE(t.losses, 0),
               COALESCE(t.alt_wins, 0)
        FROM model_meta m JOIN asof_snap p ON p.model = m.model
        LEFT JOIN asof_trades t ON t.model = m.model
    """
    history_sql = """
        WITH bounds AS (SELECT %s::date AS day, (%s::date + %s::time) AS cutoff)
        SELECT s.model, to_char(s.snapshot_timestamp, 'HH24:MI'),
               ROUND(s.cum_net::numeric, 1), ROUND(s.cum_buy_net::numeric, 1),
               ROUND(s.cum_sell_net::numeric, 1), ROUND(s.cum_alt_net::numeric, 1),
               ROUND(s.cum_buy_alt_net::numeric, 1), ROUND(s.cum_sell_alt_net::numeric, 1),
               s.open_trade_count, s.closed_trade_count
        FROM tbl_dna_model_summary_snapshots_5min s CROSS JOIN bounds b
        WHERE s.snapshot_timestamp >= b.day AND s.snapshot_timestamp <= b.cutoff
          AND s.model = ANY(%s)
        ORDER BY s.model, s.snapshot_timestamp
    """
    with _connect() as conn, conn.cursor() as cur:
        cur.execute(point_sql, (date_str, date_str, at_time,
                                product_type, product_type, product, product,
                                product_type, product_type, product, product))
        rows = cur.fetchall()
        if not rows:
            return {"date": date_str, "at_time": at_time, "scenario": scenario_key, "models": []}

        stats = []
        for row in rows:
            model, prod, strategy, target_profit, ptype, snap_ts, net, alt, opened, snap_trades, trades, wins, losses, alt_wins = row
            trades = int(trades or snap_trades or 0)
            wins, losses, alt_wins = int(wins or 0), int(losses or 0), int(alt_wins or 0)
            stats.append({
                "model": model, "product": prod, "strategy": strategy or "",
                "target_profit": _f(target_profit), "product_type": ptype,
                "net": _f(net), "alt": _f(alt), "trades": trades,
                "wins": wins, "losses": losses,
                "win_rate": round(wins / trades * 100, 1) if trades else 0.0,
                "alt_wins": alt_wins,
                "alt_win_rate": round(alt_wins / trades * 100, 1) if trades else 0.0,
            })
        family_stats = list(stats)
        if strategy_family_filter != "all":
            stats = [s for s in stats if strategy_family(s["strategy"]) == strategy_family_filter]
        eligible_ids = {s["model"] for s in stats}
        cur.execute(history_sql, (date_str, date_str, at_time, sorted(eligible_ids)))
        snaps: dict[str, list[dict]] = {}
        for m, tm, net, buy, sell, alt_net, alt_buy, alt_sell, op, tr in cur.fetchall():
            if m not in eligible_ids:
                continue
            snaps.setdefault(m, []).append({"time": tm, "net": _f(net), "buy": _f(buy), "sell": _f(sell),
                "alt_net": _f(alt_net), "alt_buy": _f(alt_buy), "alt_sell": _f(alt_sell),
                "open": int(op or 0), "trades": int(tr or 0)})

        touched_rank_one_ids: set[str] = set()
        snapshots_by_time: dict[str, list[tuple[float, str]]] = {}
        for model, values in snaps.items():
            for point in values:
                snapshots_by_time.setdefault(point["time"], []).append((point["net"], model))
        for ranked in snapshots_by_time.values():
            if ranked:
                best = max(value for value, _ in ranked)
                touched_rank_one_ids.update(model for value, model in ranked if value == best)
        selected = _scenario_ids(stats, snaps, limit, touched_rank_one_ids, family_stats).get(scenario_key, [])
        stats_by_id = {s["model"]: s for s in family_stats}
        selected = [m for m in selected if stats_by_id[m]["win_rate"] >= float(min_win_rate)]
        if not selected:
            return {"date": date_str, "at_time": at_time, "scenario": scenario_key, "models": []}
        cur.execute(SNAP_SQL, (date_str, selected))
        full_series: dict[str, list[dict]] = {}
        for m, tm, net, buy, sell, alt_net, alt_buy, alt_sell, op, tr in cur.fetchall():
            full_series.setdefault(m, []).append({"time": tm, "net": _f(net), "buy": _f(buy), "sell": _f(sell),
                "alt_net": _f(alt_net), "alt_buy": _f(alt_buy), "alt_sell": _f(alt_sell),
                "open": int(op or 0), "trades": int(tr or 0)})

    models = []
    for rank, model in enumerate(selected, 1):
        stat = stats_by_id[model]
        series = full_series.get(model, [])
        head = series[-1] if series else {}
        models.append({
            "rank": rank, "model": model, "product": stat["product"],
            "product_type": stat["product_type"], "strategy": stat["strategy"],
            "color": COLORS[(rank - 1) % len(COLORS)], "trades": stat["trades"],
            "wins": stat["wins"], "losses": stat["losses"], "win_rate": stat["win_rate"],
            "alt_wins": stat["alt_wins"], "alt_win_rate": stat["alt_win_rate"],
            "cum_net": head.get("net", 0.0), "buy_net": head.get("buy", 0.0),
            "sell_net": head.get("sell", 0.0), "cum_alt_net": head.get("alt_net", 0.0),
            "buy_alt_net": head.get("alt_buy", 0.0), "sell_alt_net": head.get("alt_sell", 0.0),
            "series": series,
        })
    return {"date": date_str, "at_time": at_time, "scenario": scenario_key, "models": models}


def build_point_in_time_scenario_hours(date_str: str, scenario: str = "top_net",
                                       return_type: str = "NET", product_type: str = "all",
                                       product: str = "all", strategy_family_filter: str = "all",
                                       limit: int = 10, min_win_rate: float = 0.0) -> dict:
    """Return the selected strategy cohort at every completed clock-hour cutoff.

    The universe, snapshots, and closed-trade evidence are read once, then each
    hourly cohort is ranked using only data available by that cutoff.
    """
    product_type = normalize_product_type(product_type)
    product = normalize_product(product)
    strategy_family_filter = normalize_strategy_family(strategy_family_filter)
    limit = normalize_model_limit(limit)
    return_type = str(return_type or "NET").upper()
    if return_type not in {"NET", "ALT"}:
        raise ValueError("return_type must be NET or ALT")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", str(scenario)):
        raise ValueError("scenario contains unsupported characters")
    if not 0 <= float(min_win_rate) <= 100:
        raise ValueError("min_win_rate must be between 0 and 100")

    metric = "alt" if return_type == "ALT" else "net"
    scenario_key = scenario
    if scenario == "family_leaders" or scenario.startswith("top5_") or scenario.startswith("top3_tp"):
        scenario_key = f"{scenario}_{metric}"
    with _connect() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT TRIM(model), MAX(LOWER(TRIM(product))), MAX(TRIM(strategy_name)),
                   MAX(target_profit), MAX(LOWER(TRIM(product_type)))
            FROM product_forex
            WHERE product IS NOT NULL
              AND (%s = 'all' OR LOWER(TRIM(product_type)) = %s)
              AND (%s = 'all' OR LOWER(TRIM(product)) = %s)
            GROUP BY TRIM(model)
        """, (product_type, product_type, product, product))
        metadata = {row[0]: {"product": row[1], "strategy": row[2] or "",
                             "target_profit": _f(row[3]), "product_type": row[4]}
                    for row in cur.fetchall()}
        if not metadata:
            return {"date": date_str, "scenario": scenario_key, "hours": []}

        cur.execute("""
            SELECT model, snapshot_timestamp, cum_net, cum_buy_net, cum_sell_net,
                   cum_alt_net, cum_buy_alt_net, cum_sell_alt_net,
                   open_trade_count, closed_trade_count
            FROM tbl_dna_model_summary_snapshots_5min
            WHERE snapshot_timestamp >= %s::date
              AND snapshot_timestamp < %s::date + INTERVAL '1 day'
              AND model = ANY(%s)
            ORDER BY snapshot_timestamp, model
        """, (date_str, date_str, list(metadata)))
        snapshot_rows = cur.fetchall()
        cur.execute("""
            SELECT model, last_update, net_return, alt_net_return
            FROM combined_trades_closed
            WHERE created >= %s::date AND created < %s::date + INTERVAL '1 day'
              AND last_update >= %s::date AND last_update < %s::date + INTERVAL '1 day'
              AND (%s = 'all' OR LOWER(TRIM(product_type)) = %s)
              AND (%s = 'all' OR LOWER(TRIM(product)) = %s)
            ORDER BY last_update, model
        """, (date_str, date_str, date_str, date_str,
              product_type, product_type, product, product))
        trade_rows = cur.fetchall()

    def naive(value):
        return value.replace(tzinfo=None) if getattr(value, "tzinfo", None) else value

    snapshot_rows = [(model, naive(ts), _f(net), _f(buy), _f(sell), _f(alt),
                      _f(alt_buy), _f(alt_sell), int(opened or 0), int(closed or 0))
                     for model, ts, net, buy, sell, alt, alt_buy, alt_sell, opened, closed
                     in snapshot_rows if model in metadata]
    trade_rows = [(model, naive(ts), _f(net), _f(alt))
                  for model, ts, net, alt in trade_rows if model in metadata]
    if not snapshot_rows:
        return {"date": date_str, "scenario": scenario_key, "hours": []}

    day = dt.date.fromisoformat(date_str)
    first_snapshot_time = snapshot_rows[0][1]
    first_hour = first_snapshot_time.hour + int(bool(first_snapshot_time.minute or first_snapshot_time.second or first_snapshot_time.microsecond))
    last_hour = snapshot_rows[-1][1].hour
    snap_index = trade_index = 0
    latest: dict[str, tuple] = {}
    histories: dict[str, list[dict]] = {}
    closed: dict[str, list[tuple[float, float]]] = {}
    hourly = []
    for hour in range(first_hour, last_hour + 1):
        cutoff = dt.datetime.combine(day, dt.time(hour=hour))
        while snap_index < len(snapshot_rows) and snapshot_rows[snap_index][1] <= cutoff:
            row = snapshot_rows[snap_index]
            model, ts, net, buy, sell, alt, alt_buy, alt_sell, opened, trades = row
            latest[model] = row
            histories.setdefault(model, []).append({"time": ts.strftime("%H:%M"), "net": net,
                "buy": buy, "sell": sell, "alt_net": alt, "alt_buy": alt_buy,
                "alt_sell": alt_sell, "open": opened, "trades": trades})
            snap_index += 1
        while trade_index < len(trade_rows) and trade_rows[trade_index][1] <= cutoff:
            model, _, net, alt = trade_rows[trade_index]
            closed.setdefault(model, []).append((net, alt))
            trade_index += 1

        stats = []
        for model, row in latest.items():
            info = metadata[model]
            events = closed.get(model, [])
            trades = len(events) or row[9]
            wins = sum(1 for net, _ in events if net > 0)
            losses = sum(1 for net, _ in events if net <= 0)
            alt_wins = sum(1 for _, alt in events if alt > 0)
            win_rate = round(wins / trades * 100, 1) if trades else 0.0
            alt_win_rate = round(alt_wins / trades * 100, 1) if trades else 0.0
            stats.append({"model": model, **info, "net": row[2], "alt": row[5],
                "trades": trades, "wins": wins, "losses": losses, "win_rate": win_rate,
                "alt_wins": alt_wins, "alt_win_rate": alt_win_rate})
        family_stats = list(stats)
        if strategy_family_filter != "all":
            stats = [item for item in stats if strategy_family(item["strategy"]) == strategy_family_filter]
        eligible_ids = {item["model"] for item in stats}
        snaps = {model: points for model, points in histories.items() if model in eligible_ids}
        snapshots_by_time: dict[str, list[tuple[float, str]]] = {}
        for model, points in snaps.items():
            for point in points:
                snapshots_by_time.setdefault(point["time"], []).append((point["net"], model))
        touched_rank_one_ids: set[str] = set()
        for ranked in snapshots_by_time.values():
            if ranked:
                best = max(value for value, _ in ranked)
                touched_rank_one_ids.update(model for value, model in ranked if value == best)
        selected = _scenario_ids(stats, snaps, limit, touched_rank_one_ids, family_stats).get(scenario_key, [])
        stats_by_id = {item["model"]: item for item in family_stats}
        selected = [model for model in selected if stats_by_id[model]["win_rate"] >= float(min_win_rate)]
        cohort = [{"rank": rank, "model": model, "product": stats_by_id[model]["product"],
                   "strategy": stats_by_id[model]["strategy"], "trades": stats_by_id[model]["trades"],
                   "win_rate": stats_by_id[model]["win_rate"], "net": stats_by_id[model]["net"]}
                  for rank, model in enumerate(selected, 1)]
        hourly.append({"at_time": f"{hour:02d}:00", "models": cohort})
    return {"date": date_str, "scenario": scenario_key, "hours": hourly}


PRODUCT_TYPES = {"all", "forex", "crypto"}
STRATEGY_FAMILIES = {"all", "breakout", "breakout_r", "breakout_rev", "breakout_r_rev"}


def normalize_product_type(value: str | None) -> str:
    product_type = (value or "all").strip().lower()
    if product_type not in PRODUCT_TYPES:
        raise ValueError("product_type must be all, forex, or crypto")
    return product_type


def normalize_product(value: str | None) -> str:
    product = (value or "all").strip().lower()
    if product != "all" and not re.fullmatch(r"[a-z0-9._-]+", product):
        raise ValueError("product contains unsupported characters")
    return product


def strategy_family(value: str | None) -> str:
    name = (value or "").strip().lower()
    for family in ("breakout_r_rev", "breakout_rev", "breakout_r", "breakout"):
        if name == family or name.startswith(f"{family}_"):
            return family
    return "unknown"


def normalize_strategy_family(value: str | None) -> str:
    family = (value or "all").strip().lower()
    if family not in STRATEGY_FAMILIES:
        raise ValueError("strategy_family must be all, breakout, breakout_r, breakout_rev, or breakout_r_rev")
    return family


def normalize_model_limit(value: int | str | None) -> int:
    limit = int(value or 10)
    if limit not in (10, 20, 30):
        raise ValueError("limit must be 10, 20, or 30")
    return limit


_LIVE_DAY_CACHE: dict[tuple, tuple[float, dict]] = {}
LIVE_DAY_CACHE_SECONDS = 30
HISTORICAL_CACHE_SECONDS = 6 * 60 * 60
_PORTFOLIO_DAY_CACHE: dict[tuple, tuple[float, dict]] = {}


def _cache_seconds(date_str: str) -> int:
    """Keep immutable historical results hot while refreshing today's data."""
    return LIVE_DAY_CACHE_SECONDS if date_str == dt.date.today().isoformat() else HISTORICAL_CACHE_SECONDS


def build_live_day(date_str: str, product_type: str = "all", product: str = "all",
                   strategy_family_filter: str = "all", limit: int = 10,
                   requested_scenario: str | None = None) -> dict:
    product_type = normalize_product_type(product_type)
    product = normalize_product(product)
    strategy_family_filter = normalize_strategy_family(strategy_family_filter)
    limit = normalize_model_limit(limit)
    requested_scenario = str(requested_scenario or "").strip() or None
    if requested_scenario and not re.fullmatch(r"[A-Za-z0-9_.-]+", requested_scenario):
        raise ValueError("scenario contains unsupported characters")
    cache_key = (date_str, product_type, product, strategy_family_filter, limit, requested_scenario)
    cached = _LIVE_DAY_CACHE.get(cache_key)
    cache_seconds = _cache_seconds(date_str)
    if cached and time.monotonic() - cached[0] < cache_seconds:
        return cached[1]
    with _connect() as conn, conn.cursor() as cur:
        cur.execute(PRODUCTS_SQL, (product_type, product_type))
        products = [r[0] for r in cur.fetchall()]
        if product != "all" and product not in products:
            raise ValueError(f"product {product!r} is not available for type {product_type!r}")
        cur.execute(STATS_SQL, (date_str, product_type, product_type, product, product))
        stats = [dict(zip(STAT_COLS, r)) for r in cur.fetchall()]
        for s in stats:
            for k in ("net", "alt", "win_rate", "alt_win_rate", "target_profit"):
                s[k] = _f(s[k])
        product_stats = list(stats)
        if strategy_family_filter != "all":
            stats = [s for s in stats if strategy_family(s["strategy"]) == strategy_family_filter]

        tp_sl_pairs = sorted({pair for stat in stats if (pair := strategy_tp_sl(stat.get("strategy")))})
        touched_rank_one_ids: set[str] = set()
        all_model_ids = [s["model"] for s in stats]
        if all_model_ids and (requested_scenario is None or requested_scenario == "touched_rank_one"):
            cur.execute(TOUCHED_RANK_ONE_SQL, (date_str, all_model_ids))
            touched_rank_one_ids = {row[0] for row in cur.fetchall()}
        buy_sell_rank: list[str] = []
        if all_model_ids and (requested_scenario is None or requested_scenario == "top_buy_sell_net"):
            cur.execute(LAST_SNAP_SIDE_SQL, (all_model_ids, date_str, date_str))
            best_side = sorted(
                ((row[0], max(_f(row[1]), _f(row[2]))) for row in cur.fetchall()),
                key=lambda r: -r[1],
            )
            buy_sell_rank = [model for model, _ in best_side]

        if requested_scenario:
            selection_snaps: dict[str, list[dict]] = {}
            if requested_scenario == "weakening_selection":
                seed_ids = {s["model"] for s in sorted(
                    stats, key=lambda s: (-s["net"], -s["win_rate"], s["model"])
                )[:limit]}
                seed_ids |= {s["model"] for s in sorted((s for s in stats if s["win_rate"] >= 50),
                                                        key=lambda s: (-s["win_rate"], -s["net"], s["model"]))[:limit]}
                if seed_ids:
                    cur.execute(SNAP_SQL, (date_str, sorted(seed_ids)))
                    for m, tm, net, buy, sell, a_net, a_buy, a_sell, op, tr in cur.fetchall():
                        selection_snaps.setdefault(m, []).append({
                            "time": tm, "net": _f(net), "buy": _f(buy), "sell": _f(sell),
                            "alt_net": _f(a_net), "alt_buy": _f(a_buy), "alt_sell": _f(a_sell),
                            "open": int(op or 0), "trades": int(tr or 0),
                        })
            scenario_lists = _scenario_ids(
                stats, selection_snaps, limit, touched_rank_one_ids, product_stats, buy_sell_rank
            )
            requested_ids = scenario_lists.get(requested_scenario, scenario_lists["top_net"])
            scenario_lists = {requested_scenario: requested_ids}
            candidates = set(requested_ids)
        else:
            # Full payload is retained for compatibility with offline/export callers.
            candidates = {s["model"] for s in sorted(stats, key=lambda s: -s["net"])[:limit]}
            candidates |= {s["model"] for s in sorted(stats, key=lambda s: -s["alt"])[:limit]}
            candidates |= {s["model"] for s in sorted((s for s in stats if s["win_rate"] >= 50),
                                                      key=lambda s: (-s["win_rate"], -s["net"], s["model"]))[:limit]}
            candidates |= {s["model"] for s in _family_leaders(stats, "net")}
            candidates |= {s["model"] for s in _family_leaders(stats, "alt")}
            for family in ("breakout", "breakout_r", "breakout_rev", "breakout_r_rev"):
                candidates |= {s["model"] for s in _top_family(product_stats, family, "net")}
                candidates |= {s["model"] for s in _top_family(product_stats, family, "alt")}
            for tp, sl in tp_sl_pairs:
                candidates |= {s["model"] for s in _top_tp_sl(stats, tp, sl, "net")}
                candidates |= {s["model"] for s in _top_tp_sl(stats, tp, sl, "alt")}
            candidates |= touched_rank_one_ids
            candidates |= set(buy_sell_rank[:limit])
            scenario_lists = None
        snaps: dict[str, list[dict]] = {}
        if candidates:
            cur.execute(SNAP_SQL, (date_str, sorted(candidates)))
            for m, tm, net, buy, sell, a_net, a_buy, a_sell, op, tr in cur.fetchall():
                snaps.setdefault(m, []).append({
                    "time": tm, "net": _f(net), "buy": _f(buy), "sell": _f(sell),
                    "alt_net": _f(a_net), "alt_buy": _f(a_buy), "alt_sell": _f(a_sell),
                    "open": int(op or 0), "trades": int(tr or 0),
                })

    by_model = {s["model"]: s for s in product_stats}

    def model_list(ids: list[str]) -> list[dict]:
        out = []
        for rank, m in enumerate(ids, start=1):
            s = by_model[m]
            series = snaps.get(m) or [{
                "time": "02:00", "net": s["net"], "buy": 0.0, "sell": s["net"],
                "alt_net": s["alt"], "alt_buy": 0.0, "alt_sell": s["alt"],
                "open": 0, "trades": int(s["trades"]),
            }]
            last = series[-1]
            out.append({
                "rank": rank, "model": m, "product": s["product"] or "GBP",
                "product_type": s["product_type"] or "forex",
                "strategy": s["strategy"] or "breakout_strategy",
                "color": COLORS[(rank - 1) % len(COLORS)],
                "trades": int(s["trades"]), "wins": int(s["wins"]), "losses": int(s["losses"]),
                "win_rate": s["win_rate"], "alt_wins": int(s["alt_wins"]), "alt_win_rate": s["alt_win_rate"],
                "cum_net": last["net"], "buy_net": last["buy"], "sell_net": last["sell"],
                "cum_alt_net": last["alt_net"], "buy_alt_net": last["alt_buy"],
                "sell_alt_net": last["alt_sell"], "series": series,
            })
        return out

    payload = {"date": date_str, "product_type": product_type, "product": product,
               "strategy_family": strategy_family_filter, "limit": limit,
               "products": products,
               "tp_sl_scenarios": [
                   {"id": f"top3_tp{tp}_sl{sl}", "tp": tp, "sl": sl}
                   for tp, sl in tp_sl_pairs
               ],
               "generated_at": dt.datetime.now().isoformat(timespec="seconds")}
    if scenario_lists is None:
        scenario_lists = _scenario_ids(stats, snaps, limit, touched_rank_one_ids, product_stats, buy_sell_rank)
    for sc, ids in scenario_lists.items():
        payload[sc] = model_list(ids)
    _LIVE_DAY_CACHE[cache_key] = (time.monotonic(), payload)
    if len(_LIVE_DAY_CACHE) > 64:
        cutoff = time.monotonic() - HISTORICAL_CACHE_SECONDS
        for key, value in list(_LIVE_DAY_CACHE.items()):
            if value[0] < cutoff:
                _LIVE_DAY_CACHE.pop(key, None)
    return payload


def build_portfolio_day(date_str: str, model_ids: list[str]) -> dict:
    clean_ids = list(dict.fromkeys(str(m).strip() for m in model_ids if str(m).strip()))
    if not clean_ids or len(clean_ids) > 10:
        raise ValueError("portfolio requires between 1 and 10 unique models")
    if any(not re.fullmatch(r"[A-Za-z0-9._-]+", model) for model in clean_ids):
        raise ValueError("portfolio contains an invalid model id")

    cache_key = (date_str, tuple(clean_ids))
    cached = _PORTFOLIO_DAY_CACHE.get(cache_key)
    cache_seconds = _cache_seconds(date_str)
    if cached and time.monotonic() - cached[0] < cache_seconds:
        return cached[1]

    with _connect() as conn, conn.cursor() as cur:
        cur.execute(PORTFOLIO_STATS_SQL, (date_str, "all", "all", "all", "all", clean_ids))
        stats = [dict(zip(STAT_COLS, row)) for row in cur.fetchall()]
        stats = [s for s in stats if s["model"] in clean_ids]
        for stat in stats:
            for key in ("net", "alt", "win_rate", "alt_win_rate", "target_profit"):
                stat[key] = _f(stat[key])
        cur.execute(SNAP_SQL, (date_str, clean_ids))
        snaps: dict[str, list[dict]] = {}
        for model, tm, net, buy, sell, a_net, a_buy, a_sell, op, trades in cur.fetchall():
            snaps.setdefault(model, []).append({
                "time": tm, "net": _f(net), "buy": _f(buy), "sell": _f(sell),
                "alt_net": _f(a_net), "alt_buy": _f(a_buy), "alt_sell": _f(a_sell),
                "open": int(op or 0), "trades": int(trades or 0),
            })

    by_model = {s["model"]: s for s in stats}
    models = []
    for rank, model in enumerate(clean_ids, start=1):
        stat = by_model.get(model)
        if not stat:
            continue
        series = snaps.get(model) or [{
            "time": "02:00", "net": stat["net"], "buy": 0.0, "sell": stat["net"],
            "alt_net": stat["alt"], "alt_buy": 0.0, "alt_sell": stat["alt"],
            "open": 0, "trades": int(stat["trades"]),
        }]
        last = series[-1]
        models.append({
            "rank": rank, "model": model, "product": stat["product"] or "GBP",
            "product_type": stat["product_type"] or "forex",
            "strategy": stat["strategy"] or "breakout_strategy",
            "color": COLORS[(rank - 1) % len(COLORS)],
            "trades": int(stat["trades"]), "wins": int(stat["wins"]), "losses": int(stat["losses"]),
            "win_rate": stat["win_rate"], "alt_wins": int(stat["alt_wins"]), "alt_win_rate": stat["alt_win_rate"],
            "cum_net": last["net"], "buy_net": last["buy"], "sell_net": last["sell"],
            "cum_alt_net": last["alt_net"], "buy_alt_net": last["alt_buy"],
            "sell_alt_net": last["alt_sell"], "series": series,
        })
    payload = {"date": date_str, "requested_models": clean_ids, "models": models,
               "generated_at": dt.datetime.now().isoformat(timespec="seconds")}
    _PORTFOLIO_DAY_CACHE[cache_key] = (time.monotonic(), payload)
    if len(_PORTFOLIO_DAY_CACHE) > 128:
        cutoff = time.monotonic() - HISTORICAL_CACHE_SECONDS
        for key, value in list(_PORTFOLIO_DAY_CACHE.items()):
            if value[0] < cutoff:
                _PORTFOLIO_DAY_CACHE.pop(key, None)
    return payload


def select_live_day_scenario(payload: dict, scenario: str | None) -> dict:
    """Return one scenario from a full day payload to minimize JSON serialization and transfer."""
    scenario = str(scenario or "").strip()
    if not scenario:
        return payload
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", scenario):
        raise ValueError("scenario contains unsupported characters")
    selected = {
        key: payload[key]
        for key in ("date", "product_type", "product", "strategy_family", "limit",
                    "products", "tp_sl_scenarios", "generated_at")
        if key in payload
    }
    selected[scenario] = payload.get(scenario, payload.get("top_net", []))
    return selected


def build_similar_strategies(date_str: str, model_id: str) -> dict:
    """Return same-product comparison sets that vary one strategy dimension only."""
    model_id = str(model_id or "").strip()
    if not re.fullmatch(r"[A-Za-z0-9._-]+", model_id):
        raise ValueError("model contains unsupported characters")
    with _connect() as conn, conn.cursor() as cur:
        cur.execute(STATS_SQL, (date_str, "all", "all", "all", "all"))
        stats = [dict(zip(STAT_COLS, row)) for row in cur.fetchall()]
    reference = next((stat for stat in stats if stat["model"] == model_id), None)
    if not reference:
        raise ValueError(f"model {model_id!r} has no trades on {date_str}")
    reference_shape = strategy_shape(reference.get("strategy"))
    if not reference_shape:
        raise ValueError(f"strategy {reference.get('strategy')!r} is not a supported family/window/TP/SL strategy")

    same_product = [
        stat for stat in stats
        if (stat.get("product") or "").strip().lower() == (reference.get("product") or "").strip().lower()
        and (stat.get("product_type") or "").strip().lower() == (reference.get("product_type") or "").strip().lower()
        and strategy_shape(stat.get("strategy"))
    ]
    dimensions = ("family", "window", "tp", "sl")
    family_order = {name: index for index, name in enumerate(("breakout", "breakout_r", "breakout_rev", "breakout_r_rev"))}
    groups: dict[str, list[dict]] = {}
    for dimension in dimensions:
        fixed_dimensions = [name for name in dimensions if name != dimension]
        matches = [
            stat for stat in same_product
            if all(strategy_shape(stat["strategy"])[name] == reference_shape[name] for name in fixed_dimensions)
        ]
        matches.sort(key=lambda stat: (
            family_order.get(strategy_shape(stat["strategy"])[dimension], 99)
            if dimension == "family" else (strategy_shape(stat["strategy"])[dimension] if strategy_shape(stat["strategy"])[dimension] is not None else -1),
            stat["model"],
        ))
        groups[dimension] = [
            {
                "model": stat["model"],
                "product": stat["product"],
                "product_type": stat["product_type"],
                "strategy": stat["strategy"],
                "value": strategy_shape(stat["strategy"])[dimension],
            }
            for stat in matches[:10]
        ]
    return {
        "date": date_str,
        "reference": {
            "model": reference["model"], "product": reference["product"],
            "product_type": reference["product_type"], "strategy": reference["strategy"],
            **reference_shape,
        },
        "groups": groups,
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
    }


def build_strategy_catalog(date_str: str) -> dict:
    """Return active models and parsed strategy dimensions for portfolio selection."""
    with _connect() as conn, conn.cursor() as cur:
        cur.execute(STATS_SQL, (date_str, "all", "all", "all", "all"))
        stats = [dict(zip(STAT_COLS, row)) for row in cur.fetchall()]
    models = []
    for stat in stats:
        shape = strategy_shape(stat.get("strategy"))
        if not shape:
            continue
        models.append({
            "model": stat["model"],
            "product": (stat.get("product") or "").strip().lower(),
            "product_type": (stat.get("product_type") or "").strip().lower(),
            "strategy": stat["strategy"],
            "net": _f(stat.get("net")),
            "alt": _f(stat.get("alt")),
            **shape,
        })
    family_order = {name: index for index, name in enumerate(("breakout", "breakout_r", "breakout_rev", "breakout_r_rev"))}
    models.sort(key=lambda item: (
        item["product_type"], item["product"], family_order.get(item["family"], 99),
        item["window"] if item["window"] is not None else -1, item["tp"], item["sl"], item["model"],
    ))
    return {"date": date_str, "models": models, "generated_at": dt.datetime.now().isoformat(timespec="seconds")}


TRADES_CLOSED_SQL = """
    SELECT 'closed', to_char(created, 'YYYY-MM-DD HH24:MI:SS'), to_char(last_update, 'YYYY-MM-DD HH24:MI:SS'),
           TRIM(signal), TRIM(product), entry_price, latest_price, trade_quantity,
           net_return, alt_net_return, min_net_return, max_net_return,
           TRIM(close_type), TRIM(trade_reason), TRIM(strategy_name), target_profit, target_loss
    FROM combined_trades_closed
    WHERE model = %s AND created::date BETWEEN %s AND %s
    ORDER BY created;
"""

TRADES_OPEN_SQL = """
    SELECT 'open', to_char(created, 'YYYY-MM-DD HH24:MI:SS'), to_char(last_update, 'YYYY-MM-DD HH24:MI:SS'),
           TRIM(signal), TRIM(product), entry_price, latest_price, trade_quantity,
           net_return, alt_net_return, min_net_return, max_net_return,
           NULL, TRIM(trade_reason), TRIM(strategy_name), target_profit, target_loss
    FROM combined_trades_open
    WHERE TRIM(model) = %s AND created::date BETWEEN %s AND %s
    ORDER BY created;
"""

TRADE_COLS = [
    "status", "opened", "last_update", "signal", "product", "entry_price", "latest_price",
    "quantity", "net_return", "alt_net_return", "min_net_return", "max_net_return",
    "close_type", "trade_reason", "strategy", "target_profit", "target_loss",
]


def build_model_trades(model: str, date_from: str, date_to: str, product_type: str = "all", product: str = "all") -> dict:
    product_type = normalize_product_type(product_type)
    product = normalize_product(product)
    with _connect() as conn, conn.cursor() as cur:
        rows = []
        for sql in (TRADES_OPEN_SQL, TRADES_CLOSED_SQL):
            cur.execute(sql.replace("ORDER BY created;", "AND (%s = 'all' OR LOWER(TRIM(product_type)) = %s) AND (%s = 'all' OR LOWER(TRIM(product)) = %s) ORDER BY created;"),
                        (model, date_from, date_to, product_type, product_type, product, product))
            rows += cur.fetchall()
        # Canonical model definition: {script}_{window}_tp{tp}_sl{sl} plus params, e.g. breakout_2_tp5_sl20
        cur.execute(
            "SELECT TRIM(strategy_name), TRIM(strategy_params) FROM product_forex WHERE TRIM(model) = %s AND (%s = 'all' OR LOWER(TRIM(product_type)) = %s) AND (%s = 'all' OR LOWER(TRIM(product)) = %s) LIMIT 1",
            (model, product_type, product_type, product, product),
        )
        pf = cur.fetchone() or (None, None)
    trades = []
    for r in rows:
        t = dict(zip(TRADE_COLS, r))
        for k in ("entry_price", "latest_price", "quantity", "net_return",
                  "alt_net_return", "min_net_return", "max_net_return",
                  "target_profit", "target_loss"):
            t[k] = float(t[k]) if t[k] is not None else None
        trades.append(t)
    return {
        "model": model, "from": date_from, "to": date_to, "product_type": product_type, "product": product,
        "strategy_name": pf[0], "strategy_params": pf[1], "trades": trades,
    }


def build_hourly_family_report(date_str: str, product_type: str = "all",
                               product: str = "all", family: str = "all",
                               interval_minutes: int = 60) -> dict:
    """Return uncached time-bucketed entries, exits, and point-in-time open exposure."""
    product_type = normalize_product_type(product_type)
    product = normalize_product(product)
    family = normalize_strategy_family(family)
    if interval_minutes not in (10, 30, 60, 180):
        raise ValueError("interval_minutes must be 10, 30, 60, or 180")
    day = dt.date.fromisoformat(date_str)
    family_pattern = {
        "all": r"^(breakout(_r_rev|_rev|_r)?_[0-9]+|dna3_crypto)_tp[0-9]+_sl[0-9]+$",
        "breakout": r"^breakout_[0-9]+_tp[0-9]+_sl[0-9]+$",
        "breakout_r": r"^breakout_r_[0-9]+_tp[0-9]+_sl[0-9]+$",
        "breakout_rev": r"^breakout_rev_[0-9]+_tp[0-9]+_sl[0-9]+$",
        "breakout_r_rev": r"^breakout_r_rev_[0-9]+_tp[0-9]+_sl[0-9]+$",
    }[family]
    scope_sql = """
      AND (%s = 'all' OR LOWER(BTRIM(t.product_type)) = %s)
      AND (%s = 'all' OR LOWER(BTRIM(t.product)) = %s)
      AND LOWER(
            CASE
              WHEN BTRIM(t.strategy_name) ~* '^dna3_crypto_tp[0-9]+_sl[0-9]+$'
                THEN regexp_replace(BTRIM(t.strategy_name), '^dna3_crypto_', 'breakout_3_', 'i')
              ELSE COALESCE(BTRIM(t.strategy_name), '')
            END
          ) ~ %s
    """
    with _connect() as conn, conn.cursor() as cur:
        cur.execute(
            """SELECT DISTINCT LOWER(BTRIM(product))
                 FROM product_forex
                WHERE product IS NOT NULL
                  AND (%s = 'all' OR LOWER(BTRIM(product_type)) = %s)
                ORDER BY 1""",
            (product_type, product_type),
        )
        products = [row[0] for row in cur.fetchall()]
        params = (product_type, product_type, product, product, family_pattern)
        cur.execute(
            """SELECT t.created, t.last_update, UPPER(BTRIM(t.signal)),
                      t.net_return, t.alt_net_return
                 FROM combined_trades_closed t
                WHERE t.created < %s::date + INTERVAL '1 day'
                  AND t.last_update >= %s::date
            """ + scope_sql,
            (date_str, date_str, *params),
        )
        trades = [
            {"opened": opened, "closed": closed, "side": side,
             "net": _f(net), "alt": _f(alt)}
            for opened, closed, side, net, alt in cur.fetchall()
        ]
        cur.execute(
            """SELECT t.created, NULL, UPPER(BTRIM(t.signal)),
                      t.net_return, t.alt_net_return
                 FROM combined_trades_open t
                WHERE t.created < %s::date + INTERVAL '1 day'
            """ + scope_sql,
            (date_str, *params),
        )
        trades.extend(
            {"opened": opened, "closed": None, "side": side,
             "net": _f(net), "alt": _f(alt)}
            for opened, _, side, net, alt in cur.fetchall()
        )

    now = dt.datetime.now()
    is_today = day == now.date()
    day_start = dt.datetime.combine(day, dt.time.min)
    current_bucket = (
        day_start + dt.timedelta(
            minutes=((now.hour * 60 + now.minute) // interval_minutes) * interval_minutes
        )
        if is_today else None
    )
    rows = []
    totals = {"opened_trades": 0, "closed_trades": 0, "net_profit_count": 0, "alt_profit_count": 0,
              "total_net": 0.0, "total_alt_net": 0.0}
    bucket_count = (
        int((current_bucket - day_start).total_seconds() // (interval_minutes * 60)) + 1
        if current_bucket else 1440 // interval_minutes
    )
    for bucket_number in range(bucket_count):
        hour_start = day_start + dt.timedelta(minutes=bucket_number * interval_minutes)
        hour_end = hour_start + dt.timedelta(minutes=interval_minutes)
        checkpoint = now if current_bucket and hour_start == current_bucket else hour_end
        for side in ("BUY", "SELL"):
            side_trades = [trade for trade in trades if trade["side"] == side]
            opened = sum(hour_start <= trade["opened"] < checkpoint for trade in side_trades)
            closed = [trade for trade in side_trades if trade["closed"] and hour_start <= trade["closed"] < checkpoint]
            open_at_end = sum(
                trade["opened"] < checkpoint and (trade["closed"] is None or trade["closed"] >= checkpoint)
                for trade in side_trades
            )
            if not (opened or closed or open_at_end or (current_bucket and hour_start == current_bucket)):
                continue
            total_net = sum(trade["net"] for trade in closed)
            total_alt = sum(trade["alt"] for trade in closed)
            row = {
                "exit_hour": hour_start.strftime("%H:%M"), "side": side,
                "opened_trades": opened, "open_at_hour_end": open_at_end,
                "closed_trades": len(closed),
                "net_profit_count": sum(trade["net"] > 0 for trade in closed),
                "alt_profit_count": sum(trade["alt"] > 0 for trade in closed),
                "avg_net": total_net / len(closed) if closed else 0.0,
                "avg_alt_net": total_alt / len(closed) if closed else 0.0,
                "total_net": total_net, "total_alt_net": total_alt,
                "is_incomplete_hour": bool(current_bucket and hour_start == current_bucket),
            }
            rows.append(row)
            totals["opened_trades"] += opened
            for key in ("closed_trades", "net_profit_count", "alt_profit_count"):
                totals[key] += row[key]
            totals["total_net"] += total_net
            totals["total_alt_net"] += total_alt
    live_open = {side: sum(trade["side"] == side and trade["closed"] is None for trade in trades)
                 for side in ("BUY", "SELL")}
    totals.update({"open_buy": live_open["BUY"], "open_sell": live_open["SELL"]})
    return {
        "date": date_str, "product_type": product_type, "product": product,
        "family": family, "products": products, "rows": rows, "summary": totals,
        "is_today": is_today,
        "current_hour": current_bucket.strftime("%H:%M") if current_bucket else None,
        "interval_minutes": interval_minutes,
        "generated_at": now.isoformat(timespec="seconds"),
    }


TRADE_LOG_SQL = """
    SELECT * FROM (
    (SELECT 'open' AS status, TRIM(model) AS model, TRIM(strategy_name) AS strategy, TRIM(signal) AS side, trade_quantity AS qty,
            UPPER(TRIM(product)) AS product, entry_price, TRIM(product_type) AS ptype, created,
            NULL::timestamp AS closed_at, NULL::text AS close_type, NULL::numeric AS exit_price, NULL::numeric AS net
     FROM combined_trades_open WHERE (%(t)s = 'all' OR TRIM(product_type) = %(t)s)
       AND (%(m)s = '' OR model ILIKE '%%' || %(m)s || '%%') AND (%(s)s = '' OR strategy_name ILIKE '%%' || %(s)s || '%%')
       AND (%(p)s = '' OR UPPER(TRIM(product)) = UPPER(%(p)s)) AND (%(g)s = '' OR TRIM(signal) = %(g)s)
     ORDER BY created DESC LIMIT %(n)s)
    UNION ALL
    (SELECT 'closed', TRIM(model), TRIM(strategy_name), TRIM(signal), trade_quantity, UPPER(TRIM(product)),
            entry_price, TRIM(product_type), created, last_update, TRIM(close_type), latest_price, net_return
     FROM combined_trades_closed WHERE created >= CURRENT_DATE - 1 AND (%(t)s = 'all' OR TRIM(product_type) = %(t)s)
       AND (%(m)s = '' OR model ILIKE '%%' || %(m)s || '%%') AND (%(s)s = '' OR strategy_name ILIKE '%%' || %(s)s || '%%')
       AND (%(p)s = '' OR UPPER(TRIM(product)) = UPPER(%(p)s)) AND (%(g)s = '' OR TRIM(signal) = %(g)s)
     ORDER BY last_update DESC LIMIT %(n)s)
    ) x
    ORDER BY CASE WHEN status = 'closed' THEN closed_at ELSE created END DESC LIMIT %(n)s;
"""
TRADE_LOG_COLS = ["status", "model", "strategy", "side", "quantity", "product", "entry_price", "product_type",
                  "created", "closed_at", "close_type", "exit_price", "net_return"]


_TRADE_LOG_CACHE: dict[tuple, tuple[float, dict]] = {}


def build_trade_log(product_type: str = "all", limit: int = 50, model: str = "", strategy: str = "", product: str = "", signal: str = "") -> dict:
    if product_type not in ("all", "forex", "crypto"):
        raise ValueError("type must be all, forex or crypto")
    limit = max(1, min(limit, 200))
    signal = signal.strip().lower()
    if signal not in ("", "buy", "sell"):
        raise ValueError("signal must be buy or sell")
    params = {"t": product_type, "n": limit, "m": model.strip()[:60], "s": strategy.strip()[:60], "p": product.strip()[:30], "g": signal}
    key = (product_type, limit, params["m"], params["s"], params["p"], signal)
    hit = _TRADE_LOG_CACHE.get(key)
    if hit and time.monotonic() - hit[0] < 8:  # combined_trades_open is bloated (~3GB, seq scan ~4s); don't pile up polls
        return hit[1]
    with _connect() as conn, conn.cursor() as cur:
        cur.execute(TRADE_LOG_SQL, params)
        rows = []
        for r in cur.fetchall():
            row = dict(zip(TRADE_LOG_COLS, r))
            for k in ("created", "closed_at"):
                row[k] = row[k].strftime("%Y-%m-%d %H:%M:%S") if row[k] else None
            for k in ("quantity", "entry_price", "exit_price", "net_return"):
                row[k] = float(row[k]) if row[k] is not None else None
            rows.append(row)
    payload = {"type": product_type, "rows": rows, "generated_at": dt.datetime.now().isoformat(timespec="seconds")}
    _TRADE_LOG_CACHE[key] = (time.monotonic(), payload)
    return payload


def build_trade_log_products(product_type: str = "all") -> dict:
    if product_type not in ("all", "forex", "crypto"):
        raise ValueError("type must be all, forex or crypto")
    with _connect() as conn, conn.cursor() as cur:
        cur.execute("SELECT DISTINCT UPPER(TRIM(product)) FROM product_forex WHERE %s = 'all' OR TRIM(product_type) = %s ORDER BY 1",
                    (product_type, product_type))
        return {"products": [r[0] for r in cur.fetchall() if r[0]]}


DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        url = urlparse(self.path)
        if url.path == "/api/hourly_family_report":
            q = parse_qs(url.query)
            report_date = q.get("date", [dt.date.today().isoformat()])[0]
            if not DATE_RE.fullmatch(report_date):
                return self._json(400, {"error": "date must be YYYY-MM-DD"})
            try:
                return self._json(200, build_hourly_family_report(
                    report_date,
                    q.get("product_type", ["all"])[0],
                    q.get("product", ["all"])[0],
                    q.get("family", ["all"])[0],
                    int(q.get("interval_minutes", ["60"])[0]),
                ))
            except (ValueError, TypeError) as exc:
                return self._json(400, {"error": str(exc)})
            except Exception as exc:
                return self._json(500, {"error": str(exc)})
        if url.path == "/trading_log.html":
            body = (HERE.parents[1] / "ep_063_Trading_log" / "trading_log.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            return self.wfile.write(body)
        if url.path == "/api/trade_log_products":
            try:
                return self._json(200, build_trade_log_products(parse_qs(url.query).get("type", ["all"])[0]))
            except ValueError as exc:
                return self._json(400, {"error": str(exc)})
            except Exception as exc:
                return self._json(500, {"error": str(exc)})
        if url.path == "/api/trade_log":
            q = parse_qs(url.query)
            try:
                return self._json(200, build_trade_log(
                    q.get("type", ["all"])[0], int(q.get("limit", ["50"])[0]), q.get("model", [""])[0],
                    q.get("strategy", [""])[0], q.get("product", [""])[0], q.get("signal", [""])[0]))
            except (ValueError, TypeError) as exc:
                return self._json(400, {"error": str(exc)})
            except Exception as exc:
                return self._json(500, {"error": str(exc)})
        if url.path == "/api/model_trades":
            q = parse_qs(url.query)
            model = q.get("model", [""])[0]
            d_from = q.get("from", [""])[0]
            d_to = q.get("to", [d_from])[0]
            product_type = q.get("product_type", ["all"])[0]
            product = q.get("product", ["all"])[0]
            if not model or not DATE_RE.fullmatch(d_from) or not DATE_RE.fullmatch(d_to):
                return self._json(400, {"error": "model, from=YYYY-MM-DD [, to=YYYY-MM-DD] required"})
            try:
                return self._json(200, build_model_trades(model, d_from, d_to, product_type, product))
            except Exception as exc:
                return self._json(500, {"error": str(exc)})
        if url.path == "/api/point_in_time_scenario":
            q = parse_qs(url.query)
            pit_date = q.get("date", [dt.date.today().isoformat()])[0]
            if not DATE_RE.fullmatch(pit_date):
                return self._json(400, {"error": "date must be YYYY-MM-DD"})
            try:
                return self._json(200, build_point_in_time_scenario(
                    pit_date, q.get("at", [""])[0], q.get("scenario", ["top_net"])[0],
                    q.get("return_type", ["NET"])[0], q.get("product_type", ["all"])[0],
                    q.get("product", ["all"])[0], q.get("strategy_family", ["all"])[0],
                    q.get("limit", ["10"])[0], q.get("min_win_rate", ["0"])[0],
                ))
            except (ValueError, TypeError) as exc:
                return self._json(400, {"error": str(exc)})
            except Exception as exc:
                return self._json(500, {"error": str(exc)})
        if url.path == "/api/point_in_time_scenario_hours":
            q = parse_qs(url.query)
            hours_date = q.get("date", [dt.date.today().isoformat()])[0]
            if not DATE_RE.fullmatch(hours_date):
                return self._json(400, {"error": "date must be YYYY-MM-DD"})
            try:
                return self._json(200, build_point_in_time_scenario_hours(
                    hours_date, q.get("scenario", ["top_net"])[0],
                    q.get("return_type", ["NET"])[0], q.get("product_type", ["all"])[0],
                    q.get("product", ["all"])[0], q.get("strategy_family", ["all"])[0],
                    q.get("limit", ["10"])[0], q.get("min_win_rate", ["0"])[0],
                ))
            except (ValueError, TypeError) as exc:
                return self._json(400, {"error": str(exc)})
            except Exception as exc:
                return self._json(500, {"error": str(exc)})
        if url.path != "/api/live_day":
            if url.path == "/api/strategy_catalog":
                catalog_date = parse_qs(url.query).get("date", [dt.date.today().isoformat()])[0]
                if not DATE_RE.fullmatch(catalog_date):
                    return self._json(400, {"error": "date must be YYYY-MM-DD"})
                try:
                    return self._json(200, build_strategy_catalog(catalog_date))
                except Exception as exc:
                    return self._json(500, {"error": str(exc)})
            if url.path == "/api/similar_strategies":
                q = parse_qs(url.query)
                similar_date = q.get("date", [dt.date.today().isoformat()])[0]
                model = q.get("model", [""])[0]
                if not model or not DATE_RE.fullmatch(similar_date):
                    return self._json(400, {"error": "model and date=YYYY-MM-DD required"})
                try:
                    return self._json(200, build_similar_strategies(similar_date, model))
                except Exception as exc:
                    return self._json(500, {"error": str(exc)})
            if url.path == "/api/portfolio_day":
                q = parse_qs(url.query)
                portfolio_date = q.get("date", [dt.date.today().isoformat()])[0]
                models = q.get("models", [""])[0].split(",")
                if not DATE_RE.fullmatch(portfolio_date):
                    return self._json(400, {"error": "date must be YYYY-MM-DD"})
                try:
                    return self._json(200, build_portfolio_day(portfolio_date, models))
                except Exception as exc:
                    return self._json(500, {"error": str(exc)})
            return super().do_GET()
        q = parse_qs(url.query)
        date_str = q.get("date", [dt.date.today().isoformat()])[0]
        product_type = q.get("product_type", ["all"])[0]
        product = q.get("product", ["all"])[0]
        strategy_family_filter = q.get("strategy_family", ["all"])[0]
        limit = q.get("limit", ["10"])[0]
        scenario = q.get("scenario", [None])[0]
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
            return self._json(400, {"error": "date must be YYYY-MM-DD"})
        try:
            payload = build_live_day(
                date_str, product_type, product, strategy_family_filter, limit, scenario
            )
            self._json(200, select_live_day_scenario(payload, scenario))
        except Exception as exc:  # surface DB errors to the page status badge
            self._json(500, {"error": str(exc)})

    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", PORT), partial(Handler, directory=str(HERE)))
    print(f"EP057 top10 live server on http://localhost:{PORT}/top10_5min_equity_curves.html")
    server.serve_forever()
