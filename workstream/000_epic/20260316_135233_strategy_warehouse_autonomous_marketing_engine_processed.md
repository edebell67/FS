# Epic: Strategy Warehouse Autonomous Marketing Engine

## Status
`READY FOR DECOMPOSITION` - Clarifications resolved 2026-03-16

## Product
Trading - Strategy Warehouse

## Strategic Objectives

1. **Increase online profile / improve reach** - Aggressively grow visibility of the product across social media platforms
2. **Increase subscriber base week-to-week** - Build and grow a subscriber list through a conversion funnel

## Requirement Summary

Build an autonomous marketing engine that:

- Generates and publishes content to social media platforms
- Drives traffic to a landing page
- Captures subscribers through the landing page
- Operates autonomously with minimal manual intervention
- Tracks and reports on reach and conversion metrics weekly

## Clarifications Resolved

### Platform Scope
- [x] **Q1:** Which social platforms are in scope?
  - [x] Twitter/X (primary)
  - [x] Discord
  - [x] Telegram
  - [x] LinkedIn
  - [x] Reddit
  - [x] TikTok

### Content Source
- [x] **Q2:** What data feeds the marketing content?
  - [x] Live trading signals from Strategy Warehouse
  - [x] Historical performance summaries
  - [x] Strategy rankings / leaderboards
  - **Data Path:** `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\{date}\_*.json`
  - **Files:** `_summary_net.json`, `_frequency.json`, `_dna_frequency.json`, `_dna_alt_frequency.json`

### Subscription Model
- [x] **Q3:** What is the subscription model?
  - [x] Free tier + paid premium tiers
  - **Payment processor:** TBD (Stripe recommended)

### Landing Page Location
- [x] **Q4:** Where should the landing page be hosted?
  - [x] New dedicated domain

### Aggressiveness Definition
- [x] **Q5:** Define "aggressive" reach targets:
  - [x] Posts per day target: TBD (to be defined per platform)
  - [x] Follower growth target (weekly): TBD
  - [x] Impressions target (weekly): TBD
  - [ ] Paid promotion budget: NOT IN SCOPE (guardrail)

### Autonomy Guardrails
- [x] **Q6:** What should the autonomous system NOT do without human approval?
  - [x] Spend money (ads/promotion) - **BLOCKED**
  - [x] Respond to user replies/DMs - **BLOCKED**
  - [ ] Post content that mentions specific prices/predictions - ALLOWED
  - [ ] Change posting frequency beyond thresholds - ALLOWED

---

## Epic Output Folder

```
ep_strategy_warehouse_marketing/
├── solution/           # Implementation code
│   ├── backend/        # Content generation, scheduling, connectors
│   ├── frontend/       # Landing page
│   └── infrastructure/ # Docker, setup scripts
├── verification/       # Screenshots, test evidence
└── workstreams/
    ├── A/              # Content Pipeline
    ├── B/              # Social Distribution
    ├── C/              # Landing Page
    ├── D/              # Orchestration
    └── Z/              # Infrastructure
```

---

## Workstream Decomposition

### WORKSTREAM Z - INFRASTRUCTURE (Priority 1)
**Goal:** Provide one-command setup for local development and deployment.
**Agent:** gemini

| Seq | Task ID | Task | Depends On | Blocks | Readiness |
|-----|---------|------|------------|--------|-----------|
| 1.1 | Z1 | Create automated setup script | none | 2.1, 2.2, 2.3, 2.4, 3.1 | ready |
| 1.2 | Z2 | Create Docker Compose configuration | none | 2.1, 2.2, 2.3, 2.4, 3.1 | ready |
| 1.3 | Z3 | Create environment template and README | none | 2.1, 2.2, 2.3 | ready |
| 1.4 | Z4 | Create health check endpoint | 1.1, 1.2 | 4.1 | blocked |

#### TASK Z1: Create Automated Setup Script

**Purpose:** Provide one-command setup for local development environment.

**Input:** None (foundation task)

**Output:**
- `ep_strategy_warehouse_marketing/setup.sh` - Unix/Mac setup script
- `ep_strategy_warehouse_marketing/setup.bat` - Windows setup script

**Verification:**
- [ ] Running `./setup.sh` on clean machine installs all dependencies
- [ ] Script creates required directories and configuration files
- [ ] Script starts application server on configured port
- [ ] Script outputs clear success/failure message with next steps

