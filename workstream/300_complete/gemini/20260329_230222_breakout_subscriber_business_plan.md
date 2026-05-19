Source: Direct user request in chat on 2026-03-29.

Task Summary: Review weekly top-100 breakout strategy JSON outputs under `TradeApps/breakout/fs/json/live/{product_type}/stats/weekly`, understand the data structure and commercial potential, and produce a concrete plan to turn the data into a subscriber business within one month, including productization, webpage, and marketing workstreams.

Context:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\weekly`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\metals\stats\weekly`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\crypto\stats\weekly`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\indices\stats\weekly`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\energy\stats\weekly`

Dependency: None

Plan:
- [x] 1. Inspect the weekly JSON folders and confirm schema, cadence, and usable commercial signals by product type.
  - [x] Test: Run PowerShell directory and JSON sampling commands; pass if product folders, weekly files, and core fields are confirmed.
  - Evidence: Confirmed `live/{forex,metals,crypto,indices,energy}/stats/weekly` plus weekly JSON schema containing `target_date`, `week_start`, `week_end`, `dates_included`, `is_full_week`, and `top_strategies[]` with `strategy`, `daily`, `total_net`, and `total_trades`.
- [x] 2. Quantify the opportunity in the data by extracting top-level metrics that support product design.
  - [x] Test: Run a local analysis command over the JSON files; pass if each product type has a clear summary of file availability and representative top strategy metrics.
  - Evidence: Captured per-product file counts, strategy counts, and top-performer summaries for the latest full-week files dated `2026-03-23.json`.
- [x] 3. Define monetizable offers, pricing ladder, positioning, and compliance-aware go-to-market strategy.
  - [x] Test: Produce a written plan in this lifecycle file; pass if at least three viable offers, target audiences, pricing assumptions, and acquisition channels are specified.
  - Evidence: Added sections `Data Understanding`, `Recommended Commercial Model`, `Pricing`, `Positioning`, `Website`, `Marketing`, and `Compliance`.
- [x] 4. Produce a 30-day execution roadmap covering website, automation, content, conversion, and delivery operations.
  - [x] Test: Produce a dated execution plan; pass if week-by-week deliverables, dependencies, and success metrics are specified.
  - Evidence: Added section `30-Day Execution Plan` with weekly milestones, ownership focus, and launch targets.

## Data Understanding
- Each product folder stores weekly JSON snapshots keyed by week start date.
- The latest full-week files observed are for `2026-03-23` through `2026-03-29`.
- Structure is consistent enough to support automation, ranking pages, downloadable reports, and member dashboards.
- The data is not raw tick data; it is already productized performance output. That is commercially valuable because customers care about ranked decisions, not raw backtest plumbing.

### Latest Full-Week Snapshot Summary
| Product | Weekly files seen | Strategies in latest full week | Highest-ranked strategy observed | Weekly net | Trades |
|---|---:|---:|---|---:|---:|
| forex | 11 | 1000 | `GBPAUD_C | breakout_2_tp20.0_sl5.0` | 2735.00 | 63 |
| metals | 3 | 505 | `SI | breakout_R_2_tp20.0_sl5.0` | 42140.00 | 502 |
| crypto | 5 | 768 | `XRP | breakout_R_Rev_2_tp20.0_sl5.0` | 6615.00 | 167 |
| indices | 3 | 698 | `NQ | breakout_R_2_tp20.0_sl5.0` | 15560.00 | 242 |
| energy | 4 | 503 | `CL | breakout_2_tp20.0_sl5.0` | 8895.00 | 161 |

### What The Data Means Commercially
- `forex` is broad and retail-friendly. It is best for a high-volume subscriber offer because the symbol set is familiar and diverse.
- `indices` and `metals` show the strongest headline performance numbers. They are best for premium positioning and ad creatives because they look differentiated.
- `crypto` supports a seven-day content cadence and is ideal for Telegram, Discord, and social content because the audience expects frequent updates.
- `energy` is narrower but useful as a specialist add-on tier for serious traders.
- Because rankings are weekly and strategy-specific, the strongest business is not generic education. The strongest business is a recurring intelligence product.

## Recommended Commercial Model
### Recommended Brand Direction
- Position the business as a `weekly breakout intelligence platform` rather than a promise-based signal seller.
- Sell `ranked research, model watchlists, and execution-ready setups`.
- Avoid language that implies guaranteed returns, managed accounts, or regulated investment advice.

### Best Initial Product Stack
1. **Free Lead Magnet: Weekly Breakout Leaderboard**
- Public page and email newsletter showing the top 10 strategies across all product types for the week.
- Purpose: SEO, social proof, email capture, and low-friction top-of-funnel.

2. **Core Subscription: Breakout Pro**
- Daily watchlist by product type.
- Weekly ranked top 100 report.
- Entry/exit profile summary per strategy family.
- Downloadable CSV/JSON plus commentary.
- Delivery via member website plus email.

3. **Premium Subscription: Breakout Desk**
- Everything in Pro.
- Telegram or Discord alerts for the current watchlist.
- Short daily regime note: what to focus on, what to avoid, which product types are dominant.
- Friday wrap-up with next-week watchlist.

4. **B2B / Licensing**
- API or flat-file feed for creators, small prop desks, educators, and signal resellers.
- This is likely the highest-margin path once the consumer offer proves demand.

### Why This Product Mix Fits The Data
- The JSON already contains ranked strategy outputs, which naturally become a leaderboard, watchlist, and member report.
- The data spans multiple product types, allowing bundle pricing and cross-sell.
- The availability of per-day contributions inside each weekly record allows narrative content such as “what worked on Tuesday vs Thursday,” which improves retention.

## Pricing
### Recommended Initial Pricing
- Free: weekly leaderboard + email signup.
- Pro: `£29/month` or `£290/year`.
- Desk: `£99/month` or `£990/year`.
- B2B license: start at `£500-£1,500/month` depending on redistribution rights and update frequency.

### Revenue Target For Month One
- Minimum viable target: 50 Pro subscribers = `~£1,450 MRR`.
- Strong early target: 25 Pro + 10 Desk = `~£1,715 MRR`.
- Stretch target with one B2B pilot: `£2,200-£3,200 MRR`.

## Positioning
### Target Customers
- Self-directed retail traders who want a structured watchlist instead of random ideas.
- Existing signal buyers who are dissatisfied with opaque Telegram groups.
- Trading educators and creators who need ranked content to discuss each week.
- Semi-professional traders who want a cross-asset breakout ranking feed.

### Messaging Angle
- “See which breakout models are leading this week before the crowd rotates.”
- “Cross-asset weekly rankings for forex, metals, crypto, indices, and energy.”
- “Research-grade model leaderboards, not noisy chatroom guesses.”

### Trust Builders
- Show transparent weekly snapshots and archive history.
- Show per-product methodology summary in plain English.
- Publish a public sample report every week.
- Include clear risk disclaimer and “education / research only” language in the footer and checkout flow.

## Website
### Minimum Viable Website To Launch In 30 Days
- Landing page.
- Public weekly leaderboard page.
- Pricing page.
- Sample report page.
- Checkout.
- Member dashboard with latest weekly report and downloadable files.

### Landing Page Structure
1. Hero:
- Headline: `Weekly breakout rankings across forex, metals, crypto, indices, and energy.`
- Subhead: `Get the market’s strongest model setups in one subscriber dashboard.`
- CTA 1: `View This Week's Leaderboard`
- CTA 2: `Start Pro Trial`

