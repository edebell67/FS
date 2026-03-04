# Breakout: Market Narrative & Distribution Platform

**Created:** 2026-02-24
**Project:** Breakout
**Status:** Backlog

---

## 1. Objective

Generate clear, descriptive, engaging market narratives in bite-sized chunks for multi-channel distribution:
- Existing web app (TradeApps/breakout/fs)
- Mobile app (pipHunter)
- Social media platforms (X/Twitter, etc.)

---

## 2. Content Generation Engine

### Source Skills (eds/skills/)
- `strategy-boxing-battle` - Dramatic fight-style narration
- `strategy-boxing-battle-pulse` - Compact interval updates
- `strategy-battle-punchy-updates` - Short periodic battle narratives

### Narrative Components
1. **Bias Battle**: BUY vs SELL net with imbalance
2. **Momentum**: Last 30m/1hr window scores
3. **Winner Call**: Likely winner + confidence
4. **Product Impact**: Top performer, weakest performer
5. **Open Pressure**: Trade count, net exposure

### Output Formats
- Ultra-compact (social media - 280 chars)
- Compact pulse (app notifications)
- Full narrative (website news feed)

---

## 3. Distribution Strategy

### 3.1 Social Media Posts
**Content**: Summarized returns ONLY (teaser)
- Overall session performance
- Headline stats (BUY vs SELL, top performer)
- CTA: "See full battle details" → link to new website

**Restriction**: No detailed strategy names or trade-level data on public social

### 3.2 Website (Full Detail)
Link destination from social media posts

### 3.3 App Integration
- Embed narrative in existing fs dashboard
- Push to pipHunter mobile

---

## 4. New Website: Breakout Live Hub

### 4.1 Design Requirements - EXTREMELY MODERN & BEAUTIFUL
- **Premium fintech aesthetic** - world-class visual design
- News/media format (engaging, exciting)
- Mobile-first responsive
- Real-time updates with smooth transitions
- **Dark mode primary** with vibrant accent colors
- Glassmorphism / frosted glass effects
- Subtle gradients and depth
- Smooth micro-animations on all data updates
- Number counters that animate on change
- Skeleton loaders during fetch
- Typography: Modern sans-serif (Inter / SF Pro Display)
- Generous whitespace, clear visual hierarchy

### 4.2 PipHunter (PH) Brand Identity

#### Logo Concept
```
   ╔═══════════════════════════════════╗
   ║                                   ║
   ║      ┌──┐   ┌──┐                  ║
   ║      │P ├───┤H │   ⊕              ║
   ║      └──┘   └──┘                  ║
   ║                                   ║
   ║   PH monogram + crosshair motif   ║
   ║   "Precision hunting" visual      ║
   ╚═══════════════════════════════════╝
```
- **PH** bold geometric monogram
- Crosshair / target element (hunting precision)
- Scalable: favicon → hero → app icon
- Works on dark and light backgrounds

#### Color Palette
| Role | Name | Hex | Usage |
|------|------|-----|-------|
| Background | Midnight | `#0A0F1C` | Primary dark bg |
| Surface | Slate | `#141B2D` | Cards, panels |
| Surface Elevated | Steel | `#1E293B` | Modals, dropdowns |
| Border | Frost | `#334155` | Subtle borders |
| Text Primary | Snow | `#F8FAFC` | Headlines |
| Text Secondary | Silver | `#94A3B8` | Body text |
| Accent Primary | Electric Blue | `#3B82F6` | CTAs, links |
| Accent Glow | Cyan | `#06B6D4` | Highlights, focus |
| BUY / Long | Emerald | `#10B981` | Positive, gains |
| SELL / Short | Coral | `#EF4444` | Negative, losses |
| Warning | Amber | `#F59E0B` | Alerts, near-target |
| Premium | Gold | `#FBBF24` | Top performer highlight |

#### Visual Effects
- **Glassmorphism panels**: `backdrop-filter: blur(12px)` + subtle border
- **Glow effects**: Box shadows with accent colors on key metrics
- **Pulse animations**: Live data indicators
- **Target rings**: Progress towards TP shown as concentric rings
- **Crosshair cursor**: On interactive trading elements
- **Gradient text**: Headlines with subtle blue→cyan gradient
- **Particle effects**: Subtle background on hero (optional)

#### Typography Scale
```
Hero:      48-64px  - Inter Bold
H1:        32-40px  - Inter Semibold
H2:        24-28px  - Inter Semibold
H3:        18-20px  - Inter Medium
Body:      14-16px  - Inter Regular
Caption:   12px     - Inter Regular
Mono/Data: 14px     - JetBrains Mono (numbers)
```

