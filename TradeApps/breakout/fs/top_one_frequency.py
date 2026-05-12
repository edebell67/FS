import os
import json
import time
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from paths import BREAKOUT_DATA_ROOT, BREAKOUT_ROOT

# [V20260104_0045] 2026-01-04 00:45 - Update output path for frequency tally
# Tracks the consistency of #1 performers for Buy, Sell, and Combo.

CONFIG_FILE = str(BREAKOUT_ROOT / "config.json")
# FREQUENCY_FILE is now dynamic: json/{run_mode}/{today_str}/_top_one_frequency.json
VERSION = "V20260104_1415"
LOCK_FILE = str(BREAKOUT_DATA_ROOT / "top_one_frequency.lock")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"run_mode": "live"}

def load_frequency(filepath):
    # [V20260104_0420] 2026-01-04 04:20 - Highly robust loading to prevent data loss
    template = {"last_updated": None, "buy": [], "sell": [], "combo": []}
    if not os.path.exists(filepath):
        return template
    try:
        with open(filepath, "r") as f:
            content = f.read().strip()
            if not content:
                print(f"[{datetime.utcnow()}] [WARN] Frequency file is empty: {filepath}")
                return template
            data = json.loads(content)
            # Ensure all required keys exist
            for key in ["buy", "sell", "combo"]:
                if key not in data or not isinstance(data[key], list):
                    data[key] = []
            return data
    except Exception as e:
        print(f"[{datetime.utcnow()}] [ERROR] Failed to load frequency data from {filepath}: {e}")
        return template

