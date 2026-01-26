# Hybrid Process Integration Checklist (sp_001_create_trades_v9_setbased)

## 1. Preparation & Analysis
- [x] Review current `sp_001_create_trades_v9_setbased` sections and confirm entry points for new EXEC blocks.
- [x] Inventory existing tables/views that supply trade history (`vwcombined_trades_*`, trade logs) and capture their keys/columns.
- [x] Verify config toggles / env flags that will guard the hybrid logic prior to activation.

## 2. Metrics Aggregation Layer (`sp_800_refresh_metrics`, `tbl_800_trade_metrics`)
- [x] Define schema for `tbl_800_trade_metrics` (product, model, pf_ord, counts, avg durations, real pnl, ghost ratios, dur/count ratios, timestamps).
- [x] Implement SQL to populate metrics from existing trade-history sources using rolling window parameter (default 30 min) with clear BUY/SELL splits.
- [x] Wrap population logic in stored proc `sp_800_refresh_metrics` (temp-table lifecycle management, configurable window length).
- [x] Add lightweight validation queries/log output confirming metrics row counts each run.

## 3. Regime Classification (`fn_800_classify_regime`, `tbl_800_regime_state`)
- [x] Design `tbl_800_regime_state` structure (product/model keys + regime_state, fast_side, slow_side, supporting metrics, prev_state guid).
- [x] Create table-valued or scalar function `fn_800_classify_regime` that consumes a metrics row + previous state and returns regime tuple per pseudocode.
- [x] Extend `sp_800_refresh_metrics` to call `fn_800_classify_regime` for every metrics row and persist results into `tbl_800_regime_state`.
- [x] Confirm handling of insufficient data (UNKNOWN) and symmetry thresholds (CHOP/COMPRESSED) according to requirements.

## 4. Regime History Persistence (`tbl_800_regime_history`, `sp_800_transition_monitor`)
- [x] Add `tbl_800_regime_history` to capture last regime per product/model/time.
- [x] Implement `sp_800_transition_monitor` to read latest metrics, compare against history, and flag TRANSITION confirmations or reversions.
- [x] Ensure monitor updates history rows atomically and exposes status via output table/resultset for downstream use.

## 5. Hybrid Controller Projections (`vw_800_hybrid_controls`)
- [x] Build view `vw_800_hybrid_controls` joining `tbl_800_regime_state` with open-trade snapshot to derive booleans: `can_stuff`, `must_ghost`, `auto_flip_armed`, `transition_active`.
- [x] Include computed helpers (slow-duration breaches, fast-duration breakdown counts, ghost ratio) to avoid recalculations inside the main proc.
- [x] Validate view outputs against sample regimes (one per state) before wiring into production flow.

## 6. Risk & Exposure Guardrails (`fn_800_fast_exposure_safe`)
- [x] Define `fn_800_fast_exposure_safe(product, model, fast_side)` to aggregate open qty + worst-case loss from existing exposure tables.
- [x] Return bit/flag indicating whether additional stuffing is permitted; handle NULL/no-open scenarios gracefully.
- [x] Integrate function call inside `vw_800_hybrid_controls` so gating logic is centralized.

## 7. Logging & Audit (`tbl_800_hybrid_log`, `sp_800_log_hybrid_action`)
- [x] Create event log table storing timestamp, product/model, regime_state, action (`stuff_attempt`, `ghost_close`, `risk_block`, etc.), and contextual metrics.
- [x] Implement `sp_800_log_hybrid_action` to insert rows and expose optional PRINT/RAISERROR output for real-time diagnostics.
- [x] Hook logging proc into each new module (metrics refresh, classification, controller decisions) but leave behind feature toggle.

## 8. Integration Touchpoints inside `sp_001_create_trades_v9_setbased`
- [ ] Add guarded EXEC calls near the top: `sp_800_refresh_metrics`, `sp_800_transition_monitor` (wrap in `IF @hybrid_enabled = 1`).
- [ ] After candidate temp tables (`#cand`) are built, join to `vw_800_hybrid_controls` by product/model to bring in regime flags.
- [ ] Update stuffing sections to require `can_stuff = 1` and `fn_800_fast_exposure_safe = 1` before inserting new shells.
- [ ] Update ghost-close logic to apply only when `must_ghost = 1` and slow-side duration exceeds threshold.
- [ ] In TRANSITION mode, block stuffing, enable ghost-close safeties, and invoke auto-flip routine if `transition_confirmed = 1`.
- [ ] Ensure all additions remain no-ops when `@hybrid_enabled = 0` (default), preserving current behaviour.

## 9. Testing & Verification
- [ ] Unit-test each new `sp_800_/fn_800_/vw_800_/tbl_800_` object with representative datasets (CHOP, TREND_BUY, TREND_SELL, TRANSITION).
- [ ] Dry-run `sp_001…` in a sandbox with `@hybrid_enabled = 0` to confirm zero diff in trade outputs/logging.
- [ ] Enable hybrid flag in simulation DB, monitor `tbl_800_hybrid_log` and trade creation counts for at least one full session.
- [ ] Document rollback procedure (disable flag + optional drop of 800 objects) for deployment safety.

## 10. Documentation & Handover
- [ ] Update internal wiki/plan with diagrams and explanation of new 800 objects and how they interact with existing trade engine.
- [ ] Provide config instructions for enabling/disabling hybrid behaviour per environment (sim vs live).
- [ ] Record sample SQL snippets for querying regimes, metrics, and event logs for debugging.
