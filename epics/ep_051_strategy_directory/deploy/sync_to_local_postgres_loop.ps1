# EP049 local Postgres sync, persistent loop variant.
# Version 1.0.0 (2026-09-15).
#
# INTERIM FIX  -  retire once the real fix (a Postgres FDW view straight into SQL
# Server) ships; see sync_to_local_postgres.ps1's header for full context.
#
# Wraps sync_to_local_postgres.ps1 in an infinite loop so it can run as a
# continuously-supervised job (see _one_run_single.ps1's $services array),
# same pattern as sync_to_hosted_loop.ps1. A single failed sync attempt is
# caught and logged so the loop keeps running rather than exiting  - 
# _one_run_single.ps1's auto-restart only kicks in on a real crash of this
# whole process, which we want to avoid for a routine transient publish
# failure (e.g. SQL Server momentarily unreachable).
#
# Usage:
#   .\sync_to_local_postgres_loop.ps1
#   .\sync_to_local_postgres_loop.ps1 -IntervalSeconds 3600 -Port 8095

param(
    [int]$IntervalSeconds = 3600,
    [int]$Port = 8095
)

$ErrorActionPreference = 'Stop'
$scriptDir = $PSScriptRoot
$syncScript = Join-Path $scriptDir 'sync_to_local_postgres.ps1'

Write-Host "EP049 local Postgres sync loop starting. Interval: ${IntervalSeconds}s. Port: $Port"

while ($true) {
    try {
        & $syncScript -Port $Port
    }
    catch {
        Write-Host "EP049 local sync attempt failed: $($_.Exception.Message)"
    }
    Start-Sleep -Seconds $IntervalSeconds
}
