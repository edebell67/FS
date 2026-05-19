## Task

Remove `auto_select_modes` and `auto_select_permitted_types` from `TradeApps\breakout\fs\config.json`.

## Context

- Target file: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
- User confirmed these auto-select config keys must not exist in the file.

## Progress Log

### 2026-04-09 01:48:00

- Confirmed `auto_select_modes` and `auto_select_permitted_types` are currently present in `config.json`.
- Proceeding to remove both keys and then validate the resulting JSON.

## Validation

- `Get-Content -Raw C:\Users\edebe\eds\TradeApps\breakout\fs\config.json | ConvertFrom-Json | Out-Null` returned `json_ok`.
- `Select-String` for `auto_select_delay_seconds|auto_select_modes|auto_select_permitted_types` returned no matches.
- Created commit `eb1df5b797` with message `Remove auto-select config keys`.
- Pushed `master` to GitHub successfully: `f902fded86..eb1df5b797`.
