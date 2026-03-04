# Task: Breakout Phase 4 - Social Distribution

## Status
IN_PROGRESS (Awaiting Twitter API credentials)

## Source
- **Backlog**: `workstream/000_backlog/20260224_124302_20260224_1100_Breakout_Market_Narrative_Distribution.md`
- **Phase**: Phase 4 from backlog execution plan
- **Project**: Breakout / PipHunter

## Description
Set up automated posting to social media (X/Twitter) with teaser content that links back to the website.

## Objective
Drive traffic to the Breakout Live Hub by posting engaging teaser content on social media with clear CTAs.

## Sub-tasks
- [ ] Set up X/Twitter API integration (MANUAL)
  - Create developer account
  - Obtain API keys (OAuth 2.0)
  - Add credentials to config.json
- [x] Build `social_publisher.py`
  - Accept narrative input
  - Format for Twitter (280 chars)
  - Add link to website
  - Add PH branding hashtags
  - Rate limiting logic (60 min min, 12/day max)
  - Error handling / retry
  - Dry run mode when API not configured
- [x] Define trigger events for posting
  - Significant bias shift
  - Net milestone (+500, +1000, etc.)
  - Hourly summary
- [x] Create social post templates with PH branding
  - Teaser template with metrics
  - Hourly summary template
  - Milestone celebration template (bias_shift, net_milestone, new_leader)
- [x] Create Twitter API setup documentation
- [x] Integrate with trade_viewer_api.py

## Implementation Log

### 2026-02-24 15:50
- Created `social_publisher.py` at `TradeApps/breakout/fs/social_publisher.py`
- Implemented `SocialPublisher` class with:
  - Rate limiting (60 min between posts, 12/day max)
  - Post formatting for teaser, hourly, milestone types
  - Dry run mode when API not configured
  - Post logging to `social_posts.json`
  - Trigger event detection (bias shift, net milestone)

### 2026-02-24 15:55
- Added Flask route integration via `add_social_routes(app)`
- Added routes:
  - `GET /api/social/status` - Check publishing status
  - `GET /api/social/preview` - Preview post content
  - `POST /api/social/publish` - Manually trigger a post
- Integrated into `trade_viewer_api.py`

### 2026-02-24 16:00
- Created `TWITTER_SETUP.md` documentation with:
  - Step-by-step Twitter developer account setup
  - API credential configuration
  - Testing instructions
  - API endpoint documentation
  - Rate limit explanation
  - Post template examples

## Deliverables

| Deliverable | Path | Status |
|-------------|------|--------|
| Social Publisher | `fs/social_publisher.py` | Done |
| API Endpoints | `/api/social/*` | Done |
| Setup Guide | `landing/TWITTER_SETUP.md` | Done |
| Twitter API Credentials | config.json | MANUAL - Pending |

## Content Restrictions (Social)
| Show | Don't Show |
|------|------------|
| Overall returns | Individual trade details |
| Bias (BUY/SELL) | Entry/exit prices |
| Top performer name | Algo parameters |

## Sample Posts (Verified Working)

### Teaser
```
🟢 LIVE BATTLE UPDATE
Bias: BUY | Confidence: HIGH

See full battle stats:
https://piphunter.io

#PipHunter #Trading
```

### Hourly
```
📊 15:00 HOUR UPDATE

Market Bias: BUY
Confidence: HIGH
Active Positions: 0

Full battle stats:
https://piphunter.io

#PipHunter #Trading
```

## Verification Test
1. Test post successfully published to Twitter - Pending API credentials
2. Link in post opens website correctly - Posts include correct URL
3. Rate limiting prevents over-posting - Implemented (60 min, 12/day)
4. Trigger events fire correctly - Implemented (bias shift, milestone)
5. Post format matches brand guidelines - Verified via preview

## Manual Steps Required

### Twitter API Setup
1. Create Twitter Developer account at https://developer.twitter.com
2. Create Project and App
3. Get API credentials (API Key, API Secret, Access Token, Access Token Secret)
4. Add to `TradeApps/breakout/fs/config.json`:
```json
{
    "twitter_api_key": "...",
    "twitter_api_secret": "...",
    "twitter_access_token": "...",
    "twitter_access_secret": "..."
}
```
5. Install tweepy: `pip install tweepy`
6. Test: `python social_publisher.py --action publish --type teaser`

## Completion Date
(To be filled after API credentials are configured)
