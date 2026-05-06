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
}
"@

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendUrl = 'http://127.0.0.1:19011/business_entity_deep_dive_preview.html?entity=invoice'
$screenshotPath = 'C:\Users\edebe\eds\workstream\verification\20260311_220500_bizpa_entity_deep_dive_invoice.png'
$chromeProfilePath = 'C:\Users\edebe\eds\workstream\verification\chrome_capture_profile_entity_deep_dive'
$frontendLogPath = 'C:\Users\edebe\eds\workstream\verification\entity_deep_dive_ui_smoke_http_server.log'
$frontendErrorLogPath = 'C:\Users\edebe\eds\workstream\verification\entity_deep_dive_ui_smoke_http_server.err.log'
$frontendProcess = $null

New-Item -ItemType Directory -Force -Path $chromeProfilePath | Out-Null

$frontendProcess = Start-Process -FilePath 'python' `
  -ArgumentList @('-m', 'http.server', '19011', '--directory', $repoRoot) `
  -WorkingDirectory $repoRoot `
  -RedirectStandardOutput $frontendLogPath `
  -RedirectStandardError $frontendErrorLogPath `
  -PassThru `
  -WindowStyle Hidden

try {
  $frontendResponse = $null
  $frontendReady = $false
  for ($i = 0; $i -lt 20; $i++) {
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

  $chromeArgs = @(
    "--user-data-dir=$chromeProfilePath",
    '--new-window',
    '--window-size=1520,1440',
    '--no-first-run',
    '--disable-session-crashed-bubble',
    '--disable-infobars',
    '--disable-breakpad',
    '--disable-crash-reporter',
    '--noerrdialogs',
    "--app=$frontendUrl"
  )

  $chrome = Start-Process 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList $chromeArgs -PassThru
  Start-Sleep -Seconds 8
  $chromeWindow = $null
  for ($i = 0; $i -lt 10; $i++) {
    $chromeWindow = Get-Process chrome -ErrorAction SilentlyContinue |
      Where-Object { $_.MainWindowHandle -ne 0 -and $_.MainWindowTitle -like '*bizPA Entity Deep Dive*' } |
      Select-Object -First 1
    if ($chromeWindow) {
      break
    }
    Start-Sleep -Seconds 1
  }

  if ($chromeWindow) {
    [WindowCaptureNative]::ShowWindow($chromeWindow.MainWindowHandle, 3) | Out-Null
    [WindowCaptureNative]::SetForegroundWindow($chromeWindow.MainWindowHandle) | Out-Null
    Start-Sleep -Seconds 1
  }

  $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
  $bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
  $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
  $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
  $bitmap.Save($screenshotPath, [System.Drawing.Imaging.ImageFormat]::Png)
  $graphics.Dispose()
  $bitmap.Dispose()

  if ($chrome -and -not $chrome.HasExited) {
    Stop-Process -Id $chrome.Id -Force -ErrorAction SilentlyContinue
  }

  "ENTITY_DEEP_DIVE_URL=$frontendUrl"
  "FRONTEND_STATUS=$($frontendResponse.StatusCode)"
  "SCREENSHOT=$screenshotPath"
} finally {
  if ($chrome -and -not $chrome.HasExited) {
    Stop-Process -Id $chrome.Id -Force -ErrorAction SilentlyContinue
  }
  if ($frontendProcess -and -not $frontendProcess.HasExited) {
    Stop-Process -Id $frontendProcess.Id -Force -ErrorAction SilentlyContinue
    $frontendProcess.WaitForExit()
  }
}

'FRONTEND_LOG_START'
if (Test-Path $frontendLogPath) {
  Get-Content -Path $frontendLogPath -ErrorAction SilentlyContinue
}
if (Test-Path $frontendErrorLogPath) {
  Get-Content -Path $frontendErrorLogPath -ErrorAction SilentlyContinue
}
'FRONTEND_LOG_END'
