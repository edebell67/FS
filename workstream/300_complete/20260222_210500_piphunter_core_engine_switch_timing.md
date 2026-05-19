# Task: Core Engine - Switch Timing Handler

## Status
TODO

## Source Document
`000_backlog/20260222_205900_pipHunter_signal_marketplace_mobile_functionality_v2 (3).md` - Section 1.6

## Description
Implement the Switch Timing system that recalculates leadership continuously and triggers promotion switches at the next signal cycle.

## Objective
Create a real-time leadership monitoring system that triggers smooth promotion transitions at appropriate signal cycle boundaries.

## Sub-tasks
- [ ] Define signal cycle interval (e.g., 1 minute, 5 minutes)
- [ ] Implement continuous leadership recalculation (background job)
- [ ] Create switch detection logic (leader changed since last cycle)
- [ ] Implement switch queue (pending switches to execute at next cycle)
- [ ] Create `/api/v1/buckets/{id}/next-switch` endpoint
- [ ] Add switch event notifications (WebSocket or push)
- [ ] Implement switch execution at cycle boundary
- [ ] Log all switches with before/after state
- [ ] Add switch cooldown to prevent rapid flipping
- [ ] Create switch analytics (frequency, duration of leadership)

## Verification Test
1. Leadership change detected mid-cycle - queued for next cycle
2. At cycle boundary - switch executes and new leader promoted
3. Verify switch is logged with timestamp and previous leader
4. WebSocket/push notification sent on switch
5. Switch cooldown prevents immediate re-switch

## Completion Date
(To be filled on completion)
