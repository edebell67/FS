"""
Phase 5 Step 5: Shadow Selector Writer

Reads live _top20.json for a product type, loads the final production model,
computes Q-values, and writes a recommendation to _selector_shadow.json.

This is READ-ONLY. No trade execution paths are touched.

Usage:
    python shadow_writer.py [product_type]   (default: forex)

Output:
    TradeApps/breakout/fs/json/live/{product_type}/{date}/_selector_shadow.json
    TradeApps/breakout/fs/json/live/{product_type}/{date}/_selector_state.json  (internal state)
"""
import json
import pickle
import sys
from datetime import datetime, date
from pathlib import Path

import numpy as np

DEPLOY_DIR = Path(__file__).parent
EPIC_DIR   = DEPLOY_DIR.parent
REPO_ROOT  = EPIC_DIR.parents[1]

MODEL_PATH = DEPLOY_DIR / "final_production.pkl"

PRODUCT_TYPE = sys.argv[1] if len(sys.argv) > 1 else "forex"
TODAY        = str(date.today())

LIVE_DIR  = REPO_ROOT / "TradeApps" / "breakout" / "fs" / "json" / "live"
PT_DIR    = LIVE_DIR / PRODUCT_TYPE / TODAY
STATE_PATH  = PT_DIR / "_selector_state.json"
OUTPUT_PATH = PT_DIR / "_selector_shadow.json"


# ---------------------------------------------------------------------------
# Load model
# ---------------------------------------------------------------------------

def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}. Run finalize.py first.")
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


# ---------------------------------------------------------------------------
# Load live top20 data
# ---------------------------------------------------------------------------

def load_top20():
    top20_path = PT_DIR / "_top20.json"
    if not top20_path.exists():
        raise FileNotFoundError(f"No _top20.json at {top20_path}")
    with open(top20_path) as f:
        data = json.load(f)
    entries = data.get("top20", [])
    last_update = data.get("last_update", "")
    return entries, last_update


# ---------------------------------------------------------------------------
# State: track held position and rolling snapshot history for slope estimates
# ---------------------------------------------------------------------------

def load_state():
    if STATE_PATH.exists():
        with open(STATE_PATH) as f:
            return json.load(f)
    return {
        "held_product":    None,
        "held_strategy":   None,
        "hold_start_snap": 0,
        "switch_count":    0,
        "snap_count":      0,
        "history":         [],   # last 10 snapshots: [{product, strategy, net, snap}]
    }


def save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


# ---------------------------------------------------------------------------
# Feature builder from live top20
# ---------------------------------------------------------------------------

def build_features(entries, state, payload):
    """
    Build the 19-feature vector from live top20 data and saved state.
    Slope features default to 0.0 (no rolling history in live mode;
    state.history used for a best-effort estimate if available).
    """
    feature_cols = payload["feature_cols"]

    # Sort entries by total_net descending, assign rank
    positive = [e for e in entries if e.get("total_net", 0) > 0]
    positive.sort(key=lambda x: x.get("total_net", 0), reverse=True)
    num_pos = len(positive)

    if not positive:
        return None, None, None, num_pos

    # Held position
    held_product  = state["held_product"]
    held_strategy = state["held_strategy"]

    held_entry = None
    if held_product and held_strategy:
        for e in positive:
            if e["product"] == held_product and e["strategy"] == held_strategy:
                held_entry = e
                break

    # If held dropped out of positive, force to best
    if held_entry is None:
        held_entry = positive[0]

    held_net   = float(held_entry.get("total_net", 0))
    held_rank  = 1.0 + next((i for i, e in enumerate(positive)
                              if e["product"] == held_entry["product"]
                              and e["strategy"] == held_entry["strategy"]), 0)
    max_net    = float(positive[0].get("total_net", 1)) or 1.0
    held_score = held_net / max_net

    # Slope estimate from history (best-effort)
    def get_slope(history, product, strategy, n):
        nets = [h["net"] for h in history
                if h["product"] == product and h["strategy"] == strategy]
        if len(nets) < 2:
            return 0.0
        nets = nets[-n:]
        if len(nets) < 2:
            return 0.0
        return float(nets[-1] - nets[0]) / len(nets)

    history = state.get("history", [])
    held_ns3  = get_slope(history, held_entry["product"], held_entry["strategy"], 3)
    held_ns5  = get_slope(history, held_entry["product"], held_entry["strategy"], 5)
    held_ns10 = get_slope(history, held_entry["product"], held_entry["strategy"], 10)

    # Positive streak from history
    def pos_streak(history, product, strategy):
        streak = 0
        for h in reversed(history):
            if h["product"] == product and h["strategy"] == strategy and h["net"] > 0:
                streak += 1
            else:
                break
        return streak

    held_streak   = pos_streak(history, held_entry["product"], held_entry["strategy"])
    hold_duration = state["snap_count"] - state.get("hold_start_snap", 0)
    switch_count  = state.get("switch_count", 0)

    # Best challenger
    challengers = [e for e in positive
                   if not (e["product"] == held_entry["product"]
                           and e["strategy"] == held_entry["strategy"])]
    if challengers:
        chal       = challengers[0]
        chal_net   = float(chal.get("total_net", 0))
        chal_rank  = 1.0 + next((i for i, e in enumerate(positive)
                                  if e["product"] == chal["product"]
                                  and e["strategy"] == chal["strategy"]), 0)
        chal_score = chal_net / max_net
        chal_ns3   = get_slope(history, chal["product"], chal["strategy"], 3)
        chal_ns5   = get_slope(history, chal["product"], chal["strategy"], 5)
        chal_ns10  = get_slope(history, chal["product"], chal["strategy"], 10)
    else:
        chal = None
        chal_net = chal_rank = chal_score = chal_ns3 = chal_ns5 = chal_ns10 = 0.0

    now = datetime.now()
    minute_of_day = now.hour * 60 + now.minute

    X = np.array([[
        held_net, held_rank, held_score,
        held_ns3, held_ns5, held_ns10,
        float(held_streak), float(hold_duration), float(switch_count),
        chal_net, chal_rank, chal_score,
        chal_ns3, chal_ns5, chal_ns10,
        chal_net - held_net,
        chal_score - held_score,
        float(num_pos),
        float(minute_of_day),
    ]])

    return X, held_entry, chal, num_pos


