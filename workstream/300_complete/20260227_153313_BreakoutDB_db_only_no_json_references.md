# BreakoutDB DB-Only Pages and Scripts Migration Backlog

## Metadata
- backlog_id: `20260227_153313_BreakoutDB_db_only_no_json_references`
- project: `BreakoutDB`
- created_at: `2026-02-27 15:33:13`
- status: `BACKLOG`
- owner: `codex`

## Request Summary
Bring `C:\Users\edebe\eds\TradeApps\breakout\DB` to a strict DB-only state where every DB page and script uses PostgreSQL-backed data paths and there are no runtime references to local JSON persistence.

## Hard Requirements
- Every DB page route/data dependency must resolve from DB APIs/tables/views only.
- Remove runtime dependency on `TradeApps\breakout\DB\json`.
- No executable code in `DB` may reference `fs/json` or `DB/json` as a persistence source.
- Preserve user-visible functionality and response contracts.

## Scope
- Backend API endpoint migration to DB-only queries/services.
- Frontend/page data source rewiring to DB-backed endpoints.
- Script/service migration off file JSON I/O.
- Backfill responsibilities separated from runtime paths.
- Final zero-reference compliance scan and runtime verification.

## Out of Scope
- Rewriting unrelated strategy logic.
- UI redesign.
- Changes to `fs` variant.

## Execution Phases (For Task Decomposition)
1. Runtime dependency inventory
- Identify all executable DB files still using JSON file reads/writes.
- Classify by page/API/script impact.

2. API DB-only hardening
- Replace any file-based fallback in runtime APIs with DB-backed equivalents.
- Ensure endpoint contracts remain stable.

3. Page-level data rewiring
- Update page scripts/JS fetch patterns to consume DB-backed API outputs.
- Remove direct file path assumptions.

4. Script/service migration
- Migrate schedulers, generators, monitors, and helpers from JSON files to DB.
- Keep one-off offline utilities explicitly marked non-runtime.

5. JSON folder decoupling
- Make app startup and normal operation resilient when `DB/json` is absent.
- Keep backfill as optional/import-only pipeline, not runtime requirement.

6. Compliance and parity validation
- Automated scan proving zero executable JSON persistence references.
- Functional checks for all major pages and critical APIs.

7. Runbook and enforcement
- Update runbook with DB-only operating mode.
- Add guardrails/checks in repo workflow.

## Acceptance Criteria
- Removing/renaming `TradeApps\breakout\DB\json` does not break runtime app behavior.
- All major DB pages load and function via DB-backed APIs.
- API smoke endpoints pass using DB data only.
- Executable-file scan reports zero JSON persistence references in `DB` runtime code.
- Workstream tasks fully completed and linked.

## Risks
- Legacy helpers may silently rely on historical JSON formats.
- Endpoint compatibility drift if payload shape changes during migration.
- Hidden runtime imports from backup or old variants.

## Completion Gate
This backlog can move to `workstream/300_complete` only after:
1. All derived tasks are in `workstream/300_complete`.
2. This file contains a completed "Completed Tasks" section with links.
3. Verified proof that `DB` runs without `DB/json` folder dependency.

---

## Completed Tasks
| Task | Completed | File |
|------|-----------|------|
| DB runtime JSON dependency inventory | 2026-02-27 | `workstream/300_complete/20260227_153401_breakoutdb_db_runtime_json_dependency_inventory.md` |
| Convert trade APIs to strict DB-only mode | 2026-02-27 | `workstream/300_complete/20260227_153402_breakoutdb_convert_trade_apis_to_strict_db_only.md` |
| Migrate page scripts to DB-only data flows | 2026-02-27 | `workstream/300_complete/20260227_153403_breakoutdb_migrate_page_scripts_to_db_only_data_flows.md` |
| Migrate runtime services/schedulers off JSON | 2026-02-27 | `workstream/300_complete/20260227_153404_breakoutdb_migrate_runtime_services_and_schedulers_off_json_files.md` |
| Remove DB/json runtime dependency | 2026-02-27 | `workstream/300_complete/20260227_153405_breakoutdb_remove_db_json_runtime_dependency.md` |
| Zero-reference compliance and regression matrix | 2026-02-27 | `workstream/300_complete/20260227_153406_breakoutdb_zero_reference_compliance_and_regression_matrix.md` |
| DB-only runbook and enforcement automation | 2026-02-27 | `workstream/300_complete/20260227_153407_breakoutdb_db_only_runbook_and_enforcement_automation.md` |
| Refactor grid_live_monitor to DB-native state | 2026-02-27 | `workstream/300_complete/20260227_154050_breakoutdb_refactor_grid_live_monitor_to_db_native_state.md` |
| Refactor summary_net_generator to DB-only pipeline | 2026-02-27 | `workstream/300_complete/20260227_154051_breakoutdb_refactor_summary_net_generator_to_db_only_pipeline.md` |
| Refactor top_one_generator to DB-derived output | 2026-02-27 | `workstream/300_complete/20260227_154052_breakoutdb_refactor_top_one_generator_to_db_derived_output.md` |
| Refactor live_scheduler to DB-backed flow | 2026-02-27 | `workstream/300_complete/20260227_154053_breakoutdb_refactor_live_scheduler_to_db_backed_control_flow.md` |
| Refactor automated_strategy_picker to DB inputs | 2026-02-27 | `workstream/300_complete/20260227_154054_breakoutdb_refactor_automated_strategy_picker_to_db_backed_inputs.md` |
| Refactor sync_active_trades to DB state sync | 2026-02-27 | `workstream/300_complete/20260227_154055_breakoutdb_refactor_sync_active_trades_to_db_state_sync.md` |
| Refactor market_update_generator to DB-backed history | 2026-02-27 | `workstream/300_complete/20260227_154056_breakoutdb_refactor_market_update_generator_to_db_backed_history.md` |
| Enforce zero-runtime-json gate and signoff | 2026-02-27 | `workstream/300_complete/20260227_154057_breakoutdb_enforce_zero_runtime_json_gate_and_signoff.md` |

## Backlog Status
**STATUS**: COMPLETE
**All Tasks Verified**: Yes
**Completion Date**: 2026-02-27
