Source: User request

Task Summary: Add pick_now threshold settings to trade_viewer.html config UI.

Context:
- Project: TradeApps/breakout
- File to Modify: `TradeApps/breakout/fs/trade_viewer.html`
- Config Fields: `pick_now.min_appearances`, `pick_now.min_net_trend`, `pick_now.min_snapshots`

Priority: 1

**Suggested Agent:** claude

## Objective

Add the pick_now configuration fields to the config UI modal in trade_viewer.html so users can tune strategy selection thresholds without editing config.json manually.

## Fields to Add

| Field | Key | Type | Default | Description |
|-------|-----|------|---------|-------------|
| Min Appearances | `pick_now.min_appearances` | number | 20 | Minimum times in top10 |
| Min Net Trend | `pick_now.min_net_trend` | number | 100 | Minimum net trend value |
| Min Snapshots | `pick_now.min_snapshots` | number | 60 | Minimum total snapshots |

## Plan

- [ ] 1. Find config UI section in trade_viewer.html
  - [ ] Locate `renderConfigForm()` or similar function
  - [ ] Identify where to add new section
  - [ ] Evidence: pending

- [ ] 2. Add "Strategy Picker" section
  - [ ] Add section header
  - [ ] Add 3 number input fields
  - [ ] Wire up to config save/load
  - [ ] Evidence: pending

- [ ] 3. Test UI
  - [ ] Verify fields appear in config modal
  - [ ] Verify values save to config.json
  - [ ] Verify values load on page refresh
  - [ ] Evidence: pending

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: false
- Evidence-Type: ui_screenshot
  - Artifact: `TradeApps/breakout/fs/trade_viewer.html`
  - Objective-Proved: Pick now thresholds editable in config UI
  - Status: planned

## Implementation Log
- 2026-03-24 19:39: Task created

Completion Status: Backlog

## Changes Made

Added new section to `trade_viewer.html` config UI (lines 3220-3227):

```javascript
{
    title: '📊 Strategy Picker (Pick Now)',
    fields: [
        { label: 'Min Appearances', key: 'pick_now.min_appearances', type: 'number' },
        { label: 'Min Net Trend', key: 'pick_now.min_net_trend', type: 'number' },
        { label: 'Min Snapshots', key: 'pick_now.min_snapshots', type: 'number' }
    ]
}
```

## Evidence
Objective-Delivery-Coverage: 100%
- Evidence-Type: code_change
  - Status: complete

## Implementation Log
- 2026-03-24 19:39: Task created
- 2026-03-24 19:40: Implemented - added Strategy Picker section to config UI

Completion Status: Complete
