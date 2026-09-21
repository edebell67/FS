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
    SELECT c.model,
           ROUND(SUM(c.net_return)::numeric, 2) AS total_net,
           ROUND(SUM(c.alt_net_return)::numeric, 2) AS total_alt_net,
           COUNT(*) AS total_trades,
           COUNT(*) FILTER (WHERE c.net_return > 0) AS wins,
           COUNT(*) FILTER (WHERE c.net_return <= 0) AS losses,
           ROUND((COUNT(*) FILTER (WHERE c.net_return > 0)::numeric / COUNT(*)::numeric * 100), 1) AS win_rate,
           COUNT(*) FILTER (WHERE c.alt_net_return > 0) AS alt_wins,
           ROUND((COUNT(*) FILTER (WHERE c.alt_net_return > 0)::numeric / COUNT(*)::numeric * 100), 1) AS alt_win_rate,
           MAX(TRIM(c.product)) AS product,
           COALESCE(MAX(TRIM(pf.strategy_name)), MAX(TRIM(c.strategy_name))) AS strategy,
           MAX(pf.target_profit) AS target_profit
    FROM combined_trades_closed c
    LEFT JOIN product_forex pf ON TRIM(pf.model) = c.model
    WHERE c.created::date = %s
    GROUP BY c.model;
"""

SNAP_SQL = """
    SELECT model,
           to_char(snapshot_timestamp, 'HH24:MI') AS time_str,
           ROUND(cum_net::numeric, 1), ROUND(cum_buy_net::numeric, 1), ROUND(cum_sell_net::numeric, 1),
           ROUND(cum_alt_net::numeric, 1), ROUND(cum_buy_alt_net::numeric, 1), ROUND(cum_sell_alt_net::numeric, 1),
           open_trade_count, closed_trade_count
    FROM tbl_dna_model_summary_snapshots_5min
    WHERE snapshot_timestamp::date = %s
      AND model = ANY(%s)
    ORDER BY snapshot_timestamp;
