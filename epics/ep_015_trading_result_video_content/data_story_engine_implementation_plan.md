# Breakout Data Story Engine Implementation Plan

## Purpose

Turn breakout trading outputs into a repeatable story engine that:
- detects meaningful market/story events from existing JSON outputs
- converts those events into structured story objects
- renders those story objects into video-content packages first
- later expands into X, website, Reddit, email, and alert outputs

This plan is the repo-specific implementation follow-up to:

- `C:\Users\edebe\Downloads\data_story_engine_plan.md`

It is aligned to epic:

- `C:\Users\edebe\eds\epics\ep_015_trading_result_video_content`

## Strategic Position

The breakout platform already produces enough data to tell compelling stories.

Current state:
- `_summary_net.json` gives strategy/product equity-curve snapshots
- related trade JSON files provide the underlying evidence
- `ep_015` already contains:
  - a process for turning `_summary_net.json` into video content
  - a template package
  - a dated sample package

Missing state:
- story detection is still mostly manual
- video package creation is not yet driven by reusable story objects
- there is no detector layer separating:
  - raw data interpretation
  - story selection
  - channel rendering

The implementation goal is to add that missing middle layer.

## High-Level Target Architecture

```text
Breakout FS JSON outputs
    ↓
Normalization layer
    ↓
Feature calculation layer
    ↓
Story detectors
    ↓
Structured story objects
    ↓
Channel renderers
        ├── video package renderer
        ├── X teaser renderer
        ├── website evidence renderer
        ├── Reddit discussion renderer
        └── subscriber alert renderer
```

## Existing Inputs To Use First

Phase 1 should stay close to the data already present in the breakout repo.

### Primary inputs

- `TradeApps/breakout/fs/json/live/<scope>/<YYYY-MM-DD>/_summary_net.json`
- `TradeApps/breakout/fs/json/live/<scope>/<YYYY-MM-DD>/breakout*.json`

### Secondary inputs

- `_top20.json`
- `_targeted_strategies.json`
- config allowlists such as:
  - `TradeApps/breakout/fs/config.json`

### Important note

Start with `forex` only in the first pass unless explicitly expanded.
The story engine should support broader scopes later, but `ep_015` should prove the workflow in one controlled domain first.

## First Story Types To Implement

Do not implement the full brief immediately.
Start with a small high-value set that maps well to `_summary_net.json`.

### 1. Top winner

Question answered:
- which strategy/product pair finished strongest?

Why first:
- simple
- useful
- already supports video recap

### 2. Worst loser

Question answered:
- which pair finished weakest?

Why first:
- creates immediate contrast with the winner
- strong for hooks and thumbnails

### 3. Biggest reversal

Question answered:
- which pair had the largest spread between session high and low?

Why first:
- fits video storytelling well
- gives a non-leaderboard angle

### 4. Market courtroom

Question answered:
- which side/product/strategy is the villain and which is the hero?

Why first:
- one of the strongest narrative formats in the brief
- maps cleanly to winner/loser divergence

### 5. Autopsy of a winning day

Question answered:
- what actually caused the session result?

Why first:
- turns raw outcome into an explanation
- strong for video and website renderers

### 6. Takeover watch

Question answered:
- which strategy is not leading yet but is accelerating?

Why first:
- introduces pre-detection without overbuilding
- supports subscriber/watch outputs later

## Story Object Schema

All renderers should consume the same story object shape.

Minimum v1 schema:

```json
{
  "story_id": "2026-04-24-forex-top-winner-001",
  "story_type": "top_winner",
  "target_date": "2026-04-24",
  "scope": "forex",
  "headline": "",
  "summary": "",
  "strategy": "",
  "product": "",
  "product_type": "forex",
  "metrics": {
    "first_net": 0,
    "last_net": 0,
    "max_net": 0,
    "min_net": 0,
    "reversal": 0,
    "points": 0
  },
  "comparison": {
    "strategy": "",
    "product": "",
    "reason": ""
  },
  "evidence": [],
  "chart_needed": true,
  "recommended_chart": "equity_curve",
  "confidence": "high",
  "risk_note": "",
  "created_at": ""
}
```

## Repo-Oriented Module Plan

Recommended initial location:

`C:\Users\edebe\eds\TradeApps\breakout\fs\tools\data_story_engine\`

Recommended files:

```text
TradeApps/breakout/fs/tools/data_story_engine/
├── README.md
├── generate_story_package.py
├── story_schema.py
├── loader.py
├── normalizers.py
├── feature_builder.py
├── detectors.py
├── confidence.py
├── renderers/
│   ├── video_package_renderer.py
│   ├── x_renderer.py
│   ├── website_renderer.py
│   └── alert_renderer.py
└── templates/
    ├── story_object_template.json
    └── renderer_defaults.json
