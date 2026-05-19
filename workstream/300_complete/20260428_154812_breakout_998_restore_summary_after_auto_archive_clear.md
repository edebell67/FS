Source: User report on 2026-04-28 that json/live/forex/2026-04-28/_summary_net.json and _trades_summary.json were emptied to { \"cleared\": true } after the prior momentum summary-name fix.
Task Type: standard
Task Attributes:
  recurring_task: false
  recurrence_type: scheduled
  recurrence_rule: None
  looping_task: false
  loop_until: manual_stop
  splittable_task: false
  split_output_type: files
  split_spawn_task: false
  split_failure_mode: fail_fast
  workflow_task: false
  workflow_name: ""
  workflow_stage: in_progress
  depends_on: []
  feeds_into: []
Task Summary: Restore the live forex summary files after auto-archive cleared them and patch the archive/runtime flow so _summary_net.json and _trades_summary.json do not remain empty placeholders.
Context: C:\Users\edebe\eds\TradeApps\breakout\fs\common.py, C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py, C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-28\
Destination Folder: C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-28\
Plan:
- [x] 1. Confirm the archive clear path and locate recoverable pre-archive summary data.
- [x] 2. Restore the live summary files from valid data and verify they are populated.
- [x] 3. Patch the archive/runtime behavior so future auto-archive does not leave the live summary files in the cleared placeholder state.
Evidence:
Objective-Delivery-Coverage: 100%
Validation:
- `python C:\Users\edebe\eds\TradeApps\breakout\fs\generate_historical_summary.py C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-28 live 2026-04-28`
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\common.py C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py`
Results:
- Restored [C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-28\_summary_net.json](/C:/Users/edebe/eds/TradeApps/breakout/fs/json/live/forex/2026-04-28/_summary_net.json) to `7,111,730` bytes and [C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-28\_trades_summary.json](/C:/Users/edebe/eds/TradeApps/breakout/fs/json/live/forex/2026-04-28/_trades_summary.json) to `10,303,405` bytes.
- Verified momentum keys in `_summary_net.json` are `momentum_b_0_tp5.0_sl7.0`, `momentum_s_0_tp5.0_sl7.0`, `momentum_bootstrapcheck`, and `momentum_localcheck`.
- Verified `_trades_summary.json` contains `0` generic `momentum` rows.
Execution Log:
- 2026-04-28 15:48:12: Fix-followup task created in workstream/200_inprogress.
- 2026-04-28 15:49:00: Confirmed the regression source in [common.py](/C:/Users/edebe/eds/TradeApps/breakout/fs/common.py) where the auto-archive flow rewrote archived underscore files with a `{ "cleared": true }` payload.
- 2026-04-28 15:49:30: Located preserved `_summary_net_pre_auto_archive.json` snapshots under `archive/`, confirming the clear operation was archival rather than data-loss at the trade-file layer.
- 2026-04-28 15:54:04: Rebuilt the live forex day summary from current trade files using `generate_historical_summary.py`, restoring populated `_summary_net.json` and `_trades_summary.json`.
- 2026-04-28 15:55:00: Patched [common.py](/C:/Users/edebe/eds/TradeApps/breakout/fs/common.py) so auto-archive keeps `_summary_net.json`, `_trades_summary.json`, `_top20.json`, and `_tb_leadership.json` live instead of moving and clearing them.
- 2026-04-28 15:55:30: Re-verified momentum naming integrity after the rebuild and restarted the summary generator.
