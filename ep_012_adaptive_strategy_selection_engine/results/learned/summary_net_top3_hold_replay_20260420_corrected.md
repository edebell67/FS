# Forex Summary Net Top-3 Hold Replay

- Source: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex`
- Source files discovered: `8`
- Loaded ranked snapshots: `7`
- Unreadable/empty/schema-missing files skipped: `0`
- Contaminated files excluded: `0`
- Product filter: `forex regex only ([A-Z]{6}_C)`
- Clean files only: `no`
- Strategy filter: `canonical base strategies only`
- Non-forex products found in source: `AUD, CAD, CHF, EUR, GBPEUR_S`
- Generated/suffixed strategies found in source: `77`
- Rule: open current #1 at/after cutoff; keep holding while held product/strategy remains in current top 3; replace with current #1 when held drops out of top 3.
- Ranking: latest `net` per product/strategy at snapshot `last_update`, sorted by net descending, then product, then strategy.
- Scoring: final held strategy net at final snapshot of day minus `$50` per replacement switch.

## Summary

| First open cutoff | Total net | Avg/day | Opened days | Switches | Days |
|---:|---:|---:|---:|---:|---:|
| 00:00 | 260 | 260 | 1 | 2 | 1 |
| 01:00 | 260 | 260 | 1 | 2 | 1 |
| 02:00 | 310 | 310 | 1 | 1 | 1 |
| 03:00 | 310 | 310 | 1 | 1 | 1 |

## Switch Event Sample

| Date | Time | Event | From | From rank | From net | To | To net |
|---|---|---|---|---:|---:|---|---:|
| 2026-04-20 | 01:28:46 | open |  |  |  | EURAUD_C / breakout_2_tp20.0_sl20.0 | 180.0 |
| 2026-04-20 | 06:27:39 | replace | EURAUD_C / breakout_2_tp20.0_sl20.0 | 13 | 140.0 | EURAUD_C / breakout_2_tp10.0_sl20.0 | 240.0 |
| 2026-04-20 | 08:16:22 | replace | EURAUD_C / breakout_2_tp10.0_sl20.0 | 10 | 240.0 | EURAUD_C / breakout_2_tp20.0_sl20.0 | 360.0 |
| 2026-04-20 | 01:28:46 | open |  |  |  | EURAUD_C / breakout_2_tp20.0_sl20.0 | 180.0 |
| 2026-04-20 | 06:27:39 | replace | EURAUD_C / breakout_2_tp20.0_sl20.0 | 13 | 140.0 | EURAUD_C / breakout_2_tp10.0_sl20.0 | 240.0 |
| 2026-04-20 | 08:16:22 | replace | EURAUD_C / breakout_2_tp10.0_sl20.0 | 10 | 240.0 | EURAUD_C / breakout_2_tp20.0_sl20.0 | 360.0 |
| 2026-04-20 | 06:27:39 | open |  |  |  | EURAUD_C / breakout_2_tp10.0_sl20.0 | 240.0 |
| 2026-04-20 | 08:16:22 | replace | EURAUD_C / breakout_2_tp10.0_sl20.0 | 10 | 240.0 | EURAUD_C / breakout_2_tp20.0_sl20.0 | 360.0 |
| 2026-04-20 | 06:27:39 | open |  |  |  | EURAUD_C / breakout_2_tp10.0_sl20.0 | 240.0 |
| 2026-04-20 | 08:16:22 | replace | EURAUD_C / breakout_2_tp10.0_sl20.0 | 10 | 240.0 | EURAUD_C / breakout_2_tp20.0_sl20.0 | 360.0 |

## Per-Day Results

### First open at/after 00:00

| Date | Net after cost | Gross final net | Switches | Final held | Snapshots |
|---|---:|---:|---:|---|---:|
| 2026-04-20 | 260 | 360 | 2 | EURAUD_C / breakout_2_tp20.0_sl20.0 | 7 |

### First open at/after 01:00

| Date | Net after cost | Gross final net | Switches | Final held | Snapshots |
|---|---:|---:|---:|---|---:|
| 2026-04-20 | 260 | 360 | 2 | EURAUD_C / breakout_2_tp20.0_sl20.0 | 7 |

### First open at/after 02:00

| Date | Net after cost | Gross final net | Switches | Final held | Snapshots |
|---|---:|---:|---:|---|---:|
| 2026-04-20 | 310 | 360 | 1 | EURAUD_C / breakout_2_tp20.0_sl20.0 | 7 |

### First open at/after 03:00

| Date | Net after cost | Gross final net | Switches | Final held | Snapshots |
|---|---:|---:|---:|---|---:|
| 2026-04-20 | 310 | 360 | 1 | EURAUD_C / breakout_2_tp20.0_sl20.0 | 7 |
