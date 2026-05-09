"""
Enhanced Multi-Date Analysis with Bidirectional Strategies
Analyzes which strategies are profitable in BOTH directions across multiple days
Created: 2026-02-09 17:01
"""
import json
from pathlib import Path
from collections import defaultdict
from json_layout import configured_product_types, load_layout_config, resolve_day_dir

dates = ['2026-02-09', '2026-02-06', '2026-02-05', '2026-02-04', '2026-02-03', '2026-02-02']
BASE_PATH = Path(__file__).parent / 'json'
CONFIG_PATH = Path(__file__).parent / 'config.json'
cfg = load_layout_config(CONFIG_PATH)

print("=" * 120)
print("BIDIRECTIONAL STRATEGY ANALYSIS - Strategies Profitable in BOTH Directions")
print("=" * 120)

# Track bidirectional strategies
bidirectional_strategies = defaultdict(list)  # key -> list of (date, buy_net, sell_net)

for date in dates:
    for product_type in configured_product_types(cfg):
        summary_file = resolve_day_dir(BASE_PATH, 'live', date, product_type) / '_summary_net.json'
        if not summary_file.exists():
            continue
        with open(summary_file, 'r') as f:
            data = json.load(f)
        for strategy_name, products in data['strategies'].items():
            for product, trades in products.items():
                if not trades:
                    continue
                latest = trades[-1]
                buy_net = latest.get('buy_net', 0)
                sell_net = latest.get('sell_net', 0)
                buy_count = latest.get('b_c', 0)
                sell_count = latest.get('s_c', 0)
                if buy_count > 0 and sell_count > 0 and buy_net > 0 and sell_net > 0:
                    key = f"{strategy_name}_{product}"
                    bidirectional_strategies[key].append({
                        'date': date,
                        'buy_net': buy_net,
                        'sell_net': sell_net,
                        'total_net': buy_net + sell_net,
                        'buy_count': buy_count,
                        'sell_count': sell_count
                    })

# Find strategies that are bidirectional on multiple dates
consistent_bidirectional = {k: v for k, v in bidirectional_strategies.items() if len(v) >= 2}
consistent_bidirectional = dict(sorted(consistent_bidirectional.items(), 
                                      key=lambda x: sum(d['total_net'] for d in x[1]), 
                                      reverse=True))

print(f"\nFound {len(consistent_bidirectional)} strategies profitable in BOTH directions on 2+ dates")
print("\n" + "=" * 120)
print("TOP 20 BIDIRECTIONAL STRATEGIES (Profitable in BOTH BUY and SELL)")
print("=" * 120)
print(f"{'Strategy_Product':<60} {'Dates':<8} {'Avg Buy':<12} {'Avg Sell':<12} {'Avg Total':<12}")
print("-" * 120)

for key, occurrences in list(consistent_bidirectional.items())[:20]:
    avg_buy = sum(d['buy_net'] for d in occurrences) / len(occurrences)
    avg_sell = sum(d['sell_net'] for d in occurrences) / len(occurrences)
    avg_total = sum(d['total_net'] for d in occurrences) / len(occurrences)
    print(f"{key:<60} {len(occurrences):<8} ${avg_buy:<11.2f} ${avg_sell:<11.2f} ${avg_total:<11.2f}")

# Show detailed breakdown for top 5
print("\n" + "=" * 120)
print("DETAILED BREAKDOWN - Top 5 Bidirectional Strategies")
print("=" * 120)

