---
name: Web_app_auto_garage_demo_template
description: Build a personalised, config-driven static demo website for a local service business (garage, salon, plumber, etc.) to send as a direct-sales preview link before converting to a live site. Use when asked to build a "demo website", "personalised site preview", "website redesign demo", or a business-specific site under epics/ep_006_website_rebuilds or epics/ep_044_web_apps. Reference implementation: epics/ep_044_web_apps/auto-garage-template. When building a new reusable trade template (not a batch of real outreach previews), check the shared colour registry epics/ep_044_web_apps/PALETTE_REGISTRY.md first so it doesn't collide with an existing ep044_*-family sibling. Every build wires the shared AI assistant (epics/ep_043_AI_native_serviceand _SEO/ai_website_assistant_framework) on by default via a self-contained assistant-embed.js with a single ASSISTANT_ENABLED flag as the switch-off.
---

# Web App: Local Business Demo Site Template

Build a static HTML/CSS/JS site that looks like it already belongs to a
specific local business, sent as a link in a direct-sales campaign, with a
clear path to "activate" it as the business's real website. This is the
pattern behind `epics/ep_006_website_rebuilds` (salons, barbers, garages) and
the reference build at `epics/ep_044_web_apps/auto-garage-template`.

Do **not** default to Next.js/React for this task unless explicitly asked —
this repo's convention is a zero-build static site (see
`web_apps/funcuts_homepage_redesign.html` and every folder under
`epics/ep_006_website_rebuilds/redesigns/`). Static means the demo link opens
instantly, hosts anywhere, and needs no build step for a non-technical
operator to tweak.

## Inherit the master blueprint (non-negotiable)

Build on the master blueprint `../ep044_common_site_blueprint/000_site_blueprint.md` — load it first and treat it as authoritative for the **common page architecture** (blueprint Section 2/3) and the **premium visual system** (blueprint Section 6: the fixed `Cormorant Garamond` + `Outfit` + `JetBrains Mono` pairing, the single shared **relative** modular type scale, the per-page **image matrix**, and the `:root` look-and-feel tokens), alongside trust, conversion, SEO, accessibility and performance. The category-specific detail in this skill **extends** the blueprint and must never drop below its Section 14 definition of done — no thin, image-poor screens. Where this skill already names fonts, image counts, or sourcing steps, they match the blueprint's shared system; keep them aligned rather than divergent.

## Before building: clarify scope

