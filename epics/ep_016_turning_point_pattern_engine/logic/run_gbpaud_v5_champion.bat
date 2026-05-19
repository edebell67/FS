@echo off
REM GBPAUD V5 CHAMPION (INSTITUTIONAL QUALITY) - Set on 2026-05-16
REM Based on May 14th Capture (Optimized via 10k Sweep)
REM Performance: 8.36 Pips-Per-Hour
REM Efficiency: 7.43 Pips-Per-Trade (Exceeded 6.0 PPT Goal)

cd /d %~dp0
python price_frequency_pattern_analyzer_v2.py --symbol GBPAUD_C --h 29 --m 24 --l 19 --bucket 10 --offset 0.01 --cost -2.0
pause
