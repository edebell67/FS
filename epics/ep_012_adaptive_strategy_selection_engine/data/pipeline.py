"""
Phase 1: Data Engineering Pipeline
Adaptive Strategy Selection Engine

Ingests daily _frequency.json snapshot files, builds a flat minute-by-minute
candidate DataFrame, computes live-safe features, and saves per-day parquet files.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[3]  # eds/
CONFIG_PATH = Path(__file__).parent / "config" / "config.json"
OUTPUT_DIR = Path(__file__).parent / "processed"

with open(CONFIG_PATH) as f:
    CFG = json.load(f)

DATA_ROOT = REPO_ROOT / CFG["data_root"]
PRODUCT_TYPES = CFG["product_types"]
INTERVAL = CFG["snapshot_interval_minutes"]
SLOPE_WINDOWS = CFG["feature_slopes"]  # [3, 5, 10] in snapshots


# ---------------------------------------------------------------------------
# Step 1: Discover all _frequency.json files
# ---------------------------------------------------------------------------
def discover_files():
    found = {}
    for pt in PRODUCT_TYPES:
        pt_dir = DATA_ROOT / pt
        if not pt_dir.exists():
            continue
        for date_dir in sorted(pt_dir.iterdir()):
            if not date_dir.is_dir():
                continue
            try:
                datetime.strptime(date_dir.name, "%Y-%m-%d")
            except ValueError:
                continue
            freq_file = date_dir / "_frequency.json"
            if freq_file.exists():
                found[(pt, date_dir.name)] = freq_file
    return found


# ---------------------------------------------------------------------------
# Step 2: Parse snapshots into flat rows
# ---------------------------------------------------------------------------
def parse_frequency_file(path: Path, product_type: str, date: str) -> list:
    with open(path) as f:
        data = json.load(f)

    rows = []
    snapshots = data.get("snapshots", [])
    for snap_idx, snap in enumerate(snapshots):
        ts_str = snap.get("time")
        try:
            ts = datetime.fromisoformat(ts_str)
        except (TypeError, ValueError):
            continue
        leaders = snap.get("leaders", [])
        for leader in leaders:
            net = leader.get("net")
            if net is None:
                continue
            rows.append({
                "date": date,
                "product_type": product_type,
                "snap_idx": snap_idx,
                "timestamp": ts,
                "product": leader.get("product", "UNKNOWN"),
                "strategy": leader.get("strategy", "UNKNOWN"),
                "net": float(net),
                "rank": leader.get("rank"),
                "score": leader.get("score"),
                "score_rank": leader.get("score_rank"),
            })
    return rows


# ---------------------------------------------------------------------------
# Step 3 & 4: Feature engineering (live-safe, per candidate per snapshot)
# ---------------------------------------------------------------------------
def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    For each (product_type, date, product, strategy) group, compute rolling
    features using only past data (no future leakage).
    """
    all_groups = []

    for (product_type, date, product, strategy), grp in df.groupby(
        ["product_type", "date", "product", "strategy"], sort=False
    ):
        grp = grp.sort_values("snap_idx").copy()
        net = grp["net"].values
        score = grp["score"].fillna(0).values
        rank = grp["rank"].values
        n = len(grp)

        # --- slope helpers ---
        def slope(arr, idx, window):
            start = max(0, idx - window + 1)
            segment = arr[start: idx + 1]
            if len(segment) < 2:
                return 0.0
            x = np.arange(len(segment), dtype=float)
            return float(np.polyfit(x, segment, 1)[0])

        net_slope_3 = [slope(net, i, SLOPE_WINDOWS[0]) for i in range(n)]
        net_slope_5 = [slope(net, i, SLOPE_WINDOWS[1]) for i in range(n)]
        net_slope_10 = [slope(net, i, SLOPE_WINDOWS[2]) for i in range(n)]
        score_slope_3 = [slope(score, i, SLOPE_WINDOWS[0]) for i in range(n)]
        score_slope_5 = [slope(score, i, SLOPE_WINDOWS[1]) for i in range(n)]
        score_slope_10 = [slope(score, i, SLOPE_WINDOWS[2]) for i in range(n)]

        # rank delta
        rank_delta = [0.0] + [float(rank[i - 1] - rank[i]) for i in range(1, n)]  # positive = improved

        # positive streak (consecutive snaps with net > 0, up to and including current)
        positive_streak = []
        streak = 0
        for v in net:
            if v > 0:
                streak += 1
            else:
                streak = 0
            positive_streak.append(streak)

        # minutes since first appearance in top-5 for this day
        first_snap = grp["snap_idx"].iloc[0]
        mins_since_first_appearance = [(grp["snap_idx"].iloc[i] - first_snap) * INTERVAL for i in range(n)]

        # minutes since net first became > 0
        first_positive_snap = None
        mins_since_positive = []
        for i, v in enumerate(net):
            if v > 0 and first_positive_snap is None:
                first_positive_snap = grp["snap_idx"].iloc[i]
            if first_positive_snap is not None:
                mins_since_positive.append((grp["snap_idx"].iloc[i] - first_positive_snap) * INTERVAL)
            else:
                mins_since_positive.append(-1)  # not yet positive

        grp = grp.assign(
            net_slope_3=net_slope_3,
            net_slope_5=net_slope_5,
            net_slope_10=net_slope_10,
            score_slope_3=score_slope_3,
            score_slope_5=score_slope_5,
            score_slope_10=score_slope_10,
            rank_delta=rank_delta,
            positive_streak=positive_streak,
            mins_since_first_appearance=mins_since_first_appearance,
            mins_since_positive=mins_since_positive,
        )
        all_groups.append(grp)

    if not all_groups:
        return df

    result = pd.concat(all_groups, ignore_index=True)
    return result


