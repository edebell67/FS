Source: User report on 2026-04-02 that `TradeApps\breakout\fs\trade_viewer_api.py` fails importing `constants.py` with `SyntaxError: source code string cannot contain null bytes`.

Task Type: bugfix
Project: breakout

## Objective
- Repair `C:\Users\edebe\eds\TradeApps\breakout\fs\constants.py` so it is valid Python source and importable by `trade_viewer_api.py`.
- Preserve the existing version value while removing the encoding issue that introduced null bytes.

## Plan
- [x] 1. Inspect the current `constants.py` bytes and decoded content.
  - [x] Test: Confirm the file contains null bytes or invalid source encoding for direct Python import.
  - Evidence: Original file bytes showed `size=128 nulls=63`, and decoding as UTF-16 revealed the intended 2-line source.
- [x] 2. Rewrite `constants.py` as UTF-8 Python source without null bytes.
  - [x] Test: Confirm the rewritten file contains the expected `VERSION` constant only and no null bytes.
  - Evidence: Rewritten file bytes show `size=64 nulls=0` and contain only the timestamp comment plus `VERSION = "V20260402_0110"`.
- [x] 3. Validate importability from the breakout runtime path.
  - [x] Test: `python -c` import of `constants` from `C:\Users\edebe\eds\TradeApps\breakout\fs` succeeds.
  - Evidence: direct import printed `V20260402_0110`; `python -m py_compile trade_viewer_api.py` also passed.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\constants.py`
  - Objective-Proved: Proves `constants.py` was rewritten into valid source form.
  - Status: complete
- Evidence-Type: test_output
  - Artifact: byte inspection output; direct `constants` import; `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - Objective-Proved: Proves the file no longer contains null bytes and imports successfully.
  - Status: complete

## Implementation Log
- 2026-04-02 02:08:54 Europe/London: Task created to fix `constants.py` null-byte import failure.
- 2026-04-02 02:09 Europe/London: Confirmed `constants.py` was UTF-16 encoded and contained 63 null bytes, which made Python reject it as source.
- 2026-04-02 02:09 Europe/London: Rewrote `constants.py` as UTF-8 source while preserving `VERSION = "V20260402_0110"`.
- 2026-04-02 02:10 Europe/London: Validated direct import of `constants` and syntax compilation of `trade_viewer_api.py`.

## Changes Made
- Replaced the invalid UTF-16 `C:\Users\edebe\eds\TradeApps\breakout\fs\constants.py` with a normal UTF-8 Python source file.
- Preserved the existing version constant value: `V20260402_0110`.

## Validation
- Original bytes
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\constants.py` reported `size=128 nulls=63`
- Rewritten bytes
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\constants.py` reported `size=64 nulls=0`
- Direct import
  - `python -` with `sys.path.insert(0, r'C:\Users\edebe\eds\TradeApps\breakout\fs'); import constants; print(constants.VERSION)`
  - Result: `V20260402_0110`
- Syntax validation
  - `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - Result: pass

## Risks/Notes
- Keep the current `VERSION` value intact while changing only file encoding/source validity.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-02 02:10:30 Europe/London
