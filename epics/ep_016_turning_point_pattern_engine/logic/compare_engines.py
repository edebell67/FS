import json
from pathlib import Path
from backtest_legacy import LegacyBacktester
from backtest_gbp_analyzer import GBPBacktester

data_path = r"X:\eds\TradeApps\breakout\fs\json\live\forex\2026-05-14\_price_capture.jsonl"
symbol = "GBPAUD_C"
params = {
    "conf_high": 80, "conf_med": 29, "conf_low": 19,
    "price_offset": -0.5, "fixed_tp": 50.0, "fixed_sl": None,
    "bucket_minutes": 5, "round_turn_cost": -2.0, "mild_threshold": 5, "accumulation": 1
}

print("Running Legacy Backtest...")
bt_leg = LegacyBacktester(data_path, symbol, params)
bt_leg.load_data()
res_leg = bt_leg.run_simulation()
print(f"Legacy Result: PPH={res_leg['pips_per_hour']}, Trades={res_leg['trade_count']}, Net={res_leg['total_net']}")

print("\nRunning Optimized Backtest...")
bt_opt = GBPBacktester(data_path, symbol, params)
bt_opt.load_data()
res_opt = bt_opt.run_simulation()
print(f"Optimized Result: PPH={res_opt['pips_per_hour']}, Trades={res_opt['trade_count']}, Net={res_opt['total_net']}")

if res_leg['pips_per_hour'] != res_opt['pips_per_hour']:
    print("\n[DISCREPANCY DETECTED]")
else:
    print("\n[RESULTS MATCH]")