**Evidence-Type:** test_output, log_output
**Auto-Acceptance:** true

---

#### TASK Z2: Create Docker Compose Configuration

**Purpose:** Enable containerized deployment of all services.

**Input:** None (foundation task)

**Output:**
- `ep_strategy_warehouse_marketing/docker-compose.yml`
- `ep_strategy_warehouse_marketing/Dockerfile`

**Verification:**
- [ ] `docker-compose up` starts all required services
- [ ] Services communicate correctly within container network
- [ ] Health checks pass for all containers

**Evidence-Type:** test_output, log_output
**Auto-Acceptance:** true

---

#### TASK Z3: Create Environment Template and README

**Purpose:** Document all configuration and setup instructions.

**Input:** None (foundation task)

**Output:**
- `ep_strategy_warehouse_marketing/.env.example`
- `ep_strategy_warehouse_marketing/README.md`

**Verification:**
- [ ] All required environment variables documented with descriptions
- [ ] README contains install steps, env vars, API docs, usage examples
- [ ] Quick start guide enables setup in under 5 minutes

**Evidence-Type:** file_output
**Auto-Acceptance:** true

---

#### TASK Z4: Create Health Check Endpoint

**Purpose:** Provide operational health monitoring for all services.

**Input:**
- Z1: Setup script (services must be running)
- Z2: Docker configuration

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/routes/healthRoutes.py`
- `/health` endpoint returning service status

**Verification:**
- [ ] GET /health returns 200 when all services operational
- [ ] Returns degraded status when optional services unavailable
- [ ] Returns failure status when critical services down

**Evidence-Type:** test_output
**Auto-Acceptance:** true

---

### WORKSTREAM A - CONTENT PIPELINE
**Goal:** Transform Strategy Warehouse data into publishable marketing content.
**Agent:** claude

| Seq | Task ID | Task | Depends On | Blocks | Readiness |
|-----|---------|------|------------|--------|-----------|
| 2.1 | A1 | Define publishable content schema | 1.1, 1.2, 1.3 | 2.2, 2.3, 2.4 | blocked |
| 2.2 | A2 | Build content generation service | 2.1 | 3.1 | blocked |
| 2.3 | A3 | Create content queue and scheduling engine | 2.1 | 4.1 | blocked |
| 2.4 | A4 | Implement content variation / A-B testing | 2.1, 2.2 | 4.2 | blocked |

#### TASK A1: Define Publishable Content Schema

**Purpose:** Define the data structures for all marketing content types.

**Input:**
- Strategy Warehouse signal data format (TBD after Q2 clarification)
- Performance metrics format

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py`
- `publishable_content_schema.json`

**Fields:**
- content_id: UUID
- content_type: enum (signal_alert, performance_summary, strategy_ranking, educational)
- headline: string (max 100 chars for Twitter)
- body: string (max 280 chars for Twitter, longer for other platforms)
- media_urls: list[string] (optional images/charts)
- hashtags: list[string]
- call_to_action: string
- landing_page_url: string
- created_at: timestamp
- scheduled_for: timestamp
- platform_variants: dict[platform, variant_content]

**Verification:**
- [ ] Schema validates all required content types
- [ ] Schema enforces platform-specific constraints (char limits)
- [ ] Schema documented with examples

**Required Skills:**
- `skills/workstream-task-lifecycle/SKILL.md` - Follow lifecycle format

**Evidence-Type:** file_output, test_output
**Auto-Acceptance:** true

---

#### TASK A2: Build Content Generation Service

**Purpose:** Generate marketing content from Strategy Warehouse data.

**Input:**
- A1: Content schema definitions
- Strategy Warehouse data API (TBD)

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/templates/` - Content templates

**Action:**
- Implement signal-to-content transformer
- Implement performance-to-content transformer
- Implement strategy ranking content generator
- Add template engine for content variation

**Verification:**
- [ ] Generate valid signal alert content from sample data
- [ ] Generate valid performance summary from sample data
- [ ] All generated content passes schema validation
- [ ] Content includes appropriate hashtags and CTAs

**Required Skills:**
- `skills/strategy-battle-punchy-updates/SKILL.md` - Use punchy, action-oriented language
- `skills/workstream-task-lifecycle/SKILL.md` - Follow lifecycle format

**Evidence-Type:** test_output, file_output
**Auto-Acceptance:** true

---

#### TASK A3: Create Content Queue and Scheduling Engine

**Purpose:** Queue and schedule content for automated posting.

**Input:**
- A1: Content schema definitions

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/services/contentQueueService.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/models/ContentQueue.py`

