@echo off
SETLOCAL

REM Daily Top 3 Multi-Product Twitter Thread Poster
REM Posts the daily top 3 strategies per product type to X

set "FS_DIR=C:\Users\edebe\eds\TradeApps\breakout\fs"
set "PACKAGE_DIR=%FS_DIR%\json\live\social_posting_package"
set "RUN_DATE=%1"

if "%RUN_DATE%"=="" (
    for /f "tokens=1-3 delims=/ " %%a in ('echo %date%') do set RUN_DATE=%%c-%%a-%%b
)

echo ============================================
echo Daily Top 3 Multi-Product Twitter Thread
echo Date: %RUN_DATE%
echo ============================================
echo.

REM Check if package exists
if not exist "%PACKAGE_DIR%\%RUN_DATE%\top3_daily_posting_package.json" (
    echo [ERROR] Package not found: %PACKAGE_DIR%\%RUN_DATE%\top3_daily_posting_package.json
    echo Please generate the package first.
    pause
    exit /b 1
)

REM Check if API is running
echo [1/3] Checking API health...
curl -s http://localhost:5000/api/health >nul 2>&1
if errorlevel 1 (
    echo [INFO] API not running. Starting trade_viewer_api.py...
    start "Trade Viewer API" cmd /k "cd /d %FS_DIR% && python trade_viewer_api.py"
    echo Waiting 10 seconds for API to start...
    timeout /t 10 /nobreak >nul
)

REM Verify API is now running
curl -s http://localhost:5000/api/health >nul 2>&1
if errorlevel 1 (
    echo [ERROR] API still not available at http://localhost:5000
    echo Please start the API manually and retry.
    pause
    exit /b 1
)
echo [OK] API is running

REM Read and post the thread
echo [2/3] Posting daily top 3 thread to X...

REM Extract thread posts from JSON and post via API
python -c "import json; import urllib.request; p=json.load(open(r'%PACKAGE_DIR%\%RUN_DATE%\top3_daily_posting_package.json')); posts=[t['text'] for t in p['thread']['posts']]; req=urllib.request.Request('http://localhost:5000/api/social/x_api_thread_post',data=json.dumps({'posts':posts,'trigger':'daily_top3_multi_product'}).encode(),headers={'Content-Type':'application/json'},method='POST'); resp=urllib.request.urlopen(req,timeout=60); print(resp.read().decode())"

if errorlevel 1 (
    echo [ERROR] Failed to post thread
    pause
    exit /b 1
)

echo.
echo [3/3] Done!
echo ============================================
echo Thread posted successfully.
echo Package: %PACKAGE_DIR%\%RUN_DATE%\top3_daily_posting_package.json
echo ============================================

ENDLOCAL
pause
