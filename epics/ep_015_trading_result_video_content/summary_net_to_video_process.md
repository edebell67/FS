# Summary Net To Video Process

Reusable operator workflow for turning breakout `_summary_net.json` into reviewable short-form or long-form trading-result video content.

## Purpose

Convert daily breakout strategy equity data into a dated video-content package that can be:
- reviewed by an operator
- handed to an editor or video-generation tool
- reused for Shorts, reels, landscape recap videos, or NotebookLM/video-prompt workflows

This process is for breakout `_summary_net.json` data only.

## Required Output Location

All output from this process must go under:

`C:\Users\edebe\eds\epics\ep_015_trading_result_video_content`

Recommended dated package path:

`C:\Users\edebe\eds\epics\ep_015_trading_result_video_content\YYYY-MM-DD\`

## Primary Input

- `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\YYYY-MM-DD\_summary_net.json`

Optional supporting inputs:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\YYYY-MM-DD\_top20.json`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\YYYY-MM-DD\_targeted_strategies.json`
- any approved screenshots/charts generated from the same date

## What The Source Means

`_summary_net.json` contains:
- `last_update`
- `session_max_net`
- `strategies`

`strategies` is a nested structure:
- strategy name
- product
- time-ordered net snapshots

This is enough to build:
- equity-curve stories
- top/worst performer comparisons
- session progression narratives
- strategy-vs-product highlights

## Output Package

For each target date, create a package folder containing:

- `summary_net_video_package.json`
  - machine-readable package metadata
- `summary_net_video_brief.md`
  - operator-facing summary of what the video says
- `summary_net_video_script.txt`
  - plain narration script
- `summary_net_video_storyboard.md`
  - scene-by-scene breakdown
- `summary_net_video_hook_options.txt`
  - opening hook variants
- `summary_net_video_overlay_copy.txt`
  - short on-screen text lines
- `summary_net_video_asset_manifest.json`
  - chart, background, logo, and visual asset references
- `summary_net_video_render_notes.md`
  - export settings, pacing, aspect ratio, and QA notes

Optional:
- `summary_net_video_prompt.txt`
  - if using an AI video generator
- `summary_net_video_thumbnail_brief.txt`
  - if a thumbnail/poster is needed

## Recommended Video Formats

Produce one of these per package:

1. Short vertical recap
   - 20-45 seconds
   - strongest hook first
   - 3-5 scenes

2. Standard daily recap
   - 45-90 seconds
   - top performers, laggards, and session close

3. Longer analyst breakdown
   - 90-180 seconds
   - more detailed curve progression and interpretation

## Narrative Framework

Use this fixed structure:

1. Hook
   - strongest claim from the day
   - example: best breakout curve, worst fade, biggest reversal, strongest trend persistence

2. Context
   - date
   - market scope
   - what the viewer is looking at

3. Main result
   - top strategy/product outcome
   - absolute or relative performance

4. Supporting comparison
   - compare against second-best, weakest, or session median

5. Interpretation
   - what changed across the session
   - whether the curve was smooth, volatile, late-recovering, or deteriorating

6. Close
   - concise takeaway
   - optional CTA for next update

## Selection Rules

When turning `_summary_net.json` into a video package, rank and select content in this order:

1. Biggest positive final net result
2. Biggest negative final net result
3. Largest intraday reversal
4. Smoothest upward curve
5. Most volatile curve worth explaining

Avoid using every strategy. Pick only the few curves that tell a clear story.

## Scene Template

Use this scene model:

1. Scene 1: hook frame
   - one bold takeaway
   - one headline metric

2. Scene 2: equity curve reveal
   - chart for the featured strategy/product
   - highlight start, inflection, and end

3. Scene 3: comparison frame
   - second curve or scoreboard comparison

4. Scene 4: interpretation frame
   - what the moves suggest about the session

5. Scene 5: closing summary
   - short conclusion
   - next update / brand line

## Operator Workflow

1. Choose the target date.
2. Load the relevant `_summary_net.json`.
3. Confirm the file only contains the intended product scope.
4. Extract final net values per strategy/product pair.
5. Rank top winners, top losers, reversals, and standout curves.
6. Decide the video format: short recap, daily recap, or analyst breakdown.
7. Write the video brief in plain English.
8. Draft 3-5 hook options.
9. Build the scene-by-scene storyboard.
10. Write the narration script.
11. Write compact overlay copy for each scene.
12. List required visuals in the asset manifest.
13. Save all outputs into the dated package folder under `ep_015_trading_result_video_content`.
14. Review the package for factual consistency against `_summary_net.json`.
15. Only then hand the package to the editor, prompt-based tool, or rendering workflow.

## Package Writing Rules

- Keep claims tied to the source data.
- Prefer relative framing over unexplained raw numbers when the raw number is not self-explanatory.
- If a curve is noisy, say so directly.
- If there is no compelling move, produce a restrained recap instead of forcing hype.
- Do not mix forex and non-forex scopes unless the package explicitly says it is multi-asset.
- If a strategy/product pair is selected, keep the same naming across brief, script, and storyboard.

## Script Rules

- Lead with the result, not the methodology.
- Use short spoken sentences.
- Keep numbers sparse and memorable.
- Convert raw analytics into viewer language:
  - "climbed steadily through the session"
  - "gave back gains late"
  - "spent most of the day underwater"
  - "finished as the cleanest breakout curve on the board"

## Visual Rules

- Use line-chart motion, not static tables, for the core story.
- Highlight only a few timestamps, not every point.
- Keep overlays short enough to read in under 2 seconds.
- Show date, strategy, and product clearly on screen.
- Keep one dominant message per scene.

## Quality Gate

Before a package is marked ready:

- the selected strategy/product pairs exist in `_summary_net.json`
- final values used in narration match the source
- the storyboard and script reference the same winners/losers
- there are no non-scope products
- the package folder is inside `ep_015_trading_result_video_content`
- file names are date-stable and readable

## Suggested Folder Layout

```text
ep_015_trading_result_video_content/
└── YYYY-MM-DD/
    ├── summary_net_video_package.json
    ├── summary_net_video_brief.md
    ├── summary_net_video_script.txt
    ├── summary_net_video_storyboard.md
    ├── summary_net_video_hook_options.txt
    ├── summary_net_video_overlay_copy.txt
    ├── summary_net_video_asset_manifest.json
    ├── summary_net_video_render_notes.md
    ├── summary_net_video_prompt.txt
    └── summary_net_video_thumbnail_brief.txt
```

## Manual Validation

Minimum validation steps:

1. Open `_summary_net.json` and confirm the chosen date/source.
2. Cross-check every named strategy/product pair in the brief.
3. Confirm every output file was written under:
   - `C:\Users\edebe\eds\epics\ep_015_trading_result_video_content\YYYY-MM-DD\`
4. Read the final script out loud once for pacing.
5. Confirm the first 5 seconds contain a clear hook.

## Future Automation Path

If this is automated later, the generator should:

- read `_summary_net.json`
- rank standout curves
- select the narrative candidate set
- emit the package files listed above
- optionally generate chart PNGs for the storyboard
- optionally emit a ready-to-use AI video prompt

The automation should still write all outputs into:

`C:\Users\edebe\eds\epics\ep_015_trading_result_video_content\YYYY-MM-DD\`

## Troubleshooting

- If `_summary_net.json` is missing:
  - regenerate or restore the daily summary first

- If there are too many candidate curves:
  - limit selection to top winner, top loser, and one reversal

- If the story feels weak:
  - shorten the video and frame it as a daily checkpoint rather than a highlight reel

- If product scope looks wrong:
  - validate the source file before building the package
