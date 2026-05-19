@echo off
REM GBP V6 UNIVERSAL CHAMPION (PRODUCTION)
REM Performance: 196.45 pips / 0.00 Drawdown

cd /d %~dp0
python price_frequency_pattern_analyzer_v2.py --symbol GBP --trade_symbol GBP --quantity 50000 --comment "EP016_V6_UNIV" --h 53 --m 20 --l 7 --bucket 15 --offset -0.35 --tp 10.0 --sl 20.0 --poll 5.0 --cost -2.0 --target_pips 100.0 --live
pause
