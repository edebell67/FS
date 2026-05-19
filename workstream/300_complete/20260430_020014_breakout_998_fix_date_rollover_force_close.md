# Fix Date Rollover Force Close

Source: Follow-up fix from `20260430_013934_breakout_999_investigate_no_trades_generated_20260430.md` and direct user request to fix continuous fight-back using force-close functionality.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

Task Summary: Fix strategy date rollover so prior-day open trades are force-closed on the new local trading day, local/BST midnight is not treated as UTC prior-day EOD, and fresh entries can be written under the current local date folder.

Context:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\momentum.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-29`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-30`

Destination Folder: None

Dependency: `C:\Users\edebe\eds\workstream\200_inprogress\20260430_013934_breakout_999_investigate_no_trades_generated_20260430.md`

Plan:
- [x] 1. Add local trading-time handling for EOD and filenames.
  - Test: [x] Run timestamp probe for `2026-04-30T00:42+01:00`; expected pass condition is not EOD and filename/date resolves to `20260430`.
  - Evidence: Probe returned `local_0042_trading_date: 2026-04-30`, `local_0042_filename_ts: 20260430_004254`, `local_0042_is_eod: false`.
- [x] 2. Add date-rollover force close for single-open breakout strategies.
  - Test: [x] Instantiate strategy with a prior-day open trade, process a new-day tick, and verify it closes with `Date Rollover Force Close` before new entries are considered.
  - Evidence: Controlled breakout probe closed one prior-day open trade with `Date Rollover Force Close` and cleared stale price history.
- [x] 3. Add date-rollover force close/reset for momentum multi-open strategies.
  - Test: [x] Instantiate momentum with prior-day open trades, process a new-day tick, and verify old trades are closed/reset and initial new-day LONG/SHORT can be generated.
  - Evidence: Controlled momentum probe closed 2 prior-day trades with `Date Rollover Force Close`, reset state, and generated new `20260430_010005` LONG/SHORT open filenames.
- [x] 4. Validate syntax and non-mutating behavior.
  - Test: [x] Run `python -m py_compile common.py momentum.py` and controlled probes with file writes stubbed.
  - Evidence: `python -m py_compile common.py momentum.py momentum_r.py breakout.py` passed. Live 30 Apr folder then populated after strategy restart.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`; `C:\Users\edebe\eds\TradeApps\breakout\fs\momentum.py`
  - Objective-Proved: Code paths updated for rollover force close.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: Controlled rollover probes and `python -m py_compile common.py momentum.py momentum_r.py breakout.py`
  - Objective-Proved: Local trading date/EOD and rollover behavior.
  - Status: captured

Implementation Log:
- 2026-04-30 02:00: Created fix task.
- 2026-04-30 02:02: Added trading timezone helpers using `Europe/London` by default, with optional `trading_timezone` config override.
- 2026-04-30 02:03: Updated trade filename/folder date derivation, EOD check, and market-bias date lookup to use local trading date.
- 2026-04-30 02:03: Added base strategy date-rollover force close for single-open strategies.
- 2026-04-30 02:04: Added momentum multi-open date-rollover force close, anchor reset, and initial dual-entry reset.
- 2026-04-30 02:04: Ran controlled probes and syntax validation.
- 2026-04-30 02:17: Restarted fixed strategy scripts and validated 30 Apr trade files are now being generated.

Changes Made:
- `common.py`: added local trading timezone helpers, changed filenames/folders/EOD to use local trading date, added `Date Rollover Force Close` before normal processing, and updated `_LATEST_TRADING_DATE` to local trading date.
- `momentum.py`: added multi-open rollover force close for prior-day trades and reset anchor/initial-dual-entry state so the new trading day can bootstrap fresh buy/sell trades.

Validation:
- `python -m py_compile common.py momentum.py momentum_r.py`: PASS.
- `python -m py_compile common.py momentum.py momentum_r.py breakout.py`: PASS.
- Controlled timestamp probe: PASS. `2026-04-30T00:42+01:00` resolves to `20260430_004254` and `is_eod=false`.
- Controlled breakout rollover probe: PASS. Prior-day open trade closed with `Date Rollover Force Close`.
- Controlled momentum rollover probe: PASS. Two prior-day open trades closed and new 30 Apr LONG/SHORT entries generated.
- Live validation after strategy restart: PASS. `json\live\forex\2026-04-30` now contains trade files: `_op=1249`, `_cl=12684`, `momentum=1350`, `momentum_r=763`, `breakout=12981` at validation time.

Risks/Notes:
- The validation will use controlled/stubbed strategy instances to avoid creating live trade/order files.
- Running processes need restart after the code fix for live behavior to pick up the change.
- Strategy scripts were restarted after the fix. The supervisor/process query was unreliable under Windows load, so the six strategy scripts were started directly to ensure the patch was active.
- `grid_live_monitor.lock` remains a separate issue from the investigation and should be handled under its own `_998_` fix if required.

Completion Status: complete - 2026-04-30 02:18
