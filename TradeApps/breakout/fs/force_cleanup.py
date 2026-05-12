
import os
import json
from pathlib import Path
from paths import BREAKOUT_JSON_ROOT

def force_cleanup():
    base_dir = Path(__file__).resolve().parent
    json_dir = BREAKOUT_JSON_ROOT / 'live' / '2025-12-31'
    activations_file = base_dir / 'activations.json'
    
    with open(activations_file, 'r') as f:
        activations_live = json.load(f).get('live', {})
        
    # Get all uniquely activated products from all strategies
    all_activated_products = set()
    for val in activations_live.values():
        if val.get('active'):
            all_activated_products.update([p.upper() for p in (val.get('products') or [])])
            
    print(f"Activated Products: {all_activated_products}")
    
    files = list(json_dir.glob('*.json'))
    modified = 0
    
    for p in files:
        if p.name.startswith(('vt_', '_')): continue
        try:
            if os.path.getsize(p) == 0: continue
            with open(p, 'r') as f:
                data = json.load(f)
        except: continue
        
        # If it's marked live but the product is NOT in any activation list
        product = data.get('product', '').upper()
        if data.get('is_live_trade') and product not in all_activated_products:
            print(f"Force cleaning orphaned trade: {p.name} (Product {product} is nowhere in activation list)")
            data['is_live_trade'] = False
            data['order_sent_net'] = False
            data['order_sent_alt'] = False
            data['trade_block_reason'] = f"Cleaned: Unauthorized L-trade (Product {product} not activated globally)."
            with open(p, 'w') as f:
                json.dump(data, f, indent=2)
            modified += 1
            
    print(f"Force cleanup finished. Modified {modified} trades.")

if __name__ == '__main__':
    force_cleanup()
