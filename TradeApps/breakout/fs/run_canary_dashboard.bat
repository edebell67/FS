@echo off
echo ==============================================
echo Starting Canary Tripwire Dashboard Server...
echo ==============================================

cd /d "%~dp0"
set TRADE_VIEWER_DISABLE_WORKERS=1
start "Trade Viewer API" python trade_viewer_api.py

echo Server is spinning up in the background...
echo Waiting 5 seconds for initialization...
timeout /t 5 /nobreak >nul

echo Opening the dashboard in your default browser...
start http://localhost:5000/canary_tripwire_dashboard.html

echo Done!
