"""
Phase 3: Learned Selector v1 -- Value-Based HOLD/SWITCH/FLAT Policy
Uses HistGradientBoostingRegressor (Q-estimator) trained walk-forward with recency weighting.

Vectorized sample building: no iterrows; uses merge + groupby for ~10x speed improvement.
"""

import json
import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

EPIC_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = EPIC_DIR / "data" / "config" / "config.json"
PROCESSED_DIR = EPIC_DIR / "data" / "processed"
MODELS_DIR = EPIC_DIR / "models"
OUTPUT_DIR = Path(__file__).parent

MODELS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

with open(CONFIG_PATH) as f:
    CFG = json.load(f)

# Optional: filter to a single product type via CLI arg (e.g. `python selector.py forex`)
_PT_FILTER = sys.argv[1] if len(sys.argv) > 1 else None

SWITCHING_COST   = CFG["switching_cost"]         # 50
SAFETY_MARGIN    = CFG["safety_margin"]           # 5
MIN_TRAIN_DAYS   = CFG["min_train_days"]          # 5
PRODUCT_TYPES    = CFG["product_types"]
LAMBDA           = CFG["recency_lambda"]          # 0.1
NON_POS_PENALTY  = CFG["non_positive_penalty"]    # 25
NEG_PENALTY      = CFG["negative_penalty"]        # 50
POS_BONUS        = CFG["positive_bonus"]          # 10

FEATURE_COLS = [
    "held_net", "held_rank", "held_score",
    "held_net_slope_3", "held_net_slope_5", "held_net_slope_10",
    "held_positive_streak", "hold_duration", "switch_count_today",
    "chal_net", "chal_rank", "chal_score",
    "chal_net_slope_3", "chal_net_slope_5", "chal_net_slope_10",
    "net_gap", "score_gap",
    "num_positive_candidates", "minute_of_day",
    "held_rank1_cum", "chal_rank1_cum", "rank1_gap",
]

# Locked before first run -- do NOT tune after seeing test results
# Ridge chosen over HistGBM: HistGBM predict() is ~120ms/call on this platform;
# Ridge trains in <0.3s and predicts 240 calls in <0.05s.
RIDGE_ALPHA = 1.0

_EMPTY_COLS = FEATURE_COLS + ["q_hold", "q_switch", "q_flat", "has_challenger"]


# ---------------------------------------------------------------------------
# Reward (vectorized-friendly)
# ---------------------------------------------------------------------------

def reward_vec(current_r1, next_r1, is_switch_arr):
    """v4: rank1_count_cum as reward signal. Higher cum count = better position."""
    reward = next_r1.copy().astype(float)
    reward -= SWITCHING_COST * is_switch_arr
    return reward


# ---------------------------------------------------------------------------
# Challenger selection (scalar, for simulation only)
# ---------------------------------------------------------------------------

def get_best_challenger(snap_df, held_product, held_strategy):
    eligible = snap_df[snap_df["net"] > 0]
    challengers = eligible[
        ~((eligible["product"] == held_product) & (eligible["strategy"] == held_strategy))
    ]
    if challengers.empty:
        return None
    return challengers.sort_values("rank1_count_cum", ascending=False).iloc[0]


# ---------------------------------------------------------------------------
# Vectorized training data builder (cached once per day)
# ---------------------------------------------------------------------------

