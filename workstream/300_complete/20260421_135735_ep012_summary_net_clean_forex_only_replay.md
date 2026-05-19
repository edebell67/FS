# EP012 Summary Net Clean Forex-Only Replay

Source: User request, 2026-04-21
Task Type: standard

## Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false
depends_on:
- `workstream/300_complete/20260421_133939_ep012_forex_summary_net_top3_hold_replay.md`
feeds_into: []

## Task Summary
Rerun the `forex/_summary_net` top-3 hold replay using the earlier 16 clean forex dates as the whitelist:
`2026-03-24, 2026-03-26, 2026-03-27, 2026-03-28, 2026-03-29, 2026-03-30, 2026-03-31, 2026-04-01, 2026-04-02, 2026-04-03, 2026-04-05, 2026-04-06, 2026-04-07, 2026-04-08, 2026-04-09, 2026-04-17`.

## Context
Prior replay filtered rows to forex regex while still loading contaminated files. A strict clean-file-only scan showed no usable ranked snapshots because almost every `_summary_net` file contains at least one non-forex key. User then clarified to use the 16 files/dates from the earlier clean forex-only set.

## Destination Folder
Destination Folder: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/`

## Dependency
Dependency: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay.py`

## Plan
- [x] 1. Add clean-file-only and date-whitelist modes to the replay script.
  - [x] Test: Run targeted commands and verify contaminated files can be counted as excluded, and selected dates can be whitelisted.
  - Evidence: Strict clean-file-only run returned `snapshots=0` with `contaminated_excluded=156`; date whitelist run returned `files=27 snapshots=26`.

- [x] 2. Rerun replay on the earlier 16 clean forex dates.
  - [x] Test: Execute replay command and capture summary output.
  - Evidence: `summary_net_top3_hold_replay_prior_16_clean_forex_dates`: all cutoffs returned `total=464372 avg_day=30958 opened=15 switches=3 days=15`.

- [x] 3. Validate and report results.
  - [x] Test: Compile script and confirm output reports were written.
  - Evidence: `python -m py_compile ...summary_net_top3_hold_replay.py` passed; markdown/CSV reports generated.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: test_output
  - Artifact: `python epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay.py --dates "<16 dates>" --open-hours 0,1,2,3 --output-stem summary_net_top3_hold_replay_prior_16_clean_forex_dates`
  - Objective-Proved: Clean-file-only replay ran successfully.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay_prior_16_clean_forex_dates.md`
  - Objective-Proved: Clean forex-only replay reports and CSVs were generated.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `python -m py_compile epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay.py`
  - Objective-Proved: Replay script remains syntactically valid after adding date whitelist support.
  - Status: captured

## Implementation Log
- 2026-04-21 13:57: Created in-progress task for clean forex-only `_summary_net` rerun.
- 2026-04-21 13:59: Added `--clean-files-only`; strict clean-file-only run produced no usable snapshots because source files are contaminated.
- 2026-04-21 14:01: Added `--dates` whitelist and reran using the earlier 16 clean forex dates.
- 2026-04-21 14:03: Ran the same 16-date set excluding `2026-04-17` to show outlier impact.

## Changes Made
- Updated `summary_net_top3_hold_replay.py`:
  - Added `--clean-files-only`.
  - Added `--dates`.
- Generated:
  - `summary_net_top3_hold_replay_clean_forex_only.md`
  - `summary_net_top3_hold_replay_prior_16_clean_forex_dates.md`
  - `summary_net_top3_hold_replay_prior_16_clean_forex_dates_summary.csv`
  - `summary_net_top3_hold_replay_prior_16_clean_forex_dates_days.csv`
  - `summary_net_top3_hold_replay_prior_16_clean_forex_dates_events.csv`
  - `summary_net_top3_hold_replay_prior_16_clean_forex_dates_excl_0417.md`

## Validation
- Strict clean-file-only all available:
  - `00:00 total=0 avg_day=0 opened=0 switches=0 days=0`
  - `files=158 snapshots=0 contaminated_excluded=156`
- Earlier 16 clean forex dates:
  - `00:00 total=464372 avg_day=30958 opened=15 switches=3 days=15`
  - `01:00 total=464372 avg_day=30958 opened=15 switches=3 days=15`
  - `02:00 total=464372 avg_day=30958 opened=15 switches=3 days=15`
  - `03:00 total=464372 avg_day=30958 opened=15 switches=3 days=15`
  - `files=27 snapshots=26`
- Earlier 16 clean forex dates excluding `2026-04-17`:
  - `00:00 total=10642 avg_day=760 opened=14 switches=3 days=14`
  - `01:00 total=10642 avg_day=760 opened=14 switches=3 days=14`
  - `02:00 total=10642 avg_day=760 opened=14 switches=3 days=14`
  - `03:00 total=10642 avg_day=760 opened=14 switches=3 days=14`
  - `files=25 snapshots=24`
- `python -m py_compile epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay.py`
  - Result: passed.

## Risks/Notes
- Strict clean-file-only cannot currently produce meaningful `_summary_net` replay output because the available files are contaminated or empty.
- The 16-date whitelist produced 15 usable days because `2026-03-28` has no `_summary_net` files.
- `2026-04-17` still dominates the 16-date result with `453,730` net from `GBPEUR_C / breakout_R_2_tp10.0_sl20.0_12141c72`.

## Completion Status
Status: Complete
Created: 2026-04-21 13:57
Completed: 2026-04-21 14:03
