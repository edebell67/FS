---
Task Type: standard
Task Summary: Fix week scroll date off-by-one in weekly_performance.html
Dependency: None
Destination Folder: TradeApps/breakout/fs/
---

## Context

`changeWeek()` used `new Date('YYYY-MM-DD')` which parses the date string as UTC midnight. Calling `.toISOString()` on this in a UTC-offset timezone (e.g. BST = UTC+1) returns the previous day's date, causing the week navigation to jump to the wrong week. Same issue affected the initial `currentTargetDate` initialisation.

## Changes Made

**`TradeApps/breakout/fs/weekly_performance.html`**

1. `currentTargetDate` initialisation (line 674): replaced `new Date().toISOString().split('T')[0]` with local-date construction using `getFullYear/getMonth/getDate`.

2. `changeWeek(dir)` function: replaced `new Date(dateString)` + `.toISOString()` with explicit year/month/day split → `new Date(y, m-1, d)` → local date formatting, avoiding UTC interpretation entirely.

Before:
```javascript
let currentTargetDate = new Date().toISOString().split('T')[0];

function changeWeek(dir) {
    const d = new Date(currentData?.week_start || currentTargetDate);
    d.setDate(d.getDate() + (dir * 7));
    currentTargetDate = d.toISOString().split('T')[0];
    storeWeeklyState();
    fetchData();
}
```

After:
```javascript
const _today = new Date(); const _pad = n => String(n).padStart(2, '0');
let currentTargetDate = `${_today.getFullYear()}-${_pad(_today.getMonth() + 1)}-${_pad(_today.getDate())}`;

function changeWeek(dir) {
    const base = currentData?.week_start || currentTargetDate;
    const [y, m, d] = base.split('-').map(Number);
    const date = new Date(y, m - 1, d);
    date.setDate(date.getDate() + (dir * 7));
    const pad = n => String(n).padStart(2, '0');
    currentTargetDate = `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
    storeWeeklyState();
    fetchData();
}
```

## Plan

- [x] 1. Fix `currentTargetDate` initialisation to use local date
  - Test: `new Date().toISOString()` in BST returns yesterday; local construction returns today
  - Evidence: edit applied

- [x] 2. Fix `changeWeek` to parse and format dates without UTC shift
  - Test: clicking prev/next week navigates exactly 7 days from the displayed week, no off-by-one
  - Evidence: edit applied

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: TradeApps/breakout/fs/weekly_performance.html
  - Objective-Proved: UTC parsing replaced with local-date construction in both locations
  - Status: captured

## Completion Status

COMPLETE — 2026-04-24
