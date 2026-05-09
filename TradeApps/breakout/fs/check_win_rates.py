import json
from pathlib import Path
from json_layout import configured_product_types, load_layout_config, resolve_day_dir

def get_top_win_rates():
    base_dir = Path(__file__).parent
    json_root = base_dir / "json"
    config = load_layout_config(base_dir / "config.json")
    data = None
    for product_type in configured_product_types(config):
        path = resolve_day_dir(json_root, "live", "2026-02-05", product_type) / "_summary_net.json"
        if not path.exists():
            continue
        with open(path, 'r') as f:
            candidate = json.load(f)
        if data is None:
            data = {'strategies': {}}
        for strat_name, products in candidate.get('strategies', {}).items():
            data['strategies'].setdefault(strat_name, {}).update(products)

    if data is None:
        print("Summary file not found.")
        return

    results = []
    strategies = data.get('strategies', {})
    for strat_name, products in strategies.items():
        for prod_name, points in products.items():
            if not points:
                continue
            
            # Get the latest point (state)
            # Find the last point that isn't 'open: true' if we want finished trades, 
            # but usually the summary points are cumulative.
            # Let's look for the point with the highest trade count to be sure.
            latest = points[-1]
            
            b_c = latest.get('b_c', 0)
            s_c = latest.get('s_c', 0)
            b_p = latest.get('buyPercent', 0)
            s_p = latest.get('sellPercent', 0)
            net = latest.get('net', 0)

            total_trades = b_c + s_c
            if total_trades < 5: # Filter for at least some statistical significance
                continue

            avg_win_rate = (b_p * b_c + s_p * s_c) / total_trades if total_trades > 0 else 0
            
            results.append({
                'id': f"{strat_name} | {prod_name}",
                'win_rate': avg_win_rate,
                'trades': total_trades,
                'net': net,
                'buy_wr': b_p,
                'sell_wr': s_p
            })

    # Sort by Win Rate
    results.sort(key=lambda x: x['win_rate'], reverse=True)

    for r in results[:15]:
        print(f"WR:{r['win_rate']:>3.0f}% Trades:{r['trades']:>3} Net:${r['net']:>7.2f} {r['id']}")

if __name__ == "__main__":
    get_top_win_rates()
