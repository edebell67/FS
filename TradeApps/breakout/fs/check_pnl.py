import json
import os
from pathlib import Path
from collections import defaultdict
from paths import BREAKOUT_JSON_ROOT # [V20260510_1955]

# [V20260510_1955] Use centralized path resolution
today_dir = BREAKOUT_JSON_ROOT / 'live' / '2025-12-26'
global_stats = defaultdict(lambda: defaultdict(lambda: {'pnl': 0.0, 'count': 0}))

for json_file in Path(today_dir).glob('*.json'):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        if data.get('status') == 'CLOSED':
            product = data.get('product', 'UNKNOWN').upper()
            net_return = float(data.get('net_return', 0.0))
            alt_net = float(data.get('alt_net', 0.0))

            # Simple assumption for strategy key mapping for this test
            # Filename usually starts with strategy name
            script_name = json_file.name.split('_')[0]
            direction = (data.get('direction') or '').lower()
            dir_key = 'buy' if 'long' in direction else 'sell'

            net_key = f"{script_name}_{dir_key}_net"
            alt_key = f"{script_name}_{dir_key}_alt"

            global_stats[net_key][product]['pnl'] += net_return
            global_stats[alt_key][product]['pnl'] += alt_net
    except:
        continue

print("BUY NET Stats:")
for k, products in global_stats.items():
    if k.endswith('_buy_net'):
        for p, s in products.items():
            print(f"  {k} - {p}: PNL={s['pnl']}")

print("\nSELL NET Stats:")
for k, products in global_stats.items():
    if k.endswith('_sell_net'):
        for p, s in products.items():
            print(f"  {k} - {p}: PNL={s['pnl']}")
