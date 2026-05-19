Source: User request on 2026-04-01 referencing the Weekly Performance screen to change the first columns of the table.

Task Type: standard
Project: breakout

Task Attributes:
- recurring_task: false
- workflow_task: false
- priority: high
- execution_owner: codex

**Suggested Agent:** codex

Task Summary: Update the Weekly Performance table so the first data column reverts to `Product | strategy name_parm` format such as `GBPAUD_C | breakout_R_2_tp30.0_sl10.0`, and add a new second column containing `gen_strategy_name`.

Context:
- Surface: Weekly Performance page shown in the attached image
- Current first data column displays combined generated strategy labels such as `NQ|cipher-lattice_2_zlb4_d22b`
- Requested target structure:
  - first column: `Product | strategy name_parm`
  - second column: `gen_strategy_name`
- Example required display:
  - `GBPAUD_C | breakout_R_2_tp30.0_sl10.0`

Dependency: None

## Plan

- [x] 1. Trace the Weekly Performance row data so the source fields for product, `strategy name_parm`, and `gen_strategy_name` are identified.
  - [x] Test: Confirm the table data already contains or can derive the three required fields without inventing values.
  - Evidence: `TradeApps/breakout/fs/summary_net_generator.py` writes `_trades_summary.json` with `app_name` sourced from `source_strategy/script_name` and `strategy` sourced from `gen_strategy_name`; sampled raw trade file `TradeApps/breakout/fs/json/live/forex/2026-04-01/breakout_2_tp10.0_sl10.0_53bf519e_GBPEUR_C_20260401_080514_2_0.00015_10.0_10.0_cld.json` confirms `product=GBPEUR_C`, `script_name=breakout_2_tp10.0_sl10.0`, and `gen_strategy_name=tango-matrix_2_z17a_d18d`.

- [x] 2. Update the table columns to restore the first column to `Product | strategy name_parm`.
  - [x] Test: Verify the first visible data column renders in the requested format for each row.
  - Evidence: `TradeApps/breakout/fs/tools/aggregate_top_strategies.py` now emits `strategy_label`/`strategy` as `product | strategy_name_parm`, and `tests/test_breakout_weekly_performance.py::test_aggregate_for_product_type_keeps_strategy_and_gen_strategy_separate` asserts `GBPAUD_C | breakout_R_2_tp30.0_sl10.0`.

- [x] 3. Add the new second column for `gen_strategy_name`.
  - [x] Test: Verify the new second column renders the corresponding `gen_strategy_name` for each row and the table layout remains usable.
  - Evidence: `TradeApps/breakout/fs/weekly_performance.html` now renders a sortable `Gen Strategy` column from `item.gen_strategy_name`, and `tests/test_breakout_weekly_performance.py::test_weekly_performance_html_defines_sortable_columns` plus the new aggregator regression cover the payload/UI contract.

