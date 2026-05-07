@echo off
echo Running verification and tests for Strategy Performance View...
cd /d "%~dp0"

if not exist "node_modules" (
    echo node_modules folder not found. Please run setup.bat first.
    pause
    exit /b 1
)

echo Running lint check...
npm run lint
if %ERRORLEVEL% neq 0 (
    echo Linting issues found.
)

echo Running tests...
npm test
if %ERRORLEVEL% neq 0 (
    echo Some tests failed.
)

echo Verification complete.
pause
