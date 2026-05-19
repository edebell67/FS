Source: User requested on 2026-04-29 a new momentum strategy variant copied from C:\Users\edebe\eds\TradeApps\breakout\fs\momentum.py as momentum_r.py with reversed buy/sell signals.
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
  workflow_task: false
  workflow_name: ""
  workflow_stage: complete
Task Summary: Add a new momentum reverse strategy script, momentum_r.py, that is identical to momentum.py except generated buy signals execute sell trades and generated sell signals execute buy trades.
Context:
- Source script: C:\Users\edebe\eds\TradeApps\breakout\fs\momentum.py
- New script: C:\Users\edebe\eds\TradeApps\breakout\fs\momentum_r.py
- Related common execution path: C:\Users\edebe\eds\TradeApps\breakout\fs\common.py
- Related config: C:\Users\edebe\eds\TradeApps\breakout\fs\config.json
- Process reference: C:\Users\edebe\eds\skills\workstream-task-lifecycle
Destination Folder: C:\Users\edebe\eds\TradeApps\breakout\fs
Dependency: C:\Users\edebe\eds\TradeApps\breakout\fs\momentum.py
Requirements:
- Create momentum_r.py as a copy of momentum.py.
- Reverse trade direction only: a momentum buy trigger must create a sell trade, and a momentum sell trigger must create a buy trade.
- Keep all other behavior identical to momentum.py, including the ability to continue adding new positions while signals continue to be generated.
- Preserve existing TP/SL and step-pip behavior unless momentum.py already defines otherwise.
- Ensure generated strategy naming clearly identifies the reverse variant and does not collide with normal momentum strategy names.
- Ensure generated JSON trade files and summaries can distinguish momentum_r trades from momentum trades.
Plan:
- [x] 1. Compare momentum.py strategy naming, entry generation, and write path.
  - Test: Inspect momentum.py for buy/sell trigger functions, strategy-name construction, and common execution entry point.
  - Evidence: momentum.py check_and_enter uses upper LONG and lower SHORT signal paths; script alias is momentum_0_tpX_slY.
- [x] 2. Create momentum_r.py from momentum.py and reverse only the trade direction mapping.
  - Test: Diff momentum_r.py against momentum.py and confirm only expected strategy identity/direction changes plus any required comments.
  - Evidence: momentum_r.py subclasses MomentumStrategy, preserves inherited behavior, and overrides signal-to-trade entry mapping plus alias.
- [x] 3. Validate syntax and import behavior.
  - Test: python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\momentum_r.py
  - Evidence: py_compile passed.
- [x] 4. Run a controlled execution or dry-run equivalent to confirm at least one reversed signal produces the opposite direction without blocking continued position creation.
  - Test: Execute the same command pattern used for momentum.py with safe/default parameters or a minimal controlled product set.
  - Evidence: In-memory controlled test showed upper LONG signals created SHORT entries at 1.10050 and 1.10100; lower SHORT signals created LONG entries at 1.09950 and 1.09900.
- [x] 5. Verify generated files and strategy names are distinct from momentum.py outputs.
  - Test: Check output JSON filename/strategy fields include momentum_r or another agreed reverse identifier and do not overwrite momentum files.
  - Evidence: build_momentum_reverse_script_alias(5.0, 7.0) returned momentum_r_0_tp5.0_sl7.0.
Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: C:\Users\edebe\eds\TradeApps\breakout\fs\momentum_r.py
  - Objective-Proved: New strategy variant is implemented as a controlled copy of momentum.py with reversed signal direction.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\momentum_r.py
  - Objective-Proved: New script is syntactically valid.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: C:\Users\edebe\eds\TradeApps\breakout\fs\momentum_r.py
  - Objective-Proved: Runtime alias is distinct from momentum.py and uses momentum_r_0_tp5.0_sl7.0 for generated trade files.
  - Status: captured
Implementation Log:
- 2026-04-29 14:23: Task created in workstream/100_backlog using new `_997_` feature/functionality filename rule.
- 2026-04-29 14:36: Task moved to workstream/200_inprogress.
- 2026-04-29 14:39: Inspected momentum.py entry generation, strategy alias, and common run_multiwindow entry point.
- 2026-04-29 14:43: Created momentum_r.py with MomentumReverseStrategy inheriting MomentumStrategy and reversing LONG/SHORT generated signals before trade entry.
- 2026-04-29 14:43: Added distinct momentum_r_0_tpX_slY script alias.
- 2026-04-29 14:44: Ran syntax and controlled in-memory behavior validation.
Changes Made:
- Added C:\Users\edebe\eds\TradeApps\breakout\fs\momentum_r.py.
- Added MomentumReverseStrategy with LONG signal -> SHORT trade and SHORT signal -> LONG trade behavior.
- Added signal-level ladder tracking so repeated reverse positions continue to open from the most recent same-signal entry threshold.
- Added reverse metadata fields momentum_signal and reversed_from_signal to new trade records.
Validation:
- python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\momentum_r.py passed.
- Controlled in-memory test output:
  - bootstrap [('SHORT', 'LONG', 1.1), ('LONG', 'SHORT', 1.1)]
  - upper_signal added SHORT trades with momentum_signal LONG at 1.1005 and 1.101
  - lower_signal added LONG trades with momentum_signal SHORT at 1.0995 and 1.0990
  - alias momentum_r_0_tp5.0_sl7.0
Risks/Notes:
- The implementation must not alter existing momentum.py behavior.
- If common.py needs registration or dispatch changes for momentum_r.py, include those edits in this task and validate normal execution.
- momentum_r.py is executable directly through the same common run_multiwindow path used by momentum.py; no common.py change was required.
- Live execution was not started as part of validation to avoid creating real strategy files/trades without explicit run instruction.
Completion Status: Complete.
