$profileDir = 'C:\Users\edebe\eds\workstream\verification\chrome_headless_profile'
if (!(Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir | Out-Null
}

$server = Start-Process python -ArgumentList 'C:\Users\edebe\eds\workstream\verification\run_kanban_test_server.py' -PassThru

try {
    Start-Sleep -Seconds 3
    & 'C:\Program Files\Google\Chrome\Application\chrome.exe' --headless --disable-gpu --disable-crash-reporter --disable-breakpad --no-first-run --no-default-browser-check --user-data-dir=$profileDir --window-size=1600,1200 --screenshot='C:\Users\edebe\eds\workstream\verification\epic_review_screen.png' 'http://127.0.0.1:8091/epic-review' | Out-Null
    if (Test-Path 'C:\Users\edebe\eds\workstream\verification\epic_review_screen.png') {
        'screenshot_created'
    } else {
        'screenshot_missing'
    }
}
finally {
    if ($server -and !$server.HasExited) {
        Stop-Process -Id $server.Id -Force
    }
}
