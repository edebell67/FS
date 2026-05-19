## Task

Remove the incorrectly restored `auto_select_delay_seconds` field from `TradeApps\breakout\fs\config.json` and keep `vtrade_persistence_seconds` as the intended delay field.

## Context

- Target file: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
- Follow-up to the config recovery commit `e799045c16`.
- The archived task record `C:\Users\edebe\eds\workstream\300_complete\gemini\20260407_185500_breakout_weekly_perf_auto_select_delay.md` states the implementation switched from `auto_select_delay_seconds` to `vtrade_persistence_seconds`.

## Progress Log

### 2026-04-09 01:29:12

- Confirmed `config.json` currently contains both `auto_select_delay_seconds` and `vtrade_persistence_seconds`.
- Confirmed the archived task record says the delay value should use `vtrade_persistence_seconds`.

### 2026-04-09 01:35:00

- Removed `auto_select_delay_seconds` from `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`.
- Verified `vtrade_persistence_seconds` remains present.
- Created follow-up commit `f902fded86` with message `Remove wrong auto-select delay config field`.
- Pushed `master` to GitHub successfully: `e799045c16..f902fded86`.

## Validation

- `Get-Content -Raw C:\Users\edebe\eds\TradeApps\breakout\fs\config.json | ConvertFrom-Json | Out-Null` returned `json_ok`.
- `git -C C:\Users\edebe\eds\TradeApps diff -- breakout/fs/config.json` showed only the removal of `auto_select_delay_seconds`.
- `Select-String` confirmed:
  - `auto_select_delay_seconds` is absent
  - `auto_select_modes` is present
  - `auto_select_permitted_types` is present
  - `vtrade_persistence_seconds` is present
