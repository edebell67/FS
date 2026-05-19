import subprocess
import json
import os
from pathlib import Path

# Strategy parameters
PARAMS = [
    "--symbol", "GBP",
    "--conf_high", "29",
    "--conf_med", "17",
    "--conf_low", "4",
    "--bucket_minutes", "3",
    "--price_offset", "3.00",
    "--fixed_tp", "20.0",
    "--fixed_sl", "10.0",
    "--round_turn_cost", "-2.0"
]

# Historical dates to test
DATES = ["2026-05-11", "2026-05-12", "2026-05-13", "2026-05-14", "2026-05-15", "2026-05-18"]
BASE_PATH = Path(r"X:\EDS\TradeApps\breakout\fs\json\live\forex")
BACKTESTER = Path(r"C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\logic\backtest_gbp_analyzer.py")

results = []

for date in DATES:
    data_file = BASE_PATH / date / "_price_capture.jsonl"
    if not data_file.exists():
        print(f"Skipping {date}: File not found.")
        continue
    
    print(f"Running backtest for {date}...")
    cmd = ["python", str(BACKTESTER), "--data", str(data_file)] + PARAMS
    
    try:
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # Handle potential encoding issues from PowerShell redirects
        output = process.stdout.strip()
        if output.startswith('\ufeff'): output = output[1:] # Strip BOM
        
        data = json.loads(output)
        trades = data.get("trades", [])
        alt_net = sum(t.get("alt_pips", 0.0) for t in trades)
        
        results.append({
            "date": date,
            "normal_net": data.get("total_net", 0.0),
            "alt_net": round(alt_net, 2),
            "trades": len(trades),
            "duration": data.get("duration_hours", 0.0)
        })
    except Exception as e:
        print(f"Error on {date}: {e}")

print("\n" + "="*60)
print(f"{'Date':<12} | {'Trades':<6} | {'Normal Net':<12} | {'Alt Net':<10}")
print("-" * 60)

total_alt = 0.0
total_trades = 0

for r in results:
    print(f"{r['date']:<12} | {r['trades']:<6} | {r['normal_net']:<12} | {r['alt_net']:<10}")
    total_alt += r["alt_net"]
    total_trades += r["trades"]

print("-" * 60)
print(f"{'TOTAL':<12} | {total_trades:<6} | {'N/A':<12} | {total_alt:<10.2f}")
print("="*60)
