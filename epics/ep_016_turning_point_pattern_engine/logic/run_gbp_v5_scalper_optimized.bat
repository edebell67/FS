@echo off
REM GBP V5 SCALPER CHAMPION (GROWTH) - Set on 2026-05-16
REM Based on May 15th Capture (Refined via V5 Hill Climbing)
REM Performance: 11.61 Pips-Per-Hour
REM Efficiency: 4.20 Pips-Per-Trade (57 Trades)

cd /d %~dp0
python price_frequency_pattern_analyzer_v2.py --symbol GBP --h 20 --m 14 --l 11 --bucket 1 --offset 0.0 --cost -2.0
pause
