function Get-TaskMetadata {
    param(
        [Parameter(Mandatory = $true)]
        [string]$TaskPath
    )

    $content = Get-Content -Path $TaskPath -Raw

    $priority = 3
    if ($content -match '(?im)^\s*Priority:\s*([1-3])\s*$') {
        $priority = [int]$matches[1]
    }

    $epic = ''
    if ($content -match '(?im)^\*\*Epic:\*\*\s*(.+?)\s*$') {
        $epic = $matches[1].Trim()
    }

    $epicSequence = ''
    if ($content -match '(?im)^\*\*Epic Sequence:\*\*\s*(.+?)\s*$') {
        $epicSequence = $matches[1].Trim()
    }

    $dependsOn = @()
    if ($content -match '(?ims)^\*\*Depends On:\*\*\s*(.+?)(?=\r?\n\*\*|\r?\n##|\r?\n---|\z)') {
        $dependsRaw = $matches[1].Trim()
        if ($dependsRaw -and $dependsRaw.ToLowerInvariant() -ne 'none') {
            $dependsOn = $dependsRaw -split '[,\r\n]+' |
                ForEach-Object { $_.Trim() } |
                ForEach-Object { $_ -replace '^[\-\*\s]+', '' } |
                ForEach-Object { $_ -replace '[`"]', '' } |
                Where-Object { $_ -and $_.ToLowerInvariant() -ne 'none' }
        }
    }

    $readiness = ''
    if ($content -match '(?im)^\*\*Readiness:\*\*\s*(.+?)\s*$') {
        $readiness = $matches[1].Trim().ToLowerInvariant()
    }

    $suggestedAgent = ''
    if ($content -match '(?im)^\*\*Suggested Agent:\*\*\s*(.+?)\s*$') {
        $suggestedAgent = $matches[1].Trim().ToLowerInvariant()
    }

    $lane = ''
    $parent = Split-Path -Parent $TaskPath
    if ($parent) {
        $lane = (Split-Path -Leaf $parent).Trim().ToLowerInvariant()
        if ($lane -notin @('gemini', 'codex', 'claude', 'general')) {
            $lane = ''
        }
    }

    $majorLayer = 0
    if ($epicSequence -match '^(\d+)') {
        $majorLayer = [int]$matches[1]
    }

    [PSCustomObject]@{
        TaskPath = $TaskPath
        Content = $content
        Priority = $priority
        Epic = $epic
        EpicSequence = $epicSequence
        DependsOn = $dependsOn
        Readiness = $readiness
        SuggestedAgent = $suggestedAgent
        Lane = $lane
        MajorLayer = $majorLayer
        SequenceSortKey = ConvertTo-SequenceSortKey -Sequence $epicSequence
    }
}

function ConvertTo-SequenceSortKey {
    param(
        [string]$Sequence
    )

    if ([string]::IsNullOrWhiteSpace($Sequence)) {
        return '999999'
    }

    $parts = $Sequence -split '\.'
    $normalized = foreach ($part in $parts) {
        if ($part -match '^\d+$') {
            '{0:D6}' -f [int]$part
        }
        else {
            '999999'
        }
    }

    ($normalized -join '.')
}

