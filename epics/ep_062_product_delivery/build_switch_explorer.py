"""Build the self-contained "Select. Compare. Switch." explorer.

Reads the five-minute model snapshots and closed positions from PostgreSQL, works out the selection,
comparison and switch cases for every decision hour using only data up to that hour, and writes ONE
html file with the data embedded. The output needs no server, no network and no other files: send it
to users and they open it by double-clicking.

    python build_switch_explorer.py                          # crypto + forex, each on its latest usable day
    python build_switch_explorer.py --product-type forex     # one asset class only
    python build_switch_explorer.py --date 2026-10-03 --product-type crypto --products avax,btc

The output name carries the build time (strategy-selection-to-switch-YYYYMMDD-HHMM.html) and the file
also holds the build time in a meta tag, an html comment and the visible header stamp. Crypto and forex
are built and shown separately: nothing is ever pooled across the two asset classes.

Connection: --dsn, or env SOURCE_DATABASE_URL, or the EP058 settings (epics/ep_058_.../hosted_directory/.env).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

import psycopg

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "switch_explorer_template.html"
EP058 = HERE.parent / "ep_058_strategy_intelligence_pg" / "hosted_directory"
NAME = re.compile(r"^(.*)_(\d+)_tp(\d+)_sl(\d+)$")
DIMS = ["family", "window", "tp", "sl"]
SCENARIOS = {"net": "Top Net", "win": "Top Win Rate", "side": "Top Buy Sell"}
OPPOSITE_CORR = -0.2


def get_dsn(arg: str | None) -> str:
    if arg:
        return arg
    if os.environ.get("SOURCE_DATABASE_URL"):
        return os.environ["SOURCE_DATABASE_URL"]
    sys.path.insert(0, str(EP058))
    os.environ.setdefault("EP051_ENV_FILE", str(EP058 / ".env"))
    from app.config import get_settings  # type: ignore

    url = get_settings().source_database_url
    if not url:
        raise SystemExit("No database URL: pass --dsn or set SOURCE_DATABASE_URL")
    return url


def model_number(model: str) -> int:
    digits = re.sub(r"\D", "", model)
    return int(digits) if digits else 0


def correlation(a: list[float], b: list[float]) -> float | None:
    """Pearson correlation of five-minute changes, over the common length."""
    n = min(len(a), len(b))
    if n < 6:
        return None
    da = [a[i] - a[i - 1] for i in range(1, n)]
    db = [b[i] - b[i - 1] for i in range(1, n)]
    ma, mb = sum(da) / len(da), sum(db) / len(db)
    va = sum((x - ma) ** 2 for x in da)
    vb = sum((x - mb) ** 2 for x in db)
    if va == 0 or vb == 0:
        return None
    return sum((x - ma) * (y - mb) for x, y in zip(da, db)) / math.sqrt(va * vb)


def load_product(cur, day: str, product: str, as_of=None):
    cur.execute(
        "select trim(model), max(strategy_name) from product_forex where lower(trim(product)) = %s group by 1",
        (product,),
    )
    meta = {m: s for m, s in cur.fetchall() if s}
    if not meta:
        return meta, {}, {}
    cur.execute(
        """select trim(model), snapshot_timestamp, cum_net, cum_buy_net, cum_sell_net
           from tbl_dna_model_summary_snapshots_5min
           where snapshot_timestamp >= %s::date and snapshot_timestamp < %s::date + interval '1 day'
             and (%s::timestamp is null or snapshot_timestamp <= %s::timestamp)
             and model = any(%s) order by snapshot_timestamp""",
        (day, day, as_of, as_of, list(meta)),
    )
    snaps = defaultdict(list)
    for m, ts, net, buy, sell in cur.fetchall():
        snaps[m].append((ts.replace(tzinfo=None), float(net), float(buy), float(sell)))
    cur.execute(
        """select trim(model), last_update, net_return from combined_trades_closed
           where lower(trim(product)) = %s and created >= %s::date
             and last_update >= %s::date and last_update < %s::date + interval '1 day'
             and (%s::timestamp is null or last_update <= %s::timestamp)""",
        (product, day, day, day, as_of, as_of),
    )
    closed = defaultdict(list)
    for m, ts, net in cur.fetchall():
        closed[m].append((ts.replace(tzinfo=None), float(net)))
    return meta, snaps, closed


def compress_curve(points):
    """One point per minute (the last), then only the first and last point of each flat run: same drawn shape,
    same lookups, a quarter of the size."""
    per_minute = {}
    for m, v in points:
        per_minute[m] = v
    pts = sorted(per_minute.items())
    out = []
    for i, (m, v) in enumerate(pts):
        before = pts[i - 1][1] if i > 0 else None
        after = pts[i + 1][1] if i + 1 < len(pts) else None
        if before != v or after != v:
            out.append([m, v])
    return out


def compact_cases(cases):
    """Turn row dicts into short arrays and move strategy names and products into one lookup, to keep the file small.
    The page rebuilds the dicts when it loads (hydrate in the template)."""
    models = {}
    def note(r):
        models[r["model"]] = [r["strategy"], r["product"]]
    for c in cases.values():
        for r in [*c["top"], *c["similar"], *c["opposite"], *[g for g in c["tinfo"].values() if g]]:
            note(r)
        c["top"] = [[r["model"], r["trades"], r["win"], r["net"]] for r in c["top"]]
        c["similar"] = [[r["model"], r["trades"], r["win"], r["net"], r["corr"], r["differs"], r["value"]] for r in c["similar"]]
        c["opposite"] = [[r["model"], r["trades"], r["win"], r["net"], r["corr"]] for r in c["opposite"]]
        c["tinfo"] = {k: ([g["model"], g["trades"], g["win"], g["net"], g["corr"]] if g else None) for k, g in c["tinfo"].items()}
    return models


def repository_sample(meta, snaps, closed, product_of, end_minute, min_closed, size=24):
    """A static, evenly spread sample of the repository (best to worst by end-of-day net, distinct nets only) with
    full-day equity curves every 15 minutes. It only illustrates what the repository holds; selection never uses it."""
    rows = []
    for model in meta:
        pts = snaps.get(model)
        done = closed.get(model, [])
        if not pts or len(done) < min_closed:
            continue
        wins = sum(1 for x in done if x[1] > 0)
        rows.append(dict(model=model, strategy=meta[model], product=product_of[model].upper(), closed=len(done),
                         win=round(wins / len(done) * 100, 1) if done else 0.0, net=round(pts[-1][1], 1), pts=pts))
    total = len(rows)
    rows.sort(key=lambda r: (-r["net"], model_number(r["model"])))
    seen, distinct = set(), []
    for r in rows:
        if r["net"] not in seen:
            seen.add(r["net"])
            distinct.append(r)
    n = len(distinct)
    if n <= size:
        pick = distinct
    else:
        idx = list(dict.fromkeys(round(i * (n - 1) / (size - 1)) for i in range(size)))
        pick = [distinct[i] for i in idx]
    items = [dict(model=r["model"], strategy=r["strategy"], product=r["product"], closed=r["closed"], win=r["win"],
                  net=r["net"], series=thumbnail(r["pts"], end_minute, 15)) for r in pick]
    return dict(total=total, distinct=n, step=15, items=items)


def thumbnail(points, end_minute, step=30):
    """Net every `step` minutes, as known at the start of that minute (nothing from inside the minute), rounded."""
    pts = sorted((x[0].hour * 60 + x[0].minute, x[1]) for x in points)
    out, i, last = [], 0, 0.0
    for m in range(0, end_minute + 1, step):
        while i < len(pts) and pts[i][0] <= m - 1:
            last = pts[i][1]
            i += 1
        out.append(round(last))
    return out


def distinct_by_net(rows):
    """Keep the first strategy for each net value; identical results are clones, not alternatives."""
    seen, out = set(), []
    for r in rows:
        key = round(r["net"], 1)
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out


def build_cases(day: str, product: str, meta, snaps, closed, first_hour: int, last_hour: int, min_closed: int, product_of=None, cls: str = "crypto"):
    minute = lambda ts: ts.hour * 60 + ts.minute
    cases, curves = {}, {}
    pof = lambda m: (product_of or {}).get(m, product).upper()

    def curve(model: str):
        return compress_curve([[minute(x[0]), round(x[1], 1)] for x in snaps[model]])

    for hour in range(first_hour, last_hour + 1):
        cut = dt.datetime.fromisoformat(f"{day} {hour:02d}:00:00")
        state = {}
        for model in meta:
            seen = [x for x in snaps.get(model, []) if x[0] <= cut]
            done = [x for x in closed.get(model, []) if x[0] <= cut]
            if not seen:
                continue
            wins = sum(1 for x in done if x[1] > 0)
            state[model] = dict(
                model=model, strategy=meta[model], product=pof(model), net=round(seen[-1][1], 1), trades=len(done),
                win=round(wins / len(done) * 100, 1) if done else 0.0,
                series=[x[1] for x in seen], dominant=max(seen[-1][2], seen[-1][3]),
            )
        eligible = [v for v in state.values() if v["trades"] >= min_closed]
        if not eligible:
            continue
        rankers = {
            "net": lambda v: (-v["net"], model_number(v["model"])),
            "win": lambda v: (-v["win"], -v["net"], model_number(v["model"])),
            "side": lambda v: (-v["dominant"], -v["net"], model_number(v["model"])),
        }
        at_cut = lambda m: [x[1] for x in snaps[m] if x[0] <= cut][-1]
        forward = lambda m: round(snaps[m][-1][1] - at_cut(m), 1)
        corr_cache = {}
        for scenario, rank_key in rankers.items():
            ranked = sorted(eligible, key=rank_key)
            selected = ranked[0]
            top_six = distinct_by_net(ranked)[:6]  # no two with the same net
            parts = NAME.match(selected["strategy"])
            if not parts:
                continue

            def row(v, extra):
                ck = (selected["model"], v["model"])
                if v["model"] == selected["model"]:
                    r = 1.0
                else:
                    if ck not in corr_cache:
                        corr_cache[ck] = correlation(selected["series"], v["series"])
                    r = corr_cache[ck]
                return dict(model=v["model"], strategy=v["strategy"], product=v["product"], trades=v["trades"], win=v["win"],
                            net=v["net"], corr=None if r is None else round(r, 2), **extra)

            similar = [row(selected, dict(differs="selected", value=""))]
            for v in state.values():
                if v["model"] == selected["model"] or v["product"] != selected["product"]:
                    continue  # similar = same product
                other = NAME.match(v["strategy"])
                if not other:
                    continue
                diff = [DIMS[i] for i in range(4) if parts.group(i + 1) != other.group(i + 1)]
                if len(diff) == 1:
                    similar.append(row(v, dict(differs=diff[0], value=other.group(DIMS.index(diff[0]) + 1))))
            # Strategies with the same net as the selected one are clones, not alternatives: never selected.
            pool = [row(v, dict(differs="", value="")) for v in eligible
                    if v["model"] != selected["model"] and v["net"] != selected["net"]]
            best_first = lambda g: (-g["net"], model_number(g["model"]))
            opposite = distinct_by_net(sorted([g for g in pool if g["corr"] is not None and g["corr"] <= OPPOSITE_CORR], key=best_first))
            # Always compare against a DIFFERENT strategy: never the selected one, never a clone of it.
            others = [g for g in similar if g["model"] != selected["model"] and g["net"] != selected["net"] and g["trades"] >= min_closed]
            by_win = lambda g: (-g["win"], -g["net"], model_number(g["model"]))
            first = lambda rows, key: sorted(rows, key=key)[0] if rows else None
            targets = dict(
                similar=first(others, best_first),
                opposite=opposite[0] if opposite else None,
                overall=first(pool, best_first),
                winrate=first(pool, by_win),
            )
            fwd = {selected["model"]: forward(selected["model"])}
            after = {}
            for g in targets.values():
                if g:
                    fwd[g["model"]] = forward(g["model"])
                    after[g["model"]] = [[minute(t[0]), round(t[1], 1)] for t in closed.get(g["model"], []) if t[0] > cut][:14]
                    curves.setdefault(g["model"], curve(g["model"]))
            curves.setdefault(selected["model"], curve(selected["model"]))
            for v in top_six:
                curves.setdefault(v["model"], curve(v["model"]))
            snap_ts = [x[0] for x in snaps[selected["model"]] if x[0] <= cut][-1]
            cases[f"{cls}|{product.upper()}|{scenario}|{hour:02d}"] = dict(
                cls=cls, product=product.upper(), scenario=scenario, hour=hour, eligible=len(eligible),
                top=[dict(model=v["model"], strategy=v["strategy"], product=v["product"], trades=v["trades"], win=v["win"], net=v["net"]) for v in top_six],
                selected=selected["model"], similar=similar, opposite=opposite[:5],
                targets={k: (g["model"] if g else None) for k, g in targets.items()},
                tinfo=targets, fwd=fwd, after=after, snap=snap_ts.strftime("%H:%M:%S"),
            )
    return cases, curves


def pick_date(cur, product_type: str, min_hours: int) -> str:
    """Latest date whose snapshots cover at least `min_hours` different hours (a usable day); else the latest date."""
    cur.execute("select distinct trim(model) from product_forex where lower(trim(product_type)) = %s", (product_type,))
    class_models = {r[0] for r in cur.fetchall()}
    # models that really have snapshots: look at the last few days only
    cur.execute("select distinct trim(model) from tbl_dna_model_summary_snapshots_5min where snapshot_timestamp >= now() - interval '4 days'")
    sample = sorted(class_models & {r[0] for r in cur.fetchall()})[:60]
    if not sample:
        raise SystemExit(f"No recent snapshots for {product_type}")
    cur.execute(
        """select snapshot_timestamp::date, count(distinct extract(hour from snapshot_timestamp))
           from tbl_dna_model_summary_snapshots_5min
           where snapshot_timestamp >= now() - interval '21 days' and model = any(%s)
           group by 1 order by 1 desc""",
        (sample,),
    )
    days = cur.fetchall()
    if not days:
        raise SystemExit(f"No snapshots for {product_type} in the last 21 days")
    for d, hours in days:
        if hours >= min_hours:
            return d.isoformat()
    return days[0][0].isoformat()


def build_class(cur, cls: str, day: str, products_arg: list[str] | None, args):
    """All cases for one asset class. Crypto and forex are never pooled together."""
    if products_arg:
        products = products_arg
    else:
        cur.execute("select distinct lower(trim(product)) from product_forex where lower(trim(product_type)) = %s order by 1", (cls,))
        products = [r[0] for r in cur.fetchall() if r[0]]
    cases, curves, loaded, last = {}, {}, [], None
    pool_meta, pool_snaps, pool_closed, product_of = {}, {}, {}, {}
    for product in products:
        meta, snaps, closed = load_product(cur, day, product, args.as_of_by_class.get(cls))
        if not snaps:
            print(f"  [{cls}] {product}: no snapshots on {day}, skipped")
            continue
        newest = max(x[0] for pts in snaps.values() for x in pts)
        last = newest if last is None or newest > last else last
        c, k = build_cases(day, product, meta, snaps, closed, args.first_hour, min(22, newest.hour), args.min_closed, None, cls)
        pool_meta.update(meta); pool_snaps.update(snaps); pool_closed.update(closed)
        product_of.update({m: product for m in meta})
        if c:
            cases.update(c)
            curves.update(k)
            loaded.append(product.upper())
        print(f"  [{cls}] {product}: {len(c)} cases")
    if len(loaded) > 1:
        newest_all = max(x[0] for pts in pool_snaps.values() for x in pts)
        c, k = build_cases(day, "all", pool_meta, pool_snaps, pool_closed, args.first_hour, min(22, newest_all.hour),
                           args.min_closed, product_of, cls)
        cases.update(c)
        curves.update(k)
        print(f"  [{cls}] all products: {len(c)} cases")
    if not cases:
        return None
    meta = dict(label=cls.capitalize(), date=day, products=loaded, last_snapshot=last.strftime("%d %b %H:%M"),
                last_minute=last.hour * 60 + last.minute)
    sample = repository_sample(pool_meta, pool_snaps, pool_closed, product_of, meta["last_minute"], args.min_closed)
    return cases, curves, meta, sample


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", help="YYYY-MM-DD for every class (default: each class uses its own latest usable day)")
    ap.add_argument("--product-type", default="both", choices=["crypto", "forex", "both"])
    ap.add_argument("--products", help="comma list, e.g. avax,btc (only with a single --product-type)")
    ap.add_argument("--min-hours", type=int, default=1, help="hours of snapshots a day needs when picking the default date (1 = always the newest day with data)")
    ap.add_argument("--first-hour", type=int, default=3)
    ap.add_argument("--min-closed", type=int, default=0, help="optional minimum of closed positions to qualify (default 0 = no filter)")
    ap.add_argument("--out", help="output file (default: strategy-selection-to-switch-YYYYMMDD-HHMM.html in this folder)")
    ap.add_argument("--no-latest", action="store_true", help="do not refresh strategy-selection-to-switch-latest.html")
    ap.add_argument("--as-of", help="rebuild as the data stood at a past time: 'YYYY-MM-DD HH:MM' for every class, or 'crypto=YYYY-MM-DD HH:MM,forex=YYYY-MM-DD HH:MM'. Used to restore an earlier build for the history.")
    ap.add_argument("--dsn")
    args = ap.parse_args()
    kinds = ["crypto", "forex"] if args.product_type == "both" else [args.product_type]
    args.as_of_by_class = {}
    if args.as_of:
        parts = [x.strip() for x in args.as_of.split(",")]
        for part in parts:
            k, _, v = part.rpartition("=")
            for cls_ in ([k] if k else kinds):
                args.as_of_by_class[cls_] = dt.datetime.fromisoformat(v.strip().replace("T", " ")).replace(second=59)
    if args.products and len(kinds) > 1:
        raise SystemExit("--products needs a single --product-type")

    cases, curves, classes = {}, {}, {}
    samples = {}
    with psycopg.connect(get_dsn(args.dsn)) as conn:
        cur = conn.cursor()
        for cls in kinds:
            day = args.date or pick_date(cur, cls, args.min_hours)
            print(f"{cls}: {day}")
            built = build_class(cur, cls, day, [p.strip().lower() for p in args.products.split(",")] if args.products else None, args)
            if built:
                cases.update(built[0]); curves.update(built[1]); classes[cls] = built[2]
                samples[cls] = built[3]
            else:
                print(f"  {cls}: nothing qualified on {day}, class left out")
    if not cases:
        raise SystemExit("No qualifying data")
    built = dt.datetime.now()
    models = compact_cases(cases)
    data = dict(built_at=built.strftime("%d %b %Y %H:%M"), rebuilt_as_of=bool(args.as_of), min_closed=args.min_closed, scen=SCENARIOS, classes=classes, models=models, cases=cases, curves=curves,
                sample=samples)
    summary = "; ".join(f"{k}: {v['date']} as of {v['last_snapshot']}" for k, v in classes.items())
    html = (TEMPLATE.read_text(encoding="utf-8")
            .replace("__BUILT_ISO__", built.strftime("%Y-%m-%dT%H:%M:%S"))
            .replace("__DATA_SUMMARY__", summary)
            .replace("__DATA__", json.dumps(data, separators=(",", ":"))))
    if args.as_of:
        newest = max(dt.datetime.strptime(f"{v['date']} {v['last_snapshot'][-5:]}", "%Y-%m-%d %H:%M") for v in classes.values())
        default_name = f"strategy-selection-to-switch-asof-{newest:%Y%m%d-%H%M}.html"
    else:
        default_name = f"strategy-selection-to-switch-{built:%Y%m%d-%H%M}.html"
    out = Path(args.out) if args.out else HERE / default_name
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out} ({len(html) / 1024:.0f} KB) - {len(cases)} cases - {summary}")
    if not args.out and not args.no_latest and not args.as_of:
        latest = HERE / "strategy-selection-to-switch-latest.html"
        latest.write_text(html, encoding="utf-8")
        print(f"refreshed {latest.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
