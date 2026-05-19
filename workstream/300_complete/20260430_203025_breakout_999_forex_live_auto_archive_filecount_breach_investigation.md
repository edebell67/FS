Source: User request on 2026-04-30 to investigate why `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-30` contains 47k+ files even though auto archive is configured to archive closed files when file count exceeds 5,000.
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
  depends_on: []
  feeds_into: []
Task Summary: Investigate the forex live JSON archive path and the auto-archive control flow to determine why the 2026-04-30 day folder grew beyond 47,000 files despite the expected behavior that closed files should be archived once file count exceeds 5,000.
Context: Likely affected areas include `TradeApps\breakout\fs\json\live\forex\2026-04-30`, the breakout live JSON writer and close-handling flow, archive threshold configuration, any file-count gate or archive job logic, and related runtime logs/configuration under `TradeApps\breakout\fs`.
Destination Folder: None
Dependency: None

## Plan
- [x] 1. Confirm the expected archive behavior, threshold source, and authoritative code paths that are supposed to archive closed forex JSON files.
  - [x] Test: Repository review identifies the exact config key(s), default threshold, triggering condition, and function(s) responsible for archiving closed files once file count exceeds 5,000.
  - Evidence: `TradeApps\breakout\fs\common.py` shows `_perform_cld_auto_archive(config)` uses `auto_archive_threshold` from config with fallback `5000`, while active `TradeApps\breakout\fs\config.json` sets `auto_archive_threshold` to `1000`.
- [x] 2. Trace the runtime decision path for the affected `2026-04-30` forex folder to determine whether the archive routine did not run, ran with the wrong threshold/scope, or skipped the files due to state/filename conditions.
  - [x] Test: Manual trace across code, config, and available logs/runtime artifacts yields a concrete explanation for why the folder was allowed to exceed 47,000 files.
  - Evidence: The live forex folder contains `50,000` `.json` files, including `37,375` `*_cl.json`, `10,252` `*_cld.json`, `2,313` `*_op.json`, and `16` underscore files; archive batches under `archive\013337`, `024221`, `082607`, `082613`, `095414`, and `153812` contain only `*_cld.json` and zero `*_cl.json`.
- [x] 3. Document root cause, affected controls, and the smallest safe follow-up action required to restore expected archive behavior.
  - [x] Test: The investigation output includes a clear root-cause statement, impacted files/settings, operational risk, and whether a distinct `_998_` fix task is required.
  - Evidence: Root cause and follow-up are recorded below, and a separate `_998_` fix task was created to implement archive coverage for `*_cl.json` plus watcher supervision hardening.

## Findings

### 1. Implemented behavior does not match the expected meaning of "archive closed files"
- The threshold-based auto-archive path is `_perform_cld_auto_archive(config)` in `TradeApps\breakout\fs\common.py`.
- That function explicitly scans only `*_cld.json` files:
  - `cld_files = [f for f in source_date_dir.glob('*_cld.json') if f.is_file()]`
- It does not scan or move `*_cl.json`, which is the normal closed-trade filename suffix produced by the trade finalization flow.
- `TRADE_CLOSED_SUFFIX` is `_cl` in `TradeApps\breakout\fs\common.py`, and `_with_trade_status_suffix(..., 'CLOSED')` writes standard closed trade files as `*_cl.json`.

### 2. The overflowing folder is mostly `*_cl.json`, not `*_cld.json`
- Current measured file counts in `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-30`:
  - `50,000` `.json` files total
  - `37,375` `*_cl.json`
  - `10,252` `*_cld.json`
  - `2,313` `*_op.json`
  - `16` underscore/support files
- Sampled `*_cl.json` contents confirm they are normal closed trades with `status: "CLOSED"`, `exit_time`, and `exit_reason`.
- This means the majority of closed files were never eligible for the threshold archiver as currently implemented.

### 3. Auto-archive did run on 2026-04-30, but only for `*_cld.json`
- The folder already contains archive batches:
  - `archive\013337` with `1,156` `*_cld.json`
  - `archive\024221` with `1,173` `*_cld.json`
  - `archive\082607` with `14,710` `*_cld.json`
  - `archive\082613` with `500` `*_cld.json`
  - `archive\095414` with `2,076` `*_cld.json`
  - `archive\153812` with `31,490` `*_cld.json`
- All inspected archive batches contain zero `*_cl.json`.
- So the auto-archive mechanism is not absent; it is simply targeting the wrong closed-file class for the stated expectation.

### 4. The active runtime threshold is lower than expected
- The user expectation referenced "less than 5k".
- The active runtime `TradeApps\breakout\fs\config.json` currently sets:
  - `auto_archive_threshold: 1000`
- The fallback/default in code and related workstream notes is `5000`, but the actual live config on 2026-04-30 is stricter at `1000`.
- This does not cause the overflow; it makes the mismatch more obvious, because `10,252` remaining `*_cld.json` should also have been archived once runtime checks stopped or fell behind.

### 5. Supervision is incomplete for the dedicated watcher
- `TradeApps\breakout\fs\archive_cld.py` is the dedicated watcher script for the threshold archiver.
- `TradeApps\breakout\fs\verify_algo_execution_and_restart_02.py` supervises `archive.py`, but not `archive_cld.py`.
- The main strategy loop in `common.py` also calls `_perform_cld_auto_archive(config)` periodically, so some archive activity can still occur without `archive_cld.py`.
- However, the dedicated threshold watcher is not part of the normal watchdog set, which weakens reliability if the in-loop path is interrupted or if only non-watcher processes remain active.

