from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_SOURCE = REPO_ROOT / "TradeApps" / "breakout" / "fs" / "json" / "live" / "forex"
OUT_DIR = Path(__file__).resolve().parent
FOREX_PRODUCT_RE = re.compile(r"^[A-Z]{6}_C$")
BASE_STRATEGY_RE = re.compile(
    r"^breakout(?:_R)?(?:_Rev)?_[234]_tp\d+(?:\.\d+)?_sl\d+(?:\.\d+)?$"
)


@dataclass(frozen=True)
class RankedItem:
    product: str
    strategy: str
    net: float
    source_time: datetime

    @property
    def key(self) -> tuple[str, str]:
        return (self.product, self.strategy)


@dataclass(frozen=True)
class Snapshot:
    date: str
    time: datetime
    path: Path
    ranked: list[RankedItem]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay forex _summary_net top-3 hold replacement rule.")
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--start-date", default="")
    parser.add_argument("--end-date", default="")
    parser.add_argument("--dates", default="", help="Optional comma-separated date whitelist, e.g. 2026-03-24,2026-03-26.")
    parser.add_argument("--open-hours", default="0,1,2,3")
    parser.add_argument("--switch-cost", type=float, default=50.0)
    parser.add_argument("--include-non-forex", action="store_true")
    parser.add_argument(
        "--include-generated-strategies",
        action="store_true",
        help="Include generated/suffixed strategy instance keys. Default excludes them.",
    )
    parser.add_argument(
        "--clean-files-only",
        action="store_true",
        help="Exclude any source file that contains at least one non-forex product key.",
    )
    parser.add_argument("--output-stem", default="summary_net_top3_hold_replay")
    return parser.parse_args()


def parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value)


def parse_open_hours(value: str) -> list[int]:
    return [int(part.strip()) for part in value.split(",") if part.strip()]


def file_date(path: Path) -> str:
    if path.parent.parent.name == "archive":
        return path.parents[2].name
    return path.parent.name


def snapshot_sort_key(path: Path) -> tuple[str, str]:
    date = file_date(path)
    time_key = path.parent.name if path.parent.parent.name == "archive" else "999999"
    return date, time_key


def iter_summary_files(source_dir: Path, start_date: str, end_date: str, date_whitelist: set[str]) -> list[Path]:
    files: list[Path] = []
    for path in source_dir.rglob("_summary_net*.json"):
        date = file_date(path)
        if date_whitelist and date not in date_whitelist:
            continue
        if start_date and date < start_date:
            continue
        if end_date and date > end_date:
            continue
        if path.stat().st_size == 0:
            continue
        files.append(path)
    return sorted(files, key=snapshot_sort_key)


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            return None
        data = json.loads(text)
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def latest_points(
    data: dict[str, Any],
    snapshot_time: datetime,
    include_non_forex: bool,
    include_generated_strategies: bool,
) -> tuple[list[RankedItem], set[str], set[str]]:
    strategies = data.get("strategies")
    if not isinstance(strategies, dict):
        return [], set()

    ranked: list[RankedItem] = []
    non_forex: set[str] = set()
    generated_strategies: set[str] = set()
    for strategy, products in strategies.items():
        if not BASE_STRATEGY_RE.match(str(strategy)):
            generated_strategies.add(str(strategy))
            if not include_generated_strategies:
                continue
        if not isinstance(products, dict):
            continue
        for product, points in products.items():
            if not FOREX_PRODUCT_RE.match(str(product)):
                non_forex.add(str(product))
                if not include_non_forex:
                    continue
            if not isinstance(points, list):
                continue
            latest: tuple[datetime, float] | None = None
            for point in points:
                if not isinstance(point, dict) or "t" not in point or "net" not in point:
                    continue
                try:
                    point_time = parse_iso(str(point["t"]))
                    net = float(point["net"])
                except (TypeError, ValueError):
                    continue
                if point_time <= snapshot_time and (latest is None or point_time > latest[0]):
                    latest = (point_time, net)
            if latest is not None:
                ranked.append(RankedItem(str(product), str(strategy), latest[1], latest[0]))

    ranked.sort(key=lambda item: (-item.net, item.product, item.strategy))
    return ranked, non_forex, generated_strategies


