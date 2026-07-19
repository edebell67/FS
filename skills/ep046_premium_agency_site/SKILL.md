---
name: ep046_premium_agency_site
description: Build a premium agency, studio, or consultancy website in an ink-first design language — near-black ground alternating with warm paper, a single high-voltage accent, hairline structure, oversized display type, and CSS-drawn imagery instead of stock photography. Use when asked for an "agency site", "studio site", "consultancy site", "portfolio site", a site that should "look high-end / expensive / like a real agency", or a redesign taking inspiration from sites like Torpedo Group, Engine Digital, or similar restrained B2B agency work. Covers the full build: palette with the dual-ground accent rule, type scale, section rhythm, motion with its fail-safes, blog/article pattern, JSON-LD SEO baseline, and a programmatic verification pass. Reference implementation: epics/ep_046_thetechprinciple/site (live at thetechprinciple.com). Also enforces claims discipline — never publish a portfolio figure derived from a folder count without reading what the folders represent.
---

# Premium Agency Site

Build a static agency/studio site that reads as expensive through **restraint**, not
decoration. Hand-written HTML/CSS/JS. No framework, no build step, no external image assets.

**Reference implementation:** `epics/ep_046_thetechprinciple/site` — live at
`https://thetechprinciple.com`. Read it before building; it is the canonical example of
everything below.

Do **not** reach for Next.js/React unless explicitly asked. These sites are a few hundred lines
of CSS and one small script. A framework adds a build step, a deploy pipeline, and a hydration
failure mode, and buys nothing.

---

## 1. The core idea

> **Ink-first, one accent, hairline structure, oversized type, generous air.**

Premium reads as *restraint plus confidence*. Near-black ground, a single high-voltage accent
used sparingly, structure drawn in 1px hairlines rather than boxes and shadows, and display
type large enough to be a graphic element in its own right.

**What to reject** — these are the tells that make a site read as a template: stock
photography, testimonial carousels, newsletter sign-ups, cart iconography, blog teasers with
thumbnails, gradient-on-gradient hero art, and the "Get Started / Watch Demo" dual-CTA cliché.

---

## 2. Colour — and the rule everyone gets wrong

Two grounds, **ink** (dark) and **paper** (warm off-white), alternating down the page. One
accent. No third hue.

```css
:root{
  --ink:   #0A0C0E;  --ink-2: #12161A;  --ink-3: #1B2026;
  --paper: #F2F0EB;  --paper-2: #FFFFFF;

  --accent:          #C8F250;  /* electric lime — dark ground only */
  --accent-deep:     #A8D62F;  /* hover state, dark ground only    */
  --accent-on-paper: #4C6410;  /* the light-ground twin            */

  --on-ink: #F4F5F3;   --on-ink-mute: #8B939B;
  --on-paper: #0A0C0E; --on-paper-mute: #55595F;

  --line-dark:  rgba(255,255,255,0.10);
  --line-light: rgba(10,12,14,0.12);
}
```

### The dual-ground accent rule

**A high-chroma accent chosen against a dark ground will almost never survive on a light one.**
This is the single most common failure in this style. Measured on the reference build:

| Pair | Ratio | |
|---|---|---|
| `--accent` on `--ink` | **15.18:1** | excellent |
| `--accent` on `--paper` | **1.50:1** | fails badly — roughly pale yellow on white |
| `--accent-on-paper` on `--paper` | **5.88:1** | AA pass |

So: **every accent needs a light-ground twin in the same hue family.** Anything meaningful on a
paper section — step numerals, list bullets, eyebrow rules, links — uses `--accent-on-paper`.
The bright accent is reserved for dark ground and the full-bleed accent panel.

Do not try to find one colour that clears 4.5:1 on both. A hue dark enough for off-white is
muddy on near-black; you trade a real accent for one that is merely adequate twice.

Pick the twin by **measuring, not eyeballing** — generate candidates and score them:

```js
const lin = c => { c/=255; return c<=0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4); };
const L = ([r,g,b]) => 0.2126*lin(r)+0.7152*lin(g)+0.0722*lin(b);
const ratio = (a,b) => +((Math.max(L(a),L(b))+0.05)/(Math.min(L(a),L(b))+0.05)).toFixed(2);
```

**Before choosing any palette**, read `epics/ep_044_web_apps/PALETTE_REGISTRY.md` and pick a hue
family no sibling has used. A lightness tweak of an existing hue counts as a collision.

---

## 3. Typography

