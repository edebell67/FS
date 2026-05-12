import json
import os
import glob
from pathlib import Path
from paths import BREAKOUT_JSON_ROOT # [V20260510_1945]

# [V20260510_1945] Use centralized path resolution
path_pattern = str(BREAKOUT_JSON_ROOT / "live" / "forex" / "2026-03-*" / "_top10_history_backfilled.json")
files = glob.glob(path_pattern)
if not files:
    print(f"No files found for pattern: {path_pattern}")
    exit()

first_file = files[0]
with open(first_file, "r") as f:
    data = json.load(f)

if "evaluations" in data:
    print("Found evaluations array. First entry keys:", data["evaluations"][0].keys() if data["evaluations"] else "empty")
elif isinstance(data, list) and data:
    print("Found list. First entry keys:", data[0].keys())
else:
    print("Keys in top level:", data.keys() if isinstance(data, dict) else "unknown dict type")
    if "history" in data:
        print("Keys in history[0]:", data["history"][0].keys())
        if "top10" in data["history"][0]:
            print("Keys in history[0]['top10'][0]:", data["history"][0]["top10"][0].keys())
