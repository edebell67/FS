@echo off
REM ============================================================
REM  run_twitter_consolidated_every4h.bat
REM  [2026-04-11 09:35] V20260411_0935
REM  Launcher for the consolidated leaderboard
REM  Twitter/X workflow - runs every 4 hours via
REM  Windows Task Scheduler.
REM
REM  Triggered by task: BreakoutTwitterConsolidated4h
REM  Runner: run_twitter_consolidated_leaderboard_workflow.py
REM  Flow: verify API -> generate consolidated package -> validate payload -> post to X
REM  Data: current-date consolidated leaderboard payload
REM ============================================================
SETLOCAL

set "FS_DIR=C:\Users\edebe\eds\TradeApps\breakout\fs"
set "PYTHON=C:\Python313\python.exe"
set "LOG_DIR=%FS_DIR%\logs"
set "LOG_FILE=%LOG_DIR%\twitter_consolidated_leaderboard_4h.log"
for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set "RUN_DATE=%%I"

REM Ensure log directory exists
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Timestamp for log
echo. >> "%LOG_FILE%"
echo ============================================ >> "%LOG_FILE%"
echo [%DATE% %TIME%] Starting consolidated leaderboard 4h Twitter workflow for %RUN_DATE% >> "%LOG_FILE%"
echo ============================================ >> "%LOG_FILE%"

REM Run the workflow
"%PYTHON%" "%FS_DIR%\run_twitter_consolidated_leaderboard_workflow.py" "%RUN_DATE%" >> "%LOG_FILE%" 2>&1

if %ERRORLEVEL% EQU 0 (
    echo [%DATE% %TIME%] SUCCESS - post completed >> "%LOG_FILE%"
) else (
    echo [%DATE% %TIME%] FAILED - exit code %ERRORLEVEL% >> "%LOG_FILE%"
)

ENDLOCAL