| Role | Face | Treatment |
|---|---|---|
| Display | Space Grotesk 600 | `letter-spacing: -0.035em`, `line-height: 1.02` |
| Body | Inter 400/500 | `line-height: 1.65`, measure capped 54–56ch |
| Meta | JetBrains Mono 500 | `0.6875rem`, `letter-spacing: 0.18em`, uppercase |

Rules that carry the look:

- **Go bigger than feels safe.** Hero at `clamp(2.9rem, 8.4vw, 7.25rem)` — 107px at 1280px.
  Timid display type is the biggest tell of an amateur build.
- **Negative tracking scales with size.** Large display needs `-0.03em`/`-0.05em`. Without it,
  big type looks loose and cheap.
- **Mono is metadata only** — eyebrows, indices, tags, footer labels. It signals technical
  credibility precisely because it is never used for prose.
- **Three tiers per section**: mono eyebrow → oversized display heading → muted body lede. This
  repeating cadence is what makes sections feel authored rather than stacked.

---

## 4. Structure and rhythm

```
nav → hero (100svh) → marquee → stats → services → work → process → writing → principles → CTA → footer
       ink            ink        ink     paper      ink    paper     paper     ink          accent  ink
```

- **Alternate grounds.** Never run three same-ground sections consecutively.
- **Section padding** `clamp(5.5rem, 11vw, 10.5rem)`. Generous air is not wasted space; it is
  the primary signal of a premium build.
- **Hairlines over cards.** Draw structure with 1px borders and 1px grid gaps (`gap: 1px` over a
  border-coloured background), not drop shadows. Shadow-heavy cards read as dated.
- **Numbered indices** (`01`–`04`) on services and process steps. Cheap, and does a lot of work
  for perceived rigour.

---

## 5. Motion — with its two non-negotiables

Compositor-only (`opacity`/`transform`). Standard easing `cubic-bezier(0.22, 0.61, 0.36, 1)`.
Scroll reveal 22px rise + fade over 0.85s, staggered 90ms. Marquee 46s linear. Hover: 2px lift
on buttons, 6px on cards, 4px arrow nudge. `prefers-reduced-motion` kills all of it.

### Non-negotiable 1 — scope the hidden state to `.js`

`.reveal { opacity: 0 }` written unconditionally means **any** JS failure ships a blank page.
Not "no animation" — no website. Inline in `<head>`, before first paint:

```html
<script>document.documentElement.classList.add('js');</script>
```

```css
.js .reveal      { opacity: 0; transform: translateY(22px); }
.js .reveal.is-in{ opacity: 1; transform: none; }
```

It must be inline and in the head — a deferred external file is exactly the thing that might
not arrive.

### Non-negotiable 2 — give the observer a deadline

Scoping to `.js` handles JS being absent. It does not handle JS running while
`IntersectionObserver` never reports — throttled tabs, background renderers, non-painting
environments. This happened during the reference build: zero callbacks, 0 of 34 elements
revealed, permanently blank.

```js
var reported = false;
var io = new IntersectionObserver(function (entries) { reported = true; /* reveal */ });
setTimeout(function () { if (!reported) revealAll(); }, 1200);
```

**Same reasoning applies to any content gated behind script:** counters that start at `0` in
markup, tabs whose panels are hidden until init, accordions collapsed before hydration. Put the
real value in the HTML and let JS take it over — never the reverse.

---

## 6. Imagery

**No stock photography. No external image assets.** Case studies use CSS "plates": a directional
gradient in a section-specific dark hue, overlaid with a fine grid, with a mono index in the
corner. Self-contained, no licensing, no network dependency — and more considered than stock.

The hero uses the same vocabulary at scale: two radial accent blooms over a 5.5rem grid,
radially masked so it dissolves toward the edges.

Generate the OG card programmatically (PIL, 1200×630) in the same language — ink ground, grid,
brand mark, display headline with the last line in accent.

---

## 7. Blog / article pattern

Section on the homepage (three cards) + a `/blog/` index + standalone post pages sharing the
site stylesheet.

- **Whole card is one link** — a single tab stop per post, not a title/"read more" pair pointing
  at the same destination.
- **Article measure `max-width: 46rem`** (~68ch). Prose, not layout.
- **`pre { overflow-x: auto }`** — wide code scrolls itself, never the page. Verify at 375px.
- Breadcrumb on every post, matching its schema exactly (see §8).

---

## 8. SEO baseline

Build these in from the start; retrofitting is worse.

