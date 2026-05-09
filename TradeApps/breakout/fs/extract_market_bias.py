import json
import os
from datetime import datetime, timezone

def extract_bias():
    # 1. Determine Path
    # Assuming standard path structure used by the app
    # Default to today's date and live mode
    today_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    base_path = r"c:\Users\edebe\eds\TradeApps\breakout\fs\json\live"
    file_path = os.path.join(base_path, today_str, "_targeted_strategies.json")
    
    print(f"Reading Highight Criteria from: {file_path}")

    if not os.path.exists(file_path):
        print(f"Error: File not found for today ({today_str}).")
        return

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # 2. Extract Fields displayed in UI
        bias = data.get('bias', 'UNKNOWN')
        status = data.get('status', 'UNKNOWN')
        condition = data.get('market_condition', 'UNKNOWN')
        
        # 3. Output
        print("\n--- MARKET BIAS HIGHLIGHT ---")
        print(f"Current Bias:     {bias}")
        print(f"Monitor Status:   {status}")
        print(f"Market Condition: {condition}")
        print("-----------------------------")
        
        # Check for Strong/Mixed logic (often used for highlighting)
        if status == "STRONG":
             print(f"ACTION: >> FOLLOW {bias} <<")
        elif status == "MIXED":
             print(f"ACTION: CAUTION (Mixed Signals)")
             
    except Exception as e:
        print(f"Error reading or parsing file: {e}")

if __name__ == "__main__":
    extract_bias()
