---
name: ep044_app_nail_bar_demo_template
description: Build a generic, reusable sales-demo website template for a nail bar / nail salon business (manicures, pedicures, gel, acrylics, nail art) when no real evidence (address/phone/name) is available yet — a clearly-marked sample identity, real verified nail-industry photography, and a config-free single-file structure ready to be adapted per real client later. Use when asked for a nail salon demo/template with placeholder or missing business details. Reference implementation: epics/ep_044_web_apps/bloom-nail-bar-template. Shared colour registry across all ep044_*-family builds: epics/ep_044_web_apps/PALETTE_REGISTRY.md — check it before picking a palette so multiple agents building sites in this family never collide. Every build wires the shared AI assistant (epics/ep_043_AI_native_serviceand _SEO/ai_website_assistant_framework) on by default via a self-contained assistant-embed.js with a single ASSISTANT_ENABLED flag as the switch-off. Sibling skill ep044_app_beauty_tanning_demo_template covers the real-evidenced-business pattern (ep_006/redesigns) for tanning/beauty/hair; this skill is for the no-evidence-yet, reusable-template case specifically for nails.
---

# Web App: Nail Bar / Nail Salon Demo Template

Build a generic, reusable demo site for the nail bar/nail salon niche when there is **no real business identified yet** (address, phone, email, name all unknown or placeholder). This is the "template" case, not the "real business" case — see the decision rule below before picking this skill over `ep044_app_beauty_tanning_demo_template`.

## Inherit the master blueprint (non-negotiable)

Build on the master blueprint `../ep044_common_site_blueprint/000_site_blueprint.md` — load it first and treat it as authoritative for the **common page architecture** (blueprint Section 2/3) and the **premium visual system** (blueprint Section 6: the fixed `Cormorant Garamond` + `Outfit` + `JetBrains Mono` pairing, the single shared **relative** modular type scale, the per-page **image matrix**, and the `:root` look-and-feel tokens), alongside trust, conversion, SEO, accessibility and performance. The category-specific detail in this skill **extends** the blueprint and must never drop below its Section 14 definition of done — no thin, image-poor screens. Where this skill already names fonts, image counts, or sourcing steps, they match the blueprint's shared system; keep them aligned rather than divergent.

## Which skill applies — decision rule

- **All evidence fields blank/placeholder** (`????`, empty, "TBC") → this skill. Build with a clearly-fictional but realistic sample identity, place output under `epics/ep_044_web_apps/<template-name>/`.
- **Real evidence exists** (a real address, phone, niche confirmed via a Bing Maps result or similar citation) → use `ep044_app_beauty_tanning_demo_template`'s pattern instead and place output under `epics/ep_006_website_rebuilds/redesigns/<business-slug>/`.
- If a real nail bar is identified *later* for this same template, adapt this reference build's structure/copy with the real facts rather than starting from scratch — swap the sample identity, keep the section catalog and image-sourcing discipline.

## Sample identity convention

Invent a plausible-but-clearly-fictional business identity (name, address, phone, email) — realistic enough that the demo doesn't feel like a broken form, but never presented as verified fact. Mark this explicitly:
- A footer line: `Business name, address, phone and prices are sample placeholders for this reusable template — replace with real details per client.`
- No fabricated star ratings, review counts, or "X years established" claims — this niche doesn't need them to look credible; honest trust pills (`Walk-ins welcome`, `Evening appointments`, `Central <area>`) do the job instead, same as the real-business pattern.

## File structure

```
epics/ep_044_web_apps/<template-name>/
├── index.html      Single file, all sections, hard-coded sample content
├── gallery.html    Dedicated editorial masonry gallery page (see below)
├── styles.css      :root tokens + every component style
└── reveal.js        Self-contained copy of the standard IntersectionObserver reveal script
```

No config.js — this niche's whole value is the photography and section structure, not swappable data-driven config. Adapting for a real client later means editing the hardcoded text/images directly in this reference build, same as every `ep_006/redesigns` sibling.

