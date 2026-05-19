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
    parser = argparse.ArgumentParser(description="Multi-Product Improvement-Only Optimizer")
    parser.add_argument("--symbol", required=True, help="Symbol to optimize")
    parser.add_argument("--date", default="2026-05-13", help="Date to use for optimization")
    parser.add_argument("--improvements", type=int, default=20, help="Number of progressive IMPROVEMENTS to find")
    parser.add_argument("--max_attempts", type=int, default=100000, help="Maximum total attempts before stopping")
    
    args = parser.parse_args()
    
    data_path = f"X:\\eds\\TradeApps\\breakout\\fs\\json\\live\\forex\\{args.date}\\_price_capture.jsonl"
    log_file = RESEARCH_ROOT / f"opt_log_{args.symbol}_{args.date}_v3_improvements.txt"
    
    best_pph = -999.0
    best_params = {}
    
    print(f"Starting UPGRADED Improvement-Only Optimization for {args.symbol} on {args.date}.")
    print(f"Target: Find {args.improvements} progressively better strategies (Max attempts: {args.max_attempts}).")
    
    RESEARCH_ROOT.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"V3 IMPROVEMENT-ONLY Optimization Log - Symbol: {args.symbol} - Date: {args.date}\n")
        f.write(f"Note: Cycle count only increments when PPH > best_pph and Trades >= 5.\n")
        f.write(f"Hard Cap: {args.max_attempts} attempts.\n")
        f.write("------------------------------------------------------------------------\n")

    improvement_count = 0
    total_attempts = 0

    while improvement_count < args.improvements and total_attempts < args.max_attempts:
        total_attempts += 1
        
        # 1. Parameter Selection: RANDOM EXPLORATION
        # We use a wide range to find the "Turning Point" surface
        params = {
            "conf_high": random.randint(15, 70),
            "conf_med": random.randint(8, 40),
            "conf_low": random.randint(2, 20),
            "price_offset": round(random.uniform(-4.0, 1.5), 2),
            "fixed_tp": random.choice([None, 10.0, 20.0, 30.0, 50.0]),
            "fixed_sl": random.choice([None, 10.0, 20.0, 30.0, 50.0]),
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
            
            # CRITERIA: Must be BETTER than previous BEST and have significant trade count
            if pph > best_pph and trades >= 5:
                improvement_count += 1
                best_pph = pph
                best_params = params.copy()
                
                print(f"Improvement {improvement_count:02}/{args.improvements}: PPH={pph} Trades={trades} (Attempt {total_attempts})")
                
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"Improvement {improvement_count:03} (Attempt {total_attempts}): PPH={pph:<7} | Trades={trades:<3} | H={params['conf_high']} M={params['conf_med']} L={params['conf_low']} Off={params['price_offset']} Min={params['bucket_minutes']} TP={params['fixed_tp']} SL={params['fixed_sl']}\n")
            
            # UI Pulse every 100 attempts to show the model is still alive
            if total_attempts % 100 == 0:
                print(f"... Still searching. Current Best PPH: {best_pph:.2f} | Total attempts: {total_attempts}")

    print(f"\nOptimization for {args.symbol} finished after {total_attempts} total attempts.")
    print(f"Final Best Params: {json.dumps(best_params, indent=2)}")
    
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
        "search_type": "improvement_only",
        "total_attempts": total_attempts,
        "last_updated": datetime.now().isoformat()
    }
    
    with open(summary_file, "w") as sf:
        json.dump(summary, sf, indent=2)

if __name__ == "__main__":
    main()
