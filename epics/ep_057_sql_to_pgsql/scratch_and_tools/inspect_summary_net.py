import json

file_path = r"X:\EDS\TradeApps\breakout\fs\json\live\forex\2026-03-29\_summary_net.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Type of root object:", type(data))
if isinstance(data, dict):
    print("Keys in root object:", list(data.keys())[:20])
    print(f"Total keys: {len(data.keys())}")
elif isinstance(data, list):
    print(f"Total items in list: {len(data)}")
    if len(data) > 0:
        print("Sample item keys:", list(data[0].keys()) if isinstance(data[0], dict) else type(data[0]))
        print("Sample item 0:", json.dumps(data[0], indent=2)[:500])