**Action:**
- Implement priority queue for pending content
- Implement scheduled posting logic
- Implement rate limiting per platform
- Add retry logic for failed posts

**Verification:**
- [ ] Content can be queued with future scheduled time
- [ ] Queue respects platform rate limits
- [ ] Failed posts are retried with exponential backoff
- [ ] Queue state persists across restarts

**Evidence-Type:** test_output, log_output
**Auto-Acceptance:** true

---

#### TASK A4: Implement Content Variation / A-B Testing

**Purpose:** Generate and track content variants for optimization.

**Input:**
- A1: Content schema (platform_variants field)
- A2: Content generation service

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/services/contentVariationService.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/models/ContentVariant.py`

**Action:**
- Implement variant generation (headline, CTA, hashtag variations)
- Implement A-B assignment logic
- Track variant performance metrics
- Feed results back to content generation

**Verification:**
- [ ] Generate 2-3 variants per content piece
- [ ] Track which variant was posted to which platform
- [ ] Record engagement metrics per variant
- [ ] Variants are statistically valid (no systematic bias)

**Evidence-Type:** test_output, log_output
**Auto-Acceptance:** true

---

### WORKSTREAM B - SOCIAL DISTRIBUTION
**Goal:** Connect to social platforms and manage posting lifecycle.
**Agent:** codex

| Seq | Task ID | Task | Depends On | Blocks | Readiness |
|-----|---------|------|------------|--------|-----------|
| 2.5 | B1 | Implement Twitter/X connector | 1.1, 1.2, 1.3 | 2.11, 2.12, 2.13, 3.1, 4.1 | blocked |
| 2.6 | B2 | Implement Discord connector | 1.1, 1.2, 1.3 | 2.11, 2.12, 2.13 | blocked |
| 2.7 | B3 | Implement Telegram connector | 1.1, 1.2, 1.3 | 2.11, 2.12, 2.13 | blocked |
| 2.8 | B4 | Implement LinkedIn connector | 1.1, 1.2, 1.3 | 2.11, 2.12, 2.13 | ready |
| 2.9 | B5 | Implement Reddit connector | 1.1, 1.2, 1.3 | 2.11, 2.12, 2.13 | blocked |
| 2.10 | B6 | Implement TikTok connector | 1.1, 1.2, 1.3 | 2.11, 2.12, 2.13 | blocked |
| 2.11 | B7 | Build posting rules engine | 2.5-2.10 | 4.1 | blocked |
| 2.12 | B8 | Create engagement tracking collector | 2.5-2.10 | 4.2 | blocked |
| 2.13 | B9 | Implement follower/reach metrics collector | 2.5-2.10 | 4.2 | blocked |

#### TASK B1: Implement Twitter/X Connector

**Purpose:** Enable posting to Twitter/X platform via API.

**Input:**
- Z1, Z2, Z3: Infrastructure setup
- Twitter Developer Account credentials (BLOCKER - external dependency)

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/connectors/twitterConnector.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/models/TwitterAuth.py`

**Action:**
- Implement OAuth 2.0 authentication flow
- Implement tweet posting (text, media, threads)
- Implement rate limit handling (15 requests/15min window)
- Implement error handling and retry logic

**Verification:**
- [ ] Successfully authenticate with Twitter API
- [ ] Post text-only tweet
- [ ] Post tweet with image attachment
- [ ] Handle rate limit gracefully (queue, not crash)
- [ ] Log all API interactions for debugging

**Required Skills:**
- `skills/workstream-task-lifecycle/SKILL.md` - Follow lifecycle format

**Evidence-Type:** test_output, log_output
**Auto-Acceptance:** true

---

#### TASK B2: Implement Discord Connector

**Purpose:** Enable posting to Discord channels via webhook or bot.

