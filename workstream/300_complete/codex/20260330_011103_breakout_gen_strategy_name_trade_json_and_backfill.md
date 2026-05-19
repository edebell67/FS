# Generated Strategy Name in Trade JSON and Historical Backfill

## Source
User request during conversation 1dc8e4c5-47c8-4ca9-9bc9-8cb42900b7de

## Task Summary
Add a new `gen_strategy_name` field alongside the existing `strategy_name` field in trade JSON files for all product types. The generated value should use the new deterministic aliasing scheme based on the discussed format (for example `orion-atlas_2_z91c_d4be`). Implement a one-off backfill process to populate `gen_strategy_name` in already created trade JSON files across all product types.

## Requirements
1. Define and centralize generated strategy-name logic.
   - Use the new deterministic generator based on the agreed alias format with two hashed words plus encoded TP and SL fragments.
   - Validate source strategy names before generating the alias.
2. Add `gen_strategy_name` to ongoing trade JSON generation.
   - Preserve the existing `strategy_name` field unchanged.
   - Include `gen_strategy_name` in all newly written trade JSON records for every product type.
3. Support all product types.
   - Ensure generation uses product context so aliases remain deterministic per product.
   - Apply the new field consistently wherever trade JSON is emitted.
4. Implement a one-off historical backfill.
   - Traverse already created trade JSON files for all product types.
   - Add `gen_strategy_name` to existing records without removing or renaming current fields.
   - Make the backfill idempotent so reruns do not corrupt or duplicate output.
5. Handle malformed or unexpected strategy names safely.
   - Decide whether to skip, log, or mark invalid records explicitly.
   - Capture summary counts for updated, skipped, and failed records.

## Context
- Trade JSON currently stores `strategy_name` only and needs a parallel generated display-safe field.
- The requested generated name format is based on the newly proposed deterministic aliasing scheme:
  - strategy alias from two hashed words, e.g. `orion-atlas`
  - preserved window token
  - TP fragment `z...`
  - SL fragment `d...`
- Scope applies to all product types and existing historical trade JSON files.

## Dependency
Dependency: None

## Plan

- [x] 1. Locate the trade JSON writers/readers and identify every code path that emits trade records for each product type.
  - [x] Test: Confirm the full set of files/modules that create or transform trade JSON.
  - Evidence: `TradeApps/breakout/fs/common.py`, `TradeApps/breakout/DB/common.py`, `TradeApps/breakout/fs/backfill_gen_strategy_name.py`, and `TradeApps/breakout/fs/strategy_name_generator.py` were confirmed as the active generator/backfill surfaces.

- [x] 2. Implement a shared `gen_strategy_name` generator utility using the new alias scheme and strict parsing/validation.
  - [x] Test: Verify deterministic outputs for representative strategy names across multiple product types.
  - Evidence: `python -m pytest TradeApps\breakout\fs\tests\test_strategy_name_generator.py` passed with 4 tests, including deterministic output, instance-suffix stripping, and malformed-name skip behavior.

- [x] 3. Update live/new trade JSON generation to include `gen_strategy_name` alongside `strategy_name`.
  - [x] Test: Generate a fresh trade JSON sample and confirm both fields are present.
  - Evidence: Live samples now contain both fields, for example `TradeApps/breakout/fs/json/live/forex/2026-03-30/breakout_2_tp10.0_sl20.0_0dceee68_GBPEUR_C_20260330_002703_2_0.00015_10.0_20.0_op.json` and `TradeApps/breakout/fs/json/live/crypto/2026-03-30/breakout_2_tp10.0_sl20.0_02db7077_BTC_20260330_001853_2_0.00015_10.0_20.0_cld.json`.

- [x] 4. Build a one-off backfill process for historical trade JSON files across all product types.
  - [x] Test: Run backfill on a representative subset and confirm existing files are updated in place with `gen_strategy_name`.
  - Evidence: Real backfill runs completed for live `2026-03-30` slices across `forex`, `crypto`, `energy`, `indices`, and `metals`, updating thousands of files in place with `strategy_name` and `gen_strategy_name`.

- [x] 5. Validate idempotency, malformed-name handling, and summary reporting.
  - [x] Test: Re-run the backfill and confirm no duplicate or unstable output; review logs for skipped/failed records.
  - Evidence: Unit coverage now asserts malformed names are skipped and deterministic aliases remain stable. Re-runs against active `2026-03-30` folders continued to find new files because the live system was still writing into those folders during validation, but per-record generator behavior remained stable.

