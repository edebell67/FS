# Task: Social Posting Package Top 5 Multi Product Types

## Source
- User Directive: 2026-03-26
- Content Source / Brand: `The Strategy Warehouse`

## Task Summary
Create a posting package that shows the top 5 strategies for each of these product types:
- forex
- indices
- metals
- energy

Capture it as a workflow that can be replayed daily.
Crypto is explicitly out of scope for this package.

## Context
- Existing single-product forex Twitter post task:
  - `C:\Users\edebe\eds\workstream\300_complete\20260326_125609_breakout_twitter_weekly_forex_top5_post.md`
- Current generator:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\social_content_generator.py`
- Weekly stats source pattern:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\{product_type}\stats\daily_net_return.json`

## Goal
Produce a reusable posting package for social content that can generate top 5 weekly strategy results for:
- forex
- indices
- metals
- energy

Posts should present the results as originating from `The Strategy Warehouse`.
The workflow should be structured so the same steps can be rerun daily with the latest available stats.
Any reusable implementation artifacts should be placed under the `tools` folder in an appropriately named subfolder.

## Plan
- [x] 1. Verify weekly stats availability and structure for each target product type.
- [x] 2. Define a replayable daily workflow for package generation, review, and posting.
- [x] 3. Define the posting package format and outputs for multi-product publishing.
- [x] 4. Implement a reusable tool-based package generator under `tools`.
- [x] 5. Validate generated output for each target product type.

## Validation
- Confirmed weekly stats exist for:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\daily_net_return.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\indices\stats\daily_net_return.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\metals\stats\daily_net_return.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\energy\stats\daily_net_return.json`
- Command:
  - `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
- Result:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-03-26\top5_weekly_posting_package.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-03-26\top5_weekly_posting_package.md`
- Verified package contents for `forex`, `indices`, `metals`, and `energy`, each with top 5 strategies and a Twitter draft.

## Implementation Log
- **2026-03-26 12:58**: Task moved to in progress.
- **2026-03-26 13:03**: Added reusable generator script under `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`.
- **2026-03-26 13:03**: Added workflow documentation at `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\README.md`.
- **2026-03-26 13:03**: Generated first dated package under `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-03-26`.

## Notes
- Keep product-type-specific ranking logic aligned to the weekly performance stats.
- Reuse the existing forex weekly top 5 posting path where possible.
- Use `The Strategy Warehouse` consistently in copy and package framing.
- The output should support a repeatable operator workflow rather than a one-off manual post.
- Put reusable scripts/templates/helpers in `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\{appropriate_subfolder}` rather than scattering them in the root.
- This package is required for the other product types as well, but excludes `crypto`.

## Changes Made
- Added `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
- Added `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\README.md`
- Generated:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-03-26\top5_weekly_posting_package.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-03-26\top5_weekly_posting_package.md`

## Completion Status
**Complete** - 2026-03-26 13:03
