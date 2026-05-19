Source: User request

Task Summary: Ensure all fields from config.json are available in the config UI in trade_viewer.html

Context:
- Project: TradeApps/breakout
- Config file: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
- UI file: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer.html`
- The config UI in trade_viewer.html currently exposes ~40 fields but config.json has ~70+ fields

Priority: 2

**Suggested Agent:** claude

## Objective

Add all missing config.json fields to the config UI modal in trade_viewer.html so users can view and edit every configuration option.

## Missing Fields Analysis

### Simple Fields (NOT in UI)
| Field | Type | Current Value |
|-------|------|---------------|
| `DATA_SOURCE` | select | "file_system" |
| `auto_archive_threshold` | number | 5000 |
| `auto_trade_count_mode` | select | "max_count" |
| `automated_trade_source` | select | "Frequency" |
| `bypass_criteria_check` | select | "immediately" |
| `close_pending_timeout` | number | 300 |
| `crypto_trade_qty_percent` | number | 50 |
| `frequency_datasource` | text | "breakout" |
| `multi_vtrade` | boolean | false |
| `picker_count_diff_threshold` | number | 0.05 |
| `picker_pnl_spread_threshold` | number | 2000 |
| `rank_alert_default_action` | select | "monitor_only" |
| `rank_alert_enabled` | boolean | false |
| `rank_alert_suspended` | boolean | true |
| `rank_alert_threshold` | select | "rank1" |
| `trade_bucket_max_strategies` | number | 3 |
| `trade_file_min_age_minutes` | number | 30 |
| `v_trade_exit_at_target` | boolean | false |
| `virtual_trade_live_by_default` | boolean | true |
| `vtrade_persistence_seconds` | number | 300 |
| `vtrade_selection_type` | select | "top_net" |

### Complex Object Fields (NOT in UI)
| Field | Type | Description |
|-------|------|-------------|
| `endpoints` | object | Live/sim API endpoints |
| `min_value_by_product` | object | Min values per product (BTC, CL, ES, etc.) |
| `min_value_by_product_type` | object | Min values per type (crypto, forex, metals) |
| `pip_multiplier_by_product` | object | Pip multipliers per product |
| `pip_multiplier_by_product_type` | object | Pip multipliers per type |
| `product_type_by_product` | object | Product type mappings |

### Sensitive Fields (consider read-only or hidden)
| Field | Type |
|-------|------|
| `supabase_url` | text |
| `supabase_anon_key` | text |

## Plan
- [ ] 1. Add new section "Virtual Trades" with vtrade fields
  - [ ] Test: Open config modal, verify Virtual Trades section appears with all vtrade fields
  - [ ] Evidence: pending
- [ ] 2. Add new section "Rank Alerts" with rank_alert fields
  - [ ] Test: Verify Rank Alerts section with enable/suspend/threshold/action fields
  - [ ] Evidence: pending
- [ ] 3. Add new section "Trade Bucket" with trade bucket specific fields
  - [ ] Test: Verify trade_bucket_max_strategies and trade_file_min_age_minutes appear
  - [ ] Evidence: pending
- [ ] 4. Add new section "AI Picker" with picker threshold fields
  - [ ] Test: Verify picker_count_diff_threshold and picker_pnl_spread_threshold appear
  - [ ] Evidence: pending
- [ ] 5. Add missing simple fields to existing sections (auto_archive_threshold, bypass_criteria_check, close_pending_timeout, etc.)
  - [ ] Test: Verify all simple missing fields are accessible in appropriate sections
  - [ ] Evidence: pending
- [ ] 6. Add new section "Product Mappings" for complex object fields with key-value editor UI
  - [ ] Test: Verify min_value_by_product, pip_multiplier_by_product can be viewed/edited
  - [ ] Evidence: pending
- [ ] 7. Add new section "Endpoints" for API endpoint configuration
  - [ ] Test: Verify live and sim endpoints arrays can be viewed/edited
  - [ ] Evidence: pending
- [ ] 8. Test save/load of all new fields
  - [ ] Test: Modify values, save config, reload page, verify values persist
  - [ ] Evidence: pending

## Validation
- [ ] All 70+ config.json fields are accessible in the config UI
- [ ] Save button correctly persists all field values
- [ ] Page reload shows saved values correctly
- [ ] No JavaScript errors in browser console
- [ ] Complex object fields (min_value_by_product, endpoints, etc.) have appropriate editor UI

## Files to Modify
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer.html` - Add missing field definitions to `renderConfigForm()` function sections array

## Implementation Notes
- The config UI uses a sections array in `renderConfigForm()` function (line ~3120)
- Simple fields use `{ label, key, type, options? }` format
- Boolean fields use `type: 'boolean'`
- Select fields use `type: 'select', options: [...]`
- Complex objects may need a new UI pattern (key-value editor or expandable sections)

Required Skills:
- `skills/workstream-task-lifecycle/SKILL.md`

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: false
- Evidence-Type: manual_verification
  - Artifact: not_applicable
  - Objective-Proved: All config.json fields accessible in trade_viewer.html config UI
  - Status: planned

## Implementation Log
- 2026-03-23 00:49: Task created from user request

## Changes Made
- Pending implementation

## Risks/Notes
- Complex object fields (endpoints, min_value_by_product, etc.) may require a new UI pattern
- Sensitive fields (supabase keys) should be handled carefully - consider read-only or masked display

Completion Status: Backlog
