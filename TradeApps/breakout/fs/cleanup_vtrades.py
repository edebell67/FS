"""
Manual cleanup script to close excess V-Trades immediately.
[2025-12-26 V20251226_0210]

This will close all V-Trades except:
- The single best LONG trade (if above threshold)
- The single best SHORT trade (if above threshold)
"""
import json
from pathlib import Path
from datetime import datetime
from paths import BREAKOUT_LEGACY_JSON_ROOT

def cleanup_excess_vtrades():
    """Close all excess V-Trades, keeping only the top performer in each direction."""
    
    # Configuration
    virtual_dir = BREAKOUT_LEGACY_JSON_ROOT / 'sim' / '2025-12-26' / 'virtual'
    threshold_y = 0.0  # Adjust if needed from your config
    
    if not virtual_dir.exists():
        print(f"Virtual directory not found: {virtual_dir}")
        return
    
    # Load all open V-Trades
    open_long_trades = []
    open_short_trades = []
    
    for v_file in virtual_dir.glob('vt_*.json'):
        try:
            with open(v_file, 'r') as f:
                data = json.load(f)
            
            if data.get('status') == 'OPEN':
                data['filepath'] = v_file
                direction = data.get('direction')
                if direction == 'LONG':
                    open_long_trades.append(data)
                elif direction == 'SHORT':
                    open_short_trades.append(data)
        except Exception as e:
            print(f"Error reading {v_file.name}: {e}")
    
    print(f"\nFound {len(open_long_trades)} LONG trades and {len(open_short_trades)} SHORT trades")
    
    # Process LONG trades
    if open_long_trades:
        # Sort by net_return descending
        open_long_trades.sort(key=lambda t: float(t.get('net_return', 0)), reverse=True)
        best_long = open_long_trades[0]
        best_long_pnl = float(best_long.get('net_return', 0))
        
        print(f"\nBest LONG: {best_long.get('product')} - {best_long.get('source_strategy')} - ${best_long_pnl:.2f}")
        
        if best_long_pnl > threshold_y:
            print(f"Keeping best LONG trade (above threshold)")
            # Close all others
            for trade in open_long_trades[1:]:
                close_trade(trade, 'TOP_PRODUCT_CHANGED')
        else:
            print(f"Best LONG below threshold - closing all LONG trades")
            for trade in open_long_trades:
                close_trade(trade, 'NO_TOP_PRODUCT')
    
    # Process SHORT trades
    if open_short_trades:
        # Sort by net_return descending
        open_short_trades.sort(key=lambda t: float(t.get('net_return', 0)), reverse=True)
        best_short = open_short_trades[0]
        best_short_pnl = float(best_short.get('net_return', 0))
        
        print(f"\nBest SHORT: {best_short.get('product')} - {best_short.get('source_strategy')} - ${best_short_pnl:.2f}")
        
        if best_short_pnl > threshold_y:
            print(f"Keeping best SHORT trade (above threshold)")
            # Close all others
            for trade in open_short_trades[1:]:
                close_trade(trade, 'TOP_PRODUCT_CHANGED')
        else:
            print(f"Best SHORT below threshold - closing all SHORT trades")
            for trade in open_short_trades:
                close_trade(trade, 'NO_TOP_PRODUCT')
    
    print("\nCleanup complete!")

def close_trade(trade, reason):
    """Close a V-Trade by updating its JSON file."""
    filepath = trade.get('filepath')
    if not filepath:
        return
    
    product = trade.get('product')
    current_price = trade.get('current_price', trade.get('entry_price'))
    
    trade['exit_time'] = datetime.utcnow().isoformat()
    trade['exit_price'] = current_price
    trade['exit_reason'] = reason
    trade['status'] = 'CLOSED'
    
    # Remove filepath key before saving
    trade.pop('filepath', None)
    
    with open(filepath, 'w') as f:
        json.dump(trade, f, indent=2)
    
    print(f"  Closed: {product} - {trade.get('source_strategy')} - ${trade.get('net_return', 0):.2f}")

if __name__ == '__main__':
    cleanup_excess_vtrades()
