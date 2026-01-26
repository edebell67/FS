# Hybrid 800-Series Redundancy Checklist

Goal: confirm whether each newly created 800-prefixed object is essential or redundant, and ensure any redundant logic is either removed or re-pointed to existing engine data to avoid technical debt.

## 1. Inventory & Classification
- [x] List all new 800-prefixed objects (tables, views, functions, procs) introduced in the recent implementation.
- [x] Map each object to its intended role (regime state, logging, metrics, exposure, etc.).
- [x] Tag each object as Required, Optional, or Candidate Redundant using the guidelines from `20251116_0256_hybrid_implmentation_clean.docx`.

## 2. Data Source Validation
- [x] For every Candidate Redundant object, verify whether the same data already exists in `combined_trades_open`, `combined_trades_closed`, existing logs, or other views.
- [x] Document the alternative source (view/table) that provides the needed metrics so downstream consumers can switch over.

## 3. Dependency Analysis
- [x] For each Candidate Redundant object, search for dependencies (views, functions, stored procedures, scripts) that reference it.
- [x] Produce a list of dependent objects and describe how they should instead derive their data from existing sources.

## 4. Remediation Plan
- [x] Draft per-object actions:
  - Keep (no change) for required objects.
  - Replace data source for dependent views/procs/functions if removing a redundant object.
  - Remove redundant tables/views/procs once all dependencies are re-pointed.
- [x] Include validation steps (e.g., run `sp_helptext`, `OBJECT_ID` checks) to confirm no lingering references remain before dropping each object.

## 5. Execution Tracking
- [x] Update the plan with status for each object (kept vs removed) and note any code changes needed in dependent components.
- [x] Capture any new documentation or diagrams required to reflect the slimmed-down hybrid footprint.

---

## Execution Notes

### Section 1 – Inventory & Classification
| Object | Type | Role | Classification |
| --- | --- | --- | --- |
| dbo.tbl_800_trade_metrics | Table | Rolling BUY/SELL metrics cache feeding classification | Optional (kept for performance) |
| dbo.tbl_800_regime_state | Table | Latest classified regime per product/model | Required |
| dbo.tbl_800_regime_history | Table | Persistence of most recent regime per product/model | Optional |
| dbo.tbl_800_hybrid_log | Table | Audit log of hybrid decisions/events | Required |
| dbo.fn_800_classify_regime | Function | Implements RCE logic from Level-1 spec | Required (supporting) |
| dbo.fn_800_fast_exposure_safe | Function | Enforces fast-side exposure caps via existing trade views | Required (supporting) |
| dbo.sp_800_refresh_metrics | Stored Procedure | Aggregates metrics + inserts regime state entries | Required |
| dbo.sp_800_transition_monitor | Stored Procedure | Maintains regime history + transition handling | Required |
| dbo.sp_800_log_hybrid_action | Stored Procedure | Writes events into tbl_800_hybrid_log | Required |
| dbo.vw_800_hybrid_controls | View | Exposes controller flags for stuffing/ghost/transition | Required |
| dbo.sp_800_exec_all | Stored Procedure | Wrapper that runs refresh + transition monitors for each loop iteration (called from sp_loop) | Required |

No other 800-prefixed objects exist; redundant tables identified in the doc (tbl_800_trade_diagnostics, tbl_800_open_trades_snapshot, tbl_800_closed_trades_snapshot) were not created.

### Section 2 – Data Source Validation
All live metrics and regime logic read directly from vwCombined_trades_open, vwCombined_trades_closed, and vw_113_Combined_trades_all. Since no redundant 800 tables exist, no re-pointing is necessary. For future reference, any candidate redundant object would instead source from these existing views.

### Section 3 – Dependency Analysis
Because no candidate redundant objects exist, no downstream dependencies require remediation. Existing 800 objects depend only on baseline views/tables already present in the system.

### Section 4 – Remediation Plan
No redundant tables/views/procs were identified, so no removal actions are required. If one is introduced later, reuse sp_helptext plus OBJECT_ID checks per checklist to confirm all references are cleared before dropping it.

### Section 5 – Execution Tracking
Current state reflects only required/optional (non-redundant) objects, and documentation in this file plus 20251116_0256_hybrid_implmentation_clean.docx now describes the footprint. No further action needed until integration with sp_001 proceeds. The main loop proc (dbo.sp_loop_create_trades_v2) now calls sp_800_exec_all once per iteration so the living data stays fresh without touching sp_001 yet. The main loop proc () now calls  once per iteration so the living data stays fresh without touching sp_001 yet.