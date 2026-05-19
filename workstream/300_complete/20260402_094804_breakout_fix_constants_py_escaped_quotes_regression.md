Source: User report on 2026-04-02 that `TradeApps\breakout\fs\constants.py` now fails with `SyntaxError: unexpected character after line continuation character` because the `VERSION` assignment contains escaped quotes as literal source.

Task Type: bugfix
Project: breakout

## Objective
- Repair `C:\Users\edebe\eds\TradeApps\breakout\fs\constants.py` so the `VERSION` assignment is valid Python syntax.
- Validate that `trade_viewer_api.py` can compile/import against the corrected file.

## Plan
- [x] 1. Inspect the current `constants.py` content and confirm the invalid escaped-quote syntax.
  - [x] Test: Confirm the file contains `VERSION = \"...\"` as literal source.
  - Evidence: `Get-Content` showed `VERSION = \"V20260402_0518\"` and raw bytes showed the backslashes were literal file contents.
- [x] 2. Patch `constants.py` to a valid plain Python assignment.
  - [x] Test: Confirm the file contains `VERSION = "..."` and no literal backslashes before the quotes.
  - Evidence: Patched file now reads `VERSION = "V20260402_0518"` and raw bytes no longer contain backslashes before the quotes.
- [x] 3. Validate importability from the breakout runtime path.
  - [x] Test: direct import of `constants.VERSION` and `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` both succeed.
  - Evidence: direct import printed `V20260402_0518`; compile passed.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\constants.py`
  - Objective-Proved: Proves the `VERSION` assignment was corrected to valid Python syntax.
  - Status: complete
- Evidence-Type: test_output
  - Artifact: `Get-Content` / raw byte inspection; direct `constants` import; `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - Objective-Proved: Proves the corrected file imports and the API module compiles.
  - Status: complete

## Implementation Log
- 2026-04-02 09:48:04 Europe/London: Task created to fix the `constants.py` escaped-quote regression.
- 2026-04-02 09:49 Europe/London: Confirmed the file contained the literal source `VERSION = \"V20260402_0518\"`.
- 2026-04-02 09:49 Europe/London: Patched the assignment back to normal Python quoting while preserving the version value.
- 2026-04-02 09:49 Europe/London: Validated direct import and `trade_viewer_api.py` compilation successfully.

## Changes Made
- Corrected `C:\Users\edebe\eds\TradeApps\breakout\fs\constants.py` from `VERSION = \"V20260402_0518\"` to `VERSION = "V20260402_0518"`.

## Validation
- File content
  - `Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\constants.py`
  - Result: `VERSION = "V20260402_0518"`
- Raw bytes
  - Result: `b'# datetime stamp: 2026-04-02 05:18\nVERSION = "V20260402_0518"\n'`
- Direct import
  - `python -` with `sys.path.insert(0, r'C:\Users\edebe\eds\TradeApps\breakout\fs'); import constants; print(constants.VERSION)`
  - Result: `V20260402_0518`
- Syntax validation
  - `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - Result: pass

## Risks/Notes
- Preserve the current version value while removing only the invalid escape characters.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-02 09:49:40 Europe/London