`reveal.js` is a **self-contained copy** here (not a shared `../reveal.js` reference), since this folder has no parent-level shared script the way `ep_006/redesigns/` does — copy the standard script verbatim, don't reinvent it.

## Design system

- **Fonts**: `Cormorant Garamond` (serif headings) + `Outfit` (sans body/UI) + `JetBrains Mono` (eyebrows, prices) — same pairing as every sibling in this family of skills.
- **Palette**: the reference build uses dusty rose/mauve (`#C9708A`) + a warm gold secondary accent for "why us" moments, warm cream/blush base (`#FCF6F3`), deep plum-black ink for dark sections (`#2B1E22`) — but don't copy these hexes into a new build without checking first. Read `epics/ep_044_web_apps/PALETTE_REGISTRY.md` (the shared cross-agent registry of every `ep044_*`-family site's `--ink`/`--accent` values) before picking, propose 2–4 candidate hexes genuinely distinct from every row (not just a shade/tint of an already-used hue), apply the choice only via `:root` CSS custom properties, grep the finished file for old/placeholder hex values to catch hardcoded duplicates outside `:root`, then append the new site's row to the registry in the same turn. This is how two nail-bar-template builds end up with genuinely non-colliding palettes instead of both defaulting to this doc's example colours.
- **"Lots of images" is the point of this niche** — nails is a visually-driven business; don't economise on photography the way the auto-garage template deliberately avoids stock photos. Real, verified Unsplash photography throughout: hero, both split sections, a 4-image gallery preview strip on the homepage, and a full 8–10 image editorial masonry gallery page.

## Section catalog

1. **Navbar** — brand name + tagline, anchor links to Services/Manicure/Pedicural sections, `Gallery` page link, `Book Now` nav-button. Sticky glassmorphism (`backdrop-filter: blur`).
2. **Hero** — eyebrow (sample location), italic-accented `<h1>`, one-sentence lede, dual CTA (call + view services), honest trust pills, real hero photo (rounded, `aspect-ratio: 4/5`).
3. **Services menu** — priced list covering the core nail-salon menu: classic manicure, gel manicure, classic pedicure, acrylic extensions, nail art (often priced *per hand* or *per nail*, distinct from other beauty niches), gel removal/rebalance. "From £X" pricing.
4. **Two split sections** (Hands / Feet, i.e. Manicure vs. Pedicure) — the storytelling core, each with eyebrow/h2/paragraph/4-item feature list/real photo, alternating image side via `.split-item.reverse`.
5. **Gallery preview strip** — 4 images on the homepage linking to the full gallery page.
6. **Why row** (dark section) — 2–4 honest differentiators. Hygiene/sterilisation between clients is a genuinely strong, niche-appropriate trust point for nail bars specifically — lead with it if nothing else stands out.
7. **Contact CTA** — dark box, call + directions buttons, honest opening-day note.
8. **Footer** — brand/address, contact column, tech badge, sample-data disclosure line.
9. **`gallery.html`** — dedicated page, CSS `column-count` masonry (no JS library), 8–10 photos captioned by category (`Manicure` / `Pedicure` / `Nail Art` / `Studio`), exhibition-style captions (italic title + small mono category label), matching the pattern already proven in `epics/ep_006_website_rebuilds/redesigns/hoxtans/gallery.html`.

## Image sourcing workflow (same discipline as the beauty/tanning skill)

1. `WebSearch`/`WebFetch` Unsplash search/collection pages for nail-specific themes — good queries: `manicure`, `pedicure`, `nail-art`, `gel-nails`. Never guess a `photo-<id>` from memory.
2. Skip `plus.unsplash.com` results (paid tier).
3. `curl -s -o /dev/null -w "%{http_code}" "https://images.unsplash.com/photo-<id>?auto=format&fit=crop&q=80&w=1000"` must return `200` for every candidate before it goes in HTML — verify the whole shortlist in one batch.
4. Check for accidental reuse across sibling sites in this repo (`grep -r "photo-<id>" epics/`) so this build doesn't duplicate an image already used by Hoxtans, Fun Cuts, or another sibling.
5. Nail photography specifically skews toward hand/foot close-ups that can look repetitive — deliberately vary composition (studio product shots, hands holding objects, selective-focus, different colour tones) rather than 10 near-identical manicure crops.

