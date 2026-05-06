"""
Phase 5: Finalization -- freeze config, build final proof report,
retrain on full dataset, run git diff check on production files.

Usage:
    python finalize.py [--force]

--force bypasses the accepted=true gate (user-directed override).
"""
import json
import pickle
import subprocess
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

EPIC_DIR   = Path(__file__).resolve().parents[1]
DEPLOY_DIR = Path(__file__).parent
CONFIG_PATH    = EPIC_DIR / "data" / "config" / "config.json"
PROCESSED_DIR  = EPIC_DIR / "data" / "processed"
LEARNED_DIR    = EPIC_DIR / "results" / "learned"
EVAL_DIR       = EPIC_DIR / "results" / "evaluation"
REPO_ROOT      = EPIC_DIR.parents[1]

FORCE = "--force" in sys.argv

RIDGE_ALPHA = 1.0
FEATURE_COLS = [
    "held_net", "held_rank", "held_score",
    "held_net_slope_3", "held_net_slope_5", "held_net_slope_10",
    "held_positive_streak", "hold_duration", "switch_count_today",
    "chal_net", "chal_rank", "chal_score",
    "chal_net_slope_3", "chal_net_slope_5", "chal_net_slope_10",
    "net_gap", "score_gap",
    "num_positive_candidates", "minute_of_day",
]


# ---------------------------------------------------------------------------
# Step 1: Gate check
# ---------------------------------------------------------------------------

def step1_gate_check(cfg):
    print("\n[Step 1] Gate check")
    eval_agg = EVAL_DIR / "aggregate_results.json"
    if not eval_agg.exists():
        sys.exit("ERROR: Phase 4 aggregate_results.json not found.")
    with open(eval_agg) as f:
        result = json.load(f)
    accepted = result.get("accepted", False)
    v3_improvement = -4.67  # v3 result from Phase 3c
    print(f"  Phase 4 verdict: {result.get('verdict')} (accepted={accepted})")
    print(f"  Best learned (v3) vs Baseline B: {v3_improvement}%")
    if not accepted:
        if FORCE:
            print("  WARNING: --force flag set; bypassing gate on user instruction.")
            print(f"  v3 is within 5% of Baseline B ({v3_improvement}%); shadow mode only.")
        else:
            sys.exit(
                "ERROR: Phase 4 verdict is REJECTED. "
                "v3 improvement (-4.67%) is below +25% threshold.\n"
                "Run with --force to proceed in shadow/read-only mode."
            )
    print("  Gate check PASSED" if accepted else "  Gate BYPASSED (--force)")


# ---------------------------------------------------------------------------
# Step 2: Freeze config
# ---------------------------------------------------------------------------

def step2_freeze_config(cfg):
    print("\n[Step 2] Freezing config")
    if cfg.get("frozen"):
        print("  Already frozen -- no change.")
        return cfg
    cfg["frozen"] = True
    cfg["frozen_date"] = str(date.today())
    cfg["frozen_model_version"] = "v3"
    cfg["v3_changes"] = [
        "absolute_reward: reward=next_net (not delta_net)",
        "flat_gate: q_flat=-9999 when num_positive_candidates>0",
    ]
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"  Wrote frozen config to {CONFIG_PATH}")
    print(f"  switching_cost={cfg['switching_cost']}, "
          f"recency_lambda={cfg['recency_lambda']}, "
          f"min_train_days={cfg['min_train_days']}")
    return cfg


# ---------------------------------------------------------------------------
# Step 3: Final proof report (from v3 results)
# ---------------------------------------------------------------------------

def step3_proof_report(cfg):
    print("\n[Step 3] Writing final proof report")
    v3_agg = LEARNED_DIR / "aggregate_learned_v3.json"
    if not v3_agg.exists():
        sys.exit("ERROR: aggregate_learned_v3.json not found. Run selector_v3.py first.")
    with open(v3_agg) as f:
        v3 = json.load(f)

    eval_agg = EVAL_DIR / "aggregate_results.json"
    with open(eval_agg) as f:
        phase4 = json.load(f)

    baseline_b = phase4["best_baseline_net"]
    total_v3   = v3["total_net_learned"]
    improvement = round((total_v3 - baseline_b) / abs(baseline_b) * 100, 2)

    report = {
        "model_version":             "v3",
        "finalized_date":            str(date.today()),
        "protocol":                  "walk_forward_forex_26_folds",
        "total_net_v3":              total_v3,
        "total_net_baseline_b":      baseline_b,
        "improvement_vs_baseline_b": improvement,
        "acceptance_threshold_pct":  cfg["improvement_threshold_pct"] * 100,
        "accepted":                  improvement >= cfg["improvement_threshold_pct"] * 100,
        "force_deployed":            FORCE,
        "avg_net_per_day":           v3["avg_net_per_day"],
        "total_switches":            v3["total_switches"],
        "avg_hold_pct":              v3["avg_hold_pct"],
        "days_tested":               v3["days_tested"],
        "v3_changes": [
            "reward=next_net (absolute, not delta)",
            "q_flat=-9999 when positive candidates exist",
        ],
        "note": (
            "v3 within 5% of Baseline B (-4.67%); "
            "residual gap from genuine zero-candidate FLAT days. "
            "Deployed shadow-only per user direction."
        ),
    }
    out = DEPLOY_DIR / "final_proof_report.json"
    with open(out, "w") as f:
        json.dump(report, f, indent=2)
    print(f"  Saved: {out}")
    print(f"  total_net_v3={total_v3}, baseline_b={baseline_b}, improvement={improvement}%")


