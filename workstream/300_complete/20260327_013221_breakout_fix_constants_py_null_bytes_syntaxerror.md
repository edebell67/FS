# Task: Fix Null Bytes SyntaxError In Breakout constants.py

## Source
- User Directive: 2026-03-27

## Task Summary
Fix the `SyntaxError: source code string cannot contain null bytes` caused by `constants.py` encoding so `trade_viewer_api.py` can import it normally.

## Goal
Restore `constants.py` to valid Python source encoding and verify the import path works.

## Plan
- [x] 1. Inspect `constants.py` bytes and confirm the null-byte cause.
- [x] 2. Rewrite the file as plain UTF-8 text.
- [x] 3. Verify Python can import the module.
- [x] 4. Record the outcome.

## Implementation Log
- **2026-03-27 01:32**: Task created. Confirmed `constants.py` is UTF-16 LE with BOM and embedded null bytes from Python's perspective.
- **2026-03-27 01:34**: Decoded the intended file content and confirmed it only contained the version constant.
- **2026-03-27 01:35**: Removed the invalid encoded file and recreated `constants.py` as plain UTF-8 text.
- **2026-03-27 01:35**: Verified Python import succeeds and returns `VERSION = 'V20260327_0115'`.

## Findings
- The `SyntaxError` was caused by `C:\Users\edebe\eds\TradeApps\breakout\fs\constants.py` being saved as UTF-16 LE with BOM.
- Python source import expected normal text source and rejected the embedded null bytes.
- The underlying source content was intact; only the file encoding was wrong.

## Validation
- Byte inspection:
  - file had `63` null bytes before repair
- Restored file contents:
  - `# datetime stamp: 2026-03-27 01:15`
  - `VERSION = 'V20260327_0115'`
- Import check:
  - `import constants`
  - returned version `V20260327_0115`

## Outcome
`constants.py` has been restored to valid UTF-8 Python source and the null-byte import failure is fixed.
