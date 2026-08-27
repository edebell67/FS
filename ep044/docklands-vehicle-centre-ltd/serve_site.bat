@echo off
setlocal
cd /d "%~dp0"
set PORT=4174
echo Serving auto garage demo template at http://localhost:%PORT%/
python -m http.server %PORT%
