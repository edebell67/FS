# Implementation Plan: Per-Title Trade Filter Allocation

**Version**: 20251127_01  
**Date**: 2025-11-27 01:11 UTC  
**Feature**: Real-Time (RT) Trade Filter Management - Per-Title Filter Allocation

---

## 1. Understanding of Requirements

The goal is to implement a system that allows **different trade filters to be assigned to different trade titles**. Currently, the filter system only supports a global `active_filters` list that applies to ALL trades. This is insufficient for managing multiple trading strategies with different filtering needs.

### Core Requirements:
1. **Per-Title Filter Assignment**: Each trade title should be able to have its own set of active filters
2. **UI for Filter Management**: A new page in `trade_monitor.py` to manage filter assignments
3. **Flexible Allocation**: Support for:
   - Assigning filters to individual trade titles
   - Applying filters to all trade titles at once
   - De-allocating filters from trade titles
4. **Drill-Down Analysis**: View which trades passed specific filters and their performance
5. **Backward Compatibility**: Existing trades and configurations should continue to work

### Current State:
- ✅ `filters.py` exists with `apply_filters()` function and one filter implemented
- ✅ `simple_trend_trader.py` calls `apply_filters()` but uses global `active_filters` list
- ✅ `config.json` exists but has no filter-related fields
- ✅ `config_trade.json` has all trade title configurations
- ❌ No per-title filter allocation mechanism
- ❌ No UI for filter management
- ❌ No `trade_filter_allocations.json` file

---

## 2. Plan of Approach

### Phase 1: Data Model & Configuration
1. Rename conceptual `active_filters` → `available_filters` in `config.json` (master list)
2. Create new `trade_filter_allocations.json` file (per-title assignments)
3. Define JSON schema for allocations file

### Phase 2: Backend Logic Updates
1. Modify `simple_trend_trader.py`:
   - Load `trade_filter_allocations.json` at startup
   - Update `save_trade_state_to_json()` to use per-title filters
   - Pass title-specific filter list to `apply_filters()`
2. Add helper functions for allocation file management

### Phase 3: UI Implementation (trade_monitor.py)
1. Add "RT Trade Filter" menu item to main menu
2. Create new page with:
   - Left pane: Listbox of active trade titles
   - Right pane: Checkbuttons for available filters
   - Action buttons: Save, Apply to All, Clear
3. Implement drill-down feature:
   - Combobox for filter selection
   - Treeview for displaying filtered trades
   - Performance metrics display

### Phase 4: Testing & Verification
1. Test filter allocation persistence
2. Test per-title filter application
3. Test UI interactions
4. Verify backward compatibility

---

## 3. Detailed Implementation Checklist

### 3.1 Configuration Files

- [ ] **`config.json`** (C:\Users\edebe\eds\Trades\config.json)
  - [ ] Add `"available_filters": ["prev_closed_same_signal_alt_net_negative"]`
  - [ ] Document this as the master list of all possible filters
  - [ ] Tag: `20251127_01`

- [ ] **`trade_filter_allocations.json`** (NEW FILE: C:\Users\edebe\eds\Trades\trade_filter_allocations.json)
  - [ ] Create new file with initial structure
  - [ ] Schema: `{ "TRADE_TITLE": ["filter1", "filter2"], ... }`
  - [ ] Initialize as empty object `{}`
  - [ ] Tag: `20251127_01`

### 3.2 Backend Logic (simple_trend_trader.py)

- [ ] **Load allocation file at startup**
  - [ ] Add global variable: `trade_filter_allocations = {}`
  - [ ] Create function: `load_trade_filter_allocations()`
  - [ ] Call in `load_app_config()` or at startup
  - [ ] Tag: `20251127_01`

- [ ] **Modify `save_trade_state_to_json()` function** (around line 570-577)
  - [ ] Get trade title from `trade_data['Trade Title']`
  - [ ] Look up filters for this title in `trade_filter_allocations`
  - [ ] Default to empty list `[]` if title not found
  - [ ] Pass title-specific filters to `apply_filters()`
  - [ ] Update comment to reflect per-title filtering
  - [ ] Tag: `20251127_01`

- [ ] **Add helper functions**
  - [ ] `load_trade_filter_allocations()` - Load allocations from JSON
  - [ ] `save_trade_filter_allocations(allocations)` - Save allocations to JSON
  - [ ] Tag: `20251127_01`

### 3.3 UI Implementation (trade_monitor.py)

- [ ] **Add menu item**
  - [ ] Define new page constant: `PAGE_RT_TRADE_FILTER = 7`
  - [ ] Add to `PAGE_TITLES_MAP`: `"RT Trade Filter Management"`
  - [ ] Add to `MAIN_MENU_ORDER` or `GLOBAL_NAV_ORDER`
  - [ ] Tag: `20251127_01`

- [ ] **Create main filter management page**
  - [ ] Function: `show_rt_trade_filter_page()`
  - [ ] Left pane: Listbox widget for trade titles
  - [ ] Populate from `config_trade.json` (active titles only)
  - [ ] Bind selection event to update right pane
  - [ ] Tag: `20251127_01`

