"""
Baseline B grid search across thresholds (net-based and rank1-based).
"""
import pandas as pd
from pathlib import Path
import sys

processed = Path(__file__).resolve().parents[2] / "data" / "processed"

def run_baseline(threshold, use_rank1=False):
    total = 0
    total_switches = 0
    days = 0
    for f in sorted(processed.glob("forex_*.parquet")):
        df = pd.read_parquet(f)
        df = df.sort_values("snap_idx")
        snaps = sorted(df["snap_idx"].unique())
        held_key = None
        switches = 0
        for snap in snaps:
            snap_df = df[df["snap_idx"] == snap]
            r1 = snap_df[snap_df["rank"] == 1]
            if r1.empty:
                continue
            if held_key is None:
                held_key = (r1.iloc[0]["product"], r1.iloc[0]["strategy"])
                continue
            held_row = snap_df[
                (snap_df["product"] == held_key[0]) &
                (snap_df["strategy"] == held_key[1])
            ]
            if held_row.empty:
                continue
            held_val = held_row.iloc[0]["rank1_count_cum"] if use_rank1 else held_row.iloc[0]["net"]
            best_chal = None
            best_val = -999999
            for _, row in snap_df.iterrows():
                key = (row["product"], row["strategy"])
                if key == held_key:
                    continue
                val = row["rank1_count_cum"] if use_rank1 else row["net"]
                if val > best_val:
                    best_val = val
                    best_chal = key
            if best_chal and (best_val - held_val) > threshold:
                held_key = best_chal
                switches += 1
        if held_key:
            held_df = df[(df["product"] == held_key[0]) & (df["strategy"] == held_key[1])]
            final_net = float(held_df.iloc[-1]["net"]) if not held_df.empty else 0.0
        else:
            final_net = 0.0
        total += final_net - switches * 50
        total_switches += switches
        days += 1
    return total, total_switches, days

print("NET-BASED THRESHOLDS")
print(f"{'Threshold':<14} {'Total Net':>10} {'Avg/day':>9} {'Switches':>9}")
print("-" * 46)
for t in [0, 25, 50, 55, 75, 100, 150, 200, 300, 500]:
    total, switches, days = run_baseline(t, use_rank1=False)
    print(f"net > {t:<8}  {total:>10.0f} {total/days:>9.0f} {switches:>9}")

print()
print("RANK1 GAP-BASED THRESHOLDS")
print(f"{'Threshold':<14} {'Total Net':>10} {'Avg/day':>9} {'Switches':>9}")
print("-" * 46)
for t in [0, 5, 10, 15, 20, 25, 50, 75, 100, 150, 200]:
    total, switches, days = run_baseline(t, use_rank1=True)
    print(f"r1 gap > {t:<5}  {total:>10.0f} {total/days:>9.0f} {switches:>9}")
