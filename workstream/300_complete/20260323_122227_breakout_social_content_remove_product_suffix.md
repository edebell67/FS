Source: User request

Task Summary: Remove _C/_S suffix from product names in social content output (combo indicator not needed for display).

Context:
- Project: TradeApps/breakout
- File Modified: `TradeApps/breakout/fs/social_content_generator.py`

Priority: 1

## Objective

Remove the `_C` (combo) and `_S` suffixes from product names in Twitter output, as these are internal indicators not needed for public display.

## Plan

- [x] 1. Add `clean_product_name()` helper function
  - [x] Strip `_C` and `_S` suffixes from product names
  - [x] Evidence: Function added at line 180-182

- [x] 2. Update Twitter templates to use cleaned names
  - [x] `generate_twitter_signal_alert()` - clean product name
  - [x] `generate_twitter_leaderboard()` - clean leader names
  - [x] `generate_twitter_performance_recap()` - clean product name
  - [x] Evidence: All 3 functions updated

- [x] 3. Test output
  - [x] Verify NZDAUD_C now displays as NZDAUD
  - [x] Evidence: Output confirmed

## Changes Made
- Modified `TradeApps/breakout/fs/social_content_generator.py`:
  - Added `clean_product_name()` function (lines 180-182)
  - Updated `generate_twitter_signal_alert()` to use cleaned name (line 243)
  - Updated `generate_twitter_leaderboard()` to use cleaned name (line 281)
  - Updated `generate_twitter_performance_recap()` to use cleaned name (line 314)

## Sample Output
Before: `NZDAUD_C` -> After: `NZDAUD`

## Evidence
Objective-Delivery-Coverage: 100%
- Evidence-Type: code_output
  - Status: complete

## Implementation Log
- 2026-03-23 12:22: User requested removal of _C suffix from product names
- 2026-03-23 12:22: Added clean_product_name() and updated all Twitter templates

Completion Status: Complete
