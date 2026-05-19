---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: backlog
  depends_on: []
  feeds_into:
    - 20260417_150200_rl_sel_phase2_baselines
---

# Phase 1: Data Engineering — Ingest Snapshot Files and Build Feature Dataset

**Source:** `workstream/000_epic/selection_strategy_rl_prd.md` (→ `_processed.md`)
**Destination Folder:** `epics/ep_012_adaptive_strategy_selection_engine/data/`
**Dependency:** None

## Task Summary
Ingest all daily `_frequency.json` snapshot files produced by `weighted_race.py`, parse into a flat minute-by-minute candidate DataFrame, compute live-safe features (no future leakage), and implement the walk-forward day splitter. Outputs are the processed dataset used by all downstream phases.

## Context
- Source files: `TradeApps/breakout/fs/json/live/{product_type}/{date}/_frequency.json`
- Each file contains `snapshots[]` (per-minute leaderboards) and `leaders[]` summary
- Product types: forex, indices, metals, crypto, energy
- Approx one month of data available
- Config values (all configurable): switching_cost=50, safety_margin_pct=0.10, improvement_threshold_pct=0.25

## Plan
- [ ] 1. Write file loader to glob all `_frequency.json` files across product types and dates
  - Test: Print count of files found; must be > 0 for each product type with data
  - Evidence:
- [ ] 2. Parse `snapshots[]` into flat DataFrame: `(date, product_type, minute_index, product, strategy, net, rank, score, score_rank)`
  - Test: DataFrame shape printed; confirm no empty rows; net column has no nulls for known-data dates
  - Evidence:
- [ ] 3. Normalize timestamps to minute resolution; forward-fill gaps where snapshot is missing
  - Test: Verify no gaps > 1 minute within a trading day for a sample date
  - Evidence:
- [ ] 4. Compute live-safe derived features per candidate per minute:
  - net slope over 3/5/10 minutes
  - score slope over 3/5/10 minutes
  - rank delta vs previous snapshot
  - positive streak length (consecutive minutes net > 0)
  - minutes since candidate first appeared in top-5
  - minutes since net first became > 0
  - hold duration (minutes as rank-1)
  - switch count today (based on rank-1 changes)
  - num_positive_candidates in snapshot
  - Test: Spot-check 3 feature columns against raw data manually for 5 rows; confirm values are correct
  - Evidence:
- [ ] 5. Feature leakage audit — confirm no column uses end-of-day or future-minute values
  - Test: Print list of all feature columns; confirm none reference final_net, final_rank, or any post-snapshot aggregation
  - Evidence:
- [ ] 6. Implement walk-forward day-index splitter: given sorted date list, yield `(train_days[], test_day)` pairs; min training window = 5 days
  - Test: For 15 days of data, confirm 10 folds produced with correct train/test boundaries (no overlap)
  - Evidence:
- [ ] 7. Save processed dataset as parquet per day to `epics/ep_012_adaptive_strategy_selection_engine/data/processed/`
  - Test: Load one saved file; confirm schema matches expected columns
  - Evidence:

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: epics/ep_012_adaptive_strategy_selection_engine/data/processed/
  - Objective-Proved: Processed daily parquet files exist and are loadable
  - Status: planned

- Evidence-Type: log_output
  - Artifact: Feature column list printed to console with leakage audit result
  - Objective-Proved: No future-derived features in dataset
  - Status: planned

- Evidence-Type: log_output
  - Artifact: Walk-forward fold summary (train days, test day per fold)
  - Objective-Proved: Splitter respects time ordering with no leakage
  - Status: planned

## Implementation Log
(append entries as work progresses)

## Changes Made
(files created/modified)

## Validation
(commands run and results)

## Risks/Notes
- `_frequency.json` already contains score and score_rank (from weighted_race.py) — use directly, do not recompute
- Some product types may have sparse data on certain dates — handle gracefully with per-product-type date filtering
- Forward-fill only within a trading day; do not fill across days

## Completion Status
NOT STARTED
