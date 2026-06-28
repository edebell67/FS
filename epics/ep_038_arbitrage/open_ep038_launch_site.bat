@echo off
setlocal
cd /d "%~dp0site_launch"
where py >nul 2>nul
if %errorlevel%==0 (
  start "EP038 local server" /min py -3 -m http.server 8765 --bind 127.0.0.1
) else (
  start "EP038 local server" /min python -m http.server 8765 --bind 127.0.0.1
)
timeout /t 2 >nul
start "" "http://127.0.0.1:8765/index.html"
endlocal
