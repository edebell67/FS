# epics/ep_057_sql_to_pgsql/cross_signal_prototype/serve_nocache.py — local web + API server for the cross-signal replay screen: capture data, live feed, saved results, product config
#
# VERSION HISTORY
# v1.5.1 · 2026-10-02 · Port comes from CROSS_PORT (default 8110) so the launcher can move to a free port.
# v1.5.0 · 2026-10-01 · Adds /api/product-config (per-product trade quantity store) for the config modal.
# v1.4.0 · 2026-10-01 · Adds the live recorder with the Z:\algo_forex\prices JSON fallback, /api/instruments, /api/live and adjustable sampling (/api/config), so live mode keeps working when the 8002 quotes API is down.
# v1.3.0 · 2026-10-01 · Adds /api/results (+ csv, delete) so strategy results can be saved for later review.
# v1.2.0 · 2026-10-01 · Adds /api/days and /api/ticks over the _price_capture.jsonl files (forex and crypto) so any date can be selected; redirects the old per-day page links.
# v1.0.0 · 2026-10-01 · Initial version: static file server with caching disabled so a rebuilt page always loads fresh.
r"""Serve this folder on 127.0.0.1:8110 (no caching) plus a small API used by cross_signal.html:
  GET /api/instruments                  -> {"instruments":[{"code","type"}], "sample_seconds"}  live codes (F = forex, C = crypto)
  GET /api/config?sample=5              -> set the live sampling interval in seconds (1..60) and return it
  GET /api/days?code=gbp                -> ["2026-09-21", ...]  capture days for that instrument's asset class
  GET /api/ticks?code=gbp&day=DATE      -> quote ticks from the _price_capture.jsonl file: [{t, iso, p, bid, ask}]
  GET /api/live?code=gbp&after=MS       -> live ticks recorded since server start with t > MS (bid/ask changes only)
  GET  /api/product-config              -> {code: {quantity, ..., updated_at}}  per-product trading configuration
  POST /api/product-config              -> {"code": "btc", "config": {...}} merge-saves it; "config": null removes the product
  POST /api/results                     -> append a saved strategy result (JSON body) to strategy_results.jsonl
  GET  /api/results                     -> all saved results;  GET /api/results.csv -> one summary row per result
  DELETE /api/results?id=ID             -> remove one saved result
Each feed (forex, crypto) tries the market-prices API first and falls back to the Z:\algo_forex\prices JSON files when the API
fails or is slow; the source in use is reported by /api/instruments ("sources").
A background thread polls the market-prices API (forex + crypto quotes) every SAMPLE_SECONDS (5 s, like the capture files) and keeps today's ticks in memory,
so a page opened mid-day can continue from the capture file without gaps. Paper trading / display only: nothing is traded."""
import json
import os
import re
import threading
import time
import urllib.request
from collections import defaultdict, deque
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "strategy_results.jsonl"
PRODUCT_CONFIG = HERE / "product_config.json"
BASE = Path("X:/EDS/TradeApps/breakout/fs/json/live")
ROOTS = {"F": BASE / "forex", "C": BASE / "crypto"}
FEEDS = {  # asset type -> (primary API, backup file)
    "F": ("http://127.0.0.1:8002/api/vw_000_fx_quotes", Path("Z:/algo_forex/prices/forex_prices.json")),
    "C": ("http://127.0.0.1:8002/api/vw_000_crypto_quotes", Path("Z:/algo_forex/prices/crypto_prices.json")),
}
API_TIMEOUT = 6.0  # a slower API response than this counts as a failure for that cycle -> use the backup file
CRYPTO = {"btc", "eth", "sol", "avax", "xrp", "ada", "doge"}  # fallback until the first poll tells us the types
_cache: dict = {}
SAMPLE_SECONDS = 5.0  # live sampling interval: matches the ~5 s spacing of the _price_capture.jsonl ticks the strategies are tested on

# ---------------- live recorder ----------------
_lock = threading.Lock()
_live: dict[str, deque] = defaultdict(lambda: deque(maxlen=200_000))
_types: dict[str, str] = {}
_last: dict[str, tuple] = {}
_status = {"at": 0.0, "err": "", "sources": {"F": "none", "C": "none"}}


def _api_rows(url: str) -> list[dict]:
    with urllib.request.urlopen(url, timeout=API_TIMEOUT) as r:
        rows = json.load(r).get("data", [])
    return [{"code": q["code"], "type": q.get("type", "F"), "bid": q.get("bid"), "ask": q.get("ask"),
             "ts": datetime.fromisoformat(q["timestamp"]), "stale": q.get("stale")} for q in rows]


