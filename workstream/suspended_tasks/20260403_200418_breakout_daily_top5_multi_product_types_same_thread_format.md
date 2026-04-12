## Objective

Deliver daily top-5 results in the exact same compact Twitter/X thread format currently used for the weekly multi-product posts, but with daily data for the specific source date.

## Task Attributes

- project: breakout
- task_type: implementation
- area: social_publisher
- priority: high
- status: todo
- workflow_ready: true

## Requirements

- Use the same compact line format already used for the weekly multi-product thread, for example:
  - `Forex | Mar 19-Mar 26 | 1. EURAUD ... | Single-contract basis. #Forex #SystemTrading`
- Produce the same style for daily results
- Daily scope should be for the exact source date, for example:
  - `Forex | 2026-04-03 | 1. ...`
- Cover the same in-scope product types:
  - forex
  - indices
  - metals
  - energy
- Use source-derived daily data only
- Do not fabricate date ranges, labels, totals, or post text
- Preserve posting-appropriate character limits where possible

## Goal

Create a repeatable daily preparation path that yields:
- lead text if needed
- one compact daily line per product type
- validated ready-to-post copy in the same established format family as the weekly thread

## Plan

1. Identify the source artifacts for daily per-product-type top-5 results.
2. Map the weekly compact format into an equivalent daily format.
3. Implement generation of the daily compact posts.
4. Validate the output for a live date such as `2026-04-03`.
5. Record exact generated lines and character counts.

## Validation

- Output exists for each of the four product types
- Each line uses the same compact posting style as the weekly version
- The date label is daily-specific rather than a week range
- The results are derived from the daily source artifacts for the given date

## Notes

- This task is about daily format parity with the previously validated weekly thread style.
- The existing weekly preparation reference is:
  - `C:\Users\edebe\eds\workstream\300_complete\20260326_174209_breakout_twitter_post_preparation_top5_multi_product_types.md`

## Outcome

Pending.
