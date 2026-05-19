Source: User request

Task Summary: Update Twitter content templates to reflect modest account journey narrative with forex and crypto focus.

Context:
- Project: TradeApps/breakout
- File Modified: `TradeApps/breakout/fs/social_content_generator.py`

Priority: 1

## Objective

Rebrand Twitter content to position as a modest account building journey, focusing on forex and crypto trading signals.

## Plan

- [x] 1. Update signal alert template
  - [x] Add "Day 1 of the modest account journey" opening
  - [x] Update hashtags to #ForexTrading #CryptoTrading #SmallAccountChallenge
  - [x] Evidence: Template updated

- [x] 2. Update leaderboard template
  - [x] Change to "Modest account leaderboard" framing
  - [x] Add forex and crypto focus messaging
  - [x] Evidence: Template updated

- [x] 3. Update performance recap template
  - [x] Change to "Modest account update" framing
  - [x] Add "Slow and steady" disciplined messaging
  - [x] Evidence: Template updated

- [x] 4. Test output
  - [x] Verify new messaging in generated posts
  - [x] Evidence: All 3 posts generated with new messaging

## Changes Made
- Modified `TradeApps/breakout/fs/social_content_generator.py`:
  - `generate_twitter_signal_alert()`: New messaging + hashtags (lines 248-254)
  - `generate_twitter_leaderboard()`: New messaging + hashtags (lines 283-286)
  - `generate_twitter_performance_recap()`: New messaging + hashtags (lines 314-318)

## Sample Output
```
Day 1 of the modest account journey. Tracking brk 2 tp20 sl20 on NZDAUD_C. Net +950 pts, sell-led bias. 1 buys vs 4 sells. Building up one signal at a time. #ForexTrading #CryptoTrading #SmallAccountChallenge #NZDAUDC
```

## Evidence
Objective-Delivery-Coverage: 100%
- Evidence-Type: code_output
  - Status: complete

## Implementation Log
- 2026-03-23 12:17: User requested modest account journey messaging with forex/crypto focus
- 2026-03-23 12:17: Updated all 3 Twitter templates

Completion Status: Complete
