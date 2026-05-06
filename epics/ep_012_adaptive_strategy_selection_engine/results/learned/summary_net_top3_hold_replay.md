# Forex Summary Net Top-3 Hold Replay

- Source: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex`
- Source files discovered: `158`
- Loaded ranked snapshots: `127`
- Unreadable/empty/schema-missing files skipped: `0`
- Product filter: `forex regex only ([A-Z]{6}_C)`
- Non-forex products found in source: `AUD, BTC, BZ, CAD, CHF, CL, ES, ETH, EUR, GBP, GBPEUR_S, GC, HG, NG, NQ, NZD, RTY, SI, SOL, XRP, YM, ZN, ZT`
- Rule: open current #1 at/after cutoff; keep holding while held product/strategy remains in current top 3; replace with current #1 when held drops out of top 3.
- Ranking: latest `net` per product/strategy at snapshot `last_update`, sorted by net descending, then product, then strategy.
- Scoring: final held strategy net at final snapshot of day minus `$50` per replacement switch.

## Summary

| First open cutoff | Total net | Avg/day | Opened days | Switches | Days |
|---:|---:|---:|---:|---:|---:|
| 00:00 | 474,170 | 14,818 | 32 | 56 | 32 |
| 01:00 | 474,320 | 14,822 | 32 | 53 | 32 |
| 02:00 | 474,470 | 14,827 | 32 | 50 | 32 |
| 03:00 | 474,470 | 14,827 | 32 | 50 | 32 |

## Switch Event Sample

| Date | Time | Event | From | From rank | From net | To | To net |
|---|---|---|---|---:|---:|---|---:|
| 2026-03-16 | 04:19:28 | open |  |  |  | GBPAUD_C / breakout_R_Rev_4_tp10.0_sl20.0 | 185.0 |
| 2026-03-16 | 06:28:27 | replace | GBPAUD_C / breakout_R_Rev_4_tp10.0_sl20.0 | 103 | 180.0 | GBPNZD_C / breakout_4_tp10.0_sl5.0 | 347.5 |
| 2026-03-16 | 07:35:39 | replace | GBPNZD_C / breakout_4_tp10.0_sl5.0 | 197 | 140.0 | GBPAUD_C / breakout_R_Rev_4_tp20.0_sl20.0 | 497.5 |
| 2026-03-16 | 08:22:48 | replace | GBPAUD_C / breakout_R_Rev_4_tp20.0_sl20.0 | 141 | 235.0 | NZDAUD_C / breakout_R_4_tp20.0_sl20.0 | 597.5 |
| 2026-03-16 | 09:23:51 | replace | NZDAUD_C / breakout_R_4_tp20.0_sl20.0 | 15 | 760.0 | GBPEUR_C / breakout_R_3_tp10.0_sl20.0 | 917.5 |
| 2026-03-16 | 10:19:43 | replace | GBPEUR_C / breakout_R_3_tp10.0_sl20.0 | 4 | 917.5 | GBPEUR_C / breakout_3_tp20.0_sl20.0 | 935.0 |
| 2026-03-16 | 18:07:13 | replace | GBPEUR_C / breakout_3_tp20.0_sl20.0 | 6 | 1035.0 | GBPEUR_C / breakout_3_tp20.0_sl50.0 | 1392.5 |
| 2026-03-16 | 23:12:16 | replace | GBPEUR_C / breakout_3_tp20.0_sl50.0 | 5 | 1010.0 | NZDAUD_C / breakout_R_2_tp20.0_sl20.0 | 1290.0 |
| 2026-03-17 | 00:00:00 | open |  |  |  | NZDAUD_C / breakout_R_2_tp20.0_sl20.0 | 1290.0 |
| 2026-03-17 | 03:46:56 | replace | NZDAUD_C / breakout_R_2_tp20.0_sl20.0 | 557 | -20.0 | NZDAUD_C / breakout_R_Rev_3_tp20.0_sl20.0 | 547.5 |
| 2026-03-17 | 06:00:38 | replace | NZDAUD_C / breakout_R_Rev_3_tp20.0_sl20.0 | 28 | 577.5 | GBPAUD_C / breakout_R_Rev_4_tp20.0_sl30.0 | 977.5 |
| 2026-03-17 | 08:16:07 | replace | GBPAUD_C / breakout_R_Rev_4_tp20.0_sl30.0 | 10 | 810.0 | EURAUD_C / breakout_R_Rev_4_tp20.0_sl20.0 | 1280.0 |
| 2026-03-17 | 12:19:05 | replace | EURAUD_C / breakout_R_Rev_4_tp20.0_sl20.0 | 12 | 927.5 | NZDAUD_C / breakout_R_Rev_2_tp20.0_sl20.0 | 1180.0 |
| 2026-03-17 | 18:14:03 | replace | NZDAUD_C / breakout_R_Rev_2_tp20.0_sl20.0 | 912 | -285.0 | EURAUD_C / breakout_R_Rev_2_tp20.0_sl5.0 | 570.0 |
| 2026-03-18 | 05:20:39 | open |  |  |  | NZDAUD_C / breakout_R_Rev_2_tp20.0_sl20.0 | 412.5 |
| 2026-03-18 | 12:46:13 | replace | NZDAUD_C / breakout_R_Rev_2_tp20.0_sl20.0 | 960 | -330.0 | GBPAUD_C / breakout_2_tp10.0_sl5.0 | 365.0 |
| 2026-03-18 | 13:45:52 | replace | GBPAUD_C / breakout_2_tp10.0_sl5.0 | 18 | 300.0 | GBPEUR_C / breakout_4_tp20.0_sl50.0 | 760.0 |
| 2026-03-18 | 16:37:45 | replace | GBPEUR_C / breakout_4_tp20.0_sl50.0 | 7 | 830.0 | GBPEUR_C / breakout_R_Rev_2_tp20.0_sl5.0 | 1237.5 |
| 2026-03-19 | 00:00:01 | open |  |  |  | GBPEUR_C / breakout_R_Rev_2_tp20.0_sl5.0 | 1317.5 |
| 2026-03-19 | 02:47:23 | replace | GBPEUR_C / breakout_R_Rev_2_tp20.0_sl5.0 | 68 | 267.5 | GBPAUD_C / breakout_R_2_tp20.0_sl5.0 | 535.0 |
| 2026-03-19 | 09:23:14 | replace | GBPAUD_C / breakout_R_2_tp20.0_sl5.0 | 32 | 710.0 | GBPEUR_C / breakout_4_tp20.0_sl20.0 | 1140.0 |
| 2026-03-19 | 14:03:01 | replace | GBPEUR_C / breakout_4_tp20.0_sl20.0 | 18 | 930.0 | GBPEUR_C / breakout_4_tp20.0_sl30.0 | 1330.0 |
| 2026-03-20 | 00:00:04 | open |  |  |  | GBPEUR_C / breakout_4_tp20.0_sl30.0 | 1710.0 |
| 2026-03-20 | 06:06:59 | replace | GBPEUR_C / breakout_4_tp20.0_sl30.0 | 21 | 372.5 | GBPEUR_C / breakout_R_Rev_4_tp20.0_sl5.0 | 467.5 |
| 2026-03-20 | 08:52:58 | replace | GBPEUR_C / breakout_R_Rev_4_tp20.0_sl5.0 | 116 | 272.5 | GBPEUR_C / breakout_R_Rev_2_tp20.0_sl50.0 | 757.5 |
| 2026-03-20 | 13:28:29 | replace | GBPEUR_C / breakout_R_Rev_2_tp20.0_sl50.0 | 559 | -147.5 | GBPEUR_C / breakout_Rev_2_tp20.0_sl5.0 | 952.5 |
| 2026-03-23 | 03:04:06 | open |  |  |  | NZDAUD_C / breakout_2_tp10.0_sl20.0 | 257.5 |
| 2026-03-23 | 05:16:21 | replace | NZDAUD_C / breakout_2_tp10.0_sl20.0 | 170 | 82.5 | GBPEUR_C / breakout_R_Rev_4_tp20.0_sl20.0 | 430.0 |
| 2026-03-23 | 05:48:35 | replace | GBPEUR_C / breakout_R_Rev_4_tp20.0_sl20.0 | 7 | 357.5 | GBPAUD_C / breakout_2_tp5.0_sl20.0 | 520.0 |
| 2026-03-23 | 07:55:53 | replace | GBPAUD_C / breakout_2_tp5.0_sl20.0 | 12 | 560.0 | GBPEUR_C / breakout_R_Rev_4_tp20.0_sl20.0 | 622.5 |

## Per-Day Results

### First open at/after 00:00

| Date | Net after cost | Gross final net | Switches | Final held | Snapshots |
|---|---:|---:|---:|---|---:|
| 2026-03-16 | 940 | 1,290 | 7 | NZDAUD_C / breakout_R_2_tp20.0_sl20.0 | 10 |
| 2026-03-17 | 355 | 605 | 5 | EURAUD_C / breakout_R_Rev_2_tp20.0_sl5.0 | 7 |
| 2026-03-18 | 968 | 1,118 | 3 | GBPEUR_C / breakout_R_Rev_2_tp20.0_sl5.0 | 8 |
| 2026-03-19 | 1,560 | 1,710 | 3 | GBPEUR_C / breakout_4_tp20.0_sl30.0 | 6 |
| 2026-03-20 | 802 | 952 | 3 | GBPEUR_C / breakout_Rev_2_tp20.0_sl5.0 | 4 |
| 2026-03-23 | 820 | 1,120 | 6 | EURNZD_C / breakout_2_tp20.0_sl20.0 | 10 |
| 2026-03-24 | 1,072 | 1,272 | 4 | EURAUD_C / breakout_R_Rev_3_tp20.0_sl5.0 | 10 |
| 2026-03-25 | 722 | 922 | 4 | GBPNZD_C / breakout_Rev_4_tp20.0_sl20.0 | 7 |
| 2026-03-26 | 535 | 535 | 0 | GBPAUD_C / breakout_2_tp20.0_sl5.0 | 2 |
| 2026-03-27 | 360 | 360 | 0 | GBPAUD_C / breakout_2_tp20.0_sl20.0 | 1 |
| 2026-03-29 | 10 | 10 | 0 | GBPNZD_C / breakout_2_tp3.0_sl20.0 | 1 |
| 2026-03-30 | 520 | 520 | 0 | EURAUD_C / breakout_R_2_tp20.0_sl20.0 | 2 |
| 2026-03-31 | 1,320 | 1,420 | 2 | GBPNZD_C / breakout_R_2_tp50.0_sl10.0 | 3 |
| 2026-04-01 | 830 | 880 | 1 | GBPAUD_C / breakout_R_2_tp10.0_sl20.0 | 3 |
| 2026-04-02 | 1,050 | 1,100 | 1 | EURNZD_C / breakout_R_2_tp30.0_sl50.0 | 3 |
| 2026-04-03 | 560 | 560 | 0 | GBPNZD_C / breakout_R_2_tp30.0_sl10.0 | 2 |
| 2026-04-04 | -20 | -20 | 0 | EURNZD_C / breakout_R_2_tp20.0_sl10.0 | 1 |
| 2026-04-05 | 280 | 280 | 0 | EURNZD_C / breakout_R_2_tp30.0_sl10.0 | 1 |
| 2026-04-06 | 470 | 520 | 1 | GBPAUD_C / breakout_2_tp20.0_sl10.0 | 2 |
| 2026-04-07 | 770 | 820 | 1 | GBPAUD_C / breakout_R_2_tp30.0_sl10.0 | 2 |
| 2026-04-08 | 1,260 | 1,260 | 0 | GBPAUD_C / breakout_R_2_tp20.0_sl10.0 | 3 |
| 2026-04-09 | 1,255 | 1,255 | 0 | GBPAUD_C / breakout_R_2_tp20.0_sl20.0 | 1 |
| 2026-04-10 | 880 | 880 | 0 | GBPNZD_C / breakout_R_2_tp30.0_sl20.0 | 2 |
| 2026-04-12 | 205 | 205 | 0 | EURAUD_C / breakout_2_tp30.0_sl20.0 | 1 |
| 2026-04-13 | 560 | 560 | 0 | EURAUD_C / breakout_R_2_tp30.0_sl50.0 | 2 |
| 2026-04-14 | 1,085 | 1,085 | 0 | GBPNZD_C / breakout_2_tp20.0_sl20.0 | 4 |
| 2026-04-15 | 470 | 620 | 3 | GBPNZD_C / breakout_R_2_tp20.0_sl20.0 | 5 |
| 2026-04-16 | 350 | 500 | 3 | GBPAUD_C / breakout_R_2_tp20.0_sl20.0 | 6 |
| 2026-04-17 | 453,630 | 453,730 | 2 | GBPEUR_C / breakout_R_2_tp10.0_sl20.0_12141c72 | 4 |
| 2026-04-19 | 180 | 180 | 0 | EURAUD_C / breakout_R_2_tp20.0_sl20.0 | 2 |
| 2026-04-20 | 160 | 360 | 4 | EURAUD_C / breakout_2_tp20.0_sl20.0 | 7 |
| 2026-04-21 | 210 | 360 | 3 | GBPEUR_C / breakout_2_tp20.0_sl20.0 | 5 |

### First open at/after 01:00

| Date | Net after cost | Gross final net | Switches | Final held | Snapshots |
|---|---:|---:|---:|---|---:|
| 2026-03-16 | 940 | 1,290 | 7 | NZDAUD_C / breakout_R_2_tp20.0_sl20.0 | 10 |
| 2026-03-17 | 405 | 605 | 4 | EURAUD_C / breakout_R_Rev_2_tp20.0_sl5.0 | 7 |
| 2026-03-18 | 968 | 1,118 | 3 | GBPEUR_C / breakout_R_Rev_2_tp20.0_sl5.0 | 8 |
| 2026-03-19 | 1,610 | 1,710 | 2 | GBPEUR_C / breakout_4_tp20.0_sl30.0 | 6 |
| 2026-03-20 | 852 | 952 | 2 | GBPEUR_C / breakout_Rev_2_tp20.0_sl5.0 | 4 |
| 2026-03-23 | 820 | 1,120 | 6 | EURNZD_C / breakout_2_tp20.0_sl20.0 | 10 |
| 2026-03-24 | 1,072 | 1,272 | 4 | EURAUD_C / breakout_R_Rev_3_tp20.0_sl5.0 | 10 |
| 2026-03-25 | 722 | 922 | 4 | GBPNZD_C / breakout_Rev_4_tp20.0_sl20.0 | 7 |
| 2026-03-26 | 535 | 535 | 0 | GBPAUD_C / breakout_2_tp20.0_sl5.0 | 2 |
| 2026-03-27 | 360 | 360 | 0 | GBPAUD_C / breakout_2_tp20.0_sl20.0 | 1 |
| 2026-03-29 | 10 | 10 | 0 | GBPNZD_C / breakout_2_tp3.0_sl20.0 | 1 |
| 2026-03-30 | 520 | 520 | 0 | EURAUD_C / breakout_R_2_tp20.0_sl20.0 | 2 |
| 2026-03-31 | 1,320 | 1,420 | 2 | GBPNZD_C / breakout_R_2_tp50.0_sl10.0 | 3 |
| 2026-04-01 | 830 | 880 | 1 | GBPAUD_C / breakout_R_2_tp10.0_sl20.0 | 3 |
| 2026-04-02 | 1,050 | 1,100 | 1 | EURNZD_C / breakout_R_2_tp30.0_sl50.0 | 3 |
| 2026-04-03 | 560 | 560 | 0 | GBPNZD_C / breakout_R_2_tp30.0_sl10.0 | 2 |
| 2026-04-04 | -20 | -20 | 0 | EURNZD_C / breakout_R_2_tp20.0_sl10.0 | 1 |
| 2026-04-05 | 280 | 280 | 0 | EURNZD_C / breakout_R_2_tp30.0_sl10.0 | 1 |
| 2026-04-06 | 470 | 520 | 1 | GBPAUD_C / breakout_2_tp20.0_sl10.0 | 2 |
| 2026-04-07 | 770 | 820 | 1 | GBPAUD_C / breakout_R_2_tp30.0_sl10.0 | 2 |
| 2026-04-08 | 1,260 | 1,260 | 0 | GBPAUD_C / breakout_R_2_tp20.0_sl10.0 | 3 |
| 2026-04-09 | 1,255 | 1,255 | 0 | GBPAUD_C / breakout_R_2_tp20.0_sl20.0 | 1 |
| 2026-04-10 | 880 | 880 | 0 | GBPNZD_C / breakout_R_2_tp30.0_sl20.0 | 2 |
| 2026-04-12 | 205 | 205 | 0 | EURAUD_C / breakout_2_tp30.0_sl20.0 | 1 |
| 2026-04-13 | 560 | 560 | 0 | EURAUD_C / breakout_R_2_tp30.0_sl50.0 | 2 |
| 2026-04-14 | 1,085 | 1,085 | 0 | GBPNZD_C / breakout_2_tp20.0_sl20.0 | 4 |
| 2026-04-15 | 470 | 620 | 3 | GBPNZD_C / breakout_R_2_tp20.0_sl20.0 | 5 |
| 2026-04-16 | 350 | 500 | 3 | GBPAUD_C / breakout_R_2_tp20.0_sl20.0 | 6 |
| 2026-04-17 | 453,630 | 453,730 | 2 | GBPEUR_C / breakout_R_2_tp10.0_sl20.0_12141c72 | 4 |
| 2026-04-19 | 180 | 180 | 0 | EURAUD_C / breakout_R_2_tp20.0_sl20.0 | 2 |
| 2026-04-20 | 160 | 360 | 4 | EURAUD_C / breakout_2_tp20.0_sl20.0 | 7 |
| 2026-04-21 | 210 | 360 | 3 | GBPEUR_C / breakout_2_tp20.0_sl20.0 | 5 |

### First open at/after 02:00

| Date | Net after cost | Gross final net | Switches | Final held | Snapshots |
|---|---:|---:|---:|---|---:|
| 2026-03-16 | 940 | 1,290 | 7 | NZDAUD_C / breakout_R_2_tp20.0_sl20.0 | 10 |
| 2026-03-17 | 405 | 605 | 4 | EURAUD_C / breakout_R_Rev_2_tp20.0_sl5.0 | 7 |
| 2026-03-18 | 968 | 1,118 | 3 | GBPEUR_C / breakout_R_Rev_2_tp20.0_sl5.0 | 8 |
| 2026-03-19 | 1,610 | 1,710 | 2 | GBPEUR_C / breakout_4_tp20.0_sl30.0 | 6 |
| 2026-03-20 | 852 | 952 | 2 | GBPEUR_C / breakout_Rev_2_tp20.0_sl5.0 | 4 |
| 2026-03-23 | 820 | 1,120 | 6 | EURNZD_C / breakout_2_tp20.0_sl20.0 | 10 |
| 2026-03-24 | 1,072 | 1,272 | 4 | EURAUD_C / breakout_R_Rev_3_tp20.0_sl5.0 | 10 |
| 2026-03-25 | 822 | 922 | 2 | GBPNZD_C / breakout_Rev_4_tp20.0_sl20.0 | 7 |
| 2026-03-26 | 535 | 535 | 0 | GBPAUD_C / breakout_2_tp20.0_sl5.0 | 2 |
| 2026-03-27 | 360 | 360 | 0 | GBPAUD_C / breakout_2_tp20.0_sl20.0 | 1 |
| 2026-03-29 | 10 | 10 | 0 | GBPNZD_C / breakout_2_tp3.0_sl20.0 | 1 |
| 2026-03-30 | 520 | 520 | 0 | EURAUD_C / breakout_R_2_tp20.0_sl20.0 | 2 |
| 2026-03-31 | 1,320 | 1,420 | 2 | GBPNZD_C / breakout_R_2_tp50.0_sl10.0 | 3 |
| 2026-04-01 | 830 | 880 | 1 | GBPAUD_C / breakout_R_2_tp10.0_sl20.0 | 3 |
| 2026-04-02 | 1,050 | 1,100 | 1 | EURNZD_C / breakout_R_2_tp30.0_sl50.0 | 3 |
| 2026-04-03 | 560 | 560 | 0 | GBPNZD_C / breakout_R_2_tp30.0_sl10.0 | 2 |
| 2026-04-04 | -20 | -20 | 0 | EURNZD_C / breakout_R_2_tp20.0_sl10.0 | 1 |
| 2026-04-05 | 280 | 280 | 0 | EURNZD_C / breakout_R_2_tp30.0_sl10.0 | 1 |
| 2026-04-06 | 470 | 520 | 1 | GBPAUD_C / breakout_2_tp20.0_sl10.0 | 2 |
| 2026-04-07 | 770 | 820 | 1 | GBPAUD_C / breakout_R_2_tp30.0_sl10.0 | 2 |
| 2026-04-08 | 1,260 | 1,260 | 0 | GBPAUD_C / breakout_R_2_tp20.0_sl10.0 | 3 |
| 2026-04-09 | 1,255 | 1,255 | 0 | GBPAUD_C / breakout_R_2_tp20.0_sl20.0 | 1 |
| 2026-04-10 | 880 | 880 | 0 | GBPNZD_C / breakout_R_2_tp30.0_sl20.0 | 2 |
| 2026-04-12 | 205 | 205 | 0 | EURAUD_C / breakout_2_tp30.0_sl20.0 | 1 |
| 2026-04-13 | 560 | 560 | 0 | EURAUD_C / breakout_R_2_tp30.0_sl50.0 | 2 |
| 2026-04-14 | 1,085 | 1,085 | 0 | GBPNZD_C / breakout_2_tp20.0_sl20.0 | 4 |
| 2026-04-15 | 470 | 620 | 3 | GBPNZD_C / breakout_R_2_tp20.0_sl20.0 | 5 |
| 2026-04-16 | 350 | 500 | 3 | GBPAUD_C / breakout_R_2_tp20.0_sl20.0 | 6 |
| 2026-04-17 | 453,630 | 453,730 | 2 | GBPEUR_C / breakout_R_2_tp10.0_sl20.0_12141c72 | 4 |
| 2026-04-19 | 180 | 180 | 0 | EURAUD_C / breakout_R_2_tp20.0_sl20.0 | 2 |
| 2026-04-20 | 210 | 360 | 3 | EURAUD_C / breakout_2_tp20.0_sl20.0 | 7 |
| 2026-04-21 | 210 | 360 | 3 | GBPEUR_C / breakout_2_tp20.0_sl20.0 | 5 |

### First open at/after 03:00

| Date | Net after cost | Gross final net | Switches | Final held | Snapshots |
|---|---:|---:|---:|---|---:|
| 2026-03-16 | 940 | 1,290 | 7 | NZDAUD_C / breakout_R_2_tp20.0_sl20.0 | 10 |
| 2026-03-17 | 405 | 605 | 4 | EURAUD_C / breakout_R_Rev_2_tp20.0_sl5.0 | 7 |
| 2026-03-18 | 968 | 1,118 | 3 | GBPEUR_C / breakout_R_Rev_2_tp20.0_sl5.0 | 8 |
| 2026-03-19 | 1,610 | 1,710 | 2 | GBPEUR_C / breakout_4_tp20.0_sl30.0 | 6 |
| 2026-03-20 | 852 | 952 | 2 | GBPEUR_C / breakout_Rev_2_tp20.0_sl5.0 | 4 |
| 2026-03-23 | 820 | 1,120 | 6 | EURNZD_C / breakout_2_tp20.0_sl20.0 | 10 |
| 2026-03-24 | 1,072 | 1,272 | 4 | EURAUD_C / breakout_R_Rev_3_tp20.0_sl5.0 | 10 |
| 2026-03-25 | 822 | 922 | 2 | GBPNZD_C / breakout_Rev_4_tp20.0_sl20.0 | 7 |
| 2026-03-26 | 535 | 535 | 0 | GBPAUD_C / breakout_2_tp20.0_sl5.0 | 2 |
| 2026-03-27 | 360 | 360 | 0 | GBPAUD_C / breakout_2_tp20.0_sl20.0 | 1 |
| 2026-03-29 | 10 | 10 | 0 | GBPNZD_C / breakout_2_tp3.0_sl20.0 | 1 |
| 2026-03-30 | 520 | 520 | 0 | EURAUD_C / breakout_R_2_tp20.0_sl20.0 | 2 |
| 2026-03-31 | 1,320 | 1,420 | 2 | GBPNZD_C / breakout_R_2_tp50.0_sl10.0 | 3 |
| 2026-04-01 | 830 | 880 | 1 | GBPAUD_C / breakout_R_2_tp10.0_sl20.0 | 3 |
| 2026-04-02 | 1,050 | 1,100 | 1 | EURNZD_C / breakout_R_2_tp30.0_sl50.0 | 3 |
| 2026-04-03 | 560 | 560 | 0 | GBPNZD_C / breakout_R_2_tp30.0_sl10.0 | 2 |
| 2026-04-04 | -20 | -20 | 0 | EURNZD_C / breakout_R_2_tp20.0_sl10.0 | 1 |
| 2026-04-05 | 280 | 280 | 0 | EURNZD_C / breakout_R_2_tp30.0_sl10.0 | 1 |
| 2026-04-06 | 470 | 520 | 1 | GBPAUD_C / breakout_2_tp20.0_sl10.0 | 2 |
| 2026-04-07 | 770 | 820 | 1 | GBPAUD_C / breakout_R_2_tp30.0_sl10.0 | 2 |
| 2026-04-08 | 1,260 | 1,260 | 0 | GBPAUD_C / breakout_R_2_tp20.0_sl10.0 | 3 |
| 2026-04-09 | 1,255 | 1,255 | 0 | GBPAUD_C / breakout_R_2_tp20.0_sl20.0 | 1 |
| 2026-04-10 | 880 | 880 | 0 | GBPNZD_C / breakout_R_2_tp30.0_sl20.0 | 2 |
| 2026-04-12 | 205 | 205 | 0 | EURAUD_C / breakout_2_tp30.0_sl20.0 | 1 |
| 2026-04-13 | 560 | 560 | 0 | EURAUD_C / breakout_R_2_tp30.0_sl50.0 | 2 |
| 2026-04-14 | 1,085 | 1,085 | 0 | GBPNZD_C / breakout_2_tp20.0_sl20.0 | 4 |
| 2026-04-15 | 470 | 620 | 3 | GBPNZD_C / breakout_R_2_tp20.0_sl20.0 | 5 |
| 2026-04-16 | 350 | 500 | 3 | GBPAUD_C / breakout_R_2_tp20.0_sl20.0 | 6 |
| 2026-04-17 | 453,630 | 453,730 | 2 | GBPEUR_C / breakout_R_2_tp10.0_sl20.0_12141c72 | 4 |
| 2026-04-19 | 180 | 180 | 0 | EURAUD_C / breakout_R_2_tp20.0_sl20.0 | 2 |
| 2026-04-20 | 210 | 360 | 3 | EURAUD_C / breakout_2_tp20.0_sl20.0 | 7 |
| 2026-04-21 | 210 | 360 | 3 | GBPEUR_C / breakout_2_tp20.0_sl20.0 | 5 |
