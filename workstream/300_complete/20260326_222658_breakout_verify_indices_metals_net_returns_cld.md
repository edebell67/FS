# Task: Verify Indices Metals Net Returns CLD

## Source
- User Directive: 2026-03-26

## Task Summary
Verify whether the high `indices` and `metals` weekly net returns in the posting package are correctly calculated by checking the underlying `*cld.json` files.

## Context
- Posting package:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-03-26\top5_weekly_posting_package.json`

## Goal
Reconcile the posted top `indices` and `metals` net returns against the underlying trade-level JSON data and identify whether the totals are correct or overstated.

## Plan
- [x] 1. Read the posting package values to verify.
- [x] 2. Locate the relevant `*cld.json` files for `indices` and `metals`.
- [x] 3. Recompute or trace the net return totals from the source data.
- [x] 4. Report whether the published net returns are correct.

## Implementation Log
- **2026-03-26 22:26**: Task created in todo and posting package values loaded for comparison.
- **2026-03-26 22:31**: Loaded current `daily_net_return.json` summaries for `indices` and `metals` and identified the exact top strategies being published: `NQ breakout_R_2_tp20.0_sl5.0` and `SI breakout_R_2_tp20.0_sl5.0`.
- **2026-03-26 22:36**: Located matching `*cld.json` files across the weekly date window `2026-03-19` to `2026-03-26` and inspected individual CLD payloads to confirm trade-level fields including `net_return`, `entry_time`, and `exit_time`.
- **2026-03-26 22:43**: Recomputed totals from non-archive CLD files only. Result: `indices/NQ breakout_R_2_tp20.0_sl5.0` reconciled to about `2920` net across `40` trades; `metals/SI breakout_R_2_tp20.0_sl5.0` reconciled to about `6930` net across `74` trades.
- **2026-03-26 22:49**: Recomputed totals including archive subfolders. Result: `indices` rose to about `15745` net across `325` files; `metals` rose to about `45200` net across `560` files`, which closely matches the inflated published summaries.
- **2026-03-26 22:52**: Confirmed root cause in `C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py`: `process_date()` performs a recursive `Path(target_dir).rglob("*.json")` scan and the initial `_cld.json` load therefore includes archived trades.

## Findings
- The very high `indices` and `metals` weekly totals are not supported by the live/top-level `*cld.json` files for the week.
- The published totals are being inflated by recursive inclusion of archived `cld` files under the product directories.
- For the published `indices` leader (`NQ breakout_R_2_tp20.0_sl5.0`), the posting package showed `14290`, current summary showed `15800`, but non-archive CLD reconciliation produced only about `2920`.
- For the published `metals` leader (`SI breakout_R_2_tp20.0_sl5.0`), the posting package showed `41820`, current summary showed `44810`, but non-archive CLD reconciliation produced only about `6930`.
- Archive-inclusive recomputation closely matched the generated summaries, which strongly indicates the summary pipeline is counting archived trade records.

## Validation
- Posting package checked:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-03-26\top5_weekly_posting_package.json`
- Current summary inputs checked:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\indices\stats\daily_net_return.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\metals\stats\daily_net_return.json`
- Generator logic checked:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py`
- Exact CLD strategy patterns checked:
  - `breakout_R_2_tp20.0_sl5.0*_NQ_*_cld.json`
  - `breakout_R_2_tp20.0_sl5.0*_SI_*_cld.json`

## Outcome
The published net returns for the top `indices` and `metals` strategies are overstated if the intended basis is the live weekly closed trades. The current stats generator is including archived CLD records and that is the likely cause of the inflated totals.
