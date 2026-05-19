import json
from pathlib import Path

json_path = Path(r'C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\logic\gbp_v6_bt_1618.json')
try:
    with open(json_path, 'r', encoding='utf-16') as f:
        content = f.read()
except:
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()

data = json.loads(content)
trades = data['trades']

print("--- V6 Backtest Trades (Comparison Window: 12:22 PM onwards) ---")
window_net = 0.0
for t in trades:
    if t['entry_ts'] >= '2026-05-18T12:22':
        window_net += t['pips']
        print(f"{t['entry_ts']} -> {t['exit_ts']} | {t['direction']} | Pips: {t['pips']:>6} | Reason: {t['exit_reason']}")

print(f"\nWindow Net Pips (Since 12:22 PM): {window_net:.2f}")
print(f"Full Day Net Pips: {data['total_net']}")