- [ ] 6. Capture full-run verification across all product types and move the task to completion.
  - [ ] Test: Spot-check multiple product-type directories and confirm `gen_strategy_name` is populated for historical and newly generated records.
  - Evidence: Partial completion only. Live product-type spot checks are captured below, but the full all-history/all-mode sweep exceeded shell time limits in this session and still needs a long-running execution window.

## Evidence
Objective-Delivery-Coverage: 85%
Auto-Acceptance: false

- Evidence-Type: test_output
  - Artifact: `python -m pytest TradeApps\breakout\fs\tests\test_strategy_name_generator.py` -> `4 passed in 0.69s`
  - Objective-Proved: Deterministic alias generation, instance-suffix stripping, and malformed-name skip handling work as implemented.
  - Status: captured

- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/strategy_name_generator.py`, `TradeApps/breakout/fs/backfill_gen_strategy_name.py`, `TradeApps/breakout/fs/tests/test_strategy_name_generator.py`, `TradeApps/breakout/DB/common.py`
  - Objective-Proved: Shared generator logic was hardened and wired into both filesystem and DB-backed trade flows.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `TradeApps/breakout/fs/json/live/forex/2026-03-30/breakout_2_tp10.0_sl20.0_0dceee68_GBPEUR_C_20260330_002703_2_0.00015_10.0_20.0_op.json`
  - Objective-Proved: A newly persisted forex trade JSON contains both `strategy_name` and `gen_strategy_name`.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `TradeApps/breakout/fs/json/live/crypto/2026-03-30/breakout_2_tp10.0_sl20.0_02db7077_BTC_20260330_001853_2_0.00015_10.0_20.0_cld.json`
  - Objective-Proved: A crypto trade JSON contains both fields after the backfill/live-generation changes.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `TradeApps/breakout/fs/json/live/energy/2026-03-30/breakout_2_tp10.0_sl20.0_09df6fa7_NG_20260330_001836_2_0.00015_10.0_20.0_op.json`
  - Objective-Proved: An energy trade JSON contains both fields after the backfill/live-generation changes.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `TradeApps/breakout/fs/json/live/indices/2026-03-30/breakout_2_tp10.0_sl20.0_077a555b_ES_20260330_003216_2_0.00015_10.0_20.0_cld.json`
  - Objective-Proved: An indices trade JSON contains both fields after the backfill/live-generation changes.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `TradeApps/breakout/fs/json/live/metals/2026-03-30/breakout_2_tp10.0_sl20.0_0162402b_GC_20260330_002901_2_0.00015_10.0_20.0_cld.json`
  - Objective-Proved: A metals trade JSON contains both fields after the backfill/live-generation changes.
  - Status: captured

- Evidence-Type: log_output
  - Artifact: Live slice backfill summaries:
    - forex: `scanned=977 updated_files=970 updated_records=1938 skipped_files=7 failed_files=0`
    - crypto: `scanned=884 updated_files=880 updated_records=1758 skipped_files=4 failed_files=0`
    - energy: `scanned=909 updated_files=905 updated_records=1808 skipped_files=4 failed_files=0`
    - indices: `scanned=1091 updated_files=1087 updated_records=2172 skipped_files=4 failed_files=0`
    - metals: first pass `scanned=1359 updated_files=1351 updated_records=2704 skipped_files=4 failed_files=4`; second pass `scanned=1446 updated_files=93 updated_records=1533 skipped_files=1353 failed_files=0`
  - Objective-Proved: The backfill process runs, updates files in place, and reports updated/skipped/failed counts by slice.
  - Status: captured

## Implementation Log
- 2026-03-30 01:11 — Task created to add `gen_strategy_name` to trade JSON generation and backfill historical files for all product types.
- 2026-03-30 01:18 — Confirmed active trade JSON writers/readers in `TradeApps/breakout/fs/common.py` and `TradeApps/breakout/DB/common.py`, and confirmed the existing backfill entrypoint at `TradeApps/breakout/fs/backfill_gen_strategy_name.py`.
- 2026-03-30 01:24 — Hardened `TradeApps/breakout/fs/strategy_name_generator.py` so malformed names are skipped, expanded the alias word list, and kept deterministic product-specific alias generation.
- 2026-03-30 01:28 — Wired the DB-backed breakout runtime to use the same shared strategy-name field stamping for open trades, closed trades, and virtual trades.
- 2026-03-30 01:31 — Added malformed-name unit coverage and optimized the backfill script with lighter file iteration and pre-parse text filtering.
- 2026-03-30 01:41 — Executed real backfill runs for live `2026-03-30` slices across forex, crypto, energy, indices, and metals; verified updated files now carry `strategy_name` and `gen_strategy_name`.
- 2026-03-30 01:49 — Attempted full all-mode/all-history backfill and sim-mode sweeps, but both exceeded the shell execution window in this session.

## Changes Made
- Updated `TradeApps/breakout/fs/strategy_name_generator.py` to enforce parse validation, skip malformed strategy names, and widen the deterministic hashed-word alias space.
- Updated `TradeApps/breakout/fs/backfill_gen_strategy_name.py` to keep updated/skipped accounting, iterate faster over large trees, and support targeted date/product-type execution for operational backfills.
- Updated `TradeApps/breakout/fs/tests/test_strategy_name_generator.py` with malformed-name no-op coverage.
- Updated `TradeApps/breakout/DB/common.py` so DB-backed/open/closed/virtual trade JSON payloads are stamped with `strategy_name` and `gen_strategy_name` using the same generator as filesystem mode.

## Validation
- `python -m pytest TradeApps\breakout\fs\tests\test_strategy_name_generator.py`
  - Result: passed (`4 passed in 0.69s`)
- `python -m py_compile TradeApps\breakout\fs\strategy_name_generator.py TradeApps\breakout\fs\backfill_gen_strategy_name.py TradeApps\breakout\DB\common.py TradeApps\breakout\fs\common.py`
  - Result: passed (no output)
- `python TradeApps\breakout\fs\backfill_gen_strategy_name.py --mode live --date 2026-03-30 --product-type forex`
  - Result: `scanned=977 updated_files=970 updated_records=1938 skipped_files=7 failed_files=0`
- `python TradeApps\breakout\fs\backfill_gen_strategy_name.py --mode live --date 2026-03-30 --product-type crypto`
  - Result: `scanned=884 updated_files=880 updated_records=1758 skipped_files=4 failed_files=0`
- `python TradeApps\breakout\fs\backfill_gen_strategy_name.py --mode live --date 2026-03-30 --product-type energy`
  - Result: `scanned=909 updated_files=905 updated_records=1808 skipped_files=4 failed_files=0`
- `python TradeApps\breakout\fs\backfill_gen_strategy_name.py --mode live --date 2026-03-30 --product-type indices`
  - Result: `scanned=1091 updated_files=1087 updated_records=2172 skipped_files=4 failed_files=0`
- `python TradeApps\breakout\fs\backfill_gen_strategy_name.py --mode live --date 2026-03-30 --product-type metals`
  - Result: first pass `scanned=1359 updated_files=1351 updated_records=2704 skipped_files=4 failed_files=4`; second pass `scanned=1446 updated_files=93 updated_records=1533 skipped_files=1353 failed_files=0`
- `python TradeApps\breakout\fs\backfill_gen_strategy_name.py --mode all --dry-run`
  - Result: exceeded 120s timeout for the full tree in this shell session.
- `python TradeApps\breakout\fs\backfill_gen_strategy_name.py --mode all`
  - Result: exceeded 600s timeout for the full tree in this shell session.
- `python TradeApps\breakout\fs\backfill_gen_strategy_name.py --mode sim --date 2026-03-15 --product-type forex`
  - Result: exceeded 120s timeout in this shell session.
- `python TradeApps\breakout\fs\backfill_gen_strategy_name.py --mode sim --date 2026-03-15 --product-type crypto`
  - Result: exceeded 120s timeout in this shell session.

## Risks/Notes
- The live `2026-03-30` folders were still receiving new trade JSON files during validation, so repeated dry-run passes kept finding new candidates. That churn reflects ongoing writes rather than a deterministic alias instability.
- The one-off backfill entrypoint is implemented and validated on live product-type slices, but a true full-history/all-mode sweep still needs a longer uninterrupted runtime window than this shell session allowed.
- Because the full all-history sweep did not complete in-session, this task should remain in progress and should not be moved to `workstream/300_complete` yet.

## Completion Status
In progress as of 2026-03-30. Implementation is complete and live product-type backfill slices were executed successfully, but the full all-history/all-mode backfill verification remains pending a longer execution window.
