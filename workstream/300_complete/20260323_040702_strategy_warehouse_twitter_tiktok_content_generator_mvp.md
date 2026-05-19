Source: `C:\Users\edebe\eds\workstream\000_epic\20260316_135233_strategy_warehouse_autonomous_marketing_engine_processed.md`

Task Summary: Carve out Twitter and TikTok content generation as standalone MVP from Strategy Warehouse Marketing Engine for immediate use alongside trading app.

Context:
- Project: Strategy Warehouse Autonomous Marketing Engine
- Parent Epic: `20260316_135233_strategy_warehouse_autonomous_marketing_engine_processed.md`
- Urgency: HIGH - needed immediately for live use
- Existing codebase: `C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\`

Priority: 1

**Suggested Agent:** claude

## Objective

Extract and package the Twitter and TikTok content generation components as a lightweight, standalone service that:
1. Runs alongside the existing trading app (TradeApps/breakout)
2. Reads live strategy data from `_summary_net.json`, `_frequency.json`, `_dna_frequency.json`
3. Generates ready-to-post Twitter content
4. Generates TikTok video scripts for animated character delivery

## Data Sources (Already Available)

| File | Path | Content |
|------|------|---------|
| `_summary_net.json` | `TradeApps/breakout/DB/json/live/{product_type}/{date}/` | Strategy net points, buy/sell counts, directional bias |
| `_frequency.json` | Same path | Leaderboard snapshots, ranked strategies |
| `_dna_frequency.json` | Same path | DNA strategy variant rankings |

## Required Outputs

### Twitter Content (Text Posts)
1. **Signal Alert** - "Momentum check: {strategy} on {product}. Net {points} pts, {bias}-led bias. {buys} buys vs {sells} sells..."
2. **Performance Recap** - "Discipline over noise: {product} leads with {points} pts while {snapshots} snapshots keep the tape honest..."
3. **Leaderboard Watch** - "Leaderboard watch: 1. {name} (+{pts}) | 2. {name} (+{pts}) | 3. {name} (+{pts})..."

### TikTok Scripts (For Animated Character)
1. **Signal Alert Script** - Engaging spoken script for animated character announcing momentum signals
2. **Leaderboard Script** - Character narrating top strategy rankings with enthusiasm
3. **Format**: JSON with `spoken_text`, `visual_cues`, `duration_seconds`, `hashtags`

## Plan

- [x] 1. Create standalone content generator script
  - [x] Location: `C:\Users\edebe\eds\TradeApps\breakout\fs\social_content_generator.py`
  - [x] Test: Run script and verify JSON output generated
  - [x] Evidence: Script runs successfully, generates valid JSON

- [x] 2. Implement data loader to read warehouse JSON files
  - [x] Read from latest date directory in `json/live/{product_type}/`
  - [x] Parse `_summary_net.json`, `_frequency.json`, `_dna_frequency.json`
  - [x] Test: Script loads data from live trading session
  - [x] Evidence: Loaded from /mnt/c/Users/edebe/eds/TradeApps/breakout/fs/json/live/forex/2026-03-23

- [x] 3. Implement Twitter content templates
  - [x] Signal Alert template with strategy, product, net points, bias, buy/sell counts
  - [x] Performance Recap template with leader, points, snapshot count
  - [x] Leaderboard Watch template with top 3 strategies
  - [x] Test: Generate sample Twitter posts from live data
  - [x] Evidence: 3 Twitter posts generated, all within 280 char limit

- [x] 4. Implement TikTok script generator
  - [x] Create character-friendly spoken scripts
  - [x] Include visual cue markers for animation sync
  - [x] Add timing/pacing for 15-30 second videos
  - [x] Test: Generate TikTok script JSON from live data
  - [x] Evidence: 3 TikTok scripts generated with spoken_text, visual_cues, duration_seconds

- [x] 5. Add CLI interface for manual triggering
  - [x] `python social_content_generator.py --twitter` - output Twitter content
  - [x] `python social_content_generator.py --tiktok` - output TikTok scripts
  - [x] `python social_content_generator.py --all` - output both
  - [x] Test: Run CLI commands successfully
  - [x] Evidence: All CLI commands tested and working

- [x] 6. Add output to file option
  - [x] `--output /path/to/output.json` flag
  - [x] Default: print to stdout
  - [x] Test: Verify file output works
  - [x] Evidence: Output written to /tmp/social_test.json successfully

- [x] 7. Integration test with live trading data
  - [x] Run during active trading session
  - [x] Verify content reflects real strategy performance
  - [x] Test: Content matches current leaderboard state
  - [x] Evidence: Content shows DNA_102200_AUD (+825), matches live leaderboard

## Output Schema

### Twitter Output
```json
{
  "platform": "twitter",
  "generated_at": "2026-03-23T04:00:00",
  "posts": [
    {
      "type": "signal_alert",
      "text": "Momentum check: brk R 2 tp10.0 sl20.0 on GBPEUR_C. Net +450 pts, buy-led bias. 12 buys vs 8 sells on the latest pass. #StrategyWarehouse #TradingSignals #AlgoTrading #GBPEUR",
      "hashtags": ["#StrategyWarehouse", "#TradingSignals", "#AlgoTrading", "#GBPEUR"],
      "char_count": 198
    },
    {
      "type": "leaderboard_watch",
      "text": "Leaderboard watch: 1. DNA_104008_CHF (+505) | 2. DNA_104025_CHF (+490) | 3. DNA_104029_CHF (+475). Rotation matters more than hype. #StrategyWarehouse #Leaderboard",
      "hashtags": ["#StrategyWarehouse", "#Leaderboard"],
      "char_count": 165
    }
  ]
}
```

### TikTok Script Output
```json
{
  "platform": "tiktok",
  "generated_at": "2026-03-23T04:00:00",
  "scripts": [
    {
      "type": "signal_alert",
      "duration_seconds": 20,
      "spoken_text": "Hey traders! Quick momentum check - our breakout strategy just hit plus four-fifty points on GBPEUR! That's twelve buys versus eight sells. The buy side is leading this one. Link in bio to join the warehouse!",
      "visual_cues": [
        {"time": 0, "cue": "wave_greeting"},
        {"time": 3, "cue": "show_chart_graphic"},
        {"time": 10, "cue": "thumbs_up"},
        {"time": 17, "cue": "point_to_link"}
      ],
      "hashtags": ["#StrategyWarehouse", "#TradingSignals", "#AlgoTrading", "#ForexTrading", "#TradingTips"],
      "caption": "Momentum alert! +450 pts on GBPEUR. Join the warehouse for more signals!"
    },
    {
      "type": "leaderboard_watch",
      "duration_seconds": 25,
      "spoken_text": "Leaderboard update! DNA one-oh-four-oh-oh-eight is crushing it at plus five-oh-five points! Second place goes to DNA one-oh-four-oh-two-five, and third is DNA one-oh-four-oh-two-nine. These DNA strategies are on fire today!",
      "visual_cues": [
        {"time": 0, "cue": "excited_intro"},
        {"time": 5, "cue": "show_rank_1"},
        {"time": 12, "cue": "show_rank_2_3"},
        {"time": 20, "cue": "celebrate"}
      ],
      "hashtags": ["#StrategyWarehouse", "#Leaderboard", "#AlgoTrading", "#DNAStrategies"],
      "caption": "Who's leading the board today? DNA strategies are dominating!"
    }
  ]
}
```

## Validation
- [x] Script runs without errors from command line
- [x] Twitter content is within 280 character limit (237, 276, 280 chars)
- [x] TikTok scripts have natural spoken language (numbers spoken as words)
- [x] Content reflects actual live trading data (2026-03-23 forex data)
- [x] Output JSON is valid and parseable
- [x] Can run alongside active trading app without interference

## Files to Create
- `C:\Users\edebe\eds\TradeApps\breakout\fs\social_content_generator.py` - Main generator script

## Dependencies
- Python 3.x (already available)
- json (standard library)
- pathlib (standard library)
- argparse (standard library)
- No external packages required

## Implementation Notes
- Keep it simple - single file script for MVP
- Read-only access to trading data (no modifications)
- Safe to run during live trading
- Can be scheduled via cron/task scheduler for automated generation

Required Skills:
- `skills/workstream-task-lifecycle/SKILL.md`

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: code_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\social_content_generator.py`
  - Objective-Proved: Standalone content generator produces Twitter and TikTok content from live trading data
  - Status: complete
  - Test Output: Script generated 3 Twitter posts (signal_alert, leaderboard_watch, performance_recap) and 3 TikTok scripts with visual cues

## Implementation Log
- 2026-03-23 04:07: Task created - urgent MVP carve-out from marketing engine
- 2026-03-23 10:27: Implementation complete - all 7 plan items implemented and tested

## Changes Made
- Created `TradeApps/breakout/fs/social_content_generator.py` (new file ~400 lines)
  - Data loader: reads `_summary_net.json`, `_frequency.json`, `_dna_frequency.json`
  - Twitter generator: signal_alert, leaderboard_watch, performance_recap templates
  - TikTok generator: spoken scripts with visual_cues, timing, hashtags
  - CLI: --twitter, --tiktok, --all, --output, --product-type, --pretty flags

## Risks/Notes
- MVP focuses on content generation only, not posting (manual copy/paste to platforms)
- TikTok scripts require external animated character tool for video creation
- Future: Add direct Twitter API posting, TikTok video generation

Completion Status: Complete