```

## Phase Plan

## Phase 0 — Definition Lock

Objective:
- freeze the initial scope and schema before writing the engine

Deliverables:
- story object v1 schema
- agreed detector list for MVP
- agreed output folder convention

Completion criteria:
- story types for MVP are named and fixed
- epic `015` remains the output root for video package outputs

## Phase 1 — Loader And Normalization

Objective:
- load breakout daily source files into a consistent internal structure

Tasks:
- load `_summary_net.json`
- normalize strategy/product bucket rows
- compute:
  - first net
  - last net
  - max net
  - min net
  - reversal
  - number of points
- optionally map supporting trade files later

Output:
- normalized row list per date and scope

Completion criteria:
- one function can produce a clean normalized list from `_summary_net.json`

## Phase 2 — Feature Builder

Objective:
- compute reusable features for detectors

MVP features:
- final net
- session high
- session low
- reversal size
- net gain from first to last
- simple slope proxy
- optional point density / update count

Future features:
- rank velocity
- rolling window return
- side dominance
- family confirmation
- trade cluster quality

Completion criteria:
- normalized rows contain all detector-ready feature fields

## Phase 3 — After-The-Fact Detectors

Objective:
- create confirmed story objects from completed daily data

MVP detectors:
- top winner detector
- worst loser detector
- biggest reversal detector
- market courtroom detector
- autopsy of a winning day detector

Logic examples:

### top winner detector
- sort by `last_net desc`
- choose highest qualifying pair

### worst loser detector
- sort by `last_net asc`
- choose lowest qualifying pair

### biggest reversal detector
- sort by `reversal desc`

### market courtroom detector
- choose the strongest positive/negative divergence pair
- prefer same family or comparable strategy naming when available

### autopsy detector
- determine whether the day was carried by one cluster, one side, or one narrow group

Completion criteria:
- one daily run produces a small set of high-confidence story objects

## Phase 4 — Video Package Renderer

Objective:
- replace manual package drafting with renderer-driven output

Renderer input:
- one or more story objects

Renderer output:
- `summary_net_video_package.json`
- `summary_net_video_brief.md`
- `summary_net_video_script.txt`
- `summary_net_video_storyboard.md`
- `summary_net_video_hook_options.txt`
- `summary_net_video_overlay_copy.txt`
- `summary_net_video_asset_manifest.json`
- `summary_net_video_render_notes.md`
- `summary_net_video_prompt.txt`
- `summary_net_video_thumbnail_brief.txt`

Output root:
- `C:\Users\edebe\eds\epics\ep_015_trading_result_video_content\YYYY-MM-DD\`

Completion criteria:
- a single command can build a dated video package directly from `_summary_net.json`

## Phase 5 — Website Evidence Renderer

Objective:
- produce evidence-room style output for the web

Possible outputs:
- story cards
- chart callout blocks
- evidence bullets
- comparison tables

Not MVP-critical for `ep_015`, but should be designed now so story objects are renderer-agnostic.

## Phase 6 — Early-Warning Layer

Objective:
- add pre-detection capability carefully

Initial pre-detection features:
- rank velocity
- return slope
- acceleration
- leaderboard compression

Initial early-warning outputs:
- takeover watch
- explosive strategy forming
- almost-signal

Important rule:
- must always be framed as developing or forming
- never as certainty

Completion criteria:
- early-warning story objects include confidence score and explicit risk note

## Recommended MVP Command

Target command shape:

```powershell
python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\data_story_engine\generate_story_package.py --scope forex --date 2026-04-24
```

Expected result:
- reads `_summary_net.json`
- emits story objects
- writes a dated video-content package into epic `015`

## Output Convention

### Story object output

Recommended machine-readable output path:

`C:\Users\edebe\eds\epics\ep_015_trading_result_video_content\YYYY-MM-DD\story_objects.json`

### Video package output

Current output path should remain:

`C:\Users\edebe\eds\epics\ep_015_trading_result_video_content\YYYY-MM-DD\`

## Validation Plan

### Validation 1
- normalized rows match `_summary_net.json` values

### Validation 2
- detector selections match manual review for a known date

### Validation 3
- generated video package matches the selected story objects exactly

### Validation 4
- no off-scope products leak into forex output

### Validation 5
- story claims remain traceable to source metrics

## Risks

### 1. Overclaim risk
- early-warning logic may sound predictive if not framed carefully

### 2. Weak-story risk
- not every day produces a strong narrative
- engine needs a fallback restrained recap mode

### 3. Data-shape drift
- `_summary_net.json` structure may evolve
- loaders should be defensive and version-aware

### 4. Scope contamination
- mixed asset types can leak into a scope if upstream cleanup is weak

## Immediate Next Tasks

1. Create `fs/tools/data_story_engine/README.md`
2. Implement `_summary_net.json` loader and row normalizer
3. Implement feature builder for final net, min, max, reversal, point count
4. Implement detectors:
   - top winner
   - worst loser
   - biggest reversal
5. Emit `story_objects.json`
6. Refactor current `ep_015` package creation into `video_package_renderer.py`
7. Validate against the existing `2026-04-24` manually produced package

## Recommended Task Decomposition

### Task 1
- build normalized summary-net loader

### Task 2
- build feature calculator

### Task 3
- build after-the-fact detectors

### Task 4
- build story object serializer

### Task 5
- build video package renderer

### Task 6
- compare automated package vs manual package for `2026-04-24`

## Definition Of Done

This plan is considered delivered when:
- the implementation path is concrete
- the modules are named
- the phases are sequenced
- the output root is fixed to epic `015`
- the next tasks are clear enough to execute without re-planning
