# Task: Breakout Phase 5 - Engagement Features

## Status
IN_PROGRESS (Core features complete, external services pending)

## Source
- **Backlog**: `workstream/000_backlog/20260224_124302_20260224_1100_Breakout_Market_Narrative_Distribution.md`
- **Phase**: Phase 5 from backlog execution plan
- **Project**: Breakout / PipHunter

## Description
Add subscriber capture, notification system, and analytics to drive ongoing engagement.

## Objective
Convert website visitors into subscribers and provide ongoing value through notifications.

## Sub-tasks
- [x] Add subscribe functionality
  - Email capture form on website - Done
  - Store in local JSON (Supabase ready) - Done
  - Email validation - Done
  - Verification token generation - Done
  - Unsubscribe mechanism - Done
- [x] Create subscriber API (`subscriber_api.py`)
  - POST /api/subscribe - Subscribe email
  - GET /api/subscribe/verify - Verify email
  - POST /api/unsubscribe - Unsubscribe
  - POST /api/subscribe/preferences - Update preferences
  - GET /api/subscribe/stats - Get statistics
- [x] Implement notification preferences
  - daily_summary
  - bias_shifts
  - milestones
  - new_leader
- [x] Create Supabase schema
  - `landing/SUPABASE_SCHEMA.sql` with table definition
  - Row Level Security policies
- [x] Add analytics placeholders
  - Plausible (privacy-friendly)
  - Vercel Analytics (if deployed on Vercel)
- [ ] External service integration (MANUAL)
  - Set up Supabase project
  - Run schema SQL
  - Add credentials to config.json
  - Set up email service (SendGrid/Resend)
- [ ] Mobile app CTA (Future phase)
  - App store links
  - QR code for download

## Implementation Log

### 2026-02-24 16:10
- Created `subscriber_api.py` at `TradeApps/breakout/fs/subscriber_api.py`
- Implemented `SubscriberManager` class with:
  - Email validation
  - Subscribe/Unsubscribe/Verify flows
  - Preference management
  - Supabase and local JSON fallback storage
  - Statistics endpoint

### 2026-02-24 16:15
- Added Flask route integration via `add_subscriber_routes(app)`
- Integrated into `trade_viewer_api.py`
- Tested subscriber API via CLI

### 2026-02-24 16:20
- Updated `breakout-live-hub.html` subscribe form
- Added async form submission
- Added loading state during submission
- Added error handling

### 2026-02-24 16:25
- Created `SUPABASE_SCHEMA.sql` with:
  - Subscribers table definition
  - Indexes for performance
  - Row Level Security policies
  - Documentation comments

### 2026-02-24 16:30
- Added analytics placeholders to website
- Added Plausible and Vercel Analytics options

## Deliverables

| Deliverable | Path | Status |
|-------------|------|--------|
| Subscriber API | `fs/subscriber_api.py` | Done |
| API Endpoints | `/api/subscribe/*` | Done |
| Website Form | `landing/breakout-live-hub.html` | Done |
| Supabase Schema | `landing/SUPABASE_SCHEMA.sql` | Done |
| Analytics | Placeholders added | Done |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/subscribe` | POST | Subscribe email |
| `/api/subscribe/verify` | GET | Verify with token |
| `/api/unsubscribe` | POST | Unsubscribe email |
| `/api/subscribe/preferences` | POST | Update preferences |
| `/api/subscribe/stats` | GET | Get statistics |

## Verification Test
1. User can subscribe with email - PASS (tested via CLI)
2. Validation rejects invalid emails - PASS
3. Preferences saved correctly - PASS
4. Unsubscribe works - PASS
5. Analytics placeholders in place - PASS

## Manual Steps Required

### Supabase Setup
1. Create project at https://supabase.com
2. Get project URL and anon key from Settings → API
3. Run `landing/SUPABASE_SCHEMA.sql` in SQL Editor
4. Add to `TradeApps/breakout/fs/config.json`:
```json
{
    "supabase_url": "https://your-project.supabase.co",
    "supabase_anon_key": "your-anon-key"
}
```

### Analytics Setup
1. Choose Plausible or Vercel Analytics
2. Uncomment the appropriate script in `breakout-live-hub.html`
3. Update domain name if using Plausible

## Completion Date
(Core features: 2026-02-24 16:30, External services pending)
