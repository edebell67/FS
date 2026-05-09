from __future__ import annotations

import argparse
import json
import os
import re
import time as time_module
import uuid
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from pathlib import Path
from typing import Any

from json_layout import day_dir, load_layout_config


ROOT_PATH = Path(__file__).resolve().parent
CONFIG_PATH = ROOT_PATH / "config.json"
JSON_ROOT = ROOT_PATH / "json"
OUTPUT_NAME = "_strategy_snapshots_15m.json"
SNAPSHOT_MINUTES = 15


@dataclass
class TradeRecord:
    key: tuple[str, str, str]
    strategy: str
    product: str
    guid: str
    direction: str
    status: str
    entry_time: datetime | None
    exit_time: datetime | None
    net_return: float
    has_direction: bool
    field_count: int
    is_closed: bool


def load_config() -> dict[str, Any]:
    return load_layout_config(CONFIG_PATH)


def parse_dt(value: Any) -> datetime | None:
    if not value:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return None


def parse_file_identity(path: Path) -> tuple[str, str, str]:
    match = re.match(
        r"^(?P<strategy>.+?)_(?P<guid>[0-9a-f]{8})_(?P<product>.+?)_\d{8}_\d{6}_.+?_(?:cld?|op)\.json$",
        path.name,
        re.IGNORECASE,
    )
    if not match:
        return "", "", ""
    return match.group("strategy"), match.group("guid"), match.group("product")


def parse_tp_sl(strategy: str) -> tuple[float | None, float | None]:
    match = re.search(r"tp([\d.]+)_sl([\d.]+)", str(strategy or ""), re.IGNORECASE)
    if not match:
        return None, None
    try:
        return float(match.group(1)), float(match.group(2))
    except ValueError:
        return None, None


def classify_strategy(strategy: str, scalper_ratio: float, rev_scalper_ratio: float) -> str:
    tp, sl = parse_tp_sl(strategy)
    if tp and sl:
        if sl >= tp * scalper_ratio:
            return "scalper"
        if tp >= sl * rev_scalper_ratio:
            return "rev_scalper"
    return "remainder"


def normalize_direction(payload: dict[str, Any]) -> tuple[str, bool]:
    raw = str(payload.get("direction") or "").strip().upper()
    if raw in {"LONG", "BUY"}:
        return "BUY", True
    if raw in {"SHORT", "SELL"}:
        return "SELL", True
    bias = str(payload.get("market_bias_at_open") or "").strip().upper()
    if bias in {"BUY", "SELL"}:
        return bias, False
    return "UNKNOWN", False


def record_rank(record: TradeRecord) -> tuple[int, int, int]:
    return (
        1 if record.has_direction else 0,
        record.field_count,
        1 if str(record.status).upper() == "CLOSED" else 0,
    )


def read_trade(path: Path) -> TradeRecord | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(payload, dict):
        return None

    file_strategy, file_guid, file_product = parse_file_identity(path)
    strategy = str(
        payload.get("strategy_name")
        or payload.get("source_strategy")
        or payload.get("script_name")
        or file_strategy
        or ""
    ).strip()
    product = str(payload.get("product") or file_product or "").strip()
    guid = str(payload.get("guid") or file_guid or "").strip()
    if not strategy or not product or not guid:
        return None

    direction, has_direction = normalize_direction(payload)
    status = str(payload.get("status") or "").strip().upper()
    is_closed = status == "CLOSED" or bool(payload.get("exit_time")) or "_cl" in path.name.lower()
    return TradeRecord(
        key=(strategy, guid, product),
        strategy=strategy,
        product=product,
        guid=guid,
        direction=direction,
        status=status,
        entry_time=parse_dt(payload.get("entry_time")),
        exit_time=parse_dt(payload.get("exit_time")),
        net_return=float(payload.get("net_return") or 0.0),
        has_direction=has_direction,
        field_count=len(payload),
        is_closed=is_closed,
    )


def iter_trade_files(base_dir: Path) -> list[Path]:
    files = list(base_dir.glob("*_cl*.json")) + list(base_dir.glob("*_op.json"))
    archive = base_dir / "archive"
    if archive.exists():
        files.extend(archive.rglob("*_cl*.json"))
        files.extend(archive.rglob("*_op.json"))
    return files


