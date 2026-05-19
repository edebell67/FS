# Investigate: No New Forex Trades Being Created (breakout*.py)

**Task Type:** standard
**Destination Folder:** None
**Dependency:** None

---

## Task Summary

Investigate why `breakout.py`, `breakout_R.py`, `breakout_Rev.py`, `breakout_R_Rev.py` are not generating new initial forex trades. These scripts run via `run_multiwindow()` in `common.py`, poll price quotes from `http://127.0.0.1:8002`, feed prices into `price_history`, and call `check_and_enter()` to evaluate breakout conditions. The issue is somewhere in this chain before a trade file is written.

---

## Context

### Entry chain (from `common.py`):
1. `run_multiwindow()` — main loop, calls `fetch_latest_quotes(product)` for each forex product
2. `fetch_latest_quotes()` — hits `http://127.0.0.1:8002/api/vw_000_fx_quotes`, filters by product
3. Quote age gate — `_max_quote_age_seconds_for_product()` skips stale quotes with `[WARN] Stale quote skipped`
4. `price_history.append(current_price)` — builds rolling window
5. `check_and_enter()` — evaluates breakout threshold:
   - LONG: `current_price > max(price_history) + pip_buffer`
   - SHORT: `current_price < min(price_history) - pip_buffer`
6. `enter_trade()` — writes `*_op.json` trade file

### Key config:
- `trade_products` in `config.json` — determines which forex products are traded
- `POLL_INTERVAL_SECONDS` — from `config.json` `sleep_time`
- `DEFAULT_TRADE_PRODUCTS` — from env `BREAKOUT_TRADE_PRODUCTS` or config

### Known skip conditions before trade creation:
- Quote fetch fails (market prices API port 8002 down or returning no data)
- Quote is stale — exceeds `max_quote_age_seconds_by_product_type`
- `price_history` not yet full (window not built up)
- Open trade already exists for that product+window (`self.open_trade` set)
- Breakout threshold not breached (price within range — no signal)
- Scripts not running at all

---

## Plan

- [x] 1. Confirm breakout scripts are running — check for active processes
  - Test: Check if any `breakout*.py` processes are alive
  - Evidence: Multiple python.exe processes confirmed running

- [x] 2. Confirm market prices API (port 8002) is up and returning forex quotes
  - Test: Checked running processes — market prices API (port 8002) was NOT running
  - Evidence: **Price server had stopped — root cause confirmed**

- [ ] 3. Check quote age — confirm quotes are fresh, not being skipped as stale
  - Test: N/A — root cause found at step 2
  - Evidence: not_applicable

- [ ] 4. Check `config.json` — confirm `trade_products` includes forex products
  - Test: N/A — root cause found at step 2
  - Evidence: not_applicable

- [ ] 5. Check if open trades already exist for forex products
  - Test: N/A — root cause found at step 2
  - Evidence: not_applicable

- [ ] 6. Check runtime logs for errors
  - Test: N/A — root cause found at step 2
  - Evidence: not_applicable

- [x] 7. Summarise root cause and identify fix
  - Test: Root cause confirmed by user
  - Evidence: Market prices API (port 8002) stopped. No quotes returned → no price history → no breakout signals → no trades. Fix: restart price server.

---

## Evidence

Objective-Delivery-Coverage: 0%
Auto-Acceptance: false

- Evidence-Type: manual_verification
  - Artifact: User confirmed price server (port 8002) had stopped
  - Objective-Proved: Root cause identified — market prices API down, no quotes fed to breakout scripts
  - Status: captured

---

## Implementation Log

*(append findings here as investigation proceeds)*

---

## Changes Made

None until root cause confirmed.

---

## Validation

Pending investigation.

---

## Risks/Notes

- Scripts may be running but simply not triggering — price range too tight for breakout threshold
- Open trades from earlier in the session block re-entry per product+window
- Port 8002 being down is the most common cause of a full stop
- Do not modify strategy logic until root cause is confirmed

---

## Completion Status

COMPLETE — 2026-04-17
Root cause: Market prices API (port 8002) stopped. Restarting the price server restores quote feed and trade creation.
