"""
Compare BUY vs SELL performance for strategies
Created: 2026-02-09 16:00
"""
import json
from pathlib import Path
from json_layout import configured_product_types, load_layout_config, resolve_day_dir

base_dir = Path(__file__).parent
json_root = base_dir / "json"
config = load_layout_config(base_dir / "config.json")
data = {'strategies': {}}

for product_type in configured_product_types(config):
    summary_file = resolve_day_dir(json_root, "live", "2026-02-09", product_type) / "_summary_net.json"
    if not summary_file.exists():
        continue
    with open(summary_file, 'r') as f:
        candidate = json.load(f)
    for strategy_name, products in candidate.get('strategies', {}).items():
        data['strategies'].setdefault(strategy_name, {}).update(products)

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
        buy_percent = latest.get('buyPercent', 0)
        sell_percent = latest.get('sellPercent', 0)
        
        # Only analyze if there are both buy and sell trades
        if buy_count > 0 and sell_count > 0:
            comparisons.append({
                'strategy': strategy_name,
                'product': product,
                'buy_net': buy_net,
                'sell_net': sell_net,
                'buy_count': buy_count,
                'sell_count': sell_count,
                'buy_percent': buy_percent,
                'sell_percent': sell_percent,
                'buy_avg': buy_net / buy_count if buy_count > 0 else 0,
                'sell_avg': sell_net / sell_count if sell_count > 0 else 0,
                'total_net': buy_net + sell_net,
                'buy_vs_sell_diff': buy_net - sell_net
            })

print("=" * 120)
print("BUY vs SELL TRADE PERFORMANCE COMPARISON")
print("=" * 120)
print(f"{'Strategy':<40} {'Product':<12} {'Buy Net':<10} {'Sell Net':<10} {'Diff':<10} {'B Cnt':<6} {'S Cnt':<6} {'B%':<6} {'S%':<6}")
print("-" * 120)

# Sort by buy vs sell difference (strategies where BUY outperforms SELL)
comparisons.sort(key=lambda x: x['buy_vs_sell_diff'], reverse=True)

print("\n>>> TOP 30: STRATEGIES WHERE BUY TRADES OUTPERFORM SELL TRADES <<<\n")
for i, comp in enumerate(comparisons[:30], 1):
    print(f"{comp['strategy']:<40} {comp['product']:<12} "
          f"${comp['buy_net']:<9.2f} ${comp['sell_net']:<9.2f} "
          f"${comp['buy_vs_sell_diff']:<9.2f} "
          f"{comp['buy_count']:<6} {comp['sell_count']:<6} "
          f"{comp['buy_percent']:<5.1f}% {comp['sell_percent']:<5.1f}%")

print("\n" + "=" * 120)
print("\n>>> BOTTOM 30: STRATEGIES WHERE SELL TRADES OUTPERFORM BUY TRADES <<<\n")
print(f"{'Strategy':<40} {'Product':<12} {'Buy Net':<10} {'Sell Net':<10} {'Diff':<10} {'B Cnt':<6} {'S Cnt':<6} {'B%':<6} {'S%':<6}")
print("-" * 120)

for i, comp in enumerate(comparisons[-30:], 1):
    print(f"{comp['strategy']:<40} {comp['product']:<12} "
          f"${comp['buy_net']:<9.2f} ${comp['sell_net']:<9.2f} "
          f"${comp['buy_vs_sell_diff']:<9.2f} "
          f"{comp['buy_count']:<6} {comp['sell_count']:<6} "
          f"{comp['buy_percent']:<5.1f}% {comp['sell_percent']:<5.1f}%")

print("\n" + "=" * 120)
print("STATISTICAL SUMMARY")
print("=" * 120)

# Calculate statistics
buy_favored = [c for c in comparisons if c['buy_vs_sell_diff'] > 0]
sell_favored = [c for c in comparisons if c['buy_vs_sell_diff'] < 0]
neutral = [c for c in comparisons if c['buy_vs_sell_diff'] == 0]

