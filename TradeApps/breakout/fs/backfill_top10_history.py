#!/usr/bin/env python3
"""
Backfill _top10_history.json from _summary_net.json data.

Reconstructs historical top10 snapshots with pick_now evaluation
to analyze strategy selection effectiveness throughout the trading day.

Usage:
    python backfill_top10_history.py --date 2026-03-24 --mode live --product-type forex
    python backfill_top10_history.py --date 2026-03-24 --analyze  # Show pick_now effectiveness
"""

import json
import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Any, Optional, Tuple
import argparse

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_BASE = os.path.join(SCRIPT_DIR, "json")
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")


def load_config() -> Dict[str, Any]:
    """Load configuration from config.json."""
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def load_pick_now_config() -> Dict[str, Any]:
    """Load pick_now thresholds from config."""
    config = load_config()
    return config.get("pick_now", {
        "min_appearances": 20,
        "min_net_trend": 100,
        "min_snapshots": 60
    })


def get_day_dir(mode: str, product_type: str, date_str: str) -> str:
    """Get the directory path for a specific day's data."""
    return os.path.join(JSON_BASE, mode, product_type, date_str)


def load_summary_net(day_dir: str) -> Optional[Dict[str, Any]]:
    """Load _summary_net.json for a day."""
    path = os.path.join(day_dir, "_summary_net.json")
    if not os.path.exists(path):
        print(f"Error: {path} not found")
        return None
    with open(path, "r") as f:
        return json.load(f)


def extract_all_timestamps(summary_net: Dict[str, Any]) -> List[datetime]:
    """Extract all unique timestamps from summary_net data."""
    timestamps = set()
    strategies = summary_net.get("strategies", {})

    for strategy_name, products in strategies.items():
        for product, snapshots in products.items():
            for snap in snapshots:
                ts_str = snap.get("t")
                if ts_str:
                    try:
                        ts = datetime.fromisoformat(ts_str)
                        timestamps.add(ts)
                    except ValueError:
                        continue

    return sorted(timestamps)


