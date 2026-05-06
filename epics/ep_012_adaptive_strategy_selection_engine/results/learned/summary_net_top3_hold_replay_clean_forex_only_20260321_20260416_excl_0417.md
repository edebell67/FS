# Forex Summary Net Top-3 Hold Replay

- Source: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex`
- Source files discovered: `42`
- Loaded ranked snapshots: `0`
- Unreadable/empty/schema-missing files skipped: `0`
- Contaminated files excluded: `41`
- Product filter: `forex regex only ([A-Z]{6}_C)`
- Clean files only: `yes`
- Non-forex products found in source: `AUD, BTC, BZ, CAD, CHF, CL, ES, ETH, EUR, GBP, GBPEUR_S, GC, HG, NG, NQ, NZD, RTY, SI, SOL, XRP, YM, ZN, ZT`
- Rule: open current #1 at/after cutoff; keep holding while held product/strategy remains in current top 3; replace with current #1 when held drops out of top 3.
- Ranking: latest `net` per product/strategy at snapshot `last_update`, sorted by net descending, then product, then strategy.
- Scoring: final held strategy net at final snapshot of day minus `$50` per replacement switch.

## Summary

| First open cutoff | Total net | Avg/day | Opened days | Switches | Days |
|---:|---:|---:|---:|---:|---:|
| 00:00 | 0 | 0 | 0 | 0 | 0 |
| 01:00 | 0 | 0 | 0 | 0 | 0 |
| 02:00 | 0 | 0 | 0 | 0 | 0 |
| 03:00 | 0 | 0 | 0 | 0 | 0 |

## Switch Event Sample

| Date | Time | Event | From | From rank | From net | To | To net |
|---|---|---|---|---:|---:|---|---:|

## Per-Day Results
