import json
import re
from pathlib import Path
from collections import defaultdict

root = Path("json/live/forex")
tp_sl_stats = defaultdict(lambda: {"picks": 0, "net_change": 0, "wins": 0, "losses": 0, "flat": 0})

for date_dir in root.iterdir():
    if not date_dir.is_dir() or len(date_dir.name) != 10:
        continue
    
    backfilled_path = date_dir / "_top10_history_backfilled.json"
    if not backfilled_path.exists():
        continue
        
    try:
        data = json.loads(backfilled_path.read_text())
        
        # Structure seems to be a list of strategies or we need to find the "picks"
        # Since I don't know the exact format, let's see if we can find 'pick_now' == True
        # Often it's stored in a list of evaluated strategies
        if "evaluations" in data:
            evals = data["evaluations"]
        elif isinstance(data, list):
            evals = data
        else:
            continue
            
        for s in evals:
            if s.get("pick_now") == True:
                strat_name = s.get("strategy", "")
                
                # Extract tp and sl using regex
                match = re.search(r'(tp\d+\.\d+_sl\d+\.\d+)', strat_name)
                if match:
                    param = match.group(1)
                    tp_sl_stats[param]["picks"] += 1
                    
                    change = s.get("net_change", 0) # guessing field name
                    # If net_change is not directly there, we might need actual net at pick vs end net
                    # But if backfilled file stores the outcome:
                    if "change" in s:
                        change = s["change"]
                    elif "end_net" in s and "pick_net" in s:
                        change = s["end_net"] - s["pick_net"]
                        
                    tp_sl_stats[param]["net_change"] += change
                    
                    if change > 0:
                        tp_sl_stats[param]["wins"] += 1
                    elif change < 0:
                        tp_sl_stats[param]["losses"] += 1
                    else:
                        tp_sl_stats[param]["flat"] += 1
    except Exception as e:
        print(f"Error reading {date_dir.name}: {e}")

print(f"{'Parameter':<20} | {'Picks':<6} | {'Total Net':<10} | {'Avg PP':<8} | {'W/L/F':<12} | {'Win Rate'}")
print("-" * 75)

for param, stats in sorted(tp_sl_stats.items(), key=lambda x: x[1]["net_change"], reverse=True):
    picks = stats["picks"]
    if picks == 0: continue
    net = stats["net_change"]
    avg = net / picks
    w = stats["wins"]
    l = stats["losses"]
    f = stats["flat"]
    win_rate = (w / picks) * 100
    wlf = f"{w}/{l}/{f}"
    print(f"{param:<20} | {picks:<6} | {net:<10.1f} | {avg:<8.1f} | {wlf:<12} | {win_rate:.1f}%")

