
import os
import json
from pathlib import Path
import re

def cleanup_l_trades():
    base_dir = Path(r'c:\Users\edebe\eds\TradeApps\breakout')
    json_dir = base_dir / 'json' / 'live' / '2025-12-31'
    activations_file = base_dir / 'activations.json'
    
    if not activations_file.exists():
        print("Activations file not found.")
        return
        
    with open(activations_file, 'r') as f:
        activations_data = json.load(f).get('live', {})
        
    print(f"Scanning trades in {json_dir}...")
    
    files = list(json_dir.glob('*.json'))
    changed_count = 0
    
    for json_path in files:
        if json_path.name.startswith(('vt_', '_')):
            continue
            
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
        except Exception as e:
            continue
            
        if not data.get('is_live_trade'):
            continue
            
        product = data.get('product', '').upper()
        direction_key = 'buy' if data.get('direction', '').upper() in ('LONG', 'BUY') else 'sell'
        print(f"Checking live trade: {json_path.name} ({product} {direction_key})")
        
        matched_any = False
        
        # Extract params from JSON 
        win = data.get('window_size')
        buf = data.get('pip_buffer')
        tp = data.get('tp_pips')
        sl = data.get('sl_pips')
        fname = json_path.stem

        for act_key, act_val in activations_data.items():
            if not act_val.get('active'):
                continue
            
            activated_products = [p.upper() for p in (act_val.get('products') or [])]
            if product not in activated_products:
                continue
                
            if f"_{direction_key}_" not in act_key:
                continue
                
            parts = act_key.split('_')
            try:
                k_dir = parts[-2]
                k_sl = float(parts[-3])
                k_tp = float(parts[-4])
                k_buf = float(parts[-5])
                k_win = int(parts[-6])
                k_script = '_'.join(parts[:-6])
                
                if (k_win == win and 
                    abs(k_buf - buf) < 1e-7 and 
                    abs(k_tp - tp) < 1e-7 and 
                    abs(k_sl - sl) < 1e-7 and 
                    k_dir == direction_key):
                    
                    if k_script in fname:
                        matched_any = True
                        print(f"  Match found: {act_key}")
                        break
            except:
                pass
        
        if not matched_any:
            print(f"  Converting {json_path.name} to normal trade (orphaned)")
            data['is_live_trade'] = False
            data['order_sent_net'] = False
            data['order_sent_alt'] = False
            data['trade_block_reason'] = f"Cleaned: Orphaned L-trade (Product {product} not activated)."
            
            with open(json_path, 'w') as f:
                json.dump(data, f, indent=2)
            changed_count += 1
            
    print(f"Cleanup complete. Modified {changed_count} trades.")

if __name__ == '__main__':
    cleanup_l_trades()
