# The Tech Principle — Design System

Reference implementation: `site/` (`index.html`, `styles.css`, `script.js`).

This document is the **skill precursor** — it records the design language distilled from a
set of premium agency sites so it can later be packaged as a reusable skill under
`skills/`. Everything below is implemented and verified in `site/`.

---

## 1. Source references

The language is distilled from the restrained end of the agency spectrum:

| Site | What was taken |
|---|---|
| `torpedogroup.com` | Editorial restraint, huge whitespace, text-first CTAs, hero video/atmosphere, "Let's talk" register |
| `enginedigital.com` | Systems-thinking tone, evidence-led copy, disciplined section rhythm |
| `ritovex.webflow.io` | Structural furniture — stat counters, numbered process, logo/capability marquee, card grid |
| `thinkdigital.design` | Confident display type at very large sizes |
| `londonwebsitedesignservices.com` | Service-card taxonomy and local/UK service framing |

**What was deliberately rejected:** stock photography, testimonial carousels, newsletter
sign-ups, cart iconography, blog teasers, gradient-on-gradient hero art, and the
"Get Started / Watch Demo" dual-CTA cliché. These are the tells that make an agency site
read as a template.

---

## 2. The core idea

> **Ink-first, one accent, hairline structure, oversized type, generous air.**

Premium reads as *restraint plus confidence*: near-black ground, a single high-voltage
accent used sparingly, structure drawn in 1px hairlines rather than boxes and shadows, and
display type large enough to be a graphic element in its own right.

---

## 3. Colour

Two grounds — **ink** (dark) and **paper** (warm off-white) — alternating down the page to
create rhythm. One accent. No third hue.

```css
--ink:  #0A0C0E;   --ink-2: #12161A;   --ink-3: #1B2026;
--paper:#F2F0EB;   --paper-2:#FFFFFF;
--accent: #C8F250;          /* electric lime */
--accent-deep: #A8D62F;     /* hover state, dark ground only */
--accent-on-paper: #4C6410; /* deep olive — the accent's light-ground twin */
```

**The accent-on-paper rule is the non-obvious part.** A high-chroma accent chosen for a dark
ground almost never survives on a light one. Measured here:

| Pair | Ratio | Verdict |
|---|---|---|
| `--accent` on `--ink` | **15.18:1** | excellent |
| `--accent` on `--paper` | **1.50:1** | fails badly |
| `--accent-on-paper` on `--paper` | **5.88:1** | AA pass |

So any meaningful mark on a light section (step numbers, list bullets, eyebrow rules) uses
`--accent-on-paper`; `--accent` is reserved for dark ground and the CTA field. Skipping this
step is how lime/cyan/chartreuse palettes end up with invisible text on light sections.

Verified contrast across the whole system:

| Pair | Ratio |
|---|---|
| Body text on ink | 17.91:1 |
| Muted text on ink | 6.29:1 |
| Body text on paper | 17.20:1 |
| Muted text on paper | 6.19:1 |
| Ink text on accent CTA | 15.18:1 |

**Palette collision note:** lime `#C8F250` was chosen partly because it does not collide with
any hue in `epics/ep_044_web_apps/PALETTE_REGISTRY.md` (amber, copper, teal, dusty rose,
steel blue, cobalt, burgundy, mint).

---

## 4. Typography

| Role | Face | Treatment |
|---|---|---|
| Display | Space Grotesk 600 | `letter-spacing: -0.035em`, `line-height: 1.02` |
| Body | Inter 400/500 | `line-height: 1.65`, measure capped at 54–56ch |
| Meta | JetBrains Mono 500 | `0.6875rem`, `letter-spacing: 0.18em`, uppercase |

**Rules that carry the look:**

- **Go bigger than feels safe.** Hero renders at `clamp(2.9rem, 8.4vw, 7.25rem)` — 107px at
  1280px wide. Timid display type is the single biggest tell of an amateur build.
- **Negative tracking scales with size.** Large display type needs `-0.03em`/`-0.05em`;
  without it, big type looks loose and cheap.
- **Mono is for metadata only** — eyebrows, indices, tags, footer labels. It signals
  technical credibility precisely because it is never used for prose.
