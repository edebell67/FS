---
name: Web_app_beauty_tanning_demo_template
description: Build a personalised sales-demo website for a real beauty, tanning, nails, lashes, or spa business, following this repo's established epics/ep_006_website_rebuilds/redesigns/ pattern (real Unsplash photography, single index.html + styles.css, shared reveal.js). Use when asked to build a demo/redesign site for a named salon, tanning studio, or beauty business with real evidence (address/phone/niche). Reference implementation: epics/ep_006_website_rebuilds/redesigns/hoxtans. Shared colour registry across all ep044_*-family builds: epics/ep_044_web_apps/PALETTE_REGISTRY.md — check it before picking a signature accent so multiple agents building sites in this family never collide. Every build wires the shared AI assistant (epics/ep_043_AI_native_serviceand _SEO/ai_website_assistant_framework) on by default via a self-contained assistant-embed.js with a single ASSISTANT_ENABLED flag as the switch-off. Sibling skill Web_app_auto_garage_demo_template covers the no-stock-photo, config-driven template pattern for generic reusable industry templates instead.
---

# Web App: Beauty & Tanning Salon Demo Site

Build a real, personalised sales-demo site for a specific beauty/tanning/nails/lashes business, matching the visual and technical convention already established across `epics/ep_006_website_rebuilds/redesigns/` (siblings: `fun-cuts`, `daksheens-hair-beauty`, `chapter-barbers`, `hoxtans`, …). This is a **different, lighter pattern** than `Web_app_auto_garage_demo_template` — no config.js, no owner-preview route, no demo-mode flag, and it uses real stock photography rather than generative CSS panels. Don't mix the two conventions.

## Inherit the master blueprint (non-negotiable)

Build on the master blueprint `../ep044_common_site_blueprint/000_site_blueprint.md` — load it first and treat it as authoritative for the **common page architecture** (blueprint Section 2/3) and the **premium visual system** (blueprint Section 6: the fixed `Cormorant Garamond` + `Outfit` + `JetBrains Mono` pairing, the single shared **relative** modular type scale, the per-page **image matrix**, and the `:root` look-and-feel tokens), alongside trust, conversion, SEO, accessibility and performance. The category-specific detail in this skill **extends** the blueprint and must never drop below its Section 14 definition of done — no thin, image-poor screens. Where this skill already names fonts, image counts, or sourcing steps, they match the blueprint's shared system; keep them aligned rather than divergent.

## Before building: locate existing research

Real candidates in this pipeline are usually already researched. Check, in order:
1. `epics/ep_006_website_rebuilds/previews/batch_*/<business-slug>/` — a lightweight auto-generated single-file "batch preview" may already exist with real evidence (address, phone, niche, source citation like "Bing Maps result: ..."). Read it for verified facts before inventing anything.
2. `epics/ep_006_website_rebuilds/operations/site_research/` and `candidate_search/` — deeper research notes if present.
3. `epics/ep_006_website_rebuilds/redesigns/DESIGN.md` — the aesthetic system all redesigns must follow.

Only use facts you actually have evidence for (address, phone, email, niche). Do not invent specific opening hours, years-in-business, review counts, or star ratings that aren't evidenced — either omit them, use honest generic differentiators ("walk-ins welcome", "central location", "evening appointments"), or phrase it as "call to confirm" rather than stating a fabricated fact as if it were true.

## File structure (matches every sibling redesign)

```
redesigns/<business-slug>/
├── index.html      Single file, all sections, hard-coded content (no config.js)
└── styles.css       :root tokens + every component style
```
References `../reveal.js` (shared, do not copy) for scroll-triggered reveal animation.

## Design system (per `redesigns/DESIGN.md`)

- **Fonts**: `Cormorant Garamond` (serif, headings — heritage/craftsmanship) + `Outfit` (sans, body/UI) + `JetBrains Mono` (eyebrows, prices, mono labels). Load via the same Google Fonts `<link>` pattern every sibling uses.
- **Signature accent colour**: one colour per business, tailored to the name/vibe — never reuse a sibling's exact accent hex. Before picking, read `epics/ep_044_web_apps/PALETTE_REGISTRY.md` (the shared cross-agent registry of every `ep044_*`-family site's `--ink`/`--accent` values — includes `hoxtans` = copper `#c1622b` plus the auto-garage, nail bar, and handyman templates); propose 2–4 candidate hexes genuinely distinct from every row (not just a shade/tint of an already-used hue) and pick the one that best fits the business's specific niche (e.g. a tanning studio reads well in warm copper/terracotta, not cool tones). Apply the choice only via the site's `:root` CSS custom properties, then grep the finished file for any old/placeholder hex to catch hardcoded duplicates outside `:root` (a `radial-gradient`/`box-shadow` using a raw rgba is the easiest place to miss one). Append the new site's row to the registry in the same turn.
- **Background**: `#FAFAFA`/`#FFFDFC`-ish warm-neutral canvas, white surface cards, ultra-soft shadows (`0 10px 40px rgba(*, 0.05–0.08)`), never a stock `box-shadow` default.
- **Real photography, not placeholders**: DESIGN.md explicitly calls for "large, high-quality placeholder imagery (via Unsplash/Picsum)" — unlike the auto-garage template, stock photos are the right call here. See sourcing workflow below.
- **Sticky glassmorphism navbar**: `position: sticky; backdrop-filter: blur(10px); background: rgba(bg, 0.85–0.9)`.
- **`.reveal` / `.reveal.active`** scroll-in classes wired by the shared `../reveal.js` (`IntersectionObserver`, threshold 0.1). Reuse the class, don't reinvent it.
- **Footer "tech badge"**: a small `✓ Modern Web Standard / Optimized for Speed & Mobile` card — the sales-framing device this pipeline uses instead of the auto-garage template's `demoMode`/owner-preview machinery.

