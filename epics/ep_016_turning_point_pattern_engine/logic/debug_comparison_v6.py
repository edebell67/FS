import json
from pathlib import Path

json_path = Path(r'C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\logic\gbp_v6_bt_latest.json')
try:
    with open(json_path, 'r', encoding='utf-16') as f:
        content = f.read()
except:
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()

data = json.loads(content)
trades = data['trades']

print("--- Backtest V6 Trades (After 12:00 PM) ---")
for t in trades:
    if t['entry_ts'] >= '2026-05-18T12:00':
        print(f"{t['entry_ts']} -> {t['exit_ts']} | {t['direction']} | Pips: {t['pips']:>6} | Reason: {t['exit_reason']}")

print(f"\nTotal trades in backtest today: {len(trades)}")
print(f"Total net pips in backtest today: {data['total_net']}")
