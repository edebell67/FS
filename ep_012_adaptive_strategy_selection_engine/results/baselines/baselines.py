"""
Phase 2: Baselines — Adaptive Strategy Selection Engine
Implements Baseline A (persistent positive leader) and Baseline B (conservative hold-with-threshold).
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
import pandas as pd
import numpy as np

EPIC_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = EPIC_DIR / "data" / "config" / "config.json"
PROCESSED_DIR = EPIC_DIR / "data" / "processed"
OUTPUT_DIR = Path(__file__).parent

with open(CONFIG_PATH) as f:
    CFG = json.load(f)

SWITCHING_COST = CFG["switching_cost"]      # 50
SAFETY_MARGIN  = CFG["safety_margin"]        # 5
SWITCH_THRESHOLD = SWITCHING_COST + SAFETY_MARGIN  # 55
MIN_TRAIN_DAYS = CFG["min_train_days"]
PRODUCT_TYPES  = CFG["product_types"]


def load_all_processed():
    files = sorted(PROCESSED_DIR.glob("*.parquet"))
    if not files:
        sys.exit("ERROR: No parquet files. Run Phase 1 first.")
    df = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def walk_forward_splits(dates, min_train=5):
    dates = sorted(dates)
    for i in range(min_train, len(dates)):
        yield dates[:i], dates[i]


def baseline_a(day_df):
    """Persistent positive leader — picks most-frequent rank-1 eligible candidate each snapshot."""
    decisions = []
    snaps = sorted(day_df["snap_idx"].unique())
    rank1_counts = defaultdict(int)
    for snap in snaps:
        snap_df = day_df[day_df["snap_idx"] == snap]
        for _, row in snap_df[snap_df["rank"] == 1].iterrows():
            rank1_counts[(row["product"], row["strategy"])] += 1
        eligible = snap_df[snap_df["net"] > 0].copy()
        if eligible.empty:
            decisions.append({"snap_idx": snap, "action": "FLAT", "product": None, "strategy": None, "net": 0.0})
            continue
        eligible["r1_count"] = eligible.apply(
            lambda r: rank1_counts.get((r["product"], r["strategy"]), 0), axis=1
        )
        best = eligible.sort_values(["r1_count", "net"], ascending=False).iloc[0]
        decisions.append({
            "snap_idx": snap, "action": "SWITCH",
            "product": best["product"], "strategy": best["strategy"], "net": float(best["net"])
        })
    return decisions


def baseline_b(day_df, switching_cost=50, safety_margin=5):
    """Conservative hold — only switch when challenger exceeds held + threshold."""
    threshold_gap = switching_cost + safety_margin
    decisions = []
    snaps = sorted(day_df["snap_idx"].unique())
    held_product = None
    held_strategy = None
    for snap in snaps:
        snap_df = day_df[day_df["snap_idx"] == snap]
        eligible = snap_df[snap_df["net"] > 0].copy()
        held_net = None
        if held_product and held_strategy:
            held_row = snap_df[
                (snap_df["product"] == held_product) & (snap_df["strategy"] == held_strategy)
            ]
            if not held_row.empty:
                v = float(held_row.iloc[0]["net"])
                held_net = v if v > 0 else None
        if held_net is not None:
            challengers = eligible[
                ~((eligible["product"] == held_product) & (eligible["strategy"] == held_strategy))
            ]
            if not challengers.empty:
                best = challengers.sort_values("net", ascending=False).iloc[0]
                if float(best["net"]) > held_net + threshold_gap:
                    held_product, held_strategy = best["product"], best["strategy"]
                    decisions.append({
                        "snap_idx": snap, "action": "SWITCH",
                        "product": held_product, "strategy": held_strategy, "net": float(best["net"])
                    })
                    continue
            decisions.append({
                "snap_idx": snap, "action": "HOLD",
                "product": held_product, "strategy": held_strategy, "net": held_net
            })
        else:
            if eligible.empty:
                held_product = held_strategy = None
                decisions.append({"snap_idx": snap, "action": "FLAT", "product": None, "strategy": None, "net": 0.0})
            else:
                best = eligible.sort_values("net", ascending=False).iloc[0]
                held_product, held_strategy = best["product"], best["strategy"]
                decisions.append({
                    "snap_idx": snap, "action": "SWITCH",
                    "product": held_product, "strategy": held_strategy, "net": float(best["net"])
                })
    return decisions


def simulate(decisions, day_df, switching_cost=50):
    """Simulate cumulative outcome for a decision series."""
    switch_count = 0
    for i, d in enumerate(decisions):
        if d["action"] == "SWITCH" and i > 0:
            prev = decisions[i - 1]
            if prev["action"] != "FLAT" and (prev["product"] != d["product"] or prev["strategy"] != d["strategy"]):
                switch_count += 1
    hold_durations = []
    start = None
    last_key = None
    for d in decisions:
        key = (d["product"], d["strategy"]) if d["action"] != "FLAT" else None
        if key != last_key:
            if last_key is not None and start is not None:
                hold_durations.append(d["snap_idx"] - start)
            start = d["snap_idx"] if key else None
        last_key = key
    if last_key and start is not None and decisions:
        hold_durations.append(decisions[-1]["snap_idx"] - start)
    positive_survivals = []
    for i, d in enumerate(decisions):
        if d["action"] == "FLAT":
            continue
        if i + 1 < len(decisions):
            next_snap = decisions[i + 1]["snap_idx"]
            ndf = day_df[
                (day_df["snap_idx"] == next_snap) &
                (day_df["product"] == d["product"]) &
                (day_df["strategy"] == d["strategy"])
            ]
            if not ndf.empty:
                positive_survivals.append(float(ndf.iloc[0]["net"]) > 0)
    final = next((d for d in reversed(decisions) if d["action"] != "FLAT"), None)
    day_net = (float(final["net"]) if final else 0.0) - switch_count * switching_cost
    return {
        "day_net": day_net,
        "switch_count": switch_count,
        "avg_hold_duration": float(np.mean(hold_durations)) if hold_durations else 0.0,
        "positive_survival_rate": float(np.mean(positive_survivals)) if positive_survivals else 0.0,
        "flat_count": sum(1 for d in decisions if d["action"] == "FLAT"),
        "total_snaps": len(decisions),
    }


def main():
    print("=" * 60)
    print("Phase 2: Baselines")
    print("=" * 60)

    df = load_all_processed()
    print(f"Loaded {len(df)} rows, {df['date'].nunique()} dates, {df['product_type'].nunique()} product types")

    daily_rows = []

    for pt in PRODUCT_TYPES:
        pt_df = df[df["product_type"] == pt]
        if pt_df.empty:
            continue
        dates = sorted(pt_df["date"].unique().tolist())
        splits = list(walk_forward_splits(dates, MIN_TRAIN_DAYS))
        print(f"\n{pt}: {len(dates)} dates -> {len(splits)} test folds")

        for train_dates, test_date in splits:
            day_df = pt_df[pt_df["date"] == test_date].copy()
            if day_df.empty:
                continue
            dec_a = baseline_a(day_df)
            dec_b = baseline_b(day_df, SWITCHING_COST, SAFETY_MARGIN)
            sim_a = simulate(dec_a, day_df, SWITCHING_COST)
            sim_b = simulate(dec_b, day_df, SWITCHING_COST)
            daily_rows.append({
                "product_type": pt, "date": test_date,
                "baseline_a_net": sim_a["day_net"], "baseline_b_net": sim_b["day_net"],
                "baseline_a_switches": sim_a["switch_count"], "baseline_b_switches": sim_b["switch_count"],
                "baseline_a_hold_avg": sim_a["avg_hold_duration"], "baseline_b_hold_avg": sim_b["avg_hold_duration"],
                "baseline_a_positive_rate": sim_a["positive_survival_rate"],
                "baseline_b_positive_rate": sim_b["positive_survival_rate"],
            })
            print(f"  {test_date}: A={sim_a['day_net']:.1f} sw={sim_a['switch_count']} | "
                  f"B={sim_b['day_net']:.1f} sw={sim_b['switch_count']}")

    if not daily_rows:
        sys.exit("ERROR: No results produced.")

    results_df = pd.DataFrame(daily_rows)

    csv_path = OUTPUT_DIR / "daily_results_baselines.csv"
    results_df.to_csv(csv_path, index=False)
    print(f"\nSaved daily CSV: {csv_path} ({len(results_df)} rows)")
    print(f"Null check: {results_df[['baseline_a_net','baseline_b_net']].isnull().sum().to_dict()}")

    total_a = float(results_df["baseline_a_net"].sum())
    total_b = float(results_df["baseline_b_net"].sum())
    agg = {
        "total_net_a": round(total_a, 2),
        "total_net_b": round(total_b, 2),
        "total_switches_a": int(results_df["baseline_a_switches"].sum()),
        "total_switches_b": int(results_df["baseline_b_switches"].sum()),
        "days_tested": len(results_df),
        "best_baseline": "A" if total_a >= total_b else "B",
        "avg_net_per_day_a": round(total_a / len(results_df), 2),
        "avg_net_per_day_b": round(total_b / len(results_df), 2),
        "baseline_b_switches_less_than_a": bool(
            results_df["baseline_b_switches"].sum() < results_df["baseline_a_switches"].sum()
        ),
    }
    json_path = OUTPUT_DIR / "aggregate_baselines.json"
    with open(json_path, "w") as f:
        json.dump(agg, f, indent=2)
    print(f"Saved aggregate JSON: {json_path}")
    print(json.dumps(agg, indent=2))
    print(f"\nBaseline B switches ({agg['total_switches_b']}) < A ({agg['total_switches_a']}): "
          f"{agg['baseline_b_switches_less_than_a']}")
    print("\nPhase 2 COMPLETE")


if __name__ == "__main__":
    main()