## Business artefact extraction from Google/Maps screenshots — reference only

For beauty/tanning previews, owner recognition matters more than generic stock
beauty imagery. If the user provides a Google Maps, Street View, or Google
Business Profile screenshot, use it only as **reference material** to extract
business-specific artefacts. Do **not** copy, crop, embed, trace, or otherwise
reuse the Google screenshot or any Google-hosted image.

Extract safe artefacts as notes:
- exact business name / wordmark text visible on signage;
- tagline or service/category text such as `TANNING & BEAUTY`;
- high-level palette cues such as charcoal fascia, gold lettering, pink neon,
  cream walls, etc.;
- simple icon concept such as sunburst, initials, leaf, scissors, nail mark;
- storefront recognition cues such as sign layout, window labels, address,
  phone, opening/service words.

Then recreate original preview assets:
- CSS/SVG-style emblem or sunburst built from shapes, not image crops;
- text wordmark rendered with web fonts, not a copied logo image;
- palette tokens derived from observed brand direction;
- CSS storefront/identity panel using verified text and service labels;
- visible/internal note: `Business artefacts recreated for preview; no Google
  imagery used.`

Before publishing, verify:
- no Google screenshot file was copied into the site folder;
- no `googleusercontent`, `gstatic`, `maps.googleapis`, Street View URL, or
  cached screenshot path appears in HTML/CSS/JS;
- the page still contains enough real business identifiers for the owner to
  recognise it quickly.

Allowed: using the screenshot to understand text, colours, layout and simple
brand cues. Not allowed: screenshot crops, direct logo/photo extraction from
Google imagery, pixel tracing, or implying a recreated mark is the official
logo unless the owner supplied/approved it.

## Section catalog for this niche

Adapt from the reference (`hoxtans`) rather than copying `fun-cuts`/`daksheens` verbatim — pick the categories that fit the actual business:

1. **Navbar** — brand name + one-line niche tagline, 2 category anchor links + a booking `nav-button`.
2. **Hero** — eyebrow (real address), `<h1>` with an italicised `<span class="accent">` word, one-sentence lede, dual CTA (`tel:` call as primary, an in-page anchor as secondary), a row of honest trust pills (no fabricated stats), and a real hero photo in a rounded `hero-image-wrapper`.
3. **Services menu** — a priced list (`service-item` = title + one-line description + price), styled as a menu, not a grid of cards. Keep prices realistic for the niche and mark them "From £X" unless you have an exact evidenced price.
4. **Split category sections** (2, alternating image side via `.split-item.reverse`) — the core storytelling device. For a tanning/beauty business: Tanning vs. Beauty. For a hair/beauty business: Hair vs. Beauty. For nails/lashes: adapt names accordingly. Each has an eyebrow, `<h2>`, one paragraph, a 4-item `feature-list`, and a real photo.
5. **Gallery strip** (new addition beyond the older siblings, used in `hoxtans`) — 3 square images in a grid with a small caption overlay (`.gallery-item .cap`), for texture and to show more of the space/products without another full section.
6. **Why row** — 2–4 short honest differentiators (location, walk-ins, evening hours), not a fabricated stats/counter row.
7. **Contact CTA** — dark full-bleed box, call + email/directions buttons, real address as `cta-meta`.
8. **Footer** — brand + address, contact column, tech badge, copyright line.

## Image sourcing workflow (do this every time — don't guess photo IDs)

