# Task: Refactor Hardcoded Price URLs to Centralized Config

**Status:** IN PROGRESS
**Date:** 2026-03-12
**Version:** V20260312_0005

## 1. Understanding of Requirements
All instances of hardcoded price-fetching URLs (specifically `http://127.0.0.1:8001/api/vw_000_fx_quotes...`) must be removed from the source code and replaced with a dynamic lookup from `config.json`. This ensures that updating the port or endpoint in one place (`config.json`) propagates to the entire system.

## 2. Plan of Approach
1.  **Audit**: Search `C:\Users\edebe\eds\TradeApps\breakout\fs` for all remaining hardcoded `127.0.0.1:8000` and `127.0.0.1:8001` URLs.
2.  **Refactor `common.py`**:
    *   Identify functions using hardcoded fallbacks (e.g., `_candidate_api_urls`, `_fetch_api_leaders`).
    *   Update logic to strictly pull from `_load_config()['endpoints']` or a similar central source.
3.  **Validate**: Ensure the system still fetches prices correctly by checking logs or verifying the new port 8002 is being hit.

## 3. List of Changes
- [ ] Audit all hardcoded IP/Port references in `fs/`.
- [ ] Update `_candidate_api_urls` in `common.py` to remove hardcoded fallback lists.
- [ ] Update `_fetch_api_leaders` in `common.py` to pull its base URL from config.
- [ ] Verify no hardcoded URLs remain in `common.py`.

---
*Created by Gemini CLI - 2026-03-12 00:05*
