# EP051 local -> hosted snapshot sync, persistent loop variant.
# Version 1.0.0 (2026-08-27).
#
# Wraps sync_to_hosted.ps1 in an infinite loop so it can run as a
# continuously-supervised job (see _one_run_single.ps1's $services array)
# instead of a Windows Scheduled Task. A single failed sync attempt is
# caught and logged so the loop keeps running rather than exiting -
# _one_run_single.ps1's auto-restart only kicks in on a real crash of this
# whole process, which we want to avoid for a routine transient publish
# failure.
#
# Usage:
#   .\sync_to_hosted_loop.ps1 -HostedUrl "https://ep051-directory.onrender.com" -SyncToken "..." -IntervalSeconds 600

param(
    [Parameter(Mandatory = $true)][string]$HostedUrl,
    [Parameter(Mandatory = $true)][string]$SyncToken,
    [int]$IntervalSeconds = 600
)

$ErrorActionPreference = 'Stop'
$scriptDir = $PSScriptRoot
$syncScript = Join-Path $scriptDir 'sync_to_hosted.ps1'

Write-Host "EP051 sync loop starting. Interval: ${IntervalSeconds}s. Target: $HostedUrl"

while ($true) {
    try {
        & $syncScript -HostedUrl $HostedUrl -SyncToken $SyncToken
    }
    catch {
        Write-Host "EP051 sync attempt failed: $($_.Exception.Message)"
    }
    Start-Sleep -Seconds $IntervalSeconds
}