#### Iconography
- Lucide Icons or Phosphor Icons (consistent line weight)
- Custom crosshair/target icons for PH-specific elements

#### Brand Taglines
- **Primary**: "Hunt the Edge"
- **Alt 1**: "Precision. Performance. Profit."
- **Alt 2**: "Track. Target. Trade."
- **Alt 3**: "Where Strategies Compete"

#### Brand Voice
- Confident, data-driven
- Exciting but professional
- Battle-ready energy
- Never hypey or scammy

#### Animation Guidelines
- Ease: `cubic-bezier(0.4, 0, 0.2, 1)` (smooth deceleration)
- Duration: 200-300ms for micro-interactions
- Duration: 500ms for page transitions
- Numbers should count up/down (not snap)
- Stagger list item appearances

### 4.3 Required Sections

#### A. Live Narrative Feed (Hero Section)
- Battle-style market commentary
- Auto-updating pulse narratives
- Timestamp per update
- Visual bias indicator (BUY/SELL dominance)

#### B. Top 10 Performers Leaderboard
- Rank, Strategy Name, Net Return
- Direction (BUY/SELL)
- Trade Count
- Win Rate %
- Last update timestamp
- Expandable detail on click

#### C. Last Hour Performance Summary
- Total trades closed
- Net return (last 60 mins)
- BUY vs SELL breakdown
- Top product performance
- Momentum indicator vs previous hour

#### D. Open Trades Dashboard
- Count of currently open trades
- Summarized open return (unrealized)
- % near target (within X% of TP)
- Exposure by direction
- Oldest open trade duration

#### E. Mobile App CTA
- "Get the App" prominent section
- App store links (when available)
- Feature highlights
- Battle Mode vs Signal Pro teaser

#### F. Subscribe / Notifications
- Email subscription form
- Notification preferences:
  - Daily summary
  - Major bias shifts
  - New leader alerts
  - Milestone achievements
- Future: Push notification opt-in

---

## 5. Technical Architecture

### 5.1 Data Sources
- `fs/grid_live.json` - Live rankings
- `fs/activations.json` - Active strategies
- `fs/bias_history.json` - Bias tracking
- `trade_viewer_api.py` - Existing API endpoints
- `summary_net_generator.py` - PnL aggregation

### 5.2 New Components Required

| Component | Purpose |
|-----------|---------|
| `narrative_generator.py` | AI-powered narrative generation using skills |
| `social_publisher.py` | Post to X/Twitter with rate limiting |
| `breakout_live_hub.html` | New public website |
| `subscriber_api.py` | Email capture + notification dispatch |
| `hourly_summary_api.py` | Last hour aggregation endpoint |

### 5.3 Integration Points
- Existing `trade_viewer_api.py` for data
- pipHunter Supabase for subscriber storage
- Social media APIs (X/Twitter)

---

## 6. Social Media Workflow

```
[grid_live_monitor.py]
    → detects significant event (leader change, milestone, etc.)
    → [narrative_generator.py] produces teaser + full narrative
    → [social_publisher.py] posts teaser to X/Twitter
    → teaser includes link to breakout_live_hub.html
    → website shows full detail
```

---

## 7. Privacy / Restriction Rules

| Channel | What to Show | What NOT to Show |
|---------|--------------|------------------|
| Social Media | Overall returns, bias, top performer name | Individual trade details, entry/exit prices |
| Website | Top 10 leaderboard, hourly stats, open summary | Sensitive algo parameters |
| App (authenticated) | Full detail | N/A |

---

## 8. Success Criteria

- [ ] Narrative generator produces engaging content every 15-30 mins
- [ ] Social posts drive clicks to website
- [ ] Website loads < 2 seconds, auto-refreshes
- [ ] Subscribe captures emails successfully
- [ ] Mobile CTA visible and functional
- [ ] Integration with existing fs infrastructure seamless

---

## 9. Website Deployment

### Hosting Options
| Option | Pros | Cons |
|--------|------|------|
| **Vercel** (Recommended) | Free tier, auto SSL, edge CDN, easy deploys | - |
| Netlify | Similar to Vercel, good free tier | - |
| Cloudflare Pages | Fast, free, good caching | Slightly more setup |
| GitHub Pages | Free, simple | No server-side |

### Domain
- Primary: `piphunter.io` or `piphunter.app` (to be acquired)
- Fallback: `breakout.piphunter.io` subdomain

### Deployment Pipeline
```
[Git Push] → [Vercel/Netlify Build] → [Deploy to Edge] → [Live]
```

### Requirements
- Auto-deploy on push to `main`
- Preview deployments for PRs
- SSL/HTTPS enforced
- Custom domain with DNS setup
- CDN caching for static assets
- API routes or serverless functions for:
  - Subscriber capture
  - Data proxy (if needed)

