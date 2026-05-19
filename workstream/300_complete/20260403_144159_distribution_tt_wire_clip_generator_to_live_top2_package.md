## Objective

Extend the `distribution_TT` clip generator so it can consume the live breakout `top2_cross_product_post.json` package directly and derive the clip payload automatically from source data.

## Task Attributes

- project: distribution_tt
- task_type: implementation
- area: media_generation
- priority: high
- status: todo

## Plan

1. Add support for breakout top-2 package JSON input.
2. Derive leader, challenger, and gap directly from `today_product_leaders`.
3. Emit a resolved clip-input JSON artifact for auditability.
4. Validate the generator using the live `2026-04-03` package.

## Outcome

Completed successfully.

## Progress Log

- 2026-04-03 14:42:10 Extended `top2_vertical_clip.py` with `--top2-package-json` support.
- 2026-04-03 14:43:05 Added direct breakout package usage examples to `distribution_TT\README.md`.
- 2026-04-03 14:44:27 Ran the generator against `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-03\top2_cross_product_post.json` in frame-only mode.
- 2026-04-03 14:45:12 Verified `resolved_clip_input.json` and the generated frames under `distribution_TT\output\live_2026_04_03`.

## Changes Made

- `C:\Users\edebe\eds\distribution_TT\top2_vertical_clip.py`
  - Added mutually exclusive source modes:
    - `--input` for direct clip JSON
    - `--top2-package-json` for breakout package JSON
  - Added package-to-clip derivation from `today_product_leaders`
  - Added `resolved_clip_input.json` output for auditability
- `C:\Users\edebe\eds\distribution_TT\README.md`
  - Added package-mode usage example
  - Documented the resolved audit artifact

## Validation

Command run:

```powershell
python C:\Users\edebe\eds\distribution_TT\top2_vertical_clip.py --top2-package-json C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-03\top2_cross_product_post.json --output-dir C:\Users\edebe\eds\distribution_TT\output\live_2026_04_03 --frames-only
```

Result:
- Success
- Output:
  - `frames_dir=C:\Users\edebe\eds\distribution_TT\output\live_2026_04_03\frames`
  - `resolved_input=C:\Users\edebe\eds\distribution_TT\output\live_2026_04_03\resolved_clip_input.json`

Resolved source-derived clip input:
- leader: `NQ`
- leader_pnl: `1460.0`
- challenger: `ES`
- challenger_pnl: `740.0`
- gap: `720.0`
- state: `live`

Generated artifacts:
- `C:\Users\edebe\eds\distribution_TT\output\live_2026_04_03\resolved_clip_input.json`
- `C:\Users\edebe\eds\distribution_TT\output\live_2026_04_03\frames\f1.png`
- `C:\Users\edebe\eds\distribution_TT\output\live_2026_04_03\frames\f2.png`
- `C:\Users\edebe\eds\distribution_TT\output\live_2026_04_03\frames\f3.png`
- `C:\Users\edebe\eds\distribution_TT\output\live_2026_04_03\frames\f4.png`