function Get-TaskState {
    param(
        [Parameter(Mandatory = $true)]
        [string]$TaskPath,
        [Parameter(Mandatory = $true)]
        [string]$TodoRoot,
        [Parameter(Mandatory = $true)]
        [string]$WorkingRoot,
        [Parameter(Mandatory = $true)]
        [string]$CompleteRoot
    )

    if ($TaskPath.StartsWith($CompleteRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        return 'complete'
    }
    if ($TaskPath.StartsWith($WorkingRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        return 'in_progress'
    }
    if ($TaskPath.StartsWith($TodoRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        return 'todo'
    }
    return 'unknown'
}

function Get-StructuredTaskFiles {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RootPath
    )

    $folders = @(
        $RootPath,
        (Join-Path $RootPath 'gemini'),
        (Join-Path $RootPath 'codex'),
        (Join-Path $RootPath 'claude'),
        (Join-Path $RootPath 'general')
    )

    $files = foreach ($folder in $folders) {
        if (Test-Path $folder) {
            Get-ChildItem -Path $folder -File -Filter *.md -ErrorAction SilentlyContinue
        }
    }

    @($files)
}

function Get-InProgressTaskCount {
    param(
        [Parameter(Mandatory = $true)]
        [string]$WorkingRoot
    )

    if (-not (Test-Path $WorkingRoot)) {
        return 0
    }

    $files = Get-StructuredTaskFiles -RootPath $WorkingRoot
    return @($files).Count
}

function Get-TaskDatePrefix {
    param(
        [string]$FileName
    )

    if ([string]::IsNullOrWhiteSpace($FileName)) {
        return $null
    }

    if ($FileName -match '^(?<date>\d{8})') {
        return $matches['date']
    }

    return $null
}

function Get-InProgressTaskCountForDate {
    param(
        [Parameter(Mandatory = $true)]
        [string]$WorkingRoot,
        [string]$DatePrefix
    )

    if (-not (Test-Path $WorkingRoot)) {
        return 0
    }

    $files = Get-StructuredTaskFiles -RootPath $WorkingRoot

    if ([string]::IsNullOrWhiteSpace($DatePrefix)) {
        return Get-InProgressTaskCount -WorkingRoot $WorkingRoot
    }

    $filtered = $files | Where-Object { $_.Name -like "$DatePrefix*" }
    return @($filtered).Count
}

function Get-AllEpicTasks {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Epic,
        [Parameter(Mandatory = $true)]
        [string]$TodoRoot,
        [Parameter(Mandatory = $true)]
        [string]$WorkingRoot,
        [Parameter(Mandatory = $true)]
        [string]$CompleteRoot
    )

    $roots = @($TodoRoot, $WorkingRoot, $CompleteRoot)
    $files = foreach ($root in $roots) {
        if (Test-Path $root) {
            Get-StructuredTaskFiles -RootPath $root
        }
    }

    $epicTasks = foreach ($file in $files) {
        $metadata = Get-TaskMetadata -TaskPath $file.FullName
        if ($metadata.Epic -eq $Epic) {
            [PSCustomObject]@{
                File = $file
                Metadata = $metadata
                State = Get-TaskState -TaskPath $file.FullName -TodoRoot $TodoRoot -WorkingRoot $WorkingRoot -CompleteRoot $CompleteRoot
            }
        }
    }

    @($epicTasks)
}

function Update-TaskReadiness {
    param(
        [Parameter(Mandatory = $true)]
        [string]$TaskPath,
        [Parameter(Mandatory = $true)]
        [ValidateSet('ready', 'blocked')]
        [string]$Readiness,
        [string]$Reason
    )

    $content = Get-Content -Path $TaskPath -Raw
    $updated = $content

    if ($updated -match '(?im)^\*\*Readiness:\*\*\s*.+$') {
        $updated = [regex]::Replace($updated, '(?im)^\*\*Readiness:\*\*\s*.+$', "**Readiness:** $Readiness", 1)
    }
    else {
        $updated = [regex]::Replace($updated, '(?im)^(\*\*Depends On:\*\*.+)$', "`$1`r`n**Readiness:** $Readiness", 1)
    }

    if ($Reason) {
        if ($updated -match '(?im)^Blocked Reason:\s*$') {
            $updated = [regex]::Replace(
                $updated,
                '(?ims)^Blocked Reason:\s*$(?:\r?\n(?:- .*)?)*',
                "Blocked Reason:`r`n- $Reason`r`n",
                1
            )
        }
        else {
            $updated += "`r`nBlocked Reason:`r`n- $Reason`r`n"
        }
    }

    if ($updated -ne $content) {
        Set-Content -Path $TaskPath -Value $updated -Encoding utf8
    }
}

function Test-TaskRunnable {
    param(
        [Parameter(Mandatory = $true)]
        [string]$TaskPath,
        [Parameter(Mandatory = $true)]
        [string]$TodoRoot,
        [Parameter(Mandatory = $true)]
        [string]$WorkingRoot,
        [Parameter(Mandatory = $true)]
        [string]$CompleteRoot
    )

    $metadata = Get-TaskMetadata -TaskPath $TaskPath
    $reasons = @()

    if ([string]::IsNullOrWhiteSpace($metadata.Epic)) {
        return [PSCustomObject]@{
            Runnable = $true
            Metadata = $metadata
            Reasons = @()
        }
    }

    $epicTasks = Get-AllEpicTasks -Epic $metadata.Epic -TodoRoot $TodoRoot -WorkingRoot $WorkingRoot -CompleteRoot $CompleteRoot

    if ($metadata.MajorLayer -gt 1) {
        $incompleteLowerLayers = $epicTasks |
            Where-Object {
                $_.Metadata.TaskPath -ne $TaskPath -and
                $_.Metadata.MajorLayer -gt 0 -and
                $_.Metadata.MajorLayer -lt $metadata.MajorLayer -and
                $_.State -ne 'complete'
            }

        if ($incompleteLowerLayers) {
            $pendingLayers = ($incompleteLowerLayers |
                Select-Object -ExpandProperty Metadata |
                Select-Object -ExpandProperty EpicSequence -Unique |
                Sort-Object) -join ', '
            $reasons += "Waiting for lower epic layer completion: $pendingLayers"
        }
    }

    foreach ($dependency in $metadata.DependsOn) {
        $dependencyTask = $null

        if ($dependency -match '\.md$' -or $dependency.Contains('\') -or $dependency.Contains('/')) {
            $dependencyLeaf = Split-Path -Leaf $dependency
            $dependencyTask = $epicTasks | Where-Object {
                $_.File.Name -eq $dependencyLeaf -or $_.File.FullName -eq $dependency
            } | Select-Object -First 1
        }
        else {
            $dependencyTask = $epicTasks | Where-Object {
                $_.Metadata.EpicSequence -eq $dependency
            } | Select-Object -First 1
        }

        if ($null -eq $dependencyTask) {
            $reasons += "Dependency not found: $dependency"
            continue
        }

        if ($dependencyTask.State -ne 'complete') {
            $reasons += "Dependency not complete: $dependency"
        }
    }

    $runnable = ($reasons.Count -eq 0)

    if ($runnable -and $metadata.Readiness -eq 'blocked') {
        Update-TaskReadiness -TaskPath $TaskPath -Readiness 'ready'
    }
    elseif (-not $runnable) {
        Update-TaskReadiness -TaskPath $TaskPath -Readiness 'blocked' -Reason ($reasons -join '; ')
    }

    [PSCustomObject]@{
        Runnable = $runnable
        Metadata = (Get-TaskMetadata -TaskPath $TaskPath)
        Reasons = $reasons
    }
}

function Select-NextRunnableTask {
    param(
        [Parameter(Mandatory = $true)]
        [string]$TodoPath,
        [Parameter(Mandatory = $true)]
        [string]$TodoRoot,
        [Parameter(Mandatory = $true)]
        [string]$WorkingRoot,
        [Parameter(Mandatory = $true)]
        [string]$CompleteRoot
    )

    $tasks = Get-ChildItem -Path $TodoPath -File -Filter *.md -ErrorAction SilentlyContinue
    if (-not $tasks) {
        return $null
    }

    $candidates = foreach ($task in $tasks) {
        $metadata = Get-TaskMetadata -TaskPath $task.FullName
        [PSCustomObject]@{
            File = $task
            Metadata = $metadata
            Priority = $metadata.Priority
            MajorLayer = if ($metadata.MajorLayer -gt 0) { $metadata.MajorLayer } else { 999999 }
            SequenceSortKey = $metadata.SequenceSortKey
            Time = $task.LastWriteTime
        }
    }

    foreach ($candidate in ($candidates | Sort-Object Priority, MajorLayer, SequenceSortKey, Time)) {
        $result = Test-TaskRunnable -TaskPath $candidate.File.FullName -TodoRoot $TodoRoot -WorkingRoot $WorkingRoot -CompleteRoot $CompleteRoot
        if ($result.Runnable) {
            return $candidate.File
        }
    }

    return $null
}

function Get-WorkerPreferenceRank {
    param(
        [Parameter(Mandatory = $true)]
        [string]$WorkerName,
        [Parameter(Mandatory = $true)]
        [psobject]$Metadata
    )

    $worker = $WorkerName.Trim().ToLowerInvariant()
    $suggested = ''
    if ($null -ne $Metadata.SuggestedAgent) {
        $suggested = [string]$Metadata.SuggestedAgent
    }
    $suggested = $suggested.Trim().ToLowerInvariant()

    $lane = ''
    if ($null -ne $Metadata.Lane) {
        $lane = [string]$Metadata.Lane
    }
    $lane = $lane.Trim().ToLowerInvariant()

    if ($suggested -eq $worker) {
        return 0
    }
    if ([string]::IsNullOrWhiteSpace($suggested) -and $lane -eq $worker) {
        return 1
    }
    if ($suggested -eq 'general' -or $lane -eq 'general' -or [string]::IsNullOrWhiteSpace($lane)) {
        return 2
    }
    return 3
}

function Select-NextRunnableTaskForWorker {
    param(
        [Parameter(Mandatory = $true)]
        [string]$WorkerName,
        [Parameter(Mandatory = $true)]
        [string]$TodoRoot,
        [Parameter(Mandatory = $true)]
        [string]$WorkingRoot,
        [Parameter(Mandatory = $true)]
        [string]$CompleteRoot,
        [int]$MaxConcurrentPerDate = 3
    )

    $tasks = Get-StructuredTaskFiles -RootPath $TodoRoot

    if (-not $tasks) {
        return $null
    }

    $candidates = foreach ($task in $tasks) {
        $metadata = Get-TaskMetadata -TaskPath $task.FullName
        [PSCustomObject]@{
            File = $task
            Metadata = $metadata
            WorkerPreference = Get-WorkerPreferenceRank -WorkerName $WorkerName -Metadata $metadata
            Priority = $metadata.Priority
            MajorLayer = if ($metadata.MajorLayer -gt 0) { $metadata.MajorLayer } else { 999999 }
            SequenceSortKey = $metadata.SequenceSortKey
            Time = $task.LastWriteTime
        }
    }

    foreach ($candidate in ($candidates | Sort-Object WorkerPreference, Priority, MajorLayer, SequenceSortKey, Time)) {
        $result = Test-TaskRunnable -TaskPath $candidate.File.FullName -TodoRoot $TodoRoot -WorkingRoot $WorkingRoot -CompleteRoot $CompleteRoot
        if ($result.Runnable) {
            $datePrefix = Get-TaskDatePrefix -FileName $candidate.File.Name
            $bucketCount = Get-InProgressTaskCountForDate -WorkingRoot $WorkingRoot -DatePrefix $datePrefix
            if ($bucketCount -ge $MaxConcurrentPerDate) {
                continue
            }
            return $candidate.File
        }
    }

    return $null
}

function Claim-NextRunnableTaskForWorker {
    param(
        [Parameter(Mandatory = $true)]
        [string]$WorkerName,
        [Parameter(Mandatory = $true)]
        [string]$TodoRoot,
        [Parameter(Mandatory = $true)]
        [string]$WorkingDirectory,
        [Parameter(Mandatory = $true)]
        [string]$WorkingRoot,
        [Parameter(Mandatory = $true)]
        [string]$CompleteRoot,
        [int]$MaxConcurrentTasksPerDate = 3
    )

    $mutexName = 'Global\WorkstreamTaskClaimLock'
    $mutex = New-Object System.Threading.Mutex($false, $mutexName)
    $hasLock = $false

    try {
        $hasLock = $mutex.WaitOne(5000)
        if (-not $hasLock) {
            return $null
        }

        if (!(Test-Path $WorkingDirectory)) {
            New-Item $WorkingDirectory -ItemType Directory | Out-Null
        }

        $task = Select-NextRunnableTaskForWorker -WorkerName $WorkerName -TodoRoot $TodoRoot -WorkingRoot $WorkingRoot -CompleteRoot $CompleteRoot -MaxConcurrentPerDate $MaxConcurrentTasksPerDate
        if ($null -eq $task) {
            return $null
        }

        $workingTask = Join-Path $WorkingDirectory $task.Name
        Move-Item $task.FullName $workingTask -Force

        [PSCustomObject]@{
            OriginalTask = $task
            WorkingTaskPath = $workingTask
        }
    }
    finally {
        if ($hasLock) {
            $mutex.ReleaseMutex()
        }
        $mutex.Dispose()
    }
}

function Move-TaskToDump {
    <#
    .SYNOPSIS
        Moves a task file to the 500_dump folder without deleting it.
    .DESCRIPTION
        Archives a task by moving it from its current location to the 500_dump folder.
        Preserves the agent subfolder structure (codex, gemini, claude, general).
    .PARAMETER TaskPath
        Full path to the task file to dump.
    .PARAMETER DumpRoot
        Root path of the 500_dump folder. Defaults to C:\Users\edebe\eds\workstream\500_dump
    .EXAMPLE
        Move-TaskToDump -TaskPath "C:\Users\edebe\eds\workstream\200_inprogress\codex\task.md"
    #>
    param(
        [Parameter(Mandatory = $true)]
        [string]$TaskPath,
        [string]$DumpRoot = 'C:\Users\edebe\eds\workstream\500_dump'
    )

    if (-not (Test-Path $TaskPath)) {
        Write-Error "Task file not found: $TaskPath"
        return $null
    }

    $fileName = Split-Path -Leaf $TaskPath
    $parentDir = Split-Path -Parent $TaskPath
    $parentName = Split-Path -Leaf $parentDir

    # Determine target dump folder based on agent subfolder
    if ($parentName -in @('codex', 'gemini', 'claude', 'general')) {
        $targetDir = Join-Path $DumpRoot $parentName
    }
    else {
        $targetDir = $DumpRoot
    }

    # Create target directory if it doesn't exist
    if (-not (Test-Path $targetDir)) {
        New-Item -Path $targetDir -ItemType Directory -Force | Out-Null
    }

    $targetPath = Join-Path $targetDir $fileName

    try {
        Move-Item -Path $TaskPath -Destination $targetPath -Force
        Write-Host "Task dumped: $TaskPath -> $targetPath"
        return [PSCustomObject]@{
            OriginalPath = $TaskPath
            DumpedPath = $targetPath
            Success = $true
        }
    }
    catch {
        Write-Error "Failed to dump task: $_"
        return [PSCustomObject]@{
            OriginalPath = $TaskPath
            DumpedPath = $null
            Success = $false
            Error = $_.Exception.Message
        }
    }
}
