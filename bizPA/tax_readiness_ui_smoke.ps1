$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;

public static class WindowCaptureNative {
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

$frontendUrl = 'http://127.0.0.1:3002'
$readinessUrl = 'http://127.0.0.1:3002/?readinessDemo=1&tab=quarter'
$exportReadyUrl = 'http://127.0.0.1:3002/?readinessDemo=1&tab=quarter&resolvedDemoIssues=all'
$verificationRoot = 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification'
$quarterScreenshotPath = Join-Path $verificationRoot 'quarter_readiness_screen.png'
$finishNowScreenshotPath = Join-Path $verificationRoot 'finish_now_queue_zero_blockers.png'
function Wait-FrontendReady {
  param (
    [string]$Url
  )

  for ($i = 0; $i -lt 45; $i++) {
    Start-Sleep -Seconds 2
    try {
      $response = Invoke-WebRequest -UseBasicParsing $Url
      if ($response.StatusCode -eq 200) {
        return $response
      }
    } catch {
    }
  }

  throw "Frontend did not become ready on $Url"
}

function Capture-AppScreenshot {
  param (
    [string]$Url,
    [string]$OutputPath
  )

  $form = New-Object System.Windows.Forms.Form
  $form.Width = 1600
  $form.Height = 1500
  $form.StartPosition = 'Manual'
  $form.Location = New-Object System.Drawing.Point(-32000, -32000)

  $browser = New-Object System.Windows.Forms.WebBrowser
  $browser.ScriptErrorsSuppressed = $true
  $browser.ScrollBarsEnabled = $false
  $browser.Dock = [System.Windows.Forms.DockStyle]::Fill
  $form.Controls.Add($browser)
  $form.Show()
  $browser.Navigate($Url)

  $ready = $false
  for ($i = 0; $i -lt 90; $i++) {
    [System.Windows.Forms.Application]::DoEvents()
    Start-Sleep -Milliseconds 250
    if ($browser.ReadyState -eq [System.Windows.Forms.WebBrowserReadyState]::Complete) {
      $ready = $true
      break
    }
  }

  if (-not $ready) {
    $form.Close()
    throw "Embedded browser did not finish loading $Url"
  }

  Start-Sleep -Seconds 3
  [System.Windows.Forms.Application]::DoEvents()

  $bitmap = New-Object System.Drawing.Bitmap $browser.Width, $browser.Height
  $browser.DrawToBitmap($bitmap, (New-Object System.Drawing.Rectangle 0, 0, $browser.Width, $browser.Height))
  $bitmap.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)
  $bitmap.Dispose()
  $form.Close()
}

New-Item -ItemType Directory -Force -Path $verificationRoot | Out-Null

$frontendJob = Start-Job -ScriptBlock {
  Set-Location 'C:\Users\edebe\eds\bizPA\frontend'
  $env:PORT = '3002'
  npm.cmd start
}

try {
  $frontendResponse = Wait-FrontendReady -Url $readinessUrl
  Capture-AppScreenshot -Url $readinessUrl -OutputPath $quarterScreenshotPath
  Capture-AppScreenshot -Url $exportReadyUrl -OutputPath $finishNowScreenshotPath

  "READINESS_URL=$readinessUrl"
  "EXPORT_READY_URL=$exportReadyUrl"
  "FRONTEND_STATUS=$($frontendResponse.StatusCode)"
  "SCREENSHOT_QUARTER=$quarterScreenshotPath"
  "SCREENSHOT_EXPORT_READY=$finishNowScreenshotPath"
  'FRONTEND_LOG_START'
  Receive-Job $frontendJob -Keep -ErrorAction SilentlyContinue 2>&1
  'FRONTEND_LOG_END'
} finally {
  Stop-Job $frontendJob -ErrorAction SilentlyContinue | Out-Null
  Remove-Job $frontendJob -Force -ErrorAction SilentlyContinue | Out-Null
}
