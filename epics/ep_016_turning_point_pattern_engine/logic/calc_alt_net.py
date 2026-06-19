import json
from pathlib import Path

p = Path(r'C:\Users\edebe\eds\gbp_10m_2_0.json')
# Attempt UTF-16 then UTF-8
try:
    with open(p, 'r', encoding='utf-16') as f:
        data = json.load(f)
except:
    with open(p, 'r', encoding='utf-8') as f:
        data = json.load(f)

trades = data['trades']
alt_net = sum(t['alt_pips'] for t in trades)

print(f"--- Analysis of Spike Killer (10m Bucket) ---")
print(f"Normal Net: {data['total_net']} pips")
print(f"Alt Net:    {alt_net:.2f} pips")
print(f"Trade Count: {len(trades)}")
print(f"Yield:       {alt_net / data['duration_hours']:.2f} PPH")
