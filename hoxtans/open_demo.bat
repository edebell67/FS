@echo off
setlocal
set "SITE_DIR=%~dp0"
set "AI_DIR=C:\Users\edebe\eds\epics\ep_043_AI_native_serviceand _SEO\ai_website_assistant_framework"

where node >nul 2>nul || (
  echo Node.js 20 or later is required for the AI service.
  pause
  exit /b 1
)
where python >nul 2>nul || (
  echo Python is required for the local Hoxtans website server.
  pause
  exit /b 1
)

powershell -NoProfile -Command "try { Invoke-WebRequest -UseBasicParsing http://127.0.0.1:4310/api/health -TimeoutSec 1 ^| Out-Null; exit 0 } catch { exit 1 }"
if errorlevel 1 start "Hoxtans AI Service" /min /D "%AI_DIR%" node src/server.js

powershell -NoProfile -Command "try { Invoke-WebRequest -UseBasicParsing http://127.0.0.1:4321/index.html -TimeoutSec 1 ^| Out-Null; exit 0 } catch { exit 1 }"
if errorlevel 1 start "Hoxtans AI Website" /min /D "%SITE_DIR%" python -m http.server 4321 --bind 127.0.0.1

timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:4321/index.html"
start "" "http://127.0.0.1:4310/admin"
echo Hoxtans AI demo: http://127.0.0.1:4321/index.html
echo Demo activity dashboard: http://127.0.0.1:4310/admin
echo Assistant service: http://127.0.0.1:4310/api/health
endlocal
