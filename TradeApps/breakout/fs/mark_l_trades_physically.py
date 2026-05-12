import json
import os
from pathlib import Path
from datetime import datetime
from json_layout import resolve_day_dir # [V20260510_1945]
from paths import BREAKOUT_JSON_ROOT # [V20260510_1945]

# datetime stamp: 2026-05-10 19:45
VERSION = "V20260510_1945" # Path standardization fix

def mark_l_trades_physically(mode='live', date_str=None, product_type='forex'):
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')

    # [V20260510_1945] Use centralized path resolution
    base_path = resolve_day_dir(BREAKOUT_JSON_ROOT, mode, date_str, product_type)
    leadership_file = base_path / "_tb_leadership.json"

    if not leadership_file.exists():
        print(f"Leadership file not found: {leadership_file}")
        return

    with open(leadership_file, 'r') as f:
        leadership_data = json.load(f)

    # Build a lookup map: (strategy, product) -> List of (bucket_name, start_ts, end_ts)
    window_map = {}
    for entry in leadership_data:
        bucket_name = entry.get('bucket')
        for window in entry.get('windows', []):
            strat_key = window.get('strategy') # "Strategy:Product"
            if strat_key not in window_map:
                window_map[strat_key] = []

            start_dt = datetime.fromisoformat(window.get('start').replace(' ', 'T'))
            end_val = window.get('end')
            end_dt = datetime.fromisoformat(end_val.replace(' ', 'T')) if end_val else None

            window_map[strat_key].append({
                'bucket': bucket_name,
                'start': start_dt,
                'end': end_dt
            })

    # Now scan trade files
    trade_count = 0
    marked_count = 0

    # Trade files are in the same directory (or archived subdirs? standard breakout stores them in day_dir)
    # Actually, they might be in product subdirs if partitioned.
    # We'll scan the day_dir and all subdirs.
    for root, dirs, files in os.walk(str(base_path)):
        for file in files:
            if not file.endswith('.json') or file.startswith('_'):
                continue

            file_path = Path(root) / file

            try:
                with open(file_path, 'r') as f:
                    trade = json.load(f)

                # Basic check if it's a trade file
                if 'trade_id' not in trade and 'direction' not in trade:
                    continue

                trade_count += 1
                entry_time = trade.get('entry_time') or trade.get('time')
                if not entry_time: continue

                entry_dt = datetime.fromisoformat(entry_time.replace('Z', '').replace(' ', 'T'))

                strategy = trade.get('app_name', '') or trade.get('script_name', '')
                product = trade.get('product', '')
                strat_key = f"{strategy}:{product}"

                alt_strat = trade.get('source_strategy')
                alt_key = f"{alt_strat}:{product}" if alt_strat else None

                relevant_windows = window_map.get(strat_key, [])
                if alt_key and alt_key in window_map:
                    relevant_windows.extend(window_map[alt_key])

                if not relevant_windows: continue

                l_buckets = set()
                # Check if it was already marked to avoid redundant writes
                existing_l = trade.get('l_trade_in_buckets', [])
                if isinstance(existing_l, str): existing_l = [existing_l]

                for w in relevant_windows:
                    if w['start'] <= entry_dt and (w['end'] is None or entry_dt < w['end']):
                        l_buckets.add(w['bucket'])

                if l_buckets:
                    # Update trade JSON
                    new_l = sorted(list(set(existing_l) | l_buckets))
                    if new_l != existing_l:
                        trade['l_trade_in_buckets'] = new_l
                        trade['tb_l_trades'] = True # General flag as requested

                        with open(file_path, 'w') as f:
                            json.dump(trade, f, indent=2)
                        marked_count += 1
            except Exception as e:
                print(f"Error processing {file}: {e}")

    print(f"Finished. Scanned {trade_count} trades, marked {marked_count} as L-trades.")

if __name__ == "__main__":
    mark_l_trades_physically()
