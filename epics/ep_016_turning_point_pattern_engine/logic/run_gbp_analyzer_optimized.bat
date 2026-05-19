@echo off
REM Champion Parameters for GBP - Set on 2026-05-14
REM Based on Multi-Day Backtest (May 11-14)
REM Champion Strategy: GBPAUD_C
REM Performance: 367.59 Total Net Pips (5.88 Avg PPH)
REM Parameters: H=52, M=16, L=13, Bucket=3m, Offset=0.49, TP=30

python price_frequency_pattern_analyzer_v2.py --symbol GBPAUD_C --h 52 --m 16 --l 13 --bucket 3 --offset 0.49 --tp 30.0 --cost -2.0
pause