## Verification

Serve locally (`python -m http.server <port>` from `ep_044_web_apps/`) and check via `javascript_tool`:
- Every `<img>` on both `index.html` and `gallery.html` has `complete: true` and `naturalWidth > 0`.
- `tel:`/`mailto:` links are consistent with the sample identity everywhere they appear (hero, contact section, footer, sticky mobile action bar).
- Section counts match intent (`service-item`, `split-item`, `why-card`, `gallery-strip-item`, `art-gallery-item`).
- Mobile nav drawer opens/closes correctly (click-based, not paint-dependent, so reliable even if this session's Browser pane has `requestAnimationFrame`/`IntersectionObserver` quirks — see the beauty/tanning skill's "known false alarm" note, which applies here too).

## AI assistant integration — default on, one-flag off

Every site built under this skill ships with the shared AI assistant wired in **by default** (see `bloom-nail-bar-template/assistant-embed.js` for the reference implementation). This is a standing requirement across all `ep044_*` templates, not optional polish.

1. Create a self-contained `assistant-embed.js` in the site's own folder — dynamically injects `widget.js` from the shared Render-hosted service, guarded by a single `const ASSISTANT_ENABLED = true;` flag at the top. That flag **is** the switch-off mechanism: flipping it to `false` disables the assistant for a client who doesn't want it, with no HTML edits needed.
2. Add `<script src="assistant-embed.js"></script>` to every visitor-facing page (`index.html`, `gallery.html`), right after `reveal.js`. Skip any internal/sales-only page.
3. Register the site as a tenant in `epics/ep_043_AI_native_serviceand _SEO/ai_website_assistant_framework` via its admin API — never by hand-editing `data/clients.json`. Check `curl http://127.0.0.1:4310/api/health` first (another agent may already have it running); otherwise `npm start` from the framework folder. `POST /api/admin/clients` with `Authorization: Bearer <ADMIN_TOKEN from .env>` and a body built from the site's own content: identity/theme/contact matching the site, `pages` (real nav anchors), `knowledge` (location/contact/services/pricing derived from the site copy, never invented), `demoWorkflows.booking` (priced services + slots), `status: "demo"`, `deployments` with `status: "local"` until actually hosted.
4. Verify before calling the build done: `curl "http://127.0.0.1:4310/api/public/config?clientKey=<publicKey>&host=localhost"` resolves the tenant, and one `POST /api/public/chat` request returns an answer genuinely grounded in the new site's knowledge.

## Where output goes + task tracking

Generic template (no real business yet) → `epics/ep_044_web_apps/<template-name>/`, lowercase-hyphenated, descriptive enough to identify the niche (e.g. `bloom-nail-bar-template`). If/when a real nail bar is identified for this template, that becomes a new build under `epics/ep_006_website_rebuilds/redesigns/<business-slug>/` following `ep044_app_beauty_tanning_demo_template` instead — don't retrofit this generic template folder with one real client's facts. Per this repo's `CLAUDE.md`, create a workstream task file in `workstream/300_complete/claude/` once built and verified.

## Required shared layout invariant

Apply §6.4 **Mandatory page-edge and footer contract**, §6.1 **Inner-page editorial hierarchy**, and §6.2 **Gallery relevance** from `ep044_common_site_blueprint/000_site_blueprint.md` without exception. The business identity/logo block, header navigation, hero copy, page content, card/form outer edges and footer content must share one responsive left gutter. Use the normal-flow sticky-footer shell for short pages; never independently centre the header or use a fixed footer. The home hero remains the largest display moment; inner-page headings require an explicitly styled, distinct premium serif face at a smaller scale, with a compact mono kicker and restrained sans-serif lede—never browser-default inner-page text. Every gallery must contain real category-relevant visual assets, never empty cards, generic decoration or “images coming later” copy. When owner work is unavailable, use provenance-recorded, clearly labelled illustrative category imagery that does not claim work by the named business. Verify live geometry, type and image loads after cache-busting production CSS.