2. Proof section:
- Cards showing the latest top-ranked strategy per product type.
- Archive count and weekly update cadence.

3. How it works:
- We rank.
- We publish.
- You review the watchlist and execute with your own risk controls.

4. Product comparison:
- Free vs Pro vs Desk.

5. Sample report:
- Teaser screenshot and downloadable example.

6. FAQ:
- What is included.
- How often it updates.
- Is this financial advice.
- Who it is for.

7. Footer:
- Disclaimer, terms, privacy, contact.

### Stack Recommendation
- Frontend: Next.js landing and member site.
- Auth: simple email/password or Clerk.
- Payments: Stripe subscriptions.
- Storage: the existing JSON files transformed into normalized tables or cached API responses.
- Automation: daily and weekly content generation jobs from the JSON folders.

## Marketing
### Fastest Acquisition Channels
1. X / Twitter:
- Daily chart-card posts by product type.
- Weekly “top 10 breakout leaderboard” thread.

2. Email newsletter:
- Weekly free report every Sunday night or Monday morning.
- Upsell to full ranked report and daily watchlist.

3. Telegram / Discord:
- Free channel for summary posts.
- Paid channel for premium watchlist notes.

4. SEO:
- Public archive pages by week, product type, and strategy family.
- This compounds over time and is supported by your existing JSON history.

5. Affiliates / creators:
- Give finance creators a custom referral code for Pro and Desk.

### Content Engine
- Weekly flagship content: “Top breakout strategies this week.”
- Daily content: “Today’s focus product type.”
- Comparative content: “Forex vs indices this week.”
- Educational content: “How to read a breakout watchlist without overtrading.”

