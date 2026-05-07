@echo off
REM ============================================
REM Market Prices API - Startup Script
REM DB-free price delivery (port 8002)
REM ============================================

title Market Prices API

echo ============================================
echo MARKET PRICES API - Starting...
echo ============================================
echo.
echo Port: 8002
echo Crypto: Binance (5s interval)
echo Futures: Yahoo (30s interval)
echo Forex: Passthrough from 8001
echo.
echo Endpoints:
echo   http://127.0.0.1:8002/api/vw_000_crypto_quotes
echo   http://127.0.0.1:8002/api/vw_000_futures_quotes
echo   http://127.0.0.1:8002/api/vw_000_fx_quotes
echo   http://127.0.0.1:8002/api/health
echo.
echo Press Ctrl+C to stop
echo ============================================
echo.

cd /d C:\Users\edebe\eds\market_prices_api
python main.py

pause
