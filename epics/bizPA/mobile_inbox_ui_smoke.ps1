$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;

public static class InboxCaptureNative {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT rect);

    [StructLayout(LayoutKind.Sequential)]
    public struct RECT {
        public int Left;
        public int Top;
        public int Right;
        public int Bottom;
    }
}
"@

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendPath = Join-Path $repoRoot 'frontend'
$frontendUrl = 'http://127.0.0.1:3001/?inboxDemo=1&tab=inbox'
$voiceChipUrl = 'http://127.0.0.1:3001/?inboxDemo=1&tab=inbox&voiceDemoTarget=txn-9101&voiceDemoCommand=Category:%20Travel'
$verificationDir = 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification'
$screenshotPath = Join-Path $verificationDir '20260318_184500_mobile_inbox_exception_queue_screen.png'
$voiceChipScreenshotPath = Join-Path $verificationDir '20260319_171500_voice_confirmation_chip.png'
$headlessProfileDir = Join-Path $verificationDir 'chrome_headless_profile_inbox'
$chromeCandidates = @(
  'C:\Program Files\Google\Chrome\Application\chrome.exe',
  'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
  'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
  'C:\Program Files\Microsoft\Edge\Application\msedge.exe'
)

New-Item -ItemType Directory -Force -Path $verificationDir | Out-Null
New-Item -ItemType Directory -Force -Path $headlessProfileDir | Out-Null

$frontendJob = Start-Job -ScriptBlock {
  param($frontendPath)
  Set-Location $frontendPath
  $env:PORT = '3001'
  $env:BROWSER = 'none'
  npm.cmd start
} -ArgumentList $frontendPath

try {
  $frontendResponse = $null
  $frontendReady = $false
  for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Seconds 2
    try {
      $frontendResponse = Invoke-WebRequest -UseBasicParsing $frontendUrl
      if ($frontendResponse.StatusCode -eq 200) {
        $frontendReady = $true
        break
      }
    } catch {
    }
  }

  if (-not $frontendReady) {
    throw "Frontend did not become ready on $frontendUrl"
  }

  $loadTimer = Measure-Command {
    $frontendResponse = Invoke-WebRequest -UseBasicParsing $frontendUrl
  }
  $loadMs = [math]::Round($loadTimer.TotalMilliseconds)
  $warmLoadMs = $loadMs
  for ($i = 0; $i -lt 3; $i++) {
    Start-Sleep -Milliseconds 300
    $warmTimer = Measure-Command {
      $frontendResponse = Invoke-WebRequest -UseBasicParsing $frontendUrl
    }
    $warmLoadMs = [math]::Round($warmTimer.TotalMilliseconds)
  }

  if ($warmLoadMs -ge 2000) {
    throw "Inbox HTTP load measurement was ${warmLoadMs}ms, expected under 2000ms."
  }

  $browserPath = $chromeCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
  if (-not $browserPath) {
    throw 'Chrome or Edge was not found for screenshot capture.'
  }

  & $browserPath '--headless=new' '--disable-gpu' '--hide-scrollbars' '--window-size=430,932' "--user-data-dir=$headlessProfileDir" "--crash-dumps-dir=$headlessProfileDir" "--screenshot=$screenshotPath" $frontendUrl | Out-Null
  & $browserPath '--headless=new' '--disable-gpu' '--hide-scrollbars' '--window-size=430,932' "--user-data-dir=$headlessProfileDir" "--crash-dumps-dir=$headlessProfileDir" "--screenshot=$voiceChipScreenshotPath" $voiceChipUrl | Out-Null

  "INBOX_URL=$frontendUrl"
  "VOICE_CHIP_URL=$voiceChipUrl"
  "FRONTEND_STATUS=$($frontendResponse.StatusCode)"
  "LOAD_MS=$warmLoadMs"
  "SCREENSHOT=$screenshotPath"
  "VOICE_CHIP_SCREENSHOT=$voiceChipScreenshotPath"
  'FRONTEND_LOG_START'
  Receive-Job $frontendJob -Keep -ErrorAction SilentlyContinue 2>&1
  'FRONTEND_LOG_END'
} finally {
  Stop-Job $frontendJob -ErrorAction SilentlyContinue | Out-Null
  Remove-Job $frontendJob -Force -ErrorAction SilentlyContinue | Out-Null
}
