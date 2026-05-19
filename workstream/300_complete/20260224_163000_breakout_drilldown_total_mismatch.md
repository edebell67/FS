# Breakout: Fix Drilldown Total Mismatch in Strategy Performance

**Created:** 2026-02-24 16:30
**Project:** Breakout
**Status:** Complete

---

## Task Summary

Fix the mismatch between summary totals and drilldown trade totals in `strategy_performance.html` when viewing Performance Summary at product level.

---

## Context

**File:** `TradeApps/breakout/fs/strategy_performance.html`

**Issue:** When Performance Summary is selected and data displays at product level, clicking on buy/sell/total net values drills down to show trade list. The total net of displayed trades does not match the summary number on the parent page.

**Root Cause Analysis:**

1. Summary hierarchy aggregates data as: Category → Window → Ratio → Product
2. Multiple strategies with same (cat, window, ratio, product) get stats SUMMED into ONE product node
3. BUT only the FIRST entry's `parm_raw` is stored in `prodNode.meta.parm_raw` (line 5117)
4. Drilldown calls `showDrillDown(product, 'all', prodNode.meta.parm_raw, direction)`
5. This filters by a SINGLE `parm_raw`, missing trades from other strategies in the same summary bucket

**Evidence:**
- Line 5117: `meta: { strategy: d.strategy, parm_raw: d.parm_raw || d.params }` - only set on first creation
- Line 5328-5337: Drilldown uses `prodNode.meta.parm_raw` which is only ONE value
- `summaryRowMembers` (line 5104-5105) already tracks ALL strategies per bucket but wasn't used in drilldown

---

## Implementation Log

### Attempt 1 (V20260224_1630) - FAILED
- Tried using `summaryRowMembers` to get list of strategies per bucket
- Problem: Model name matching was too loose, showed trades from all 4 strategy families
- User feedback: "requires the user to select the trades by using the strategy filter again"

### Attempt 2 (V20260224_1700) - Current Fix
**Approach:** Filter by CATEGORY (strategy family) directly, using same logic as aggregation

### Step 1: Modified showDrillDown Function (lines 2825-2855)
- Changed 6th parameter from `memberKey` to `summaryCategory`
- Parse category from first part of key (e.g., "Breakout Standard" from "Breakout Standard|Window 2|...")
- Keep original fetch logic (fetch by params, not all trades)
- Version tag: `[V20260224_1700]`

### Step 2: Added Category Matching Helper (lines 2901-2909)
- Added `getTradeCategory(modelName)` function
- Uses EXACT same logic as summary aggregation:
  - `breakout_r_rev*` → "Breakout R_Rev"
  - `breakout_rev*` → "Breakout Rev"
  - `breakout_r*` → "Breakout R"
  - `breakout*` → "Breakout Standard"

### Step 3: Updated Filtering Logic (lines 2921-2936)
- When `categoryFilter` is set:
  - Check trade's category matches expected category
  - AND check params (TP/SL) match
- Else: use original matching logic (backwards compatible)

### Step 4: Updated Product-Level Drilldown Calls (lines 5356-5371)
- Pass full hierarchy key as `summaryCategory` parameter
- Category extracted from key at runtime

### Step 5: Added Total Row to Drilldown Table (lines 3106-3120)
- Shows TOTAL row at bottom with sum of net_return and alt_net
- Makes comparison with summary totals easy

---

## Changes Made

**File:** `fs/strategy_performance.html`

| Line Range | Change |
|------------|--------|
| 2825-2855 | Changed to `summaryCategory` param, parse category from key |
| 2901-2909 | Added `getTradeCategory()` helper function |
| 2921-2936 | Category-based filtering when `categoryFilter` is set |
| 2986-2991 | Use category in drilldown title for clarity |
| 3106-3120 | Added total row to drilldown table |
| 5356-5371 | Pass full hierarchy key as `summaryCategory` |

---

## Validation

- [x] Click product-level buy net in summary → drilldown total should match summary
- [x] Click product-level sell net in summary → drilldown total should match summary
- [x] Click product-level total net in summary → drilldown total should match summary
- [x] Trade count in drilldown matches summary count
- [x] Other drilldown paths (non-summary) still work correctly (categoryFilter=null falls back to original logic)

---

## Risks/Notes

- Backwards compatible: When `memberKey` is null, original filtering logic is used
- Console logging added for debugging: `[DRILLDOWN] Using summary bucket...`
- Total row only appears when there are trades to display

---

## Completion Status

**Status:** COMPLETE
**Completion Date:** 2026-02-24
