Source: Direct user request in this session.

Task Summary: Add `auto_archive_threshold` to the FS version of the Breakout config so it matches the DB config setting.

Context:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
- `C:\Users\edebe\eds\TradeApps\breakout\DB\config.json`

Plan:
- [x] 1. Confirm the DB config value and the matching insertion point in the FS config.
  - [x] Test: Inspect both config files around `market_update_enabled`; pass if the DB file contains `auto_archive_threshold` and the FS file does not.
  - [x] Evidence: DB config showed `"auto_archive_threshold": 5000` between `market_update_enabled` and `market_update_interval_minutes`; FS config had the same surrounding keys but no threshold entry.
- [x] 2. Add `auto_archive_threshold` to the FS config with the same value and placement used by the DB config.
  - [x] Test: Update `TradeApps\breakout\fs\config.json`; pass if the JSON contains `"auto_archive_threshold": 5000` in the expected section.
  - [x] Evidence: Added `"auto_archive_threshold": 5000` to `TradeApps\breakout\fs\config.json` immediately after `market_update_enabled`.
- [x] 3. Validate the FS config remains valid JSON.
  - [x] Test: Parse the updated FS config with PowerShell JSON conversion; pass if parsing succeeds without errors.
  - [x] Evidence: `Get-Content ... | ConvertFrom-Json | Out-Null` completed without errors.

Implementation Log:
- 2026-03-13 04:17 Europe/London: Created lifecycle task for adding `auto_archive_threshold` to the FS config.
- 2026-03-13 04:18 Europe/London: Compared the DB and FS config files and confirmed the DB config already had `auto_archive_threshold: 5000` while the FS config was missing it.
- 2026-03-13 04:18 Europe/London: Updated `TradeApps\breakout\fs\config.json` to add `"auto_archive_threshold": 5000` in the same location used by the DB config.
- 2026-03-13 04:18 Europe/London: Parsed the updated FS config with PowerShell JSON conversion to verify syntax.

Changes Made:
- Updated `TradeApps\breakout\fs\config.json` to include `"auto_archive_threshold": 5000`.

Validation:
- `Select-String -Path 'C:\Users\edebe\eds\TradeApps\breakout\fs\config.json' -Pattern 'auto_archive_threshold'`
  - Result: Found `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json:39:"auto_archive_threshold": 5000,`
- `Get-Content 'C:\Users\edebe\eds\TradeApps\breakout\fs\config.json' -Raw | ConvertFrom-Json | Out-Null`
  - Result: Passed with no errors.

Risks/Notes:
- This change only adds the config key to the FS JSON file; it does not modify runtime code paths.

Completion Status:
- Complete - 2026-03-13 04:18 Europe/London
