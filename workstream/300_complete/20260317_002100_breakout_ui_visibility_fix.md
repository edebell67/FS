# Task: UI Visibility Fix - Product Type Selection
**Project**: Breakout Trade Viewer
**Version**: V20260317_0025
**Status**: Completed
**Started**: 2026-03-17 00:21
**Completed**: 2026-03-17 00:26

## Summary
Fix unreadable product type selection list in `strategy_performance.html`.

## Detailed Log
- [2026-03-17 00:25] Created plan and task file.
- [2026-03-17 00:25] Investigated `strategy_performance.html` styles. Found that `select option` lacks consistent dark-theme styling, making options potentially invisible on some browsers. Also found undefined CSS variables in date range controls.
- [2026-03-17 00:26] Implemented global `select option` styling and fixed date range control inline styles. Updated version to V20260317_0025.

## To-Do
- [x] Update CSS in `strategy_performance.html` for `select` and `option`.
- [x] Fix inline styles for date range controls.
- [x] Update `VERSION` in `constants.py`.
- [x] Verify changes.
- [x] Move task to `300_complete`.
