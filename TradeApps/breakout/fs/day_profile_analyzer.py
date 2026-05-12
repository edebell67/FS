import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from json_layout import configured_product_types, load_layout_config, resolve_day_dir
from paths import BREAKOUT_JSON_ROOT

def parse_time(ts):
    try:
        return datetime.fromisoformat(ts.replace('Z', ''))
    except:
        return datetime.min

def analyze_day_profile(date_str):
    base_dir = Path(__file__).parent
    json_root = BREAKOUT_JSON_ROOT
    config = load_layout_config(base_dir / 'config.json')
    summary_path = None
    for product_type in configured_product_types(config):
        candidate = resolve_day_dir(json_root, 'live', date_str, product_type) / '_trades_summary.json'
        if candidate.exists():
            summary_path = candidate
            break
    if summary_path is None or not os.path.exists(summary_path):
        print("Summary not found")
        return

    with open(summary_path, 'r') as f:
        data = json.load(f)
    trades = data.get('trades', [])

    hourly_stats = {}
    for t in trades:
        et = parse_time(t.get('entry_time'))
        if et == datetime.min: continue
        
        hour = et.hour
        side = 'BUY' if 'long' in (t.get('direction') or 'LONG').lower() else 'SELL'
        net = t.get('net_return', 0)
        
        if hour not in hourly_stats:
            hourly_stats[hour] = {'BUY_NET': 0, 'SELL_NET': 0, 'BUY_COUNT': 0, 'SELL_COUNT': 0}
        
        if side == 'BUY':
            hourly_stats[hour]['BUY_NET'] += net
            hourly_stats[hour]['BUY_COUNT'] += 1
        else:
            hourly_stats[hour]['SELL_NET'] += net
            hourly_stats[hour]['SELL_COUNT'] += 1

    print(f"Hourly Profile for {date_str}")
    print(f"{'Hour':<5} | {'BUY Net':<10} | {'SELL Net':<10} | {'B Count':<8} | {'S Count':<8}")
    print("-" * 55)
    for h in sorted(hourly_stats.keys()):
        s = hourly_stats[h]
        print(f"{h:02d}:00 | {s['BUY_NET']:<10.2f} | {s['SELL_NET']:<10.2f} | {s['BUY_COUNT']:<8} | {s['SELL_COUNT']:<8}")

if __name__ == "__main__":
    analyze_day_profile('2026-02-05')