def load_records(base_dir: Path) -> tuple[list[TradeRecord], list[TradeRecord]]:
    closed: dict[tuple[str, str, str], TradeRecord] = {}
    open_records: dict[tuple[str, str, str], TradeRecord] = {}
    files = iter_trade_files(base_dir)
    if not files:
        return [], []

    worker_count = min(32, max(4, (os.cpu_count() or 4) * 2))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        records = executor.map(read_trade, files)

    for record in records:
        if not record:
            continue
        target = closed if record.is_closed else open_records
        existing = target.get(record.key)
        if existing is None or record_rank(record) > record_rank(existing):
            target[record.key] = record

    # If a trade is closed, do not also count it as open.
    for key in list(open_records):
        if key in closed:
            del open_records[key]

    return list(closed.values()), list(open_records.values())


def build_snapshot_times(date_str: str, closed: list[TradeRecord], open_records: list[TradeRecord]) -> list[datetime]:
    date_value = datetime.strptime(date_str, "%Y-%m-%d").date()
    start = datetime.combine(date_value, time.min)
    today = datetime.now().date()
    if date_value == today:
        end = datetime.now()
    else:
        events = [r.exit_time for r in closed if r.exit_time] + [r.entry_time for r in open_records if r.entry_time]
        end = max(events) if events else datetime.combine(date_value, time.max).replace(microsecond=0)
    end = end.replace(second=0, microsecond=0)
    minute = (end.minute // SNAPSHOT_MINUTES) * SNAPSHOT_MINUTES
    end = end.replace(minute=minute)
    times = []
    current = start
    while current <= end:
        times.append(current)
        current += timedelta(minutes=SNAPSHOT_MINUTES)
    return times


def new_row(snapshot_time: datetime, product: str, strategy: str, group: str) -> dict[str, Any]:
    return {
        "snapshot_time": snapshot_time.isoformat(),
        "strategy_group": group,
        "product": product,
        "strategy": strategy,
        "closed_count": 0,
        "open_count": 0,
        "profit_count": 0,
        "loss_count": 0,
        "breakeven_count": 0,
        "buy_profit": 0,
        "buy_loss": 0,
        "sell_profit": 0,
        "sell_loss": 0,
        "unknown_profit": 0,
        "unknown_loss": 0,
        "buy_profit_net": 0.0,
        "buy_loss_net": 0.0,
        "sell_profit_net": 0.0,
        "sell_loss_net": 0.0,
        "profit_net": 0.0,
        "loss_net": 0.0,
        "net": 0.0,
    }


def apply_closed(row: dict[str, Any], record: TradeRecord) -> None:
    net = record.net_return
    row["closed_count"] += 1
    row["net"] += net
    if net > 0:
        row["profit_count"] += 1
        row["profit_net"] += net
        if record.direction == "BUY":
            row["buy_profit"] += 1
            row["buy_profit_net"] += net
        elif record.direction == "SELL":
            row["sell_profit"] += 1
            row["sell_profit_net"] += net
        else:
            row["unknown_profit"] += 1
    elif net < 0:
        row["loss_count"] += 1
        row["loss_net"] += net
        if record.direction == "BUY":
            row["buy_loss"] += 1
            row["buy_loss_net"] += net
        elif record.direction == "SELL":
            row["sell_loss"] += 1
            row["sell_loss_net"] += net
        else:
            row["unknown_loss"] += 1
    else:
        row["breakeven_count"] += 1


def round_row(row: dict[str, Any]) -> dict[str, Any]:
    rounded = dict(row)
    for key in ("buy_profit_net", "buy_loss_net", "sell_profit_net", "sell_loss_net", "profit_net", "loss_net", "net"):
        rounded[key] = round(float(rounded[key]), 2)
    return rounded


def summarize_group(snapshot_time: datetime, group: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary = new_row(snapshot_time, "__ALL__", "__ALL__", group)
    for row in rows:
        for key, value in row.items():
            if key in {"snapshot_time", "strategy_group", "product", "strategy"}:
                continue
            summary[key] += value
    return round_row(summary)


def rollup_rows_by_strategy(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rolled: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        key = (row["strategy_group"], row["strategy"])
        if key not in rolled:
            rolled[key] = new_row(datetime.fromisoformat(row["snapshot_time"]), "__ALL__", row["strategy"], row["strategy_group"])
        target = rolled[key]
        target["snapshot_time"] = row["snapshot_time"]
        for metric, value in row.items():
            if metric in {"snapshot_time", "strategy_group", "product", "strategy"}:
                continue
            target[metric] += value
    result = [round_row(row) for row in rolled.values()]
    result.sort(key=lambda r: (r["strategy_group"], -r["net"], r["strategy"]))
    return result


def build_payload(run_mode: str, product_type: str, date_str: str, base_dir: Path, config: dict[str, Any]) -> dict[str, Any]:
    scalper_ratio = float(config.get("scalper_ratio", 5.0))
    rev_scalper_ratio = float(config.get("rev_scalper_ratio", 2.0))
    closed, open_records = load_records(base_dir)
    closed_with_exit = [record for record in closed if record.exit_time]
    snapshot_times = build_snapshot_times(date_str, closed, open_records)

    closed_sorted = sorted(closed_with_exit, key=lambda r: r.exit_time or datetime.min)
    rows_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    closed_idx = 0
    snapshots = []
    open_by_key: dict[tuple[str, str], list[TradeRecord]] = defaultdict(list)
    for open_record in open_records:
        open_by_key[(open_record.product, open_record.strategy)].append(open_record)

    for snapshot_time in snapshot_times:
        while closed_idx < len(closed_sorted) and (closed_sorted[closed_idx].exit_time or datetime.max) <= snapshot_time:
            record = closed_sorted[closed_idx]
            group = classify_strategy(record.strategy, scalper_ratio, rev_scalper_ratio)
            row_key = (record.product, record.strategy)
            if row_key not in rows_by_key:
                rows_by_key[row_key] = new_row(snapshot_time, record.product, record.strategy, group)
            apply_closed(rows_by_key[row_key], record)
            closed_idx += 1

        product_rows = []
        for row_key, row in rows_by_key.items():
            current = dict(row)
            current["snapshot_time"] = snapshot_time.isoformat()
            current["open_count"] = 0
            product, strategy = row_key
            for open_record in open_by_key.get((product, strategy), []):
                if open_record.entry_time and open_record.entry_time <= snapshot_time:
                    current["open_count"] += 1
            product_rows.append(round_row(current))

        product_rows.sort(key=lambda r: (r["strategy_group"], -r["net"], r["product"], r["strategy"]))
        strategy_rows = rollup_rows_by_strategy(product_rows)
        group_summaries = {
            group: summarize_group(snapshot_time, group, [r for r in strategy_rows if r["strategy_group"] == group])
            for group in ("scalper", "rev_scalper", "remainder")
        }
        snapshots.append(
            {
                "time": snapshot_time.isoformat(),
                "rows": strategy_rows,
                "strategy_rows": strategy_rows,
                "product_rows": product_rows,
                "group_summaries": group_summaries,
            }
        )

    return {
        "generated_at": datetime.now().isoformat(),
        "date": date_str,
        "run_mode": run_mode,
        "product_type": product_type,
        "snapshot_minutes": SNAPSHOT_MINUTES,
        "source": "closed_and_open_trade_json",
        "strategy_group_rules": {
            "scalper": f"SL / TP >= {scalper_ratio}",
            "rev_scalper": f"TP / SL >= {rev_scalper_ratio}",
            "remainder": "not scalper and not rev_scalper",
        },
        "source_counts": {
            "closed_records_total": len(closed),
            "closed_records_with_exit_time": len(closed_with_exit),
            "closed_records_without_exit_time": len(closed) - len(closed_with_exit),
            "open_records": len(open_records),
        },
        "snapshot_count": len(snapshots),
        "default_view": "strategy",
        "snapshots": snapshots,
    }


def write_payload(payload: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = output_path.with_name(f"{output_path.name}.{uuid.uuid4().hex}.tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
            handle.flush()
            os.fsync(handle.fileno())

        last_error = None
        for _ in range(10):
            try:
                os.replace(tmp, output_path)
                last_error = None
                break
            except PermissionError as exc:
                last_error = exc
                time_module.sleep(0.05)
        if last_error is not None:
            raise last_error
    finally:
        try:
            if tmp.exists():
                tmp.unlink()
        except OSError:
            pass


def output_name_from_filename(filename: str | None) -> str:
    value = str(filename or OUTPUT_NAME).strip()
    if not value:
        value = OUTPUT_NAME
    if not value.endswith(".json"):
        value = f"{value}.json"
    if not value.startswith("_"):
        value = f"_{value}"
    return value


def iter_date_dirs(run_mode: str, product_type: str) -> list[Path]:
    root = day_dir(JSON_ROOT, run_mode, "__DATE__", product_type).parent
    if not root.exists():
        return []
    dirs = []
    for child in root.iterdir():
        if not child.is_dir():
            continue
        if re.match(r"^\d{4}-\d{2}-\d{2}$", child.name):
            dirs.append(child)
    return sorted(dirs, key=lambda p: p.name)


def generate_for_day(run_mode: str, product_type: str, date_str: str, config: dict[str, Any], output_name: str) -> dict[str, Any]:
    base_dir = day_dir(JSON_ROOT, run_mode, date_str, product_type)
    if not base_dir.exists():
        raise FileNotFoundError(f"Day directory does not exist: {base_dir}")
    payload = build_payload(run_mode, product_type, date_str, base_dir, config)
    output_path = base_dir / output_name
    write_payload(payload, output_path)
    return {
        "date": date_str,
        "path": str(output_path),
        "snapshot_count": payload["snapshot_count"],
        "closed_with_exit": payload["source_counts"]["closed_records_with_exit_time"],
        "open": payload["source_counts"]["open_records"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate 15-minute cumulative strategy snapshots.")
    parser.add_argument("--run-mode", default="live")
    parser.add_argument("--product-type", default=None)
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--all-dates", action="store_true", help="Generate for every available date folder under the selected product_type.")
    parser.add_argument("--filename", default=OUTPUT_NAME, help="Output filename. A leading underscore is added if missing.")
    parser.add_argument("--skip-existing", action="store_true", help="Skip dates where the output file already exists.")
    parser.add_argument("--newest-first", action="store_true", help="Process date folders newest to oldest.")
    args = parser.parse_args()

    config = load_config()
    product_type = args.product_type or str(config.get("product_type") or "forex")
    output_name = output_name_from_filename(args.filename)

    if args.all_dates:
        date_dirs = iter_date_dirs(args.run_mode, product_type)
        if args.newest_first:
            date_dirs = list(reversed(date_dirs))
        if not date_dirs:
            raise SystemExit(f"No date folders found for {args.run_mode}/{product_type}")
        generated = []
        skipped = []
        for date_dir in date_dirs:
            output_path = date_dir / output_name
            if args.skip_existing and output_path.exists():
                skipped.append((date_dir.name, "exists"))
                print(f"Skipped {date_dir.name}: {output_path} already exists", flush=True)
                continue
            try:
                result = generate_for_day(args.run_mode, product_type, date_dir.name, config, output_name)
                generated.append(result)
                print(
                    f"Wrote {result['snapshot_count']} snapshots to {result['path']} "
                    f"(closed_with_exit={result['closed_with_exit']}, open={result['open']})",
                    flush=True,
                )
            except Exception as exc:
                skipped.append((date_dir.name, str(exc)))
                print(f"Skipped {date_dir.name}: {exc}", flush=True)
        print(f"Backfill complete: generated={len(generated)} skipped={len(skipped)}")
        return

    result = generate_for_day(args.run_mode, product_type, args.date, config, output_name)
    print(
        f"Wrote {result['snapshot_count']} snapshots to {result['path']} "
        f"(closed_with_exit={result['closed_with_exit']}, open={result['open']})"
    )


if __name__ == "__main__":
    main()
