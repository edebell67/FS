---
name: ep044_fix_finish_demo_template
description: Build a generic, reusable sales-demo website template for a multi-trade handyman/home-services business (handyman, painting and decorating, plumbing and drains, electrical works, gardening, kitchen fitting) when no real evidence (address/phone/name) is available yet — a clearly-marked sample identity, real verified renovation/trade photography, and a config-free single-file structure ready to be adapted per real client later. Use when asked for a handyman/trades/home-services demo or template with placeholder or missing business details, or to re-theme/duplicate this template with a new non-colliding colour scheme. Reference implementation: epics/ep_044_web_apps/fix-and-finish-handyman-template. Shared colour registry across all ep044_* sibling builds: epics/ep_044_web_apps/PALETTE_REGISTRY.md — check it before picking a palette so multiple agents building sites in this family never collide. Every build wires the shared AI assistant (epics/ep_043_AI_native_serviceand _SEO/ai_website_assistant_framework) on by default via a self-contained assistant-embed.js with a single ASSISTANT_ENABLED flag as the switch-off. Sibling skill ep044_app_nail_bar_demo_template covers the same "no evidence yet, generic template" case for nails; ep044_app_beauty_tanning_demo_template covers the real-evidenced-business pattern (ep_006/redesigns).
---

# Web App: Handyman / Multi-Trade Home Services Demo Template

Build a generic, reusable demo site for the handyman/home-services niche (handyman, painting & decorating, plumbing & drains, electrical works, gardening, kitchen fitting) when there is **no real business identified yet** — this is the "template" case, same family as `ep044_app_nail_bar_demo_template`, not the "real business" case (`ep044_app_beauty_tanning_demo_template`).

## Which skill applies — decision rule

- **All evidence fields blank/placeholder** (`????`, empty, "TBC") → this skill. Build with a clearly-fictional but realistic sample identity, place output under `epics/ep_044_web_apps/<template-name>/`.
- **Real evidence exists** (a real address, phone, niche confirmed via a citation) → use `ep044_app_beauty_tanning_demo_template`'s pattern instead and place output under `epics/ep_006_website_rebuilds/redesigns/<business-slug>/`.
- If a real handyman/trades business is identified *later*, adapt this reference build's structure/copy with the real facts rather than starting from scratch.

## Handling "use image as references" style briefs

The user may paste a handful of images directly into the chat (not files) as **mood/style reference** rather than literal assets to embed — e.g. "here's what I mean by premium bathroom renovation" or "this is the tradesperson vibe I want." You cannot extract pasted chat images to disk directly. Treat them as art direction only:
1. Describe what the reference images communicate (palette, subject matter, composition, tone) in your own words.
2. Translate that into **search terms** for the real image-sourcing workflow below (e.g. reference photos of a marble bathroom + white shaker kitchen + tradesperson in workwear + painter on a ladder → search `bathroom-renovation`, `kitchen-renovation`, `handyman`, `painter-decorator`).
3. Never claim the resulting stock photos "are" the referenced images — they're independently sourced photography matching the same mood.

## Sample identity convention

Invent a plausible-but-clearly-fictional business identity (name, address, phone, email) — realistic enough to read credibly, never presented as verified fact. Mark this explicitly with a footer disclosure line, e.g.:
`Business name, address, phone and prices are sample placeholders for this reusable template — replace with real details per client.`
No fabricated stats/ratings/years-established claims — use honest generic differentiators instead (`Fully insured`, `Free written quotes`, `Local to <area>`).

## File structure

```
epics/ep_044_web_apps/<template-name>/
├── index.html      Single file, all sections, hard-coded sample content
├── gallery.html    Dedicated editorial masonry gallery page
├── styles.css      :root tokens + every component style
└── reveal.js        Self-contained copy of the standard IntersectionObserver reveal script
```

No config.js — same reasoning as the nail bar skill: this is meant to be manually adapted per real future client, not driven by a swappable data file. `reveal.js` is a **self-contained copy**, not a shared `../reveal.js` reference (this folder has no parent-level shared script).

## Design system

