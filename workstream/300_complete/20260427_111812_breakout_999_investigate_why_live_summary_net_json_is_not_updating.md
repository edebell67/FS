# Task: Investigate Why Live Summary Net JSON Is Not Updating

## Created
- 2026-04-27 11:18:12

## Status
- Complete

## Reference
- 999

## Request
- Investigate why `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-27\_summary_net.json` is not being updated.

## Scope
- Trace the writer path for `_summary_net.json` on `live/forex/2026-04-27`.
- Confirm whether `summary_net_generator.py` is running and targeting the correct day folder.
- Verify whether required input trade files are present and changing.
- Identify whether the issue is input absence, generator failure, filtering logic, path resolution, lock/process state, or write suppression.

## Acceptance Criteria
- The root cause blocking updates to `_summary_net.json` is identified.
- The explanation is tied to concrete process, file, and code-path evidence.
- Any mismatch between expected and actual update behavior is documented.

## Validation
- Inspect `summary_net_generator.py` and the active `live/forex/2026-04-27` folder.
- Check generator runtime/lock/log state.
- Verify whether source trade files exist and whether the target file timestamp/content is stale.

## Investigation Notes
- 2026-04-27 11:20: Confirmed target file [\_summary_net.json](/abs/path/C:/Users/edebe/eds/TradeApps/breakout/fs/json/live/forex/2026-04-27/_summary_net.json:1) is stale with `LastWriteTime=2026-04-27 05:02:12`.
- 2026-04-27 11:21: Confirmed live source trade files in `json/live/forex/2026-04-27` are actively updating around `11:23`, including fresh `*_op.json` and `*_cl.json` files. This rules out missing inputs as the blocker.
- 2026-04-27 11:22: Confirmed [config.json](/abs/path/C:/Users/edebe/eds/TradeApps/breakout/fs/config.json:1) is on `run_mode=live`, so the generator should target `live/forex/2026-04-27`.
- 2026-04-27 11:23: Confirmed [summary_net_generator.py](/abs/path/C:/Users/edebe/eds/TradeApps/breakout/fs/summary_net_generator.py:535) uses `summary_gen.lock` and aborts if the PID in that file is alive, without verifying that the process is still the summary generator.
- 2026-04-27 11:24: Confirmed [summary_gen_debug.log](/abs/path/C:/Users/edebe/eds/TradeApps/breakout/fs/summary_gen_debug.log:305378) shows the last successful live update at `2026-04-27 05:02:14`, then no more live updates.
- 2026-04-27 11:24: Confirmed [summary_gen_debug.log](/abs/path/C:/Users/edebe/eds/TradeApps/breakout/fs/summary_gen_debug.log:305380) begins repeated restarts at `2026-04-27 07:05:46`, each aborting with `Another instance (PID 20508) is running.`
- 2026-04-27 11:25: Confirmed [summary_gen.lock](/abs/path/C:/Users/edebe/eds/TradeApps/breakout/fs/summary_gen.lock:1) still contains `20508`, but the lock file timestamp is `2026-04-27 00:36:23`, so it was not rewritten by the later aborting launches.
- 2026-04-27 11:26: Confirmed current PID `20508` is a live `cmd.exe` started at `2026-04-27 07:05:39`, not the original summary generator process.

## Root Cause
- `_summary_net.json` stopped updating because the original summary generator process exited without clearing `summary_gen.lock`.
- The lock file retained PID `20508`.
- Later, Windows reused PID `20508` for an unrelated `cmd.exe` process started at `07:05:39`.
- The lock check in [summary_net_generator.py](/abs/path/C:/Users/edebe/eds/TradeApps/breakout/fs/summary_net_generator.py:535) only checks whether the PID is alive, not whether it still belongs to `summary_net_generator.py`.
- As a result, every scheduled restart after `07:05` falsely concluded that another generator instance was already running and aborted before processing live trade files.

## Conclusion
- The blocker is a stale lock plus PID reuse false-positive.
- The writer path, input files, mode selection, and day-folder targeting are all functioning as expected up to the lock gate.

## Outcome
- Investigation complete.
- No code change applied in this task.
- Follow-on fix should harden the lock ownership check or clear the invalid lock before restart.
