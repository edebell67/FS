Source: User traceback from `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
Task Summary: Fix the `ImportError` caused by `trade_viewer_api.py` importing `VERSION` from `fs/constants.py` when `constants.py` has the assignment accidentally commented out by a literal newline marker.
Context: `TradeApps/breakout/fs/constants.py`, `TradeApps/breakout/fs/trade_viewer_api.py`
Destination Folder: None
Dependency: None
Plan:
- [x] 1. Confirm the import failure root cause in `constants.py`.
  - [x] Test: Inspect `constants.py` and verify whether `VERSION` is defined as a Python binding.
  - Evidence: `constants.py` had `# datetime stamp: 2026-05-16 23:00`nVERSION = "V20260516_2300"` on one physical line, so `VERSION` was commented out.
- [x] 2. Restore a valid `VERSION` binding without changing API behavior.
  - [x] Test: Patch `constants.py` so `from constants import VERSION` succeeds.
  - Evidence: Split the comment and assignment onto separate lines.
- [x] 3. Validate the import path used by `trade_viewer_api.py`.
  - [x] Test: Run a Python import check from `TradeApps/breakout/fs`.
  - Evidence: `python -c "...; from constants import VERSION; print(VERSION)"` printed `V20260516_2300`; `python -m py_compile constants.py trade_viewer_api.py` passed.
Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/constants.py`
  - Objective-Proved: The malformed one-line comment/assignment was corrected so `VERSION` is a module-level binding.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -c "import sys; sys.path.insert(0, r'C:\Users\edebe\eds\TradeApps\breakout\fs'); from constants import VERSION; print(VERSION)"` -> `V20260516_2300`
  - Objective-Proved: `trade_viewer_api.py` can import `VERSION` from `constants.py`.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m py_compile "C:\Users\edebe\eds\TradeApps\breakout\fs\constants.py" "C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py"` -> exit code 0
  - Objective-Proved: The edited constants file and importing API module are syntactically valid.
  - Status: captured
Implementation Log:
- 2026-05-18 00:10:44 Created lifecycle record for the constants import failure.
- 2026-05-18 00:11:20 Confirmed `VERSION` was accidentally commented out by a literal backtick-n sequence.
- 2026-05-18 00:12:00 Updated `constants.py` so the timestamp comment and `VERSION` assignment are separate lines.
- 2026-05-18 00:12:30 Validated the direct import and Python compilation.
Changes Made:
- `TradeApps/breakout/fs/constants.py`: restored `VERSION = "V20260516_2300"` as an executable module-level assignment.
Validation:
- `python -c "import sys; sys.path.insert(0, r'C:\Users\edebe\eds\TradeApps\breakout\fs'); from constants import VERSION; print(VERSION)"` -> `V20260516_2300`
- `python -m py_compile "C:\Users\edebe\eds\TradeApps\breakout\fs\constants.py" "C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py"` -> passed
Risks/Notes:
- This is scoped to restoring the missing `VERSION` export only.
Completion Status: Complete - 2026-05-18 00:12:30