## Evidence
Objective-Delivery-Coverage: 90%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `git diff -- TradeApps/breakout/fs/tools/aggregate_top_strategies.py TradeApps/breakout/fs/weekly_performance.html tests/test_breakout_weekly_performance.py`
  - Objective-Proved: Proves the Weekly Performance table columns were updated to the requested structure.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m pytest C:\Users\edebe\eds\tests\test_breakout_weekly_performance.py` output `5 passed in 1.21s`; plus inline Python validation confirming `rows 1000`, `first_strategy_label GBPNZD_C | breakout_R_2_tp50.0_sl5.0`, and `first_gen_strategy_name harbor-cobalt_2_z55b_d701`
  - Objective-Proved: Proves the weekly-performance payload and UI column contract pass the regression suite after the change and that regenerated weekly data carries the restored first-column label plus separate `gen_strategy_name`.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: User verification requested for the Weekly Performance screen to confirm the first column shows `Product | strategy name_parm` and the second column shows `gen_strategy_name`.
  - Objective-Proved: Proves the first column now shows `Product | strategy name_parm` and the second column shows `gen_strategy_name`.
  - Status: planned

## Implementation Log
- 2026-04-01 15:50:58 Europe/London: Task created from the user request to restore `Product | strategy name_parm` as the first column and add a new `gen_strategy_name` second column.
- 2026-04-01 16:59:00 Europe/London: Traced Weekly Performance data flow through `TradeApps/breakout/fs/tools/aggregate_top_strategies.py`, `TradeApps/breakout/fs/weekly_performance.html`, `TradeApps/breakout/fs/summary_net_generator.py`, and a sampled closed-trade JSON. Confirmed the current first column is built from `product | gen_strategy_name`, while the requested first column should use `product | app_name/script_name` and the generated strategy should be surfaced as a dedicated second column.
- 2026-04-01 17:01:00 Europe/London: Updated the weekly aggregator to keep `product`, `strategy_name_parm`, and `gen_strategy_name` separate per row while preserving the existing `strategy` field as the restored `Product | strategy name_parm` label for compatibility.
- 2026-04-01 17:02:00 Europe/London: Updated the Weekly Performance page to render sortable `Product | Strategy` and `Gen Strategy` columns and added regression coverage for the revised payload/UI contract.
- 2026-04-01 17:03:00 Europe/London: Ran `python -m pytest tests/test_breakout_weekly_performance.py`; all 5 tests passed.
- 2026-04-01 17:02:05 Europe/London: Re-ran the regression suite from the repo root (`5 passed in 1.21s`) and separately validated that regenerated weekly stats still emit `strategy_label = "{product} | {strategy_name_parm}"` plus a dedicated `gen_strategy_name` field while the HTML still defines both sortable columns.
- 2026-04-01 17:02:05 Europe/London: Moved the lifecycle file into `workstream/200_inprogress/codex/` so its queue state matches `AWAITING USER VERIFICATION`.

## Changes Made
- `TradeApps/breakout/fs/tools/aggregate_top_strategies.py`
  - Changed weekly aggregation keys from `product | gen_strategy_name` display strings to a structured tuple of `product`, `strategy_name_parm`, and `gen_strategy_name`.
  - Added row fields `product`, `strategy_name_parm`, `gen_strategy_name`, and `strategy_label`.
  - Restored the compatibility `strategy` field to `Product | strategy name_parm`.
- `TradeApps/breakout/fs/weekly_performance.html`
  - Replaced the single `Strategy / Product` column with sortable `Product | Strategy` and `Gen Strategy` columns.
  - Updated sorting logic to use `strategy_label` and `gen_strategy_name`.
  - Added styling for the generated-strategy column.
- `tests/test_breakout_weekly_performance.py`
  - Extended the fixture helper to carry `gen_strategy_name`.
  - Added payload assertions for the restored first-column fields.
  - Added a regression test covering separation of `strategy_name_parm` and `gen_strategy_name`.
  - Updated the HTML contract test for the new sortable headers.

## Validation
- Step 1 validation:
  - `Get-Content -Raw 'C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html'`
  - `Get-Content -Raw 'C:\Users\edebe\eds\TradeApps\breakout\fs\tools\aggregate_top_strategies.py'`
  - `Get-Content -Raw 'C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py'`
  - `Get-Content -Raw 'C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-01\breakout_2_tp10.0_sl10.0_53bf519e_GBPEUR_C_20260401_080514_2_0.00015_10.0_10.0_cld.json'`
  - Result: Pass. Verified canonical fields exist without inventing values.
- Step 2 validation:
  - `python -m pytest tests/test_breakout_weekly_performance.py`
  - Result: Pass. `5 passed in 3.74s`, including `test_aggregate_for_product_type_keeps_strategy_and_gen_strategy_separate` proving the first column now resolves to `Product | strategy name_parm`.
- Step 3 validation:
  - `python -m pytest tests/test_breakout_weekly_performance.py`
  - Result: Pass. `test_weekly_performance_html_defines_sortable_columns` confirms the new sortable `Gen Strategy` column is defined in the page contract.
- Additional validation:
  - `@' ... aggregate_for_product_type('forex', target_date='2026-03-30', output_file=...) ... '@ | python -`
  - Result: Pass. Output reported `rows 1000`, `first_strategy_label GBPNZD_C | breakout_R_2_tp50.0_sl5.0`, and `first_gen_strategy_name harbor-cobalt_2_z55b_d701`.
  - `@' ... checks = { 'header_product_strategy': ..., 'header_gen_strategy': ..., 'row_strategy_label': ..., 'row_gen_strategy': ... } ... '@ | python -`
  - Result: Pass. Output reported all checks as `True`, confirming the HTML still renders the sortable `Product | Strategy` and `Gen Strategy` columns against the expected payload fields.
- User verification request:
  - Please open the Weekly Performance page and confirm pass/fail for:
    1. The first data column shows `Product | strategy name_parm` values such as `GBPAUD_C | breakout_R_2_tp30.0_sl10.0`.
    2. The second data column shows the corresponding `gen_strategy_name`.
    3. Sorting and table layout remain usable with the added column.

## Risks/Notes
- The implementation should use canonical row fields already present in the weekly-performance data flow, not string hacks on display labels unless no structured field exists.
- Column width and truncation may need adjustment after adding the new second column.
- User-visible verification is still pending, so the task remains in progress per lifecycle rules.

## Completion Status
- State: AWAITING USER VERIFICATION
- Timestamp: 2026-04-01 17:02:05 Europe/London
