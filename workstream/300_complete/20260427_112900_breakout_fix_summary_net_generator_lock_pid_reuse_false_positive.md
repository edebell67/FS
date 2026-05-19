# Task: Fix Summary Net Generator Lock PID Reuse False Positive

## Created
- 2026-04-27 11:29:00

## Status
- Complete

## Request
- Fix `summary_net_generator.py` so `_summary_net.json` updates are not blocked by a stale `summary_gen.lock` when Windows reuses the old PID for an unrelated process.

## Scope
- Update the lock ownership check in `summary_net_generator.py`.
- Ensure the generator only aborts when the lock PID still belongs to the summary generator process.
- Preserve protection against true duplicate generator instances.

## Acceptance Criteria
- A stale lock containing a recycled PID does not block the generator.
- A real running `summary_net_generator.py` instance still blocks duplicate startup.
- The change is validated with code inspection and a syntax/compile check.

## Validation
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py`
- Inspect the updated lock-check code path.

## Implementation Notes
- Added `find_summary_generator_pids()` to detect real `python ... summary_net_generator.py` processes instead of trusting the lock PID alone.
- Updated generator startup to abort only when another actual summary generator PID exists.
- Preserved the existing lock file, but downgraded a live non-generator lock PID to a stale-lock warning instead of a hard abort.

## Validation Results
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py` passed.
- Direct helper probe from `fs/` returned `[]`, confirming no real summary generator process was active at validation time.
- Bounded startup run of `python C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py` no longer aborted on PID `20508`.
- [summary_gen_debug.log](/abs/path/C:/Users/edebe/eds/TradeApps/breakout/fs/summary_gen_debug.log:1) now shows:
  - `[STALE LOCK] Ignoring live non-generator PID 20508 from summary_gen.lock.`
  - `[INIT] Initializing live/2026-04-27/forex from existing _cld files...`

## Outcome
- Fix complete.
- The stale-lock / PID-reuse false positive no longer blocks generator startup.