1. **Search, don't recall.** Use `WebSearch` for `site:unsplash.com <theme>` or the niche term, then `WebFetch` the resulting Unsplash collection/search page with a prompt asking it to list the actual `images.unsplash.com/photo-...` URLs and descriptions shown on the page. Never type a `photo-<id>` from memory — IDs are effectively random and unguessable.
2. **Skip `plus.unsplash.com` results** — those are paid Unsplash+ photos, not free-tier.
3. **Verify every URL before writing it into HTML**: `curl -s -o /dev/null -w "%{http_code}" "https://images.unsplash.com/photo-<id>?auto=format&fit=crop&q=80&w=800"` must return `200`. Do this for the whole shortlist in one batch before picking final images.
4. **Check for accidental reuse** — `grep -r "photo-" epics/ep_006_website_rebuilds/redesigns/*/index.html` and avoid picking an ID a sibling already uses, so each business's page feels distinct.
5. If the Browser pane's `navigate`/`preview_start` is declined or unavailable for browsing Unsplash directly, `WebSearch` + `WebFetch` is the fallback path — it doesn't need the Browser pane at all.

## Verification

Serve the `redesigns/` folder locally (`python -m http.server <port>` from that directory, so `../reveal.js` resolves for the business subfolder) and check via `javascript_tool`:
- Every `<img>` has `complete: true` and `naturalWidth > 0` (confirms the Unsplash URLs actually loaded, not just returned 200 on a HEAD request).
- `tel:`/`mailto:` links have the correct evidenced phone/email.
- Section counts match what you intended (`service-item`, `split-item`, `gallery-item`, `why-item`).

**Known false alarm**: this Browser pane environment can report `window.innerHeight === 0` even after `resize_window`, which makes `IntersectionObserver`-based `.reveal` sections never gain `.active` (they'll sit at `opacity: 0` in this tool even though the exact same shared `reveal.js` works fine in a real browser for every sibling redesign already in production). Don't "fix" `reveal.js` chasing this — confirm it's the same shared script and move on. If screenshot/zoom tools also time out (seen in this same class of environment), fall back to `read_page` / `get_page_text` / DOM assertions for verification instead of visual proof.

## AI assistant integration — default on, one-flag off

Every site built under this skill ships with the shared AI assistant wired in **by default** (see `epics/ep_044_web_apps/Hoxtans_ai/assistant-embed.js` for the reference implementation). This is a standing requirement across all `ep044_*`-family builds, not optional polish.

1. Create a self-contained `assistant-embed.js` in the site's own folder — dynamically injects `widget.js` from the shared Render-hosted service, guarded by a single `const ASSISTANT_ENABLED = true;` flag at the top. That flag **is** the switch-off mechanism: flipping it to `false` disables the assistant for a client who doesn't want it, with no HTML edits needed.
2. Add `<script src="assistant-embed.js"></script>` to every page, right after `reveal.js`.
3. Register the business as a tenant in `epics/ep_043_AI_native_serviceand _SEO/ai_website_assistant_framework` via its admin API — never by hand-editing `data/clients.json`. Check `curl http://127.0.0.1:4310/api/health` first (another agent may already have it running); otherwise `npm start` from the framework folder. `POST /api/admin/clients` with `Authorization: Bearer <ADMIN_TOKEN from .env>` and a body built only from **real, evidenced** facts already established for this build: real contact details, real `pages` anchors, `knowledge` entries drawn from the actual verified content (never invent hours/prices/claims that weren't already evidenced for the site itself), `demoWorkflows.booking` seeded from the site's real service menu, `status: "demo"`, and a `deployments` entry matching whatever the site's actual deployment `status` already is (`local`/`github`/`github+render`/`demo`/`live`).
4. Verify before calling the build done: `curl "http://127.0.0.1:4310/api/public/config?clientKey=<publicKey>&host=localhost"` resolves the tenant, and one `POST /api/public/chat` request returns an answer genuinely grounded in the business's real knowledge.

## Where output goes + task tracking

Real candidate → `epics/ep_006_website_rebuilds/redesigns/<business-slug>/`, matching sibling naming (lowercase, hyphenated). Per this repo's `CLAUDE.md`, create a workstream task file in `workstream/300_complete/claude/` once built and verified.

## Required shared layout invariant

Apply §6.4 **Mandatory page-edge and footer contract**, §6.1 **Inner-page editorial hierarchy**, and §6.2 **Gallery relevance** from `ep044_common_site_blueprint/000_site_blueprint.md` without exception. The business identity/logo block, header navigation, hero copy, page content, card/form outer edges and footer content must share one responsive left gutter. Use the normal-flow sticky-footer shell for short pages; never independently centre the header or use a fixed footer. The home hero remains the largest display moment; inner-page headings require an explicitly styled, distinct premium serif face at a smaller scale, with a compact mono kicker and restrained sans-serif lede—never browser-default inner-page text. Every gallery must contain real category-relevant visual assets, never empty cards, generic decoration or “images coming later” copy. When owner work is unavailable, use provenance-recorded, clearly labelled illustrative category imagery that does not claim work by the named business. Verify live geometry, type and image loads after cache-busting production CSS.
