@echo off
REM GBP HEAVY CHAMPION - Set on 2026-05-15
REM Based on Multi-Day Backtest (May 11-14)
REM Stability: 100% (Profitable every day)
REM Performance: 235.27 Total Net Pips (Avg 4.57 PPH)
REM Parameters: H=70, M=40, L=15, Bucket=8m, Offset=0.01, TP=50

python price_frequency_pattern_analyzer_v2.py --symbol GBP --h 70 --m 40 --l 15 --bucket 8 --offset 0.01 --tp 50.0 --cost -2.0
pause
