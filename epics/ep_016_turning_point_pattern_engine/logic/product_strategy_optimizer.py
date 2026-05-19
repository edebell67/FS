import json
import os
import subprocess
from pathlib import Path
import random
import argparse
from datetime import datetime

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
# DATA_PATH = r"X:\eds\TradeApps\breakout\fs\json\live\forex\2026-05-13\_price_capture.jsonl"
BACKTEST_SCRIPT = r"C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\logic\backtest_gbp_analyzer.py"
RESEARCH_ROOT = Path(r"C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\research")

def run_backtest(data_path, symbol, params):
    cmd = ["python", BACKTEST_SCRIPT, "--data", data_path, "--symbol", symbol]
    for k, v in params.items():
        if v is not None:
            cmd.extend([f"--{k}", str(v)])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except:
        return None

def main():
    parser = argparse.ArgumentParser(description="Multi-Product Randomized Optimizer")
    parser.add_argument("--symbol", required=True, help="Symbol to optimize")
    parser.add_argument("--date", default="2026-05-13", help="Date to use for optimization")
    parser.add_argument("--cycles", type=int, default=100, help="Number of optimization cycles")
    
    args = parser.parse_args()
    
    data_path = f"X:\\eds\\TradeApps\\breakout\\fs\\json\\live\\forex\\{args.date}\\_price_capture.jsonl"
    log_file = RESEARCH_ROOT / f"opt_log_{args.symbol}_{args.date}.txt"
    
    best_pph = -999
    best_params = {}
    
    print(f"Starting Clean {args.cycles}-Cycle Optimization for {args.symbol} on {args.date}.")
    
    RESEARCH_ROOT.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"Optimization Log - Symbol: {args.symbol} - Date: {args.date}\n")
        f.write("----------------------------------------------------------------\n")

    for i in range(args.cycles):
        params = {
            "conf_high": random.randint(15, 60),
            "conf_med": random.randint(8, 35),
            "conf_low": random.randint(2, 15),
            "price_offset": round(random.uniform(-5.0, 2.0), 2),
            "fixed_tp": random.choice([None, 10.0, 20.0, 30.0, 50.0]),
            "fixed_sl": random.choice([None, 10.0, 20.0, 30.0]),
            "bucket_minutes": random.choice([1, 2, 3, 5, 8, 10, 15]),
            "round_turn_cost": -2.0
        }
        
        # Ensure thresholds are hierarchical
        if params["conf_med"] >= params["conf_high"]: params["conf_med"] = params["conf_high"] - 5
        if params["conf_low"] >= params["conf_med"]: params["conf_low"] = params["conf_med"] - 3
        if params["conf_low"] <= 0: params["conf_low"] = 1

        res = run_backtest(data_path, args.symbol, params)
        if res:
            pph = res['pips_per_hour']
            trades = res['trade_count']
            
            # Penalize low trade counts (want at least 5 trades a day for statistical significance)
            score = pph if trades >= 5 else pph - 15 
            
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"Cycle {i+1:03}: PPH={pph:<7} | Trades={trades:<3} | H={params['conf_high']} M={params['conf_med']} L={params['conf_low']} Off={params['price_offset']} Min={params['bucket_minutes']} TP={params['fixed_tp']} SL={params['fixed_sl']}\n")

            if score > best_pph:
                best_pph = score
                best_params = params.copy()
                print(f"Cycle {i+1:03}: New Best! PPH={pph} Trades={trades} (H={params['conf_high']} M={params['conf_med']} L={params['conf_low']} Off={params['price_offset']} Min={params['bucket_minutes']})")

    print(f"\nOptimization for {args.symbol} finished.")
    print(f"Best Realistic Params: {json.dumps(best_params, indent=2)}")
    
    # Save best results to a summary file
    summary_file = RESEARCH_ROOT / "top_product_strategies.json"
    summary = {}
    if summary_file.exists():
        with open(summary_file, "r") as sf:
            summary = json.load(sf)
    
    summary[args.symbol] = {
        "best_pph": best_pph,
        "params": best_params,
        "date_optimized": args.date,
        "last_updated": datetime.now().isoformat()
    }
    
    with open(summary_file, "w") as sf:
        json.dump(summary, sf, indent=2)

if __name__ == "__main__":
    main()