def load_snapshots(
    files: list[Path],
    include_non_forex: bool,
    clean_files_only: bool,
    include_generated_strategies: bool,
) -> tuple[list[Snapshot], set[str], set[str], int, int]:
    snapshots: list[Snapshot] = []
    non_forex: set[str] = set()
    generated_strategies: set[str] = set()
    unreadable = 0
    contaminated = 0

    for path in files:
        data = load_json(path)
        if not data:
            unreadable += 1
            continue
        last_update = data.get("last_update")
        if not last_update:
            unreadable += 1
            continue
        try:
            snapshot_time = parse_iso(str(last_update))
        except ValueError:
            unreadable += 1
            continue
        ranked, found_non_forex, found_generated = latest_points(
            data,
            snapshot_time,
            include_non_forex,
            include_generated_strategies,
        )
        non_forex.update(found_non_forex)
        generated_strategies.update(found_generated)
        if clean_files_only and found_non_forex:
            contaminated += 1
            continue
        if not ranked:
            continue
        snapshots.append(Snapshot(snapshot_time.date().isoformat(), snapshot_time, path, ranked))

    dedup: dict[tuple[str, datetime], Snapshot] = {}
    for snap in snapshots:
        dedup[(snap.date, snap.time)] = snap
    return (
        sorted(dedup.values(), key=lambda snap: (snap.date, snap.time)),
        non_forex,
        generated_strategies,
        unreadable,
        contaminated,
    )


