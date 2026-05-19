# EP012 Summary Net Replay Correction

Source: User correction, 2026-04-21
Task Type: standard

## Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false
depends_on:
- `workstream/300_complete/20260421_135735_ep012_summary_net_clean_forex_only_replay.md`
feeds_into: []

## Task Summary
Correct the unrealistic `_summary_net` top-3 hold replay results. The previous replay incorrectly allowed generated/suffixed strategy keys such as `breakout_R_2_tp10.0_sl20.0_12141c72`, causing unrealistic outlier nets.

## Context
The replay must represent selectable base strategies, not generated trade instance identifiers or contaminated/non-canonical strategy keys.

## Destination Folder
Destination Folder: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/`

## Dependency
Dependency: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay.py`

## Plan
- [x] 1. Audit outlier strategy keys and scoring path.
  - [x] Test: Inspect event/day outputs and source data for `2026-04-17` and `2026-03-31` outliers.
  - Evidence: Previous run opened generated strategies `breakout_R_2_tp10.0_sl20.0_12141c72` and `breakout_R_2_tp3.0_sl10.0_400f3f6d`; source audit found 191 non-canonical strategy keys in the 16-date whitelist.

- [x] 2. Add canonical strategy filtering to exclude suffixed/generated strategy keys.
  - [x] Test: Rerun 16-date replay and verify outlier strategy keys no longer appear.
  - Evidence: Corrected event output opens `GBPEUR_C / breakout_2_tp20.0_sl20.0` on `2026-04-17`, not the suffixed `_12141c72` key; `2026-03-31` opens `GBPAUD_C / breakout_2_tp10.0_sl5.0`, not `_400f3f6d`.

- [x] 3. Validate corrected results and report.
  - [x] Test: Compile script and display aligned corrected table.
  - Evidence: `py_compile` passed; corrected 16-date replay returned `total=11342 avg_day=756 opened=15 switches=3 days=15`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: test_output
  - Artifact: `python epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay.py --dates "<16 dates>" --open-hours 0,1,2,3 --output-stem summary_net_top3_hold_replay_prior_16_clean_forex_dates_corrected`
  - Objective-Proved: Corrected replay excludes invalid suffixed/generated strategies.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `python -m py_compile epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay.py`
  - Objective-Proved: Script remains syntactically valid after correction.
  - Status: captured

## Implementation Log
- 2026-04-21 14:05: Created correction task after user flagged prior results as unrealistic/wrong.
- 2026-04-21 14:06: Audited outlier strategy keys and confirmed generated GUID-suffixed keys were included.
- 2026-04-21 14:07: Added canonical base strategy regex filtering.
- 2026-04-21 14:08: Reran corrected 16-date whitelist and no-`2026-04-17` variants.

## Changes Made
- Updated `summary_net_top3_hold_replay.py`:
  - Added canonical base strategy regex filter.
  - Added `--include-generated-strategies` opt-in for diagnostic runs only.
  - Default behavior now excludes generated/suffixed strategy instance keys.
- Generated corrected outputs:
  - `summary_net_top3_hold_replay_prior_16_clean_forex_dates_corrected.md`
  - `summary_net_top3_hold_replay_prior_16_clean_forex_dates_corrected_summary.csv`
  - `summary_net_top3_hold_replay_prior_16_clean_forex_dates_corrected_days.csv`
  - `summary_net_top3_hold_replay_prior_16_clean_forex_dates_corrected_events.csv`
  - `summary_net_top3_hold_replay_prior_16_clean_forex_dates_excl_0417_corrected.md`

## Validation
- Corrected 16-date whitelist:
  - `00:00 total=11342 avg_day=756 opened=15 switches=3 days=15`
  - `01:00 total=11342 avg_day=756 opened=15 switches=3 days=15`
  - `02:00 total=11342 avg_day=756 opened=15 switches=3 days=15`
  - `03:00 total=11342 avg_day=756 opened=15 switches=3 days=15`
- Corrected 16-date whitelist excluding `2026-04-17`:
  - `00:00 total=10642 avg_day=760 opened=14 switches=3 days=14`
  - `01:00 total=10642 avg_day=760 opened=14 switches=3 days=14`
  - `02:00 total=10642 avg_day=760 opened=14 switches=3 days=14`
  - `03:00 total=10642 avg_day=760 opened=14 switches=3 days=14`
- `python -m py_compile epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay.py`
  - Result: passed.

## Risks/Notes
- Corrected results exclude generated/suffixed strategy keys by default.
- `2026-03-28` still has no usable `_summary_net` files in the whitelist, so 16 dates produce 15 usable days.

## Completion Status
Status: Complete
Created: 2026-04-21 14:05
Completed: 2026-04-21 14:09
