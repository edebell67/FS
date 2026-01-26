# Live Data Snapshot and Preservation Plan

## Objectives
- Ensure no live trading data is destroyed during restarts or refreshes.
- Maintain rolling, timestamped snapshots of `Game_trader/live_data` for rapid recovery.
- Provide a clear path to restore the latest snapshot or start a fresh session when needed.

## Snapshot Strategy
- **Scope**: Entire `Game_trader/live_data` directory (participants, logs, market data, config-derived state).
- **Destination**: `Game_trader/live_data_snapshots/` with subfolders named `live_data_<yyyyMMdd_HHmmss>` (e.g., `live_data_20251022_135900`).
- **Frequency**: Default every 1 minute; make interval configurable (e.g., environment variable, config, or admin endpoint).
- **Retention**: Keep the most recent 20 snapshots by default; delete oldest once the limit is exceeded. Both values configurable.

## Implementation Steps
1. **Scheduler**
   - Add a lightweight background task or external service that triggers snapshot creation at the configured interval.
   - Ensure only one snapshot job runs at a time (use a lock or “in-progress” flag).
2. **Snapshot Creation**
   - Copy `live_data` into a temp directory inside `live_data_snapshots` (e.g., `tmp_live_data_<timestamp>`).
   - Verify copy completes, then atomically rename temp folder to the final `live_data_<timestamp>`.
   - Log success/failure via existing logging utilities.
3. **Retention Management**
   - After each snapshot, list existing `live_data_*` folders sorted by timestamp.
   - Remove oldest folders until the count is within the configured retention limit.
4. **Operational Controls**
   - Add admin endpoints or CLI helpers for:
     - Listing available snapshots.
     - Triggering an on-demand snapshot.
     - Restoring a selected snapshot (only when the simulation is stopped) by replacing `live_data` with the snapshot contents.
   - Document required stop/start flow to avoid overwriting current data mid-copy.
5. **Documentation & Monitoring**
   - Update runbooks to cover snapshot schedule, restore steps, and expected log messages.
   - Optionally emit metrics/alerts if snapshot fails or retention prune errors occur.

## Restore Workflow (Future)
- **Safe Stop**: Use `/admin/stop_preserve` to halt trading without wiping state.
- **Select Snapshot**: Choose latest or specific timestamp from `live_data_snapshots`.
- **Restore**: Replace `Game_trader/live_data` with snapshot contents (consider a helper script to handle copy + backup of current state).
- **Restart**: Launch simulation using preserved data or start fresh if desired.

## Next Actions
- Decide where to host the scheduler (within Flask app vs. external service).
- Define configuration mechanism for interval/retention (config file, env vars, admin API).
- Implement snapshot/restore tooling and integrate with logging.
- Verify workflow in staging before enabling in production.
