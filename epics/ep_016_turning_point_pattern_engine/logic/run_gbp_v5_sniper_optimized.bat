@echo off
REM GBP V5 SNIPER CHAMPION (EFFICIENCY) - Set on 2026-05-16
REM Based on May 15th Capture (Refined via V5 Hill Climbing)
REM Performance: 8.76 Pips-Per-Hour
REM Efficiency: 6.69 Pips-Per-Trade (27 Trades)

cd /d %~dp0
python price_frequency_pattern_analyzer_v2.py --symbol GBP --h 80 --m 45 --l 4 --bucket 10 --offset -0.49 --cost -2.0
pause
