@echo off
echo Preparing and opening demo for Strategy Performance View...
cd /d "%~dp0"

if not exist "node_modules" (
    echo node_modules folder not found. Please run setup.bat first.
    pause
    exit /b 1
)

echo Starting development server...
start "WebApp Dev Server" cmd /c "npm run dev"

echo Waiting for server to start...
timeout /t 5 /nobreak

echo Opening browser to http://localhost:3000...
start http://localhost:3000

echo Demo started.
pause
