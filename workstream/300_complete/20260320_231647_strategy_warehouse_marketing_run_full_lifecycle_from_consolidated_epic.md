Source: User request in Codex thread on 2026-03-20 to go through the full lifecycle with the updated consolidated Strategy Warehouse marketing epic.

Task Summary: Run a simplified full lifecycle reset for the consolidated Strategy Warehouse epic by dumping all non-complete related tasks, decomposing the updated epic afresh, identifying what is already delivered, and focusing execution on the remainder.

Context:
- Active epic: `C:\Users\edebe\eds\workstream\000_epic\20260316_135233_strategy_warehouse_autonomous_marketing_engine_processed.md`
- Merged older epic: `C:\Users\edebe\eds\workstream\300_complete\20260316_135212_trading_strategy_warehouse_marketing_engine_processed.md`
- Comparison baseline: `C:\Users\edebe\eds\workstream\300_complete\20260320_223352_strategy_warehouse_marketing_compare_deliverable_to_epic.md`

Dependency:
- `C:\Users\edebe\eds\workstream\300_complete\20260320_224747_strategy_warehouse_marketing_merge_epics_into_single_replacement.md`

Plan:
- [x] 1. Inventory all non-complete Strategy Warehouse tasks currently in review, backlog, and in-progress lanes.
  - [x] Test: Enumerate all related markdown tasks outside `300_complete` that match the consolidated epic.
  - [x] Evidence: Identified 52 non-complete related tasks across `050_review`, `100_backlog`, `200_inprogress`, and `200_inprogress/blocker`.
- [x] 2. Dump all those non-complete related tasks out of the active lifecycle lanes.
  - [x] Test: Move the identified tasks from `050_review`, `100_backlog`, and `200_inprogress` into a timestamped dump location under `500_dump`.
  - [x] Evidence: Moved 52 tasks into `C:\Users\edebe\eds\workstream\500_dump\strategy_warehouse_marketing_reset_20260320_231647`.
- [x] 3. Run a full decomposition of the consolidated epic.
  - [x] Test: Execute the epic decomposition command against the active consolidated epic and produce a fresh task set.
  - [x] Evidence: Fresh decomposition completed from `20260316_135233_strategy_warehouse_autonomous_marketing_engine_processed.md` with artefacts under `C:\Users\edebe\eds\workstream\artefacts\epic_decomp_20260320_232723_696675`.
- [x] 4. Compare the fresh decomposition against what is already in `300_complete` and the current deliverable.
  - [x] Test: Identify which decomposed tasks are already delivered and which remain outstanding.
  - [x] Evidence: Delivered set classified as `Z1,Z2,Z3,Z4,A2,A3,B1,B2,B4,B5,B6,B7`; remaining set classified as `Z5,Z6,A1,A4,A5,A6,B3,B8,B9,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,D1,D2,D3,D4,D5,D6,D7`.
- [x] 5. Queue focus only on the remaining work.
  - [x] Test: Ensure the remaining work is represented as active tasks and that already delivered work is not re-queued.
  - [x] Evidence: Created 26 fresh remainder backlog tasks under `100_backlog/{claude,codex,gemini}` and did not recreate tasks mapped as already delivered.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\20260320_231647_strategy_warehouse_marketing_run_full_lifecycle_from_consolidated_epic.md`
  - Objective-Proved: Lifecycle control file exists for the consolidated-epic rebaseline.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: Non-complete task inventory, dump move output, successful decomposition JSON output, and remainder task creation output from 2026-03-20
  - Objective-Proved: Strategy Warehouse lifecycle artefacts are inventoried and reconciled to the consolidated epic.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\workstream\500_dump\strategy_warehouse_marketing_reset_20260320_231647`, `C:\Users\edebe\eds\workstream\artefacts\epic_decomp_20260320_232723_696675`, and 26 new backlog task files under `C:\Users\edebe\eds\workstream\100_backlog`
  - Objective-Proved: Epic/task files are updated so the lifecycle reflects the single consolidated epic.
  - Status: captured

Implementation Log:
- 2026-03-20 23:16:47: Created in-progress lifecycle task for consolidated epic rebaseline.
- 2026-03-20 23:17:00: Initial scan confirmed the epic already has artefacts across `050_review`, `100_backlog`, `200_inprogress`, `300_complete`, blocker lanes, failed lanes, and dump lanes.
- 2026-03-20 23:20:00: User directed a simpler reset approach: dump all related non-complete tasks, decompose the consolidated epic afresh, identify already delivered items, and focus only on the remainder.
- 2026-03-20 23:25:00: Enumerated 52 non-complete related tasks across active lanes for the consolidated Strategy Warehouse epic.
- 2026-03-20 23:31:00: Moved those 52 tasks into `500_dump\strategy_warehouse_marketing_reset_20260320_231647`, preserving relative paths for traceability.
- 2026-03-20 23:27:23: Started fresh decomposition of the consolidated epic via `epic_decompose_cli.py`.
- 2026-03-20 23:30:32: Fresh decomposition completed successfully; output saved in `artefacts\epic_decomp_20260320_232723_696675`.
- 2026-03-20 23:31:48: Classified already delivered tasks from the previous deliverable as `Z1,Z2,Z3,Z4,A2,A3,B1,B2,B4,B5,B6,B7`.
- 2026-03-20 23:31:48: Created 26 new backlog tasks for the remaining scope only, covering `Z5,Z6,A1,A4,A5,A6,B3,B8,B9,C1-C10,D1-D7`.

Changes Made:
- Added lifecycle control task for running the full lifecycle from the consolidated Strategy Warehouse epic.
- Dumped all active non-complete Strategy Warehouse tasks into `C:\Users\edebe\eds\workstream\500_dump\strategy_warehouse_marketing_reset_20260320_231647`.
- Ran a fresh decomposition from the consolidated active epic.
- Created 26 new remainder-only backlog tasks under `100_backlog\claude`, `100_backlog\codex`, and `100_backlog\gemini`.

Validation:
- [x] Create a lifecycle task file for the consolidated-epic full-lifecycle run.
- [x] Inventory non-complete Strategy Warehouse tasks.
- [x] Dump those non-complete tasks out of active lanes.
- [x] Run fresh decomposition from the consolidated epic.
- [x] Classify delivered versus remaining work from the new decomposition.

Risks/Notes:
- This approach intentionally discards the current active-lane task set in favor of a clean re-decomposition baseline; any useful but incomplete task history will live in `500_dump`.
- The critical comparison source after decomposition is `300_complete` plus the current deliverable under `C:\Users\edebe\eds\ep_strategy_warehouse_marketing`.

Completion Status: In progress
Completion Status: Complete - 2026-03-20 23:31:48
