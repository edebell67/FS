# sp_001 Sequential Processing Checklist

- [x] Confirm tracking table script (`db_scripts/create_sp_001_tracking_table.sql`) exists and matches required schema.
- [x] Ensure bookmark retrieval defaults to `GETDATE()` when a product has no prior record.
- [x] Materialize `vw_201_zone_distribution_snapshots` into `#vw_snapshot` once per run.
- [x] Pull all snapshots with `snapshot_time > last_processed_time` for each product, ordered by `snapshot_time DESC`.
- [x] Persist a descending `row_num` column in `#snapshot_batch` for deterministic pair comparisons.
- [x] Iterate through each adjacent snapshot pair to detect number->NULL transitions for buy/sell logic.
- [x] Skip processing when fewer than two new snapshots exist for a product without raising errors.
- [x] Update the bookmark to the newest processed snapshot time after each product batch.
- [x] Document the no-tie-breaker assumption (time-only ordering) and rationale for ignoring historical backlog.
- [ ] Validate the stored procedure end-to-end to ensure `#snapshot_batch` populates and signals fire as expected.