If any of these are ambiguous, ask (don't assume):
- **Target**: a specific real business (name/location/trade already known,
  e.g. from `epics/ep_006_website_rebuilds/operations/candidate_search`) vs.
  a generic reusable template with sample/placeholder data.
- **Where it lives**: a specific candidate's folder under
  `epics/ep_006_website_rebuilds/redesigns/<business-slug>/` (real outreach
  target) vs. a new template under `epics/ep_044_web_apps/<name>/` (reusable
  starting point for a trade not yet templated).
- **Stack**: static HTML/CSS/JS (default) vs. a framework, if the user's
  brief explicitly asks for React/Next.js/component reuse across many sites.

## Architecture: one config file drives everything

Never hard-code business data (name, phone, services, reviews, colours,
hours) directly into HTML or CSS. All of it lives in a single
`assets/js/config.js` with these objects, populated at runtime by
`assets/js/main.js`:

- `businessConfig` (or `garageConfig`, `salonConfig`, etc.) — identity,
  contact, hours, brand colours, stats, about copy, trust indicators,
  why-choose-us, social links, booking/payment links, SEO fields, and a
  `demoMode: true` flag.
- `servicesData` — array of service cards.
- `reviewsData` — array of reviews, each flagged `placeholder: true` until
  replaced with genuine ones.
- `galleryData` — array of `{ category, caption }` (see Images below).
- `offersData` — array with an `enabled` toggle per offer.
- Trade-specific extras as needed (e.g. `diagnosticSymptoms` for a garage's
  "what's wrong with my vehicle?" tool, `paymentProducts` for a payment demo
  grid).

`main.js` binds this data two ways:
1. **Static text/links** — elements tagged `[data-cfg="key"]` /
   `[data-cfg-href="key"]` get their `textContent` / `href` set from a flat
   `bindings` object built from the config at load time.
2. **Repeated content** — dedicated `render*()` functions
   (`renderServices()`, `renderReviews()`, `renderGallery()`, …) build
   innerHTML from the data arrays into named container elements
   (`#servicesGrid`, `#reviewsTrack`, …).

This means rebranding for a new business touches **only `config.js`** (plus
the CSS `:root` colour variables, which should mirror the config colours).

## Standard file structure

```
<business-or-template-name>/
├── index.html            Homepage, all sections, data-page="home"
├── owner-preview.html    /owner-preview route — sales conversion page, data-page="owner"
├── serve_site.bat         Local static server helper (python -m http.server <port>)
├── README.md              Personalisation checklist + deployment steps
└── assets/
    ├── css/styles.css    Design system + every component style
    └── js/
        ├── config.js     SINGLE SOURCE OF TRUTH — see above
        └── main.js       Icon system, config bindings, renderers, interactions
```

Mirror this exactly — it's what makes the next business's version a
copy-and-edit-config job instead of a rebuild.

## Standard homepage section catalog

Header (sticky, mobile drawer) → Hero (headline + dual CTA + trust line) →
Trust strip (icon row) → Services grid → Interactive tool panel (tabbed:
quote form / trade-specific engagement tool e.g. diagnostic or symptom
picker / booking calendar) → Why-choose-us → About + animated stats counters
→ Specialism/brand badges → Offers → Gallery (filterable + lightbox) +
before/after slider → Video slot → Review carousel → Payment demo grid → FAQ
accordion → Contact + map + form → Owner activation band → Footer → sticky
mobile action bar (call/message/book/directions) → cookie banner.

Not every business needs every section (a salon doesn't need a "diagnostic
symptom picker") — adapt the tool panel and specialism/offer content to the
trade, keep the rest of the skeleton.

## Visual direction

Load the `frontend-design` skill (or the project's `design-taste-frontend` /
`high-end-visual-design` skill) before styling. Pick ONE bold, trade-
appropriate aesthetic and commit — do not default to purple-gradient-on-
white or an Inter/Roboto/Space Grotesk font stack. For the garage reference
build: graphite/steel base, workshop-amber + diagnostic-blue accents,
Unbounded (display) + Plus Jakarta Sans (body) + IBM Plex Mono (data/mono
accents). A salon, plumber, or café should land on a completely different
palette and type pairing — vary it per trade and per business.

**If you're building a new reusable trade template** (a sibling to
`auto-garage-template`/`bloom-nail-bar-template`/`fix-and-finish-handyman-template`
under `epics/ep_044_web_apps/<name>/`, not a one-off real-business outreach
preview), read `epics/ep_044_web_apps/PALETTE_REGISTRY.md` first — the shared
cross-agent registry of every `ep044_*`-family site's `--ink`/`--accent`
values. Propose 2–4 candidate palettes genuinely distinct from every row (not
just a shade/tint of an already-used hue), apply the chosen one only via the
site's CSS custom properties, grep the finished file for any hardcoded
duplicate of an old/placeholder colour (a `radial-gradient`/`box-shadow`
using a raw rgba is the easiest place to miss one), then append the new
site's row to the registry in the same turn. The high-volume "Batch variation
rule" below is a separate concern — it governs rotating palettes across many
*real* outreach candidates, which don't need registry entries since each is
already distinct by business data.

Avoid stock photography and invented claims. Use generative CSS/SVG
placeholder panels (gradient block + icon + a visible "placeholder" caption)
for hero/about/gallery/video imagery instead of fake or generic photos.
Mark every unverified number (years trading, vehicles/clients served,
rating, review content) with a `placeholder: true` flag in the config and a
visible "sample" label in the UI — never present invented stats as fact.

### Batch variation rule

Do **not** use the same colour palette, hero treatment, or visual rhythm for
every business in a batch. Repeated colours make the previews feel mass-
generated and destroy the personalised-owner effect. For every candidate,
derive a distinct-but-controlled theme from the business/trade data:

- rotate accent palettes (e.g. amber/graphite, blue/steel, green/charcoal,
  red/black, teal/navy) while keeping garage credibility;
- vary the initials/emblem shape and recognition-card layout;
- vary hero microcopy and service emphasis using business name, area, phone,
  and source evidence;
- keep interaction structure consistent, but vary surface styling so two
  previews side-by-side do not look cloned.

### Owner-recognition visuals, not generic AI filler

For outreach previews, the page must make the owner think "that's my business"
within 3 seconds. Generic AI garage/salon/plumber images are not enough.
Create a business-specific recognition block/card from verified public data:

- exact business name and short initials/emblem;
- exact address/postcode/area;
- phone/email when verified;
- stylised map/location card using coordinates when available;
- service category matched to the trade;
- a visible note that imagery is a custom non-copied preview, not official
  branding.

Do **not** copy Google Maps, Google Business Profile, Street View, Facebook,
Instagram, directory, or owner website images into a preview page unless the
user explicitly says it is for internal review only. For owner outreach, use
Google/Maps imagery only as a reference to build a clearly original visual
layout (SVG/CSS illustration, map-pin card, identity panel). Prefer
OpenStreetMap embeds for location recognition when coordinates exist.

If real owner photos/logos are needed, ask the owner to approve or supply them
after they engage. Do not present generated initials/emblems as a real logo.

### Extract business artefacts from Google/Maps screenshots — reference only

When the user provides a Google Maps / Street View / Google Business Profile
screenshot to make a preview recognisable, treat it as **reference material**,
not a usable image asset. The goal is to extract safe business-specific
artefacts and recreate them, never to crop, embed, trace, or copy the Google
screenshot itself.

Workflow:
1. Inspect the screenshot only to identify factual/brand cues:
   - exact visible business name / wordmark text;
   - tagline or category text visible on signage;
   - rough colour palette (e.g. charcoal fascia + gold lettering);
   - simple logo/icon concept (e.g. sunburst, wrench, shield, initials);
   - storefront recognition cues such as sign layout, window-label themes,
     address, phone, service words.
2. Record these as text notes in the working brief or config, not as copied
   pixels. Example: `brandCue: "gold sunburst mark + HOXTANS wordmark on dark
   fascia"`.
3. Recreate an original artefact with CSS/SVG/HTML:
   - original initials/emblem or simplified icon inspired by the category;
   - recreated wordmark text using web fonts, not an image crop;
   - palette tokens derived from observed colours, not sampled/cropped image
     files;
   - storefront/identity panel built from CSS shapes and verified text.
4. Add a visible or internal note where appropriate:
   `Business artefacts recreated for preview; no Google imagery used.`
5. Verify before publishing:
   - no Google screenshot/image file is copied into the project;
   - no `googleusercontent`, `gstatic`, `maps.googleapis`, Street View, or
     copied screenshot path appears in HTML/CSS/JS;
   - the page still contains the real business identifiers needed for owner
     recognition.

Allowed: using the screenshot to understand text, colours, layout and simple
brand cues. Not allowed: screenshot crops, direct logo/photo extraction from
Google imagery, pixel tracing, or presenting recreated marks as official logos.

## Icon system (avoid this exact mistake)

Build a small inline-SVG icon library keyed by name inside `main.js`
(`ICONS = { name: "<path d>", ... }` + an `icon(name)` helper). **Do not**
write `${icon('name')}`-style JS template-literal syntax directly inside a
static `.html` file — it is not a templating context and will render as
literal text. Instead:
- In JS-built content (inside `render*()` template literals), call
  `icon('name')` directly — it returns real `<svg>` markup.
- In hand-written static HTML, use a placeholder element —
  `<span class="icon-inline" data-icon="name"></span>` — and resolve all of
  them at load time with a `renderInlineIcons()` pass over
  `[data-icon]`. Expose it as `window.renderInlineIcons` so any page that
  injects new `data-icon` elements after load (e.g. `owner-preview.html`'s
  checklist) can re-resolve them.

If you do introduce the `${icon...}` mistake, `grep -c '\${icon' *.html`
should return 0 before calling the build done.

## Demo mode & the owner-preview page

`demoMode: true` in the config means: forms show an in-page "thank you, this
is a demonstration" message instead of sending data; payment buttons open a
"demonstration only, no card details collected" modal; a discreet banner
links to `owner-preview.html`. `owner-preview.html` lists three lanes —
already demonstrated / required before launch / optional enhancements — plus
an activation CTA, and must **not** show pricing unless explicitly told to.

**Known pitfall**: if `main.js` sets `document.title` /
`<meta name="description">` from the config unconditionally, it will
clobber `owner-preview.html`'s own `<title>` on load (both pages share the
same script). Scope any document-level overwrite to
`document.body.dataset.page === "home"`, and give `owner-preview.html`
`data-page="owner"`.

