import json
import subprocess
import sys
from pathlib import Path
import argparse
from datetime import datetime
from itertools import product

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
PYTHON_EXE = sys.executable
BACKTEST_SCRIPT = Path(__file__).parent / "backtest_gbp_analyzer.py"
RESEARCH_ROOT = Path(__file__).parent.parent / "research"
OPTIMIZATION_ROOT = Path(__file__).parent.parent / "optimization"

# EUR product group symbols
EUR_SYMBOLS = ["EURAUD_C", "EURCAD_C", "EURCHF_C", "EURGBP_C", "EURJPY_C", "EURNZD_C", "EURUSD_C"]

# Smart parameter search space - focused ranges based on prior optimization results
PARAM_GRID = {
    "conf_high": [30, 40, 50, 60],
    "conf_med": [12, 16, 20, 25],
    "conf_low": [5, 8, 10, 13],
    "price_offset": [-2.0, -1.0, 0.0, 0.5],
    "bucket_minutes": [3, 5, 8],
    "fixed_tp": [None, 20.0, 30.0],
    "fixed_sl": [None, 20.0, 30.0]
}

def run_backtest(data_path, symbol, params):
    cmd = [PYTHON_EXE, str(BACKTEST_SCRIPT), "--data", data_path, "--symbol", symbol]
    for k, v in params.items():
        if v is not None:
            cmd.extend([f"--{k}", str(v)])

    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except:
        return None

def generate_random_params():
    """
    Random parameter generation - wide exploration.
    """
    import random
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

    # Ensure hierarchical constraints
    if params["conf_med"] >= params["conf_high"]:
        params["conf_med"] = params["conf_high"] - 5
    if params["conf_low"] >= params["conf_med"]:
        params["conf_low"] = params["conf_med"] - 3
    if params["conf_low"] <= 0:
        params["conf_low"] = 1

    return params

def main():
    parser = argparse.ArgumentParser(description="EUR Smart Optimizer - Improvement-Based with Early Stop")
    parser.add_argument("--symbol", default="EURAUD_C", help="EUR symbol to optimize")
    parser.add_argument("--date", default="2026-05-13", help="Date to use for optimization")
    parser.add_argument("--max_cycles", type=int, default=100, help="Maximum cycles to run")
    parser.add_argument("--target_high_pph", type=float, default=10.0, help="PPH threshold for early stop")
    parser.add_argument("--high_pph_count", type=int, default=5, help="Number of high PPH cycles for early stop")
    parser.add_argument("--min_improvement", type=float, default=1.0, help="Minimum PPH improvement to count as valid cycle")

    args = parser.parse_args()

    data_path = f"X:\\eds\\TradeApps\\breakout\\fs\\json\\live\\forex\\{args.date}\\_price_capture.jsonl"
    log_file = RESEARCH_ROOT / f"eur_smart_opt_{args.symbol}_{args.date}.txt"
    result_file = RESEARCH_ROOT / f"eur_smart_best_{args.symbol}.json"

    best_pph = 0.0  # Must be positive
    best_params = {}
    high_pph_cycles = []  # Track cycles above target_high_pph
    valid_cycles = []  # All valid improvement cycles

    print(f"EUR Smart Optimizer - {args.symbol} on {args.date}", flush=True)
    print(f"Criteria: PPH > 0 AND PPH > previous best", flush=True)
    print(f"Termination: {args.max_cycles} cycles OR {args.high_pph_count} cycles above {args.target_high_pph} PPH", flush=True)
    print("-" * 70, flush=True)

    RESEARCH_ROOT.mkdir(parents=True, exist_ok=True)

    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"EUR Smart Optimizer Log - Symbol: {args.symbol} - Date: {args.date}\n")
        f.write(f"Validation: PPH > 0 AND PPH > previous best\n")
        f.write(f"Termination: {args.max_cycles} cycles OR {args.high_pph_count} cycles above {args.target_high_pph} PPH\n")
        f.write("=" * 70 + "\n")

    cycle_count = 0
    total_attempts = 0

    while cycle_count < args.max_cycles:
        # Early stop check
        if len(high_pph_cycles) >= args.high_pph_count:
            print(f"\nEARLY STOP: Found {args.high_pph_count} cycles above {args.target_high_pph} PPH!")
            break

        total_attempts += 1
        params = generate_random_params()

        res = run_backtest(data_path, args.symbol, params)
        if res:
            pph = res['pips_per_hour']
            trades = res['trade_count']

            # Validation criteria:
            # 1. Must be positive (PPH > 0)
            # 2. Must beat previous best
            # 3. Must have at least 3 trades for minimal validity
            if pph > 0 and pph > best_pph and trades >= 3:
                cycle_count += 1

                improvement = pph - best_pph
                best_pph = pph
                best_params = params.copy()

                cycle_data = {
                    "cycle": cycle_count,
                    "pph": pph,
                    "trades": trades,
                    "improvement": round(improvement, 2),
                    "params": params,
                    "attempt": total_attempts
                }
                valid_cycles.append(cycle_data)

                # Check if this is a high PPH cycle
                if pph >= args.target_high_pph:
                    high_pph_cycles.append(cycle_data)
                    marker = f" *** HIGH PPH ({len(high_pph_cycles)}/{args.high_pph_count}) ***"
                else:
                    marker = ""

                print(f"Cycle {cycle_count:02}/{args.max_cycles}: PPH={pph:.2f} (+{improvement:.2f}) Trades={trades} [Attempt {total_attempts}]{marker}", flush=True)

                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"Cycle {cycle_count:03}: PPH={pph:<7.2f} | +{improvement:<5.2f} | Trades={trades:<3} | H={params['conf_high']} M={params['conf_med']} L={params['conf_low']} Off={params['price_offset']} Min={params['bucket_minutes']} TP={params['fixed_tp']} SL={params['fixed_sl']}{marker}\n")

        # Progress pulse every 50 attempts
        if total_attempts % 50 == 0:
            print(f"  ... Searching. Best PPH: {best_pph:.2f} | Valid cycles: {cycle_count} | High PPH: {len(high_pph_cycles)} | Attempts: {total_attempts}", flush=True)

    # Summary
    print("\n" + "=" * 70)
    print(f"OPTIMIZATION COMPLETE - {args.symbol}")
    print(f"Total attempts: {total_attempts}")
    print(f"Valid cycles: {cycle_count}")
    print(f"High PPH cycles (>={args.target_high_pph}): {len(high_pph_cycles)}")
    print(f"Best PPH: {best_pph:.2f}")
    print(f"Best params: {json.dumps(best_params, indent=2)}")

    # Save results
    result = {
        "symbol": args.symbol,
        "date": args.date,
        "best_pph": best_pph,
        "best_params": best_params,
        "total_attempts": total_attempts,
        "valid_cycles": cycle_count,
        "high_pph_cycles": len(high_pph_cycles),
        "high_pph_details": high_pph_cycles,
        "all_valid_cycles": valid_cycles,
        "completed_at": datetime.now().isoformat()
    }

    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    with open(log_file, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 70 + "\n")
        f.write(f"FINAL RESULT: Best PPH = {best_pph:.2f} after {total_attempts} attempts\n")
        f.write(f"Best Params: {json.dumps(best_params)}\n")
        if high_pph_cycles:
            f.write(f"\nHigh PPH Cycles (>= {args.target_high_pph}):\n")
            for hpc in high_pph_cycles:
                f.write(f"  Cycle {hpc['cycle']}: PPH={hpc['pph']:.2f}\n")

    print(f"\nResults saved to: {result_file}")

if __name__ == "__main__":
    main()