# ---------------------------------------------------------------------------
# Helpers for full retrain (shared with selector_v3 logic)
# ---------------------------------------------------------------------------

def make_model():
    return Pipeline([("scaler", StandardScaler()), ("ridge", Ridge(alpha=RIDGE_ALPHA))])


def reward_vec(current_net, next_net, is_switch_arr, cfg):
    """v3: absolute next_net reward."""
    sc  = cfg["switching_cost"]
    npp = cfg["non_positive_penalty"]
    np_ = cfg["negative_penalty"]
    pb  = cfg["positive_bonus"]
    reward  = next_net.copy()
    reward -= sc  * is_switch_arr
    reward -= npp * (next_net <= 0).astype(float)
    reward -= np_ * (next_net <  0).astype(float)
    reward += pb  * ((next_net > current_net) & (next_net > 0)).astype(float)
    return reward


def build_day_samples(day_df, cfg):
    """Vectorized sample builder (same logic as selector_v3)."""
    snaps = sorted(day_df["snap_idx"].unique())
    if len(snaps) < 2:
        return pd.DataFrame()

    rows = []
    for i, snap in enumerate(snaps[:-1]):
        curr = day_df[day_df["snap_idx"] == snap]
        nxt  = day_df[day_df["snap_idx"] == snaps[i + 1]]
        if curr.empty or nxt.empty:
            continue
        eligible = curr[curr["net"] > 0].copy()
        if eligible.empty:
            continue
        eligible = eligible.sort_values("net", ascending=False).reset_index(drop=True)
        top1 = eligible.iloc[0]
        top2 = eligible.iloc[1] if len(eligible) > 1 else None

        # Next-snap net for top1 (held) and top2 (challenger)
        nxt1 = nxt[(nxt["product"] == top1["product"]) & (nxt["strategy"] == top1["strategy"])]
        held_next_net = float(nxt1.iloc[0]["net"]) if not nxt1.empty else 0.0
        chal_net  = float(top2["net"])   if top2 is not None else 0.0
        chal_next = 0.0
        if top2 is not None:
            nr = nxt[(nxt["product"] == top2["product"]) & (nxt["strategy"] == top2["strategy"])]
            chal_next = float(nr.iloc[0]["net"]) if not nr.empty else 0.0

        held_cur  = float(top1["net"])
        is_sw     = np.array([0.0, 1.0])
        cur_nets  = np.array([held_cur, chal_net])
        nxt_nets  = np.array([held_next_net, chal_next])
        rewards   = reward_vec(cur_nets, nxt_nets, is_sw, cfg)

        num_pos = len(eligible)
        feat = {
            "held_net":             held_cur,
            "held_rank":            float(top1["rank"]),
            "held_score":           float(top1["score"]),
            "held_net_slope_3":     float(top1.get("net_slope_3", 0)),
            "held_net_slope_5":     float(top1.get("net_slope_5", 0)),
            "held_net_slope_10":    float(top1.get("net_slope_10", 0)),
            "held_positive_streak": float(top1.get("positive_streak", 0)),
            "hold_duration":        float(top1.get("hold_duration", 0)),
            "switch_count_today":   0.0,
            "chal_net":             chal_net,
            "chal_rank":            float(top2["rank"])    if top2 is not None else 0.0,
            "chal_score":           float(top2["score"])   if top2 is not None else 0.0,
            "chal_net_slope_3":     float(top2.get("net_slope_3", 0)) if top2 is not None else 0.0,
            "chal_net_slope_5":     float(top2.get("net_slope_5", 0)) if top2 is not None else 0.0,
            "chal_net_slope_10":    float(top2.get("net_slope_10", 0)) if top2 is not None else 0.0,
            "net_gap":              chal_net - held_cur,
            "score_gap":            (float(top2["score"]) - float(top1["score"])) if top2 is not None else 0.0,
            "num_positive_candidates": float(num_pos),
            "minute_of_day":        float(top1.get("minute_of_day", 0)),
            "q_hold":               rewards[0],
            "q_switch":             rewards[1],
            "has_challenger":       1 if top2 is not None and chal_net > 0 else 0,
        }
        rows.append(feat)

    return pd.DataFrame(rows) if rows else pd.DataFrame()


