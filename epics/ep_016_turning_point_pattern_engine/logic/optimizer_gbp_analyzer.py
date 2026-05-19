import json
import os
import subprocess
from pathlib import Path
import random

DATA_PATH = r"X:\eds\TradeApps\breakout\fs\json\live\forex\2026-05-13\_price_capture.jsonl"
BACKTEST_SCRIPT = r"C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\logic\backtest_gbp_analyzer.py"
LOG_FILE = r"C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\optimization\clean_optimization_log_20260514.txt"

def run_backtest(params):
    cmd = ["python", BACKTEST_SCRIPT, "--data", DATA_PATH]
    for k, v in params.items():
        if v is not None:
            cmd.extend([f"--{k}", str(v)])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except:
        return None

def main():
    best_pph = -999
    best_params = {}
    
    print(f"Starting Clean 100-Cycle Optimization. Logic bug resolved.")
    
    # Ensure directory exists
    Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("Clean Optimization Log - Date: 2026-05-14\n")
        f.write("------------------------------------------------\n")

    for i in range(100):
        params = {
            "conf_high": random.randint(15, 45),
            "conf_med": random.randint(8, 25),
            "conf_low": random.randint(2, 10),
            "price_offset": round(random.uniform(-5.0, 1.0), 2),
            "fixed_tp": random.choice([None, 5.0, 10.0, 15.0, 20.0]),
            "fixed_sl": random.choice([None, 5.0, 10.0, 15.0]),
            "bucket_minutes": random.choice([1, 2, 3, 5, 8, 10]),
            "round_turn_cost": -2.0
        }
        
        # Ensure thresholds are hierarchical
        if params["conf_med"] >= params["conf_high"]: params["conf_med"] = params["conf_high"] - 5
        if params["conf_low"] >= params["conf_med"]: params["conf_low"] = params["conf_med"] - 3
        if params["conf_low"] <= 0: params["conf_low"] = 1

        res = run_backtest(params)
        if res:
            pph = res['pips_per_hour']
            trades = res['trade_count']
            
            # Penalize low trade counts to find active strategies
            score = pph if trades >= 3 else pph - 10 
            
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"Cycle {i+1:03}: PPH={pph:<7} | Trades={trades:<3} | H={params['conf_high']} M={params['conf_med']} L={params['conf_low']} Off={params['price_offset']} Min={params['bucket_minutes']} TP={params['fixed_tp']} SL={params['fixed_sl']}\n")

            if score > best_pph:
                best_pph = score
                best_params = params.copy()
                print(f"Cycle {i+1:03}: New Best! PPH={pph} Trades={trades} (H={params['conf_high']} M={params['conf_med']} L={params['conf_low']} Off={params['price_offset']} Min={params['bucket_minutes']})")

    print(f"\nOptimization finished.")
    print(f"Best Realistic Params: {json.dumps(best_params, indent=2)}")

if __name__ == "__main__":
    main()
