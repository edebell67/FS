# Task: NotebookLM Reinstall CLI Python313

## Source
- User Directive: 2026-03-26

## Task Summary
Reinstall the NotebookLM CLI/MCP tooling into the active Python 3.13 environment so `nlm.exe` works again on this machine.

## Context
- Active Python version:
  - `C:\Python313\python.exe`
- Broken legacy shim:
  - `C:\Users\edebe\AppData\Roaming\Python\Python312_bkup\Scripts\nlm.exe`
- Failure observed:
  - `ModuleNotFoundError: No module named 'notebooklm_tools'`

## Plan
- [x] 1. Confirm the Python 3.13 pip target and script location.
- [x] 2. Install or reinstall the NotebookLM CLI package into Python 3.13.
- [x] 3. Validate that `nlm.exe` or the Python module runs correctly from the repaired environment.

## Validation
- Confirmed active Python:
  - `C:\Python313\python.exe`
- Install command:
  - `py -3.13 -m pip install --user notebooklm-mcp-cli`
- Installed package:
  - `notebooklm-mcp-cli 0.5.9`
- Verified CLI startup:
  - `C:\Users\edebe\AppData\Roaming\Python\Python313\Scripts\nlm.exe --help`
- Result:
  - `nlm.exe` starts correctly and exposes the expected command set including `login`, `audio`, `video`, `download`, and `setup`

## Implementation Log
- **2026-03-26 14:20**: Task created.
- **2026-03-26 14:24**: Confirmed Python 3.13 as the active interpreter and verified `notebooklm-mcp-cli` was not installed there.
- **2026-03-26 14:26**: Installed `notebooklm-mcp-cli` into the Python 3.13 user environment.
- **2026-03-26 14:27**: Verified the repaired `nlm.exe` launcher under `Python313\\Scripts`.
- **2026-03-26 14:28**: Updated NotebookLM skill/docs to point at the repaired Python 3.13 CLI path.

## Changes Made
- Installed into Python 3.13 user environment:
  - `notebooklm-mcp-cli 0.5.9`
- Updated:
  - `C:\Users\edebe\eds\skills\notebooklm-video-automation\SKILL.md`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\notebooklm_weekly_returns\README.md`

## Risks/Notes
- The install upgraded some shared Python 3.13 user-site dependencies, including `starlette`, `typing-extensions`, and `uvicorn`.
- `pip` reported dependency conflicts with existing packages such as `fastapi` and `selenium`.
- NotebookLM CLI is now functional, but if any unrelated Python 3.13 tooling starts failing, these user-site dependency changes are the first place to inspect.

## Completion Status
**Complete** - 2026-03-26 14:28