# ---------------------------------------------------------------------------
# Step 4: Full retrain on all data -> final_production.pkl
# ---------------------------------------------------------------------------

def step4_full_retrain(cfg):
    print("\n[Step 4] Full retrain on all forex data")
    files = sorted(PROCESSED_DIR.glob("*.parquet"))
    if not files:
        sys.exit("ERROR: No parquet files in processed/")
    df = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
    pt_df = df[df["product_type"] == "forex"]
    dates = sorted(pt_df["date"].unique().tolist())
    print(f"  Loaded {len(pt_df)} forex rows, {len(dates)} dates")

    today_ts = pd.Timestamp(str(date.today()))
    frames, weights = [], []
    for d in dates:
        samples = build_day_samples(pt_df[pt_df["date"] == d], cfg)
        if samples.empty:
            continue
        days_ago = max((today_ts - pd.Timestamp(d)).days, 0)
        w = float(np.exp(-cfg["recency_lambda"] * days_ago))
        frames.append(samples)
        weights.append(np.full(len(samples), w))

    if not frames:
        sys.exit("ERROR: No samples built.")

    combined  = pd.concat(frames, ignore_index=True)
    combined_w = np.concatenate(weights)
    print(f"  Training on {len(combined)} samples from {len(frames)} days")

    X        = combined[FEATURE_COLS].values.astype(float)
    y_hold   = combined["q_hold"].values.astype(float)
    y_switch = combined["q_switch"].values.astype(float)
    sw_mask  = (combined["has_challenger"] == 1).values

    model_hold = make_model()
    model_hold.fit(X, y_hold, ridge__sample_weight=combined_w)

    model_switch = None
    if sw_mask.sum() >= 10:
        model_switch = make_model()
        model_switch.fit(X[sw_mask], y_switch[sw_mask], ridge__sample_weight=combined_w[sw_mask])

    payload = {
        "model_hold":    model_hold,
        "model_switch":  model_switch,
        "feature_cols":  FEATURE_COLS,
        "model_version": "v3",
        "trained_on":    str(date.today()),
        "n_samples":     len(combined),
        "n_days":        len(frames),
        "product_type":  "forex",
        "config": {
            "switching_cost":       cfg["switching_cost"],
            "flat_gate":            "q_flat=-9999 when num_pos>0",
            "reward":               "absolute next_net",
            "ridge_alpha":          RIDGE_ALPHA,
            "recency_lambda":       cfg["recency_lambda"],
        },
    }
    out = DEPLOY_DIR / "final_production.pkl"
    with open(out, "wb") as f:
        pickle.dump(payload, f)
    print(f"  Saved: {out}")

    # Verify load
    with open(out, "rb") as f:
        check = pickle.load(f)
    assert check["model_hold"] is not None, "model_hold missing"
    print(f"  Load check PASSED (n_samples={check['n_samples']}, n_days={check['n_days']})")


# ---------------------------------------------------------------------------
# Step 6: Diff check on production files
# ---------------------------------------------------------------------------

def step6_diff_check():
    print("\n[Step 6] Git diff check on production files")
    targets = [
        "TradeApps/breakout/fs/common.py",
        "TradeApps/breakout/fs/breakout.py",
        "TradeApps/breakout/fs/breakout_R.py",
    ]
    clean = True
    for t in targets:
        result = subprocess.run(
            ["git", "diff", "HEAD", "--", t],
            cwd=str(REPO_ROOT),
            capture_output=True, text=True
        )
        if result.stdout.strip():
            print(f"  WARN: {t} has uncommitted changes:")
            print(result.stdout[:500])
            clean = False
        else:
            print(f"  CLEAN: {t}")
    if clean:
        print("  All production files unmodified -- PASS")
    else:
        print("  WARNING: production file changes detected (see above)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Phase 5: Finalization")
    print("=" * 60)

    with open(CONFIG_PATH) as f:
        cfg = json.load(f)

    step1_gate_check(cfg)
    cfg = step2_freeze_config(cfg)
    step3_proof_report(cfg)
    step4_full_retrain(cfg)
    step6_diff_check()

    print("\n" + "=" * 60)
    print("Phase 5 Steps 1-4, 6 COMPLETE")
    print("Run shadow_writer.py for Step 5 (shadow output)")
    print("=" * 60)


if __name__ == "__main__":
    main()
