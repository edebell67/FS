from __future__ import annotations

import argparse
import json
from datetime import datetime, time, timedelta
from pathlib import Path
from typing import Any

from json_layout import load_layout_config, resolve_day_dir


ROOT_PATH = Path(__file__).resolve().parent
CONFIG_PATH = ROOT_PATH / "config.json"
JSON_ROOT = ROOT_PATH / "json"
OUTPUT_NAME = "_summary_net_delta_snapshots_15m.json"
SNAPSHOT_MINUTES = 15
TOP_N = 10


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


def parse_tp_sl(strategy: str) -> tuple[float | None, float | None]:
    import re

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


def load_summary_series(base_dir: Path) -> dict[tuple[str, str], list[dict[str, Any]]]:
    summary_path = base_dir / "_summary_net.json"
    if not summary_path.exists():
        raise FileNotFoundError(f"Missing summary file: {summary_path}")

    data = json.loads(summary_path.read_text(encoding="utf-8"))
    loaded: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for strategy, products in (data.get("strategies") or {}).items():
        if not isinstance(products, dict):
            continue
        for product, series in products.items():
            if not isinstance(series, list):
                continue
            normalized = []
            for point in series:
                if not isinstance(point, dict):
                    continue
                point_time = parse_dt(point.get("t"))
                if point_time is None:
                    continue
                normalized.append(
                    {
                        "t": point_time,
                        "net": round(float(point.get("net") or 0.0), 2),
                    }
                )
            normalized.sort(key=lambda item: item["t"])
            if normalized:
                loaded[(strategy, product)] = normalized
    return loaded


def latest_point_at_or_before(series: list[dict[str, Any]], target: datetime) -> dict[str, Any] | None:
    latest: dict[str, Any] | None = None
    for point in series:
        if point["t"] <= target:
            latest = point
        else:
            break
    return latest


def build_snapshot_times(date_str: str, series_map: dict[tuple[str, str], list[dict[str, Any]]]) -> list[datetime]:
    date_value = datetime.strptime(date_str, "%Y-%m-%d").date()
    start = datetime.combine(date_value, time.min)
    events = [point["t"] for series in series_map.values() for point in series if point["t"].date() == date_value]
    today = datetime.now().date()
    if date_value == today:
        latest_event = max(events) if events else None
        end = max(datetime.now(), latest_event) if latest_event else datetime.now()
    else:
        end = max(events) if events else datetime.combine(date_value, time.max).replace(microsecond=0)
    end = end.replace(second=0, microsecond=0)
    end = end.replace(minute=(end.minute // SNAPSHOT_MINUTES) * SNAPSHOT_MINUTES)
    times = []
    current = start
    while current <= end:
        times.append(current)
        current += timedelta(minutes=SNAPSHOT_MINUTES)
    return times


def make_delta_row(
    snapshot_time: datetime,
    strategy: str,
    product: str,
    strategy_group: str,
    current_point: dict[str, Any],
    baseline_point: dict[str, Any],
    window_minutes: int,
) -> dict[str, Any]:
    current_net = round(float(current_point["net"]), 2)
    baseline_net = round(float(baseline_point["net"]), 2)
    delta = round(current_net - baseline_net, 2)
    return {
        "snapshot_time": snapshot_time.isoformat(),
        "window_minutes": window_minutes,
        "strategy_group": strategy_group,
        "strategy": strategy,
        "product": product,
        "baseline_time": baseline_point["t"].isoformat(),
        "current_time": current_point["t"].isoformat(),
        "baseline_net": baseline_net,
        "current_net": current_net,
        "delta_net": delta,
    }


def top_rows_for_window(
    snapshot_time: datetime,
    series_map: dict[tuple[str, str], list[dict[str, Any]]],
    window_minutes: int,
    scalper_ratio: float,
    rev_scalper_ratio: float,
) -> list[dict[str, Any]]:
    baseline_time = snapshot_time - timedelta(minutes=window_minutes)
    rows = []
    for (strategy, product), series in series_map.items():
        current_point = latest_point_at_or_before(series, snapshot_time)
        baseline_point = latest_point_at_or_before(series, baseline_time)
        if current_point is None or baseline_point is None:
            continue
        strategy_group = classify_strategy(strategy, scalper_ratio, rev_scalper_ratio)
        rows.append(
            make_delta_row(
                snapshot_time=snapshot_time,
                strategy=strategy,
                product=product,
                strategy_group=strategy_group,
                current_point=current_point,
                baseline_point=baseline_point,
                window_minutes=window_minutes,
            )
        )
    rows.sort(
        key=lambda row: (
            -float(row["delta_net"]),
            -float(row["current_net"]),
            row["strategy"],
            row["product"],
        )
    )
    return rows[:TOP_N]


def summarize_snapshot(rows: list[dict[str, Any]]) -> dict[str, Any]:
    deltas = [float(row["delta_net"]) for row in rows]
    return {
        "row_count": len(rows),
        "best_delta": round(max(deltas), 2) if deltas else 0.0,
        "avg_delta": round(sum(deltas) / len(deltas), 2) if deltas else 0.0,
    }


def build_payload(run_mode: str, product_type: str, date_str: str, base_dir: Path, config: dict[str, Any]) -> dict[str, Any]:
    scalper_ratio = float(config.get("scalper_ratio", 5.0))
    rev_scalper_ratio = float(config.get("rev_scalper_ratio", 2.0))
    series_map = load_summary_series(base_dir)
    snapshot_times = build_snapshot_times(date_str, series_map)
    snapshots = []

    for snapshot_time in snapshot_times:
        top10_30m = top_rows_for_window(snapshot_time, series_map, 30, scalper_ratio, rev_scalper_ratio)
        top10_60m = top_rows_for_window(snapshot_time, series_map, 60, scalper_ratio, rev_scalper_ratio)
        snapshots.append(
            {
                "time": snapshot_time.isoformat(),
                "top10_30m": top10_30m,
                "top10_60m": top10_60m,
                "summary_30m": summarize_snapshot(top10_30m),
                "summary_60m": summarize_snapshot(top10_60m),
            }
        )

    return {
        "generated_at": datetime.now().isoformat(),
        "date": date_str,
        "run_mode": run_mode,
        "product_type": product_type,
        "snapshot_minutes": SNAPSHOT_MINUTES,
        "windows_minutes": [30, 60],
        "top_n": TOP_N,
        "source": "_summary_net.json",
        "strategy_group_rules": {
            "scalper": f"SL / TP >= {scalper_ratio}",
            "rev_scalper": f"TP / SL >= {rev_scalper_ratio}",
            "remainder": "not scalper and not rev_scalper",
        },
        "series_count": len(series_map),
        "snapshot_count": len(snapshots),
        "default_window": "30m",
        "snapshots": snapshots,
    }


def generate(run_mode: str, product_type: str, date_str: str) -> Path:
    config = load_config()
    base_dir = resolve_day_dir(JSON_ROOT, run_mode, date_str, product_type)
    if not base_dir.exists():
        raise FileNotFoundError(f"Day directory not found: {base_dir}")
    payload = build_payload(run_mode, product_type, date_str, base_dir, config)
    output_path = base_dir / OUTPUT_NAME
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate 15m snapshot leaders for 30m and 60m summary-net deltas.")
    parser.add_argument("--mode", default="live")
    parser.add_argument("--product-type", default="forex")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    args = parser.parse_args()
    output_path = generate(args.mode, args.product_type, args.date)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
