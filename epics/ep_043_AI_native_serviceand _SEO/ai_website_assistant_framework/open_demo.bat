@echo off
setlocal
cd /d "%~dp0"
where node >nul 2>nul || (
  echo Node.js 20 or later is required.
  pause
  exit /b 1
)
if not exist .env copy /Y .env.example .env >nul
start "AI Website Assistant Service" /min cmd /c "npm start"
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:4310/"
start "" "http://127.0.0.1:4310/admin"
echo Demo opened. Visitor site: http://127.0.0.1:4310/
echo Admin workspace: http://127.0.0.1:4310/admin
endlocal