- **Fonts**: `Cormorant Garamond` (serif headings) + `Outfit` (sans body/UI) + `JetBrains Mono` (eyebrows, prices) — same pairing as every sibling in this family of skills.
- **Palette — must be distinct per site, chosen via the shared registry, not hardcoded from this doc.** The reference build currently uses steel blue (`--ink: #1b2733`, `--accent: #3d6b8a`) — it originally shipped as forest green + ochre-gold, then was deliberately re-themed to steel blue on 2026-07-16 specifically so a **second** handyman/trades site could exist alongside it with its own distinct scheme. Do not copy this doc's example hex values into a new build without checking the registry first — they may already be taken by the time you read this.
  - **Selection process** (applies to every future `ep044_*` build, run by any agent/model, not just this skill): read `epics/ep_044_web_apps/PALETTE_REGISTRY.md` first, propose 2–4 candidate accent options genuinely distinct from every row in that table (not just a shade/tint of an already-used hue), apply the chosen one **only** via the site's `:root` CSS custom properties, then grep the finished file for the old hex values to catch hardcoded duplicates outside `:root` (a `radial-gradient(...rgba(...))` on a `::before`/`::after` is the easiest place to miss one — it won't update just by editing `:root`). Append the new site's row to the registry in the same turn.
  - This is how two sites in the same niche (e.g. two handyman-template builds) end up with genuinely non-colliding palettes instead of both defaulting to this doc's example colors.
- **"Lots of images" matters here too** — renovation and trade work is inherently visual proof of quality. Real, verified photography throughout: hero, both split sections, a 4-image homepage gallery preview, and a full 9–10 image editorial masonry gallery page.

## Section catalog

1. **Navbar** — brand + tagline, anchor links (Services / Renovations / General Trades), `Gallery` page link, `Get a Quote` nav-button.
2. **Hero** — eyebrow (sample location), italic-accented `<h1>`, one-sentence lede emphasising "one team, every trade" (the core handyman-niche value proposition — no chasing separate tradespeople), dual CTA (call + view services), honest trust pills (`Fully insured`, `Free written quotes`, `Local to <area>`), real hero photo.
3. **Services menu** — priced list covering all six core trades: general handyman, painting & decorating, plumbing & drains, electrical works, gardening, kitchen fitting. Price per-hour where sensible (`From £35/hr`) and "Free quote" for larger jobs (painting, kitchen fitting) rather than a misleading flat price.
4. **Two split sections** — "Kitchens & Bathrooms" (renovation-grade work: kitchen fitting, bathroom refits, tiling) vs. "General Trades" (handyman, painting, plumbing, electrical, gardening as everyday call-outs). This mirrors the real distinction handyman businesses make between big renovation jobs and quick repairs — keep both framed honestly, not inflating small jobs into "renovations."
5. **Gallery preview strip** — 4 images on the homepage linking to the full gallery.
6. **Why row** (dark section) — insurance/certification, written quotes before work starts, and "one number for every trade" are the strongest, most niche-appropriate trust points — lead with those over generic claims.
7. **Contact CTA** — dark box, call + email buttons (no fabricated live-booking system unless one is confirmed real).
8. **Footer** — brand/address, contact column, tech badge, sample-data disclosure line.
9. **`gallery.html`** — CSS `column-count` masonry, 9–10 photos captioned by category (`Kitchen` / `Bathroom` / `Painting` / `Handyman` / `Gardening` / `Studio`), exhibition-style captions (italic title + small mono category label).

## Image sourcing workflow

Same discipline as `ep044_app_nail_bar_demo_template`:
1. `WebSearch`/`WebFetch` Unsplash search pages for trade-specific themes — good queries: `kitchen-renovation`, `bathroom-renovation`, `handyman`, `painter-decorator`, `gardener-landscaping`. Never guess a `photo-<id>` from memory.
2. Skip `plus.unsplash.com` results (paid tier).
3. `curl -s -o /dev/null -w "%{http_code}" "https://images.unsplash.com/photo-<id>?auto=format&fit=crop&q=80&w=1000"` must return `200` for every candidate before it goes in HTML.
4. Check for accidental reuse across sibling sites (`grep -r "photo-<id>" epics/`).
5. Vary composition across trades deliberately — a gallery of 10 near-identical "person holding a tool" shots reads as filler; mix finished-space photography (kitchens, bathrooms) with in-progress trade shots (painting, sawing, gardening) and one or two studio/product shots (a toolkit laid out) for texture.

## Mandatory EP044 skill stack — common blueprint first

For **every** EP044 local-business category (bathrooms, carpentry/joinery, barbers, interiors, fencing, kitchens, or any later category), load and apply these in this order:

1. `ep044_common_site_blueprint/000_site_blueprint.md` — mandatory shared architecture, conversion, assistant, accessibility, privacy, SEO, legal and QA requirements.
2. The relevant `ep044_app_<category>_demo_template/<category>.md` — mandatory category-specific services, gallery, qualification data, FAQs, trust signals and CTA language.
3. Private-preview evidence boundaries — real identity facts may be used; unknown commercial facts, reviews, projects, prices, brands, coverage and guarantees must remain unclaimed until owner-confirmed.

A category skill extends the common blueprint; it **never replaces or weakens it**. Do not begin a category rebuild after loading only the category file.

## Outreach rendering gate — resolve variables before sending

