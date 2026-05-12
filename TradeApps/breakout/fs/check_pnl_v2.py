import json
import os
from pathlib import Path
from collections import defaultdict
from paths import BREAKOUT_JSON_ROOT # [V20260510_1955]

def _get_trade_script_name_from_data(trade_data):
    if trade_data.get('app_name'):
        return trade_data['app_name']
    if trade_data.get('filename'):
        fname_parts = trade_data['filename'].split('_')
        timestamp_idx = -1
        for i, part in enumerate(fname_parts):
            if len(part) == 8 and part.isdigit():
                timestamp_idx = i
                break
        if timestamp_idx != -1:
            potential_product_idx = timestamp_idx - 1
            if potential_product_idx > 0 and len(fname_parts[potential_product_idx]) == 3 and fname_parts[potential_product_idx].isalpha() and fname_parts[potential_product_idx].isupper():
                return '_'.join(fname_parts[:potential_product_idx])
            else:
                return '_'.join(fname_parts[:timestamp_idx])
    return "UNKNOWN"

# [V20260510_1955] Use centralized path resolution
today_dir = BREAKOUT_JSON_ROOT / 'live' / '2025-12-26'
global_stats = defaultdict(lambda: defaultdict(lambda: {'pnl': 0.0, 'count': 0}))

for json_file in Path(today_dir).glob('*.json'):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        data['filename'] = json_file.name
        if data.get('status') == 'CLOSED':
            script_name = _get_trade_script_name_from_data(data)
            product = data.get('product', 'UNKNOWN').upper()
            direction = (data.get('direction') or '').lower()
            dir_key = 'buy' if 'long' in direction else 'sell'

            net_key = f"{script_name}_{dir_key}_net"
            alt_key = f"{script_name}_{dir_key}_alt"

            global_stats[net_key][product]['pnl'] += float(data.get('net_return', 0.0))
            global_stats[alt_key][product]['pnl'] += float(data.get('alt_net', 0.0))
    except Exception as e:
        print(f"Error {json_file.name}: {e}")
        continue

print("TOP BUY NET:")
top_buy = []
for k, products in global_stats.items():
    if k.endswith('_buy_net'):
        for p, s in products.items():
            top_buy.append((k, p, s['pnl']))

top_buy.sort(key=lambda x: x[2], reverse=True)
for item in top_buy[:5]:
    print(f"  {item[0]} - {item[1]}: {item[2]}")

print("\nTOP SELL NET:")
top_sell = []
for k, products in global_stats.items():
    if k.endswith('_sell_net'):
        for p, s in products.items():
            top_sell.append((k, p, s['pnl']))

top_sell.sort(key=lambda x: x[2], reverse=True)
for item in top_sell[:5]:
    print(f"  {item[0]} - {item[1]}: {item[2]}")
