## Objective

Build a full TikTok upload workflow under `C:\Users\edebe\eds\distribution_TT` that turns the live breakout top-2 package into a TikTok-ready video post, prepares caption text from the same source data, executes the upload path, and records proof of the final post outcome.

## Task Attributes

- project: distribution_tt
- task_type: implementation
- area: tiktok_distribution
- priority: high
- status: todo

## Requirements

- Use only source-derived values from the live breakout top-2 package
- Generate or reuse the vertical MP4 clip from `top2_cross_product_post.json`
- Produce TikTok caption text from the same resolved package input
- Support a concrete upload workflow:
  - either TikTok API if available
  - or browser automation if API access is not available
- Persist upload-ready artifacts locally:
  - MP4 path
  - caption text
  - resolved input payload
  - upload result metadata
- Record proof of outcome:
  - success with TikTok post URL or video identifier
  - or exact blocker with screenshots/log output
- Do not fabricate publish status, URLs, IDs, timestamps, or media metadata

## Desired Output

- Implementation in `C:\Users\edebe\eds\distribution_TT`
- A callable workflow entry point for:
  - preparing media
  - preparing caption
  - executing upload
  - writing a run artifact or report
- Documentation for runtime prerequisites:
  - TikTok login or API credentials
  - browser automation dependencies if used
  - output locations

## Plan

1. Inspect current `distribution_TT` clip-generation assets and choose the TikTok workflow structure.
2. Define the upload mode and required credentials or browser session assumptions.
3. Implement media-plus-caption preparation from the live top-2 package.
4. Implement TikTok upload execution with result capture.
5. Validate end to end with a real or dry-run upload path and record evidence.

## Validation

- The workflow can derive a TikTok-ready package from the live top-2 source data
- The workflow writes MP4, caption, and resolved-input artifacts
- The workflow executes a real upload or a clearly defined dry-run with concrete blockers
- The workflow records proof of result without inventing any external outcome

## Notes

- Prefer an auditable workflow with saved artifacts over a one-shot script
- If TikTok API access is unavailable, browser automation is acceptable but must capture the exact result
- Reuse the existing `distribution_TT` clip generator where possible rather than duplicating media logic

## Progress Log

- 2026-04-03 15:34:12 Inspected the existing `distribution_TT` clip generator and selected a run-folder based TikTok workflow design.
- 2026-04-03 15:37:05 Added `tiktok_workflow.py` to prepare MP4, caption, resolved input, manifest, and upload result artifacts.
- 2026-04-03 15:37:40 Added `run_tiktok_workflow_2026-04-03_example.ps1` and updated `README.md` with workflow usage.
- 2026-04-03 15:39:37 Validated the workflow end to end in `dry-run` mode against the live `2026-04-03` breakout top-2 package.

## Changes Made

- Added [tiktok_workflow.py](C:\Users\edebe\eds\distribution_TT\tiktok_workflow.py)
  - prepares a TikTok run folder from live `top2_cross_product_post.json`
  - generates MP4 via the existing clip generator
  - writes `caption.txt`
  - writes `resolved_clip_input.json`
  - writes `workflow_manifest.json`
  - writes `upload_result.json`
  - supports `--upload-mode dry-run`
  - supports `--upload-mode playwright`
- Added [run_tiktok_workflow_2026-04-03_example.ps1](C:\Users\edebe\eds\distribution_TT\run_tiktok_workflow_2026-04-03_example.ps1)
- Updated [README.md](C:\Users\edebe\eds\distribution_TT\README.md) with full workflow usage and prerequisites

## Validation

Command run:

```powershell
python C:\Users\edebe\eds\distribution_TT\tiktok_workflow.py --top2-package-json C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-03\top2_cross_product_post.json --output-root C:\Users\edebe\eds\distribution_TT\runs --ffmpeg-binary C:\Users\edebe\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe --upload-mode dry-run
```

Run artifacts:
- [tiktok_top2.mp4](C:\Users\edebe\eds\distribution_TT\runs\20260403_153937\tiktok_top2.mp4)
- [caption.txt](C:\Users\edebe\eds\distribution_TT\runs\20260403_153937\caption.txt)
- [resolved_clip_input.json](C:\Users\edebe\eds\distribution_TT\runs\20260403_153937\resolved_clip_input.json)
- [workflow_manifest.json](C:\Users\edebe\eds\distribution_TT\runs\20260403_153937\workflow_manifest.json)
- [upload_result.json](C:\Users\edebe\eds\distribution_TT\runs\20260403_153937\upload_result.json)

Dry-run result:
- `upload_status=dry_run`
- no fabricated external post result was recorded
- the workflow wrote the exact reason that publish was intentionally not attempted in dry-run mode

Resolved source-derived values used:
- leader: `NQ`
- leader_pnl: `1460.0`
- challenger: `ES`
- challenger_pnl: `740.0`
- gap: `720.0`
- source_last_update: `2026-04-03T13:02:40.333118`

## Outcome

Completed successfully.

The full TikTok workflow is implemented and validated in dry-run mode. Real publish is now gated only on providing a logged-in TikTok browser session or equivalent Playwright storage state for `--upload-mode playwright`.
