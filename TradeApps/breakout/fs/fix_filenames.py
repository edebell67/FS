import os
from pathlib import Path

base_dir = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\2026-01-29")

if base_dir.exists():
    for f in base_dir.glob("*.json.json"):
        new_name = f.name[:-5]  # Remove trailing .json
        print(f"Renaming {f.name} -> {new_name}")
        try:
            f.rename(f.with_name(new_name))
        except Exception as e:
            print(f"Error: {e}")
else:
    print("Directory not found")

print("Cleanup complete.")
