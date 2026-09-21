import json

with open(r'C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\scratch\top10_by_date_equity_data.json', 'r') as f:
    d = json.load(f)

for dt, models in d.items():
    print(f"=== {dt} ===")
    for m in models:
        print(f"#{m['rank']} {m['model']} net={m['cum_net']} win={m['win_rate']}% trades={m['trades']}")
