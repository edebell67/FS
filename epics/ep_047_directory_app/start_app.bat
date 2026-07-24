@echo off
REM Business Activation Directory Platform - one-click local launcher.
REM Installs dependencies if needed, starts Postgres if it isn't running,
REM waits for it to actually accept connections, applies any pending
REM migrations, then starts the dev server and opens the browser.

cd /d "%~dp0"

if not exist ".env.local" (
    echo [!] .env.local not found - copying .env.example.
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

set "PG_ISREADY=C:\Program Files\PostgreSQL\17\bin\pg_isready.exe"

echo [*] Checking Postgres on localhost:5432...
"%PG_ISREADY%" -h localhost -p 5432 >nul 2>&1
if not errorlevel 1 goto :pg_ready

echo [*] Postgres is not responding - attempting to start the service...
echo     (its data directory is on a network share, so this can take a
echo      couple of minutes; this window will wait for it)
net start postgresql-x64-17 >nul 2>&1
REM net start needs an elevated shell - if this isn't one, the command
REM above fails silently and we just fall through to polling below in case
REM someone started it manually via Services at the same time.

set /a "PG_WAIT_ELAPSED=0"
:pg_wait_loop
"%PG_ISREADY%" -h localhost -p 5432 >nul 2>&1
if not errorlevel 1 goto :pg_ready
if %PG_WAIT_ELAPSED% GEQ 120 goto :pg_timeout
timeout /t 5 /nobreak >nul
set /a "PG_WAIT_ELAPSED+=5"
echo     ...still waiting (%PG_WAIT_ELAPSED%s)
goto :pg_wait_loop

:pg_timeout
echo.
echo [!] Postgres still isn't responding after 2 minutes.
echo     Open Services (services.msc), find "postgresql-x64-17", right-click
echo     it and choose Start - this window is not elevated, so it can't do
echo     that for you. Once it's running, re-run this script.
echo.
pause
exit /b 1

:pg_ready
echo [*] Postgres is up.

echo [*] Applying any pending database migrations...
call npm run db:migrate
if errorlevel 1 (
    echo [X] Migration failed. See errors above.
    pause
    exit /b 1
)

echo.
echo [*] Starting dev server...
echo     Public site : http://localhost:8140/directory
echo     Admin login : http://localhost:8140/directoryadmin/login
echo     (no admin user yet? run: npm run auth:create-admin)
echo.
start "" http://localhost:8140/directory
call npm run dev
