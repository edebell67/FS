param(
    [int]$RunHours = 6,
    [int]$CheckIntervalSeconds = 15,
    [switch]$Continuous
)

$ErrorActionPreference = "Stop"

$workspaceRoot = "C:\Users\edebe\eds"
$logicRoot = Join-Path $workspaceRoot "epics\ep_016_turning_point_pattern_engine\logic"
$logRoot = Join-Path $workspaceRoot "workstream\logs"
$supervisorLog = Join-Path $logRoot "ep016_supervisor.log"
$statePath = Join-Path $logRoot "ep016_supervisor_state.json"

New-Item -ItemType Directory -Force -Path $logRoot | Out-Null

$workers = @(
    @{ Name = "writer"; Script = Join-Path $logicRoot "price_frequency_db_writer.py" },
    @{ Name = "turning"; Script = Join-Path $logicRoot "turning_point_processor.py" },
    @{ Name = "normalization"; Script = Join-Path $logicRoot "normalization_processor.py" },
    @{ Name = "feature"; Script = Join-Path $logicRoot "feature_processor.py" },
    @{ Name = "live"; Script = Join-Path $logicRoot "live_similarity_engine.py" },
    @{ Name = "cross"; Script = Join-Path $logicRoot "cross_product_relationship_engine.py" }
)

$runtime = [ordered]@{
    started_at = (Get-Date).ToString("s")
    run_hours = if ($Continuous) { $null } else { $RunHours }
    check_interval_seconds = $CheckIntervalSeconds
    continuous = [bool]$Continuous
    supervisor_pid = $PID
    expected_end = if ($Continuous) { $null } else { (Get-Date).AddHours($RunHours).ToString("s") }
    workers = @{}
}

function Write-SupervisorLog {
    param([string]$Message)

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $supervisorLog -Value "[$timestamp] $Message"
}

function Save-State {
    $runtime | ConvertTo-Json -Depth 6 | Set-Content -Path $statePath -Encoding utf8
}

function Start-Worker {
    param(
        [string]$Name,
        [string]$ScriptPath
    )

    $stdoutPath = Join-Path $logRoot ("ep016_{0}.out.log" -f $Name)
    $stderrPath = Join-Path $logRoot ("ep016_{0}.err.log" -f $Name)

    if (-not $runtime.workers.Contains($Name)) {
        $runtime.workers[$Name] = [ordered]@{
            script = $ScriptPath
            stdout = $stdoutPath
            stderr = $stderrPath
            restart_count = 0
            last_start = $null
            pid = $null
        }
    }

    $cmd = "Set-Location '$workspaceRoot'; python -u '$ScriptPath'"
    $process = Start-Process `
        -FilePath "C:\Program Files\PowerShell\7\pwsh.exe" `
        -ArgumentList @("-NoLogo", "-NoProfile", "-Command", $cmd) `
        -RedirectStandardOutput $stdoutPath `
        -RedirectStandardError $stderrPath `
        -WindowStyle Hidden `
        -PassThru

    $runtime.workers[$Name].pid = $process.Id
    $runtime.workers[$Name].last_start = (Get-Date).ToString("s")
    $runtime.workers[$Name].restart_count = [int]$runtime.workers[$Name].restart_count + 1

    Write-SupervisorLog "started $Name pid=$($process.Id)"
    Save-State
    return $process.Id
}

function Stop-Worker {
    param([string]$Name)

    if (-not $runtime.workers.Contains($Name)) {
        return
    }

    $workerPid = $runtime.workers[$Name].pid
    if (-not $workerPid) {
        return
    }

    $proc = Get-Process -Id $workerPid -ErrorAction SilentlyContinue
    if ($proc) {
        Stop-Process -Id $workerPid -Force
        Write-SupervisorLog "stopped $Name pid=$workerPid"
    }
}

function Ensure-Worker {
    param(
        [string]$Name,
        [string]$ScriptPath
    )

    $known = $runtime.workers[$Name]
    $workerPid = $known.pid
    $proc = $null
    if ($workerPid) {
        $proc = Get-Process -Id $workerPid -ErrorAction SilentlyContinue
    }

    if (-not $proc) {
        Write-SupervisorLog "worker $Name not running; restarting"
        Start-Worker -Name $Name -ScriptPath $ScriptPath | Out-Null
    }
}

Write-SupervisorLog "supervisor starting run_hours=$RunHours check_interval_seconds=$CheckIntervalSeconds continuous=$([bool]$Continuous)"

foreach ($worker in $workers) {
    Start-Worker -Name $worker.Name -ScriptPath $worker.Script | Out-Null
}

try {
    while ($true) {
        if (-not $Continuous) {
            $endTime = [datetime]::Parse($runtime.expected_end)
            if ((Get-Date) -ge $endTime) {
                break
            }
        }
        foreach ($worker in $workers) {
            Ensure-Worker -Name $worker.Name -ScriptPath $worker.Script
        }
        Save-State
        Start-Sleep -Seconds $CheckIntervalSeconds
    }
}
finally {
    Write-SupervisorLog "supervisor ending; stopping workers"
    foreach ($worker in $workers) {
        Stop-Worker -Name $worker.Name
    }
    Save-State
}
