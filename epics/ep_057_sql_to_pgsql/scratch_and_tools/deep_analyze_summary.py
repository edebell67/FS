import json

file_path = r"X:\EDS\TradeApps\breakout\fs\json\live\forex\2026-03-29\_summary_net.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Root last_update:", data.get("last_update"))
print("Root session_max_net:", data.get("session_max_net"))

strategies = data.get("strategies", {})
print(f"Total strategy keys: {len(strategies)}")

sample_keys = list(strategies.keys())[:5]
print("\nSample strategy keys:")
for k in sample_keys:
    print(" -", k)

first_strat = strategies[sample_keys[0]]
print("\nFirst strategy structure:")
print(json.dumps(first_strat, indent=2)[:800])

