# Task: Core Engine - Promotion Logic

## Status
TODO

## Source Document
`000_backlog/20260222_205900_pipHunter_signal_marketplace_mobile_functionality_v2 (3).md` - Section 1.5

## Description
Implement the Promotion Logic that determines which strategy is eligible for live recommendation. Only Rank 1 (leader) is eligible, and must be: formulated, positive P&L, and above leadership gap. If no positive leader exists, no trade is promoted.

## Objective
Create a promotion eligibility engine that enforces all qualification criteria and handles "no trade" scenarios gracefully.

## Sub-tasks
- [ ] Implement `get_promotable_strategy(bucket_id)` function
- [ ] Add promotion eligibility checks:
  - [ ] Must be Rank 1 in bucket
  - [ ] Must be formulated (min trade count met)
  - [ ] Must have positive daily P&L
  - [ ] Must meet minimum leadership gap
- [ ] Create `bucket_promotions` table (bucket_id, strategy_id, promoted_at, demoted_at)
- [ ] Implement "No Trade" state when no eligible leader
- [ ] Create `/api/v1/buckets/{id}/promoted` endpoint
- [ ] Add promotion change event logging
- [ ] Implement promotion history tracking
- [ ] Create promotion eligibility explanation response (why/why not promoted)

## Verification Test
1. Rank 1 strategy meeting all criteria - returns as promoted
2. Rank 1 with negative P&L - returns "No Trade" state
3. Rank 1 unformulated - returns "No Trade" state
4. Rank 1 below leadership gap - returns "No Trade" state
5. Verify promotion history is logged with timestamps

## Completion Date
(To be filled on completion)
