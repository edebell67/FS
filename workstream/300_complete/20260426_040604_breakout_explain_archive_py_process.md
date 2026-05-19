Source: User request in Codex session on 2026-04-26
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
Task Summary: Explain the process implemented in `C:\Users\edebe\eds\TradeApps\breakout\fs\archive.py`.
Context: `TradeApps/breakout/fs/archive.py` and any directly related modules, inputs, outputs, scheduling, and side effects required to explain the script accurately.
Destination Folder: None
Dependency: None

Plan:
- [x] 1. Read `TradeApps/breakout/fs/archive.py` and identify the main control flow.
  - [x] Test: Review the file and identify entry points, major functions, and execution order; pass when the top-level process is mapped.
  - Evidence: `archive.py` consists of config load/save helpers plus `main(run_once=False)`, which polls `config.json` every 5 seconds and calls `common._perform_archiving(cfg)` when `cfg["archive"]` is true.
- [x] 2. Trace the script’s inputs, outputs, and dependent files or systems.
  - [x] Test: Review directly referenced modules, paths, and external interactions; pass when the operational process can be explained end-to-end.
  - Evidence: Traced `archive.py` into `common._perform_archiving()`, `_json_root_dir()`, `_iter_day_directories()`, and the config fields `archive`, `run_mode`, `send_json_files`, and `send_json_files_sim`.
- [x] 3. Write a clear explanation of the process and any important caveats.
  - [x] Test: Capture source references that support the explanation; pass when the explanation is backed by code evidence.
  - Evidence: Captured source references in `archive.py` and `common.py` covering the watcher loop, archive preflight close-orders, file moves, underscore-file reset, trade-bucket reset, and `grid_live.json` reset.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `TradeApps/breakout/fs/archive.py`
  - Objective-Proved: The watcher loop, config flag check, and invocation path into the archive implementation were read directly from source.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `TradeApps/breakout/fs/common.py`
  - Objective-Proved: The underlying archive execution steps, file-system effects, and reset behavior were traced directly from source.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: not_applicable
  - Objective-Proved: This was a code explanation task, not a user-visible behavior change requiring runtime verification.
  - Status: not_applicable

## Implementation Log
- 2026-04-26 04:06:04+01:00 Created backlog lifecycle task for explaining the `TradeApps/breakout/fs/archive.py` process.
- 2026-04-26 04:08:00+01:00 Moved the lifecycle file into `200_inprogress` and read `TradeApps/breakout/fs/archive.py`.
- 2026-04-26 04:08:30+01:00 Traced the implementation into `TradeApps/breakout/fs/common.py` to inspect `_perform_archiving()`, layout resolution, and runtime archive call sites.
- 2026-04-26 04:09:10+01:00 Completed the source-backed explanation and recorded the key caveat that actual archive path resolution happens in `common.py`, not in the simplified path variables inside `archive.py`.

## Changes Made
- Added lifecycle task file `workstream/100_backlog/20260426_040604_breakout_explain_archive_py_process.md`.
- Updated the lifecycle file with completed investigation evidence and explanation coverage.

## Validation
- Reviewed `TradeApps/breakout/fs/archive.py`.
- Reviewed `TradeApps/breakout/fs/common.py` around `_perform_archiving()`, `_json_root_dir()`, `_iter_day_directories()`, and archive trigger call sites.
- Verified the explanation is supported by direct source references rather than inference alone.

## Risks/Notes
- The explanation task may require reading a small set of directly referenced modules if `archive.py` delegates key behavior elsewhere.
- `archive.py` logs a simple `json/<mode>/<date>` style source/target context, but the real archive directory selection is delegated to `common._iter_day_directories(...)`, which supports the current product-type-aware layout.

## Completion Status
- Complete at 2026-04-26 04:09:10+01:00.
