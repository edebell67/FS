# Source
- User request in Codex thread on 2026-03-26 to add a freshness guard after confirming stale forex quotes had caused missing forex trades.

# Task Summary
Add a configurable quote-freshness guard so stale market data is logged and skipped before it can silently suppress trade generation.

# Context
- `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`

# Dependency
Dependency: None

# Plan
- [x] 1. Identify the runtime point where latest quotes are handed to breakout processors.
  - [x] Test: Inspect the live loop in `run_multiwindow()` and confirm where fetched ticks are processed.
  - [x] Evidence: Located the `latest_tick = quotes[-1]` branch immediately before `processor.process_new_tick(...)`.
- [x] 2. Add configurable max quote age thresholds by product type.
  - [x] Test: Add `max_quote_age_seconds_by_product_type` to config and a resolver helper in `common.py`.
  - [x] Evidence: Config now contains thresholds for `crypto`, `energy`, `forex`, `indices`, and `metals`; `common.py` now contains `_max_quote_age_seconds_for_product()`.
- [x] 3. Enforce the guard in the live loop.
  - [x] Test: Skip processing when the latest quote timestamp is older than the configured threshold and emit a warning.
  - [x] Evidence: The live loop now computes quote age and logs `[WARN] Stale quote skipped for ...` before continuing.
- [x] 4. Record the change and leave the task ready for user verification.
  - [x] Test: Update the lifecycle record with the implementation and validation notes.
  - [x] Evidence: This lifecycle file captures the config/code change and intended runtime behavior.

# Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
  - Objective-Proved: Confirms quote age thresholds are configurable by product type.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
  - Objective-Proved: Confirms stale quotes are now checked and skipped in the live processing loop.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: pending
  - Objective-Proved: Will confirm at runtime that stale forex quotes are surfaced as warnings instead of silently producing a `NO_DATA` day.
  - Status: planned

# Implementation Log
- 2026-03-26 11:37:38 Created lifecycle file for quote-freshness guard.
- 2026-03-26 11:37:38 Added `max_quote_age_seconds_by_product_type` config.
- 2026-03-26 11:37:38 Added `_max_quote_age_seconds_for_product()` to `common.py`.
- 2026-03-26 11:37:38 Added stale-quote checks to the live processing loop before `process_new_tick(...)`.

# Changes Made
- Updated `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json` with:
  - `crypto: 60`
  - `energy: 120`
  - `forex: 60`
  - `indices: 120`
  - `metals: 120`
- Updated `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py` to:
  - resolve per-product-type max quote age
  - skip stale quotes in `run_multiwindow()`
  - log product, age, timestamp, and threshold when a stale quote is skipped

# Validation
- Reviewed the live loop and confirmed the stale check runs before:
  - latest price cache update
  - trading-date update
  - processor tick handling
- Expected runtime behavior:
  - stale forex quotes older than 60 seconds are skipped
  - stale crypto quotes older than 60 seconds are skipped
  - stale futures/energy/indices/metals quotes older than 120 seconds are skipped
  - warning lines identify which product is stale and by how much

# Risks/Notes
- This change prevents stale data from being processed, but it does not repair the upstream feed.
- If an upstream feed pauses, the symptom will now be visible in logs rather than silently degrading into no-trade output.
- User verification is still needed against a live stale-feed scenario or a normal healthy run.

# Completion Status
Awaiting user verification - 2026-03-26 11:37:38


# User Feedback
User Verified: PASS