def _file_rows(kind: str, path: Path) -> list[dict]:
    d = json.loads(path.read_text(encoding="utf-8"))
    ts = datetime.fromisoformat(d["timestamp"])
    sections = ("forex", "synthetic") if kind == "F" else ("crypto",)  # futures in the forex file are not recorded
    return [{"code": c, "type": kind, "bid": q.get("bid"), "ask": q.get("ask"), "ts": ts, "stale": False}
            for sec in sections for c, q in d.get(sec, {}).items()]


def _record(rows: list[dict]) -> None:
    for q in rows:
        if q.get("stale") or not q.get("bid") or q["bid"] <= 0 or q["ask"] < q["bid"]:
            continue
        code = q["code"].lower()
        key = (q["bid"], q["ask"])
        with _lock:
            _types[code] = q["type"]
            if _last.get(code) == key:
                continue
            _last[code] = key
            ts = q["ts"]
            _live[code].append({"t": int(ts.timestamp() * 1000), "iso": ts.strftime("%H:%M:%S"),
                                "p": [[(q["bid"] + q["ask"]) / 2, 1, "q"]], "bid": q["bid"], "ask": q["ask"]})


def _poll_once(kind: str) -> None:
    api, backup = FEEDS[kind]
    try:
        rows, src = _api_rows(api), "api"
        _status["err"] = ""
    except Exception as e:  # API down / slow -> backup file
        _status["err"] = f"{api}: {e}"
        try:
            rows, src = _file_rows(kind, backup), "file"
        except Exception as e2:
            _status["sources"][kind] = "none"
            _status["err"] += f" | backup {backup}: {e2}"
            return
    _status["sources"][kind] = src
    _status["at"] = time.time()
    _record(rows)


def _recorder(kind: str) -> None:
    """One thread per feed, so a slow response from one never delays the other."""
    while True:
        try:
            _poll_once(kind)
        except Exception as e:  # never let the thread die
            _status["err"] = str(e)
        time.sleep(SAMPLE_SECONDS)


def asset_of(code: str) -> str:
    return _types.get(code.lower()) or ("C" if code.lower() in CRYPTO else "F")


# ---------------- capture files ----------------
_days: dict = {}


def days(asset: str) -> list[str]:
    """Date folders (one listdir; globbing for the capture file in each is far too slow on the X: share). Cached 60s."""
    d = _days.get(asset)
    if not d or time.time() - d[0] > 60:
        d = (time.time(), sorted(n for n in os.listdir(ROOTS[asset]) if re.fullmatch(r"20\d\d-\d\d-\d\d", n)))
        _days[asset] = d
    return d[1]


def ticks(code: str, day: str) -> list[dict]:
    path = ROOTS[asset_of(code)] / day / "_price_capture.jsonl"
    st = path.stat()  # FileNotFoundError -> 404 in do_GET
    key = (code, day, st.st_mtime_ns, st.st_size)
    if key not in _cache:
        out = []
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except ValueError:  # last line may be mid-write
                    continue
                q = d.get(code.upper())
                if q and q["bid"] > 0 and q["ask"] >= q["bid"]:
                    ts = datetime.fromisoformat(d["ts"])
                    out.append({"t": int(ts.timestamp() * 1000), "iso": ts.strftime("%H:%M:%S"),
                                "p": [[(q["bid"] + q["ask"]) / 2, 1, "q"]], "bid": q["bid"], "ask": q["ask"]})
        _cache.clear()  # keep only the latest load
        _cache[key] = out
    return _cache[key]