**Input:**
- Z1, Z2, Z3: Infrastructure setup
- Discord webhook URL or bot token (BLOCKER - external dependency)

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/connectors/discordConnector.py`

**Action:**
- Implement webhook-based posting (simpler)
- Implement rich embed formatting
- Implement rate limit handling

**Verification:**
- [ ] Post message to Discord channel via webhook
- [ ] Post rich embed with title, description, image
- [ ] Handle rate limits gracefully

**Evidence-Type:** test_output, log_output
**Auto-Acceptance:** true

---

#### TASK B3: Implement Telegram Connector

**Purpose:** Enable posting to Telegram channels via bot API.

**Input:**
- Z1, Z2, Z3: Infrastructure setup
- Telegram bot token (BLOCKER - external dependency)

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/connectors/telegramConnector.py`

**Action:**
- Implement bot API authentication
- Implement channel posting
- Implement formatted message support (Markdown)
- Implement rate limit handling

**Verification:**
- [ ] Post message to Telegram channel
- [ ] Post message with inline keyboard buttons
- [ ] Handle rate limits gracefully

**Evidence-Type:** test_output, log_output
**Auto-Acceptance:** true

---

#### TASK B4: Implement LinkedIn Connector

**Purpose:** Enable posting to LinkedIn for professional audience reach.

**Input:**
- Z1, Z2, Z3: Infrastructure setup
- LinkedIn API credentials (BLOCKER - external dependency)

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/connectors/linkedinConnector.py`

**Action:**
- Implement OAuth 2.0 authentication flow
- Implement post creation (text, images, articles)
- Implement company page posting
- Implement rate limit handling

**Verification:**
- [ ] Successfully authenticate with LinkedIn API
- [ ] Post text update to company page
- [ ] Post with image attachment
- [ ] Handle rate limits gracefully

**Evidence-Type:** test_output, log_output
**Auto-Acceptance:** true

---

#### TASK B5: Implement Reddit Connector

**Purpose:** Enable posting to Reddit for community engagement.

**Input:**
- Z1, Z2, Z3: Infrastructure setup
- Reddit API credentials (BLOCKER - external dependency)

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/connectors/redditConnector.py`

**Action:**
- Implement OAuth 2.0 authentication
- Implement subreddit posting
- Implement comment posting
- Implement karma and rate limit handling
- Respect subreddit rules and posting frequency

**Verification:**
- [ ] Successfully authenticate with Reddit API
- [ ] Post to designated subreddit
- [ ] Handle rate limits and karma requirements
- [ ] Log all API interactions

**Evidence-Type:** test_output, log_output
**Auto-Acceptance:** true

---

#### TASK B6: Implement TikTok Connector

**Purpose:** Enable video content posting to TikTok for viral reach.

**Input:**
- Z1, Z2, Z3: Infrastructure setup
- TikTok for Business API credentials (BLOCKER - external dependency)

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/connectors/tiktokConnector.py`

**Action:**
- Implement OAuth 2.0 authentication
- Implement video upload API
- Implement caption and hashtag formatting
- Implement rate limit handling
- Note: May require video generation service (A5)

**Verification:**
- [ ] Successfully authenticate with TikTok API
- [ ] Upload video with caption
- [ ] Apply hashtags correctly
- [ ] Handle rate limits gracefully

**Evidence-Type:** test_output, log_output
**Auto-Acceptance:** true

---

#### TASK B7: Build Posting Rules Engine

**Purpose:** Define and enforce posting rules across all 6 platforms.

**Input:**
- B1-B6: All platform connectors (Twitter, Discord, Telegram, LinkedIn, Reddit, TikTok)

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/services/postingRulesService.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/config/posting_rules.yaml`

**Action:**
- Implement timing rules (best times to post per platform)
- Implement frequency rules (max posts per day per platform)
- Implement content rules (hashtag limits, mention limits)
- Implement guardrail rules (content approval thresholds)

**Verification:**
- [ ] Rules prevent posting outside configured windows
- [ ] Rules enforce daily post limits
- [ ] Rules add required hashtags/mentions
- [ ] Guardrails block posts that need human approval

**Evidence-Type:** test_output, file_output
**Auto-Acceptance:** true

---

#### TASK B8: Create Engagement Tracking Collector

**Purpose:** Collect engagement metrics from posted content across all platforms.

