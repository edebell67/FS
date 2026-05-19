@echo off
setlocal

set "WORKSPACE=C:\Users\edebe\eds"
set "PWSH=C:\Program Files\PowerShell\7\pwsh.exe"
set "SUPERVISOR=%WORKSPACE%\epics\ep_016_turning_point_pattern_engine\logic\ep016_run_supervisor.ps1"
set "STATE_FILE=%WORKSPACE%\workstream\logs\ep016_supervisor_state.json"
set "SUPERVISOR_LOG=%WORKSPACE%\workstream\logs\ep016_supervisor.log"

set "RUN_HOURS=%~1"
set "CHECK_INTERVAL=%~2"
if "%CHECK_INTERVAL%"=="" set "CHECK_INTERVAL=15"
set "MODE_LABEL=continuous"

if not "%RUN_HOURS%"=="" (
    if /I "%RUN_HOURS%"=="continuous" (
        set "MODE_LABEL=continuous"
    ) else (
        set "MODE_LABEL=bounded"
    )
)

if not exist "%PWSH%" (
    echo ERROR: PowerShell 7 not found at "%PWSH%"
    exit /b 1
)

if not exist "%SUPERVISOR%" (
    echo ERROR: Epic 016 supervisor not found at "%SUPERVISOR%"
    exit /b 1
)

echo Launching Epic 016 supervisor...
echo   mode=%MODE_LABEL%
if /I "%MODE_LABEL%"=="bounded" echo   run_hours=%RUN_HOURS%
echo   check_interval_seconds=%CHECK_INTERVAL%
echo   supervisor=%SUPERVISOR%

if /I "%MODE_LABEL%"=="continuous" (
    "%PWSH%" -NoLogo -NoProfile -Command ^
     "$p = Start-Process -FilePath '%PWSH%' -ArgumentList @('-NoLogo','-NoProfile','-File','%SUPERVISOR%','-Continuous','-CheckIntervalSeconds','%CHECK_INTERVAL%') -WindowStyle Hidden -PassThru; Write-Output ('supervisor_parent_pid=' + $p.Id)"
) else (
    "%PWSH%" -NoLogo -NoProfile -Command ^
     "$p = Start-Process -FilePath '%PWSH%' -ArgumentList @('-NoLogo','-NoProfile','-File','%SUPERVISOR%','-RunHours','%RUN_HOURS%','-CheckIntervalSeconds','%CHECK_INTERVAL%') -WindowStyle Hidden -PassThru; Write-Output ('supervisor_parent_pid=' + $p.Id)"
)

if errorlevel 1 (
    echo ERROR: Failed to launch Epic 016 supervisor.
    exit /b 1
)

echo.
echo Epic 016 launch requested successfully.
echo State file: %STATE_FILE%
echo Supervisor log: %SUPERVISOR_LOG%
echo.
echo Usage:
echo   start_ep016_process.bat
echo   start_ep016_process.bat continuous
echo   start_ep016_process.bat 6
echo   start_ep016_process.bat 6 15

endlocal
