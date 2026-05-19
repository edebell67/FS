Source: User request in Codex thread on 2026-04-13 asking where `pick_now` gets set.
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
  depends_on: []
  feeds_into: []
Task Summary: Trace the code path that computes and writes `pick_now`, identify the source files involved, and summarize the thresholds that control it.
Context: `C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\strategy_predictor.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`.
Destination Folder: None
Dependency: None
Plan:
- [x] 1. Locate the assignment site for `pick_now`.
  - [x] Test: Search for `pick_now` references and inspect the file that writes it into output payloads.
  - [x] Evidence: `summary_net_generator.py` lines captured showing `pick_now` added to top-20 candidate rows.
- [x] 2. Trace the evaluation logic and configuration source.
  - [x] Test: Inspect `strategy_predictor.py` for `evaluate_pick_now_logic`, config loading, and default thresholds.
  - [x] Evidence: `strategy_predictor.py` lines captured for config loading and boolean evaluation logic.
- [x] 3. Summarize the result for the user with code references.
  - [x] Test: Final response identifies the writer, the evaluator, and the config/default thresholds.
  - [x] Evidence: Final Codex response in this thread.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py`
  - Objective-Proved: The exact write site for `pick_now` is identified.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\strategy_predictor.py`
  - Objective-Proved: The evaluation logic and hidden defaults are identified.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: Final response in Codex thread
  - Objective-Proved: The user receives the requested explanation with references.
  - Status: captured

## Implementation Log
- 2026-04-13 12:26:26: Created lifecycle file for `pick_now` trace request.
- 2026-04-13 12:26:40: Located `pick_now` assignment in `summary_net_generator.py`.
- 2026-04-13 12:27:00: Located threshold evaluation and config loading in `strategy_predictor.py`.

## Changes Made
- Added this lifecycle task file only.

## Validation
- `rg -n "pick_now" 'C:\Users\edebe\eds\TradeApps\breakout\fs'`
  - Result: Pass. Located assignment and evaluation paths.
- Numbered reads of `summary_net_generator.py`, `strategy_predictor.py`, and `config.json`
  - Result: Pass. Confirmed write site and config source.

## Risks/Notes
- `config.json` exposes only part of the effective `pick_now` criteria; additional defaults remain in `strategy_predictor.py`.

## Completion Status
- Complete as of 2026-04-13 12:27:00.
