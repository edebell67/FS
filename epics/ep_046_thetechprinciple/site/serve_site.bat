@echo off
REM The Tech Principle — local preview
REM Serves this folder on http://localhost:8130 and opens it in the default browser.

cd /d "%~dp0"
start "" http://localhost:8130
python -m http.server 8130
