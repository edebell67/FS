import json
from collections import defaultdict

file_path = r"X:\EDS\TradeApps\breakout\fs\json\live\forex\2026-03-29\_summary_net.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

strategies = data.get("strategies", {})

products = set()
strat_family = defaultdict(int)
total_datapoints = 0
open_positions_count = 0

model_final_net = {}
product_final_net = defaultdict(float)
product_trades = defaultdict(lambda: {"b_c": 0, "s_c": 0})

time_stamps = []

for strat_name, prod_dict in strategies.items():
    # classify strategy family
    family = strat_name.split("_2_")[0].split("_3_")[0].split("_4_")[0]
    strat_family[family] += 1
    
    strat_net_sum = 0.0
    for prod, points in prod_dict.items():
        products.add(prod)
        total_datapoints += len(points)
        if not points:
            continue
        last_pt = points[-1]
        time_stamps.append(last_pt.get("t", ""))
        net_val = last_pt.get("net", 0.0)
        strat_net_sum += net_val
        product_final_net[prod] += net_val
        
        # trade counts
        product_trades[prod]["b_c"] += last_pt.get("b_c", 0)
        product_trades[prod]["s_c"] += last_pt.get("s_c", 0)
        
        if last_pt.get("open"):
            open_positions_count += 1
            
    model_final_net[strat_name] = strat_net_sum

print("=================================================================")
print("SUMMARY NET FILE ANALYSIS: 2026-03-29")
print("=================================================================")
print(f"File: {file_path}")
print(f"Last Update Timestamp: {data.get('last_update')}")
print(f"Session Max Net: {data.get('session_max_net')}")
print(f"Total Models / Strategies: {len(strategies)}")
print(f"Total Currency Products Tracked: {len(products)} -> {sorted(list(products))}")
print(f"Total Time-series Datapoints: {total_datapoints}")
print(f"Currently Active Open Markers: {open_positions_count}")

print("\n--- Strategy Families Breakdown ---")
for fam, count in sorted(strat_family.items(), key=lambda x: x[1], reverse=True):
    print(f" - {fam}: {count} parameter variants")

print("\n--- P&L and Trade Counts by Currency Product ---")
total_session_net = 0.0
for prod in sorted(products):
    p_net = product_final_net[prod]
    total_session_net += p_net
    b = product_trades[prod]["b_c"]
    s = product_trades[prod]["s_c"]
    print(f" {prod:10s} | Net P&L: {p_net:10.2f} | Buy Closed: {b:5d} | Sell Closed: {s:5d} | Total Closed: {b+s:5d}")

print(f"\nTOTAL AGGREGATE SYSTEM NET: {total_session_net:.2f}")

# Top 10 Best Performers
sorted_models = sorted(model_final_net.items(), key=lambda x: x[1], reverse=True)

print("\n--- TOP 10 BEST PERFORMING STRATEGY MODELS ---")
for idx, (m, n) in enumerate(sorted_models[:10], 1):
    print(f" {idx:2d}. {m:35s} | Net P&L: {n:8.2f}")

print("\n--- TOP 10 WORST PERFORMING STRATEGY MODELS ---")
for idx, (m, n) in enumerate(sorted_models[-10:], 1):
    print(f" {idx:2d}. {m:35s} | Net P&L: {n:8.2f}")

# Timestamp bounds
valid_ts = [t for t in time_stamps if t]
if valid_ts:
    print(f"\nTimeline Coverage: From {min(valid_ts)} To {max(valid_ts)}")

