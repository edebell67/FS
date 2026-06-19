@echo off
python backtest_gbp_analyzer.py --data "X:\eds\TradeApps\breakout\fs\json\live\forex\2026-05-18\_price_capture.jsonl" --symbol GBP --conf_high 29 --conf_med 17 --conf_low 4 --bucket_minutes 3 --price_offset 1.00 --fixed_tp 20.0 --fixed_sl 10.0 --round_turn_cost -2.0
pause
