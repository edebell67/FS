
import os
import json
from pathlib import Path
from paths import BREAKOUT_LEGACY_JSON_ROOT

BASE_PATH = BREAKOUT_LEGACY_JSON_ROOT

def count_live_trades():
    count = 0
    total_files = 0
    
    print(f"Scanning {BASE_PATH}...")
    
    for file_path in BASE_PATH.rglob('*.json'):
        # Skip activations.json and non-trade files if any
        if file_path.name == 'activations.json':
            continue
            
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
                # Check if it's a trade file (has trade_id)
                if 'trade_id' in data:
                    total_files += 1
                    if data.get('is_live_trade') is True:
                        count += 1
                        # Optional: Print first few found
                        # if count <= 5:
                        #     print(f"Found live trade: {file_path}")
                        
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            
    print(f"\nTotal trade files scanned: {total_files}")
    print(f"Trades with is_live_trade: true: {count}")

if __name__ == "__main__":
    count_live_trades()
