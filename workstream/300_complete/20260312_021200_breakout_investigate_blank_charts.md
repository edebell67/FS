# Task: Investigate Blank Cards in Multi-Chart P&L Grid
**Date**: 2026-03-12
**Status**: In Progress

## 1. Problem Description
The Multi-Chart P&L Grid (multi_chart.html) is displaying blank cards for the trade date 2026-03-12 in Live mode, despite the page loading the grid structure.

## 2. Initial Observations
- Dashboard version: V20260311_1345.
- Simulation clock is at 00:00:00.
- `_top_one.json` for 2026-03-12 is open in the editor.

## 3. Investigation Steps
- [x] Check content of `fs/json/live/2026-03-12/_top_one.json`.
- [x] Check content of `fs/json/live/2026-03-12/_summary_net.json`.
- [ ] Fix JS SyntaxError: Failed to execute 'querySelector' on 'Element' due to unsanitized groupName in IDs.
- [ ] Investigate 500 errors on `/api/system_health` and `/api/bias_history`.
- [ ] Verify `trade_viewer_api.py` internal logic for health checks.

## 4. Log
- 2026-03-12 02:12:00: Task started. Created workstream file.
- 2026-03-12 02:18:00: Browser subagent reported 500 errors on health/bias APIs and JS TypeError in `autoActivateStrategy`. 
- 2026-03-12 02:19:00: Identified `SyntaxError` in `multi_chart.js` caused by pipes and spaces in chart IDs used in `querySelector`.
