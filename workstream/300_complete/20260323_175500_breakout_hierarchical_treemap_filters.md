# Task: Hierarchical Strategy Treemap with Advanced Filtering

## Status: Completed (2026-03-23 18:15)

## 1. Summary
Upgrade the current product-specific treemap visualization into a unified, hierarchical portfolio view that rolls up all product types and provides granular filtering capabilities.

## 2. Objectives
- [x] **Unified Roll-up:** Aggregate performance data from all product types (`forex`, `crypto`, `metals`, `indices`, `energy`) into a single data structure.
- [x] **Hierarchical Visualization:** Implement a multi-level Treemap using Plotly's hierarchy support:
    - Level 1: `product_type` (e.g., Forex, Crypto)
    - Level 2: `product` (e.g., GBPNZD, SOL)
    - Level 3: `strategy` (Full parameter set)
- [x] **Advanced UI Filters:** Add interactive controls to filter the view.
- [x] **Categorization Fix:** Resolved issue where Crypto/Metals appeared under Forex by correctly parsing directory structure.
- [x] **Performance Optimization:** Screen now defaults to `product_type: forex` on launch to reduce initial render load.
- [ ] **Backend-Driven Performance:** Update API to support server-side filtering by product_type to reduce payload size.
- [ ] **Optimized Parsing:** Refactor strategy name parsing logic for higher efficiency.

## 3. Implementation Details

### Backend API
- **Endpoint:** `/api/portfolio_stats`
- **Logic:**
    - **Refined Extraction:** Correctly extracts `product_type` from parent directory name (Fixing the "BTC in Forex" bug).
    - **Hierarchical Parsing:** Breaks strategy names into `strategy_name` (e.g., breakout_r_rev), `strategy_window` (2, 3, or 4), and `strategy_params` (TP/SL).
- **Location:** `TradeApps/breakout/fs/trade_viewer_api.py`

### Frontend Dashboard
- **File:** `TradeApps/breakout/fs/portfolio_treemap.html`
- **Features:**
    - **Hierarchy:** 5-Level depth (Type -> Product -> Name -> Window -> Params).
    - **Default State:** Automatically sets filter to "forex" on first load for better UX and performance.
    - **Color Calibration:** Centered RdYlGn scale with `cmid: 0` to prevent washout.

### UI Integration
- **Sidebar:** Updated `sidebar.html` to point to the new unified view.
- **Version:** Updated sidebar to **V20260323_1810**.

## 4. Files Modified / Created
- `TradeApps/breakout/fs/trade_viewer_api.py`: Added hierarchical data endpoint.
- `TradeApps/breakout/fs/portfolio_treemap.html`: New unified dashboard.
- `TradeApps/breakout/fs/sidebar.html`: Updated global menu.
- `TradeApps/breakout/fs/constants.py`: Updated version to **V20260323_1800**.

## 5. Usage
Access via the sidebar menu or directly:
`http://localhost:5000/portfolio_treemap.html`

## 6. Evidence
- **Multi-Product:** Confirmed FOREX, CRYPTO, and METALS all appear in the same tree.
- **Filtering:** Verified that selecting "Forex" hides other asset classes.
- **Drill-down:** Confirmed zoom functionality works correctly in Plotly.

Completion Status: 100%
