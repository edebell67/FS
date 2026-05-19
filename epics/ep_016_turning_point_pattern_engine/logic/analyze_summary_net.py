import json
import sys
from datetime import datetime
from collections import defaultdict
from pathlib import Path

def analyze_summary_net(file_path):
    """
    Analyze summary_net.json:
    - Take snapshot every 15 min
    - Count profitable buy and sell strategies in each 15min block
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Collect all snapshots with their timestamps
    all_snapshots = []

    strategies = data.get('strategies', {})
    for strategy_name, products in strategies.items():
        for product_name, snapshots in products.items():
            for snap in snapshots:
                ts = snap.get('t')
                if ts:
                    all_snapshots.append({
                        'timestamp': ts,
                        'strategy': strategy_name,
                        'product': product_name,
                        'buy_net': snap.get('buy_net', 0),
                        'sell_net': snap.get('sell_net', 0),
                        'b_c': snap.get('b_c', 0),
                        's_c': snap.get('s_c', 0),
                        'net': snap.get('net', 0)
                    })

    # Group by 15-minute blocks
    blocks = defaultdict(lambda: {
        'profitable_buy': 0,
        'profitable_sell': 0,
        'total_buy': 0,
        'total_sell': 0,
        'snapshots': 0
    })

    for snap in all_snapshots:
        try:
            dt = datetime.fromisoformat(snap['timestamp'])
            # Round down to 15-minute block
            minute = (dt.minute // 15) * 15
            block_time = dt.replace(minute=minute, second=0, microsecond=0)
            block_key = block_time.strftime('%Y-%m-%d %H:%M')

            blocks[block_key]['snapshots'] += 1

            # Count profitable buy strategies (buy_net > 0)
            if snap['buy_net'] > 0:
                blocks[block_key]['profitable_buy'] += 1
            if snap['b_c'] > 0:
                blocks[block_key]['total_buy'] += 1

            # Count profitable sell strategies (sell_net > 0)
            if snap['sell_net'] > 0:
                blocks[block_key]['profitable_sell'] += 1
            if snap['s_c'] > 0:
                blocks[block_key]['total_sell'] += 1

        except Exception as e:
            continue

    # Sort and print results
    print("=" * 80)
    print("SUMMARY NET ANALYSIS - 15 Minute Blocks")
    print("=" * 80)
    print(f"{'Time Block':<20} {'Prof Buy':<10} {'Prof Sell':<10} {'Tot Buy':<10} {'Tot Sell':<10} {'Snaps':<8}")
    print("-" * 80)

    total_prof_buy = 0
    total_prof_sell = 0

    for block_key in sorted(blocks.keys()):
        b = blocks[block_key]
        print(f"{block_key:<20} {b['profitable_buy']:<10} {b['profitable_sell']:<10} {b['total_buy']:<10} {b['total_sell']:<10} {b['snapshots']:<8}")
        total_prof_buy += b['profitable_buy']
        total_prof_sell += b['profitable_sell']

    print("-" * 80)
    print(f"{'TOTAL':<20} {total_prof_buy:<10} {total_prof_sell:<10}")
    print("=" * 80)

    # Summary stats
    print(f"\nTotal 15-min blocks: {len(blocks)}")
    print(f"Total snapshots analyzed: {len(all_snapshots)}")
    print(f"Total profitable BUY registrations: {total_prof_buy}")
    print(f"Total profitable SELL registrations: {total_prof_sell}")

    return blocks

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = r"X:\EDS\TradeApps\breakout\fs\json\live\forex\2026-05-14\_summary_net.json"

    analyze_summary_net(file_path)
