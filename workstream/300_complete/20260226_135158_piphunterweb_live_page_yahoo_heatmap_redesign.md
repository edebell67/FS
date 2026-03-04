# PipHunterWeb - Live Page Redesign (Yahoo Finance Heatmap Style)

## Source
New task - no backlog item (direct user request)

## Task Summary
Create a new web-based trading dashboard at `localhost:5001/live` for the PipHunterWeb project using Yahoo Finance heatmap look and feel. Apply visual DNA, color language, and interaction patterns from `/skills/yahoo_heatmap_look_and_feel_skill.md`.

## Context
- **Project**: piphunterweb (web-based tasks for piphunter)
- **Target**: `localhost:5001/live`, `/signals`, `/strategies`
- **Data Source**: PipHunter API `/api/v1/strategies/universe`, `/api/v1/signals`
- **Reference Skill**: `/skills/yahoo_heatmap_look_and_feel_skill.md`

## Implementation Log
| Timestamp | Action |
|-----------|--------|
| 2026-02-26 13:51 | Task created |
| 2026-02-26 13:55 | Moved to in_progress |
| 2026-02-26 14:10 | Created templates folder |
| 2026-02-26 14:12 | Created live.html with Yahoo heatmap design |
| 2026-02-26 14:14 | Created routes/web.py |
| 2026-02-26 14:15 | Registered web_bp in app.py |
| 2026-02-26 15:35 | User requested strategy-focused heatmap instead of market prices |
| 2026-02-26 15:40 | Rewrote live.html to use /api/v1/strategies/universe endpoint |
| 2026-02-26 15:42 | Added P&L-based coloring, trade count sizing, filters |
| 2026-02-26 15:50 | Added dark mode toggle with localStorage persistence |
| 2026-02-26 16:00 | Created signals.html - card-based signal display |
| 2026-02-26 16:05 | Created strategies.html - sortable table view |
| 2026-02-26 16:10 | Updated web.py with /signals and /strategies routes |
| 2026-02-26 16:15 | Task complete - moved to 300_complete |

## Changes Made
| File | Change |
|------|--------|
| `api/templates/live.html` | Strategy heatmap with ECharts treemap, P&L coloring, dark mode |
| `api/templates/signals.html` | NEW - Card-based signals page with bias indicator |
| `api/templates/strategies.html` | NEW - Sortable table with rankings and win rate bars |
| `api/routes/web.py` | Web blueprint with /live, /signals, /strategies routes |
| `api/app.py` | Added web_bp import and registration |

## Features Implemented

### All Pages
- **Dark/Light Mode**: Toggle button with localStorage persistence, respects system preference
- **Consistent Navigation**: Header with links to all three pages
- **Auto-refresh**: Every 30 seconds
- **Responsive**: Mobile-friendly layouts
- **Yahoo-style Design**: Purple gradient header, Inter font, green/red color scale

### /live - Strategy Heatmap
- **Treemap Heatmap**: Strategies as tiles colored by P&L (green=profit, red=loss)
- **Filters**: Min trades (0/5/10/20/50+), P&L filter (all/profitable/losing), Size by (trades/pnl/equal)
- **Stats Cards**: Total P&L, Profitable count, Losing count, Total strategies
- **Table View**: Toggle between heatmap and table
- **Tooltips**: Strategy name, P&L, trades, win rate, buy/sell breakdown

### /signals - Trading Signals
- **Bias Indicator**: Current market bias (BUY/SELL) with status badge
- **Signal Cards**: Card-based layout with direction, P&L, win rate, trades, confidence
- **Color-coded**: Green border for BUY, red border for SELL

### /strategies - Strategy Performance
- **Sortable Table**: Click column headers to sort
- **Rank Badges**: Gold/silver/bronze for top 3
- **Win Rate Bars**: Visual progress bars
- **Stats Summary**: Total P&L, profitable/losing counts

## Validation
- `/live` - http://localhost:5001/live
- `/signals` - http://localhost:5001/signals
- `/strategies` - http://localhost:5001/strategies

## Acceptance Criteria
- [x] Heatmap fills available space cleanly
- [x] Color intensity matches P&L magnitude
- [x] Text readable on all tile colors (white text with shadow)
- [x] Hover tooltip works on desktop
- [x] Filters update heatmap correctly
- [x] Legend always visible
- [x] Auto-refresh with timestamp
- [x] Mobile responsive
- [x] Fast loading
- [x] Dark mode support
- [x] Signals page formatted (not JSON)
- [x] Strategies page formatted (not JSON)

## Risks/Notes
- Depends on `/api/v1/strategies/universe` and `/api/v1/signals` endpoints
- Yahoo skill provided design guidance - applied color palette, typography, layout patterns

## Completion Status
**COMPLETE** - 2026-02-26 16:15