def save_frequency(filepath, data):
    # [V20260104_1415] Atomic write: save to temp then rename
    data["last_updated"] = datetime.utcnow().isoformat()
    temp_path = str(filepath) + ".tmp"
    try:
        with open(temp_path, "w") as f:
            json.dump(data, f, indent=4)
        # Atomic replace
        if os.path.exists(temp_path):
            os.replace(temp_path, filepath)
    except Exception as e:
        print(f"[{datetime.utcnow()}] [ERROR] Atomic save failed: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)

def update_counts(category_list, product, strategy, current_time):
    # Find existing entry or create new one
    for entry in category_list:
        if entry["product"] == product and entry["strategy"] == strategy:
            entry["#1 count"] += 1
            entry["most recent top time"] = current_time
            return
    
    category_list.append({
        "product": product,
        "strategy": strategy,
        "#1 count": 1,
        "most recent top time": current_time
    })

def run_frequency_update(run_mode):
    # config = load_config()
    # run_mode = config.get("run_mode", "live").lower()
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # [V20260104_0335] Use absolute path for output and source data
    project_root = BREAKOUT_DATA_ROOT
    output_dir = project_root / "json" / run_mode / today_str
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    
    freq_filepath = output_dir / "_top_one_frequency.json"
    
    # Process breakout trades from the daily directory
    base_dir = output_dir
    # Note: Using mode-specific directories ensures we read Sim trades when in Sim mode
    # print(f"[{datetime.utcnow()}] [DEBUG] Checking for trades in: {base_dir}")
    if not base_dir.exists():
        # print(f"[{datetime.utcnow()}] [WARN] Directory not found: {base_dir}")
        return

    # Aggregate performance
    # stats[strategy][product][direction] = pnl
    stats = defaultdict(lambda: defaultdict(lambda: {"buy": 0.0, "sell": 0.0}))
    
    # Search for breakout trade files (matching top_one_generator source)
    files = list(base_dir.glob("breakout_*.json"))
    # print(f"[{datetime.utcnow()}] [DEBUG] Found {len(files)} virtual trade files to process.")
    
    for i, json_file in enumerate(files):
        # if (i + 1) % 100 == 0:
        #     print(f"[{datetime.utcnow()}] [DEBUG] Processed {i + 1}/{len(files)} files...")
        try:
            with open(json_file, "r") as f:
                data = json.load(f)
            
            if data.get("status") != "CLOSED":
                continue
                
            strategy = data.get("source_strategy")
            product = data.get("product", "UNKNOWN").upper()
            
            # [V20260104_0420] Aggressive fallback: ignore "UNKNOWN" strings and derive from filename
            if not strategy or strategy == "UNKNOWN" or strategy == "unknown_strategy":
                # [V20260104_0350] Hardened strategy extraction from filename
                filename = json_file.name
                # Try common splitters like _AUD_ or _NZD_
                splitter = f'_{product}_'
                if splitter in filename:
                    strategy = filename.split(splitter)[0]
                elif f'_{product.lower()}_' in filename:
                    strategy = filename.split(f'_{product.lower()}_')[0]
                else:
                    # Final fallback: take everything before the product string if found
                    import re
                    match = re.search(f'^(.*)_{product}', filename, re.IGNORECASE)
                    if match:
                        strategy = match.group(1)
                    else:
                        strategy = "UNKNOWN"
            
            direction = (data.get("direction") or "").upper()
            pnl = float(data.get("net_return", 0.0))
            
            dir_key = "buy" if "LONG" in direction else "sell"
            stats[strategy][product][dir_key] += pnl
        except Exception as e:
            continue

    # print(f"[{datetime.utcnow()}] [DEBUG] Aggregation complete. Found stats for {len(stats)} strategies.")
    if not stats:
        # print(f"[{datetime.utcnow()}] [INFO] No closed virtual trades found for today.")
        return

    # Find leaders
    # print(f"[{datetime.utcnow()}] [DEBUG] Finding leaders...")
    buy_leader = {"pnl": -999999, "prod": None, "strat": None}
    sell_leader = {"pnl": -999999, "prod": None, "strat": None}
    combo_leader = {"pnl": -999999, "prod": None, "strat": None}

    for strategy, products in stats.items():
        for product, dirs in products.items():
            b_pnl = dirs["buy"]
            s_pnl = dirs["sell"]
            c_pnl = b_pnl + s_pnl
            
            if b_pnl > buy_leader["pnl"]:
                buy_leader = {"pnl": b_pnl, "prod": product, "strat": strategy}
            if s_pnl > sell_leader["pnl"]:
                sell_leader = {"pnl": s_pnl, "prod": product, "strat": strategy}
            if c_pnl > combo_leader["pnl"]:
                combo_leader = {"pnl": c_pnl, "prod": product, "strat": strategy}

    # Update Persistence (Additive)
    freq_data = load_frequency(freq_filepath)
    now_iso = datetime.utcnow().isoformat()
    
    # [V20260104_0421] STRICT: Do not output any records where strategy is UNKNOWN
    def is_valid(strat):
        return strat and strat.upper() not in ["UNKNOWN", "UNKNOWN_STRATEGY", "NONE", ""]

    if buy_leader["prod"] and is_valid(buy_leader["strat"]):
        update_counts(freq_data["buy"], buy_leader["prod"], buy_leader["strat"], now_iso)
    if sell_leader["prod"] and is_valid(sell_leader["strat"]):
        update_counts(freq_data["sell"], sell_leader["prod"], sell_leader["strat"], now_iso)
    if combo_leader["prod"] and is_valid(combo_leader["strat"]):
        update_counts(freq_data["combo"], combo_leader["prod"], combo_leader["strat"], now_iso)

    # Final cleanup of the freq_data to ensure no UNKNOWNs leaked in from manual edits or old code
    for key in ["buy", "sell", "combo"]:
        freq_data[key] = [item for item in freq_data[key] if is_valid(item.get("strategy"))]

    save_frequency(freq_filepath, freq_data)
    # print(f"[{datetime.utcnow()}] [SUCCESS] Frequency tally updated at {freq_filepath}. Buy: {buy_leader['prod']}, Sell: {sell_leader['prod']}, Combo: {combo_leader['prod']}")

def main():
    print(f"[{datetime.utcnow()}] [START] top_one_frequency.py {VERSION} initialized.")
    
    # [V20260104_0420] Strict singleton check via lock file to prevent overwriting
    if os.path.exists(LOCK_FILE):
        print(f"[{datetime.utcnow()}] [TERMINATE] Lock file exists at {LOCK_FILE}. Another instance is running. Exiting.")
        return

    try:
        # Create lock file with current PID
        with open(LOCK_FILE, "w") as f:
            f.write(str(os.getpid()))
        
        while True:
            try:
                # [V20260131_0435] Process both modes
                for mode in ['live', 'sim']:
                    run_frequency_update(mode)
            except Exception as e:
                print(f"[{datetime.utcnow()}] [ERROR] in main loop: {e}")
            
            time.sleep(5) # [V20260131_0435] Increased frequency
    finally:
        # Cleanup lock on exit
        if os.path.exists(LOCK_FILE):
            # Verify it's OUR lock file (PID matches) before removing
            try:
                with open(LOCK_FILE, "r") as f:
                    pid = f.read().strip()
                if pid == str(os.getpid()):
                    os.remove(LOCK_FILE)
            except Exception:
                pass

if __name__ == "__main__":
    main()