for key, occurrences in list(consistent_bidirectional.items())[:5]:
    strategy, product = key.rsplit('_', 1)
    print(f"\n{strategy} on {product}")
    print(f"{'Date':<12} {'Buy Net':<12} {'Sell Net':<12} {'Total Net':<12} {'Buy Trades':<12} {'Sell Trades':<12}")
    print("-" * 80)
    for occ in occurrences:
        print(f"{occ['date']:<12} ${occ['buy_net']:<11.2f} ${occ['sell_net']:<11.2f} "
              f"${occ['total_net']:<11.2f} {occ['buy_count']:<12} {occ['sell_count']:<12}")
    
    avg_buy = sum(d['buy_net'] for d in occurrences) / len(occurrences)
    avg_sell = sum(d['sell_net'] for d in occurrences) / len(occurrences)
    avg_total = sum(d['total_net'] for d in occurrences) / len(occurrences)
    print("-" * 80)
    print(f"{'AVERAGE':<12} ${avg_buy:<11.2f} ${avg_sell:<11.2f} ${avg_total:<11.2f}")

# Check if the same strategies appear on both Feb 6 and Feb 9
print("\n" + "=" * 120)
print("STRATEGIES PROFITABLE IN BOTH DIRECTIONS ON BOTH FEB 6 AND FEB 9")
print("=" * 120)

feb6_bidirectional = set()
feb9_bidirectional = set()

for key, occurrences in bidirectional_strategies.items():
    dates_present = [d['date'] for d in occurrences]
    if '2026-02-06' in dates_present:
        feb6_bidirectional.add(key)
    if '2026-02-09' in dates_present:
        feb9_bidirectional.add(key)

common_strategies = feb6_bidirectional & feb9_bidirectional

print(f"\nStrategies profitable in BOTH directions on Feb 6: {len(feb6_bidirectional)}")
print(f"Strategies profitable in BOTH directions on Feb 9: {len(feb9_bidirectional)}")
print(f"Common to BOTH dates: {len(common_strategies)}")

if common_strategies:
    print(f"\n{'Strategy_Product':<60} {'Feb 6 Total':<15} {'Feb 9 Total':<15}")
    print("-" * 120)
    
    common_data = []
    for key in common_strategies:
        occurrences = bidirectional_strategies[key]
        feb6_data = next((d for d in occurrences if d['date'] == '2026-02-06'), None)
        feb9_data = next((d for d in occurrences if d['date'] == '2026-02-09'), None)
        
        if feb6_data and feb9_data:
            common_data.append({
                'key': key,
                'feb6_total': feb6_data['total_net'],
                'feb9_total': feb9_data['total_net'],
                'avg_total': (feb6_data['total_net'] + feb9_data['total_net']) / 2
            })
    
    common_data.sort(key=lambda x: x['avg_total'], reverse=True)
    
    for item in common_data[:20]:
        print(f"{item['key']:<60} ${item['feb6_total']:<14.2f} ${item['feb9_total']:<14.2f}")

print("\n" + "=" * 120)
print("KEY INSIGHTS")
print("=" * 120)

print(f"\n1. BIDIRECTIONAL CONSISTENCY:")
print(f"   - Only {len(consistent_bidirectional)} strategies are profitable in BOTH directions on 2+ dates")
print(f"   - This represents a small fraction of all strategies tested")
print(f"   - These are the most versatile strategies that can profit regardless of market bias")

print(f"\n2. DATE-SPECIFIC BIDIRECTIONAL PERFORMANCE:")
print(f"   - Feb 6 had {len(feb6_bidirectional)} bidirectional strategies")
print(f"   - Feb 9 had {len(feb9_bidirectional)} bidirectional strategies")
print(f"   - Only {len(common_strategies)} strategies were bidirectional on BOTH dates")
print(f"   - This suggests market conditions significantly affect which strategies work in both directions")

if consistent_bidirectional:
    top_strategy = list(consistent_bidirectional.items())[0]
    top_key = top_strategy[0]
    top_occurrences = top_strategy[1]
    avg_total = sum(d['total_net'] for d in top_occurrences) / len(top_occurrences)
    
    print(f"\n3. MOST RELIABLE BIDIRECTIONAL STRATEGY:")
    print(f"   - {top_key}")
    print(f"   - Appeared on {len(top_occurrences)} dates")
    print(f"   - Average total net: ${avg_total:.2f}")

print("\n" + "=" * 120)
