import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from json_layout import configured_product_types, load_layout_config, resolve_day_dir

base_dir = Path(__file__).parent
json_root = base_dir / "json"
config = load_layout_config(base_dir / "config.json")
file_path = None
top20_path = None
for product_type in configured_product_types(config):
    trades_candidate = resolve_day_dir(json_root, "live", "2026-02-06", product_type) / "_trades_summary.json"
    top20_candidate = resolve_day_dir(json_root, "live", "2026-02-06", product_type) / "_top20.json"
    if file_path is None and trades_candidate.exists():
        file_path = trades_candidate
    if top20_path is None and top20_candidate.exists():
        top20_path = top20_candidate

if file_path is None:
    raise FileNotFoundError("No _trades_summary.json found for 2026-02-06 in configured product-type folders")

with open(file_path, 'r') as f:
    data = json.load(f)

trades = data.get('trades', [])

# 1. Determine Bias & Initial Profitability (First 2 hours)
def parse_time(ts):
    try:
        return datetime.fromisoformat(ts.replace('Z', ''))
    except:
        return datetime.min

start_time = datetime.min
for t in trades:
    et = parse_time(t.get('entry_time'))
    if start_time == datetime.min or (et != datetime.min and et < start_time):
        start_time = et

bias_window_end = start_time + timedelta(hours=2)
bias_trades = [t for t in trades if parse_time(t.get('entry_time')) <= bias_window_end]

# Calculate Global Bias
total_buys = sum(1 for t in bias_trades if 'long' in (t.get('direction') or 'LONG').lower())
total_sells = sum(1 for t in bias_trades if 'short' in (t.get('direction') or 'SHORT').lower())
bias = 'BUY' if total_buys > total_sells else 'SELL'

# Calculate per-strategy Side Net in first 2 hours
init_side_net = {}
for t in bias_trades:
    is_correct_side = (bias == 'BUY' and 'long' in (t.get('direction') or '').lower()) or \
                      (bias == 'SELL' and 'short' in (t.get('direction') or '').lower())
    if is_correct_side:
        app = t.get('app_name')
        init_side_net[app] = init_side_net.get(app, 0) + (t.get('net_return') or 0)

# Load Top 20 names (Strategy only, ignoring product for global focus)
top20_names = set()
if top20_path is not None and os.path.exists(top20_path):
    with open(top20_path, 'r') as f:
        t20_data = json.load(f)
        for item in t20_data.get('top20', []):
            top20_names.add(item.get('strategy'))

# 2. Identify Groups (1:4 Ratio required for both)
import re

def get_tp_sl(name):
    # Regex to extract tp and sl: e.g. tp10.0_sl50.0
    tp_match = re.search(r'tp([\d\.]+)', name)
    sl_match = re.search(r'sl([\d\.]+)', name)
    if tp_match and sl_match:
        return float(tp_match.group(1)), float(sl_match.group(1))
    return None, None

group_top20 = []
group_posnet = []
all_apps = set(t.get('app_name') for t in trades)

for app in all_apps:
    tp, sl = get_tp_sl(app)
    ratio_ok = (tp is not None and sl is not None and sl > 0 and (tp / sl) <= 0.25)
    if not ratio_ok: continue
    
    if app in top20_names:
        group_top20.append(app)
    if init_side_net.get(app, 0) > 0:
        group_posnet.append(app)

print(f"Bias Window: {start_time.strftime('%H:%M:%S')} - {bias_window_end.strftime('%H:%M:%S')}")
print(f"Bias: {bias} | Top20 Count: {len(group_top20)} | PosNet Count: {len(group_posnet)}")

# 3. Simulate Sequential Trading After 2 Hours
trading_trades = [t for t in trades if parse_time(t.get('entry_time')) > bias_window_end]

def simulate_group(apps, label):
    group_results = []
    for app in apps:
        selected_trades = [t for t in trading_trades if t.get('app_name') == app]
        if bias == 'BUY':
            selected_trades = [t for t in selected_trades if 'long' in (t.get('direction') or 'LONG').lower()]
        else:
            selected_trades = [t for t in selected_trades if 'short' in (t.get('direction') or 'SHORT').lower()]

        selected_trades.sort(key=lambda x: parse_time(x.get('entry_time')))
        executed_trades = []
        last_exit_time = datetime.min
        for t in selected_trades:
            if parse_time(t.get('entry_time')) >= last_exit_time:
                executed_trades.append(t)
                last_exit_time = parse_time(t.get('exit_time'))

        if executed_trades:
            net = sum(t.get('net_return', 0) for t in executed_trades)
            group_results.append({'strategy': app, 'net': net, 'trades': len(executed_trades)})
    
    group_results.sort(key=lambda x: x['net'], reverse=True)
    return group_results

res_top20 = simulate_group(group_top20, "Top 20")
res_posnet = simulate_group(group_posnet, "Positive Net")

print(f"\n--- Comparison (Sequential Bias Trading) ---")
print(f"{'Metric':<20} | {'Top 20 Group':<15} | {'PosNet Group':<15}")
print("-" * 55)
print(f"{'Eligible Count':<20} | {len(group_top20):<15} | {len(group_posnet):<15}")
print(f"{'Total Sum Net':<20} | {sum(r['net'] for r in res_top20):<15.2f} | {sum(r['net'] for r in res_posnet):<15.2f}")
avg_top = sum(r['net'] for r in res_top20)/len(res_top20) if res_top20 else 0
avg_pos = sum(r['net'] for r in res_posnet)/len(res_posnet) if res_posnet else 0
print(f"{'Avg Net Per Strat':<20} | {avg_top:<15.2f} | {avg_pos:<15.2f}")

print(f"\n--- Best Performers in PosNet Group (not in Top 20) ---")
top20_set = set(top20_names)
pos_only = [r for r in res_posnet if r['strategy'] not in top20_set]
print(f"{'Strategy':<35} | {'Trades':<10} | {'Net Return':<10}")
print("-" * 60)
for res in pos_only[:10]:
    print(f"{res['strategy']:<35} | {res['trades']:<10} | {res['net']:<10.2f}")
