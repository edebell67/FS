import json
import os
import subprocess
import random
from pathlib import Path

# Paths
DATA_PATH = r"X:\eds\TradeApps\breakout\fs\json\live\forex\2026-05-13\_price_capture.jsonl"
BACKTEST_SCRIPT = r"epics\ep_016_turning_point_pattern_engine\logic\backtest_gbp_analyzer.py"
OUTPUT_DIR = Path(r"epics\ep_016_turning_point_pattern_engine\optimization")

def run_backtest(symbol, params):
    cmd = ["python", BACKTEST_SCRIPT, "--data", DATA_PATH, "--symbol", symbol]
    for k, v in params.items():
        if v is not None:
            cmd.extend([f"--{k}", str(v)])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except:
        return None

def optimize_symbol(symbol, cost=-2.0):
    print(f"\n{'='*40}")
    print(f"OPTIMIZING SYMBOL (MARKET ONLY): {symbol} (Cost: {cost})")
    print(f"{'='*40}")
    
    best_pph = -999.0
    best_params = {
        "conf_high": 20,
        "conf_med": 10,
        "conf_low": 5,
        "price_offset": 0.0,
        "fixed_tp": None,
        "fixed_sl": None,
        "bucket_minutes": 5,
        "round_turn_cost": cost
    }
    
    log_file = OUTPUT_DIR / f"opt_log_market_{symbol}.txt"
    best_file = OUTPUT_DIR / f"best_config_market_{symbol}.json"
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"Starting 100-Cycle Market-Only Optimization for {symbol}\n")
        f.write("-" * 80 + "\n")

    for i in range(1, 101):
        test_params = best_params.copy()
        test_params["price_offset"] = 0.0 # Strict enforcement
        
        # Mutation strategy
        if random.random() < 0.7:
            # Narrow search on thresholds
            test_params["conf_high"] = max(5, test_params["conf_high"] + random.randint(-5, 5))
            test_params["conf_med"] = max(3, test_params["conf_med"] + random.randint(-3, 3))
            test_params["conf_low"] = max(1, test_params["conf_low"] + random.randint(-2, 2))
            
            # Ensure order
            if test_params["conf_low"] >= test_params["conf_med"]: test_params["conf_low"] = test_params["conf_med"] - 1
            if test_params["conf_med"] >= test_params["conf_high"]: test_params["conf_med"] = test_params["conf_high"] - 1
            
            # TP/SL mutations
            if random.random() < 0.3:
                test_params["fixed_tp"] = random.choice([None, 5, 10, 15, 20, 30, 50])
                test_params["fixed_sl"] = random.choice([None, 5, 10, 15, 20])
        else:
            # Wide search on thresholds and buckets
            test_params["conf_high"] = random.randint(10, 80)
            test_params["conf_med"] = random.randint(5, 40)
            test_params["conf_low"] = random.randint(1, 20)
            test_params["bucket_minutes"] = random.choice([1, 2, 3, 5, 8, 10, 15])
            
            if test_params["conf_low"] >= test_params["conf_med"]: test_params["conf_low"] = max(1, test_params["conf_med"] - 1)
            if test_params["conf_med"] >= test_params["conf_high"]: test_params["conf_med"] = max(2, test_params["conf_high"] - 1)

        res = run_backtest(symbol, test_params)
        if res:
            pph = res["pips_per_hour"]
            log_line = f"Cycle {i:03}: PPH={pph:<7} | H={test_params['conf_high']} M={test_params['conf_med']} L={test_params['conf_low']} Min={test_params['bucket_minutes']} TP={test_params['fixed_tp']} SL={test_params['fixed_sl']} Trades={res['trade_count']}"
            
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(log_line + "\n")
            
            if pph > best_pph:
                best_pph = pph
                best_params = test_params.copy()
                print(f"[{symbol}] Cycle {i:03} NEW BEST: {best_pph} PPH")
                with open(best_file, "w", encoding="utf-8") as f:
                    json.dump({"symbol": symbol, "pph": best_pph, "results": res, "cycle": i}, f, indent=4)

def main():
    target_symbols = [
        "GBPAUD_C",
        "EURAUD_C",
        "NZDAUD_C",
        "AUDCAD_C",
        "CHFCAD_C",
        "CADJPY_C"
    ]
    for target in target_symbols:
        cost = -3.0 if target.endswith("_C") else -2.0
        optimize_symbol(target, cost=cost)
    print("\nMARKET-ONLY OPTIMIZATIONS COMPLETE.")

if __name__ == "__main__":
    main()
