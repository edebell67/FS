"""
Automated Strategy Selector Agent
[V20260206_1000]
Selects the top-performing strategy from today's _top20.json and promotes it to grid_live.json.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from json_layout import configured_product_types, load_layout_config, resolve_day_dir
from paths import BREAKOUT_DATA_FS_ROOT, BREAKOUT_FS_ROOT, BREAKOUT_JSON_ROOT

# --- Configuration ---
BASE_DIR = BREAKOUT_DATA_FS_ROOT
JSON_DIR = BREAKOUT_JSON_ROOT
GRID_LIVE_FILE = BASE_DIR / "grid_live.json"
HISTORY_FILE = BREAKOUT_JSON_ROOT / "grid_live_history.json"
CONFIG_FILE = BREAKOUT_FS_ROOT / "config.json"

def get_today_str():
    return datetime.now().strftime('%Y-%m-%d')

def load_json(path, default=None):
    if not path.exists():
        return default
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load {path.name}: {e}")
        return default

def save_json(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save {path.name}: {e}")
        return False

def select_top_strategy():
    today = get_today_str()
    cfg = load_layout_config(CONFIG_FILE)
    top20_path = None
    for product_type in configured_product_types(cfg):
        candidate = resolve_day_dir(JSON_DIR, "live", today, product_type) / "_top20.json"
        if candidate.exists():
            top20_path = candidate
            break
    if top20_path is None:
        print(f"[INFO] No top20 data found for {today}")
        return None
    
    data = load_json(top20_path)
    if not data or "top20" not in data or not data["top20"]:
        print(f"[INFO] No top20 data found for {today}")
        return None
        
    candidates = []
    for s in data["top20"]:
        # Criteria: Must have at least 3 trades for statistical significance
        if s.get("trade_count", 0) < 3:
            continue
            
        # Must have positive profit
        if s.get("total_net", 0) <= 0:
            continue
            
        # Calculate Average Win Rate (Profitability %)
        # buyPercent and sellPercent are already 0-100 values in top20.json
        bp = s.get("buyPercent", 0)
        sp = s.get("sellPercent", 0)
        
        # If one side has no trades, we treat it as 0
        win_rate_avg = (bp + sp) / 2.0
        s["win_rate_avg"] = win_rate_avg
        candidates.append(s)
        
    if not candidates:
        print(f"[INFO] No strategies for {today} met the criteria (trade_count >= 3, total_net > 0).")
        return None
        
    # Sort: Primary = Win Rate (Desc), Secondary = Total Net (Desc)
    candidates.sort(key=lambda x: (x["win_rate_avg"], x["total_net"]), reverse=True)
    
    top_strat = candidates[0]
    print(f"[INFO] Selected strategy based on Win Rate: {top_strat['win_rate_avg']}% (Total Net: {top_strat['total_net']})")
    
    return top_strat

def update_grid_live(selected_strat):
    if not selected_strat:
        return False
        
    grid = load_json(GRID_LIVE_FILE, {"live": [], "sim": []})
    
    model = selected_strat["strategy"]
    product = selected_strat["product"]
    source = f"auto_selector_{get_today_str()}"
    
    # Check if already present
    for entry in grid.get("live", []):
        if entry.get("model") == model and entry.get("product") == product:
            print(f"[INFO] Strategy {model} | {product} is already in the grid.")
            return False
            
    # Add new entry (placing it at the top)
    new_entry = {
        "model": model,
        "product": product,
        "metric": "net",
        "activated_at": datetime.now().isoformat()[:19],
        "group": f"{model} | {product}",
        "source": source
    }
    
    grid["live"].insert(0, new_entry)
    
    if save_json(GRID_LIVE_FILE, grid):
        print(f"[SUCCESS] Promoted {model} | {product} to grid_live.json (Total Net: {selected_strat['total_net']})")
        log_history(grid)
        return True
        
    return False

def log_history(grid_snapshot):
    history = load_json(HISTORY_FILE, [])
    history.append({
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "mode": "live",
        "snapshot": grid_snapshot
    })
    
    # Keep last 100 entries
    if len(history) > 100:
        history = history[-100:]
        
    save_json(HISTORY_FILE, history)

def main():
    print(f"[{datetime.now()}] Starting Automated Strategy Selector...")
    top_strat = select_top_strategy()
    if top_strat:
        update_grid_live(top_strat)
    print(f"[{datetime.now()}] Job finished.")

if __name__ == "__main__":
    main()