# ---------------------------------------------------------------------------
# Confidence: softmax-based [0, 1]
# ---------------------------------------------------------------------------

def softmax_confidence(q_hold, q_switch, q_flat):
    qs = np.array([q_hold, max(q_switch, -100.0), q_flat])
    qs = qs - qs.max()
    exp_qs = np.exp(qs)
    probs  = exp_qs / exp_qs.sum()
    return round(float(probs.max()), 4)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Shadow writer: product_type={PRODUCT_TYPE}, date={TODAY}")

    # Load model
    payload      = load_model()
    model_hold   = payload["model_hold"]
    model_switch = payload.get("model_switch")
    print(f"  Model loaded: version={payload['model_version']}, "
          f"trained={payload['trained_on']}, n_samples={payload['n_samples']}")

    # Load live data
    entries, last_update = load_top20()
    print(f"  Live data: {len(entries)} entries, last_update={last_update}")

    # Load state
    state = load_state()
    state["snap_count"] = state.get("snap_count", 0) + 1

    # Build features
    X, held_entry, chal_entry, num_pos = build_features(entries, state, payload)

    if X is None:
        print("  No positive candidates -- outputting FLAT")
        output = {
            "timestamp": datetime.now().isoformat(),
            "product_type": PRODUCT_TYPE,
            "current_production_selection": None,
            "learned_recommendation": "FLAT",
            "learned_target": None,
            "q_hold": 0.0, "q_switch": 0.0, "q_flat": 0.0,
            "confidence": 1.0,
            "num_positive_candidates": 0,
            "model_version": payload["model_version"],
        }
    else:
        q_hold = float(model_hold.predict(X)[0])
        # v3 gate: FLAT only when no positive candidates
        q_flat = 0.0 if num_pos == 0 else -9999.0
        q_switch = -9999.0
        if chal_entry is not None and float(chal_entry.get("total_net", 0)) > 0 and model_switch:
            q_switch = float(model_switch.predict(X)[0])

        scores = {"HOLD": q_hold, "SWITCH": q_switch, "FLAT": q_flat}
        best_action = max(scores, key=scores.get)
        confidence  = softmax_confidence(q_hold, q_switch, q_flat)

        current_sel = (f"{held_entry['strategy']}|{held_entry['product']}"
                       if held_entry else None)
        if best_action == "SWITCH" and chal_entry:
            target = f"{chal_entry['strategy']}|{chal_entry['product']}"
        elif best_action == "HOLD" and held_entry:
            target = f"{held_entry['strategy']}|{held_entry['product']}"
        else:
            target = None

        output = {
            "timestamp": datetime.now().isoformat(),
            "product_type": PRODUCT_TYPE,
            "current_production_selection": current_sel,
            "learned_recommendation": best_action,
            "learned_target": target,
            "q_hold":   round(q_hold, 4),
            "q_switch": round(q_switch, 4) if q_switch > -9000 else 0.0,
            "q_flat":   round(q_flat, 4) if q_flat > -9000 else 0.0,
            "confidence": confidence,
            "num_positive_candidates": num_pos,
            "model_version": payload["model_version"],
        }

        print(f"  Held:   {current_sel} (net={held_entry.get('total_net', 0):.1f})")
        if chal_entry:
            print(f"  Chal:   {chal_entry['strategy']}|{chal_entry['product']} "
                  f"(net={chal_entry.get('total_net', 0):.1f})")
        print(f"  Q_hold={q_hold:.2f} Q_switch={q_switch:.2f} Q_flat={q_flat:.2f}")
        print(f"  Recommendation: {best_action} -> {target} (confidence={confidence})")

        # Update state
        if best_action == "SWITCH" and chal_entry:
            state["held_product"]    = chal_entry["product"]
            state["held_strategy"]   = chal_entry["strategy"]
            state["hold_start_snap"] = state["snap_count"]
            state["switch_count"]    = state.get("switch_count", 0) + 1
        elif best_action == "FLAT":
            state["held_product"]  = None
            state["held_strategy"] = None
        elif held_entry:
            state["held_product"]  = held_entry["product"]
            state["held_strategy"] = held_entry["strategy"]

        # Append to history (keep last 10)
        if held_entry:
            state.setdefault("history", []).append({
                "snap":     state["snap_count"],
                "product":  held_entry["product"],
                "strategy": held_entry["strategy"],
                "net":      held_entry.get("total_net", 0),
            })
        if len(state["history"]) > 10:
            state["history"] = state["history"][-10:]

    # Write output
    PT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)
    save_state(state)
    print(f"  Written: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
