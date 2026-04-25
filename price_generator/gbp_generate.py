import os
import time
import random
import json
from datetime import datetime
from itertools import combinations

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
# [V20260425_1845] DB Connection REMOVED per user request
JSON_OUTPUT_PATH = r"z:\algo_forex\prices\forex_price_sim.json"

SPREAD = 0.0001
MOVE_RANGE = 0.00007

# ---------------------------------------------------
# Initial prices
# ---------------------------------------------------
prices = {
    "gbp": 1.3058,
    "eur": 1.1701,
    "aud": 0.6505,
    "nzd": 0.5050,
}

# ---------------------------------------------------
def write_json_snapshot(snapshot):
    try:
        # Create directory if missing
        os.makedirs(os.path.dirname(JSON_OUTPUT_PATH), exist_ok=True)
        with open(JSON_OUTPUT_PATH, "w") as f:
            json.dump(snapshot, f, indent=4)
    except Exception as e:
        print(f"Error writing JSON: {e}")

def generate_combinations(price_snapshot):
    """Generate synthetic pair sums (_c)"""
    combos = {}
    for a, b in combinations(price_snapshot.keys(), 2):
        name = f"{a}{b}_c"
        combos[name] = {
            "bid": round(price_snapshot[a]["bid"] + price_snapshot[b]["bid"], 6),
            "ask": round(price_snapshot[a]["ask"] + price_snapshot[b]["ask"], 6),
        }
    return combos

# ---------------------------------------------------
def simulate_market_data():
    print("--- FX Simulation Started (Local JSON Only) ---")
    print(f"Target: {JSON_OUTPUT_PATH}")

    try:
        while True:
            timestamp = datetime.now()

            # Base shocks
            shock_gbp_eur = random.uniform(-MOVE_RANGE, MOVE_RANGE)
            shock_aud_nzd = random.uniform(-MOVE_RANGE, MOVE_RANGE)
            shock_eur_aud = random.uniform(-MOVE_RANGE, MOVE_RANGE)

            # Dynamic correlations
            corr_gbp_eur = random.uniform(0.87, 0.93)
            corr_aud_nzd = random.uniform(0.88, 0.92)
            corr_eur_aud = random.uniform(0.49, 0.51)

            snapshot = {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"),
                "prices": {}
            }

            # --- Process Base instruments
            for code in ["gbp", "eur", "aud", "nzd"]:
                independent = random.uniform(-MOVE_RANGE, MOVE_RANGE)

                if code == "gbp":
                    delta = (
                        corr_gbp_eur * shock_gbp_eur +
                        (1 - corr_gbp_eur) * independent
                    )

                elif code == "eur":
                    delta = (
                        corr_gbp_eur * shock_gbp_eur +
                        corr_eur_aud * shock_eur_aud +
                        (1 - corr_gbp_eur - corr_eur_aud) * independent
                    )

                elif code == "aud":
                    delta = (
                        corr_aud_nzd * shock_aud_nzd +
                        corr_eur_aud * shock_eur_aud +
                        (1 - corr_aud_nzd - corr_eur_aud) * independent
                    )

                elif code == "nzd":
                    delta = (
                        corr_aud_nzd * shock_aud_nzd +
                        (1 - corr_aud_nzd) * independent
                    )

                prices[code] += delta

                bid = round(prices[code] - SPREAD / 2, 6)
                ask = round(prices[code] + SPREAD / 2, 6)

                snapshot["prices"][code] = {
                    "bid": bid,
                    "ask": ask
                }

                print(f"{code.upper()} | {bid:.6f} / {ask:.6f}")

            # --- Generate synthetic combinations (_c)
            combo_prices = generate_combinations(snapshot["prices"])
            for combo_code, px in combo_prices.items():
                snapshot["prices"][combo_code] = px
                print(f"{combo_code.upper()} | {px['bid']:.6f} / {px['ask']:.6f}")

            write_json_snapshot(snapshot)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nSimulation stopped.")

# ---------------------------------------------------
if __name__ == "__main__":
    simulate_market_data()
