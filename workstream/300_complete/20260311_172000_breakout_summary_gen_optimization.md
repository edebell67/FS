# Summary Net Generator Investigation & Optimization [2026-03-11]

## 1. Understanding of Requirements
The user reported that `summary_net_generator.py` is not working. 
Investigation revealed:
1. **Multiple Instances:** 8+ generator processes were running simultaneously, causing I/O contention and double-counting of P&L in RAM.
2. **Performance Bottleneck:** The script reads 1800+ `_op.json` files every 5 seconds. On Windows, this takes too long (estimated 3-4 minutes per loop), causing the summary to lag significantly.
3. **Data Aggregation Bug:** Open trades are not aggregated. If a strategy has 10 open trades, 10 separate points are added to the summary at the same timestamp, which can break chart visualization and doesn't reflect total strategy equity.
4. **Stale Source Data:** Trade scripts (`algo_execute_trades_sp.py`) seem to have stopped updating their `_op.json` files around 17:03, but the generator is still trying to process them.

## 2. Plan of Approach
1.  **Cleanup**: Forcefully terminate all existing `summary_net_generator.py` processes.
2.  **Deduplication/Locking**: Implement a simple lock-file mechanism to prevent multiple instances from running.
3.  **Performance Optimization**:
    *   Use `os.scandir` instead of `glob.glob` for faster directory scanning.
    *   Implement `mtime` caching: Only read `_op.json` if the file has been modified since the last read.
4.  **Floating P&L Aggregation**:
    *   Modify the `open_data` logic to SUM the floating P&L of all open trades for a given `(model, product)` before adding a single aggregate point to the summary.
5.  **Logging**: Add loop duration metrics to `summary_gen_debug.log`.

## 3. List of Changes
* **`C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py`**:
    * [ ] Implement `Lock` class for single-instance enforcement.
    * [ ] Add `self.last_mtime_cache = {}` to track file changes.
    * [ ] Replace `glob.glob` with `os.scandir` where appropriate.
    * [ ] Modify `process_mode` to aggregate open trade P&L by `(strat, prod)`.
    * [ ] Add timing logic to the main loop.
    * [ ] Update Version to `V20260311_1720`.

## 4. Execution Log
- [ ] Kill all Python processes matching `summary_net_generator.py`.
- [ ] Apply code optimizations.
- [ ] Start one clean instance.
- [ ] Verify `summary_gen_debug.log` and `_summary_net.json` updates.
