$ErrorActionPreference = 'Stop'

$frontendUrl = 'http://127.0.0.1:3001/?inboxDemo=1&tab=inbox'
$voiceChipUrl = 'http://127.0.0.1:3001/?inboxDemo=1&tab=inbox&voiceDemoTarget=txn-9101&voiceDemoCommand=Category:%20Travel'
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendPath = Join-Path $repoRoot 'frontend'

Write-Host 'Starting bizPA mobile inbox exception queue UI...' -ForegroundColor Cyan
Write-Host ''
Write-Host 'Verification URL:' -ForegroundColor Green
Write-Host "  $frontendUrl" -ForegroundColor Yellow
Write-Host 'Voice chip verification URL:' -ForegroundColor Green
Write-Host "  $voiceChipUrl" -ForegroundColor Yellow
Write-Host ''
Write-Host 'Mode:' -ForegroundColor Green
Write-Host '  Demo inbox with mobile triage controls plus a seeded voice-confirmation-chip review path.' -ForegroundColor Yellow
Write-Host ''
Write-Host 'Press Ctrl+C to stop the local UI server.' -ForegroundColor Cyan

Set-Location $frontendPath
$env:PORT = '3001'
$env:BROWSER = 'none'
npm.cmd start