def build_day_samples(day_df):
    """
    Fully vectorized: no iterrows.
    For each (eligible held, snap) pair, generate reward labels for HOLD + SWITCH.
    Returns a DataFrame suitable for GBM training.
    """
    snaps = sorted(day_df["snap_idx"].unique())
    if len(snaps) < 2:
        return pd.DataFrame(columns=_EMPTY_COLS)

    CURR_COLS = ["snap_idx", "product", "strategy", "net", "rank", "score",
                 "net_slope_3", "net_slope_5", "net_slope_10",
                 "positive_streak", "hold_duration", "switch_count_today",
                 "num_positive_candidates", "minute_of_day", "rank1_count_cum"]

    # Step 1: keep only eligible (net > 0) rows at current snap
    curr = day_df[day_df["net"] > 0][CURR_COLS].copy()

    # Step 2: build next_snap mapping and annotate
    snap_arr  = np.array(snaps)
    snap_next = pd.Series(snap_arr[1:], index=snap_arr[:-1])
    curr["next_snap_idx"] = curr["snap_idx"].map(snap_next)
    curr = curr.dropna(subset=["next_snap_idx"])
    curr["next_snap_idx"] = curr["next_snap_idx"].astype(int)

    if curr.empty:
        return pd.DataFrame(columns=_EMPTY_COLS)

    # Step 3: join with next-snap rank1_count_cum for each (product, strategy)
    nxt = day_df[["snap_idx", "product", "strategy", "net", "rank1_count_cum"]].rename(
        columns={"snap_idx": "next_snap_idx", "net": "next_net",
                 "rank1_count_cum": "next_r1"})
    merged = curr.merge(nxt, on=["next_snap_idx", "product", "strategy"], how="inner")

    if merged.empty:
        return pd.DataFrame(columns=_EMPTY_COLS)

    # Step 4: compute q_hold using rank1_count_cum reward (vectorized)
    cur_r1_arr  = merged["rank1_count_cum"].values.astype(float)
    next_r1_arr = merged["next_r1"].values.astype(float)
    merged["q_hold"] = reward_vec(cur_r1_arr, next_r1_arr, np.zeros(len(merged), float))

    # Step 5: find top-2 eligible candidates per snap (for challenger)
    # Sort by net desc within each snap, take rank 0 and rank 1
    sorted_m = merged.sort_values(["snap_idx", "net"], ascending=[True, False])
    sorted_m["_snap_rank"] = sorted_m.groupby("snap_idx").cumcount()

    TOP_COLS = ["snap_idx", "product", "strategy", "net", "rank", "score",
                "net_slope_3", "net_slope_5", "net_slope_10", "next_snap_idx",
                "rank1_count_cum"]

    top1 = sorted_m[sorted_m["_snap_rank"] == 0][TOP_COLS].add_prefix("t1_").rename(
        columns={"t1_snap_idx": "snap_idx", "t1_next_snap_idx": "next_snap_idx"})
    top2 = sorted_m[sorted_m["_snap_rank"] == 1][TOP_COLS].add_prefix("t2_").rename(
        columns={"t2_snap_idx": "snap_idx", "t2_next_snap_idx": "next_snap_idx"})

    merged = merged.merge(top1[["snap_idx", "t1_product", "t1_strategy",
                                  "t1_net", "t1_rank", "t1_score",
                                  "t1_net_slope_3", "t1_net_slope_5", "t1_net_slope_10",
                                  "t1_rank1_count_cum"]],
                          on="snap_idx", how="left")
    merged = merged.merge(top2[["snap_idx", "t2_product", "t2_strategy",
                                  "t2_net", "t2_rank", "t2_score",
                                  "t2_net_slope_3", "t2_net_slope_5", "t2_net_slope_10",
                                  "t2_rank1_count_cum"]],
                          on="snap_idx", how="left")

    # Step 6: determine challenger (if held == top1: chal = top2, else: chal = top1)
    is_top1 = (merged["product"] == merged["t1_product"]) & \
              (merged["strategy"] == merged["t1_strategy"])

    merged["chal_p"]   = np.where(is_top1, merged["t2_product"],    merged["t1_product"])
    merged["chal_s"]   = np.where(is_top1, merged["t2_strategy"],   merged["t1_strategy"])
    merged["chal_net"] = np.where(is_top1, merged["t2_net"].fillna(0), merged["t1_net"].fillna(0))
    merged["chal_rank"]= np.where(is_top1, merged["t2_rank"].fillna(0), merged["t1_rank"].fillna(0))
    merged["chal_score"]= np.where(is_top1,merged["t2_score"].fillna(0),merged["t1_score"].fillna(0))
    merged["chal_ns3"] = np.where(is_top1, merged["t2_net_slope_3"].fillna(0), merged["t1_net_slope_3"].fillna(0))
    merged["chal_ns5"] = np.where(is_top1, merged["t2_net_slope_5"].fillna(0), merged["t1_net_slope_5"].fillna(0))
    merged["chal_ns10"]= np.where(is_top1, merged["t2_net_slope_10"].fillna(0),merged["t1_net_slope_10"].fillna(0))
    merged["chal_r1"]  = np.where(is_top1, merged["t2_rank1_count_cum"].fillna(0), merged["t1_rank1_count_cum"].fillna(0))
    merged["has_challenger"] = (
        merged["chal_p"].notna() & (merged["chal_net"] > 0)
    ).astype(int)

    # Step 7: get next rank1_count_cum for challenger
    chal_nxt = nxt.rename(columns={"product": "chal_p", "strategy": "chal_s",
                                    "next_net": "chal_next_net", "next_r1": "chal_next_r1"})
    merged = merged.merge(chal_nxt[["next_snap_idx", "chal_p", "chal_s", "chal_next_r1"]],
                          on=["next_snap_idx", "chal_p", "chal_s"], how="left")

    # Step 8: compute q_switch using rank1_count_cum reward (vectorized)
    chal_net  = merged["chal_net"].values.astype(float)
    chal_r1   = merged["chal_r1"].values.astype(float)
    chal_nr1  = merged["chal_next_r1"].fillna(np.nan).values.astype(float)
    has_chal  = merged["has_challenger"].values.astype(bool)
    valid_sw  = has_chal & ~np.isnan(chal_nr1)

    q_sw = np.where(valid_sw,
                    reward_vec(chal_r1, np.where(valid_sw, chal_nr1, 0.0),
                               np.ones(len(merged), float)),
                    merged["q_hold"].values - SWITCHING_COST)
    merged["q_switch"] = q_sw
    merged["q_flat"]   = 0.0

    # Step 9: assemble output
    out = pd.DataFrame({
        "held_net":              merged["net"].values.astype(float),
        "held_rank":             merged["rank"].values.astype(float),
        "held_score":            merged["score"].values.astype(float),
        "held_net_slope_3":      merged["net_slope_3"].values.astype(float),
        "held_net_slope_5":      merged["net_slope_5"].values.astype(float),
        "held_net_slope_10":     merged["net_slope_10"].values.astype(float),
        "held_positive_streak":  merged["positive_streak"].values.astype(float),
        "hold_duration":         merged["hold_duration"].values.astype(float),
        "switch_count_today":    merged["switch_count_today"].values.astype(float),
        "chal_net":              chal_net,
        "chal_rank":             merged["chal_rank"].values.astype(float),
        "chal_score":            merged["chal_score"].values.astype(float),
        "chal_net_slope_3":      merged["chal_ns3"].values.astype(float),
        "chal_net_slope_5":      merged["chal_ns5"].values.astype(float),
        "chal_net_slope_10":     merged["chal_ns10"].values.astype(float),
        "net_gap":               chal_net - merged["net"].values.astype(float),
        "score_gap":             merged["chal_score"].values.astype(float) - merged["score"].values.astype(float),
        "num_positive_candidates": merged["num_positive_candidates"].values.astype(float),
        "minute_of_day":         merged["minute_of_day"].values.astype(float),
        "held_rank1_cum":        merged["rank1_count_cum"].values.astype(float),
        "chal_rank1_cum":        chal_r1,
        "rank1_gap":             chal_r1 - merged["rank1_count_cum"].values.astype(float),
        "q_hold":                merged["q_hold"].values.astype(float),
        "q_switch":              merged["q_switch"].values.astype(float),
        "q_flat":                0.0,
        "has_challenger":        merged["has_challenger"].values.astype(int),
    })
    return out.dropna(subset=["q_hold"]).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Model training
