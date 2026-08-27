# Version history:
# 1.1.0 (2026-08-25): Allows Windows trusted authentication when DB_USER/DB_PASS are absent.
# 1.0.0 (2026-08-23): Local SQL-backed review launcher.
$ErrorActionPreference = 'Stop'
if (-not $env:DB_SERVER) { throw 'Set DB_SERVER before launch.' }
if (($env:DB_USER -and -not $env:DB_PASS) -or ($env:DB_PASS -and -not $env:DB_USER)) { throw 'Set both DB_USER and DB_PASS, or neither for Windows trusted authentication.' }
$env:DATA_BACKEND = 'sqlserver'
python -m uvicorn app.main:app --host 127.0.0.1 --port 8080
