@echo off
REM GBP V6 REVERSAL CHAMPION (THE SPIKE KILLER) - Set on 2026-05-18
REM Strategy Discovery: Fading 3-minute momentum spikes with a +3.00 pip entry trap.
REM Performance: +1,224 pips (May 11-18 Validation).
REM DATE: 2026-05-19 RESTART

cd /d %~dp0
python price_frequency_pattern_analyzer_v2.py --symbol GBP --trade_symbol GBP --quantity 50000 --comment "SPIKE_KILLER" --h 29 --m 17 --l 4 --bucket 3 --offset 3.00 --tp 20.0 --sl 10.0 --poll 5.0 --cost -2.0 --live --flip
pause
