
import os
import json
from pathlib import Path

def sync_active_trades():
    # Use absolute paths
    base_dir = Path(r'C:\Users\edebe\eds\TradeApps\breakout')
    config_file = base_dir / 'config.json'
    active_trades_file = base_dir / 'active_trades.json'
    
    if not config_file.exists():
        print("Config not found.")
        return
        
    with open(config_file, 'r') as f:
        config = json.load(f)
        
    run_mode = config.get('run_mode', 'live').lower()
    key = 'send_json_files' if run_mode == 'live' else 'send_json_files_sim'
    # Default fallback
    default_dir = r'C:\Users\edebe\eds\trades_rt3\orders' if run_mode == 'live' else r'C:\Users\edebe\eds\trades_rt3_sim\orders'
    orders_dir = Path(config.get(key, default_dir))
    
    print(f"Syncing active trades from: {orders_dir}")
    
    new_state = {}
    
    if orders_dir.exists():
        for json_path in orders_dir.glob('*.json'):
            # Only count open orders? 
            # Actually, the orders directory usually only contains active orders.
            # Filename pattern: order_{mode}_{product}_{direction}_{script}_{id}_{phase}.json
            try:
                with open(json_path, 'r') as f:
                    data = json.load(f)
                    
                if data.get('phase', '').upper() == 'OPEN':
                    product = data.get('product', '').upper()
                    # Mapping 'BUY'/'LONG' and 'SELL'/'SHORT'
                    direction = data.get('direction', '').upper()
                    if direction in ('BUY', 'LONG'): direction = 'LONG'
                    if direction in ('SELL', 'SHORT'): direction = 'SHORT'
                    
                    key = f"{product}_{direction}"
                    new_state[key] = new_state.get(key, 0) + 1
                    print(f"Found active order: {json_path.name}")
            except Exception as e:
                print(f"Error reading {json_path}: {e}")
                
    print(f"Final sync state: {new_state}")
    
    with open(active_trades_file, 'w') as f:
        json.dump(new_state, f, indent=2)
    print("Done.")

if __name__ == '__main__':
    sync_active_trades()
