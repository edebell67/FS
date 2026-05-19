@echo off
REM GBPAUD_C CHAMPION LIVE - Optimized on 2026-05-15
REM Focus: High Yield Aggressive Scalping
REM Performance: 367.59 Pips | 75% Consistency (3/4 Days)
REM Parameters: H=52, M=16, L=13, Bucket=3m, Offset=0.49, TP=30.0
REM Trade Cost: 3.0 pips per round turn

python price_frequency_pattern_analyzer_v2.py --symbol GBPAUD_C --h 52 --m 16 --l 13 --bucket 3 --offset 0.49 --tp 30.0 --cost -3.0
pause
