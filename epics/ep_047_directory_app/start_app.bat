@echo off
REM Business Activation Directory Platform — local dev launcher
REM Installs dependencies if needed, checks Postgres is reachable, then
REM starts the Next.js dev server on http://localhost:8140.

cd /d "%~dp0"

if not exist ".env.local" (
    echo [!] .env.local not found — copying .env.example.
    echo     Edit .env.local and set DATABASE_URL before continuing if needed.
    copy /y ".env.example" ".env.local" >nul
)

if not exist "node_modules" (
    echo [*] Installing dependencies, this only happens once...
    call npm install
    if errorlevel 1 (
        echo [X] npm install failed. See errors above.
        pause
        exit /b 1
    )
)

echo [*] Checking Postgres on localhost:5432...
"C:\Program Files\PostgreSQL\17\bin\pg_isready.exe" -h localhost -p 5432 >nul 2>&1
if errorlevel 1 (
    echo [!] Postgres does not appear to be running on localhost:5432.
    echo     Start the "postgresql-x64-17" service from Services ^(services.msc^)
    echo     and wait a minute or two — its data directory is on a network
    echo     share, so startup is slow. This launcher will continue anyway;
    echo     the app will fail to connect until Postgres is up.
    echo.
)

echo [*] Starting dev server at http://localhost:8140/directory ...
start "" http://localhost:8140/directory
call npm run dev
