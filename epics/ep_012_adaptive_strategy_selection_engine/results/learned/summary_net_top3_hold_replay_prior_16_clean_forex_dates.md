# Forex Summary Net Top-3 Hold Replay

- Source: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex`
- Source files discovered: `27`
- Loaded ranked snapshots: `26`
- Unreadable/empty/schema-missing files skipped: `0`
- Contaminated files excluded: `0`
- Product filter: `forex regex only ([A-Z]{6}_C)`
- Clean files only: `no`
- Non-forex products found in source: `AUD, BTC, BZ, CAD, CHF, CL, ES, ETH, EUR, GBP, GBPEUR_S, GC, HG, NG, NQ, NZD, RTY, SI, SOL, XRP, YM, ZN, ZT`
- Rule: open current #1 at/after cutoff; keep holding while held product/strategy remains in current top 3; replace with current #1 when held drops out of top 3.
- Ranking: latest `net` per product/strategy at snapshot `last_update`, sorted by net descending, then product, then strategy.
- Scoring: final held strategy net at final snapshot of day minus `$50` per replacement switch.

## Summary

| First open cutoff | Total net | Avg/day | Opened days | Switches | Days |
|---:|---:|---:|---:|---:|---:|
| 00:00 | 464,372 | 30,958 | 15 | 3 | 15 |
| 01:00 | 464,372 | 30,958 | 15 | 3 | 15 |
| 02:00 | 464,372 | 30,958 | 15 | 3 | 15 |
| 03:00 | 464,372 | 30,958 | 15 | 3 | 15 |

## Switch Event Sample

| Date | Time | Event | From | From rank | From net | To | To net |
|---|---|---|---|---:|---:|---|---:|
| 2026-03-24 | 22:16:37 | open |  |  |  | EURAUD_C / breakout_R_Rev_3_tp20.0_sl5.0 | 1272.5 |
| 2026-03-26 | 21:07:26 | open |  |  |  | GBPAUD_C / breakout_2_tp20.0_sl5.0 | 470.0 |
| 2026-03-27 | 08:07:01 | open |  |  |  | GBPAUD_C / breakout_2_tp20.0_sl20.0 | 360.0 |
| 2026-03-29 | 23:59:54 | open |  |  |  | GBPNZD_C / breakout_2_tp3.0_sl20.0 | 10.0 |
| 2026-03-30 | 15:06:45 | open |  |  |  | EURAUD_C / breakout_R_2_tp20.0_sl20.0 | 360.0 |
| 2026-03-31 | 22:01:51 | open |  |  |  | GBPAUD_C / breakout_R_2_tp3.0_sl10.0_400f3f6d | 401350.0 |
| 2026-03-31 | 23:59:35 | replace | GBPAUD_C / breakout_R_2_tp3.0_sl10.0_400f3f6d | 417 | 10.0 | GBPNZD_C / breakout_R_2_tp50.0_sl10.0 | 1420.0 |
| 2026-04-01 | 19:22:47 | open |  |  |  | GBPAUD_C / breakout_R_2_tp10.0_sl20.0 | 880.0 |
| 2026-04-02 | 22:15:06 | open |  |  |  | EURNZD_C / breakout_R_2_tp30.0_sl50.0 | 1120.0 |
| 2026-04-03 | 16:56:03 | open |  |  |  | GBPNZD_C / breakout_R_2_tp30.0_sl10.0 | 560.0 |
| 2026-04-05 | 23:59:57 | open |  |  |  | EURNZD_C / breakout_R_2_tp30.0_sl10.0 | 280.0 |
| 2026-04-06 | 18:21:36 | open |  |  |  | GBPEUR_C / breakout_2_tp20.0_sl30.0 | 540.0 |
| 2026-04-06 | 23:59:49 | replace | GBPEUR_C / breakout_2_tp20.0_sl30.0 | 57 | 220.0 | GBPAUD_C / breakout_2_tp20.0_sl10.0 | 520.0 |
| 2026-04-07 | 11:25:55 | open |  |  |  | EURAUD_C / breakout_R_2_tp20.0_sl10.0 | 360.0 |
| 2026-04-07 | 23:59:47 | replace | EURAUD_C / breakout_R_2_tp20.0_sl10.0 | 14 | 520.0 | GBPAUD_C / breakout_R_2_tp30.0_sl10.0 | 820.0 |
| 2026-04-08 | 13:07:35 | open |  |  |  | GBPAUD_C / breakout_R_2_tp20.0_sl10.0 | 720.0 |
| 2026-04-09 | 16:32:35 | open |  |  |  | GBPAUD_C / breakout_R_2_tp20.0_sl20.0 | 1255.0 |
| 2026-04-17 | 20:59:42 | open |  |  |  | GBPEUR_C / breakout_R_2_tp10.0_sl20.0_12141c72 | 830.0 |
| 2026-03-24 | 22:16:37 | open |  |  |  | EURAUD_C / breakout_R_Rev_3_tp20.0_sl5.0 | 1272.5 |
| 2026-03-26 | 21:07:26 | open |  |  |  | GBPAUD_C / breakout_2_tp20.0_sl5.0 | 470.0 |
| 2026-03-27 | 08:07:01 | open |  |  |  | GBPAUD_C / breakout_2_tp20.0_sl20.0 | 360.0 |
| 2026-03-29 | 23:59:54 | open |  |  |  | GBPNZD_C / breakout_2_tp3.0_sl20.0 | 10.0 |
| 2026-03-30 | 15:06:45 | open |  |  |  | EURAUD_C / breakout_R_2_tp20.0_sl20.0 | 360.0 |
| 2026-03-31 | 22:01:51 | open |  |  |  | GBPAUD_C / breakout_R_2_tp3.0_sl10.0_400f3f6d | 401350.0 |
| 2026-03-31 | 23:59:35 | replace | GBPAUD_C / breakout_R_2_tp3.0_sl10.0_400f3f6d | 417 | 10.0 | GBPNZD_C / breakout_R_2_tp50.0_sl10.0 | 1420.0 |
| 2026-04-01 | 19:22:47 | open |  |  |  | GBPAUD_C / breakout_R_2_tp10.0_sl20.0 | 880.0 |
| 2026-04-02 | 22:15:06 | open |  |  |  | EURNZD_C / breakout_R_2_tp30.0_sl50.0 | 1120.0 |
| 2026-04-03 | 16:56:03 | open |  |  |  | GBPNZD_C / breakout_R_2_tp30.0_sl10.0 | 560.0 |
| 2026-04-05 | 23:59:57 | open |  |  |  | EURNZD_C / breakout_R_2_tp30.0_sl10.0 | 280.0 |
| 2026-04-06 | 18:21:36 | open |  |  |  | GBPEUR_C / breakout_2_tp20.0_sl30.0 | 540.0 |

## Per-Day Results

### First open at/after 00:00

| Date | Net after cost | Gross final net | Switches | Final held | Snapshots |
|---|---:|---:|---:|---|---:|
| 2026-03-24 | 1,272 | 1,272 | 0 | EURAUD_C / breakout_R_Rev_3_tp20.0_sl5.0 | 2 |
| 2026-03-26 | 535 | 535 | 0 | GBPAUD_C / breakout_2_tp20.0_sl5.0 | 2 |
| 2026-03-27 | 360 | 360 | 0 | GBPAUD_C / breakout_2_tp20.0_sl20.0 | 1 |
| 2026-03-29 | 10 | 10 | 0 | GBPNZD_C / breakout_2_tp3.0_sl20.0 | 1 |
| 2026-03-30 | 520 | 520 | 0 | EURAUD_C / breakout_R_2_tp20.0_sl20.0 | 2 |
| 2026-03-31 | 1,370 | 1,420 | 1 | GBPNZD_C / breakout_R_2_tp50.0_sl10.0 | 2 |
| 2026-04-01 | 880 | 880 | 0 | GBPAUD_C / breakout_R_2_tp10.0_sl20.0 | 2 |
| 2026-04-02 | 1,100 | 1,100 | 0 | EURNZD_C / breakout_R_2_tp30.0_sl50.0 | 2 |
| 2026-04-03 | 560 | 560 | 0 | GBPNZD_C / breakout_R_2_tp30.0_sl10.0 | 2 |
| 2026-04-05 | 280 | 280 | 0 | EURNZD_C / breakout_R_2_tp30.0_sl10.0 | 1 |
| 2026-04-06 | 470 | 520 | 1 | GBPAUD_C / breakout_2_tp20.0_sl10.0 | 2 |
| 2026-04-07 | 770 | 820 | 1 | GBPAUD_C / breakout_R_2_tp30.0_sl10.0 | 2 |
| 2026-04-08 | 1,260 | 1,260 | 0 | GBPAUD_C / breakout_R_2_tp20.0_sl10.0 | 2 |
| 2026-04-09 | 1,255 | 1,255 | 0 | GBPAUD_C / breakout_R_2_tp20.0_sl20.0 | 1 |
| 2026-04-17 | 453,730 | 453,730 | 0 | GBPEUR_C / breakout_R_2_tp10.0_sl20.0_12141c72 | 2 |

### First open at/after 01:00

| Date | Net after cost | Gross final net | Switches | Final held | Snapshots |
|---|---:|---:|---:|---|---:|
| 2026-03-24 | 1,272 | 1,272 | 0 | EURAUD_C / breakout_R_Rev_3_tp20.0_sl5.0 | 2 |
| 2026-03-26 | 535 | 535 | 0 | GBPAUD_C / breakout_2_tp20.0_sl5.0 | 2 |
| 2026-03-27 | 360 | 360 | 0 | GBPAUD_C / breakout_2_tp20.0_sl20.0 | 1 |
| 2026-03-29 | 10 | 10 | 0 | GBPNZD_C / breakout_2_tp3.0_sl20.0 | 1 |
| 2026-03-30 | 520 | 520 | 0 | EURAUD_C / breakout_R_2_tp20.0_sl20.0 | 2 |
| 2026-03-31 | 1,370 | 1,420 | 1 | GBPNZD_C / breakout_R_2_tp50.0_sl10.0 | 2 |
| 2026-04-01 | 880 | 880 | 0 | GBPAUD_C / breakout_R_2_tp10.0_sl20.0 | 2 |
| 2026-04-02 | 1,100 | 1,100 | 0 | EURNZD_C / breakout_R_2_tp30.0_sl50.0 | 2 |
| 2026-04-03 | 560 | 560 | 0 | GBPNZD_C / breakout_R_2_tp30.0_sl10.0 | 2 |
| 2026-04-05 | 280 | 280 | 0 | EURNZD_C / breakout_R_2_tp30.0_sl10.0 | 1 |
| 2026-04-06 | 470 | 520 | 1 | GBPAUD_C / breakout_2_tp20.0_sl10.0 | 2 |
| 2026-04-07 | 770 | 820 | 1 | GBPAUD_C / breakout_R_2_tp30.0_sl10.0 | 2 |
| 2026-04-08 | 1,260 | 1,260 | 0 | GBPAUD_C / breakout_R_2_tp20.0_sl10.0 | 2 |
| 2026-04-09 | 1,255 | 1,255 | 0 | GBPAUD_C / breakout_R_2_tp20.0_sl20.0 | 1 |
| 2026-04-17 | 453,730 | 453,730 | 0 | GBPEUR_C / breakout_R_2_tp10.0_sl20.0_12141c72 | 2 |

### First open at/after 02:00

| Date | Net after cost | Gross final net | Switches | Final held | Snapshots |
|---|---:|---:|---:|---|---:|
| 2026-03-24 | 1,272 | 1,272 | 0 | EURAUD_C / breakout_R_Rev_3_tp20.0_sl5.0 | 2 |
| 2026-03-26 | 535 | 535 | 0 | GBPAUD_C / breakout_2_tp20.0_sl5.0 | 2 |
| 2026-03-27 | 360 | 360 | 0 | GBPAUD_C / breakout_2_tp20.0_sl20.0 | 1 |
| 2026-03-29 | 10 | 10 | 0 | GBPNZD_C / breakout_2_tp3.0_sl20.0 | 1 |
| 2026-03-30 | 520 | 520 | 0 | EURAUD_C / breakout_R_2_tp20.0_sl20.0 | 2 |
| 2026-03-31 | 1,370 | 1,420 | 1 | GBPNZD_C / breakout_R_2_tp50.0_sl10.0 | 2 |
| 2026-04-01 | 880 | 880 | 0 | GBPAUD_C / breakout_R_2_tp10.0_sl20.0 | 2 |
| 2026-04-02 | 1,100 | 1,100 | 0 | EURNZD_C / breakout_R_2_tp30.0_sl50.0 | 2 |
| 2026-04-03 | 560 | 560 | 0 | GBPNZD_C / breakout_R_2_tp30.0_sl10.0 | 2 |
| 2026-04-05 | 280 | 280 | 0 | EURNZD_C / breakout_R_2_tp30.0_sl10.0 | 1 |
| 2026-04-06 | 470 | 520 | 1 | GBPAUD_C / breakout_2_tp20.0_sl10.0 | 2 |
| 2026-04-07 | 770 | 820 | 1 | GBPAUD_C / breakout_R_2_tp30.0_sl10.0 | 2 |
| 2026-04-08 | 1,260 | 1,260 | 0 | GBPAUD_C / breakout_R_2_tp20.0_sl10.0 | 2 |
| 2026-04-09 | 1,255 | 1,255 | 0 | GBPAUD_C / breakout_R_2_tp20.0_sl20.0 | 1 |
| 2026-04-17 | 453,730 | 453,730 | 0 | GBPEUR_C / breakout_R_2_tp10.0_sl20.0_12141c72 | 2 |

### First open at/after 03:00

| Date | Net after cost | Gross final net | Switches | Final held | Snapshots |
|---|---:|---:|---:|---|---:|
| 2026-03-24 | 1,272 | 1,272 | 0 | EURAUD_C / breakout_R_Rev_3_tp20.0_sl5.0 | 2 |
| 2026-03-26 | 535 | 535 | 0 | GBPAUD_C / breakout_2_tp20.0_sl5.0 | 2 |
| 2026-03-27 | 360 | 360 | 0 | GBPAUD_C / breakout_2_tp20.0_sl20.0 | 1 |
| 2026-03-29 | 10 | 10 | 0 | GBPNZD_C / breakout_2_tp3.0_sl20.0 | 1 |
| 2026-03-30 | 520 | 520 | 0 | EURAUD_C / breakout_R_2_tp20.0_sl20.0 | 2 |
| 2026-03-31 | 1,370 | 1,420 | 1 | GBPNZD_C / breakout_R_2_tp50.0_sl10.0 | 2 |
| 2026-04-01 | 880 | 880 | 0 | GBPAUD_C / breakout_R_2_tp10.0_sl20.0 | 2 |
| 2026-04-02 | 1,100 | 1,100 | 0 | EURNZD_C / breakout_R_2_tp30.0_sl50.0 | 2 |
| 2026-04-03 | 560 | 560 | 0 | GBPNZD_C / breakout_R_2_tp30.0_sl10.0 | 2 |
| 2026-04-05 | 280 | 280 | 0 | EURNZD_C / breakout_R_2_tp30.0_sl10.0 | 1 |
| 2026-04-06 | 470 | 520 | 1 | GBPAUD_C / breakout_2_tp20.0_sl10.0 | 2 |
| 2026-04-07 | 770 | 820 | 1 | GBPAUD_C / breakout_R_2_tp30.0_sl10.0 | 2 |
| 2026-04-08 | 1,260 | 1,260 | 0 | GBPAUD_C / breakout_R_2_tp20.0_sl10.0 | 2 |
| 2026-04-09 | 1,255 | 1,255 | 0 | GBPAUD_C / breakout_R_2_tp20.0_sl20.0 | 1 |
| 2026-04-17 | 453,730 | 453,730 | 0 | GBPEUR_C / breakout_R_2_tp10.0_sl20.0_12141c72 | 2 |
