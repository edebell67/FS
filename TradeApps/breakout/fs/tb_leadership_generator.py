import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# datetime stamp: 2026-03-20 12:50
VERSION = "V20260320_1250"

def generate_tb_leadership(mode='live', date_str=None, product_type='forex'):
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    base_path = Path(f"c:/Users/edebe/eds/TradeApps/breakout/fs/json/{mode}/{product_type}/{date_str}")
    bucket_file = base_path / "_trade_buckets.json"
    summary_net_file = base_path / "_summary_net.json"
    output_file = base_path / "_tb_leadership.json"

    if not bucket_file.exists() or not summary_net_file.exists():
        print(f"Missing required files in {base_path}")
        return

    with open(bucket_file, 'r') as f:
        buckets_data = json.load(f)
    
    with open(summary_net_file, 'r') as f:
        summary_net = json.load(f)

    strategies_data = summary_net.get('strategies', {})
    
    leadership_report = []

    for bucket in buckets_data.get('buckets', []):
        bucket_name = bucket.get('name', 'Unknown')
        members = bucket.get('strategies', [])
        min_diff = float(bucket.get('minimum_difference', 0.0))
        
        # Collect all timestamps for strategies in this bucket
        all_timestamps = set()
        member_series = {}
        
        for m in members:
            # Extract strategy and product from bucket key (e.g., "strat | PROD")
            raw_key = m if isinstance(m, str) else m.get('key')
            if not raw_key: continue
            
            # Normalize bucket key
            if ' | ' in raw_key:
                b_strat, b_prod = raw_key.split(' | ', 1)
            elif ':' in raw_key:
                b_strat, b_prod = raw_key.split(':', 1)
            else:
                b_strat, b_prod = raw_key, None

            found = False
            for s_name, products in strategies_data.items():
                if s_name == b_strat:
                    for p_name, series in products.items():
                        if b_prod is None or p_name == b_prod:
                            series_key = f"{s_name}:{p_name}"
                            member_series[series_key] = series
                            for entry in series:
                                all_timestamps.add(entry['t'])
                            found = True
                            break # Found product
                if found: break
            
        if not member_series:
            continue

        sorted_ts = sorted(list(all_timestamps))
        
        current_leader = None
        leader_start_time = None
        
        bucket_leadership = {
            "bucket": bucket_name,
            "windows": []
        }

        # Helper to get net at or before T
        def get_net_at(series, ts):
            last_net = 0.0
            for entry in series:
                if entry['t'] <= ts:
                    last_net = float(entry.get('net', 0.0))
                else:
                    break
            return last_net

        for ts in sorted_ts:
            nets = []
            for k, series in member_series.items():
                net = get_net_at(series, ts)
                nets.append({'key': k, 'net': net})
            
            if not nets: continue
            
            nets.sort(key=lambda x: x['net'], reverse=True)
            
            potential_leader = nets[0]
            is_valid_leader = True
            if len(nets) > 1:
                if (nets[0]['net'] - nets[1]['net']) < min_diff:
                    is_valid_leader = False
            
            new_leader_key = potential_leader['key'] if is_valid_leader else None
            
            if new_leader_key != current_leader:
                # Leadership changed
                # Close previous
                if current_leader:
                    bucket_leadership["windows"].append({
                        "strategy": current_leader,
                        "start": leader_start_time,
                        "end": ts
                    })
                
                current_leader = new_leader_key
                leader_start_time = ts

        # Close final leader
        if current_leader:
            bucket_leadership["windows"].append({
                "strategy": current_leader,
                "start": leader_start_time,
                "end": None # Active
            })
            
        leadership_report.append(bucket_leadership)

    # Save to JSON
    with open(output_file, 'w') as f:
        json.dump(leadership_report, f, indent=2)
    
    print(f"Leadership report saved to {output_file}")
    
    # Also print in requested format to console/log
    for bl in leadership_report:
        print(f"TB: {bl['bucket']}")
        for w in bl['windows']:
            print(f"  strategy name : {w['strategy']}")
            print(f"  leadership start : {w['start']}")
            print(f"  leadership end : {w['end'] if w['end'] else ''}")
            print("")

if __name__ == "__main__":
    generate_tb_leadership()
