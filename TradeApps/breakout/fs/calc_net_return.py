import json
import os
from pathlib import Path
from paths import BREAKOUT_LEGACY_JSON_ROOT

def calculate_total_net_return():
    path = BREAKOUT_LEGACY_JSON_ROOT / "live" / "2026-01-05" / "virtual"
    total = 0.0
    count = 0
    closed_count = 0
    open_count = 0
    
    # [V20260105_1219] Added buy/sell breakdown
    buy_total = 0.0
    buy_count = 0
    sell_total = 0.0
    sell_count = 0
    
    if not path.exists():
        print(f"Directory not found: {path}")
        return

    for f in path.glob("*.json"):
        try:
            with open(f, 'r') as h:
                data = json.load(h)
                pnl = float(data.get('net_return', 0.0))
                direction = (data.get('direction') or "").upper()
                
                total += pnl
                count += 1
                
                if "BUY" in direction or "LONG" in direction:
                    buy_total += pnl
                    buy_count += 1
                elif "SELL" in direction or "SHORT" in direction:
                    sell_total += pnl
                    sell_count += 1
                    
                if data.get('status') == 'CLOSED':
                    closed_count += 1
                else:
                    open_count += 1
        except Exception as e:
            pass
            
    print(f"Summary for {path.name}:")
    print(f"Total Net Return: ${total:.2f}")
    print(f"Total Files Processed: {count}")
    print(f"  - Buy/Long:  ${buy_total:.2f} ({buy_count} trades)")
    print(f"  - Sell/Short: ${sell_total:.2f} ({sell_count} trades)")
    print(f"Closed Trades: {closed_count}")
    print(f"Open/Running Trades: {open_count}")

if __name__ == "__main__":
    calculate_total_net_return()
