import json
from pathlib import Path

json_path = Path(r'C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\logic\gbp_bt_debug_may15.json')
try:
    with open(json_path, 'r', encoding='utf-16') as f:
        content = f.read()
except:
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()

data = json.loads(content)
trades = data['trades']

for t in trades[:10]:
    print(f"{t['entry_ts']} -> {t['exit_ts']} | {t['direction']} | Pips: {t['pips']:>6} | Reason: {t['exit_reason']}")
