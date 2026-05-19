# Task Summary
Add explicit archive source/target path logging when archive is detected to avoid date-folder confusion.

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
- Minimal logging-only change.

## Completion Status
- In progress.

## Implementation Log
- Added explicit archive context logs at detection and execution points.
- Included mode/date/source/target path output to remove ambiguity around which folder is being processed.

## Changes Made
- `TradeApps/breakout/fs/common.py`
  - Added `[ARCHIVE-DETECT] archive=true mode=... date=...` in both archive detection paths.
  - Added `[ARCHIVE-CONTEXT] mode=... date=... source=... target=...` inside `_perform_archiving`.
- `TradeApps/breakout/fs/archive.py`
  - Added `[ARCHIVE-CONTEXT] mode=... date=... source=... target=...` before invoking `_perform_archiving`.

## Validation
- Syntax check passed:
  - `python -m py_compile TradeApps/breakout/fs/common.py TradeApps/breakout/fs/archive.py`
- Confirmed log markers exist:
  - `ARCHIVE-DETECT`
  - `ARCHIVE-CONTEXT`

## Risks/Notes
- Logging-only change; no archive decision logic modified.

## Completion Status
- Completed on 2026-02-23.
