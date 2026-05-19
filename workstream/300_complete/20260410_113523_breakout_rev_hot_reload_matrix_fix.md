## Source

- Follow-up implementation task from `20260410_103642_breakout_rev_missing_tp_matrix_investigation.md`
- User instruction on 2026-04-10: create a task and proceed

## Task Type

standard

## Task Attributes

- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

## Task Summary

Implement and validate a code fix so long-running breakout strategy processes resolve TP/SL/window matrices from fresh config data unless explicitly overridden by CLI arguments.

## Context

- Target module: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Related scripts: `breakout.py`, `breakout_R.py`, `breakout_Rev.py`, `breakout_R_Rev.py`
- Related investigation: `C:\Users\edebe\eds\workstream\200_inprogress\20260410_103642_breakout_rev_missing_tp_matrix_investigation.md`

## Destination Folder

None

## Dependency

- Requires preserving existing explicit CLI override behaviour

## Plan

- [x] 1. Create lifecycle file and move to `200_inprogress`.
- [x] 2. Patch runtime matrix resolution in `common.py`.
- [x] 3. Add focused regression test coverage.
- [x] 4. Run targeted validation commands.
- [x] 5. Document results and next action.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: code_change
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
  - Objective-Proved: TP/SL matrix resolution now uses explicit `None` sentinel semantics rather than comparing against startup-frozen defaults
  - Status: captured
- Evidence-Type: code_change
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\breakout.py`, `breakout_R.py`, `breakout_Rev.py`, `breakout_R_Rev.py`
  - Objective-Proved: Strategy entry scripts now pass `None` when TP/SL are not explicitly overridden on the CLI
  - Status: captured
- Evidence-Type: test
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_breakout_runtime_state.py`
  - Objective-Proved: Runtime state follows current config matrix when TP/SL args are omitted and pins dimensions when explicit CLI values are provided
  - Status: captured

## Implementation Notes

Chronological update:

- Created a new lifecycle task because the scope changed from investigation to implementation.
- Re-checked `common.py` and confirmed the previous comparison logic inferred "use config" by testing `tp_pips_arg == BASE_TP_PIPS` and `sl_pips_arg == BASE_SL_PIPS`.
- Replaced that inference with explicit sentinel behaviour:
  - `tp_pips_arg is None` means use current `config.json` TP list
  - `sl_pips_arg is None` means use current `config.json` SL list
  - explicit numeric values still pin the runtime to that single TP/SL value
- Updated all four breakout entry scripts so `--tp-pips` and `--sl-pips` default to `None` instead of startup-imported constants.
- Added targeted tests around `_build_runtime_state(...)` using a dummy strategy class to avoid live runtime dependencies.

## Validation

Command:

```powershell
python -m pytest "C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_breakout_runtime_state.py"
```

Result:

```text
2 passed in 2.56s
```

## Outcome

- The code now has a reliable distinction between:
  - no CLI TP/SL override supplied
  - explicit CLI TP/SL override supplied
- This removes dependence on startup-time default equality for TP/SL matrix expansion.
- Existing long-running processes will still need to be restarted once to pick up the new code.

## Risks/Notes

- The fix must not break explicit CLI overrides for `--window-size`, `--tp-pips`, or `--sl-pips`
- Tests should avoid live services and filesystem-heavy dependencies
- Live process command-line inspection remained blocked by sandbox permissions, so this task validates code behaviour rather than the already-running Windows processes
- A process restart is still required for the production Rev/R_Rev loops to load the patched code

## Completion Status

- State: COMPLETE
- Timestamp: 2026-04-10 11:40:00 +01:00
- Next Action: Restart the live `breakout_Rev.py` and `breakout_R_Rev.py` processes so they load the patched code