## Root Cause
- Primary root cause: the implemented auto-archive selector only archives `*_cld.json`, while the vast majority of actual closed forex trade files are written as `*_cl.json`. As a result, normal closed trade records are excluded from auto-archive eligibility and accumulate indefinitely in the live day folder.
- Secondary reliability issue: the dedicated `archive_cld.py` watcher is not supervised by `verify_algo_execution_and_restart_02.py`, so the threshold archiver relies on incidental execution through active strategy loops rather than a guaranteed always-on watcher.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: manual_verification
  - Artifact: Repository review of `TradeApps\breakout\fs\common.py`, `TradeApps\breakout\fs\json_layout.py`, `TradeApps\breakout\fs\archive_cld.py`, and `TradeApps\breakout\fs\verify_algo_execution_and_restart_02.py`
  - Objective-Proved: Confirms the authoritative archive trigger, the file selector used by auto-archive, the active threshold source, and the current watchdog coverage.
  - Status: captured
- Evidence-Type: log_output
  - Artifact: April 30 archive batches under `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-30\archive\013337`, `024221`, `082607`, `082613`, `095414`, `153812`
  - Objective-Proved: Confirms auto-archive executed on 2026-04-30 and moved `*_cld.json` files only, with zero archived `*_cl.json` files in inspected batches.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: Local file counts from `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-30` showing `50,000` `.json`, `37,375` `*_cl.json`, `10,252` `*_cld.json`, `2,313` `*_op.json`
  - Objective-Proved: Confirms the overflowing folder is dominated by standard closed trade files outside the implemented auto-archive selector.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: C:\Users\edebe\eds\workstream\300_complete\20260430_203025_breakout_999_forex_live_auto_archive_filecount_breach_investigation.md
  - Objective-Proved: Captures the completed investigation and root-cause record in the lifecycle task.
  - Status: captured

## Implementation Log
- 2026-04-30 20:30:25 BST: User requested creation of an investigation task for unexpected growth in `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-30`.
- 2026-04-30 20:30:25 BST: Reviewed `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md` and confirmed that investigation tasks must include `_999_` in the filename and use the lifecycle template.
- 2026-04-30 20:30:25 BST: Created this lifecycle task in `workstream/100_todo` with the suspected archive-threshold breach, affected path, and investigation plan.
- 2026-04-30 20:35:00 BST: Moved the lifecycle task into `workstream/200_inprogress` and started repository/runtime investigation.
- 2026-04-30 20:40:00 BST: Measured the forex day folder at `49,997` to `50,000` files and traced archive-related code paths in `common.py`, `archive.py`, and `archive_cld.py`.
- 2026-04-30 21:10:00 BST: Confirmed `_perform_cld_auto_archive(config)` uses `auto_archive_threshold` but only scans `*_cld.json`.
- 2026-04-30 21:20:00 BST: Confirmed standard closed trade filenames are emitted as `*_cl.json` via `TRADE_CLOSED_SUFFIX = '_cl'`.
- 2026-04-30 21:35:00 BST: Counted live folder file classes and identified that `*_cl.json` dominates the overflow.
- 2026-04-30 21:45:00 BST: Inspected existing archive batches for 2026-04-30 and confirmed they contain archived `*_cld.json` only, with zero `*_cl.json`.
- 2026-04-30 21:55:03 BST: Documented root cause and prepared a separate `_998_` follow-up task for the implementation fix.

## Changes Made
- Updated the investigation lifecycle file with:
  - the authoritative archive function and active threshold
  - the closed-file suffix mismatch (`*_cl.json` vs `*_cld.json`)
  - measured file-count evidence from the live forex folder
  - archive-batch evidence showing only `*_cld.json` were moved
  - the root-cause statement and follow-up recommendation

## Validation
- Verified `TradeApps\breakout\fs\config.json` currently sets `auto_archive_threshold` to `1000`.
- Verified `TradeApps\breakout\fs\common.py` defines `TRADE_CLOSED_SUFFIX = '_cl'` and writes normal closed files as `*_cl.json`.
- Verified `TradeApps\breakout\fs\common.py` auto-archives only `source_date_dir.glob('*_cld.json')`.
- Verified the live forex folder currently contains `37,375` `*_cl.json` files and `10,252` `*_cld.json` files.
- Verified the April 30 archive subfolders contain `*_cld.json` files only and zero `*_cl.json`.
- Verified `TradeApps\breakout\fs\verify_algo_execution_and_restart_02.py` supervises `archive.py` but not `archive_cld.py`.

## Risks/Notes
- This investigation did not move or delete any live/archive files; it only measured and traced behavior.
- The `*_cld.json` count remaining above threshold suggests runtime auto-archive may also be intermittent after the last observed archive batch, but that is secondary to the larger selector mismatch because `*_cl.json` was never eligible to move at all.
- The safest fix is to update archive selection to include standard closed files (`*_cl.json`) without affecting open files (`*_op.json`) or underscore support files, then harden supervision for the dedicated watcher.
- A separate `_998_` follow-up task is required for implementation and validation of the fix.

## Completion Status
- State: Complete
- Timestamp: 2026-04-30 21:55:03 BST
