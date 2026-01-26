Plan: Strategy08SR Historical Condition Exclusion

*   **File to modify**: `C:\Users\edebe\eds\algo_viewer\tradepanel\strategies\s08sr.py`
*   **Changes**:
    1.  Copy the `evaluate` method's content from `Strategy08S` (from `tradepanel/strategies/s08s.py`).
    2.  Replace the existing `evaluate` method in `Strategy08SR` with this copied content.
    3.  Within the new `evaluate` method in `Strategy08SR`, locate the lines that calculate `hist_buy_ok` and `hist_sell_ok` and change their assignments to `True`.
    4.  Add a comment ` # 2025-07-30: NEXT_VERSION_NUMBER - Historical condition excluded for S08SR` to these lines.
    5.  Re-integrate the existing `Strategy08SR`-specific logic (recalculating the `S07/S08` entry threshold when the trade book is flat) at the end of this new `evaluate` method.
*   **Version Number**: `64_3_19`
*   **Plan File**: `C:\Users\edebe\eds\plans\20250730_2105_64_3_19_Strategy08SR_Historical_Condition_Exclusion.md`