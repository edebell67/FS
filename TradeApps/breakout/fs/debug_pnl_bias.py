import json
from pathlib import Path
from datetime import datetime, timezone
from json_layout import configured_product_types, load_layout_config, resolve_day_dir

def analyze_pnl():
    base_dir = Path(__file__).parent
    json_root = base_dir / "json"
    config = load_layout_config(base_dir / "config.json")
    path = None
    for product_type in configured_product_types(config):
        candidate = resolve_day_dir(json_root, "live", "2026-02-10", product_type) / "_trades_summary.json"
        if candidate.exists():
            path = candidate
            break
    if path is None or not path.exists():
        print("File not found")
        return

    with open(path, 'r') as f:
        data = json.load(f)

    trades = data['trades']
    
    total_buy_net = 0
    total_sell_net = 0
    buy_count = 0
    sell_count = 0

    for t in trades:
        direction = (t.get('direction') or '').upper()
        net = t.get('net_return', 0)
        if 'LONG' in direction or 'BUY' in direction:
            total_buy_net += net
            buy_count += 1
        elif 'SHORT' in direction or 'SELL' in direction:
            total_sell_net += net
            sell_count += 1

    print(f"Total Buy Net: {total_buy_net:.2f} ({buy_count} trades)")
    print(f"Total Sell Net: {total_sell_net:.2f} ({sell_count} trades)")
    
    if buy_count > 0:
        print(f"Avg Buy Net: {total_buy_net/buy_count:.2f}")
    if sell_count > 0:
        print(f"Avg Sell Net: {total_sell_net/sell_count:.2f}")

    # Recent (last hour)
    now = datetime.now(timezone.utc)
    one_hour_ago = now.timestamp() - 3600
    
    recent_buy_net = 0
    recent_sell_net = 0
    recent_buy_count = 0
    recent_sell_count = 0
    
    for t in trades:
        entry_time = t.get('entry_time')
        if not entry_time: continue
        et_ts = datetime.fromisoformat(entry_time.replace('Z', '')).replace(tzinfo=timezone.utc).timestamp()
        if et_ts < one_hour_ago: continue
        
        direction = (t.get('direction') or '').upper()
        net = t.get('net_return', 0)
        if 'LONG' in direction or 'BUY' in direction:
            recent_buy_net += net
            recent_buy_count += 1
        elif 'SHORT' in direction or 'SELL' in direction:
            recent_sell_net += net
            recent_sell_count += 1

    print(f"\nRecent (1h) Buy Net: {recent_buy_net:.2f} ({recent_buy_count} trades)")
    print(f"Recent (1h) Sell Net: {recent_sell_net:.2f} ({recent_sell_count} trades)")

if __name__ == "__main__":
    analyze_pnl()
