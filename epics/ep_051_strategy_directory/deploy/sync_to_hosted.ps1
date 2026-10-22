# EP051 local -> hosted snapshot sync.
# Version 1.1.0 (2026-09-07): Passes --history-limit 20 to export_snapshot.py.
#   Hosted's /finalize has a real capacity ceiling somewhere between 37.7MB
#   and 76MB of staged payload (confirmed empirically 2026-09-06/07, see
#   agent_board/board.jsonl topic ep051_render_deployment) - a full
#   2000-strategy export (up to 1000 trades/strategy) exceeds it and
#   finalize fails every time, which is why every automated sync cycle had
#   been silently failing since 2026-09-06 despite this loop running -
#   export_snapshot.py itself always succeeded, only publish_snapshot.py's
#   /finalize call ever failed, and this script's error handling (see the
#   loop wrapper) just logs the failure and waits for the next cycle
#   instead of stopping, so it kept quietly retrying and failing for over
#   14 hours. This is an EXPLICIT INTERIM WORKAROUND, not a permanent
#   product decision (Hermes flagged on 2026-09-06 that permanently
#   reducing history depth needs one) - each strategy's trade history on
#   hosted is capped at its most recent 20 trades instead of the normal
#   up to 1000, until a proper streamed/incremental /finalize design ships.
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

$timestamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
$snapshotPath = Join-Path $snapshotDir "snapshot_$timestamp.json"

Push-Location $hostedDirectory
try {
    Write-Host "Exporting local snapshot to $snapshotPath ..."
    python -m sync.export_snapshot --output $snapshotPath --history-limit 20
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