**Input:**
- B1-B6: All platform connectors

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/services/engagementTrackerService.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/models/EngagementMetric.py`

**Action:**
- Poll Twitter API for tweet metrics (likes, retweets, replies)
- Poll Discord for message reactions
- Poll Telegram for message views
- Poll LinkedIn for post impressions and engagement
- Poll Reddit for upvotes, comments, karma
- Poll TikTok for views, likes, shares
- Store metrics with content_id foreign key

**Verification:**
- [ ] Collect metrics for posted tweets after 1hr, 24hr
- [ ] Store metrics in persistent database
- [ ] Handle API errors gracefully (don't lose data)

**Evidence-Type:** test_output, log_output
**Auto-Acceptance:** true

---

#### TASK B9: Implement Follower/Reach Metrics Collector

**Purpose:** Track account-level growth metrics across all platforms.

**Input:**
- B1-B6: All platform connectors

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/services/accountMetricsService.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/models/AccountMetric.py`

**Action:**
- Poll follower/subscriber counts daily per platform
- Poll impressions/reach weekly per platform
- Calculate growth rates per platform and aggregate
- Store historical data for trending
- Track: Twitter followers, Discord members, Telegram subscribers, LinkedIn followers, Reddit karma/subscribers, TikTok followers

**Verification:**
- [ ] Record daily follower count per platform
- [ ] Calculate week-over-week growth percentage
- [ ] Store 90 days of historical data
- [ ] Generate aggregate cross-platform metrics

**Evidence-Type:** test_output, log_output
**Auto-Acceptance:** true

---

### WORKSTREAM C - LANDING PAGE & CONVERSION
**Goal:** Build the subscriber capture funnel.
**Agent:** claude

| Seq | Task ID | Task | Depends On | Blocks | Readiness |
|-----|---------|------|------------|--------|-----------|
| 3.1 | C1 | Design and build landing page | 1.1, 1.2, 1.3, 2.1, 2.5 | 3.2 | blocked |
| 3.2 | C2 | Build subscription capture flow | 3.1 | 3.3 | blocked |
| 3.3 | C3 | Implement subscriber database | 3.2 | 4.2 | blocked |
| 3.4 | C4 | Create conversion tracking | 3.1, 3.2 | 4.2 | blocked |
| 3.5 | C5 | Build subscriber growth dashboard | 3.3, 3.4 | none | blocked |

#### TASK C1: Design and Build Landing Page

**Purpose:** Create a high-converting landing page for Strategy Warehouse.

**Input:**
- A1: Content schema (for value prop messaging)
- B1: Twitter connector (for social proof embed)
- Z1, Z2, Z3: Infrastructure

**Output:**
- `ep_strategy_warehouse_marketing/solution/frontend/` - React + Vite project
- `ep_strategy_warehouse_marketing/solution/frontend/src/pages/LandingPage.tsx`
- `ep_strategy_warehouse_marketing/start_landing_page.bat`

**Route:** `/` (root)

**Components:**
- Hero section with value proposition
- Social proof section (testimonials, metrics)
- Feature highlights
- Call-to-action subscription form
- Footer with legal/compliance

**Verification:**
- [ ] Navigate to http://localhost:3000/
- [ ] Page loads in under 2 seconds
- [ ] Mobile responsive (375px viewport)
- [ ] CTA button prominent and clickable
- [ ] Screenshot captured showing full page

**Required Skills:**
- `skills/skills-main/skills/frontend-design/SKILL.md` - Distinctive design, avoid generic aesthetics
- `skills/skills-main/skills/web-artifacts-builder/SKILL.md` - React + Vite + Tailwind setup
- `skills/ui-delivery-viewability/SKILL.md` - Starter script and screenshot evidence

**Evidence-Type:** url, screenshot, demo
**Auto-Acceptance:** false (user-visible, requires manual verification)

---

#### TASK C2: Build Subscription Capture Flow

**Purpose:** Capture subscriber email and preferences.

**Input:**
- C1: Landing page

**Output:**
- `ep_strategy_warehouse_marketing/solution/frontend/src/components/SubscriptionForm.tsx`
- `ep_strategy_warehouse_marketing/solution/backend/src/routes/subscriptionRoutes.py`

**Action:**
- Implement email capture form with validation
- Implement double opt-in flow (email confirmation)
- Implement preference selection (signal types, frequency)
- Handle form submission and success/error states

**Verification:**
- [ ] Submit email via form
- [ ] Receive confirmation email (mock in test)
- [ ] Form validates email format
- [ ] Form shows success message after submission
- [ ] Screenshot of subscription flow captured

**Required Skills:**
- `skills/ui-delivery-viewability/SKILL.md` - Screenshot evidence

**Evidence-Type:** demo, screenshot, test_output
**Auto-Acceptance:** false (user-visible, requires manual verification)

