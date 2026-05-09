"""
Analyze _summary_net.json to identify patterns in profitable BUY strategies
Created: 2026-02-09 15:40
"""
import json
from collections import defaultdict
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
buy_performance = []

for strategy_name, products in data['strategies'].items():
    for product, trades in products.items():
        if not trades:
            continue
        
        # Get the latest trade data
        latest = trades[-1]
        
        buy_net = latest.get('buy_net', 0)
        buy_count = latest.get('b_c', 0)
        buy_percent = latest.get('buyPercent', 0)
        
        # Only analyze if there are buy trades
        if buy_count > 0:
            buy_performance.append({
                'strategy': strategy_name,
                'product': product,
                'buy_net': buy_net,
                'buy_count': buy_count,
                'buy_percent': buy_percent,
                'avg_per_trade': buy_net / buy_count if buy_count > 0 else 0
            })

# Sort by buy_net (most profitable first)
buy_performance.sort(key=lambda x: x['buy_net'], reverse=True)

print("=" * 100)
print("TOP 30 MOST PROFITABLE BUY STRATEGIES (by total buy_net)")
print("=" * 100)
print(f"{'Rank':<6} {'Strategy':<40} {'Product':<12} {'Buy Net':<12} {'Trades':<8} {'Avg/Trade':<12} {'Win%':<8}")
print("-" * 100)

for i, perf in enumerate(buy_performance[:30], 1):
    print(f"{i:<6} {perf['strategy']:<40} {perf['product']:<12} "
          f"${perf['buy_net']:<11.2f} {perf['buy_count']:<8} "
          f"${perf['avg_per_trade']:<11.2f} {perf['buy_percent']:<7.1f}%")

print("\n" + "=" * 100)
print("PATTERN ANALYSIS - What makes BUY strategies profitable?")
print("=" * 100)

# Extract patterns from top performers
top_20 = buy_performance[:20]

# Pattern 1: Strategy name patterns
strategy_patterns = defaultdict(list)
for perf in top_20:
    # Extract key parts of strategy name
    parts = perf['strategy'].split('_')
    if len(parts) >= 2:
        base_strategy = parts[0]  # e.g., "breakout"
        strategy_patterns[base_strategy].append(perf['buy_net'])

print("\n1. STRATEGY TYPE PATTERNS:")
for strategy_type, nets in sorted(strategy_patterns.items(), key=lambda x: sum(x[1]), reverse=True):
    avg_net = sum(nets) / len(nets)
    total_net = sum(nets)
    print(f"   {strategy_type:<20} -> Avg: ${avg_net:>8.2f} | Total: ${total_net:>10.2f} | Count: {len(nets)}")

# Pattern 2: Parameter patterns (TP/SL)
tp_sl_patterns = defaultdict(list)
for perf in top_20:
    # Extract TP and SL from strategy name
    parts = perf['strategy'].split('_')
    tp = None
    sl = None
    for part in parts:
        if part.startswith('tp'):
            tp = part.replace('tp', '')
        elif part.startswith('sl'):
            sl = part.replace('sl', '')
    
    if tp and sl:
        key = f"TP:{tp}/SL:{sl}"
        tp_sl_patterns[key].append(perf['buy_net'])

print("\n2. TP/SL PARAMETER PATTERNS (Top 10):")
for params, nets in sorted(tp_sl_patterns.items(), key=lambda x: sum(x[1]), reverse=True)[:10]:
    avg_net = sum(nets) / len(nets)
    total_net = sum(nets)
    print(f"   {params:<20} -> Avg: ${avg_net:>8.2f} | Total: ${total_net:>10.2f} | Count: {len(nets)}")

# Pattern 3: Product patterns
product_patterns = defaultdict(list)
for perf in top_20:
    product_patterns[perf['product']].append(perf['buy_net'])

print("\n3. PRODUCT PATTERNS:")
for product, nets in sorted(product_patterns.items(), key=lambda x: sum(x[1]), reverse=True):
    avg_net = sum(nets) / len(nets)
    total_net = sum(nets)
    print(f"   {product:<20} -> Avg: ${avg_net:>8.2f} | Total: ${total_net:>10.2f} | Count: {len(nets)}")

# Pattern 4: Win rate patterns
print("\n4. WIN RATE PATTERNS:")
high_winrate = [p for p in top_20 if p['buy_percent'] >= 90]
med_winrate = [p for p in top_20 if 70 <= p['buy_percent'] < 90]
low_winrate = [p for p in top_20 if p['buy_percent'] < 70]

print(f"   High Win Rate (≥90%): {len(high_winrate)} strategies, Avg Net: ${sum(p['buy_net'] for p in high_winrate) / len(high_winrate) if high_winrate else 0:.2f}")
print(f"   Med Win Rate (70-89%): {len(med_winrate)} strategies, Avg Net: ${sum(p['buy_net'] for p in med_winrate) / len(med_winrate) if med_winrate else 0:.2f}")
print(f"   Low Win Rate (<70%): {len(low_winrate)} strategies, Avg Net: ${sum(p['buy_net'] for p in low_winrate) / len(low_winrate) if low_winrate else 0:.2f}")

# Pattern 5: Trade count patterns
print("\n5. TRADE COUNT PATTERNS:")
high_volume = [p for p in top_20 if p['buy_count'] >= 10]
med_volume = [p for p in top_20 if 5 <= p['buy_count'] < 10]
low_volume = [p for p in top_20 if p['buy_count'] < 5]

print(f"   High Volume (≥10 trades): {len(high_volume)} strategies, Avg Net: ${sum(p['buy_net'] for p in high_volume) / len(high_volume) if high_volume else 0:.2f}")
print(f"   Med Volume (5-9 trades): {len(med_volume)} strategies, Avg Net: ${sum(p['buy_net'] for p in med_volume) / len(med_volume) if med_volume else 0:.2f}")
print(f"   Low Volume (<5 trades): {len(low_volume)} strategies, Avg Net: ${sum(p['buy_net'] for p in low_volume) / len(low_volume) if low_volume else 0:.2f}")

print("\n" + "=" * 100)
print("KEY INSIGHTS:")
print("=" * 100)

# Find the best overall pattern
best_strategy = buy_performance[0]
print(f"BEST BUY Strategy: {best_strategy['strategy']} on {best_strategy['product']}")
print(f"   Net: ${best_strategy['buy_net']:.2f} | Trades: {best_strategy['buy_count']} | Win%: {best_strategy['buy_percent']:.1f}%")

# Find strategies with best avg per trade
best_avg = sorted(buy_performance, key=lambda x: x['avg_per_trade'], reverse=True)[0]
print(f"\nBest Avg Per Trade: {best_avg['strategy']} on {best_avg['product']}")
print(f"   Avg: ${best_avg['avg_per_trade']:.2f} | Net: ${best_avg['buy_net']:.2f} | Trades: {best_avg['buy_count']}")

print("\n" + "=" * 100)
