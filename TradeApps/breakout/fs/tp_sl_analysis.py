import json
import re
from pathlib import Path
from collections import defaultdict
from paths import BREAKOUT_JSON_ROOT # [V20260510_1945]

# [V20260510_1945] Use centralized path resolution
root = BREAKOUT_JSON_ROOT / "live" / "forex"
tp_sl_stats = defaultdict(lambda: {"picks": 0, "net_change": 0, "wins": 0, "losses": 0, "flat": 0})

for date_dir in root.iterdir():
    if not date_dir.is_dir() or len(date_dir.name) != 10:
        continue

    backfilled_path = date_dir / "_top10_history_backfilled.json"
    if not backfilled_path.exists():
        continue

    try:
        data = json.loads(backfilled_path.read_text())
        if "history" not in data:
            continue

        picked_strategies = {}
        # Find first pick time
        for snap in data["history"]:
            for item in snap.get("top10", []):
                key = f"{item['strategy']}|{item['product']}"
                if item.get("pick_now") and key not in picked_strategies:
                    picked_strategies[key] = {
                        "strategy": item['strategy'],
                        "pick_net": item.get('net', 0)
                    }

        # Find end net
        for key in picked_strategies:
            strat, prod = key.split("|")
            end_net = picked_strategies[key]["pick_net"] # default if never seen again
            # find last appearance
            for snap in reversed(data["history"]):
                found = False
                for item in snap.get("top10", []):
                    if item['strategy'] == strat and item['product'] == prod:
                        end_net = item.get('net', 0)
                        found = True
                        break
                if found:
                    break

            # Record it
            strat_name = picked_strategies[key]["strategy"]
            match = re.search(r'(tp\d+\.\d+_sl\d+\.\d+)', strat_name)
            if match:
                param = match.group(1)
                change = end_net - picked_strategies[key]["pick_net"]

                tp_sl_stats[param]["picks"] += 1
                tp_sl_stats[param]["net_change"] += change

                if change > 0:
                    tp_sl_stats[param]["wins"] += 1
                elif change < 0:
                    tp_sl_stats[param]["losses"] += 1
                else:
                    tp_sl_stats[param]["flat"] += 1
    except Exception as e:
        print(f"Error reading {date_dir.name}: {e}")

print(f"{'Parameter':<18} | {'Picks':<5} | {'Tot Net':<8} | {'Avg PP':<7} | {'W/L/F':<10} | {'Win Rate'}")
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
    print(f"{param:<18} | {picks:<5} | {net:<8.1f} | {avg:<7.1f} | {wlf:<10} | {win_rate:.1f}%")