"""


def _f(v) -> float:
    return float(v) if v is not None else 0.0


def _connect():
    return psycopg2.connect(
        host=os.environ.get("PGHOST", "localhost"),
        port=int(os.environ.get("PGPORT", "5432")),
        dbname=os.environ.get("PGDATABASE", "tradedb"),
        user=os.environ.get("PGUSER", "postgres"),
        password=os.environ.get("PGPASSWORD"),
        connect_timeout=5,
    )


STAT_COLS = ["model", "net", "alt", "trades", "wins", "losses", "win_rate",
             "alt_wins", "alt_win_rate", "product", "strategy", "target_profit"]
MIN_SCENARIO_MODELS = 2  # fewer qualifying models -> scenario falls back to top_net


def _scenario_ids(stats: list[dict], snaps: dict[str, list[dict]]) -> dict[str, list[str]]:
    """Scenario model lists for one trading date.

    Rules reproduce the stored 14-18 Sep lists: each scenario filters the day's pool
    (Top 10 Net Return + Top 10 Win Rate) and falls back to Top 10 Net Return when fewer
    than MIN_SCENARIO_MODELS qualify. weakening_selection follows its catalogue text
    (high-volume pool models below their intraday peak) - the original rule is unknown.
    """
    by_net = sorted(stats, key=lambda s: (-s["net"], -s["win_rate"], s["model"]))
    top_net = by_net[:10]
    top_alt = sorted(stats, key=lambda s: (-s["alt"], s["model"]))[:10]
    top_win = sorted((s for s in stats if s["win_rate"] >= 50),
                     key=lambda s: (-s["win_rate"], -s["net"], s["model"]))[:10]
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

    def pick(models, limit=10):
        models = list(models)[:limit]
        return models if len(models) >= MIN_SCENARIO_MODELS else top_net

    lists = {
        "top_net": top_net,
        "top_alt_net": top_alt,
        "top_win": top_win or top_net,
        "strongest_three": sorted(pool, key=lambda s: -s["net"])[:3],
        "strengthening_cluster": pick(s for s in pool if (s["strategy"] or "").startswith("breakout_R_")),
        "relative_value": pick(sorted((s for s in pool if s["win_rate"] >= 85), key=lambda s: -s["win_rate"])),
        "market_move": pick(s for s in pool if tp_pips(s) >= 10),
        "opposite_cluster": pick(s for s in pool if 3 <= tp_pips(s) <= 5),
        "weakening_selection": pick(sorted((s for s in pool if drawdown(s) > 0),
                                           key=lambda s: (-s["trades"], -drawdown(s)))),
        "repair_negative": pick(s for s in pool if s["win_rate"] == 100 and s["net"] > 0),
    }
    lists["NET_RETURN"] = lists["top_net"]
    lists["WIN_RATE"] = lists["top_win"]
    return {k: [s["model"] for s in v] for k, v in lists.items()}


def build_live_day(date_str: str) -> dict:
    with _connect() as conn, conn.cursor() as cur:
        cur.execute(STATS_SQL, (date_str,))
        stats = [dict(zip(STAT_COLS, r)) for r in cur.fetchall()]
        for s in stats:
            for k in ("net", "alt", "win_rate", "alt_win_rate", "target_profit"):
                s[k] = _f(s[k])

        # Snapshots for every model that can appear in a scenario (top net / alt / win-rate pools)
        candidates = {s["model"] for s in sorted(stats, key=lambda s: -s["net"])[:10]}
        candidates |= {s["model"] for s in sorted(stats, key=lambda s: -s["alt"])[:10]}
        candidates |= {s["model"] for s in sorted((s for s in stats if s["win_rate"] >= 50),
                                                  key=lambda s: (-s["win_rate"], -s["net"], s["model"]))[:10]}
        snaps: dict[str, list[dict]] = {}
        if candidates:
            cur.execute(SNAP_SQL, (date_str, sorted(candidates)))
            for m, tm, net, buy, sell, a_net, a_buy, a_sell, op, tr in cur.fetchall():
                snaps.setdefault(m, []).append({
                    "time": tm, "net": _f(net), "buy": _f(buy), "sell": _f(sell),
                    "alt_net": _f(a_net), "alt_buy": _f(a_buy), "alt_sell": _f(a_sell),
                    "open": int(op or 0), "trades": int(tr or 0),
                })

    by_model = {s["model"]: s for s in stats}

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
                "strategy": s["strategy"] or "breakout_strategy",
                "color": COLORS[(rank - 1) % len(COLORS)],
                "trades": int(s["trades"]), "wins": int(s["wins"]), "losses": int(s["losses"]),
                "win_rate": s["win_rate"], "alt_wins": int(s["alt_wins"]), "alt_win_rate": s["alt_win_rate"],
                "cum_net": last["net"], "buy_net": last["buy"], "sell_net": last["sell"],
                "cum_alt_net": last["alt_net"], "buy_alt_net": last["alt_buy"],
                "sell_alt_net": last["alt_sell"], "series": series,
            })
        return out

    payload = {"date": date_str, "generated_at": dt.datetime.now().isoformat(timespec="seconds")}
    for sc, ids in _scenario_ids(stats, snaps).items():
        payload[sc] = model_list(ids)
    return payload


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


def build_model_trades(model: str, date_from: str, date_to: str) -> dict:
    with _connect() as conn, conn.cursor() as cur:
        rows = []
        for sql in (TRADES_OPEN_SQL, TRADES_CLOSED_SQL):
            cur.execute(sql, (model, date_from, date_to))
            rows += cur.fetchall()
        # Canonical model definition: {script}_{window}_tp{tp}_sl{sl} plus params, e.g. breakout_2_tp5_sl20
        cur.execute(
            "SELECT TRIM(strategy_name), TRIM(strategy_params) FROM product_forex WHERE TRIM(model) = %s LIMIT 1",
            (model,),
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
        "model": model, "from": date_from, "to": date_to,
        "strategy_name": pf[0], "strategy_params": pf[1], "trades": trades,
    }


DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        url = urlparse(self.path)
        if url.path == "/api/model_trades":
            q = parse_qs(url.query)
            model = q.get("model", [""])[0]
            d_from = q.get("from", [""])[0]
            d_to = q.get("to", [d_from])[0]
            if not model or not DATE_RE.fullmatch(d_from) or not DATE_RE.fullmatch(d_to):
                return self._json(400, {"error": "model, from=YYYY-MM-DD [, to=YYYY-MM-DD] required"})
            try:
                return self._json(200, build_model_trades(model, d_from, d_to))
            except Exception as exc:
                return self._json(500, {"error": str(exc)})
        if url.path != "/api/live_day":
            return super().do_GET()
        date_str = parse_qs(url.query).get("date", [dt.date.today().isoformat()])[0]
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
            return self._json(400, {"error": "date must be YYYY-MM-DD"})
        try:
            self._json(200, build_live_day(date_str))
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
