# Tweetable Dashboard Summary for Social Media

**Source**: User request for shareable FXPilot dashboard preview

## Task Summary
Create a summarized view of the FXPilot dashboard that can be tweeted as a link, generating a rich preview card when shared on social media platforms.

## Context
- **Full Dashboard URL**: `http://172.22.108.121:3001/`
- **API Server**: `http://172.22.108.121:5050/api`
- **Share URL**: `http://172.22.108.121:5050/share?date=YYYY-MM-DD&mode=live`
- **Related**: `social_publisher.py` exists for automated text tweets but doesn't include visual previews

## Implementation (Option C: Separate Flask Endpoint)

### Changes Made

**File**: `TradeApps/breakout/piphunter/landing_page/server.py`

1. Added `Response` import from Flask
2. Added `/share` endpoint (`share_summary()` function at line 225)

### Share Endpoint Features
- **Route**: `/share?date=YYYY-MM-DD&mode=live`
- **Returns**: Full HTML page with embedded CSS
- **Meta Tags**:
  - `og:title` - "FXPilot Trading Summary - {date}"
  - `og:description` - Dynamic summary (e.g., "327 strategies | +$48698 net | 100.0% profitable | 1544 trades | Top: GBP")
  - `og:type` - "website"
  - `og:url` - Full share URL
  - `twitter:card` - "summary"
  - `twitter:title` - Same as og:title
  - `twitter:description` - Same as og:description

### Summary Metrics Displayed
- Total Net P&L (with +/- coloring)
- Number of Strategies
- Win Rate (% profitable)
- Total Trades
- Top Performer (product + strategy)
- "View Full Dashboard" CTA button

### Visual Design
- Dark gradient background (#1a1a2e to #16213e)
- Glassmorphism card container
- Gradient accent colors (cyan #00d4ff to green #00ff88)
- 2x2 metric grid layout
- Mobile responsive

## Validation
- [x] Share endpoint returns valid HTML with meta tags
- [x] Summary metrics match dashboard data (327 strategies, $48698 net for 2026-02-27)
- [x] Link navigates to full dashboard with correct date/mode
- [x] External access works (http://172.22.108.121:5050/share)
- [ ] Twitter card preview (requires public URL - not localhost/WSL)
- [x] Works on mobile devices (responsive CSS)

## Usage Examples
```
# Default (today, live mode)
http://172.22.108.121:5050/share

# Specific date
http://172.22.108.121:5050/share?date=2026-02-27&mode=live

# Simulation mode
http://172.22.108.121:5050/share?date=2026-02-27&mode=sim
```

## Next Steps (Optional Enhancements)
- Add `og:image` with auto-generated chart screenshot (requires headless browser or chart library)
- Deploy to public URL for Twitter card testing
- Add `twitter:site` handle when Twitter account is configured
- Consider caching summary data for performance

## Dependencies
- Public URL for full Twitter card preview testing
- Twitter API credentials for auto-posting (separate task)

## Completion Status
**Complete** - Basic implementation with Open Graph and Twitter Card meta tags