---

#### TASK C3: Implement Subscriber Database

**Purpose:** Store and manage subscriber lifecycle.

**Input:**
- C2: Subscription capture flow

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/models/Subscriber.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/services/subscriberService.py`
- `ep_strategy_warehouse_marketing/schema/subscribers.sql`

**Fields:**
- subscriber_id: UUID
- email: string (unique, indexed)
- status: enum (pending, confirmed, unsubscribed)
- preferences: jsonb
- source: string (utm_source tracking)
- created_at: timestamp
- confirmed_at: timestamp
- unsubscribed_at: timestamp

**Verification:**
- [ ] Create new subscriber record
- [ ] Confirm subscriber via token
- [ ] Unsubscribe subscriber via token
- [ ] Query subscribers by status
- [ ] Prevent duplicate email registrations

**Evidence-Type:** test_output
**Auto-Acceptance:** true

---

#### TASK C4: Create Conversion Tracking

**Purpose:** Track visitor-to-subscriber conversion funnel.

**Input:**
- C1: Landing page
- C2: Subscription flow

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/services/conversionTrackingService.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/models/ConversionEvent.py`

**Action:**
- Track page views with source attribution (utm params)
- Track form impressions
- Track form submissions
- Track confirmation completions
- Calculate conversion rates

**Verification:**
- [ ] Record page view with utm_source
- [ ] Record form submission event
- [ ] Calculate conversion rate (submissions / views)
- [ ] Attribute conversions to traffic source

**Evidence-Type:** test_output, log_output
**Auto-Acceptance:** true

---

#### TASK C5: Build Subscriber Growth Dashboard

**Purpose:** Visualize subscriber metrics and growth trends.

**Input:**
- C3: Subscriber database
- C4: Conversion tracking

**Output:**
- `ep_strategy_warehouse_marketing/solution/frontend/src/pages/Dashboard.tsx`
- `ep_strategy_warehouse_marketing/solution/backend/src/routes/dashboardRoutes.py`

**Route:** `/dashboard` (protected)

**Components:**
- Total subscribers card
- Growth chart (daily/weekly)
- Conversion funnel visualization
- Source attribution breakdown
- Subscriber status breakdown (confirmed/pending/unsubscribed)

**Verification:**
- [ ] Navigate to http://localhost:3000/dashboard
- [ ] Dashboard shows real subscriber count
- [ ] Growth chart renders with sample data
- [ ] All charts responsive on mobile
- [ ] Screenshot captured showing dashboard

**Required Skills:**
- `skills/skills-main/skills/frontend-design/SKILL.md` - Dashboard aesthetics
- `skills/ui-delivery-viewability/SKILL.md` - Starter script and screenshot evidence

**Evidence-Type:** url, screenshot
**Auto-Acceptance:** false (user-visible, requires manual verification)

---

### WORKSTREAM D - ORCHESTRATION & AUTONOMY
**Goal:** Make the system self-running with appropriate controls.
**Agent:** gemini

| Seq | Task ID | Task | Depends On | Blocks | Readiness |
|-----|---------|------|------------|--------|-----------|
| 4.1 | D1 | Build autonomous scheduler | 1.4, 2.3, 2.5, 2.8 | 4.2, 4.3 | blocked |
| 4.2 | D2 | Create performance feedback loop | 2.4, 2.9, 2.10, 3.3, 3.4, 4.1 | none | blocked |
| 4.3 | D3 | Build manual override and kill-switch | 4.1 | 4.4 | blocked |
| 4.4 | D4 | Create weekly metrics report generator | 4.2, 4.3 | none | blocked |
| 4.5 | D5 | Implement health monitoring and alerting | 1.4, 4.1 | none | blocked |

#### TASK D1: Build Autonomous Scheduler

**Purpose:** Orchestrate all automated marketing activities.

