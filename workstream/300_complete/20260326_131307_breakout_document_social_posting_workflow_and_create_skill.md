# Task: Document Social Posting Workflow And Create Skill

## Source
- User Directive: 2026-03-26

## Task Summary
Fully document the reusable The Strategy Warehouse social posting workflow and create a skill that other models can use to run the process.

## Context
- Existing workflow tool:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
- Existing workflow doc:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\README.md`
- Existing generated package example:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-03-26\top5_weekly_posting_package.md`

## Goal
- Produce complete workflow documentation for daily replay.
- Create a reusable skill that other models can trigger to run the workflow correctly.

## Plan
- [x] 1. Expand the workflow documentation with prerequisites, steps, outputs, and validation.
- [x] 2. Create a skill folder with a focused `SKILL.md`.
- [x] 3. Reference the reusable generator and workflow artifacts from the skill.
- [x] 4. Validate that the documented commands and outputs match the live repo.

## Validation
- Verified workflow doc:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\README.md`
- Verified skill files:
  - `C:\Users\edebe\eds\skills\strategy-warehouse-social-posting\SKILL.md`
  - `C:\Users\edebe\eds\skills\strategy-warehouse-social-posting\agents\openai.yaml`
- Validation command:
  - `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
- Validation result:
  - dated JSON and Markdown outputs regenerated successfully under `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-03-26`

## Implementation Log
- **2026-03-26 13:13**: Task created.
- **2026-03-26 13:16**: Expanded the workflow documentation to include purpose, prerequisites, review checklist, validation, and troubleshooting.
- **2026-03-26 13:17**: Created workspace skill package under `C:\Users\edebe\eds\skills\strategy-warehouse-social-posting`.
- **2026-03-26 13:18**: Re-ran the generator to confirm the documented workflow still produces the dated package outputs.

## Changes Made
- Updated:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\README.md`
- Added:
  - `C:\Users\edebe\eds\skills\strategy-warehouse-social-posting\SKILL.md`
  - `C:\Users\edebe\eds\skills\strategy-warehouse-social-posting\agents\openai.yaml`

## Completion Status
**Complete** - 2026-03-26 13:18
