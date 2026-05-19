@echo off
REM GBP HEAVY CHAMPION (PRODUCTION) - Set on 2026-05-18
REM Aggressive 8-minute bucket for maximum momentum capture.
REM Frequency: Locked to 8-minute bucket starts.

cd /d %~dp0
python price_frequency_pattern_analyzer_v2.py --symbol GBP --trade_symbol GBP --quantity 50000 --comment "HEAVY" --h 70 --m 40 --l 15 --bucket 8 --offset 0.01 --tp 50.0 --poll 480.0 --cost -2.0 --live
pause
