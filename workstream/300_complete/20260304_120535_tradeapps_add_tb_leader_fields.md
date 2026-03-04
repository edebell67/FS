# Task Lifecycle

- Task: Add TB leader metadata fields on first TB classification event
- Project: tradeapps
- Started: 2026-03-04 11:07:00
- Completed: 2026-03-04 12:16:40
- Status: complete

## Objective
Add immutable TB-origin metadata fields on the first TB classification event for each trade:
- `tb_leader`
- `tb_leader_set_at` (timestamp)
- `tb_leader_bucket` (bucket name/id)

## Scope
- TB classification/write path where trade JSON is produced/updated.
- JSON contract in active FS/DB trade writer paths.

## Requirements
1. First-write semantics
- On first TB classification event for a trade, set all three fields.
- Do not overwrite these fields during normal processing once present.

2. Field definitions
- `tb_leader`: `"Y" | "N"`
- `tb_leader_set_at`: ISO timestamp
- `tb_leader_bucket`: TB bucket/group identifier/name at classification time

3. Source-of-truth direction
- TB writes these fields.
- Downstream consumers read; no normal-flow mutation.

4. Config gating
- Applied when config includes Trade Bucket source (`automated_trade_sources` / `Automated Trade Sources`) with fallback to `l_trade_generation_mode == trade_bucket`.

## Implementation
- Updated active writer paths:
  - `TradeApps/breakout/fs/common.py`
  - `TradeApps/breakout/DB/common.py`

### fs/common.py
- Added `_is_trade_bucket_source_enabled()` for config gate.
- Added `_stamp_tb_leader_fields_if_missing(trade_data)` with immutable first-write behavior.
- Extended `live_keys` merge list to persist/sync:
  - `tb_leader`, `tb_leader_set_at`, `tb_leader_bucket`
- Called stamping helper in `_save_trade_json(...)` before write.

### DB/common.py
- Added `_is_trade_bucket_source_enabled()` for config gate.
- Added `_stamp_tb_leader_fields_if_missing(trade_data)` with immutable first-write behavior.
- Called stamping helper in `_save_trade_json(...)` before JSON/DB raw_data update.

## Validation Plan (Executed)
- Syntax check:
  - `python -m py_compile TradeApps/breakout/fs/common.py TradeApps/breakout/DB/common.py`
  - Result: Success
- Presence check:
  - `rg -n "_stamp_tb_leader_fields_if_missing|_is_trade_bucket_source_enabled|tb_leader|tb_leader_set_at|tb_leader_bucket" TradeApps/breakout/fs/common.py TradeApps/breakout/DB/common.py`
  - Result: New helper methods and fields present in both files
- Manual code inspection:
  - Verified first-write guard (`Y/N` immutable if already set)
  - Verified stamping invoked during `_save_trade_json` path

## Notes
- Classification context detection uses TB markers from `source_screen`/`source_group` (`trade_bucket` or `TB_*`).
- Field value rule:
  - `tb_leader = "Y"` when live/order-sent flags are true at first TB classification stamp
  - otherwise `"N"` in TB context
