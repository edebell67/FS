"""
Rank-1 switching grid search with first-open time cutoffs.

Valid switching criteria:
- net: switch when new rank-1 net > held rank-1 net + net_threshold.
- gap: switch when new rank-1 cumulative rank-1 count > held cumulative count + gap_threshold.
- and/or: combine both criteria explicitly.

No implicit fallback is used when held comparison data is missing.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT / "data" / "processed"
OUT_DIR = Path(__file__).resolve().parent
DEFAULT_NET_THRESHOLDS = [0, 25, 50, 75, 100, 150, 200, 300, 500]
DEFAULT_GAP_THRESHOLDS = [0, 5, 10, 15, 20, 25, 50]


@dataclass(frozen=True)
class Snapshot:
    minute_of_day: int
    rank1_key: tuple[str, str] | None
    rank1_net: float | None
    nets_by_key: dict[tuple[str, str], float]
    rank1_counts_by_key: dict[tuple[str, str], int]


@dataclass(frozen=True)
class DayData:
    product_type: str
    date: str
    snapshots: list[Snapshot]
    final_net_by_key: dict[tuple[str, str], float]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--product-type", default="forex", help="Processed product type prefix, e.g. forex.")
    parser.add_argument("--start-date", default="2026-03-21")
    parser.add_argument("--end-date", default="2026-04-17")
    parser.add_argument("--open-hours", default="1,2,3", help="Comma-separated first-open hours.")
    parser.add_argument("--rule-family", choices=["net", "gap", "and", "or"], default="net")
    parser.add_argument(
        "--net-thresholds",
        default=",".join(str(v) for v in DEFAULT_NET_THRESHOLDS),
        help="Comma-separated net-gap thresholds.",
    )
    parser.add_argument(
        "--gap-thresholds",
        default=",".join(str(v) for v in DEFAULT_GAP_THRESHOLDS),
        help="Comma-separated rank1-count gap thresholds.",
    )
    parser.add_argument("--switch-cost", type=float, default=50.0)
    parser.add_argument("--output-stem", default="rank1_open_time_grid_search")
    return parser.parse_args()


def parse_int_list(value: str) -> list[int]:
    return [int(part.strip()) for part in value.split(",") if part.strip()]


def load_day(path: Path) -> DayData:
    df = pd.read_parquet(
        path,
        columns=["snap_idx", "minute_of_day", "product", "strategy", "net", "rank", "rank1_count_cum"],
    ).sort_values("snap_idx")
    product_type, date = path.stem.split("_", 1)

    final_net_by_key: dict[tuple[str, str], float] = {}
    for row in df.itertuples(index=False):
        final_net_by_key[(row.product, row.strategy)] = float(row.net)

    snapshots: list[Snapshot] = []
    for _, snap_df in df.groupby("snap_idx", sort=True):
        minute_of_day = int(snap_df["minute_of_day"].iloc[0])
        nets_by_key = {
            (row.product, row.strategy): float(row.net)
            for row in snap_df.itertuples(index=False)
        }
        rank1_counts_by_key = {
            (row.product, row.strategy): int(row.rank1_count_cum)
            for row in snap_df.itertuples(index=False)
        }
        rank1_df = snap_df[(snap_df["rank"] == 1) & (snap_df["net"] > 0)]
        if rank1_df.empty:
            rank1_key = None
            rank1_net = None
        else:
            rank1 = rank1_df.iloc[0]
            rank1_key = (str(rank1["product"]), str(rank1["strategy"]))
            rank1_net = float(rank1["net"])
        snapshots.append(
            Snapshot(
                minute_of_day=minute_of_day,
                rank1_key=rank1_key,
                rank1_net=rank1_net,
                nets_by_key=nets_by_key,
                rank1_counts_by_key=rank1_counts_by_key,
            )
        )

    return DayData(
        product_type=product_type,
        date=date,
        snapshots=snapshots,
        final_net_by_key=final_net_by_key,
    )


def load_days(product_type: str, start_date: str, end_date: str) -> list[DayData]:
    days: list[DayData] = []
    for path in sorted(PROCESSED_DIR.glob(f"{product_type}_*.parquet")):
        _, date = path.stem.split("_", 1)
        if start_date <= date <= end_date:
            days.append(load_day(path))
    return days


def run_rank1_filtered(
    days: list[DayData],
    rule_family: str,
    net_threshold: int | None,
    gap_threshold: int | None,
    open_hour: int,
    switch_cost: float,
) -> dict[str, float | int]:
    open_minute = open_hour * 60
    total_net = 0.0
    total_switches = 0
    opened_days = 0
    skipped_days = 0

    for day in days:
        held_key: tuple[str, str] | None = None
        switches = 0

        for snap in day.snapshots:
            if snap.minute_of_day < open_minute or snap.rank1_key is None:
                continue

            if held_key is None:
                held_key = snap.rank1_key
                opened_days += 1
                continue

            if snap.rank1_key == held_key:
                continue

            held_net = snap.nets_by_key.get(held_key)
            held_gap = snap.rank1_counts_by_key.get(held_key)
            new_gap = snap.rank1_counts_by_key.get(snap.rank1_key)

            net_fires = (
                snap.rank1_net is not None
                and held_net is not None
                and net_threshold is not None
                and snap.rank1_net > held_net + net_threshold
            )
            gap_fires = (
                held_gap is not None
                and new_gap is not None
                and gap_threshold is not None
                and new_gap > held_gap + gap_threshold
            )

            if rule_family == "net":
                should_switch = net_fires
            elif rule_family == "gap":
                should_switch = gap_fires
            elif rule_family == "and":
                should_switch = net_fires and gap_fires
            else:
                should_switch = net_fires or gap_fires

            if should_switch:
                held_key = snap.rank1_key
                switches += 1

        if held_key is None:
            skipped_days += 1
            continue

        total_net += day.final_net_by_key.get(held_key, 0.0) - (switches * switch_cost)
        total_switches += switches

    day_count = len(days)
    return {
        "open_hour": open_hour,
        "rule_family": rule_family,
        "net_threshold": net_threshold if net_threshold is not None else "",
        "gap_threshold": gap_threshold if gap_threshold is not None else "",
        "total_net": total_net,
        "avg_day": total_net / day_count if day_count else 0.0,
        "switches": total_switches,
        "days": day_count,
        "opened_days": opened_days,
        "skipped_days": skipped_days,
    }


def format_rule(rule_family: str, net_threshold: int | str | None, gap_threshold: int | str | None) -> str:
    net_part = f"net>{net_threshold}" if net_threshold != "" and net_threshold is not None else ""
    gap_part = f"gap>{gap_threshold}" if gap_threshold != "" and gap_threshold is not None else ""
    if rule_family == "net":
        return f"rank-1 + {net_part}"
    if rule_family == "gap":
        return f"rank-1 + {gap_part}"
    joiner = " AND " if rule_family == "and" else " OR "
    return f"rank-1 + {net_part}{joiner}{gap_part}"


def write_markdown(results: pd.DataFrame, path: Path, product_type: str, start_date: str, end_date: str, rule_family: str) -> None:
    best_by_hour = results.sort_values(["open_hour", "total_net"], ascending=[True, False]).groupby("open_hour").head(1)
    lines = [
        "# Rank-1 First-Open Time Grid Search",
        "",
        f"- Product type: `{product_type}`",
        f"- Test window: `{start_date}` to `{end_date}`",
        f"- Rule family: `{rule_family}`",
        "- Rule: first positive rank-1 opens at/after cutoff; later switches require rank-1 change and the configured valid criterion.",
        "- No implicit missing-held-net fallback is used.",
        "- Switch cost: `$50` per switch",
        "",
        "## Best By First-Open Cutoff",
        "",
        "| First open cutoff | Best rule | Total net | Avg/day | Switches | Days |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in best_by_hour.itertuples(index=False):
        lines.append(
            f"| {int(row.open_hour):02d}:00 | {row.rule} | "
            f"{row.total_net:,.0f} | {row.avg_day:,.0f} | {int(row.switches)} | {int(row.days)} |"
        )

    lines.extend(["", "## Full Results", ""])
    for open_hour, group in results.groupby("open_hour", sort=True):
        lines.extend(
            [
                f"### First open at/after {int(open_hour):02d}:00",
                "",
                "| Rule | Total net | Avg/day | Switches | Opened days | Skipped days |",
                "|---|---:|---:|---:|---:|---:|",
            ]
        )
        for row in group.itertuples(index=False):
            lines.append(
                f"| {row.rule} | {row.total_net:,.0f} | "
                f"{row.avg_day:,.0f} | {int(row.switches)} | {int(row.opened_days)} | {int(row.skipped_days)} |"
            )
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    product_type = str(args.product_type).strip().lower()
    open_hours = parse_int_list(args.open_hours)
    net_thresholds = parse_int_list(args.net_thresholds)
    gap_thresholds = parse_int_list(args.gap_thresholds)
    days = load_days(product_type, args.start_date, args.end_date)
    if not days:
        raise SystemExit(f"No processed day files found for {product_type} between {args.start_date} and {args.end_date}")

    rows = []
    for open_hour in open_hours:
        if args.rule_family == "net":
            for net_threshold in net_thresholds:
                rows.append(run_rank1_filtered(days, "net", net_threshold, None, open_hour, args.switch_cost))
        elif args.rule_family == "gap":
            for gap_threshold in gap_thresholds:
                rows.append(run_rank1_filtered(days, "gap", None, gap_threshold, open_hour, args.switch_cost))
        else:
            for net_threshold in net_thresholds:
                for gap_threshold in gap_thresholds:
                    rows.append(run_rank1_filtered(days, args.rule_family, net_threshold, gap_threshold, open_hour, args.switch_cost))
    results = pd.DataFrame(rows)
    results["rule"] = results.apply(
        lambda row: format_rule(str(row["rule_family"]), row["net_threshold"], row["gap_threshold"]),
        axis=1,
    )
    results = results[
        [
            "open_hour",
            "rule_family",
            "net_threshold",
            "gap_threshold",
            "rule",
            "total_net",
            "avg_day",
            "switches",
            "days",
            "opened_days",
            "skipped_days",
        ]
    ]

    csv_path = OUT_DIR / f"{args.output_stem}_{product_type}.csv"
    md_path = OUT_DIR / f"{args.output_stem}_{product_type}.md"
    results.to_csv(csv_path, index=False)
    write_markdown(results, md_path, product_type, args.start_date, args.end_date, args.rule_family)

    print(f"Loaded {len(days)} {product_type} days")
    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")
    print()
    print(results.to_string(index=False, formatters={
        "total_net": "{:.0f}".format,
        "avg_day": "{:.0f}".format,
    }))


if __name__ == "__main__":
    main()
