import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:5000/api"

def run_test():
    print("--- STEP 1: ACTIVATING BUY STRATEGY ---")
    payload = {
        "strategy": "breakout_4_tp5.0_sl30.0",
        "product": "CAD",
        "metric": "buy_net",
        "mode": "live",
        "bias": "BUY"
    }
    r = requests.post(f"{BASE_URL}/smart_target/activate", json=payload)
    print(f"Activation Result: {r.json()}")

    # Check the grid
    with open('grid_live.json', 'r') as f:
        grid = json.load(f)
        print(f"\nCurrent Grid State: {json.dumps(grid, indent=2)}")

if __name__ == "__main__":
    run_test()
