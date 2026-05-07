@echo off
echo Installing dependencies for Strategy Performance View...
cd /d "%~dp0"
npm install
if %ERRORLEVEL% neq 0 (
    echo Error during npm install. Please check the logs.
    pause
    exit /b %ERRORLEVEL%
)
echo Dependencies installed successfully.
pause
