"""
Multi-Date BUY vs SELL Pattern Analysis
Analyzes historical trading data to identify consistent patterns
Created: 2026-02-09 16:48
"""
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from json_layout import configured_product_types, load_layout_config, resolve_day_dir
from paths import BREAKOUT_JSON_ROOT

# Dates to analyze
dates = [
    '2026-02-09',
    '2026-02-06',
    '2026-02-05',
    '2026-02-04',
    '2026-02-03',
    '2026-02-02',
]

base_path = BREAKOUT_JSON_ROOT
config_path = Path(__file__).parent / 'config.json'
cfg = load_layout_config(config_path)

print("=" * 120)
print("MULTI-DATE BUY vs SELL PATTERN ANALYSIS")
print("=" * 120)

# Store results for each date
date_results = {}
all_buy_specialists = defaultdict(list)  # strategy -> list of (date, buy_net, sell_net)
all_products = defaultdict(lambda: {'buy_wins': 0, 'sell_wins': 0, 'total_buy_net': 0, 'total_sell_net': 0})

for date in dates:
    loaded_any = False
    for product_type in configured_product_types(cfg):
        summary_file = resolve_day_dir(base_path, 'live', date, product_type) / '_summary_net.json'
        if not summary_file.exists():
            continue
        loaded_any = True
        with open(summary_file, 'r') as f:
            data = json.load(f)

        # Analyze strategies
        comparisons = []

        for strategy_name, products in data['strategies'].items():
            for product, trades in products.items():
                if not trades:
                    continue
                
                # Get the latest trade data
                latest = trades[-1]
                
                buy_net = latest.get('buy_net', 0)
                sell_net = latest.get('sell_net', 0)
                buy_count = latest.get('b_c', 0)
                sell_count = latest.get('s_c', 0)
                
                # Only analyze if there are both buy and sell trades
                if buy_count > 0 and sell_count > 0:
                    diff = buy_net - sell_net
                    comparisons.append({
                        'strategy': strategy_name,
                        'product': product,
                        'buy_net': buy_net,
                        'sell_net': sell_net,
                        'diff': diff
                    })
                    
                    # Track buy specialists (strategies that consistently favor BUY)
                    if buy_net > 100 and sell_net < 0:
                        key = f"{strategy_name}_{product}"
                        all_buy_specialists[key].append((date, buy_net, sell_net, diff))
                    
                    # Track product performance
                    if diff > 0:
                        all_products[product]['buy_wins'] += 1
                        all_products[product]['total_buy_net'] += buy_net
                    else:
                        all_products[product]['sell_wins'] += 1
                        all_products[product]['total_sell_net'] += sell_net

        existing = date_results.get(date)
        if existing is None:
            date_results[date] = {'comparisons': []}
        date_results[date]['comparisons'].extend(comparisons)

    if not loaded_any:
        print(f"\nSkipping {date} - file not found")
        continue

    comparisons = date_results[date]['comparisons']
    # Calculate statistics for this date
    buy_favored = [c for c in comparisons if c['diff'] > 0]
    sell_favored = [c for c in comparisons if c['diff'] < 0]
    
    avg_buy_net = sum(c['buy_net'] for c in comparisons) / len(comparisons) if comparisons else 0
    avg_sell_net = sum(c['sell_net'] for c in comparisons) / len(comparisons) if comparisons else 0
    
    date_results[date] = {
        'total_strategies': len(comparisons),
        'buy_favored': len(buy_favored),
        'sell_favored': len(sell_favored),
        'buy_favored_pct': len(buy_favored) / len(comparisons) * 100 if comparisons else 0,
        'avg_buy_net': avg_buy_net,
        'avg_sell_net': avg_sell_net,
        'best_buy': max(comparisons, key=lambda x: x['buy_net']) if comparisons else None,
        'best_diff': max(comparisons, key=lambda x: x['diff']) if comparisons else None
    }

# Print daily summary
print("\n" + "=" * 120)
print("DAILY PERFORMANCE SUMMARY")
print("=" * 120)
print(f"{'Date':<12} {'Strategies':<12} {'BUY Favored':<15} {'%':<8} {'Avg BUY Net':<15} {'Avg SELL Net':<15}")
print("-" * 120)

for date in dates:
    if date not in date_results:
        continue
    r = date_results[date]
    print(f"{date:<12} {r['total_strategies']:<12} {r['buy_favored']:<15} "
          f"{r['buy_favored_pct']:<7.1f}% ${r['avg_buy_net']:<14.2f} ${r['avg_sell_net']:<14.2f}")

# Find consistent BUY specialists (appear in multiple dates)
print("\n" + "=" * 120)
print("CONSISTENT BUY SPECIALISTS (Appear in 3+ dates)")
print("=" * 120)