def add_board_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add per-snapshot board-level features: num_positive_candidates, hold_duration, switch_count_today."""
    df = df.sort_values(["product_type", "date", "snap_idx"]).copy()

    hold_duration_col = []
    switch_count_col = []
    num_positive_col = []
    rank1_cum_col = []

    for (product_type, date), day_grp in df.groupby(["product_type", "date"], sort=False):
        snaps = sorted(day_grp["snap_idx"].unique())
        current_leader = None
        hold_dur = 0
        switch_count = 0

        snap_hold = {}
        snap_switch = {}
        snap_positive = {}

        rank1_cum = {}   # (product, strategy) -> cumulative rank1 count
        snap_rank1_cum = {}  # snap_idx -> {(product, strategy): count}

        for snap in snaps:
            snap_df = day_grp[day_grp["snap_idx"] == snap]
            # rank-1 candidate
            rank1 = snap_df[snap_df["rank"] == 1]
            if not rank1.empty:
                leader_key = (rank1.iloc[0]["product"], rank1.iloc[0]["strategy"])
                if leader_key != current_leader:
                    if current_leader is not None:
                        switch_count += 1
                    current_leader = leader_key
                    hold_dur = 1
                else:
                    hold_dur += 1
                rank1_cum[leader_key] = rank1_cum.get(leader_key, 0) + 1
            snap_hold[snap] = hold_dur
            snap_switch[snap] = switch_count
            snap_positive[snap] = int((snap_df["net"] > 0).sum())
            snap_rank1_cum[snap] = dict(rank1_cum)

        idx = day_grp.index
        hold_duration_col.extend(day_grp["snap_idx"].map(snap_hold).reindex(idx).tolist())
        switch_count_col.extend(day_grp["snap_idx"].map(snap_switch).reindex(idx).tolist())
        num_positive_col.extend(day_grp["snap_idx"].map(snap_positive).reindex(idx).tolist())
        rank1_cum_col.extend(
            day_grp.apply(
                lambda r: snap_rank1_cum.get(r["snap_idx"], {}).get((r["product"], r["strategy"]), 0),
                axis=1
            ).reindex(idx).tolist()
        )

    df["hold_duration"] = hold_duration_col
    df["switch_count_today"] = switch_count_col
    df["num_positive_candidates"] = num_positive_col
    df["rank1_count_cum"] = rank1_cum_col
    df["minute_of_day"] = df["timestamp"].apply(
        lambda t: t.hour * 60 + t.minute if pd.notnull(t) else 0
    )
    return df


# ---------------------------------------------------------------------------
# Step 6: Walk-forward splitter
# ---------------------------------------------------------------------------
def walk_forward_splits(dates: list, min_train: int = 5):
    """
    Yields (train_dates, test_date) pairs.
    No overlap: test_date is never in train_dates.
    """
    dates = sorted(dates)
    for i in range(min_train, len(dates)):
        train = dates[:i]
        test = dates[i]
        yield train, test


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("Phase 1: Data Engineering Pipeline")
    print("=" * 60)

    # Step 1: Discover files
    files = discover_files()
    print(f"\nStep 1: Discovered {len(files)} _frequency.json files")
    by_pt = defaultdict(int)
    for (pt, date), _ in files.items():
        by_pt[pt] += 1
    for pt, count in sorted(by_pt.items()):
        print(f"  {pt}: {count} dates")

    if not files:
        print("ERROR: No files found. Check DATA_ROOT path.")
        sys.exit(1)

    # Step 2 & 3: Parse all files into flat rows
    print("\nStep 2: Parsing snapshots...")
    all_rows = []
    for (pt, date), path in sorted(files.items()):
        rows = parse_frequency_file(path, pt, date)
        all_rows.extend(rows)
        print(f"  {pt}/{date}: {len(rows)} rows")

    df = pd.DataFrame(all_rows)
    print(f"\nTotal rows: {len(df)}")
    print(f"Null check - net nulls: {df['net'].isnull().sum()}")
    print(f"DataFrame shape: {df.shape}")

    # Step 4: Compute features
    print("\nStep 4: Computing live-safe features...")
    df = compute_features(df)
    df = add_board_features(df)

    # Step 5: Feature leakage audit
    print("\nStep 5: Feature leakage audit")
    forbidden = ["final_net", "final_rank", "end_of_day", "future"]
    all_cols = df.columns.tolist()
    leakage_found = [c for c in all_cols if any(f in c.lower() for f in forbidden)]
    print(f"  All features: {all_cols}")
    print(f"  Leakage risk columns: {leakage_found if leakage_found else 'NONE — clean'}")

    # Step 6: Walk-forward splits (per product type)
    print("\nStep 6: Walk-forward split validation")
    for pt in PRODUCT_TYPES:
        pt_dates = sorted(df[df["product_type"] == pt]["date"].unique().tolist())
        if not pt_dates:
            continue
        splits = list(walk_forward_splits(pt_dates, CFG["min_train_days"]))
        print(f"  {pt}: {len(pt_dates)} dates -> {len(splits)} folds")
        if splits:
            print(f"    First fold: train={splits[0][0]}, test={splits[0][1]}")
            print(f"    Last fold:  train={splits[-1][0][:3]}...({len(splits[-1][0])} days), test={splits[-1][1]}")

    # Step 7: Save processed parquet per (product_type, date)
    print("\nStep 7: Saving processed parquet files...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    saved = 0
    for (pt, date), grp in df.groupby(["product_type", "date"]):
        out_path = OUTPUT_DIR / f"{pt}_{date}.parquet"
        grp.to_parquet(out_path, index=False)
        saved += 1

    print(f"  Saved {saved} parquet files to {OUTPUT_DIR}")

    # Verify one file
    if saved > 0:
        sample = list(OUTPUT_DIR.glob("*.parquet"))[0]
        check = pd.read_parquet(sample)
        print(f"\nVerification — loaded {sample.name}: shape={check.shape}, cols={check.columns.tolist()}")

    print("\nPhase 1 COMPLETE")
    return df


if __name__ == "__main__":
    df = main()
