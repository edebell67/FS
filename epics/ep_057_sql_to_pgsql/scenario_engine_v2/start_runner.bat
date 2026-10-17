@echo off
rem epics/ep_057_sql_to_pgsql/scenario_engine_v2/start_runner.bat - starts the virtual race runner + strategy intelligence provider on :8766.
rem VERSION HISTORY
rem v1.0.0 2026-10-17 Initial version: shares the EP052 arena's intelligence token (gitignored file) as EP057_INTELLIGENCE_TOKEN.
setlocal
set TOKEN_FILE=%~dp0..\..\ep_052_strategy_directory_agentic_trade_arena\lean_delivery\app\.credentials\ep057_intelligence_token.txt
if exist "%TOKEN_FILE%" for /f "usebackq delims=" %%T in ("%TOKEN_FILE%") do set EP057_INTELLIGENCE_TOKEN=%%T
cd /d %~dp0
python -m runner.server