## Compliance
- Keep all copy in research, analytics, and watchlist language.
- Do not promise profits or “best trades.”
- Include visible disclaimer that the service is for informational and educational purposes and users make their own trading decisions.
- Before scaling paid acquisition, have the copy and subscription flow reviewed for the jurisdictions you care about most.

## 30-Day Execution Plan
### Week 1: Offer And Funnel Foundation
- Finalize brand, positioning, disclaimer language, and pricing.
- Normalize JSON ingestion into one API-ready structure.
- Build landing page wireframe and public leaderboard template.
- Set up Stripe products and email capture.
- Success target: landing page live with waitlist and sample leaderboard.

### Week 2: Subscriber Product Build
- Build member dashboard.
- Add weekly report pages and downloads.
- Add admin process to publish each week’s report from the JSON.
- Create one free sample report and one premium sample report.
- Success target: a user can sign up, pay, and access the latest report.

### Week 3: Content And Launch Prep
- Create 14 days of scheduled social posts.
- Launch email welcome sequence.
- Open free Telegram or Discord channel.
- Publish the first public weekly leaderboard and route traffic to checkout.
- Success target: first 100 email subscribers and first 10 paying users.

### Week 4: Launch And Iterate
- Run a public launch campaign across X, email, and community channels.
- Add urgency with founding-member pricing.
- Track signup rate, trial-to-paid conversion, churn signals, and top-visited pages.
- Start outbound for 10 B2B prospects using the archive and sample feed.
- Success target: 25-50 paying users and one live B2B conversation.

## Immediate Build Sequence After This Plan
1. Create the public landing page and leaderboard.
2. Create a transformation script that turns the weekly JSON into page-ready data.
3. Create the Stripe-backed pricing and checkout flow.
4. Create the member dashboard and report archive.
5. Create the content automation for weekly email and social posts.

## Implementation Log
- 2026-03-29 23:02:22 Created lifecycle task file in backlog for the subscriber business planning request.
- 2026-03-29 23:06:00 Confirmed live weekly folders for `forex`, `metals`, `crypto`, `indices`, and `energy`.
- 2026-03-29 23:08:00 Sampled weekly JSON structure and confirmed consistent commercial fields across product types.
- 2026-03-29 23:10:00 Extracted latest full-week strategy counts and leading strategy metrics for each product type.
- 2026-03-29 23:18:00 Wrote commercialization model, pricing, website, marketing, compliance, and 30-day launch plan.
## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\gemini\20260329_230222_breakout_subscriber_business_plan.md`
  - Objective-Proved: The full subscriber-business plan, offer design, pricing, website scope, marketing strategy, and execution roadmap were documented in one lifecycle file.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: PowerShell inspection output confirming folders `live/{forex,metals,crypto,indices,energy}/stats/weekly` and JSON keys `target_date`, `week_start`, `week_end`, `dates_included`, `is_full_week`, `top_strategies.strategy`, `top_strategies.daily`, `top_strategies.total_net`, `top_strategies.total_trades`.
  - Objective-Proved: The business plan is grounded in the actual source data structure and update cadence.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: PowerShell summary output for latest full-week files dated `2026-03-23.json` showing strategy counts and leaders: forex `1000`, metals `505`, crypto `768`, indices `698`, energy `503`.
  - Objective-Proved: Product opportunities and pricing were based on observed coverage breadth and product-type differentiation.
  - Status: captured

## Changes Made
- Added lifecycle file `C:\Users\edebe\eds\workstream\200_inprogress\gemini\20260329_230222_breakout_subscriber_business_plan.md`.
- Added data-backed business analysis, offer design, pricing, website scope, marketing plan, compliance notes, and a 30-day execution plan.

## Validation
- Ran PowerShell inspection to confirm product folders under `TradeApps/breakout/fs/json/live`.
- Ran PowerShell sampling of `2026-03-23.json` for `forex` and `crypto` to confirm weekly schema and top strategy objects.
- Ran PowerShell summarization to extract per-product latest full-week file counts, strategy counts, and leading strategy metrics.
- Validation result: pass. The commercialization plan is grounded in the observed data and current file structure.

## Risks/Notes
- Commercialization of trading-related outputs may require careful disclaimer language and jurisdiction-specific compliance review.
- The initial deliverable is a business and execution plan. Separate implementation tasks should be created for the public website, subscriber dashboard, payment flow, and content automation.
- The largest practical risk is not data availability. It is trust, positioning, and compliance copy. That should be handled before paid traffic.

## Completion Status
- Complete on 2026-03-29 23:18:00. Auto-acceptance criteria met with objective-delivery coverage at 100%.
