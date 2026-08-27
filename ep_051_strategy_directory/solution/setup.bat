@echo off
rem EP051 deterministic setup. Version 1.0.0 (2026-08-23).
setlocal
cd /d "%~dp0"
python verify_runtime.py
if errorlevel 1 exit /b 1
echo EP051 runtime verified. No network install or secret required.