- [ ] **Create filter selection pane**
  - [ ] Right pane: Frame with Checkbuttons
  - [ ] Load `available_filters` from `config.json`
  - [ ] Create one Checkbutton per filter
  - [ ] Load current state from `trade_filter_allocations.json`
  - [ ] Tag: `20251127_01`

- [ ] **Implement action buttons**
  - [ ] "Save for Selected" button
    - [ ] Get selected trade title
    - [ ] Get checked filters
    - [ ] Update `trade_filter_allocations.json`
  - [ ] "Apply to All Active" button
    - [ ] Get all active trade titles
    - [ ] Apply checked filters to all
    - [ ] Update `trade_filter_allocations.json`
  - [ ] "Clear for Selected" button
    - [ ] Set selected title's filters to `[]`
    - [ ] Update `trade_filter_allocations.json`
  - [ ] Tag: `20251127_01`

- [ ] **Implement drill-down feature**
  - [ ] Bottom frame with Combobox (filter selection)
  - [ ] Treeview widget for trade display
  - [ ] Columns: Trade No., Title, Position, Entry Time, Exit Time, Net P&L, Alt Net
  - [ ] On filter selection:
    - [ ] Scan `closed_trades` folder (all date subdirectories)
    - [ ] Find trades where this filter was active for their title
    - [ ] Display in Treeview with performance metrics
  - [ ] Tag: `20251127_01`

- [ ] **Add helper functions**
  - [ ] `_load_filter_allocations_ui()` - Load allocations for UI
  - [ ] `_save_filter_allocations_ui(allocations)` - Save from UI
  - [ ] `_get_available_filters_ui()` - Load from config.json
  - [ ] `_scan_trades_by_filter(filter_name)` - Drill-down logic
  - [ ] Tag: `20251127_01`

### 3.4 Documentation & Comments

- [ ] **Add comments to all new code**
  - [ ] Tag all changes with: `# 20251127_01 - Per-title filter allocation`
  - [ ] Document function purposes
  - [ ] Explain data flow

- [ ] **Update this plan**
  - [ ] Check off items as completed
  - [ ] Note any deviations or issues

---

## 4. File Changes Summary

| File | Type | Changes |
|------|------|---------|
| `config.json` | Modify | Add `available_filters` field |
| `trade_filter_allocations.json` | Create | New allocation mapping file |
| `simple_trend_trader.py` | Modify | Load allocations, use per-title filters |
| `trade_monitor.py` | Modify | Add new page and UI components |
| `filters.py` | No Change | Already supports filter application |

---

## 5. Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│ User configures filters in trade_monitor.py UI             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ trade_filter_allocations.json                               │
│ {                                                           │
│   "GBP_TPUSD250_...": ["prev_closed_same_signal_..."],    │
│   "AUD_TPUSD100_...": [],                                  │
│   "EUR_TPUSD250_...": ["prev_closed_same_signal_..."]     │
│ }                                                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ simple_trend_trader.py loads allocations at startup        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ When saving trade:                                          │
│ 1. Get trade title from trade_data                         │
│ 2. Look up filters for this title                          │
│ 3. Pass title-specific filters to apply_filters()          │
│ 4. Save only if filters pass                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Testing Checklist

- [ ] **Configuration Loading**
  - [ ] Verify `available_filters` loads from `config.json`
  - [ ] Verify allocations load from `trade_filter_allocations.json`
  - [ ] Test with missing allocation file (should create empty)

- [ ] **Filter Application**
  - [ ] Test trade with assigned filter (should apply)
  - [ ] Test trade without assigned filter (should save normally)
  - [ ] Test trade with multiple filters (should pass all)
  - [ ] Test trade that fails filter (should not save)

- [ ] **UI Functionality**
  - [ ] Test trade title selection
  - [ ] Test filter checkbox state loading
  - [ ] Test "Save for Selected" button
  - [ ] Test "Apply to All Active" button
  - [ ] Test "Clear for Selected" button
  - [ ] Test drill-down filter selection and display

- [ ] **Backward Compatibility**
  - [ ] Existing trades without filter assignments should work
  - [ ] Empty allocation file should not break anything
  - [ ] Missing `available_filters` in config should default to empty

---

## 7. Potential Issues & Mitigations

| Issue | Mitigation |
|-------|------------|
| Allocation file doesn't exist on first run | Create empty `{}` if missing |
| Trade title not in allocations | Default to empty list `[]` (no filtering) |
| `available_filters` missing from config | Default to empty list, log warning |
| UI performance with many trades | Limit drill-down to recent date range |
| Concurrent access to allocation file | Use file locking or atomic writes |

---

## 8. Future Enhancements (Out of Scope)

- Add more filter types beyond `prev_closed_same_signal_alt_net_negative`
- Filter composition (AND/OR logic)
- Filter parameters (e.g., threshold values)
- Export drill-down results to CSV
- Historical filter effectiveness analysis

---

## 9. Verification Steps

After implementation, verify:
1. ✅ All checklist items completed
2. ✅ All files tagged with `20251127_01`
3. ✅ No unrelated functionality modified
4. ✅ All tests passing
5. ✅ Documentation complete

---

**Plan Status**: PENDING APPROVAL  
**Next Step**: Await user confirmation to proceed with implementation
