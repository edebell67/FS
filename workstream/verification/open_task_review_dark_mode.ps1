$root = "C:\Users\edebe\eds"
$appScript = Join-Path $root "workstream\apps\task_review\app.py"
$url = "http://127.0.0.1:8765/?theme=dark"

Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$root'; python '$appScript'"
Start-Sleep -Seconds 3
Start-Process $url
