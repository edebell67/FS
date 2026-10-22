# EP051 local SQL Server -> local Postgres (tradedb) snapshot sync.
# Version 1.0.0 (2026-09-15).
#
# INTERIM FIX, not the real one  -  see workstream/100_backlog/general/
# 20260915_104529_ep049_999_late_day_riser_intelligence_broken.md. EP049's
# Postgres tradedb (directory_snapshot/directory_strategy/directory_return_series/
# directory_current/directory_intelligence_profile) is a downstream copy of SQL
# Server, kept fresh only when this runs. The proper fix is a Postgres FDW view
# straight into SQL Server, eliminating this duplication entirely  -  this script
# should be retired once that ships.
#
# The live EP051 instance on :8012 is SQL-Server-direct (DATA_BACKEND=sqlserver,
# no Postgres wired up) and cannot receive a publish, so this script starts a
# throwaway Postgres-backed instance of the same app on a scratch port purely to
# receive the publish, then kills it  -  :8012, :8013 (EP049) and :8056 (the Arena)
# are never touched.
#
# Usage:
#   .\sync_to_local_postgres.ps1
#   .\sync_to_local_postgres.ps1 -Port 8095
#
# Prerequisites (User environment variables, already set for the existing
# EP049/EP051 launcher scripts  -  see ep049_start_strategy_intelligence.ps1):
#   EP051_SYNC_TOKEN        - sync token, must match app/config.py's sync_token
#   EP049_DATABASE_PASSWORD - Postgres password for role ep049_runtime

param(
    [int]$Port = 8095,
    [int]$TimeoutSeconds = 90
)

$ErrorActionPreference = 'Stop'

$repoRoot = 'C:\Users\edebe\eds\epics\ep_051_strategy_directory'
$hostedDirectory = Join-Path $repoRoot 'hosted_directory'
$pythonExe = 'C:\Python313\python.exe'
$psqlExe = 'C:\Program Files\PostgreSQL\17\bin\psql.exe'

if (-not (Test-Path (Join-Path $hostedDirectory 'app\main.py'))) {
    throw "EP051 application not found at $hostedDirectory"
}

$syncToken = [Environment]::GetEnvironmentVariable('EP051_SYNC_TOKEN', 'User')
$dbPassword = [Environment]::GetEnvironmentVariable('EP049_DATABASE_PASSWORD', 'User')
if ([string]::IsNullOrWhiteSpace($syncToken)) { throw 'EP051_SYNC_TOKEN is not configured (User environment variable).' }
if ([string]::IsNullOrWhiteSpace($dbPassword)) { throw 'EP049_DATABASE_PASSWORD is not configured (User environment variable).' }

$snapshotDir = Join-Path $repoRoot 'deploy\release'
if (-not (Test-Path $snapshotDir)) { New-Item -ItemType Directory -Force -Path $snapshotDir | Out-Null }
$timestamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
$snapshotPath = Join-Path $snapshotDir "snapshot_localsync_$timestamp.json"

$tempProc = $null
$publishSucceeded = $false
try {
    # --- 1. Export a fresh snapshot from SQL Server ---
    Write-Host "[1/4] Exporting snapshot from SQL Server -> $snapshotPath"
    Push-Location $hostedDirectory
    try {
        & $pythonExe -m sync.export_snapshot --output $snapshotPath --history-limit 20
        if ($LASTEXITCODE -ne 0) { throw "export_snapshot exited with code $LASTEXITCODE" }
    } finally { Pop-Location }

    # --- 2. Start a throwaway Postgres-backed instance to receive the publish ---
    $existing = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if ($existing) { throw "Port $Port is already in use (pid $($existing.OwningProcess))  -  pick a different -Port." }

    Write-Host "[2/4] Starting temporary Postgres-backed instance on port $Port"
    $databaseUrl = "postgresql://ep049_runtime:$dbPassword@localhost:5432/tradedb"
    # Start-Process has no -Environment parameter; a spawned child inherits this
    # process's environment block by default, so set it here (this whole script
    # process exits right after, so nothing leaks beyond this run).
    $env:DATA_BACKEND = 'postgres'
    $env:DATABASE_URL = $databaseUrl
    $env:SYNC_TOKEN = $syncToken
    $tempProc = Start-Process -FilePath $pythonExe `
        -ArgumentList '-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', $Port `
        -WorkingDirectory $hostedDirectory -WindowStyle Hidden -PassThru

    $healthy = $false
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        try {
            # -UseBasicParsing avoids Invoke-WebRequest hanging on the IE-engine DOM
            # parser under Windows PowerShell 5.1 when IE's first-run setup was
            # never completed - confirmed hang, the server itself answers fine.
            $resp = Invoke-WebRequest -Uri "http://127.0.0.1:$Port/healthz" -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
            if ($resp.StatusCode -eq 200) { $healthy = $true; break }
        } catch { Start-Sleep -Seconds 1 }
    }
    if (-not $healthy) { throw "Temporary instance on port $Port never became healthy within ${TimeoutSeconds}s." }

    # --- 3. Publish the snapshot into it ---
    Write-Host "[3/4] Publishing snapshot"
    Push-Location $hostedDirectory
    try {
        $publishResult = & $pythonExe -m sync.publish_snapshot $snapshotPath --url "http://127.0.0.1:$Port" --token $syncToken
        if ($LASTEXITCODE -ne 0) { throw "publish_snapshot exited with code $LASTEXITCODE" }
        Write-Host "  $publishResult"
        if ($publishResult -notmatch "'accepted': True") { throw "Publish did not report accepted=True: $publishResult" }
        $publishSucceeded = $true
    } finally { Pop-Location }
}
finally {
    # --- 4. Always stop the temporary instance, even on failure ---
    if ($tempProc -and -not $tempProc.HasExited) {
        Write-Host "[4/4] Stopping temporary instance (pid $($tempProc.Id))"
        Start-Process -FilePath 'taskkill' -ArgumentList "/PID $($tempProc.Id) /T /F" -NoNewWindow -Wait -ErrorAction SilentlyContinue | Out-Null
    }
    # Clean up the exported JSON on success only - kept on failure for debugging.
    if ($publishSucceeded -and (Test-Path $snapshotPath)) {
        Remove-Item -LiteralPath $snapshotPath -Force -ErrorAction SilentlyContinue
        Write-Host "Removed $snapshotPath"
    }
}

# --- Verify freshness directly against Postgres ---
$env:PGPASSWORD = $dbPassword
$verify = & $psqlExe -h localhost -U ep049_runtime -d tradedb -t -c `
    "SELECT snapshot_id || ' | ' || promoted_at || ' | ' || status || ' | ' || item_count FROM directory_snapshot ORDER BY promoted_at DESC LIMIT 1;"
Write-Host "Latest snapshot: $($verify.Trim())"
Write-Host "Sync complete."