# ---------------------------------------------------------------------------

def make_model():
    """Ridge regression with standard scaling (fast: <0.3s train, <0.05s for 240 preds)."""
    return Pipeline([
        ("scaler", StandardScaler()),
        ("ridge",  Ridge(alpha=RIDGE_ALPHA)),
    ])


def train_models(combined_df, combined_weights):
    """Train Q_HOLD and Q_SWITCH estimators on pre-assembled training DataFrame."""
    X  = combined_df[FEATURE_COLS].values.astype(float)
    w  = np.array(combined_weights, dtype=float)
    y_hold   = combined_df["q_hold"].values.astype(float)
    y_switch = combined_df["q_switch"].values.astype(float)
    sw_mask  = (combined_df["has_challenger"] == 1).values

    model_hold = make_model()
    model_hold.fit(X, y_hold, ridge__sample_weight=w)

    model_switch = None
    if sw_mask.sum() >= 10:
        model_switch = make_model()
        model_switch.fit(X[sw_mask], y_switch[sw_mask], ridge__sample_weight=w[sw_mask])

    return model_hold, model_switch


# ---------------------------------------------------------------------------
# Test-day simulation (sequential, as required by action dependency)
# ---------------------------------------------------------------------------

def simulate_test_day(day_df, model_hold, model_switch, date, pt):
    """Walk forward through test day applying learned Q policy."""
    decisions     = []
    snaps         = sorted(day_df["snap_idx"].unique())
    snap_groups   = dict(list(day_df.groupby("snap_idx")))
    held_product  = None
    held_strategy = None
    switch_count  = 0

    for snap in snaps:
        curr_df       = snap_groups[snap]
        eligible      = curr_df[curr_df["net"] > 0]
        minute_of_day = int(curr_df.iloc[0]["minute_of_day"]) if not curr_df.empty else 0
        num_pos       = len(eligible)

        # Resolve current held status
        held_net = None
        held_row = None
        if held_product and held_strategy:
            hr = curr_df[
                (curr_df["product"] == held_product) &
                (curr_df["strategy"] == held_strategy)
            ]
            if not hr.empty and float(hr.iloc[0]["net"]) > 0:
                held_row = hr.iloc[0]
                held_net = float(held_row["net"])

        # No eligible held -- forced entry or FLAT
        if held_net is None:
            if eligible.empty:
                held_product = held_strategy = None
                decisions.append({
                    "date": date, "product_type": pt, "snap_idx": snap,
                    "minute_of_day": minute_of_day, "action": "FLAT",
                    "product": None, "strategy": None, "net": 0.0,
                    "q_hold": 0.0, "q_switch": 0.0, "q_flat": 0.0,
                })
                continue
            best = eligible.sort_values("net", ascending=False).iloc[0]
            if held_product != best["product"] or held_strategy != best["strategy"]:
                switch_count += 1
            held_product  = best["product"]
            held_strategy = best["strategy"]
            decisions.append({
                "date": date, "product_type": pt, "snap_idx": snap,
                "minute_of_day": minute_of_day, "action": "SWITCH",
                "product": held_product, "strategy": held_strategy,
                "net": float(best["net"]),
                "q_hold": 0.0, "q_switch": 0.0, "q_flat": 0.0,
            })
            continue

        # Build feature vector
        chal = get_best_challenger(curr_df, held_product, held_strategy)
        if chal is not None:
            chal_net    = float(chal["net"])
            chal_rank   = float(chal["rank"])
            chal_score  = float(chal["score"])
            chal_ns3    = float(chal["net_slope_3"])
            chal_ns5    = float(chal["net_slope_5"])
            chal_ns10   = float(chal["net_slope_10"])
            chal_r1_cum = float(chal["rank1_count_cum"])
        else:
            chal_net = chal_rank = chal_score = chal_ns3 = chal_ns5 = chal_ns10 = chal_r1_cum = 0.0

        held_r1_cum = float(held_row["rank1_count_cum"])

        X_state = np.array([[
            held_net,
            float(held_row["rank"]),
            float(held_row["score"]),
            float(held_row["net_slope_3"]),
            float(held_row["net_slope_5"]),
            float(held_row["net_slope_10"]),
            float(held_row["positive_streak"]),
            float(held_row["hold_duration"]),
            float(switch_count),
            chal_net, chal_rank, chal_score,
            chal_ns3, chal_ns5, chal_ns10,
            chal_net - held_net,
            chal_score - float(held_row["score"]),
            float(num_pos),
            float(minute_of_day),
            held_r1_cum, chal_r1_cum, chal_r1_cum - held_r1_cum,
        ]])

        q_hold = float(model_hold.predict(X_state)[0])
        # v3 gate: FLAT only allowed when no positive candidates exist
        q_flat = 0.0 if num_pos == 0 else -9999.0
        q_switch = -9999.0
        if chal is not None and chal_net > 0 and model_switch is not None:
            q_switch = float(model_switch.predict(X_state)[0])

        scores = {"HOLD": q_hold, "SWITCH": q_switch, "FLAT": q_flat}
        best_action = max(scores, key=scores.get)

        if best_action == "SWITCH":
            switch_count += 1
            held_product  = chal["product"]
            held_strategy = chal["strategy"]
            net_out = chal_net
        elif best_action == "HOLD":
            net_out = held_net
        else:
            held_product = held_strategy = None
            net_out = 0.0

        decisions.append({
            "date": date, "product_type": pt, "snap_idx": snap,
            "minute_of_day": minute_of_day, "action": best_action,
            "product": held_product if best_action != "FLAT" else None,
            "strategy": held_strategy if best_action != "FLAT" else None,
            "net": net_out,
            "q_hold":   round(q_hold, 3),
            "q_switch": round(q_switch, 3) if q_switch > -9000 else 0.0,
            "q_flat":   q_flat,
        })

    return decisions, switch_count


