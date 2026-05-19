import json
import os
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
DATA_ROOT = Path(r"X:\eds\TradeApps\breakout\fs\json\live\forex")
BACKTEST_SCRIPT = Path(r"C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\logic\backtest_gbp_analyzer.py")

def run_backtest_for_date(date_str, symbol, params):
    file_path = DATA_ROOT / date_str / "_price_capture.jsonl"
    if not file_path.exists():
        return None
    
    cmd = ["python", str(BACKTEST_SCRIPT), "--data", str(file_path), "--symbol", symbol]
    for k, v in params.items():
        if v is not None:
            cmd.extend([f"--{k}", str(v)])
            
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(result.stdout)
    except:
        return None

def main():
    parser = argparse.ArgumentParser(description="Multi-Day Strategy Performance Harness")
    parser.add_argument("--symbol", required=True, help="Symbol to test")
    parser.add_argument("--dates", nargs="+", help="Space separated date list (YYYY-MM-DD)")
    parser.add_argument("--conf_high", type=int, default=30)
    parser.add_argument("--conf_med", type=int, default=22)
    parser.add_argument("--conf_low", type=int, default=8)
    parser.add_argument("--bucket_minutes", type=int, default=8)
    parser.add_argument("--price_offset", type=float, default=0.57)
    parser.add_argument("--fixed_tp", type=float, default=20.0)
    parser.add_argument("--fixed_sl", type=float, default=None)
    parser.add_argument("--round_turn_cost", type=float, default=-2.0)
    
    args = parser.parse_args()
    
    params = {
        "conf_high": args.conf_high,
        "conf_med": args.conf_med,
        "conf_low": args.conf_low,
        "bucket_minutes": args.bucket_minutes,
        "price_offset": args.price_offset,
        "fixed_tp": args.fixed_tp,
        "fixed_sl": args.fixed_sl,
        "round_turn_cost": args.round_turn_cost
    }
    
    dates = args.dates or ["2026-05-11", "2026-05-12", "2026-05-13", "2026-05-14"]
    
    print(f"--- Multi-Day Test: {args.symbol} ---")
    print(f"Params: {json.dumps(params, indent=2)}")
    print("-" * 40)
    
    results = []
    for d in dates:
        print(f"Processing {d}...", end=" ", flush=True)
        res = run_backtest_for_date(d, args.symbol, params)
        if res:
            results.append({"date": d, "pph": res["pips_per_hour"], "net": res["total_net"], "trades": res["trade_count"]})
            print(f"Done. Net: {res['total_net']} | PPH: {res['pips_per_hour']}")
        else:
            print("Failed or Data Missing.")
            
    if not results:
        print("No data processed.")
        return
        
    total_net = sum(r["net"] for r in results)
    avg_pph = sum(r["pph"] for r in results) / len(results)
    total_trades = sum(r["trades"] for r in results)
    
    print("-" * 40)
    print(f"FINAL SUMMARY ({len(results)} Days)")
    print(f"Total Net Pips: {total_net:.2f}")
    print(f"Average PPH:    {avg_pph:.2f}")
    print(f"Total Trades:   {total_trades}")
    print("-" * 40)

if __name__ == "__main__":
    main()
