@echo off
echo Testing EP017 Lead Capture Infrastructure...

echo 1. Checking API Health...
curl.exe -s http://localhost:5017/health | findstr "healthy"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] API is not running or unhealthy!
    exit /b 1
)
echo [SUCCESS] API is healthy.

echo 2. Sending Test Lead via API...
powershell -Command "Invoke-RestMethod -Uri http://localhost:5017/api/capture_lead -Method Post -Body '{\"email\": \"verify_batch@example.com\", \"page_id\": \"verify_batch_page\"}' -ContentType 'application/json'"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] API call failed!
    exit /b 1
)
echo [SUCCESS] Lead sent to API.

echo 3. Verifying Database Record...
set PGPASSWORD=admin6093
psql.exe -h 127.0.0.1 -U postgres -d bizpa -c "SELECT count(*) FROM leads_pain_points WHERE email = 'verify_batch@example.com';"
echo Note: If 'cat' error appears, check DB manually. Exit code 0 means table is reachable.

echo Infrastructure Verification Complete.
pause
