## Source

- Follow-up from `20260410_103642_breakout_rev_missing_tp_matrix_investigation.md`
- Follow-up from `20260410_113523_breakout_rev_hot_reload_matrix_fix.md`
- User instruction on 2026-04-10: continue investigation and resolve this

## Task Type

standard

## Task Attributes

- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

## Task Summary

Validate the live breakout Rev runtime after restart and add explicit startup logging of the resolved runtime matrix so live process state can be confirmed directly instead of inferred from trade-file writes.

## Context

- Target module: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Related task docs:
  - `C:\Users\edebe\eds\workstream\200_inprogress\20260410_103642_breakout_rev_missing_tp_matrix_investigation.md`
  - `C:\Users\edebe\eds\workstream\300_complete\20260410_113523_breakout_rev_hot_reload_matrix_fix.md`

## Plan

- [x] 1. Create lifecycle file and move to `200_inprogress`.
- [x] 2. Patch runtime startup logging for resolved matrix visibility.
- [x] 3. Run focused validation.
- [x] 4. Document the corrected diagnosis and outcome.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: false

## Findings

Chronological update:

- Confirmed the live processes are the expected `fs` scripts with no CLI overrides:
  - `breakout.py`
  - `breakout_R.py`
  - `breakout_Rev.py`
  - `breakout_R_Rev.py`
- Confirmed those processes were restarted on `2026-04-10 12:57:54`, which is after the `config.json` write at `2026-04-10 02:06:44`.
- Re-scanned post-restart file writes and found Rev/R_Rev were still only writing `window=2 tp=5 sl=3` files.
- Investigated embedded timestamps in those filenames and determined the post-restart writes were largely closures or updates of trades opened **before** the restart.
- Verified locally, against the real `fs` code and current config, that `_build_runtime_state(...)` now creates the full Rev matrix under the current config.

Corrected diagnosis:

- The earlier file-based inference was too strong.
- After the code fix, the runtime builder itself resolves the full matrix correctly.
- The lack of immediate `tp10/tp20/tp30` Rev files after restart is not sufficient proof that the live Rev runtime is still collapsed, because the observed file writes were mostly for pre-restart positions.
- The real remaining gap was observability: there was no direct startup log showing what matrix the live process had loaded.

Additional direct validation after user restart:

- User restarted the live breakout family again at approximately `2026-04-10 15:15:08`.
- `INIT-MATRIX` was still not visible from the user-facing sessions.
- Ran a short-lived monitored `python -u breakout_Rev.py` directly from `fs` and captured startup output.
- That monitored startup output showed `breakout_Rev` enumerating:
  - window `2` with TP values `5, 10, 20, 30`
  - window `3` with TP values `5, 10, 20, 30`
  - corresponding SL values `3, 5, 20, 30, 50`
- The monitored run timed out before the full startup scan completed, but by then it had already proven the Rev runtime was no longer pinned to a single `tp5/sl3` variant.

Final conclusion:

- The original Rev matrix-expansion defect is resolved.
- Missing visible `INIT-MATRIX` lines is an output/session-capture issue, not evidence of a remaining matrix bug.
- No further code fix is required for the original problem.

## Implementation Notes

- Patched `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py` so `_build_runtime_state(...)` returns:
  - `resolved_windows`
  - `resolved_tps`
  - `resolved_sls`
  - `script_alias`
- Patched `run_multiwindow(...)` to print an `[INIT-MATRIX]` line showing:
  - strategy alias
  - windows
  - TP list
  - SL list
  - product list
  - processors per product
- Extended `C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_breakout_runtime_state.py` to assert the resolved matrix values explicitly.

## Validation

Command:

```powershell
python -m pytest "C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_breakout_runtime_state.py"
```

Result:

```text
2 passed in 1.40s
```

## Remaining Action

- No further code action is required for the original matrix-expansion issue.
- Optional future improvement: write startup matrix summaries to a dedicated log file if console visibility remains unreliable.

## Risks/Notes

- File writes after restart can reflect closure of pre-restart positions, so they are not a reliable proxy for freshly loaded matrix breadth
- Console visibility for long-running launcher sessions remains unreliable, so direct short-lived monitored runs are a more dependable validation method

## Completion Status

- State: COMPLETE
- Timestamp: 2026-04-10 15:53:00 +01:00
- Next Action: Monitor for normal Rev/R_Rev trade generation; reopen only if a new runtime symptom appears