- **Canonical, OG and Twitter meta** on every page. Title ≤ 60 chars, description ≤ 160.
- **Favicon as an inline SVG data URI** — no extra request, nothing to 404.
- **JSON-LD**: `ProfessionalService` + `WebSite` + `WebPage` on the homepage with an
  `OfferCatalog` of the service lines and `areaServed`; `BlogPosting` + `BreadcrumbList` per
  post; `CollectionPage` + `ItemList` on the blog index.
- **`robots.txt` + `sitemap.xml`** covering every real URL.
- **A `noindex` 404 page.**

Three traps that cost time on the reference build:

1. **Match the canonical host form to what actually serves.** If the CNAME is the apex and
   `www` 301s to it, then `www` canonicals point search engines at a redirect. Check with
   `curl -o /dev/null -w "%{http_code} %{redirect_url}"` before writing 70 URLs the wrong way.
2. **The visible breadcrumb must match `BreadcrumbList` exactly.** Ending the visible trail with
   a section name while the schema ends with the page title is a mismatch Google flags.
3. **No invented NAP.** A wrong postal address or phone in `LocalBusiness`/`ProfessionalService`
   is worse than none — Google cross-references it against the Business Profile and
   inconsistency suppresses local ranking. Omit and leave a comment until the real details exist.

---

## 9. Accessibility baseline

Skip link, semantic landmarks, exactly one `h1` per page, no heading-level skips.
`:focus-visible` ring in accent at 2px/3px offset — never removed. Mobile drawer with
`aria-expanded`, `aria-controls`, dynamic `aria-label`, Escape to close, closes on link
activation. Decorative elements (marquee, plates, grid fields) `aria-hidden`. All text pairs
≥ 4.5:1 — measured, not assumed.

---

## 10. Claims discipline — read this before writing any number

**A folder count is not a portfolio claim.**

On the reference build the stat band was drafted as "44 Client sites shipped" and "11 Legacy
rebuilds", both generated with `ls | wc -l`. Reading the underlying records showed the folders
were **unsolicited outreach demos** — every README said *"Pipeline state: queued — not yet
processed"* and *"No public site, outreach, or external action has been created from this
folder"* — and the rebuilds were described by their own design doc as a *"Premium Salon Sales
Tool"*, i.e. speculative pitch material. Published commercially those would have been false
claims about client work, with CAP Code exposure, disprovable by any prospect asking for two
references.

Rules:

- Any figure destined for public marketing copy: **read the underlying records**, don't count files.
- Prefer **qualitative phrases** ("Multiple sites in the deployment pipeline") over exact counts.
  An exact number invites an audit; the phrase carries the same weight without the exposure.
- Prefer **conservative** ("25+") over precise when a number is wanted.
- Label outcome copy **"What we build toward"**, not "Typical outcome" — the latter asserts
  observed results. Never write "converts twice as well" or similar without a measurement.
- Date any figure that will drift, and say it describes work in progress.

---

## 11. Anti-patterns

- `transition: all`
- Unconditional `opacity: 0` animation hooks (§5)
- One accent token used on both light and dark grounds (§2)
- Stock photography, testimonial carousels
- Heavy drop shadows as the primary structural device
- Timid display type
- Scroll-jacking
- Non-semantic `div` buttons
- Portfolio numbers derived from folder counts (§10)

---

## 12. Verify before shipping

Run these in the browser against the built site. They catch what eyeballing misses.

```js
// contrast across every text/ground pair — all must be >= 4.5
// heading outline: exactly one h1, no level skips
[...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h=>+h.tagName[1]);

// no horizontal overflow at 1280 / 768 / 375
document.documentElement.scrollWidth > window.innerWidth;

// every internal link resolves
await Promise.all([...document.querySelectorAll('a[href]')]
  .map(a=>a.getAttribute('href')).filter(h=>h&&!h.startsWith('#')&&!h.startsWith('mailto'))
  .map(async h=>({h, s:(await fetch(h)).status})));

// every JSON-LD block parses; breadcrumb trail matches its schema
// no-JS path: remove the .js class — content must still be visible
```

Checklist: fonts loaded · no console errors · grids collapse to one column at 375 · drawer
opens/closes on click, link and Escape · code blocks scroll internally · reveal watchdog fires ·
`404` returns the styled page.

**And look at it.** Every check above can pass on a page that is visually wrong. If the
environment cannot screenshot, say so plainly rather than implying the design is verified —
structural verification is not visual verification.
