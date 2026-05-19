---
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false

Task Summary: Identify the code component(s) responsible for creating virtual trade JSON files in `TradeApps/breakout/fs/json/live/forex/<date>/virtual/` and document how `is_live_trade` is set on those files.

Context:
- Trade files follow the pattern: `vt_<timestamp>_<status>_<direction>_<product>_<strategy>_<uuid>.json`
- Sample file: `vt_20260420_010149_open_sell_GBPEUR_C_breakout_2_tp10.0_sl5.0_26c3b7ba.json`
- File contains `is_live_trade: true` despite being in a `virtual/` folder
- Investigation confirmed root cause: `virtual_trade_live_by_default` defaults to `True` from config

Destination Folder: None

Dependency: None

Plan:
- [x] 1. Search TradeApps/breakout codebase for code that writes `vt_` prefixed JSON files
  - Test: Grep for write patterns and virtual folder path references; confirm source file identified
  - Evidence: `fs/common.py:3858` — function `_create_new_v_trade()` creates the files
- [x] 2. Identify what drives `is_live_trade` value in virtual trade files
  - Test: Trace `is_live` parameter back to its source in the call chain
  - Evidence: `fs/common.py:4014` — `virtual_trade_live_by_default = config.get('virtual_trade_live_by_default', True)` — defaults to `True`
- [x] 3. Identify the entry point that calls `_create_new_v_trade`
  - Test: Grep for all call sites; confirm caller function name
  - Evidence: `fs/common.py:4056` and `4074` — called from `_manage_virtual_trades()` (line 3976) for both LONG and SHORT directions
- [x] 4. Document findings in this task file
  - Test: Findings recorded below
  - Evidence: See Changes Made section

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: manual_verification
  - Artifact: fs/common.py lines 3858, 4014, 4056, 4074
  - Objective-Proved: File creator, entry point, and is_live_trade default all identified in source
  - Status: captured

Implementation Log:
- 2026-04-20: Task created and investigated in same session.
- Grepped `is_live_trade` and `virtual` references in `fs/common.py`.
- Traced `_create_new_v_trade` calls and `virtual_trade_live_by_default` origin.

Changes Made:
No code changes — investigation only.

**Findings:**
- **File creator function**: `_create_new_v_trade()` at `fs/common.py:3858`
  - Writes `vt_<ts>_open_<direction>_<product>_<strategy>.json` into the passed `virtual_dir`
  - Sets `is_live_trade` from the `is_live` parameter (line 3928)
- **Caller / entry point**: `_manage_virtual_trades()` at `fs/common.py:3976`
  - Called for top LONG candidate (line 4056) and top SHORT candidate (line 4074)
  - Passes `virtual_trade_live_by_default` as the `is_live` argument
- **Why `is_live_trade: true` in virtual files**: Line 4014:
  ```python
  virtual_trade_live_by_default = config.get('virtual_trade_live_by_default', True)
  ```
  Default is `True`. Override requires explicit `virtual_trade_live_by_default: false` in config.
- **Duplicate guard**: Before creating, the function scans for any existing `vt_*_open_*.json` for the same product+direction and skips if found (lines 3880–3891).
- **Archive guard**: Creation is blocked if `config.get('archive', False)` is True (line 3873).

Validation:
- Grep confirmed single definition of `virtual_trade_live_by_default` at line 4014
- Grep confirmed two call sites for `_create_new_v_trade` at lines 4056 and 4074
- Both call sites pass `virtual_trade_live_by_default` as `is_live`

Risks/Notes:
- `is_live_trade: true` on virtual trades means they may be picked up by live order routing logic unless callers guard on the `virtual` folder path separately.
- Config key `virtual_trade_live_by_default` is the single toggle to change this behaviour.

Completion Status: Complete — 2026-04-20
---
