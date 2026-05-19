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

def mutate_params(params, target):
    """
    Applies tiny 'Hill Climbing' mutations to a parameter set.
    """
    new_params = params.copy()
    
    # 1. Selection Strategy based on Target
    if target == "efficiency":
        # For efficiency, we want "Thicker" trades. 
        # Nudges: Increase thresholds, increase price offset (wait for better price)
        key = random.choice(["conf_high", "conf_med", "conf_low", "price_offset"])
        if key.startswith("conf"):
            new_params[key] += random.choice([1, 2]) # Move UP to be more selective
        elif key == "price_offset":
            new_params[key] = round(new_params[key] - random.uniform(0.01, 0.05), 2) # More negative = harder fill
    else:
        # For growth, we want "Velocity".
        # Nudges: Decrease thresholds, bring price offset closer to market
        key = random.choice(["conf_high", "conf_med", "conf_low", "price_offset"])
        if key.startswith("conf"):
            new_params[key] += random.choice([-3, -2, -1, 1, 2, 3])
        elif key == "price_offset":
            new_params[key] = round(new_params[key] + random.uniform(-0.05, 0.05), 2)

    # Occasionally swap discrete values (5% chance)
    if random.random() < 0.05:
        new_params["bucket_minutes"] = random.choice([1, 2, 3, 5, 8, 10, 15, 30])
    
    # Keep within reasonable bounds
    new_params["conf_high"] = max(20, min(100, new_params["conf_high"]))
    new_params["conf_med"] = max(10, min(70, new_params["conf_med"]))
    new_params["conf_low"] = max(2, min(40, new_params["conf_low"]))
    new_params["price_offset"] = max(-5.0, min(5.0, new_params["price_offset"]))

    # Enforce hierarchy
    if new_params["conf_med"] >= new_params["conf_high"]: new_params["conf_med"] = new_params["conf_high"] - 2
    if new_params["conf_low"] >= new_params["conf_med"]: new_params["conf_low"] = new_params["conf_med"] - 2
    if new_params["conf_low"] <= 0: new_params["conf_low"] = 1
    
    return new_params

def main():
    parser = argparse.ArgumentParser(description="V5 Hill Climbing Optimizer")
    parser.add_argument("--symbol", required=True, help="Symbol to optimize")
    parser.add_argument("--date", default="2026-05-15", help="Date to use for optimization")
    parser.add_argument("--improvements", type=int, default=20, help="Number of progressive IMPROVEMENTS to find")
    parser.add_argument("--max_attempts", type=int, default=5000, help="Maximum total attempts before stopping")
    parser.add_argument("--target", choices=["growth", "efficiency"], default="growth", 
                        help="growth: >=10 PPH + 15h, efficiency: >=6 PPT + 25 trades")
    
    args = parser.parse_args()
    
    data_path = f"X:\\eds\\TradeApps\\breakout\\fs\\json\\live\\forex\\{args.date}\\_price_capture.jsonl"
    log_file = RESEARCH_ROOT / f"opt_log_{args.symbol}_{args.date}_v5_hc_{args.target}.txt"
    
    # 1. LOAD DATA ONCE
    print(f"Loading data for {args.symbol} on {args.date}...")
    loader = GBPBacktester(data_path, args.symbol)
    if not loader.load_data():
        print(f"Failed to load data from {data_path}")
        return
    print(f"Data loaded successfully. Snapshots: {len(loader.all_snapshots)}")

    # 2. FIND INITIAL SEED
    summary_file = RESEARCH_ROOT / "top_product_strategies.json"
    seed_params = None
    if summary_file.exists():
        with open(summary_file, "r") as sf:
            summary = json.load(sf)
            if args.symbol in summary:
                seed_params = summary[args.symbol]["params"]
                print(f"Loaded SEED parameters for {args.symbol} from summary file.")

    if not seed_params:
        # Fallback to defaults if no champion exists
        seed_params = {
            "conf_high": 50, "conf_med": 30, "conf_low": 15,
            "price_offset": 0.0, "fixed_tp": 50.0, "fixed_sl": 30.0,
            "bucket_minutes": 5, "round_turn_cost": -2.0, "mild_threshold": 5, "accumulation": 1
        }
        print("No champion found. Starting with default SEED.")

    # Run initial backtest to set baseline
    bt_seed = GBPBacktester(data_path, args.symbol, seed_params)
    bt_seed.all_snapshots = loader.all_snapshots
    bt_seed.minute_data = loader.minute_data
    res_seed = bt_seed.run_simulation()
    
    best_pph = res_seed['pips_per_hour']
    current_params = seed_params.copy()
    
    print(f"Initial SEED PPH: {best_pph:.2f}")
    print(f"Starting V5 HILL CLIMBING for {args.symbol} on {args.date}.")
    
    RESEARCH_ROOT.mkdir(parents=True, exist_ok=True)
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"V5 HILL CLIMBING Optimization Log - Symbol: {args.symbol} - Date: {args.date} - Target: {args.target}\n")
        f.write(f"Seed PPH: {best_pph}\n")
        f.write("------------------------------------------------------------------------\n")

    improvement_count = 0
    total_attempts = 0

    while improvement_count < args.improvements and total_attempts < args.max_attempts:
        total_attempts += 1
        
        # 1. GENERATE NEIGHBOR (Mutation)
        params = mutate_params(current_params, args.target)

        # 2. RUN SIMULATION
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
            
            # CRITERIA Check
            is_improvement = False
            
            if args.target == "growth":
                if pph > best_pph and pph >= 10.0 and duration >= 12.0:
                    is_improvement = True
            elif args.target == "efficiency":
                if pph > best_pph and ppt >= 6.0 and trades >= 25:
                    is_improvement = True

            if is_improvement:
                improvement_count += 1
                best_pph = pph
                current_params = params.copy() # Champion moves to new peak
                
                print(f"Climb {improvement_count:02}/{args.improvements}: PPH={pph} PPT={ppt:.2f} Trades={trades} (Attempt {total_attempts})")
                
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"Climb {improvement_count:03} (Attempt {total_attempts}): PPH={pph:<7} | PPT={ppt:0.2f} | Trades={trades:<3} | H={params['conf_high']} M={params['conf_med']} L={params['conf_low']} Off={params['price_offset']} Min={params['bucket_minutes']}\n")
            
            # UI Pulse
            if total_attempts % 500 == 0:
                print(f"... Climbing. Peak PPH: {best_pph:.2f} | Attempts: {total_attempts}")

    print(f"\nHill Climb for {args.symbol} finished after {total_attempts} total attempts.")
    print(f"Final Peak Params: {json.dumps(current_params, indent=2)}")

if __name__ == "__main__":
    main()