def group_timestamps_to_intervals(timestamps: List[datetime], interval_minutes: int = 5) -> List[datetime]:
    """Group timestamps into interval buckets, return representative timestamp for each bucket."""
    if not timestamps:
        return []

    buckets = []
    current_bucket_start = None

    for ts in timestamps:
        # Round down to nearest interval
        bucket = ts.replace(
            minute=(ts.minute // interval_minutes) * interval_minutes,
            second=0,
            microsecond=0
        )

        if current_bucket_start is None or bucket > current_bucket_start:
            current_bucket_start = bucket
            buckets.append(ts)  # Use actual timestamp as representative

    return buckets


def get_strategy_state_at_time(
    summary_net: Dict[str, Any],
    target_time: datetime
) -> List[Dict[str, Any]]:
    """Get the state of all strategies at a specific point in time."""
    strategies = summary_net.get("strategies", {})
    results = []

    for strategy_name, products in strategies.items():
        # Skip DNA strategies
        if "dna" in strategy_name.lower():
            continue

        for product, snapshots in products.items():
            # Find the last snapshot at or before target_time
            last_snap = None
            for snap in snapshots:
                ts_str = snap.get("t")
                if ts_str:
                    try:
                        ts = datetime.fromisoformat(ts_str)
                        if ts <= target_time:
                            last_snap = snap
                        else:
                            break  # Snapshots are ordered by time
                    except ValueError:
                        continue

            if last_snap:
                results.append({
                    "strategy": strategy_name,
                    "product": product,
                    "net": last_snap.get("net", 0),
                    "buy_count": last_snap.get("b_c", 0),
                    "sell_count": last_snap.get("s_c", 0),
                    "timestamp": last_snap.get("t")
                })

    return results


def calculate_net_trend(history: List[float]) -> float:
    """Calculate net trend from a list of net values."""
    if len(history) < 2:
        return 0.0

    # Simple: last value minus first value
    return history[-1] - history[0]


def evaluate_pick_now(
    strategy_key: str,
    appearances: int,
    net_trend: float,
    total_snapshots: int,
    config: Dict[str, Any]
) -> bool:
    """Evaluate if a strategy meets pick_now criteria."""
    min_appearances = config.get("min_appearances", 20)
    min_net_trend = config.get("min_net_trend", 100)
    min_snapshots = config.get("min_snapshots", 60)

    return (
        appearances >= min_appearances and
        net_trend > min_net_trend and
        total_snapshots >= min_snapshots
    )


def backfill_top10_history(
    mode: str,
    product_type: str,
    date_str: str,
    interval_minutes: int = 5,
    top_n: int = 10,
    config_override: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Backfill _top10_history.json from _summary_net.json data.

    Returns the reconstructed history with pick_now evaluations.
    """
    day_dir = get_day_dir(mode, product_type, date_str)
    summary_net = load_summary_net(day_dir)

    if not summary_net:
        return None

    pick_now_config = load_pick_now_config()
    # Apply overrides
    if config_override:
        pick_now_config.update(config_override)
    print(f"Using pick_now config: {pick_now_config}")

    # Extract and group timestamps
    all_timestamps = extract_all_timestamps(summary_net)
    print(f"Found {len(all_timestamps)} unique timestamps in _summary_net.json")

    interval_timestamps = group_timestamps_to_intervals(all_timestamps, interval_minutes)
    print(f"Grouped into {len(interval_timestamps)} {interval_minutes}-minute intervals")

    # Track appearances and net history for each strategy-product
    appearances_tracker: Dict[str, int] = defaultdict(int)
    net_history_tracker: Dict[str, List[float]] = defaultdict(list)

    history = []

    for idx, ts in enumerate(interval_timestamps):
        snapshot_num = idx + 1

        # Get all strategies' state at this time
        all_strategies = get_strategy_state_at_time(summary_net, ts)

        # Sort by net descending and take top N
        sorted_strategies = sorted(all_strategies, key=lambda x: x["net"], reverse=True)
        top_strategies = sorted_strategies[:top_n]

        # Update trackers and evaluate pick_now for top strategies
        top10_entries = []
        for strat in top_strategies:
            key = f"{strat['strategy']}|{strat['product']}"

            # Update trackers
            appearances_tracker[key] += 1
            net_history_tracker[key].append(strat["net"])

            # Calculate metrics for pick_now
            appearances = appearances_tracker[key]
            net_trend = calculate_net_trend(net_history_tracker[key])

            # Evaluate pick_now
            pick_now = evaluate_pick_now(
                key,
                appearances,
                net_trend,
                snapshot_num,
                pick_now_config
            )

            top10_entries.append({
                "strategy": strat["strategy"],
                "product": strat["product"],
                "net": strat["net"],
                "pick_now": pick_now,
                "appearances": appearances,
                "net_trend": round(net_trend, 2),
                "snapshot_num": snapshot_num
            })

        history.append({
            "timestamp": ts.isoformat(),
            "snapshot_num": snapshot_num,
            "top10": top10_entries
        })

    result = {
        "version": "backfilled",
        "backfill_time": datetime.now().isoformat(),
        "config_used": pick_now_config,
        "total_snapshots": len(history),
        "history": history,
        "date": date_str
    }

    return result


def analyze_pick_now_effectiveness(history_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze how effective pick_now would have been.

    Tracks:
    - When each strategy first got pick_now=True
    - What happened to that strategy's net after pick_now
    - Whether it stayed in top 10 throughout
    - Whether net ever dropped below pick price
    - Overall success rate
    """
    history = history_data.get("history", [])
    if not history:
        return {"error": "No history data"}

    # Track when strategies first got pick_now
    first_pick_now: Dict[str, Dict] = {}

    # Track final state of each strategy
    final_snapshot = history[-1] if history else {}
    final_top10 = {
        f"{e['strategy']}|{e['product']}": e
        for e in final_snapshot.get("top10", [])
    }

    # Find all strategies that ever had pick_now=True
    for snap in history:
        for entry in snap.get("top10", []):
            key = f"{entry['strategy']}|{entry['product']}"
            if entry.get("pick_now") and key not in first_pick_now:
                first_pick_now[key] = {
                    "strategy": entry["strategy"],
                    "product": entry["product"],
                    "pick_now_at_snapshot": snap.get("snapshot_num"),
                    "pick_now_at_time": snap.get("timestamp"),
                    "net_at_pick": entry["net"],
                    "appearances_at_pick": entry.get("appearances", 0),
                    "net_trend_at_pick": entry.get("net_trend", 0)
                }

    # Calculate outcomes with detailed tracking
    results = []
    for key, pick_info in first_pick_now.items():
        pick_snapshot = pick_info["pick_now_at_snapshot"]
        net_at_pick = pick_info["net_at_pick"]

        # Track performance after pick
        stayed_in_top10 = True
        stayed_above_pick_net = True
        min_net_after_pick = net_at_pick
        max_net_after_pick = net_at_pick
        snapshots_in_top10 = 0
        snapshots_above_pick_net = 0
        total_snapshots_after_pick = 0
        last_seen_net = net_at_pick
        last_seen_snapshot = pick_snapshot

        # Scan all snapshots after the pick
        for snap in history:
            snap_num = snap.get("snapshot_num", 0)
            if snap_num <= pick_snapshot:
                continue

            total_snapshots_after_pick += 1

            # Find this strategy in this snapshot
            found = False
            for entry in snap.get("top10", []):
                entry_key = f"{entry['strategy']}|{entry['product']}"
                if entry_key == key:
                    found = True
                    snapshots_in_top10 += 1
                    current_net = entry["net"]
                    last_seen_net = current_net
                    last_seen_snapshot = snap_num

                    if current_net >= net_at_pick:
                        snapshots_above_pick_net += 1
                    else:
                        stayed_above_pick_net = False

                    min_net_after_pick = min(min_net_after_pick, current_net)
                    max_net_after_pick = max(max_net_after_pick, current_net)
                    break

            if not found:
                stayed_in_top10 = False

        final_entry = final_top10.get(key)
        if final_entry:
            final_net = final_entry["net"]
            net_change = final_net - net_at_pick
            still_in_top10_at_end = True
        else:
            final_net = last_seen_net
            net_change = last_seen_net - net_at_pick
            still_in_top10_at_end = False

        # Determine outcome
        if still_in_top10_at_end and net_change > 0:
            outcome = "WIN"
        elif still_in_top10_at_end and net_change < 0:
            outcome = "LOSS"
        elif still_in_top10_at_end and net_change == 0:
            outcome = "FLAT"
        else:
            # Dropped - but check if net was above pick when last seen
            if net_change > 0:
                outcome = "DROPPED_UP"
            elif net_change < 0:
                outcome = "DROPPED_DOWN"
            else:
                outcome = "DROPPED_FLAT"

        results.append({
            **pick_info,
            "final_net": final_net,
            "net_change_after_pick": net_change,
            "still_in_top10_at_end": still_in_top10_at_end,
            "stayed_in_top10_always": stayed_in_top10,
            "stayed_above_pick_net": stayed_above_pick_net,
            "min_net_after_pick": min_net_after_pick,
            "max_net_after_pick": max_net_after_pick,
            "snapshots_in_top10": snapshots_in_top10,
            "snapshots_above_pick_net": snapshots_above_pick_net,
            "total_snapshots_after_pick": total_snapshots_after_pick,
            "last_seen_snapshot": last_seen_snapshot,
            "outcome": outcome
        })

    # Summary stats
    wins = sum(1 for r in results if r["outcome"] == "WIN")
    losses = sum(1 for r in results if r["outcome"] == "LOSS")
    dropped_up = sum(1 for r in results if r["outcome"] == "DROPPED_UP")
    dropped_down = sum(1 for r in results if r["outcome"] == "DROPPED_DOWN")
    dropped_flat = sum(1 for r in results if r["outcome"] == "DROPPED_FLAT")

    stayed_in_top10_always = sum(1 for r in results if r["stayed_in_top10_always"])
    stayed_above_pick_net = sum(1 for r in results if r["stayed_above_pick_net"])
    still_in_top10_at_end = sum(1 for r in results if r["still_in_top10_at_end"])

    # Net change includes all strategies (using last seen net for dropped ones)
    total_net_change = sum(r["net_change_after_pick"] for r in results)

    # Calculate "above pick net" at last observation
    above_pick_at_last = sum(1 for r in results if r["net_change_after_pick"] >= 0)

    return {
        "total_strategies_picked": len(results),
        "wins": wins,
        "losses": losses,
        "dropped_up": dropped_up,
        "dropped_down": dropped_down,
        "dropped_flat": dropped_flat,
        "stayed_in_top10_always": stayed_in_top10_always,
        "stayed_above_pick_net_always": stayed_above_pick_net,
        "still_in_top10_at_end": still_in_top10_at_end,
        "above_pick_net_at_last_observation": above_pick_at_last,
        "win_rate": f"{(wins / len(results) * 100):.1f}%" if results else "N/A",
        "total_net_change_after_picks": total_net_change,
        "details": sorted(results, key=lambda x: x["pick_now_at_snapshot"])
    }


def main():
    parser = argparse.ArgumentParser(description="Backfill _top10_history.json with pick_now evaluation")
    parser.add_argument("--date", type=str, help="Date to backfill (YYYY-MM-DD)",
                       default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--mode", type=str, default="live", choices=["live", "sim"])
    parser.add_argument("--product-type", type=str, default="forex",
                       choices=["forex", "crypto", "energy", "indices", "metals"])
    parser.add_argument("--interval", type=int, default=5, help="Interval in minutes")
    parser.add_argument("--top-n", type=int, default=10, help="Number of top strategies to track")
    parser.add_argument("--output", type=str, help="Output file path (default: overwrite existing)")
    parser.add_argument("--analyze", action="store_true", help="Analyze pick_now effectiveness")
    parser.add_argument("--dry-run", action="store_true", help="Don't write file, just show stats")
    parser.add_argument("--min-appearances", type=int, help="Override min appearances threshold")
    parser.add_argument("--min-net-trend", type=float, help="Override min net trend threshold")
    parser.add_argument("--min-snapshots", type=int, help="Override min snapshots threshold")

    args = parser.parse_args()

    print(f"Backfilling top10 history for {args.date} ({args.mode}/{args.product_type})")

    # Build config override from CLI args
    config_override = {}
    if args.min_appearances is not None:
        config_override["min_appearances"] = args.min_appearances
    if args.min_net_trend is not None:
        config_override["min_net_trend"] = args.min_net_trend
    if args.min_snapshots is not None:
        config_override["min_snapshots"] = args.min_snapshots

    # Run backfill
    result = backfill_top10_history(
        mode=args.mode,
        product_type=args.product_type,
        date_str=args.date,
        interval_minutes=args.interval,
        top_n=args.top_n,
        config_override=config_override if config_override else None
    )

    if not result:
        print("Backfill failed - no data")
        sys.exit(1)

    print(f"\nBackfilled {result['total_snapshots']} snapshots")

    # Show analysis
    if args.analyze or True:  # Always show analysis
        print("\n" + "=" * 70)
        print("PICK NOW EFFECTIVENESS ANALYSIS")
        print("=" * 70)

        analysis = analyze_pick_now_effectiveness(result)

        print(f"\nStrategies that received pick_now=True: {analysis['total_strategies_picked']}")
        print(f"\n  POSITION TRACKING:")
        print(f"    Still in top 10 at end:            {analysis['still_in_top10_at_end']}")
        print(f"    Stayed in top 10 ALWAYS:           {analysis['stayed_in_top10_always']}")
        print(f"    Stayed above pick net ALWAYS:      {analysis['stayed_above_pick_net_always']}")
        print(f"    Above pick net at last observation:{analysis['above_pick_net_at_last_observation']}")

        print(f"\n  OUTCOMES:")
        print(f"    WIN (in top10, net up):            {analysis['wins']}")
        print(f"    LOSS (in top10, net down):         {analysis['losses']}")
        print(f"    DROPPED_UP (left top10, net up):   {analysis['dropped_up']}")
        print(f"    DROPPED_DOWN (left top10, net down): {analysis['dropped_down']}")
        print(f"    DROPPED_FLAT (left top10, net same): {analysis['dropped_flat']}")

        print(f"\n  SUMMARY:")
        print(f"    Win Rate (in top10 at end):        {analysis['win_rate']}")
        print(f"    Total Net Change After Picks:      {analysis['total_net_change_after_picks']:.2f}")

        if analysis.get("details"):
            print("\n" + "-" * 130)
            print(f"{'Strategy':<35} {'Product':<12} {'Pick#':<6} {'Net@Pick':<9} {'Last Net':<9} {'Change':<8} {'InTop10':<8} {'AbovePick':<10} {'Result'}")
            print("-" * 130)

            for d in analysis["details"]:
                change_str = f"{d['net_change_after_pick']:+.1f}"
                final_str = f"{d['final_net']:.1f}"
                in_top10 = "always" if d['stayed_in_top10_always'] else f"{d['snapshots_in_top10']}/{d['total_snapshots_after_pick']}"
                above_pick = "always" if d['stayed_above_pick_net'] else f"{d['snapshots_above_pick_net']}/{d['snapshots_in_top10']}"
                print(f"{d['strategy']:<35} {d['product']:<12} #{d['pick_now_at_snapshot']:<5} {d['net_at_pick']:<9.1f} {final_str:<9} {change_str:<8} {in_top10:<8} {above_pick:<10} {d['outcome']}")

    # Write output
    if not args.dry_run:
        day_dir = get_day_dir(args.mode, args.product_type, args.date)
        output_path = args.output or os.path.join(day_dir, "_top10_history_backfilled.json")

        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

        print(f"\nWrote backfilled history to: {output_path}")
    else:
        print("\n[DRY RUN - no file written]")

    return result


if __name__ == "__main__":
    main()
