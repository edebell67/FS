@echo off
echo Starting development server for Strategy Performance View...
cd /d "%~dp0"

if not exist "node_modules" (
    echo node_modules folder not found. Please run setup.bat first.
    pause
    exit /b 1
)

npm run dev
if %ERRORLEVEL% neq 0 (
    echo Dev server stopped with an error.
    pause
)
