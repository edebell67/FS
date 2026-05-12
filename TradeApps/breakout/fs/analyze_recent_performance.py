import json
from collections import defaultdict
import math
from paths import BREAKOUT_JSON_ROOT

def analyze():
    dates = ["2026-02-09", "2026-02-10"]
    base_path = BREAKOUT_JSON_ROOT / "live"
    
    aggregation = defaultdict(lambda: {"net_return": 0, "count": 0, "wins": 0})
    
    for date in dates:
        summary_path = base_path / date / "_trades_summary.json"
        if not summary_path.exists():
            print(f"Skipping {date}, file not found.")
            continue
            
        try:
            with open(summary_path, 'r') as f:
                data = json.load(f)
            
            trades = data.get('trades', [])
            for t in trades:
                # We only want CLOSED trades for return calculations
                if t.get('status') != 'CLOSED':
                    continue
                    
                app = t.get('app_name', 'unknown')
                params = t.get('strategy', '')
                product = t.get('product', 'unknown')
                
                # Treat empty strategy as "no-params"
                param_str = params if params else "default"
                
                key = (app, param_str, product)
                
                net = t.get('net_return', 0)
                aggregation[key]["net_return"] += net
                aggregation[key]["count"] += 1
                if net > 0:
                    aggregation[key]["wins"] += 1
        except Exception as e:
            print(f"Error processing {date}: {e}")

    results = []
    for (app, params, product), stats in aggregation.items():
        count = stats["count"]
        net = stats["net_return"]
        win_rate = (stats["wins"] / count * 100) if count > 0 else 0
        
        # Scoring: (Net Return) * log10(Frequency + 1)
        # This rewards both high returns and high activity. 
        # Using log to dampen the effect of extreme frequency.
        score = net * math.log10(count + 1) if net > 0 else net
        
        results.append({
            "app": app,
            "params": params,
            "product": product,
            "net_return": round(net, 2),
            "trade_count": count,
            "win_rate": round(win_rate, 1),
            "score": round(score, 2)
        })

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    
    print(f"{'Strategy':<30} | {'Product':<8} | {'Params':<25} | {'Trades':<6} | {'Net Return':<12} | {'Score'}")
    print("-" * 100)
    for r in results[:20]:
        print(f"{r['app']:<30} | {r['product']:<8} | {r['params']:<25} | {r['trade_count']:<6} | {r['net_return']:<12.2f} | {r['score']}")

if __name__ == "__main__":
    analyze()
