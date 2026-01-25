# Plan: PostgreSQL P&L Performance & Live Update Fix
**Date:** 2026-01-21 14:51
**Version:** V20260121_1450

## 1. Requirements
- Ensure `strategy_performance.html` loads instantly despite 300k+ historical trades.
- Ensure "Exit Price" and "Net P&L" update in real-time on the frontend.
- Fix the `pnl_update_service.py` to correctly fetch and sync quotes.
- Fix SQL stored procedure errors (ambiguous columns).

## 2. Approach
- **Database**: 
    - Restrict `vw_trades_all` and `vw_strategy_performance_live` to `CURRENT_DATE` to avoid heavy scans.
    - Use index-friendly range searches (`>= CURRENT_DATE`).
    - Fix variable naming in `process_open_trades` to avoid PostgreSQL ambiguity errors.
- **API (`trade_viewer_api.py`)**:
    - Separate `/api/trades` and `/api/stats_summary` routes (was colliding).
    - Update endpoints to consume the optimized views.
    - Add logic to handle historical dates via table aggregation and current date via the live view.
- **Service (`pnl_update_service.py`)**:
    - Fix JSON parsing for quotes API (needs to look in `.data`).
    - Uppercase product codes to match database constraints.

## 3. Checklist
- [x] Create optimized "Today-Only" views (`vw_trades_all`, `vw_strategy_performance_live`).
- [x] Fix ambiguous column error in `process_open_trades` stored procedure.
- [x] Fix API routing collision in `trade_viewer_api.py`.
- [x] Fix syntax error in `trade_viewer_api.py` (missing except block).
- [ ] Verify `pnl_update_service.py` is running without errors.
- [ ] Confirm frontend performance is restored.
- [ ] Confirm Live P&L and Exit Prices are ticking.
- [ ] Update `Constants.py` with new version V20260121_1450.

## 4. Progress Log
- **14:22**: Created `get_live_strategy_stats` function for optimized aggregation.
- **14:24**: Created `trades_archive` system (user opted to skip physical move for now).
- **14:41**: Refactored views to use `CURRENT_DATE` restriction.
- **14:46**: Fixed SQL typo in view replacement and applied index-friendly range.
- **14:48**: Fixed API routing in `trade_viewer_api.py`.
- **14:50**: Fixed missing `except` block in API.
