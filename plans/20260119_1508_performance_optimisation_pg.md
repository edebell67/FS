# Performance Optimization Plan: Database Migration (targeted)

This document outlines the plan to solve the performance issue by switching the data source from the file system to PostgreSQL.

## 1. Understanding of Requirements
The system has over 400,000 JSON files, causing "dire" performance lag in the UI. Transitioning to a database-driven API will resolve this. The user requires a ZERO-IMPACT approach for their live scenario.

## 2. Plan of Approach
The plan involves targeted synchronization of recent data to PostgreSQL and switching the API mode without disrupting the live trading bots.

1.  **Phase 1: Targeted Backfill (Today & Yesterday)**
    *   Initialize/Verify PostgreSQL connection in `.env`.
    *   Run `backfill_trades.py` specifically for `2026-01-19` and `2026-01-18`.
2.  **Phase 2: Database Source Activation**
    *   Update `config.json` to set `"DATA_SOURCE": "database"`.
    *   Restart the `trade_viewer_api.py` server to pick up the change.
3.  **Phase 3: Automated Sync Setup**
    *   Advise the user to schedule the backfill script for continuous updates.

## 3. List of Changes
*   **`backfill_trades.py`**: Hardcoded TARGET_DATES to `2026-01-19, 2026-01-18` for safety. [x]
*   **`config.json`**: Update `DATA_SOURCE` to `database`. [x]
*   **Verification**: Ensure today's trades appear in the DB via API. [x]

## 4. Verification
- [x] Targeted backfill for `2026-01-19, 2026-01-18` completes. (Done: 45646 files)
- [x] `DATA_SOURCE` flipped to `database`.
- [x] API server restarted and responding with DB data.
- [x] Version remains consistent and performance verified (~0.7s for 500 trades).
- [ ] Fix JavaScript `replace` error in `trade_viewer.html`.
- [ ] Implement continuous sync loop (1 min) in `backfill_trades.py`.

## 5. Action Log
- **2026-01-19 15:08**: Created performance optimization plan.
- **2026-01-19 15:10**: Attempted to run backfill with env var, failed to propagate correctly.
- **2026-01-19 15:11**: Modified `backfill_trades.py` to hardcode `2026-01-19, 2026-01-18` as default for safety.
- **2026-01-19 15:13**: Started targeted backfill (Command ID: 0ab55195-4061-4120-bc5d-9f64f95fb2cf).
- **2026-01-19 15:58**: Verified backfill completion: 45,646 files processed successfully.
- **2026-01-19 16:05**: Switched `config.json` to `database` mode.
- **2026-01-19 16:06**: Triggered API reload by touching `trade_viewer_api.py`.
- **2026-01-19 16:08**: Verified API response: `data_source` is `database`, response time ~0.7s (Fixed).
