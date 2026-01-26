# Plan: Reuse S09 Lookback for JSON Generation Rules

## Goal
- Allow `'gen on neg alt_net close'` and `'gen on neg net_return close'` to consider the last *N* trades (where *N* = S09 lookback) instead of only the immediately preceding close.
- Maintain existing behavior when lookback is 1 or history is insufficient.

## Checklist
1. **Clarify Configuration**  
   - Confirm `s09_lookback_var` is available in `config` and determine valid range / default (fallback to 1 if missing).  
   - Decide whether both rules share the same lookback or need separate overrides.

2. **Capture Rolling History**  
   - Replace single-entry caches (`last_closed_trade_by_product`, `_signal`) with per-product/per-signal deques storing up to `lookback` closed-trade summaries.  
   - On every close, append `{net_return, alt_net_return, timestamp, trade_type}` to the relevant deque and trim to `maxlen`.

3. **Helper for Recent Trades**  
   - Implement `_get_recent_closed_trades(product, signal, config)` that:  
     • Reads `lookback = max(1, int(config.get('s09_lookback_var', 1)))`.  
     • Returns a list of up to `lookback` entries from the deque, respecting `apply_csv_rule_at_signal_level`.  
     • Handles missing or stale history gracefully.

4. **Alt-Net Rule Update**  
   - Update `_should_generate_alt_net_json_on_open()` to iterate over the list from step 3 and return `True` if any entry’s `alt_net_return_at_close < 0`.  
   - Preserve existing manual JSON behavior and ensure duplicates are avoided.

5. **Net-Return Rule Update**  
   - In `execute_close_trade`, after recording the current close in the deque, evaluate the last `lookback` entries for negative net returns.  
   - If any qualifying entry exists, emit the closing JSON and set the pending-open flag (as today).  
   - Decide whether to include/exclude the just-closed trade in the evaluation (document the choice).

6. **Validation & Defaults**  
   - Ensure `s09_lookback_var` is parsed as an integer and clamped to a safe maximum (e.g., 20) to avoid excessive memory.  
   - Document that lookback values <=0 revert to 1.

7. **Testing**  
   - Unit tests for helper functions with mocked histories covering positive, negative, and mixed alt/net sequences.  
   - Integration tests simulating sequences of closes to confirm JSON is generated only when any of the last `lookback` trades are negative.  
   - Regression tests for manual Buy/Sell flows (manual JSON must still appear).  
   - Verify behavior when history length is < lookback (should fallback to available entries).

8. **State Reset & Persistence**  
   - When clearing trades (`clear_all_trades_data` or restarting the manager), reset the deques so stale history is not reused.  
   - Optionally persist the deques if cross-session continuity is required; otherwise document that they reset on restart.

9. **Documentation & UI**  
   - Update plan/docs to mention the new lookback-driven behavior.  
   - Add tooltips or labels in the UI explaining that S09 lookback now drives both JSON generation rules.  
   - Include release notes for the change.
