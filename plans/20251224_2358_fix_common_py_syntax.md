# Plan to Fix Syntax Error in common.py

## 1. Issue Description
The user reported a `SyntaxError: unexpected character after line continuation character` in `c:\Users\edebe\eds\TradeApps\breakout\common.py` at line 1714.
Current code on line 1714 appears to be a malformed line resulting from a bad merge or edit:
`with open(sell_filepath, 'w') as f:\n                    json.dump(finalized, f, indent=2)`

## 2. Plan of Approach
I will correct the syntax by splitting the malformed line into two proper Python lines.

## 3. List of Changes
*   **`c:\Users\edebe\eds\TradeApps\breakout\common.py`**:
    *   [x] Replace line 1714 with:
        ```python
        with open(sell_filepath, 'w') as f:
            json.dump(finalized, f, indent=2)
        ```
    *   [x] Verify syntax using `py_compile`.
