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

set "FS_DIR=%~dp0"
for %%I in ("%FS_DIR%\.") do set "FS_DIR=%%~fI"
for %%I in ("%FS_DIR%\..\..\..") do set "SOURCE_EDS_ROOT=%%~fI"
for /f "usebackq delims=" %%I in (`python -c "import json, pathlib; p=pathlib.Path(r'%FS_DIR%')/'config.json'; d=json.load(open(p, encoding='utf-8')); print(d.get('path_settings', {}).get('generated_data_root', ''))"`) do set "CFG_DATA_ROOT=%%I"
if defined CFG_DATA_ROOT (
    set "EDS_DATA_ROOT=%CFG_DATA_ROOT%"
) else if not defined EDS_DATA_ROOT (
    set "EDS_DATA_ROOT=%SOURCE_EDS_ROOT%"
)
set "PYTHON=C:\Python313\python.exe"
set "LOG_DIR=%EDS_DATA_ROOT%\TradeApps\breakout\fs\logs"
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