Before any test or prospect email is sent, build an exact message artifact from the mail-only subject/body template (never from Markdown review metadata) and fail closed unless all checks pass:

1. Provide only declared values, e.g. `business_name` and `private_preview_url`.
2. Reject missing variables and reject any remaining `{{...}}` token in the final subject or body.
3. Verify every inserted preview URL returns HTTP 200 and belongs to the intended business slug.
4. Inspect the generated `From`, `To`, `Subject` and body artifact before delivery. Recipient, suppression and authorisation fields are separate send gates; they must not be inferred from template rendering.
5. Send only through an authenticated approved sender; record the provider result/message ID. Never report delivery from a dry run.

## Bathroom-fitter extension — extensive but compact illustrative imagery

When a real-evidenced business is categorised as **`bathroom fitters`**, use a shared bathroom-fitter design language rather than a generic trades layout:

1. **Image-first private demo:** use a premium bathroom collage as the hero/design-direction asset. Prefer one AI-generated 3×4 or 3×6 contact-sheet collage over 9–18 independent images: it provides visible range while reducing requests and page weight.
2. **Quality bar:** every panel must read as newly completed, immaculate and contemporary: no people, personal items, toiletries, clutter, wet towels, wear, dated fittings, stains, exposed pipes, unfinished work or lived-in rooms.
3. **Clear boundary:** label visible image treatment as `AI-ILLUSTRATIVE BATHROOM DIRECTIONS` and state that it is not the named business's verified work, showroom, stock, supplier range, price or availability. Never imply a generated bathroom is an actual completed project.
4. **Extensive visual presentation:** make the collage prominent in the hero and, where the page needs a gallery section, reuse it as a single low-weight visual reference rather than inventing a product catalogue. Do not claim that individual panels are selectable ranges unless owner-approved products exist.
5. **Per-site variation:** bathroom-fitters share the same gallery-led architecture but must not look cloned. Assign a distinct collage or crop/palette treatment to each site, record that assignment in an internal JSON manifest, and avoid using the same collage for adjacent previews where alternatives exist.
6. **Asset provenance:** record the generation prompt, source file, generated-date/identifier if available, and `AI-generated illustrative` classification internally. User-supplied generated assets may be embedded only after the user authorises their use. Replace all demo imagery with owner-approved project, supplier or product assets before official launch.
7. **Existing source correction:** retain the source-workbook category exactly. If an existing preview says a different trade but the workbook category is `bathroom fitters`, correct the category label, the visual page language and bounded assistant knowledge before publishing.

## Canonical bathroom-fitter site — depth first, then visual variants

Build **one deep, reusable bathroom-fitter conversion model** and apply that information architecture consistently across each fitter. Do not make every prospect a different thin landing page.

### Shared conversion structure

1. `index.html` — image-led hero, visual-direction entry point, value proposition, project-type navigation, trust/evidence area, repeated quote/survey CTA.
2. `gallery.html` — immersive inspiration and completed-project gallery. Before real assets arrive, use clearly marked AI-illustrative direction boards; after owner approval, use real gallery filters for style, room type, size and budget.
3. `services.html` — complete renovation, fitting, wet rooms, showers, tiling, plumbing, electrics, heating, design and accessibility modules. Mark each as `owner confirmation required` until evidence is supplied; never claim availability by default.
4. `process.html` — consultation, survey, design, quote, scheduling, installation and final inspection journey. Use only owner-approved operational detail in a live version.
5. `guides.html` — bathroom styles, materials, inspiration, care and planning content. This is the long-tail content/depth layer; it must be useful and clearly distinguished from verified business claims.
6. `faq.html` — timing, disruption, removal, materials, plumbing, guarantees and quotation questions. Use safe answers that defer unverified facts to owner confirmation.
7. `contact.html` — quote/survey/callback/photo-upload journey. All real capture, sending, booking and notification stays disabled until the owner authorises the workflow and privacy basis.

### Per-business variables — keep these deliberately limited

Change only the identity layer and art direction unless verified facts justify more:

- business name, initials, verified address/phone/email;
- one assigned AI collage set (light / dark / mixed);
- palette, font pairing, logo treatment and layout rhythm;
- owner-approved service scope, project images, reviews, brands, prices, coverage and warranties when they arrive.

### Assistant business value

The assistant is a **showroom and enquiry-routing layer**, not a generic chat bubble. It should be able to guide visitors through approved gallery/style/project information and route to an owner-approved consultation flow. Do not make personal behavioural claims (for example, "you seem drawn to...") or store/act on visitor behaviour without a disclosed, lawful implementation and owner approval.

## Verification

