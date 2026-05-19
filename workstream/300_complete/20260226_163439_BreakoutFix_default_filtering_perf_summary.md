# Task: Fix Default Strategy Filtering in Performance Summary

- **Source**: User request
- **Task Summary**: Fix the issue where strategies are pre-filtered to show only 'Rev Scalper' on entry to the Strategy Performance screen. The filter should only apply when explicitly selected by the user, defaulting to showing ALL strategies.
- **Context**: 
  - On navigating to `strategy_performance.html`, the "Rev Scalper" checkbox appears to be pre-checked or the filter is applied automatically.
  - The expected behavior is that both "Scalper Only" and "Rev Scalper" are unchecked initially, allowing all strategies to populate the hierarchy table and leaderboard.
- **Implementation Plan**:
  - [x] **Check HTML Initialization**: Inspect `TradeApps/breakout/fs/strategy_performance.html` to see if the "Rev Scalper" checkbox has an unintended `checked` attribute by default.
  - [x] **Check JavaScript Initialization**: Look for any JS restoring state from `localStorage` or initializing the `revScalperOnlyCheckbox` to true on page load.
  - [x] **Fix Filtering Logic**: Ensure that the initial filter state applies to "all strategies" and does not pre-filter into `Rev Scalper`.
- **Validation**:
  - [x] Load the `strategy_performance.html` screen fresh.
  - [x] Verify both filter checkboxes are unchecked by default.
  - [x] Verify that all strategies (standard, rev, etc.) are visible in the hierarchy immediately on load without user intervention.
- **Completion Status**: Complete. (Will move to `300_complete` folder)