**Input:**
- Z4: Health check endpoint
- A3: Content queue
- B1: Twitter connector
- B4: Posting rules engine

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/services/autonomousSchedulerService.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/config/scheduler_config.yaml`

**Action:**
- Implement main scheduling loop
- Coordinate content generation triggers
- Coordinate posting execution
- Coordinate metric collection
- Handle graceful shutdown

**Verification:**
- [ ] Scheduler starts automatically on system boot
- [ ] Scheduler triggers content generation on schedule
- [ ] Scheduler posts content at scheduled times
- [ ] Scheduler respects rate limits across platforms
- [ ] Scheduler stops cleanly on SIGTERM

**Evidence-Type:** log_output, test_output
**Auto-Acceptance:** true

---

#### TASK D2: Create Performance Feedback Loop

**Purpose:** Learn from engagement data to improve content.

**Input:**
- A4: Content variation service
- B5, B6: Engagement and metrics collectors
- C3, C4: Subscriber and conversion data
- D1: Autonomous scheduler

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/services/feedbackLoopService.py`

**Action:**
- Analyze engagement by content type
- Analyze engagement by posting time
- Analyze conversion by traffic source
- Generate content recommendations
- Feed recommendations to content generator

**Verification:**
- [ ] Identify top-performing content type
- [ ] Identify optimal posting windows
- [ ] Generate actionable recommendations
- [ ] Recommendations influence content generation

**Evidence-Type:** log_output, file_output
**Auto-Acceptance:** true

---

#### TASK D3: Build Manual Override and Kill-Switch

**Purpose:** Enable human control over autonomous system.

**Input:**
- D1: Autonomous scheduler

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/services/killSwitchService.py`
- `ep_strategy_warehouse_marketing/solution/frontend/src/pages/AdminPanel.tsx`

**Route:** `/admin` (protected)

**Action:**
- Implement global pause/resume control
- Implement per-platform pause control
- Implement content approval queue
- Implement emergency stop (kill all pending)
- Log all manual interventions

**Verification:**
- [ ] Pause button stops all posting immediately
- [ ] Resume button continues from queue
- [ ] Kill switch clears pending queue
- [ ] All actions logged with timestamp and user
- [ ] Screenshot of admin panel captured

**Required Skills:**
- `skills/ui-delivery-viewability/SKILL.md` - Screenshot evidence

**Evidence-Type:** demo, screenshot, test_output
**Auto-Acceptance:** false (user-visible, requires manual verification)

---

#### TASK D4: Create Weekly Metrics Report Generator

**Purpose:** Generate automated weekly performance reports.

**Input:**
- D2: Performance feedback data
- D3: Manual override controls

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/services/reportGeneratorService.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/templates/weekly_report.html`

**Action:**
- Aggregate weekly reach metrics
- Aggregate weekly subscriber growth
- Aggregate weekly conversion rates
- Generate HTML/PDF report
- Email report to stakeholders

**Verification:**
- [ ] Generate report for past 7 days
- [ ] Report includes follower growth
- [ ] Report includes subscriber growth
- [ ] Report includes conversion rates
- [ ] Report exports to PDF
- [ ] Screenshot of report captured

**Required Skills:**
- `skills/ui-delivery-viewability/SKILL.md` - Screenshot evidence

**Evidence-Type:** file_output, screenshot
**Auto-Acceptance:** false (user-visible, requires manual verification)

---

#### TASK D5: Implement Health Monitoring and Alerting

**Purpose:** Monitor system health and alert on failures.

**Input:**
- Z4: Health check endpoint
- D1: Autonomous scheduler

**Output:**
- `ep_strategy_warehouse_marketing/solution/backend/src/services/healthMonitorService.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/config/alerting_config.yaml`

**Action:**
- Monitor scheduler heartbeat
- Monitor API connector health
- Monitor queue depth and backlog
- Send alerts on failure (email, Slack, etc.)
- Track uptime metrics

**Verification:**
- [ ] Alert sent when scheduler stops unexpectedly
- [ ] Alert sent when API auth fails
- [ ] Alert sent when queue exceeds threshold
- [ ] No false-positive alerts during normal operation

**Evidence-Type:** log_output, test_output
**Auto-Acceptance:** true

---

## Dependency Graph Summary

