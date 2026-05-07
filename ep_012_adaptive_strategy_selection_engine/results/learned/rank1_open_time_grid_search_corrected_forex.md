# Rank-1 First-Open Time Grid Search

- Product type: `forex`
- Test window: `2026-03-21` to `2026-04-17`
- Rule: first positive rank-1 opens at/after cutoff; later switches require rank-1 change and net gap threshold.
- Switch cost: `$50` per switch

## Best By First-Open Cutoff

| First open cutoff | Best rule | Total net | Avg/day | Switches | Days |
|---|---:|---:|---:|---:|---:|
| 00:00 | rank-1 + net>500 | 28,425 | 1,093 | 76 | 26 |
| 01:00 | rank-1 + net>300 | 28,875 | 1,111 | 67 | 26 |
| 02:00 | rank-1 + net>300 | 28,925 | 1,112 | 66 | 26 |
| 03:00 | rank-1 + net>300 | 29,075 | 1,118 | 63 | 26 |

## Full Results

### First open at/after 00:00

| Rule | Total net | Avg/day | Switches | Opened days | Skipped days |
|---|---:|---:|---:|---:|---:|
| Always rank-1 | 26,130 | 1,005 | 128 | 25 | 1 |
| rank-1 + net>0 | 26,230 | 1,009 | 126 | 25 | 1 |
| rank-1 + net>25 | 27,180 | 1,045 | 107 | 25 | 1 |
| rank-1 + net>50 | 28,030 | 1,078 | 90 | 25 | 1 |
| rank-1 + net>75 | 28,040 | 1,078 | 89 | 25 | 1 |
| rank-1 + net>100 | 28,090 | 1,080 | 88 | 25 | 1 |
| rank-1 + net>150 | 27,995 | 1,077 | 87 | 25 | 1 |
| rank-1 + net>200 | 28,175 | 1,084 | 81 | 25 | 1 |
| rank-1 + net>300 | 28,275 | 1,087 | 79 | 25 | 1 |
| rank-1 + net>500 | 28,425 | 1,093 | 76 | 25 | 1 |

### First open at/after 01:00

| Rule | Total net | Avg/day | Switches | Opened days | Skipped days |
|---|---:|---:|---:|---:|---:|
| Always rank-1 | 26,980 | 1,038 | 111 | 25 | 1 |
| rank-1 + net>0 | 27,080 | 1,042 | 109 | 25 | 1 |
| rank-1 + net>25 | 27,980 | 1,076 | 91 | 25 | 1 |
| rank-1 + net>50 | 28,680 | 1,103 | 77 | 25 | 1 |
| rank-1 + net>75 | 28,690 | 1,103 | 76 | 25 | 1 |
| rank-1 + net>100 | 28,740 | 1,105 | 75 | 25 | 1 |
| rank-1 + net>150 | 28,645 | 1,102 | 74 | 25 | 1 |
| rank-1 + net>200 | 28,825 | 1,109 | 68 | 25 | 1 |
| rank-1 + net>300 | 28,875 | 1,111 | 67 | 25 | 1 |
| rank-1 + net>500 | 28,875 | 1,111 | 67 | 25 | 1 |

### First open at/after 02:00

| Rule | Total net | Avg/day | Switches | Opened days | Skipped days |
|---|---:|---:|---:|---:|---:|
| Always rank-1 | 27,380 | 1,053 | 103 | 25 | 1 |
| rank-1 + net>0 | 27,480 | 1,057 | 101 | 25 | 1 |
| rank-1 + net>25 | 28,180 | 1,084 | 87 | 25 | 1 |
| rank-1 + net>50 | 28,730 | 1,105 | 76 | 25 | 1 |
| rank-1 + net>75 | 28,740 | 1,105 | 75 | 25 | 1 |
| rank-1 + net>100 | 28,790 | 1,107 | 74 | 25 | 1 |
| rank-1 + net>150 | 28,695 | 1,104 | 73 | 25 | 1 |
| rank-1 + net>200 | 28,875 | 1,111 | 67 | 25 | 1 |
| rank-1 + net>300 | 28,925 | 1,112 | 66 | 25 | 1 |
| rank-1 + net>500 | 28,925 | 1,112 | 66 | 25 | 1 |

### First open at/after 03:00

| Rule | Total net | Avg/day | Switches | Opened days | Skipped days |
|---|---:|---:|---:|---:|---:|
| Always rank-1 | 27,530 | 1,059 | 100 | 25 | 1 |
| rank-1 + net>0 | 27,630 | 1,063 | 98 | 25 | 1 |
| rank-1 + net>25 | 28,330 | 1,090 | 84 | 25 | 1 |
| rank-1 + net>50 | 28,880 | 1,111 | 73 | 25 | 1 |
| rank-1 + net>75 | 28,890 | 1,111 | 72 | 25 | 1 |
| rank-1 + net>100 | 28,940 | 1,113 | 71 | 25 | 1 |
| rank-1 + net>150 | 28,845 | 1,109 | 70 | 25 | 1 |
| rank-1 + net>200 | 29,025 | 1,116 | 64 | 25 | 1 |
| rank-1 + net>300 | 29,075 | 1,118 | 63 | 25 | 1 |
| rank-1 + net>500 | 29,075 | 1,118 | 63 | 25 | 1 |