Serve locally (`python -m http.server <port>` from `ep_044_web_apps/`) and check via `javascript_tool`:
- Every `<img>` on both `index.html` and `gallery.html` has `complete: true` and `naturalWidth > 0`.
- `tel:`/`mailto:` links are consistent with the sample identity everywhere they appear (hero, contact section, footer, sticky mobile action bar).
- Section counts match intent (`service-item`, `split-item`, `why-card`, `gallery-strip-item`, `art-gallery-item`).
- Mobile nav drawer opens/closes correctly (click-based, reliable regardless of this session's known Browser-pane `requestAnimationFrame`/`IntersectionObserver` quirks — don't chase those as real bugs, see the beauty/tanning skill's note on this).

## AI assistant integration — default on, one-flag off

Every site built under this skill ships with the shared AI assistant wired in **by default**. This is a standing requirement across all `ep044_*` templates, not optional polish.

1. Create a self-contained `assistant-embed.js` in the site's own folder (same pattern as `fix-and-finish-handyman-template/assistant-embed.js`):
   ```js
   (() => {
     const ASSISTANT_ENABLED = true; // set to false to disable the assistant for this client — no HTML edits needed
     if (!ASSISTANT_ENABLED) return;
     const apiBase = String(window.<SITE>_AI_API_BASE || "https://shared-website-assistant-api.onrender.com").replace(/\/$/, "");
     const widget = document.createElement("script");
     widget.src = `${apiBase}/widget.js?v=<date>-<site>`;
     widget.dataset.client = "<publicKey>";
     widget.dataset.apiBase = apiBase;
     widget.defer = true;
     widget.onerror = () => console.warn("<Business> assistant is currently unavailable.");
     document.head.append(widget);
   })();
   ```
   The `ASSISTANT_ENABLED` flag is the entire switch-off mechanism — flipping one boolean in one file disables the assistant for a client who doesn't want it, without touching any HTML page.
2. Add `<script src="assistant-embed.js"></script>` to every **visitor-facing** page (`index.html`, `gallery.html`, …), right after the page's own scripts (`reveal.js`). Do not add it to internal/sales-only pages like an `owner-preview.html`.
3. Register the site as a tenant in `epics/ep_043_AI_native_serviceand _SEO/ai_website_assistant_framework` via its admin API — never by hand-editing `data/clients.json`. Check `curl http://127.0.0.1:4310/api/health` first (another agent may already have it running locally); otherwise `npm start` from the framework folder. `POST /api/admin/clients` with `Authorization: Bearer <ADMIN_TOKEN from .env>` and a body built from the site's own content: `businessName`/`tagline`/`logoText`/`theme` (matching the site's actual palette), `contact`, `pages` (the site's real nav anchors + keywords), `knowledge` (location/contact/services/pricing/differentiators derived from the site copy — never invent facts beyond what the site itself states), `demoWorkflows.booking` (priced services + a few slots so demo booking/payment/email/CRM actions work), `status: "demo"`, and a `deployments` entry with `status: "local"` until the site is actually pushed/hosted.
4. Verify end-to-end before calling the build done: `curl "http://127.0.0.1:4310/api/public/config?clientKey=<publicKey>&host=localhost"` resolves the new tenant, and one `POST /api/public/chat` request answers a real question grounded in the site's own knowledge (not a generic/hallucinated answer).

See the framework's own `README.md` for full API/architecture detail.

## Where output goes + task tracking

Generic template (no real business yet) → `epics/ep_044_web_apps/<template-name>/`, lowercase-hyphenated, descriptive of the sample identity or niche (e.g. `fix-and-finish-handyman-template`). If a real handyman/trades business is identified later, that becomes a new build under `epics/ep_006_website_rebuilds/redesigns/<business-slug>/` per `ep044_app_beauty_tanning_demo_template` instead — don't retrofit this generic template folder with one real client's facts. Per this repo's `CLAUDE.md`, create a workstream task file in `workstream/300_complete/claude/` once built and verified.

## Required shared layout invariant

Apply §6.4 **Mandatory page-edge and footer contract**, §6.1 **Inner-page editorial hierarchy**, and §6.2 **Gallery relevance** from `ep044_common_site_blueprint/000_site_blueprint.md` without exception. The business identity/logo block, header navigation, hero copy, page content, card/form outer edges and footer content must share one responsive left gutter. Use the normal-flow sticky-footer shell for short pages; never independently centre the header or use a fixed footer. The home hero remains the largest display moment; inner-page headings require an explicitly styled, distinct premium serif face at a smaller scale, with a compact mono kicker and restrained sans-serif lede—never browser-default inner-page text. Every gallery must contain real category-relevant visual assets, never empty cards, generic decoration or “images coming later” copy. When owner work is unavailable, use provenance-recorded, clearly labelled illustrative category imagery that does not claim work by the named business. Verify live geometry, type and image loads after cache-busting production CSS.
