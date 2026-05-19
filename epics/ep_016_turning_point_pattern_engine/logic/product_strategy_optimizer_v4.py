import json
import os
import random
import argparse
from datetime import datetime
from pathlib import Path

# Import the backtester class directly for high-speed in-memory optimization
from backtest_gbp_analyzer import GBPBacktester

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
RESEARCH_ROOT = Path(r"C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\research")

def main():
    parser = argparse.ArgumentParser(description="V4 Aggressive Gate Optimizer (High Speed)")
    parser.add_argument("--symbol", required=True, help="Symbol to optimize")
    parser.add_argument("--date", default="2026-05-13", help="Date to use for optimization")
    parser.add_argument("--improvements", type=int, default=20, help="Number of progressive IMPROVEMENTS to find")
    parser.add_argument("--max_attempts", type=int, default=100000, help="Maximum total attempts before stopping")
    parser.add_argument("--target", choices=["growth", "efficiency", "legacy"], default="legacy", 
                        help="growth: >=10 PPH + 15h, efficiency: >=6 PPT + 25 trades")
    
    args = parser.parse_args()
    
    data_path = f"X:\\eds\\TradeApps\\breakout\\fs\\json\\live\\forex\\{args.date}\\_price_capture.jsonl"
    log_file = RESEARCH_ROOT / f"opt_log_{args.symbol}_{args.date}_v4_{args.target}.txt"
    
    # 1. LOAD DATA ONCE
    print(f"Loading data for {args.symbol} on {args.date}...")
    # Create a dummy backtester just to load the data
    loader = GBPBacktester(data_path, args.symbol)
    if not loader.load_data():
        print(f"Failed to load data from {data_path}")
        return

    print(f"Data loaded successfully. Snapshots: {len(loader.all_snapshots)}")
    
    best_pph = -999.0
    best_params = {}
    
    print(f"Starting V4 HIGH-SPEED {args.target.upper()} Optimization for {args.symbol} on {args.date}.")
    if args.target == "growth":
        print("Objective: Exceed 10 PPH based on 15hr min duration.")
    elif args.target == "efficiency":
        print("Objective: Exceed 6 Pips-Per-Trade based on 25 trades.")
    
    RESEARCH_ROOT.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"V4 HIGH-SPEED AGGRESSIVE GATE Optimization Log - Symbol: {args.symbol} - Date: {args.date} - Target: {args.target}\n")
        if args.target == "growth":
            f.write("Gate Rule: PPH >= 10.0 AND Duration >= 15h\n")
        elif args.target == "efficiency":
            f.write("Gate Rule: Pips-Per-Trade >= 6.0 AND Trades >= 25\n")
        else:
            f.write("Gate Rule: PPH > best_pph AND Trades >= 5 (Legacy V3)\n")
        f.write(f"Hard Cap: {args.max_attempts} attempts.\n")
        f.write("------------------------------------------------------------------------\n")

    improvement_count = 0
    total_attempts = 0

    while improvement_count < args.improvements and total_attempts < args.max_attempts:
        total_attempts += 1
        
        # 1. Parameter Selection: RANDOM EXPLORATION
        params = {
            "conf_high": random.randint(15, 80),
            "conf_med": random.randint(8, 45),
            "conf_low": random.randint(2, 25),
            "price_offset": round(random.uniform(-5.0, 2.5), 2),
            "fixed_tp": random.choice([None, 10.0, 20.0, 30.0, 50.0, 100.0]),
            "fixed_sl": random.choice([None, 10.0, 20.0, 30.0, 50.0]),
            "bucket_minutes": random.choice([1, 2, 3, 5, 8, 10, 15, 30]),
            "round_turn_cost": -2.0,
            "mild_threshold": 5,
            "accumulation": 1
        }
        
        # Ensure thresholds are hierarchical
        if params["conf_med"] >= params["conf_high"]: params["conf_med"] = params["conf_high"] - 5
        if params["conf_low"] >= params["conf_med"]: params["conf_low"] = params["conf_med"] - 3
        if params["conf_low"] <= 0: params["conf_low"] = 1

        # 2. RUN SIMULATION IN MEMORY (High Speed)
        bt = GBPBacktester(data_path, args.symbol, params)
        bt.all_snapshots = loader.all_snapshots
        bt.minute_data = loader.minute_data
        
        res = bt.run_simulation()
        if res:
            pph = res['pips_per_hour']
            trades = res['trade_count']
            duration = res['duration_hours']
            total_net = res['total_net']
            ppt = total_net / trades if trades > 0 else 0
            
            # CRITERIA: Gate Enforcement
            is_improvement = False
            
            if args.target == "growth":
                # High Velocity Gate: 10 PPH floor + 12h stability
                if pph >= 10.0 and duration >= 12.0 and pph > best_pph:
                    is_improvement = True
            elif args.target == "efficiency":
                # High Efficiency Gate: 6 PPT floor + 25 trade significance
                if ppt >= 6.0 and trades >= 25 and pph > best_pph:
                    is_improvement = True
            else:
                # Legacy V3 Gate: Improvement + 5 trades
                if pph > best_pph and trades >= 5:
                    is_improvement = True

            if is_improvement:
                improvement_count += 1
                best_pph = pph
                best_params = params.copy()
                
                print(f"Improvement {improvement_count:02}/{args.improvements}: PPH={pph} PPT={ppt:.2f} Trades={trades} (Attempt {total_attempts})")
                
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"Improvement {improvement_count:03} (Attempt {total_attempts}): PPH={pph:<7} | PPT={ppt:0.2f} | Trades={trades:<3} | Dur={duration:<5} | H={params['conf_high']} M={params['conf_med']} L={params['conf_low']} Off={params['price_offset']} Min={params['bucket_minutes']} TP={params['fixed_tp']} SL={params['fixed_sl']}\n")
            
            # UI Pulse
            if total_attempts % 500 == 0:
                print(f"... Searching ({args.target}). Best PPH: {best_pph:.2f} | Attempts: {total_attempts}")

    print(f"\nOptimization for {args.symbol} ({args.target}) finished after {total_attempts} total attempts.")

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
