---
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false

Task Summary: Add a config guard to `_create_new_v_trade` in `fs/common.py` so that virtual trade file creation can be disabled via a config flag without requiring code changes.

Context:
- `_create_new_v_trade` at `fs/common.py:3858` is the sole creator of `vt_*.json` files in the `virtual/` directory
- Currently the only creation stop is `archive: true` (which triggers archiving as a side effect) or the API returning no leaders
- A dedicated `enable_virtual_trades: false` (or equivalent) config flag does not exist
- Target config file: loaded via `_load_config()` in `fs/common.py`

Destination Folder: None

Dependency: None

Plan:
- [ ] 1. Confirm the config key name to use and where `_load_config()` reads from
  - Test: Grep for `_load_config` and `CONFIG_FILE_PATH` to confirm config file path
  - Evidence:
- [ ] 2. Add early-return guard at the top of `_create_new_v_trade` that checks the config flag
  - Implementation: After the `archive` guard (line 3873), add:
    ```python
    if not _config.get('enable_virtual_trades', True):
        print(f"[V-TRADE-BLOCK] Virtual trade creation disabled via config.")
        return
    ```
  - Test: Set `enable_virtual_trades: false` in config; confirm no new `vt_` files are created on next poll cycle
  - Evidence:
- [ ] 3. Verify existing trades are unaffected (open trades continue to update, close normally)
  - Test: With `enable_virtual_trades: false`, confirm `_update_open_v_trades_prices` and close logic still run
  - Evidence:

Evidence:
Objective-Delivery-Coverage: 0%
Auto-Acceptance: false

- Evidence-Type: diff
  - Artifact: fs/common.py
  - Objective-Proved: Guard added to _create_new_v_trade
  - Status: planned
- Evidence-Type: manual_verification
  - Artifact: virtual/ directory after one poll cycle with flag set
  - Objective-Proved: No new vt_ files created when enable_virtual_trades is false
  - Status: planned

Implementation Log:
- 2026-04-21: Task created.

Changes Made: (to be populated)

Validation: (to be populated)

Risks/Notes:
- `DB/common.py:3332` has an identical `_create_new_v_trade` — if the DB code path is active it will need the same guard applied
- Setting `enable_virtual_trades: false` will stop creation but will NOT close existing open vt_ trades; a separate cleanup step may be needed if that is required
- Default is `False` — virtual trades are OFF unless `enable_virtual_trades: true` is set in config
- `DB/common.py:3332` has an identical function — same guard should be applied if DB path is active

Changes Made:
- `TradeApps/breakout/fs/common.py` — added guard after archive check in `_create_new_v_trade`:
  ```python
  if not _config.get('enable_virtual_trades', False):
      print(f"[V-TRADE-BLOCK] Virtual trade creation disabled (enable_virtual_trades=false).")
      return
  ```

Validation:
- Guard confirmed absent before change (grep returned no matches)
- Guard confirmed present after edit (grep matches line ~3876)

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false

- Evidence-Type: diff
  - Artifact: TradeApps/breakout/fs/common.py ~line 3876
  - Objective-Proved: Guard blocks _create_new_v_trade when enable_virtual_trades is false/absent
  - Status: captured

Completion Status: Complete — 2026-04-21
---
