import time
import json
from pathlib import Path
from backtest_gbp_analyzer import GBPBacktester

data_path = r"X:\eds\TradeApps\breakout\fs\json\live\forex\2026-05-14\_price_capture.jsonl"
symbol = "GBPAUD_C"

print("Loading data...")
bt = GBPBacktester(data_path, symbol)
bt.load_data()

print(f"Loaded {len(bt.all_snapshots)} snapshots.")

start = time.time()
for _ in range(100):
    bt.run_simulation()
end = time.time()

avg = (end - start) / 100
print(f"Average Simulation Time: {avg:.4f}s")
print(f"Total time for 100 runs: {end-start:.2f}s")
