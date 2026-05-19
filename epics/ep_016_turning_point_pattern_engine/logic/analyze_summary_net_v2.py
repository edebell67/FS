import json
import sys
from datetime import datetime
from collections import defaultdict

def analyze_summary_net_by_strategy(file_path):
    """
    Analyze summary_net.json by strategy type:
    - breakout, breakout_r, breakout_rev, breakout_r_rev
    - Count profitable buy/sell for each in 15min blocks
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Strategy type mapping
    def get_strategy_type(name):
        name_lower = name.lower()
        if 'breakout_r_rev' in name_lower:
            return 'breakout_r_rev'
        elif 'breakout_rev' in name_lower:
            return 'breakout_rev'
        elif 'breakout_r' in name_lower:
            return 'breakout_r'
        elif 'breakout' in name_lower:
            return 'breakout'
        return 'other'

    # Collect snapshots by block and strategy type
    blocks = defaultdict(lambda: {
        'breakout': {'buy': 0, 'sell': 0},
        'breakout_r': {'buy': 0, 'sell': 0},
        'breakout_rev': {'buy': 0, 'sell': 0},
        'breakout_r_rev': {'buy': 0, 'sell': 0}
    })

    strategies = data.get('strategies', {})
    for strategy_name, products in strategies.items():
        strat_type = get_strategy_type(strategy_name)
        if strat_type == 'other':
            continue

        for product_name, snapshots in products.items():
            for snap in snapshots:
                ts = snap.get('t')
                if not ts:
                    continue

                try:
                    dt = datetime.fromisoformat(ts)
                    # Filter: start from 00:15 on 2026-05-14
                    if dt < datetime(2026, 5, 14, 0, 15):
                        continue

                    minute = (dt.minute // 15) * 15
                    block_time = dt.replace(minute=minute, second=0, microsecond=0)
                    block_key = block_time.strftime('%H:%M')

                    # Count profitable buy/sell
                    if snap.get('buy_net', 0) > 0:
                        blocks[block_key][strat_type]['buy'] += 1
                    if snap.get('sell_net', 0) > 0:
                        blocks[block_key][strat_type]['sell'] += 1

                except Exception:
                    continue

    # Print results
    print("=" * 100)
    print("STRATEGY BREAKDOWN - Profitable Buy/Sell by 15min Block (from 00:15)")
    print("=" * 100)
    print(f"{'Time':<8} | {'BREAKOUT':<16} | {'BREAKOUT_R':<16} | {'BREAKOUT_REV':<16} | {'BREAKOUT_R_REV':<16}")
    print(f"{'':8} | {'Buy':>7} {'Sell':>7} | {'Buy':>7} {'Sell':>7} | {'Buy':>7} {'Sell':>7} | {'Buy':>7} {'Sell':>7}")
    print("-" * 100)

    totals = {
        'breakout': {'buy': 0, 'sell': 0},
        'breakout_r': {'buy': 0, 'sell': 0},
        'breakout_rev': {'buy': 0, 'sell': 0},
        'breakout_r_rev': {'buy': 0, 'sell': 0}
    }

    for block_key in sorted(blocks.keys()):
        b = blocks[block_key]
        print(f"{block_key:<8} | {b['breakout']['buy']:>7} {b['breakout']['sell']:>7} | "
              f"{b['breakout_r']['buy']:>7} {b['breakout_r']['sell']:>7} | "
              f"{b['breakout_rev']['buy']:>7} {b['breakout_rev']['sell']:>7} | "
              f"{b['breakout_r_rev']['buy']:>7} {b['breakout_r_rev']['sell']:>7}")

        for st in totals:
            totals[st]['buy'] += b[st]['buy']
            totals[st]['sell'] += b[st]['sell']

    print("-" * 100)
    print(f"{'TOTAL':<8} | {totals['breakout']['buy']:>7} {totals['breakout']['sell']:>7} | "
          f"{totals['breakout_r']['buy']:>7} {totals['breakout_r']['sell']:>7} | "
          f"{totals['breakout_rev']['buy']:>7} {totals['breakout_rev']['sell']:>7} | "
          f"{totals['breakout_r_rev']['buy']:>7} {totals['breakout_r_rev']['sell']:>7}")
    print("=" * 100)

    # Summary
    print("\nSUMMARY:")
    for st in ['breakout', 'breakout_r', 'breakout_rev', 'breakout_r_rev']:
        total = totals[st]['buy'] + totals[st]['sell']
        print(f"  {st.upper():<15}: Buy={totals[st]['buy']:>5}, Sell={totals[st]['sell']:>5}, Total={total:>5}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = r"X:\EDS\TradeApps\breakout\fs\json\live\forex\2026-05-14\_summary_net.json"

    analyze_summary_net_by_strategy(file_path)
