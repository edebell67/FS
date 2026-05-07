# Rank-1 First-Open Time Grid Search

- Product type: `forex`
- Test window: `2026-03-21` to `2026-04-17`
- Rule: first positive rank-1 opens at/after cutoff; later switches require rank-1 change and net gap threshold.
- Switch cost: `$50` per switch

## Best By First-Open Cutoff

| First open cutoff | Best rule | Total net | Avg/day | Switches | Days |
|---|---:|---:|---:|---:|---:|
| 01:00 | rank-1 + net>25 | 18,935 | 728 | 20 | 26 |
| 02:00 | rank-1 + net>25 | 19,140 | 736 | 16 | 26 |
| 03:00 | rank-1 + net>25 | 19,525 | 751 | 15 | 26 |

## Full Results

### First open at/after 01:00

| Rule | Total net | Avg/day | Switches | Opened days | Skipped days |
|---|---:|---:|---:|---:|---:|
| Always rank-1 | 18,160 | 698 | 32 | 25 | 1 |
| rank-1 + net>0 | 18,160 | 698 | 32 | 25 | 1 |
| rank-1 + net>25 | 18,935 | 728 | 20 | 25 | 1 |
| rank-1 + net>50 | 18,350 | 706 | 13 | 25 | 1 |
| rank-1 + net>75 | 18,915 | 727 | 12 | 25 | 1 |
| rank-1 + net>100 | 18,775 | 722 | 10 | 25 | 1 |
| rank-1 + net>150 | 18,655 | 717 | 8 | 25 | 1 |
| rank-1 + net>200 | 18,035 | 694 | 5 | 25 | 1 |
| rank-1 + net>300 | 14,675 | 564 | 1 | 25 | 1 |
| rank-1 + net>500 | 14,675 | 564 | 1 | 25 | 1 |

### First open at/after 02:00

| Rule | Total net | Avg/day | Switches | Opened days | Skipped days |
|---|---:|---:|---:|---:|---:|
| Always rank-1 | 18,560 | 714 | 24 | 25 | 1 |
| rank-1 + net>0 | 18,560 | 714 | 24 | 25 | 1 |
| rank-1 + net>25 | 19,140 | 736 | 16 | 25 | 1 |
| rank-1 + net>50 | 18,170 | 699 | 10 | 25 | 1 |
| rank-1 + net>75 | 18,000 | 692 | 7 | 25 | 1 |
| rank-1 + net>100 | 17,860 | 687 | 5 | 25 | 1 |
| rank-1 + net>150 | 17,810 | 685 | 4 | 25 | 1 |
| rank-1 + net>200 | 17,780 | 684 | 2 | 25 | 1 |
| rank-1 + net>300 | 14,985 | 576 | 0 | 25 | 1 |
| rank-1 + net>500 | 14,985 | 576 | 0 | 25 | 1 |

### First open at/after 03:00

| Rule | Total net | Avg/day | Switches | Opened days | Skipped days |
|---|---:|---:|---:|---:|---:|
| Always rank-1 | 18,995 | 731 | 22 | 25 | 1 |
| rank-1 + net>0 | 18,995 | 731 | 22 | 25 | 1 |
| rank-1 + net>25 | 19,525 | 751 | 15 | 25 | 1 |
| rank-1 + net>50 | 18,555 | 714 | 9 | 25 | 1 |
| rank-1 + net>75 | 18,495 | 711 | 7 | 25 | 1 |
| rank-1 + net>100 | 18,265 | 702 | 4 | 25 | 1 |
| rank-1 + net>150 | 18,215 | 701 | 3 | 25 | 1 |
| rank-1 + net>200 | 18,185 | 699 | 1 | 25 | 1 |
| rank-1 + net>300 | 18,185 | 699 | 1 | 25 | 1 |
| rank-1 + net>500 | 15,795 | 607 | 0 | 25 | 1 |
