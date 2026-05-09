#!/usr/bin/env python3
"""
Analyze _summary_net.json to find top 5 strategies by net value at each 15-minute interval
From 00:00 to 16:00
"""
import json
from datetime import datetime
import sys
from pathlib import Path
from json_layout import configured_product_types, load_layout_config, resolve_day_dir

# Get date from command line argument or use default
if len(sys.argv) > 1:
    target_date = sys.argv[1]
else:
    target_date = "2026-01-24"

base_dir = Path(__file__).parent
json_root = base_dir / "json"
config = load_layout_config(base_dir / "config.json")
strategies = {}
loaded_paths = []

for product_type in configured_product_types(config):
    json_path = resolve_day_dir(json_root, "live", target_date, product_type) / "_summary_net.json"
    if not json_path.exists():
        continue
    loaded_paths.append(str(json_path))
    with open(json_path, 'r') as f:
        data = json.load(f)
    for strategy_name, products in data.get('strategies', {}).items():
        strategies.setdefault(strategy_name, {}).update(products)

if not loaded_paths:
    raise FileNotFoundError(f"No _summary_net.json found for {target_date} in configured product-type folders")

print("Loading data from:")
for loaded_path in loaded_paths:
    print(f"  - {loaded_path}")

data = {"strategies": strategies}

# Generate 15-minute timestamps from 00:15 to 16:00
intervals = []
for hour in range(0, 17):  # 0 to 16 inclusive
    for minute in [0, 15, 30, 45]:
        if hour == 0 and minute == 0:
            continue  # Skip 00:00 (midnight)
        if hour == 16 and minute > 0:
            break  # Stop at 16:00, don't include 16:15, 16:30, 16:45
        time_str = f"{target_date}T{hour:02d}:{minute:02d}:00"
        intervals.append(time_str)

# For each interval, find the top 5 strategies by net value
results = []

for target_time_str in intervals:
    target_time = datetime.fromisoformat(target_time_str)
    
    # Collect all strategy/product combinations and their net values at or before this time
    strategy_values = {}
    
    for strategy_name, products in data.get('strategies', {}).items():
        for product_name, time_series in products.items():
            # Find the latest entry at or before target_time
            latest_entry = None
            latest_time = None
            
            for entry in time_series:
                entry_time_str = entry['t'].replace('Z', '')
                entry_time = datetime.fromisoformat(entry_time_str)
                
                if entry_time <= target_time:
                    if latest_time is None or entry_time > latest_time:
                        latest_time = entry_time
                        latest_entry = entry
            
            if latest_entry and 'net' in latest_entry:
                key = f"{strategy_name}_{product_name}"
                strategy_values[key] = latest_entry['net']
    
    # Sort by net value (descending) and get top 5
    if strategy_values:
        sorted_strategies = sorted(strategy_values.items(), key=lambda x: x[1], reverse=True)
        top_5 = sorted_strategies[:5]
        
        results.append({
            'time': target_time_str,
            'top_5': top_5
        })

# Save to misc directory
output_file = rf"C:\Users\edebe\eds\misc\top_strategies_{target_date}.txt"

with open(output_file, 'w') as f:
    f.write(f"TOP 5 STRATEGIES BY NET VALUE AT EACH 15-MINUTE INTERVAL ({target_date})\n")
    f.write(f"Time Range: 00:15 - 16:00\n")
    f.write("=" * 100 + "\n\n")
    
    for result in results:
        time_str = result['time'][11:16]  # Extract HH:MM
        
        f.write(f"Time: {time_str}\n")
        f.write("-" * 100 + "\n")
        
        if result['top_5']:
            for i, (strategy, net) in enumerate(result['top_5'], 1):
                f.write(f"  {i}. {strategy:<70} ${net:>10.2f}\n")
        else:
            f.write("  No data available\n")
        
        f.write("\n")
    
    f.write("=" * 100 + "\n")
    f.write(f"Total intervals analyzed: {len(results)}\n")

print(f"\nAnalysis complete!")
print(f"Results saved to: {output_file}")
print(f"Total intervals analyzed: {len(results)}")
