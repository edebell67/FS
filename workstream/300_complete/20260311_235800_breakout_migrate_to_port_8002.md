# Task: Migrate Breakout UI to Market Prices API (Port 8002)

**Status:** IN PROGRESS
**Date:** 2026-03-11
**Version:** V20260311_2358

## 1. Understanding of Requirements
Update the `Breakout UI` configuration to use the new `market_prices_api` on port `8002`. This API serves prices directly from `Z:\algo_forex\prices\forex_prices.json` in-memory, replacing the slower database-backed endpoint.

## 2. Plan of Approach
1.  **Modify `config.json`**: Update the `endpoints` section to replace port `8001` database URLs with port `8002` DB-free URLs.
2.  **Verify**: Ensure the JSON structure remains valid.

## 3. List of Changes
- [ ] Update `live` endpoints in `config.json`.
- [ ] Update `sim` endpoints in `config.json`.
- [ ] Verify connectivity (manual verification by user).

---
*Created by Gemini CLI - 2026-03-11 23:58*
