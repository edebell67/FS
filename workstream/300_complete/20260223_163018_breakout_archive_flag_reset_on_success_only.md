# Task Summary
Fix archive flag behavior so config.archive resets to false only after successful archive completion (source day folder emptied as expected), not immediately on failed attempts.

## Context
- TradeApps/breakout/fs/common.py
- TradeApps/breakout/fs/archive.py

## Implementation Log
- Created lifecycle task and moved to in-progress.

## Changes Made
- Pending.

## Validation
- Pending.

## Risks/Notes
- Pending.

## Completion Status
- In progress.

## Implementation Log
- Inspected archive execution and flag reset points in:
  - `TradeApps/breakout/fs/common.py`
  - `TradeApps/breakout/fs/archive.py`
- Identified unconditional reset behavior (`archive=false` in finally/post-attempt blocks).
- Updated flow to reset archive flag only when archive completes successfully.

## Changes Made
- `TradeApps/breakout/fs/common.py`
  - Changed `_perform_archiving` signature to return `bool` success.
  - Returns `False` on skip/error/no-move cases.
  - Returns `True` only when archive move path completes.
  - Updated two caller paths to:
    - set `config['archive']=False` only when `archived_ok` is true.
    - keep `archive=True` on incomplete/failed attempts.
- `TradeApps/breakout/fs/archive.py`
  - Replaced unconditional `finally` reset.
  - Now resets `archive` only when `_perform_archiving(cfg)` returns success.

## Validation
- Syntax validation passed:
  - `python -m py_compile TradeApps/breakout/fs/common.py TradeApps/breakout/fs/archive.py`
- Confirmed new conditional reset markers:
  - `common.py` includes `archived_ok` and `[ARCHIVE-PENDING]` branches.
  - `archive.py` includes `archived_ok` and retains flag on incomplete/skip.

## Risks/Notes
- If archive repeatedly skips/errors (e.g., missing source folder), `archive` now remains true by design until a successful run.
- This aligns with requirement to avoid immediate false reset without actual completion.

## Completion Status
- Completed on 2026-02-23.