- **Three tiers of contrast per section**: mono eyebrow → oversized display heading → muted
  body lede. This repeating cadence is what makes sections feel authored rather than stacked.

---

## 5. Structure & rhythm

Section order in the reference build:

```
nav → hero (100svh) → marquee → stats → services → work → process → principles → CTA → footer
       ink            ink        ink     paper      ink    paper     ink          lime   ink
```

- **Alternate grounds.** Never run three same-ground sections consecutively.
- **Section padding** `clamp(5.5rem, 11vw, 10.5rem)` — generous air is not wasted space, it
  is the primary signal of a premium build.
- **Hairlines over cards.** Structure is drawn with 1px borders and 1px grid gaps
  (`gap: 1px` over a border-coloured background) rather than drop shadows. Shadow-heavy
  cards read as dated/templated.
- **Numbered indices** (`01`–`04`) on services and process steps — cheap, and does a lot of
  work for perceived rigour.

---

## 6. Motion

Restrained and compositor-only (`opacity` / `transform`). Standard easing
`cubic-bezier(0.22, 0.61, 0.36, 1)`.

- Scroll reveal: 22px rise + fade, 0.85s, staggered by `data-delay` in 90ms steps.
- Stat counters: `easeOutExpo` over 1.25s.
- Capability marquee: 46s linear loop.
- Hover: 2px lift on buttons, 6px on case plates, 4px arrow nudge.

**Two non-negotiables, both learned the hard way in this build:**

1. **The hidden state must be scoped to `.js`.** `.reveal { opacity: 0 }` written
   unconditionally means any JS failure renders a completely blank page. An inline
   `<script>` in `<head>` adds `.js` to `<html>` before first paint; CSS uses
   `.js .reveal { opacity: 0 }`. No JS → everything visible.
2. **Observers need a watchdog.** `IntersectionObserver` callbacks never arrive in
   throttled, backgrounded, or non-painting renderers. A 1200ms timeout force-reveals
   everything if the observer has not reported once. Without it the page can hang blank —
   this was caught live in exactly such an environment during this build.

`prefers-reduced-motion: reduce` kills all animation, stops the marquee, and settles the
counters to their final values.

---

## 7. Imagery

**No stock photography, no external image assets.** Case studies use CSS "plates": a
directional gradient in a section-specific dark hue, overlaid with a fine grid, with a mono
index in the corner. This keeps the build fully self-contained (no network dependency, no
licensing) and looks more considered than generic stock.

The hero uses the same vocabulary at full scale: two radial accent blooms over a 5.5rem grid,
radially masked so it dissolves toward the edges.

---

## 8. Accessibility baseline

- Skip link, semantic landmarks, single `h1`, ordered heading hierarchy.
- `:focus-visible` ring in accent at 2px with 3px offset — never removed.
- Mobile drawer: `aria-expanded`, `aria-controls`, dynamic `aria-label`, Escape to close,
  closes on link activation.
- Decorative elements (marquee, plates, grid fields) are `aria-hidden`.
- All text pairs verified ≥4.5:1 (see §3).

---

## 9. Anti-patterns

- `transition: all`
- Unconditional `opacity: 0` animation hooks (see §6)
- A single accent token used on both light and dark grounds
- Stock photography and testimonial carousels
- Heavy drop shadows as the primary structural device
- Timid display type
- Scroll-jacking
- Non-semantic `div` buttons

---

## 10. Verification performed

Verified live at `http://localhost:8130` via computed styles and DOM inspection
(screenshots were unavailable — the preview renderer in this environment does not paint):

- Fonts loaded (Space Grotesk / Inter / JetBrains Mono all `document.fonts.check` true).
- Hero display type resolves to 107.52px at `-3.76px` tracking.
- No horizontal overflow at 1280px, 768px or 375px.
- All grids collapse to single column at mobile; burger appears, nav links hide.
- Drawer verified: opens, `aria-label` flips, closes on link click and on Escape.
- Reveal watchdog verified: 34/34 elements revealed, counters settled to 44/11/45/4.
- No-JS path verified: hero resolves to `opacity: 1` with the `.js` class absent.
- Contrast measured programmatically across all seven text/ground pairs.
