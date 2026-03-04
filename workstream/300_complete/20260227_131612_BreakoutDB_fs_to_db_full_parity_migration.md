# BreakoutDB FS-to-DB Full Parity Migration Backlog

## Metadata
- backlog_id: `20260227_131612_BreakoutDB_fs_to_db_full_parity_migration`
- project: `BreakoutDB`
- created_at: `2026-02-27 13:16:12`
- status: `BACKLOG`
- owner: `codex`

## Request Summary
Create a fully separate DB-backed variant of the breakout app by copying:
- `C:\Users\edebe\eds\TradeApps\breakout\fs`

into:
- `C:\Users\edebe\eds\TradeApps\breakout\DB`

Then modify all pages and scripts in `DB` to use PostgreSQL (instead of the `fs\json` file-based model), while preserving identical functionality and keeping `fs` and `DB` entirely separate.

`...\DB\backfill_trades.py` is the reference point for PostgreSQL implementation details.

## Non-Negotiable Constraints
- `fs` and `DB` must remain fully isolated (no cross-imports, shared mutable runtime files, or coupled configs).
- `DB` must remove dependency on `...\fs\json` entirely.
- End-state `DB` behavior must be functionally equivalent to `fs` from a user perspective.
- PostgreSQL must be the sole data source for `DB` runtime behavior (except static assets/config not related to trade-state persistence).

## Scope
- Clone app structure from `fs` to `DB`.
- Repoint backend data-access paths from JSON/file store to PostgreSQL.
- Update UI pages and scripts under `DB` that currently assume file-backed data.
- Add/adjust migration and backfill routines using `DB\backfill_trades.py` as canonical guide.
- Validate parity across core workflows (viewing data, strategy actions, lifecycle updates, and outputs).

## Out of Scope
- Re-architecting `fs`.
- Merging `fs` and `DB` code paths into one hybrid runtime.
- Unrelated UI redesign.

## Target Architecture (DB Variant)
- App root: `TradeApps\breakout\DB`
- Data layer: PostgreSQL adapters/services/repositories
- Configuration: environment-driven DB connection settings
- Optional seed/backfill: `DB\backfill_trades.py`
- No runtime reads/writes to `TradeApps\breakout\fs\json`

## Execution Phases (For Task Decomposition)
1. Discovery and inventory
- Enumerate all `fs` pages/scripts touching `json` paths.
- Map each file usage to equivalent DB query/command behavior.

2. Structure bootstrap
- Copy `fs` to `DB` preserving folder layout.
- Rename/normalize app identifiers and startup scripts for DB variant.

3. Data access refactor
- Replace JSON read/write flows with PostgreSQL repositories.
- Centralize SQL access patterns and connection handling.

4. Backfill and schema alignment
- Use `DB\backfill_trades.py` to define table expectations and fill strategy.
- Ensure required tables/indexes/views exist for runtime parity.

5. UI and script rewiring
- Update all pages/scripts to call DB-backed endpoints/services.
- Remove or neutralize dead file-based branches in `DB`.

6. Validation and parity testing
- Run side-by-side behavior checks (`fs` vs `DB`) across key workflows.
- Verify outputs and state transitions are equivalent.

7. Operational hardening
- Add configuration docs and run instructions for DB variant.
- Confirm no accidental reference back to `fs\json` remains.

## Acceptance Criteria
- `TradeApps\breakout\DB` exists as an independent runnable app variant.
- Search of `DB` codebase shows no dependency on `TradeApps\breakout\fs\json` for runtime state.
- Core functional flows match `fs` behavior (same user-facing outcomes).
- `DB\backfill_trades.py` is present and aligned with active PostgreSQL schema/usage.
- Runbook for starting/testing `DB` is documented.

## Decomposition Guidance
Use `skills/document-to-task-decomposition` to split this backlog into atomic tasks in `workstream/100_todo`, each with explicit verification tests.

## Risks and Notes
- Hidden file-based assumptions in helper utilities may cause partial parity failures.
- SQL schema drift between environments can mask defects.
- Performance may differ when replacing local file reads with DB calls; parity should prioritize correctness first.

## Completion Gate
This backlog can move to `workstream/300_complete` only after:
1. All derived tasks are in `workstream/300_complete`.
2. This file contains a completed "Completed Tasks" section with links.
3. Final parity verification (`fs` vs `DB`) is documented and passed.

---

## Completed Tasks

| Task | Completed | File |
|------|-----------|------|
| Discovery and JSON dependency inventory | 2026-02-27 | `workstream/300_complete/20260227_131801_breakoutdb_discovery_json_dependency_inventory.md` |
| Clone fs app into isolated DB variant | 2026-02-27 | `workstream/300_complete/20260227_131802_breakoutdb_clone_fs_to_db_isolated_variant.md` |
| Implement PostgreSQL repository layer | 2026-02-27 | `workstream/300_complete/20260227_131803_breakoutdb_implement_postgresql_repository_layer.md` |
| Align schema and backfill workflow | 2026-02-27 | `workstream/300_complete/20260227_131804_breakoutdb_align_schema_and_backfill_workflow.md` |
| Rewire pages and scripts to DB services | 2026-02-27 | `workstream/300_complete/20260227_131805_breakoutdb_rewire_pages_and_scripts_to_db_services.md` |
| FS-vs-DB parity validation suite | 2026-02-27 | `workstream/300_complete/20260227_131806_breakoutdb_fs_vs_db_parity_validation_suite.md` |
| Runbook and separation guardrails | 2026-02-27 | `workstream/300_complete/20260227_131807_breakoutdb_runbook_and_separation_guardrails.md` |

## Backlog Status

**STATUS**: COMPLETE  
**All Tasks Verified**: Yes  
**Completion Date**: 2026-02-27