consistent_specialists = {k: v for k, v in all_buy_specialists.items() if len(v) >= 3}
consistent_specialists = dict(sorted(consistent_specialists.items(), key=lambda x: len(x[1]), reverse=True))

print(f"{'Strategy_Product':<60} {'Dates':<8} {'Avg Buy':<12} {'Avg Sell':<12} {'Avg Diff':<12}")
print("-" * 120)

for key, occurrences in list(consistent_specialists.items())[:20]:
    avg_buy = sum(o[1] for o in occurrences) / len(occurrences)
    avg_sell = sum(o[2] for o in occurrences) / len(occurrences)
    avg_diff = sum(o[3] for o in occurrences) / len(occurrences)
    print(f"{key:<60} {len(occurrences):<8} ${avg_buy:<11.2f} ${avg_sell:<11.2f} ${avg_diff:<11.2f}")

# Product consistency analysis
print("\n" + "=" * 120)
print("PRODUCT PERFORMANCE CONSISTENCY")
print("=" * 120)

sorted_products = sorted(all_products.items(), 
                        key=lambda x: x[1]['buy_wins'] - x[1]['sell_wins'], 
                        reverse=True)

print(f"{'Product':<15} {'BUY Wins':<12} {'SELL Wins':<12} {'Win Diff':<12} {'Avg Buy Net':<15}")
print("-" * 120)

for product, stats in sorted_products[:20]:
    win_diff = stats['buy_wins'] - stats['sell_wins']
    avg_buy = stats['total_buy_net'] / stats['buy_wins'] if stats['buy_wins'] > 0 else 0
    print(f"{product:<15} {stats['buy_wins']:<12} {stats['sell_wins']:<12} "
          f"{win_diff:<12} ${avg_buy:<14.2f}")

# Find best overall performers
print("\n" + "=" * 120)
print("BEST OVERALL PERFORMERS (Highest average difference across all dates)")
print("=" * 120)

# Calculate average performance for each strategy-product combo
avg_performance = {}
for key, occurrences in all_buy_specialists.items():
    avg_diff = sum(o[3] for o in occurrences) / len(occurrences)
    avg_performance[key] = {
        'dates': len(occurrences),
        'avg_diff': avg_diff,
        'avg_buy': sum(o[1] for o in occurrences) / len(occurrences),
        'avg_sell': sum(o[2] for o in occurrences) / len(occurrences)
    }

sorted_performers = sorted(avg_performance.items(), key=lambda x: x[1]['avg_diff'], reverse=True)

print(f"{'Strategy_Product':<60} {'Dates':<8} {'Avg Diff':<12} {'Avg Buy':<12} {'Avg Sell':<12}")
print("-" * 120)

for key, perf in sorted_performers[:20]:
    print(f"{key:<60} {perf['dates']:<8} ${perf['avg_diff']:<11.2f} "
          f"${perf['avg_buy']:<11.2f} ${perf['avg_sell']:<11.2f}")

print("\n" + "=" * 120)
print("KEY INSIGHTS")
print("=" * 120)

# Calculate overall bias trend
total_buy_favored = sum(r['buy_favored'] for r in date_results.values())
total_strategies = sum(r['total_strategies'] for r in date_results.values())
overall_buy_pct = total_buy_favored / total_strategies * 100 if total_strategies > 0 else 0

print(f"\n1. OVERALL BIAS TREND:")
print(f"   Across all {len(dates)} dates analyzed:")
print(f"   - BUY favored in {overall_buy_pct:.1f}% of strategy-product combinations")
print(f"   - Total combinations analyzed: {total_strategies}")

print(f"\n2. MOST CONSISTENT BUY PRODUCTS:")
top_products = sorted_products[:5]
for product, stats in top_products:
    total_appearances = stats['buy_wins'] + stats['sell_wins']
    buy_consistency = stats['buy_wins'] / total_appearances * 100 if total_appearances > 0 else 0
    print(f"   - {product}: {buy_consistency:.1f}% BUY wins ({stats['buy_wins']} BUY / {stats['sell_wins']} SELL)")

print(f"\n3. MOST RELIABLE STRATEGIES:")
print(f"   (Appear in 4+ dates with consistent BUY advantage)")
ultra_consistent = {k: v for k, v in consistent_specialists.items() if len(v) >= 4}
for key, occurrences in list(ultra_consistent.items())[:5]:
    strategy, product = key.rsplit('_', 1)
    avg_diff = sum(o[3] for o in occurrences) / len(occurrences)
    print(f"   - {strategy} on {product}")
    print(f"     Appeared in {len(occurrences)} dates, Avg advantage: ${avg_diff:.2f}")

print("\n" + "=" * 120)
