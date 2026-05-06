@echo off
echo Building production version for Strategy Performance View...
cd /d "%~dp0"

if not exist "node_modules" (
    echo node_modules folder not found. Please run setup.bat first.
    pause
    exit /b 1
)

echo Building the application...
npm run build
if %ERRORLEVEL% neq 0 (
    echo Error during npm run build.
    pause
    exit /b %ERRORLEVEL%
)

echo Starting production server...
npm start
if %ERRORLEVEL% neq 0 (
    echo Production server stopped with an error.
    pause
)
