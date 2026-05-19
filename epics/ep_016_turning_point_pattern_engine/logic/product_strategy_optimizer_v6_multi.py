import json
import os
import random
import argparse
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Import the backtester class directly for high-speed in-memory optimization
from backtest_gbp_analyzer import GBPBacktester

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
RESEARCH_ROOT = Path(r"C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\research")
DATA_ROOT = Path(r"X:\eds\TradeApps\breakout\fs\json\live\forex")

class MultiDayOptimizer:
    def __init__(self, symbol, dates):
        self.symbol = symbol
        self.dates = dates
        self.day_loaders = {}
        
    def load_all_days(self):
        print(f"Pre-loading data for {len(self.dates)} days...")
        for date_str in self.dates:
            data_path = DATA_ROOT / date_str / "_price_capture.jsonl"
            if not data_path.exists():
                print(f"Warning: Data missing for {date_str}")
                continue
                
            loader = GBPBacktester(str(data_path), self.symbol)
            if loader.load_data():
                self.day_loaders[date_str] = loader
                print(f"Loaded {date_str}: {len(loader.all_snapshots)} snapshots.")
            else:
                print(f"Failed to load {date_str}")
        return len(self.day_loaders) > 0

    def run_multi_day_sim(self, params):
        day_results = []
        for date_str, loader in self.day_loaders.items():
            bt = GBPBacktester("", self.symbol, params)
            # Inject pre-loaded data
            bt.all_snapshots = loader.all_snapshots
            bt.minute_data = loader.minute_data
            
            res = bt.run_simulation()
            if res:
                day_results.append(res)
        
        if not day_results:
            return None
            
        total_net = sum(r['total_net'] for r in day_results)
        total_hours = sum(r['duration_hours'] for r in day_results)
        total_trades = sum(r['trade_count'] for r in day_results)
        
        # Stability Metrics
        pph_list = [r['pips_per_hour'] for r in day_results]
        min_pph = min(pph_list)
        avg_pph = total_net / total_hours if total_hours > 0 else 0
        profitable_days = sum(1 for p in pph_list if p > 0)
        profit_ratio = profitable_days / len(day_results)
        
        return {
            "total_net": total_net,
            "avg_pph": avg_pph,
            "min_pph": min_pph,
            "profit_ratio": profit_ratio,
            "total_trades": total_trades,
            "day_results": day_results
        }

def main():
    parser = argparse.ArgumentParser(description="V6 Multi-Day Optimizer")
    parser.add_argument("--symbol", required=True, help="Symbol to optimize")
    parser.add_argument("--dates", nargs="+", required=True, help="Dates list (YYYY-MM-DD)")
    parser.add_argument("--improvements", type=int, default=20, help="Number of progressive IMPROVEMENTS to find")
    parser.add_argument("--max_attempts", type=int, default=10000, help="Maximum total attempts before stopping")
    
    args = parser.parse_args()
    
    log_file = RESEARCH_ROOT / f"opt_log_{args.symbol}_multi_v6.txt"
    
    opt = MultiDayOptimizer(args.symbol, args.dates)
    if not opt.load_all_days():
        print("Error: No data loaded.")
        return

    best_stability_score = -999.0 # We use Min PPH as our primary stability score
    best_params = {}
    
    print(f"Starting V6 MULTI-DAY Optimization for {args.symbol} across {len(opt.day_loaders)} days.")
    print(f"Objective: Maximize MINIMUM PPH (Stability).")
    
    RESEARCH_ROOT.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"V6 MULTI-DAY Optimization Log - Symbol: {args.symbol} - Dates: {args.dates}\n")
        f.write(f"Primary Objective: Max(Min PPH) across all days.\n")
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
            "price_offset": round(random.uniform(-4.0, 1.5), 2),
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

        res = opt.run_multi_day_sim(params)
        if res:
            score = res['min_pph'] # STABILITY FIRST: Optimize for the worst day
            avg_pph = res['avg_pph']
            
            # Acceptance Criteria: 
            # 1. Higher Min PPH (more stable)
            # 2. Minimum trade count (at least 5 per day average)
            if score > best_stability_score and res['total_trades'] >= (len(opt.day_loaders) * 5):
                improvement_count += 1
                best_stability_score = score
                best_params = params.copy()
                
                print(f"Improvement {improvement_count:02}/{args.improvements}: MinPPH={score:.2f} AvgPPH={avg_pph:.2f} (Attempt {total_attempts})")
                
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"Improvement {improvement_count:03} (Attempt {total_attempts}): MinPPH={score:<7} | AvgPPH={avg_pph:<7} | WinRate={res['profit_ratio']*100:.0f}% | H={params['conf_high']} M={params['conf_med']} L={params['conf_low']} Off={params['price_offset']} Min={params['bucket_minutes']}\n")
            
            # UI Pulse
            if total_attempts % 100 == 0:
                print(f"... Searching. Best MinPPH: {best_stability_score:.2f} | Attempts: {total_attempts}")

    print(f"\nOptimization for {args.symbol} finished after {total_attempts} total attempts.")
    print(f"Universal Champion Params: {json.dumps(best_params, indent=2)}")

if __name__ == "__main__":
    main()
