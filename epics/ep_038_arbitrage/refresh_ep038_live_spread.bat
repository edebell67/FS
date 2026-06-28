@echo off
setlocal
cd /d "%~dp0"

REM Launch headed Chrome with CDP if it is not already available.
powershell.exe -NoProfile -Command "try { Invoke-WebRequest -UseBasicParsing http://127.0.0.1:9222/json/version | Out-Null; exit 0 } catch { exit 1 }"
if errorlevel 1 (
  echo Starting headed Chrome for eBay refresh...
  powershell.exe -NoProfile -Command "$profile='C:\Users\edebe\eds\.chrome-ep038-ebay'; New-Item -ItemType Directory -Force -Path $profile | Out-Null; Start-Process 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList @('--remote-debugging-port=9222','--user-data-dir=' + $profile,'--new-window','https://www.ebay.co.uk/')"
  timeout /t 5 >nul
)

echo Capturing live eBay spread snapshot...
node scripts\capture_ebay_live_spread_snapshot.js
if errorlevel 1 goto :fail

echo Applying snapshot to EP038 board...
python scripts\apply_ebay_live_spread_snapshot.py
if errorlevel 1 goto :fail

echo Starting local EP038 server...
start "EP038 local server" /min python -m http.server 8765 --bind 127.0.0.1 -d site_launch
timeout /t 2 >nul
start "" "http://127.0.0.1:8765/live-spreads.html"

echo Done. Board refreshed.
goto :eof

:fail
echo Refresh failed.
exit /b 1
