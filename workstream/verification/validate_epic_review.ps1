$verificationDir = 'C:\Users\edebe\eds\workstream\verification'
$jsonPath = Join-Path $verificationDir 'epic_review_validation.json'
$rootHtmlPath = Join-Path $verificationDir 'kanban_root_validation.html'
$reviewHtmlPath = Join-Path $verificationDir 'epic_review_validation.html'
$screenshotPath = Join-Path $verificationDir 'epic_review_screen.png'

function Invoke-ScreenshotAttempt {
    param(
        [string]$BrowserPath,
        [string]$ProfileDir,
        [string]$Url,
        [string]$OutputPath
    )

    if (!(Test-Path $BrowserPath)) {
        return @{
            success = $false
            browser = $BrowserPath
            detail = 'browser_missing'
        }
    }

    if (!(Test-Path $ProfileDir)) {
        New-Item -ItemType Directory -Path $ProfileDir | Out-Null
    }

    $arguments = @(
        '--headless=new',
        '--disable-gpu',
        '--disable-crash-reporter',
        '--disable-breakpad',
        '--no-first-run',
        '--no-default-browser-check',
        "--user-data-dir=$ProfileDir",
        '--window-size=1600,1200',
        "--screenshot=$OutputPath",
        $Url
    )

    $stdoutPath = Join-Path $ProfileDir 'stdout.log'
    $stderrPath = Join-Path $ProfileDir 'stderr.log'
    $process = Start-Process -FilePath $BrowserPath -ArgumentList $arguments -PassThru -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath

    try {
        if (!$process.WaitForExit(15000)) {
            Stop-Process -Id $process.Id -Force
            return @{
                success = $false
                browser = $BrowserPath
                detail = 'timeout'
            }
        }
    }
    catch {
        if ($process -and !$process.HasExited) {
            Stop-Process -Id $process.Id -Force
        }
        return @{
            success = $false
            browser = $BrowserPath
            detail = $_.Exception.Message
        }
    }

    return @{
        success = (Test-Path $OutputPath)
        browser = $BrowserPath
        detail = if (Test-Path $stderrPath) { (Get-Content $stderrPath -Raw).Trim() } else { '' }
    }
}

$server = Start-Process python -ArgumentList 'C:\Users\edebe\eds\workstream\verification\run_kanban_test_server.py' -PassThru

try {
    Start-Sleep -Seconds 3

    $root = (Invoke-WebRequest -UseBasicParsing 'http://127.0.0.1:8091/').Content
    $epicReview = (Invoke-WebRequest -UseBasicParsing 'http://127.0.0.1:8091/epic-review').Content
    $epicsJson = Invoke-WebRequest -UseBasicParsing 'http://127.0.0.1:8091/api/epics' | Select-Object -ExpandProperty Content
    $modelsJson = Invoke-WebRequest -UseBasicParsing 'http://127.0.0.1:8091/api/models/status' | Select-Object -ExpandProperty Content
    $epics = $epicsJson | ConvertFrom-Json

    $firstSlug = $null
    $taskJson = ''
    if ($epics.epics.Count -gt 0) {
        $firstSlug = $epics.epics[0].slug
        $taskJson = Invoke-WebRequest -UseBasicParsing ("http://127.0.0.1:8091/api/epics/{0}/tasks" -f $firstSlug) | Select-Object -ExpandProperty Content
    }

    $root | Set-Content $rootHtmlPath
    $epicReview | Set-Content $reviewHtmlPath

    if (Test-Path $screenshotPath) {
        Remove-Item $screenshotPath -Force
    }

    $attempts = @(
        Invoke-ScreenshotAttempt -BrowserPath 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ProfileDir (Join-Path $verificationDir 'chrome_headless_profile_epic_review') -Url 'http://127.0.0.1:8091/epic-review' -OutputPath $screenshotPath
        Invoke-ScreenshotAttempt -BrowserPath 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe' -ProfileDir (Join-Path $verificationDir 'edge_headless_profile_epic_review') -Url 'http://127.0.0.1:8091/epic-review' -OutputPath $screenshotPath
    )
    $successfulAttempt = $attempts | Where-Object { $_.success } | Select-Object -First 1

    $result = [pscustomobject]@{
        RootHasEpicReviewButton = ($root -match 'Epic Review')
        EpicReviewHasBackLink = ($epicReview -match 'Back to Kanban')
        EpicReviewHasAllocateAction = ($epicReview -match 'Allocate All Accepted')
        EpicCount = $epics.epics.Count
        FirstEpicSlug = $firstSlug
        ModelsJson = $modelsJson
        TaskQuerySample = if ($taskJson) { $taskJson.Substring(0, [Math]::Min(400, $taskJson.Length)) } else { '' }
        ScreenshotExists = (Test-Path $screenshotPath)
        ScreenshotBrowser = if ($successfulAttempt) { $successfulAttempt.browser } else { $null }
        ScreenshotAttempts = $attempts
    }

    $json = $result | ConvertTo-Json -Depth 6
    $json | Set-Content $jsonPath
    $json
}
finally {
    if ($server -and !$server.HasExited) {
        Stop-Process -Id $server.Id -Force
    }
}
