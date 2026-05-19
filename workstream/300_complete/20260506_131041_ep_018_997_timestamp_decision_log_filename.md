Source: User request on 2026-05-06 to modify `C:\Users\edebe\eds\epics\ep_018_multi_product_trade_manager\trade_manager_pair_entry_maintain_buy_sell.py` so it generates a decision log file with a timestamp in the filename.
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
  depends_on: []
  feeds_into: []
Task Summary: Update the trade manager so decision-log CSV output is written to a timestamped filename per run rather than the current static `{product}_decision_log.csv`, reducing overwrite/append ambiguity across separate executions while preserving the existing row structure and logging behavior.
Context: The current decision log is emitted by `log_decision()` in `C:\Users\edebe\eds\epics\ep_018_multi_product_trade_manager\trade_manager_pair_entry_maintain_buy_sell.py`, which writes to `Path(cfg["output_dir"]) / f"{v.product}_decision_log.csv"`. The change should keep log writes stable within a single run while ensuring a distinct timestamped file is created for each new execution.
Destination Folder: None
Dependency: None

## Plan
- [x] 1. Create and activate the lifecycle task for this requirement and confirm the current decision-log filename behavior in the script.
  - [x] Test: Repository review confirms the authoritative decision-log path logic and this lifecycle file is moved into the active in-progress lane.
  - Evidence: Confirmed `log_decision()` originally targeted a static `{product}_decision_log.csv` path and this lifecycle file is now archived at `C:\Users\edebe\eds\workstream\300_complete\20260506_131041_ep_018_997_timestamp_decision_log_filename.md`.
- [x] 2. Patch the script so decision logs use a timestamped filename that remains stable for the duration of one process run.
  - [x] Test: Code review confirms the timestamp is introduced once per run and the constructed path for decision logs includes that timestamp in the filename.
  - Evidence: Added `get_run_timestamp(cfg)` and changed the decision log path to `f"{v.product}_decision_log_{run_timestamp}.csv"` in `trade_manager_pair_entry_maintain_buy_sell.py`.
- [x] 3. Run a focused validation that exercises `log_decision()` and confirms a timestamped decision-log CSV is created as expected.
  - [x] Test: A local Python validation creates a decision log in a temporary output directory and confirms the generated filename matches the timestamped pattern and contains the CSV header/data row.
  - Evidence: Validation output confirmed `eurusd_decision_log_20260506_131552.csv` was created under `C:\Users\edebe\eds\workstream\artefacts\decision_log_test` with `rows=2`, `header_first=timestamp`, and `action_value=HOLD_SIZE`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: `python -c "import csv, importlib.util, shutil; from pathlib import Path; module_path=Path(r'C:\\Users\\edebe\\eds\\epics\\ep_018_multi_product_trade_manager\\trade_manager_pair_entry_maintain_buy_sell.py'); spec=importlib.util.spec_from_file_location('tm_pair', module_path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); tmp_dir=Path(r'C:\\Users\\edebe\\eds\\workstream\\artefacts\\decision_log_test'); shutil.rmtree(tmp_dir, ignore_errors=True); tmp_dir.mkdir(parents=True, exist_ok=True); cfg={'output_dir': str(tmp_dir), 'commission_pips': 0.1, 'pip_size_default': 0.0001, 'pip_sizes': {'eurusd': 0.0001}}; v=mod.Variant(product='eurusd', name='eurusd_bank_10', bank_threshold=10); t=mod.Trade(signal='BUY', entry_price=1.1, size=1000, total_cost=1.0, open_pnl=2.5, realised_pnl=0.5, last_bid=1.1001, last_ask=1.1003); v.trades.append(t); mod.log_decision(v, t, 'HOLD_SIZE', 'validation', 1.1005, 1.1007, cfg); files=sorted(tmp_dir.glob('*.csv')); path=files[0]; rows=list(csv.reader(path.open())); print(f'output_dir={tmp_dir}'); print(f'file={path.name}'); print(f'rows={len(rows)}'); print(f'header_first={rows[0][0]}'); print(f'action_value={rows[1][5]}')"`
  - Objective-Proved: Confirms the updated code creates a timestamped decision-log CSV in the expected naming format and writes both header and data rows.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\epics\ep_018_multi_product_trade_manager\trade_manager_pair_entry_maintain_buy_sell.py`
  - Objective-Proved: Confirms the code change introduces a cached run timestamp and uses it in the decision-log filename format.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: C:\Users\edebe\eds\workstream\300_complete\20260506_131041_ep_018_997_timestamp_decision_log_filename.md
  - Objective-Proved: Confirms the lifecycle task captured the implementation and validation trail for the timestamped decision-log requirement.
  - Status: captured

## Implementation Log
- 2026-05-06 13:10:41 BST: User requested the first requirement: modify the script to generate a decision log file with a timestamp in the filename.
- 2026-05-06 13:10:41 BST: Reviewed the script and confirmed `log_decision()` currently writes to a static file path named `{product}_decision_log.csv`.
- 2026-05-06 13:10:41 BST: Created this lifecycle file in `workstream\100_todo` for the implementation task.
- 2026-05-06 13:10:41 BST: Moved the task to `workstream\200_inprogress` when active implementation began.
- 2026-05-06 13:10:41 BST: Patched the script to generate a per-run timestamp once via `get_run_timestamp(cfg)` and append that timestamp to the decision-log filename.
- 2026-05-06 13:15:52 BST: Ran a focused local validation against `log_decision()` using a workspace artifact folder and confirmed a timestamped CSV file was created with the expected header and one data row.

## Changes Made
- Created a dedicated lifecycle task for the timestamped decision-log filename requirement.
- Updated `trade_manager_pair_entry_maintain_buy_sell.py` so decision logs now write to `{product}_decision_log_{yyyyMMdd_HHmmss}.csv` using a timestamp cached in `cfg` for the duration of one run.

## Validation
- Verified `log_decision()` is the authoritative decision-log writer in `trade_manager_pair_entry_maintain_buy_sell.py`.
- Verified the pre-change decision-log filename is static and does not include a timestamp.
- Verified the code change now derives a single run timestamp and uses it in the decision-log filename, avoiding a new file per row.
- Executed a local validation command that wrote `eurusd_decision_log_20260506_131552.csv` to `C:\Users\edebe\eds\workstream\artefacts\decision_log_test`.
- Confirmed the generated CSV contained 2 rows total, with `timestamp` as the first header column and `HOLD_SIZE` recorded in the action column for the test row.

## Risks/Notes
- The timestamp should be generated once per process run, not once per log row, otherwise each decision could create a new file.
- The change should preserve existing CSV columns and append behavior within the same run.
- If downstream tooling expects the old static filename, that consumer will need to be updated or made pattern-aware.

## Completion Status
- State: Complete
- Timestamp: 2026-05-06 13:15:52 BST