print(f"\nTotal strategies with both BUY and SELL trades: {len(comparisons)}")
print(f"  BUY outperforms SELL: {len(buy_favored)} ({len(buy_favored)/len(comparisons)*100:.1f}%)")
print(f"  SELL outperforms BUY: {len(sell_favored)} ({len(sell_favored)/len(comparisons)*100:.1f}%)")
print(f"  Neutral (equal): {len(neutral)} ({len(neutral)/len(comparisons)*100:.1f}%)")

# Average performance
avg_buy_net = sum(c['buy_net'] for c in comparisons) / len(comparisons)
avg_sell_net = sum(c['sell_net'] for c in comparisons) / len(comparisons)
avg_buy_winrate = sum(c['buy_percent'] for c in comparisons) / len(comparisons)
avg_sell_winrate = sum(c['sell_percent'] for c in comparisons) / len(comparisons)

print(f"\nAverage BUY Net: ${avg_buy_net:.2f}")
print(f"Average SELL Net: ${avg_sell_net:.2f}")
print(f"Average BUY Win Rate: {avg_buy_winrate:.1f}%")
print(f"Average SELL Win Rate: {avg_sell_winrate:.1f}%")

# Best performers
best_buy_performer = max(comparisons, key=lambda x: x['buy_net'])
best_sell_performer = max(comparisons, key=lambda x: x['sell_net'])

print(f"\nBest BUY Performer:")
print(f"  {best_buy_performer['strategy']} on {best_buy_performer['product']}")
print(f"  Buy Net: ${best_buy_performer['buy_net']:.2f} | Sell Net: ${best_buy_performer['sell_net']:.2f}")
print(f"  Difference: ${best_buy_performer['buy_vs_sell_diff']:.2f}")

print(f"\nBest SELL Performer:")
print(f"  {best_sell_performer['strategy']} on {best_sell_performer['product']}")
print(f"  Sell Net: ${best_sell_performer['sell_net']:.2f} | Buy Net: ${best_sell_performer['buy_net']:.2f}")
print(f"  Difference: ${best_sell_performer['buy_vs_sell_diff']:.2f}")

# Most balanced
most_balanced = min(comparisons, key=lambda x: abs(x['buy_vs_sell_diff']))
print(f"\nMost Balanced Strategy:")
print(f"  {most_balanced['strategy']} on {most_balanced['product']}")
print(f"  Buy Net: ${most_balanced['buy_net']:.2f} | Sell Net: ${most_balanced['sell_net']:.2f}")
print(f"  Difference: ${most_balanced['buy_vs_sell_diff']:.2f}")

print("\n" + "=" * 120)
print("KEY INSIGHTS FOR CURRENT BUY BIAS")
print("=" * 120)

# Find strategies that perform well in BUY but poorly in SELL
buy_specialists = [c for c in comparisons if c['buy_net'] > 100 and c['sell_net'] < 0]
print(f"\nBUY Specialists (good in BUY, bad in SELL): {len(buy_specialists)}")
if buy_specialists:
    buy_specialists.sort(key=lambda x: x['buy_vs_sell_diff'], reverse=True)
    print("Top 5 BUY Specialists:")
    for i, comp in enumerate(buy_specialists[:5], 1):
        print(f"  {i}. {comp['strategy']:<40} {comp['product']:<12}")
        print(f"     Buy: ${comp['buy_net']:>7.2f} ({comp['buy_percent']:.1f}%) | Sell: ${comp['sell_net']:>7.2f} ({comp['sell_percent']:.1f}%)")

# Find strategies that are profitable in both directions
both_profitable = [c for c in comparisons if c['buy_net'] > 0 and c['sell_net'] > 0]
print(f"\nProfitable in BOTH directions: {len(both_profitable)}")
if both_profitable:
    both_profitable.sort(key=lambda x: x['total_net'], reverse=True)
    print("Top 5 Bidirectional Strategies:")
    for i, comp in enumerate(both_profitable[:5], 1):
        print(f"  {i}. {comp['strategy']:<40} {comp['product']:<12}")
        print(f"     Buy: ${comp['buy_net']:>7.2f} | Sell: ${comp['sell_net']:>7.2f} | Total: ${comp['total_net']:>7.2f}")

print("\n" + "=" * 120)
