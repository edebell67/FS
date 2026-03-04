# Task: Define Revision Scalper (rev_scalper) Config

## Status
TODO

## Source
- User request: "i want to define a new group rev_scalper where this relationship is reversed.. i.e. TP>SL... add rev_scalper ratio to config (similar to above)..."
- Prerequisite: Task 1 (Identify Scalper TP/SL Relationship)

## Task Summary
Define a new strategy grouping called `rev_scalper` where the Take Profit (TP) is strictly greater than the Stop Loss (SL). Add the corresponding `rev_scalper` ratio or threshold to the system configuration file so it can be used dynamically.

## Context
- Project: Breakout
- Target Files: `config.json` (or relevant config file), and any backend/frontend code parsing strategy groups.

## Implementation Log
- 2026-02-25 14:57: Task created.

## Changes Made
- Pending

## Validation
- Verify the new config value is loaded and accessible by the frontend/backend.

## Risks/Notes
- Make sure the logic correctly separates standard scalpers (TP < SL or similar) from rev_scalpers (TP > SL).

## Completion Status
Pending.
