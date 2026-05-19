@echo off
REM EPIC 016 PRICE CAPTURE DAEMON - Set on 2026-05-16
REM Responsibility: Generate _price_capture.jsonl independently of analyzers.
REM Interval: 5.0 seconds.

cd /d %~dp0
python price_capture_daemon.py
pause