## Verification

The Browser pane's `navigate` tool generally refuses `file://` URLs — serve
the folder locally first (`python -m http.server <port>` from the site
folder, or the bundled `serve_site.bat`) and preview `http://localhost:<port>/`.

Prefer DOM/JS assertions over trusting a visual screenshot alone:
`javascript_tool` calls counting rendered items per section
(`document.querySelectorAll('#servicesGrid .service-card').length` etc.,
compared against the config array lengths), simulated clicks on every
interactive control (tabs, gallery lightbox open/close, FAQ accordion,
mobile nav, payment modal), and a full empty-submit → filled-submit cycle on
every form to confirm validation and the demo success message reference the
business name. If the screenshot/zoom tool times out (including on a
trivial blank test page — a sign it's an infra issue, not a page bug), note
that explicitly rather than silently skipping visual proof, and fall back to
the DOM-assertion approach above.

## AI assistant integration — default on, one-flag off

Every site built under this skill ships with the shared AI assistant wired in
**by default** (see `auto-garage-template/assistant-embed.js` for the
reference implementation). This is a standing requirement across all
`ep044_*` templates and real-business builds alike, not optional polish.

1. Create a self-contained `assistant-embed.js` in the site's own folder —
   dynamically injects `widget.js` from the shared Render-hosted service,
   guarded by a single `const ASSISTANT_ENABLED = true;` flag at the top.
   That flag **is** the switch-off mechanism: flipping it to `false` disables
   the assistant for a client who doesn't want it, with no HTML edits needed.
2. Add `<script src="assistant-embed.js"></script>` to every visitor-facing
   page (e.g. `index.html`). Do **not** add it to `owner-preview.html` or
   other internal/sales-only pages — the widget is for the site's visitors,
   not the internal conversion page.
3. Register the site as a tenant in
   `epics/ep_043_AI_native_serviceand _SEO/ai_website_assistant_framework`
   via its admin API — never by hand-editing `data/clients.json`. Check
   `curl http://127.0.0.1:4310/api/health` first (another agent may already
   have it running); otherwise `npm start` from the framework folder.
   `POST /api/admin/clients` with `Authorization: Bearer <ADMIN_TOKEN from
   .env>` and a body built from the site's own config data
   (`businessName`/`tagline`/theme colours/contact from `config.js`,
   `pages` matching the real nav anchors, `knowledge` derived from
   `servicesData` and the site's real copy — never invent facts beyond what
   the config already states), `demoWorkflows.booking` seeded from
   `servicesData`'s priced items, `status: "demo"`, and a `deployments`
   entry with `status: "local"` until actually hosted.
4. Verify before calling the build done:
   `curl "http://127.0.0.1:4310/api/public/config?clientKey=<publicKey>&host=localhost"`
   resolves the tenant, and one `POST /api/public/chat` request returns an
   answer genuinely grounded in the site's own knowledge.

This applies to both the batch real-outreach case and the new-reusable-template
case — every business gets an assistant by default; only the palette
distinctness rule above is scoped differently between those two cases.

## Where output goes + task tracking

- A specific real outreach candidate → its own folder under
  `epics/ep_006_website_rebuilds/redesigns/<business-slug>/`, matching
  siblings like `fun-cuts/`, `chapter-barbers/`.
- A new reusable trade template (not tied to one real business) →
  `epics/ep_044_web_apps/<template-name>/`, matching
  `auto-garage-template/`.

Per this repo's `CLAUDE.md`, every qualifying change needs a workstream task
file (see the `workstream-task-lifecycle` skill) — create it directly in
`workstream/300_complete/claude/` once built and verified, with the Evidence
section citing the DOM-assertion/form-cycle checks above.

## Required shared layout invariant

Apply §6.4 **Mandatory page-edge and footer contract**, §6.1 **Inner-page editorial hierarchy**, and §6.2 **Gallery relevance** from `ep044_common_site_blueprint/000_site_blueprint.md` without exception. The business identity/logo block, header navigation, hero copy, page content, card/form outer edges and footer content must share one responsive left gutter. Use the normal-flow sticky-footer shell for short pages; never independently centre the header or use a fixed footer. The home hero remains the largest display moment; inner-page headings require an explicitly styled, distinct premium serif face at a smaller scale, with a compact mono kicker and restrained sans-serif lede—never browser-default inner-page text. Every gallery must contain real category-relevant visual assets, never empty cards, generic decoration or “images coming later” copy. When owner work is unavailable, use provenance-recorded, clearly labelled illustrative category imagery that does not claim work by the named business. Verify live geometry, type and image loads after cache-busting production CSS.
