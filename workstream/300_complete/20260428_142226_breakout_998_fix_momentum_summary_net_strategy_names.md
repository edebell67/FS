Source: User request on 2026-04-28 to ensure `_summary_net.json` contains the correct direction-specific strategy names for momentum strategies with no generic `momentum` gaps.
Task Type: standard
Task Attributes:
  recurring_task: false
  recurrence_type: scheduled
  recurrence_rule: None
  looping_task: false
  loop_until: manual_stop
  splittable_task: false
  split_output_type: files
  split_spawn_task: false
  split_failure_mode: fail_fast
  workflow_task: false
  workflow_name: ""
  workflow_stage: in_progress
  depends_on: []
  feeds_into: []
Task Summary: Fix momentum strategy naming in `_summary_net.json` so momentum trades are represented under the correct direction-specific strategy keys and no generic `momentum` summary rows remain when enough trade metadata exists to classify them.
Context: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-28\_summary_net.json`, `C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-28\`
Destination Folder: C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-28\
Dependency: Investigation concluded momentum strategy names are summary-eligible and current trade artifacts contain enough data to classify most entries by direction.
Plan:
- [x] 1. Inspect `_summary_net.json` and the underlying momentum trade files to identify any remaining generic `momentum` strategy keys and their source records.
  - [x] Test: Enumerate momentum-related keys in `_summary_net.json` and compare against current trade artifacts.
  - Evidence: `_summary_net.json` contained generic `momentum` and `momentum_0_tp5.0_sl7.0` keys; 32 residual momentum trade artifacts still carried generic strategy metadata and stale summary index rows also remained.
- [x] 2. Apply the fix so summary generation or summary data uses `momentum_b_0_tp5.0_sl7.0` and `momentum_s_0_tp5.0_sl7.0` consistently.
  - [x] Test: Regenerate or rewrite the affected summary data and validate the updated JSON.
  - Evidence: Patched `summary_net_generator.py` to normalize/dedupe legacy momentum trades; directly canonicalized residual momentum trade files in the live day folder; rebuilt the momentum sections of `_summary_net.json` and `_trades_summary.json`.
- [x] 3. Verify there are no residual generic `momentum` strategy keys in `_summary_net.json` when direction can be inferred from available trade data.
  - [x] Test: Re-scan momentum-related strategy keys in `_summary_net.json`.
  - Evidence: `_summary_net.json` now lists only `momentum_b_0_tp5.0_sl7.0`, `momentum_s_0_tp5.0_sl7.0`, `momentum_bootstrapcheck`, and `momentum_localcheck`; `_trades_summary.json` has `GENERIC_ROWS=0`; live trade artifacts have `GENERIC_FILES=0`.
Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-28\_summary_net.json`, `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-28\_trades_summary.json`
  - Objective-Proved: `_summary_net.json` momentum strategy keys were corrected.
  - Status: complete
Execution Log:
- 2026-04-28 14:22:26: Fix-followup task created in `workstream/100_todo`.
- 2026-04-28 14:26:00: Confirmed the root issue was a mix of residual generic momentum trade artifacts and stale summary index data, not a breakout-only allowlist in the generator.
- 2026-04-28 14:28:00: Patched `summary_net_generator.py` to canonicalize legacy momentum strategy names, infer missing direction from trade metadata, and dedupe stale old/new copies by GUID.
- 2026-04-28 15:08:12: Canonicalized the remaining live-day momentum trade artifacts in place, rewrote the momentum portions of `_summary_net.json` and `_trades_summary.json`, and verified that no generic `momentum` entries remain.
- 2026-04-28 15:09:00: Restarted `summary_net_generator.py` so subsequent writes use the patched normalization logic.
