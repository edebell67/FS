# Breakout FS Add Crypto Price Endpoint To Sim Config

## Metadata
- Project: breakout
- Task: add crypto price endpoint to FS sim config
- Status: Complete
- Owner: Codex
- Started: 2026-03-15 10:59:00

## Request
Add `http://127.0.0.1:8002/api/vw_000_crypto_quotes` to the FS `sim` endpoints list.

## Plan
1. Update `TradeApps/breakout/fs/config.json` to include the crypto endpoint under `endpoints.sim`.
2. Validate JSON parsing after the change.
3. Record the result and complete the lifecycle file.

## Execution Log
### 2026-03-15 10:59:00
- Created lifecycle record.
- Preparing to patch `TradeApps/breakout/fs/config.json`.

### 2026-03-15 11:00:00
- Added `http://127.0.0.1:8002/api/vw_000_crypto_quotes` to `endpoints.sim` in `TradeApps/breakout/fs/config.json`.
- Validated the JSON file with PowerShell `ConvertFrom-Json`.

## Validation
```powershell
Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\config.json | ConvertFrom-Json | Out-Null
Select-String -Path C:\Users\edebe\eds\TradeApps\breakout\fs\config.json -Pattern 'vw_000_crypto_quotes'
```

## Result
- JSON parse passed.
- Crypto quote endpoint is now present in both `endpoints.live` and `endpoints.sim`.
