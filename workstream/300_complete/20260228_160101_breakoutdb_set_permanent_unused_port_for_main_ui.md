# Source
- User request on 2026-02-28: use an unused port permanently for DB main screen.

# Task Summary
Set permanent default port for `trade_viewer_api.py` and provide run URL for `strategy_performance.html`.

# Context
- File: `TradeApps/breakout/DB/trade_viewer_api.py`

# Implementation Log
- 2026-02-28 16:01:01: Task created and moved to in-progress.
- 2026-02-28 16:02: Updated app entrypoint to use permanent default port `5051` with env override via `BREAKOUT_DB_PORT`.

# Changes Made
- `TradeApps/breakout/DB/trade_viewer_api.py`
  - Replaced hardcoded `5001` with:
    - `port = int(os.getenv("BREAKOUT_DB_PORT", "5051"))`
    - startup log includes active port
    - `app.run(... port=port ... )`

# Validation
- Command: `python -m py_compile TradeApps/breakout/DB/trade_viewer_api.py`
- Result: `py_compile_ok`

# Risks/Notes
- If port `5051` is already occupied on a machine, set `BREAKOUT_DB_PORT` explicitly.

# Completion Status
- Complete (2026-02-28 16:02)