---

## 10. Dependencies

- Existing fs ranking engine (operational)
- Skills folder narrative templates (available)
- Social media API credentials (to be set up)
- Email service (to be selected - SendGrid/Resend/etc.)
- Domain name (to be acquired)
- Hosting account (Vercel/Netlify)

---

## 11. Execution Phases

### Phase 0: Brand & Design Foundation
1. Finalize PH logo (monogram + crosshair)
2. Create design system / component library
3. Set up color tokens and typography
4. Create favicon and social sharing images

### Phase 1: Website Build
5. Build `breakout_live_hub.html` with all sections
6. Implement PH brand design system
7. Wire to existing API endpoints
8. Add real-time data updates with animations

### Phase 2: Deployment
9. Acquire domain (`piphunter.io` / `.app`)
10. Set up Vercel/Netlify hosting
11. Configure DNS and SSL
12. Deploy and test live

### Phase 3: Content Engine
13. Build `narrative_generator.py` using skills templates
14. Integrate narrative feed into website
15. Test output quality and frequency

### Phase 4: Social Distribution
16. Set up X/Twitter API integration
17. Build `social_publisher.py` with rate limiting
18. Define trigger events for posting
19. Create social post templates with PH branding

### Phase 5: Engagement
20. Add subscribe functionality (Supabase)
21. Integrate mobile app CTA
22. Set up notification dispatch
23. Analytics tracking (Plausible/Vercel Analytics)

### Phase 6: Polish
24. Performance optimization (Lighthouse 90+)
25. A/B test narrative styles
26. Cross-browser/device testing

---

## References

- Skills: `eds/skills/strategy-boxing-battle*`
- Data: `TradeApps/breakout/fs/`
- Mobile: `TradeApps/breakout/piphunter/`
- pipHunter spec: `workstream/000_backlog/20260222_205900_pipHunter_signal_marketplace*`

---

## Derived Tasks

Tasks decomposed from this backlog (created 2026-02-24):

| Phase | Task | Status | Location |
|-------|------|--------|----------|
| 0 | Brand & Design Foundation | COMPLETE | `300_complete/20260224_130100_breakout_phase0_brand_design_foundation.md` |
| 1 | Website Build | COMPLETE | `300_complete/20260224_130200_breakout_phase1_website_build.md` |
| 2 | Deployment | PENDING (Manual) | `200_inprogress/20260224_130300_breakout_phase2_deployment.md` |
| 3 | Content Engine | COMPLETE | `300_complete/20260224_130400_breakout_phase3_content_engine.md` |
| 4 | Social Distribution | COMPLETE | `300_complete/20260224_130500_breakout_phase4_social_distribution.md` |
| 5 | Engagement Features | COMPLETE | `300_complete/20260224_130600_breakout_phase5_engagement.md` |
| 6 | Polish & Optimization | COMPLETE | `300_complete/20260224_130700_breakout_phase6_polish.md` |

**Total Tasks**: 7
**Completed**: 6/7 (Code complete, Phase 2 awaiting manual deployment steps)

---

## Key Deliverables Created

| Deliverable | Path | Description |
|-------------|------|-------------|
| PH Logo | `landing/assets/logo/ph-logo.svg` | PH monogram with crosshair |
| Design Tokens | `landing/styles/design-tokens.css` | Color palette, typography, spacing |
| Components | `landing/styles/components.css` | Buttons, cards, badges, tables |
| Website | `landing/breakout-live-hub.html` | Full Live Hub with API integration |
| Vercel Config | `landing/vercel.json` | Deployment configuration |
| Netlify Config | `landing/netlify.toml` | Deployment configuration |
| Deployment Guide | `landing/DEPLOYMENT.md` | Step-by-step instructions |
| Narrative Generator | `fs/narrative_generator.py` | 4 output formats (social, pulse, full, html) |
| Social Publisher | `fs/social_publisher.py` | Twitter integration with rate limiting |
| Subscriber API | `fs/subscriber_api.py` | Email subscription management |
| Supabase Schema | `landing/SUPABASE_SCHEMA.sql` | Subscriber table definition |
| Twitter Guide | `landing/TWITTER_SETUP.md` | API setup instructions |

---

## Backlog Status

**STATUS**: ACTIVE (Code Complete - Awaiting Deployment)
**Completion Criteria**: All 7 tasks must be in `300_complete` with verification passed
**Remaining Manual Steps**:
1. Domain purchase (piphunter.io / piphunter.app)
2. Vercel/Netlify deployment
3. Twitter API credentials
4. Supabase project setup
**Completion Date**: (To be filled when all tasks complete)
