# Task: Modify Multi-Chart Green Dot Logic
        
## Status: TODO
        
## Objective:
Refine the "Leadership Change" green dot logic in `multi_chart.js` to:
- Show green dots whenever there are multiple charts on a card (including split Buy/Sell views).
- Correctly distinguish between Buy and Sell metrics of the same strategy.
- Exclude single-chart cards (leadership doesn't "change" if there's only one).
- Prevent green dots when a single chart is dominant without competition on the same card.

## Plan:
- [x] Update `leadershipChanges` calculation in `activationDotsPlugin` to use `dataset._key + '|' + metric` for unique tracking.
- [x] Verify `allDatasets.length > 1` condition.
- [x] Update `Constants.py` version.
- [x] Update `multi_chart.html` script version.

## Log:
- 20260323 16:50: Created task.
- 20260323 17:00: Implemented composite key for leadership tracking. Verified split-chart support. Updated system versions.