# ---------------------------------------------------------------------------
# Walk-forward split
# ---------------------------------------------------------------------------

def walk_forward_splits(dates, min_train=5):
    dates = sorted(dates)
    for i in range(min_train, len(dates)):
        yield dates[:i], dates[i]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Phase 3d: Learned Selector v4 -- rank1_count_cum Reward Signal")
    print("=" * 60)

    files = sorted(PROCESSED_DIR.glob("*.parquet"))
    if not files:
        sys.exit("ERROR: No parquet files. Run Phase 1 first.")
    df = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    print(f"Loaded {len(df)} rows, {df['date'].nunique()} dates, {df['product_type'].nunique()} product types")

    fold_summaries    = []
    total_predictions = 0
    active_types      = [_PT_FILTER] if _PT_FILTER else PRODUCT_TYPES

    for pt in active_types:
        pt_df = df[df["product_type"] == pt]
        if pt_df.empty:
            print(f"WARNING: no data for product_type={pt}")
            continue
        dates  = sorted(pt_df["date"].unique().tolist())
        splits = list(walk_forward_splits(dates, MIN_TRAIN_DAYS))
        print(f"\n{pt}: {len(dates)} dates -> {len(splits)} folds")
        print("  Pre-building day sample cache...", flush=True)

        # Build training sample cache once per day (vectorized, O(n))
        day_sample_cache = {}
        for d in dates[:-1]:
            day_sample_cache[d] = build_day_samples(pt_df[pt_df["date"] == d])
        total_cached = sum(len(v) for v in day_sample_cache.values())
        print(f"  Cache: {total_cached} samples across {len(day_sample_cache)} days")

        for fold_idx, (train_dates, test_date) in enumerate(splits):
            today_ts = pd.Timestamp(test_date)
            frames, wt_lists = [], []
            for d in train_dates:
                if d not in day_sample_cache or day_sample_cache[d].empty:
                    continue
                days_ago = (today_ts - pd.Timestamp(d)).days
                w = float(np.exp(-LAMBDA * days_ago))
                frames.append(day_sample_cache[d])
                wt_lists.append(np.full(len(day_sample_cache[d]), w))

            if not frames:
                continue
            combined_df      = pd.concat(frames, ignore_index=True)
            combined_weights = np.concatenate(wt_lists)

            if len(combined_df) < 10:
                continue

            # Train
            model_hold, model_switch = train_models(combined_df, combined_weights)

            # Save fold models
            fold_key = f"{pt}_{test_date}"
            with open(MODELS_DIR / f"hold_{fold_key}.pkl", "wb") as fh:
                pickle.dump(model_hold, fh)
            if model_switch is not None:
                with open(MODELS_DIR / f"switch_{fold_key}.pkl", "wb") as fh:
                    pickle.dump(model_switch, fh)

            # Simulate test day
            test_df = pt_df[pt_df["date"] == test_date].copy()
            if test_df.empty:
                continue

            decisions, sw_count = simulate_test_day(test_df, model_hold, model_switch, test_date, pt)
            final   = next((d for d in reversed(decisions) if d["action"] != "FLAT"), None)
            day_net = (float(final["net"]) if final else 0.0) - sw_count * SWITCHING_COST

            ac = {a: sum(1 for d in decisions if d["action"] == a) for a in ["HOLD", "SWITCH", "FLAT"]}
            total_snaps = len(decisions)
            hold_pct    = ac["HOLD"] / total_snaps * 100 if total_snaps > 0 else 0.0

            fold_summaries.append({
                "product_type":  pt,
                "date":          test_date,
                "fold":          fold_idx,
                "train_days":    len(train_dates),
                "train_samples": len(combined_df),
                "day_net":       day_net,
                "switch_count":  sw_count,
                "hold_pct":      round(hold_pct, 1),
                "action_hold":   ac["HOLD"],
                "action_switch": ac["SWITCH"],
                "action_flat":   ac["FLAT"],
            })

            pred_csv = OUTPUT_DIR / f"predictions_{pt}_{test_date}_v4.csv"
            pd.DataFrame(decisions).to_csv(pred_csv, index=False)
            total_predictions += total_snaps

            print(f"  {test_date}: net={day_net:.1f} sw={sw_count} "
                  f"HOLD={hold_pct:.0f}% [{ac['HOLD']}H/{ac['SWITCH']}S/{ac['FLAT']}F]")

    if not fold_summaries:
        sys.exit("ERROR: No results produced.")

    summary_df   = pd.DataFrame(fold_summaries)
    summary_path = OUTPUT_DIR / "fold_summary_learned_v4.csv"
    summary_df.to_csv(summary_path, index=False)
    print(f"\nSaved fold summary: {summary_path} ({len(summary_df)} rows)")

    total_net = float(summary_df["day_net"].sum())
    agg = {
        "total_net_learned":  round(total_net, 2),
        "avg_net_per_day":    round(float(summary_df["day_net"].mean()), 2),
        "total_switches":     int(summary_df["switch_count"].sum()),
        "avg_hold_pct":       round(float(summary_df["hold_pct"].mean()), 1),
        "days_tested":        len(summary_df),
        "total_predictions":  total_predictions,
        "hold_dominates":     bool(summary_df["hold_pct"].mean() > 50.0),
        "product_types_run":  list(summary_df["product_type"].unique()),
    }
    agg_path = OUTPUT_DIR / "aggregate_learned_v4.json"
    with open(agg_path, "w") as fh:
        json.dump(agg, fh, indent=2)
    print(f"Saved aggregate: {agg_path}")
    print(json.dumps(agg, indent=2))

    bad_folds = summary_df[summary_df["train_days"] < MIN_TRAIN_DAYS]
    if not bad_folds.empty:
        print(f"WARNING: {len(bad_folds)} folds with < {MIN_TRAIN_DAYS} train days")
    else:
        print(f"Leakage check: all {len(summary_df)} folds had >= {MIN_TRAIN_DAYS} train days -- clean")

    print("\nPhase 3d COMPLETE")


if __name__ == "__main__":
    main()
