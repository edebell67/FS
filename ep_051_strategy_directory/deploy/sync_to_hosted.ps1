# EP051 local -> hosted snapshot sync.
# Version 1.0.0 (2026-08-27).
#
# Wraps hosted_directory/sync/export_snapshot.py + publish_snapshot.py into
# one call, for registering as a Windows Scheduled Task (e.g. every 10
# minutes, matching the cadence of the existing local runtime cache
# refresh). Run manually first to confirm it works before scheduling.
#
# Usage:
#   .\sync_to_hosted.ps1 -HostedUrl "https://ep051-directory.onrender.com" -SyncToken "..."
#
# Prerequisites:
#   - hosted_directory/.env configured for the LOCAL backend (DATA_BACKEND=
#     sqlserver, DB_SERVER, etc.) so export_snapshot.py can read local trade
#     data. This script does not modify or read that file directly; it lets
#     app/config.py pick it up via the working directory below.
#   - SyncToken must match the SYNC_TOKEN configured on the hosted Render
#     service (see deploy/render.yaml / deploy/render_deploy_package.md).
#   - Python environment with hosted_directory/requirements.txt installed
#     and importable as `python -m sync....` (run from hosted_directory/).

param(
    [Parameter(Mandatory = $true)][string]$HostedUrl,
    [Parameter(Mandatory = $true)][string]$SyncToken,
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'

$hostedDirectory = Join-Path $RepoRoot 'hosted_directory'
if (-not (Test-Path $hostedDirectory)) {
    throw "hosted_directory not found under $RepoRoot"
}

$snapshotDir = Join-Path $RepoRoot 'deploy\release'
if (-not (Test-Path $snapshotDir)) { New-Item -ItemType Directory -Force -Path $snapshotDir | Out-Null }

$timestamp = Get-Date -AsUTC -Format 'yyyyMMddTHHmmssZ'
$snapshotPath = Join-Path $snapshotDir "snapshot_$timestamp.json"

Push-Location $hostedDirectory
try {
    Write-Host "Exporting local snapshot to $snapshotPath ..."
    python -m sync.export_snapshot --output $snapshotPath
    if ($LASTEXITCODE -ne 0) { throw "export_snapshot.py failed with exit code $LASTEXITCODE" }

    Write-Host "Publishing snapshot to $HostedUrl ..."
    python -m sync.publish_snapshot $snapshotPath --url $HostedUrl --token $SyncToken
    if ($LASTEXITCODE -ne 0) { throw "publish_snapshot.py failed with exit code $LASTEXITCODE" }

    Write-Host "Sync complete."
}
finally {
    Pop-Location
}

# Keep only the most recent 50 local snapshot exports so deploy/release
# doesn't grow unbounded under a 10-minute schedule.
Get-ChildItem -Path $snapshotDir -Filter 'snapshot_*.json' |
    Sort-Object LastWriteTime -Descending |
    Select-Object -Skip 50 |
    Remove-Item -Force
