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

TOP_SQL = """
    SELECT model,
           ROUND(SUM(net_return)::numeric, 2) AS total_net,
           ROUND(SUM(alt_net_return)::numeric, 2) AS total_alt_net,
           COUNT(*) AS total_trades,
           COUNT(*) FILTER (WHERE net_return > 0) AS wins,
           COUNT(*) FILTER (WHERE net_return <= 0) AS losses,
           ROUND((COUNT(*) FILTER (WHERE net_return > 0)::numeric / COUNT(*)::numeric * 100), 1) AS win_rate,
           COUNT(*) FILTER (WHERE alt_net_return > 0) AS alt_wins,
           ROUND((COUNT(*) FILTER (WHERE alt_net_return > 0)::numeric / COUNT(*)::numeric * 100), 1) AS alt_win_rate,
           MAX(product) AS product,
           MAX(strategy_name) AS strategy
    FROM combined_trades_closed
    WHERE created::date = %s
    GROUP BY model
    ORDER BY {order} DESC
    LIMIT 10;
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


def build_live_day(date_str: str) -> dict:
    with _connect() as conn, conn.cursor() as cur:
        cur.execute(TOP_SQL.format(order="total_net"), (date_str,))
        top_net = cur.fetchall()
        cur.execute(TOP_SQL.format(order="total_alt_net"), (date_str,))
        top_alt = cur.fetchall()

        models = sorted({r[0] for r in top_net} | {r[0] for r in top_alt})
        snaps: dict[str, list[dict]] = {}
        if models:
            cur.execute(SNAP_SQL, (date_str, models))
            for m, tm, net, buy, sell, a_net, a_buy, a_sell, op, tr in cur.fetchall():
                snaps.setdefault(m, []).append({
                    "time": tm, "net": _f(net), "buy": _f(buy), "sell": _f(sell),
                    "alt_net": _f(a_net), "alt_buy": _f(a_buy), "alt_sell": _f(a_sell),
                    "open": int(op or 0), "trades": int(tr or 0),
                })

    def model_list(rows) -> list[dict]:
        out = []
        for rank, r in enumerate(rows, start=1):
            m, tot_net, tot_alt, tr, w, l, wr, alt_w, alt_wr, prod, strat = r
            series = snaps.get(m) or [{
                "time": "02:00", "net": _f(tot_net), "buy": 0.0, "sell": _f(tot_net),
                "alt_net": _f(tot_alt), "alt_buy": 0.0, "alt_sell": _f(tot_alt),
                "open": 0, "trades": int(tr),
            }]
            last = series[-1]
            out.append({
                "rank": rank, "model": m, "product": prod or "GBP",
                "strategy": strat or "breakout_strategy",
                "color": COLORS[(rank - 1) % len(COLORS)],
                "trades": int(tr), "wins": int(w), "losses": int(l),
                "win_rate": _f(wr), "alt_wins": int(alt_w), "alt_win_rate": _f(alt_wr),
                "cum_net": last["net"], "buy_net": last["buy"], "sell_net": last["sell"],
                "cum_alt_net": last["alt_net"], "buy_alt_net": last["alt_buy"],
                "sell_alt_net": last["alt_sell"], "series": series,
            })
        return out

    return {
        "date": date_str,
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "top_net": model_list(top_net),
        "top_alt_net": model_list(top_alt),
    }


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
    trades = []
    for r in rows:
        t = dict(zip(TRADE_COLS, r))
        for k in ("entry_price", "latest_price", "quantity", "net_return",
                  "alt_net_return", "min_net_return", "max_net_return",
                  "target_profit", "target_loss"):
            t[k] = float(t[k]) if t[k] is not None else None
        trades.append(t)
    return {"model": model, "from": date_from, "to": date_to, "trades": trades}


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