# ---------------- per-product trading config ----------------
def load_product_config() -> dict:
    try:
        return json.loads(PRODUCT_CONFIG.read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        return {}


def save_product_config(code: str, cfg) -> dict:
    with _lock:
        all_cfg = load_product_config()
        if cfg is None:
            all_cfg.pop(code, None)
        else:
            all_cfg[code] = {**all_cfg.get(code, {}), **cfg, "updated_at": datetime.now().isoformat(timespec="seconds")}
        PRODUCT_CONFIG.write_text(json.dumps(all_cfg, indent=2), encoding="utf-8")
        return all_cfg


# ---------------- saved results ----------------
def load_results() -> list[dict]:
    if not RESULTS.exists():
        return []
    return [json.loads(line) for line in RESULTS.read_text(encoding="utf-8").splitlines() if line.strip()]


def results_csv(rows: list[dict]) -> str:
    cols = ["id", "saved_at", "day", "code", "strategy", "n", "mode", "minutes", "tp", "sl", "comm", "stop_at", "as_of", "trades",
            "win_pct", "total_pips", "alt_total_pips", "note"]
    lines = [",".join(cols)]
    for r in rows:
        v = {**r, **r.get("params", {}), **r.get("stats", {})}
        lines.append(",".join('"' + str(v.get(c, "")).replace('"', "'") + '"' for c in cols))
    return "\n".join(lines) + "\n"


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

    def _json(self, obj, code: int = 200) -> None:
        body = json.dumps(obj, separators=(",", ":")).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _redirect(self, to: str) -> None:
        self.send_response(302)
        self.send_header("Location", to)
        self.end_headers()

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/product-config":
            n = int(self.headers.get("Content-Length", 0))
            try:
                body = json.loads(self.rfile.read(n))
                code = str(body["code"]).lower()
                cfg = body.get("config")
                if not re.fullmatch(r"[a-z0-9_]{1,20}", code) or not (cfg is None or isinstance(cfg, dict)):
                    raise ValueError("bad config")
            except (ValueError, KeyError, TypeError):
                return self._json({"error": "bad request"}, 400)
            return self._json(save_product_config(code, cfg))
        if path != "/api/results":
            return self._json({"error": "not found"}, 404)
        n = int(self.headers.get("Content-Length", 0))
        if n <= 0 or n > 5_000_000:
            return self._json({"error": "bad size"}, 400)
        try:
            rec = json.loads(self.rfile.read(n))
        except ValueError:
            return self._json({"error": "bad json"}, 400)
        now = datetime.now()
        rec["id"] = now.strftime("%Y%m%d%H%M%S%f")
        rec["saved_at"] = now.isoformat(timespec="seconds")
        with RESULTS.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, separators=(",", ":")) + "\n")
        self._json({"ok": True, "id": rec["id"]})

    def do_DELETE(self) -> None:
        u = urlparse(self.path)
        if u.path != "/api/results":
            return self._json({"error": "not found"}, 404)
        rid = parse_qs(u.query).get("id", [""])[0]
        rows = [r for r in load_results() if r.get("id") != rid]
        RESULTS.write_text("".join(json.dumps(r, separators=(",", ":")) + "\n" for r in rows), encoding="utf-8")
        self._json({"ok": True, "left": len(rows)})

    def do_GET(self) -> None:
        global SAMPLE_SECONDS
        u = urlparse(self.path)
        q = parse_qs(u.query)
        m = re.fullmatch(r"/cross_signal_(\d{4})(\d{2})(\d{2})\.html", u.path)
        if m:  # old per-day page links -> the dynamic page opened on that date
            return self._redirect(f"/cross_signal.html?day={m[1]}-{m[2]}-{m[3]}")
        if u.path == "/":
            return self._redirect("/cross_signal.html")
        if u.path == "/api/product-config":
            return self._json(load_product_config())
        if u.path == "/api/instruments":
            with _lock:
                items = [{"code": c, "type": t} for c, t in sorted(_types.items(), key=lambda kv: (kv[1] != "F", kv[0]))]
            return self._json({"instruments": items, "feed_ok": time.time() - _status["at"] < 10, "error": _status["err"],
                               "sample_seconds": SAMPLE_SECONDS, "sources": _status["sources"]})
        if u.path == "/api/config":
            if "sample" in q:
                try:
                    SAMPLE_SECONDS = min(60.0, max(1.0, float(q["sample"][0])))
                except ValueError:
                    return self._json({"error": "bad sample"}, 400)
            return self._json({"sample_seconds": SAMPLE_SECONDS})
        if u.path == "/api/days":
            return self._json(days(asset_of(q.get("code", ["gbp"])[0])))
        if u.path == "/api/live":
            code, after = q.get("code", ["gbp"])[0].lower(), int(q.get("after", ["0"])[0] or 0)
            with _lock:
                out = [t for t in _live.get(code, ()) if t["t"] > after]
            return self._json(out)
        if u.path == "/api/ticks":
            code, day = q.get("code", ["gbp"])[0], q.get("day", [""])[0]
            if not re.fullmatch(r"20\d\d-\d\d-\d\d", day):
                return self._json({"error": "bad day"}, 400)
            try:
                return self._json(ticks(code, day))
            except FileNotFoundError:
                return self._json({"error": "no capture for that day"}, 404)
        if u.path == "/api/results":
            return self._json(load_results())
        if u.path == "/api/results.csv":
            body = results_csv(load_results()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/csv")
            self.send_header("Content-Disposition", "attachment; filename=strategy_results.csv")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()


if __name__ == "__main__":
    for kind in FEEDS:
        threading.Thread(target=_recorder, args=(kind,), daemon=True).start()
    ThreadingHTTPServer((os.environ.get("CROSS_HOST", "127.0.0.1"), int(os.environ.get("CROSS_PORT", "8110"))), Handler).serve_forever()