def replay_day(day_snaps: list[Snapshot], open_hour: int, switch_cost: float) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    held: RankedItem | None = None
    switches = 0
    events: list[dict[str, Any]] = []
    open_minute = open_hour * 60

    for snap in day_snaps:
        minute = snap.time.hour * 60 + snap.time.minute
        if minute < open_minute:
            continue
        if not snap.ranked:
            continue

        current_top1 = snap.ranked[0]
        top3_keys = {item.key for item in snap.ranked[:3]}

        if held is None:
            held = current_top1
            events.append(
                {
                    "date": snap.date,
                    "time": snap.time.isoformat(),
                    "event": "open",
                    "from_product": "",
                    "from_strategy": "",
                    "from_rank": "",
                    "from_net": "",
                    "to_product": held.product,
                    "to_strategy": held.strategy,
                    "to_rank": 1,
                    "to_net": held.net,
                    "source_file": str(snap.path),
                }
            )
            continue

        held_rank = next((idx + 1 for idx, item in enumerate(snap.ranked) if item.key == held.key), None)
        held_net = next((item.net for item in snap.ranked if item.key == held.key), None)
        if held.key in top3_keys:
            continue

        previous = held
        switches += 1
        held = current_top1
        events.append(
            {
                "date": snap.date,
                "time": snap.time.isoformat(),
                "event": "replace",
                "from_product": previous.product,
                "from_strategy": previous.strategy,
                "from_rank": held_rank if held_rank is not None else "missing",
                "from_net": held_net if held_net is not None else "",
                "to_product": held.product,
                "to_strategy": held.strategy,
                "to_rank": 1,
                "to_net": held.net,
                "source_file": str(snap.path),
            }
        )

    final_net = 0.0
    if held is not None:
        final_snap = day_snaps[-1]
        final_item = next((item for item in final_snap.ranked if item.key == held.key), None)
        final_net = final_item.net if final_item is not None else 0.0

    return (
        {
            "date": day_snaps[0].date if day_snaps else "",
            "open_hour": open_hour,
            "opened": held is not None,
            "held_product": held.product if held else "",
            "held_strategy": held.strategy if held else "",
            "gross_final_net": final_net,
            "switches": switches,
            "switch_cost": switch_cost * switches,
            "net_after_switch_cost": final_net - (switch_cost * switches) if held is not None else 0.0,
            "snapshot_count": len(day_snaps),
        },
        events,
    )


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, Any]],
    day_rows: list[dict[str, Any]],
    event_rows: list[dict[str, Any]],
    source_dir: Path,
    files_count: int,
    snapshots_count: int,
    unreadable_count: int,
    contaminated_count: int,
    non_forex_products: set[str],
    generated_strategies: set[str],
    include_non_forex: bool,
    clean_files_only: bool,
    include_generated_strategies: bool,
) -> None:
    lines = [
        "# Forex Summary Net Top-3 Hold Replay",
        "",
        f"- Source: `{source_dir}`",
        f"- Source files discovered: `{files_count}`",
        f"- Loaded ranked snapshots: `{snapshots_count}`",
        f"- Unreadable/empty/schema-missing files skipped: `{unreadable_count}`",
        f"- Contaminated files excluded: `{contaminated_count}`",
        f"- Product filter: `{'include all products' if include_non_forex else 'forex regex only ([A-Z]{6}_C)'}`",
        f"- Clean files only: `{'yes' if clean_files_only else 'no'}`",
        f"- Strategy filter: `{'include generated/suffixed strategy keys' if include_generated_strategies else 'canonical base strategies only'}`",
        f"- Non-forex products found in source: `{', '.join(sorted(non_forex_products)) if non_forex_products else 'none'}`",
        f"- Generated/suffixed strategies found in source: `{len(generated_strategies)}`",
        "- Rule: open current #1 at/after cutoff; keep holding while held product/strategy remains in current top 3; replace with current #1 when held drops out of top 3.",
        "- Ranking: latest `net` per product/strategy at snapshot `last_update`, sorted by net descending, then product, then strategy.",
        "- Scoring: final held strategy net at final snapshot of day minus `$50` per replacement switch.",
        "",
        "## Summary",
        "",
        "| First open cutoff | Total net | Avg/day | Opened days | Switches | Days |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary_rows:
        lines.append(
            f"| {int(row['open_hour']):02d}:00 | {row['total_net']:,.0f} | {row['avg_day']:,.0f} | "
            f"{int(row['opened_days'])} | {int(row['switches'])} | {int(row['days'])} |"
        )

    lines.extend(
        [
            "",
            "## Switch Event Sample",
            "",
            "| Date | Time | Event | From | From rank | From net | To | To net |",
            "|---|---|---|---|---:|---:|---|---:|",
        ]
    )
    for event in event_rows[:30]:
        from_label = (
            f"{event['from_product']} / {event['from_strategy']}"
            if event.get("from_product")
            else ""
        )
        to_label = f"{event['to_product']} / {event['to_strategy']}"
        lines.append(
            f"| {event['date']} | {event['time'][11:19]} | {event['event']} | {from_label} | "
            f"{event['from_rank']} | {event['from_net']} | {to_label} | {event['to_net']} |"
        )

    lines.extend(["", "## Per-Day Results", ""])
    for open_hour in sorted({int(row["open_hour"]) for row in day_rows}):
        lines.extend(
            [
                f"### First open at/after {open_hour:02d}:00",
                "",
                "| Date | Net after cost | Gross final net | Switches | Final held | Snapshots |",
                "|---|---:|---:|---:|---|---:|",
            ]
        )
        for row in [r for r in day_rows if int(r["open_hour"]) == open_hour]:
            final_held = f"{row['held_product']} / {row['held_strategy']}" if row["held_product"] else ""
            lines.append(
                f"| {row['date']} | {row['net_after_switch_cost']:,.0f} | {row['gross_final_net']:,.0f} | "
                f"{int(row['switches'])} | {final_held} | {int(row['snapshot_count'])} |"
            )
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    open_hours = parse_open_hours(args.open_hours)
    date_whitelist = {part.strip() for part in args.dates.split(",") if part.strip()}
    files = iter_summary_files(args.source_dir, args.start_date, args.end_date, date_whitelist)
    snapshots, non_forex_products, generated_strategies, unreadable_count, contaminated_count = load_snapshots(
        files,
        args.include_non_forex,
        args.clean_files_only,
        args.include_generated_strategies,
    )

    snaps_by_date: dict[str, list[Snapshot]] = {}
    for snap in snapshots:
        snaps_by_date.setdefault(snap.date, []).append(snap)

    day_rows: list[dict[str, Any]] = []
    event_rows: list[dict[str, Any]] = []
    for open_hour in open_hours:
        for date in sorted(snaps_by_date):
            day_result, day_events = replay_day(snaps_by_date[date], open_hour, args.switch_cost)
            day_result["open_hour"] = open_hour
            day_rows.append(day_result)
            for event in day_events:
                event["open_hour"] = open_hour
            event_rows.extend(day_events)

    summary_rows: list[dict[str, Any]] = []
    for open_hour in open_hours:
        rows = [row for row in day_rows if int(row["open_hour"]) == open_hour]
        opened_days = sum(1 for row in rows if row["opened"])
        total_net = sum(float(row["net_after_switch_cost"]) for row in rows)
        switches = sum(int(row["switches"]) for row in rows)
        summary_rows.append(
            {
                "open_hour": open_hour,
                "total_net": total_net,
                "avg_day": total_net / len(rows) if rows else 0.0,
                "opened_days": opened_days,
                "switches": switches,
                "days": len(rows),
            }
        )

    stem = args.output_stem
    write_csv(OUT_DIR / f"{stem}_summary.csv", summary_rows)
    write_csv(OUT_DIR / f"{stem}_days.csv", day_rows)
    write_csv(OUT_DIR / f"{stem}_events.csv", event_rows)
    write_markdown(
        OUT_DIR / f"{stem}.md",
        summary_rows,
        day_rows,
        event_rows,
        args.source_dir,
        len(files),
        len(snapshots),
        unreadable_count,
        contaminated_count,
        non_forex_products,
        generated_strategies,
        args.include_non_forex,
        args.clean_files_only,
        args.include_generated_strategies,
    )

    for row in summary_rows:
        print(
            f"{int(row['open_hour']):02d}:00 total={row['total_net']:.0f} "
            f"avg_day={row['avg_day']:.0f} opened={row['opened_days']} switches={row['switches']} days={row['days']}"
        )
    print(f"files={len(files)} snapshots={len(snapshots)} skipped={unreadable_count}")
    print(f"contaminated_excluded={contaminated_count}")
    print(f"non_forex={','.join(sorted(non_forex_products)) if non_forex_products else 'none'}")
    print(f"generated_strategies={len(generated_strategies)}")


if __name__ == "__main__":
    main()