```
Layer 1 (Foundation - Parallel):
├── Z1: Setup script
├── Z2: Docker compose
└── Z3: Env template & README

Layer 1.4:
└── Z4: Health check → depends on Z1, Z2

Layer 2 (Platform Connectors - After Infra, Parallel):
├── A1: Content schema
├── B1: Twitter connector
├── B2: Discord connector
├── B3: Telegram connector
├── B4: LinkedIn connector
├── B5: Reddit connector
└── B6: TikTok connector

Layer 2+ (Dependent Services):
├── A2: Content generation → A1
├── A3: Content queue → A1
├── A4: Content variation → A1, A2
├── B7: Posting rules → B1-B6
├── B8: Engagement tracking → B1-B6
└── B9: Account metrics → B1-B6

Layer 3 (UI & Conversion):
├── C1: Landing page → A1, B1, Z*
├── C2: Subscription flow → C1 (+ Stripe payment)
├── C3: Subscriber DB → C2
├── C4: Conversion tracking → C1, C2
└── C5: Subscriber dashboard → C3, C4

Layer 4 (Orchestration):
├── D1: Autonomous scheduler → Z4, A3, B1, B7
├── D2: Feedback loop → A4, B8, B9, C3, C4, D1
├── D3: Kill switch → D1
├── D4: Weekly reports → D2, D3
└── D5: Health monitoring → Z4, D1
```

---

## Agent Assignment Summary

| Workstream | Agent | Rationale |
|------------|-------|-----------|
| Z - Infrastructure | gemini | Backend infrastructure, Docker, DevOps |
| A - Content Pipeline | claude | Content generation, templates, creative |
| B - Social Distribution | codex | API integrations, connectors |
| C - Landing Page | claude | UI/UX, frontend, creative |
| D - Orchestration | gemini | Backend services, scheduling, monitoring |

---

## External Dependencies (BLOCKERS)

| Dependency | Required For | Status | Owner |
|------------|--------------|--------|-------|
| Twitter Developer Account | B1, B8, B9 | UNKNOWN | TBD |
| Discord Webhook/Bot Token | B2 | UNKNOWN | TBD |
| Telegram Bot Token | B3 | UNKNOWN | TBD |
| LinkedIn API Credentials | B4 | UNKNOWN | TBD |
| Reddit API Credentials | B5 | UNKNOWN | TBD |
| TikTok for Business API | B6 | UNKNOWN | TBD |
| Strategy Warehouse Data API | A1, A2 | RESOLVED | Local JSON files |
| Landing Page Domain | C1 | UNKNOWN | TBD (new domain) |
| Hosting Provider | C1 | UNKNOWN | TBD |
| Payment Processor (Stripe) | C2, C3 | UNKNOWN | TBD |
| SMTP Service (email) | C2, D4 | UNKNOWN | TBD |

---

## Success Criteria

### Launch Criteria (MVP)
- [ ] Z1-Z4 complete: Infrastructure operational
- [ ] A1-A3 complete: Content generation functional
- [ ] B1, B4 complete: Twitter posting operational
- [ ] C1-C3 complete: Landing page capturing subscribers
- [ ] D1, D3 complete: Autonomous with kill switch

### Week 1-4 Targets
| Metric | Week 1 | Week 2 | Week 3 | Week 4 |
|--------|--------|--------|--------|--------|
| Posts published | TBD | TBD | TBD | TBD |
| Impressions | TBD | TBD | TBD | TBD |
| Follower growth | TBD | TBD | TBD | TBD |
| Landing page visits | TBD | TBD | TBD | TBD |
| New subscribers | TBD | TBD | TBD | TBD |

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Twitter API rate limits / suspension | Medium | High | Conservative posting, quality content |
| Content quality insufficient | Medium | High | Human review initially, feedback loop |
| Low conversion rate | Medium | Medium | A-B testing, iterate landing page |
| Scope creep on "autonomous" | High | Medium | Explicit guardrails defined |
| Data feed unavailable | Low | High | Fallback content generation |

---

## Audit Trail

| Date | Action | Actor |
|------|--------|-------|
| 2026-03-16 13:52 | Epic created, awaiting clarifications | Claude |
| 2026-03-16 14:00 | Updated with full decomposition, dependencies, skills | Claude |
| 2026-03-16 14:15 | Clarifications resolved: All 6 platforms (+ Reddit, TikTok), Free+Paid tiers, New domain | User |
| 2026-03-16 14:15 | Added B4-B6 (LinkedIn, Reddit, TikTok), renumbered B7-B9, updated dependencies | Claude |

---

## Next Steps

1. **Owner to resolve Q1-Q6** in Clarifications Required section
2. **Owner to confirm external dependencies** (Twitter dev account, etc.)
3. **Once clarified**, decomposition generates atomic task files to `050_review`
4. **Review** approves/rejects tasks for `100_backlog/{agent}`
5. **Execution** begins with Layer 1 (Z1, Z2, Z3 in parallel)
