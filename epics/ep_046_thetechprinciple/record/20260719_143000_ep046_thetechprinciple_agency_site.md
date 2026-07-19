# The Tech Principle — umbrella agency site (design-language reference build)

**Task Type:** standard
**Destination Folder:** `workstream/300_complete/claude/`
**Task Summary:** Build a new agency site for `thetechprinciple` — the umbrella tech agency behind everything in `epics/` — taking its look and feel from a set of premium agency references supplied by the user (Torpedo Group, Engine Digital, Ritovex, Think Digital, London Website Design Services). The site covers all four service lines (web design & rebuilds, AI site assistants, local SEO & lead gen, trading & data products) and surfaces the real estate of work across the epics directory. The build is deliberately structured as a **reference implementation for a future design skill** — `DESIGN.md` captures the distilled language so it can be packaged under `skills/` in a follow-up task.
**Dependency:** None

---

## Plan

- [x] Fetched and analysed the five reference sites. Two were unreachable (`enginedigital.com` returned HTTP 403; `thinkdigital.design` returned an empty body), so the language was distilled from the three that resolved plus genre knowledge — recorded honestly in `DESIGN.md` §1 rather than inventing detail for the two that failed.
- [x] Surveyed the existing estate to ground the site's claims in real numbers: 44 built sites in `ep_044_web_apps`, 11 salon/barber rebuilds in `ep_006_website_rebuilds/redesigns`, the assistant framework in `ep_043`, and 45 total epic folders.
- [x] Read the house design conventions before writing anything — `ep_008_product_showcase_website/DESIGN.md` (anti-patterns, motion standards) and `ep_044_web_apps/PALETTE_REGISTRY.md` (sibling palette-collision discipline).
- [x] Confirmed brand + scope with the user via `AskUserQuestion`: brand is `thetechprinciple` as the umbrella agency; all four service lines in scope.
- [x] Created `epics/ep_046_thetechprinciple/site/` — `index.html`, `styles.css`, `script.js`, `serve_site.bat` (matching the `ep_008` convention).
- [x] Chose electric lime `#C8F250` as the accent specifically because it collides with no hue in `PALETTE_REGISTRY.md` (amber, copper, teal, dusty rose, steel blue, cobalt, burgundy, mint were all already taken).
- [x] Added `.claude/launch.json` with a `thetechprinciple-site` config on port 8130, and verified live in the browser pane.
- [x] Wrote `epics/ep_046_thetechprinciple/DESIGN.md` — the skill precursor, documenting palette, type scale, section rhythm, motion rules, imagery approach, accessibility baseline and anti-patterns.

## Changes Made

- `epics/ep_046_thetechprinciple/site/index.html` — full single-page site: nav + mobile drawer, 100svh hero, capability marquee, stat band, four numbered service blocks, six-card work grid, three-step process, four principles, CTA band, footer.
- `epics/ep_046_thetechprinciple/site/styles.css` — the design system: ink/paper dual-ground palette, three-face type system, hairline structure, reveal + marquee motion, three responsive breakpoints, reduced-motion block.
- `epics/ep_046_thetechprinciple/site/script.js` — nav scroll state, accessible mobile drawer, IntersectionObserver reveal, animated stat counters. Progressive enhancement throughout.
- `epics/ep_046_thetechprinciple/site/serve_site.bat` — local preview launcher.
- `epics/ep_046_thetechprinciple/DESIGN.md` — distilled design language for the follow-up skill.
- `.claude/launch.json` — new preview server config (file did not previously exist).

## Two real defects found and fixed during live verification

**1. Blank-page fragility in the reveal animation (design defect).**
`.reveal { opacity: 0 }` was written unconditionally in CSS, so *any* failure of JS or of
`IntersectionObserver` would render the entire site blank. This surfaced because the preview
renderer in this environment never paints — `IntersectionObserver` was confirmed by direct
test to never fire a single callback, leaving 0 of 34 elements revealed and every stat stuck
at "0".

That specific non-painting behaviour is an environment artifact, **not** a bug in the code —
it would have animated correctly in a real browser. But it exposed a genuine fragility worth
fixing on its own merits. Fixed three ways:
- An inline `<script>` in `<head>` adds `.js` to `<html>` before first paint; the hidden state
  is now scoped to `.js .reveal`, so with scripting unavailable the page renders fully visible.
- A 1200ms watchdog force-reveals everything if the observer has not reported once.
- The same watchdog settles the stat counters to their final values.

**2. Accent failed contrast on light sections (accessibility defect).**
The lime accent measures a strong 15.18:1 on ink but collapses to **1.50:1** on the paper
ground — and `--accent-deep` was being used there for the `01`/`02`/`03` process step numbers,
which are meaningful text, plus the service list bullets. Those would have been effectively
unreadable. Fixed by introducing `--accent-on-paper: #4C6410`, a deep olive in the same hue
family measured at **5.88:1** (AA pass), selected by testing seven candidates programmatically
against the paper ground. Audited afterwards with `grep` to confirm `--accent-deep` now
survives only as a hover background on dark ground.

## Evidence

Verified live at `http://localhost:8130`. **Screenshots were not obtainable** — the browser
pane's renderer does not paint in this environment (`computer{action:"screenshot"}` timed out
on every attempt, and `IntersectionObserver` never fired, both symptoms of the same cause).
Verification was therefore done through computed styles and DOM inspection, which is weaker
evidence than a visual check and is stated as such:

- **Rendering:** page loads, `script.js` 200 OK, zero console errors/warnings.
- **Typography:** all three faces confirmed loaded via `document.fonts.check`. Hero resolves to
  `107.52px` at `-3.7632px` tracking.
- **Palette:** hero accent `rgb(200, 242, 80)`, body ground `rgb(10, 12, 14)` — tokens applying correctly.
- **Layout:** no horizontal overflow at 1280px, 768px or 375px (`scrollWidth` 1265/375 vs viewport).
- **Responsive:** at 375px every grid collapses to a single column, nav links hide, burger shows.
- **Drawer:** verified open → `aria-expanded` true, `aria-label` flips to "Close menu", `display: flex`; closes on link activation and on Escape.
- **Reveal watchdog:** after fix, 34/34 elements revealed and counters settled to `["44","11","45","4"]`.
- **No-JS path:** with `.js` removed from `<html>`, hero resolves to `opacity: 1` — page is not blank.
- **Reveal target value:** with the transition neutralised, `.reveal.is-in` resolves to `opacity: 1`, confirming the selector is correct and the observed `0` was a stalled tween, not a broken rule.
- **Contrast (computed):** body/ink 17.91, muted/ink 6.29, accent/ink 15.18, body/paper 17.20, muted/paper 6.19, ink-on-CTA 15.18, step numbers 5.88 — all ≥4.5:1.

`Objective-Delivery-Coverage: 90%` — the site is built, structurally and behaviourally
verified, and the design language is documented. Held below 100% for two reasons: **no visual
confirmation was possible** in this environment, so the aesthetic result is unproven in the
one way that matters most for a design deliverable; and the skill itself — the stated end goal
— is not yet built.

## Risks / Notes

- **The visual result is unverified.** Every structural, behavioural and contrast check passes,
  but nobody has actually looked at this page. It should be opened via `serve_site.bat` (or the
  `thetechprinciple-site` launch config) and reviewed by eye before it goes anywhere near a
  client or a deploy. Type scale, hero density and the case-plate gradients are the most likely
  things to want tuning.
- **Copy is placeholder-grade in one specific respect:** the outcome claims under each service
  ("loads in under a second", "converts twice as well") are plausible positioning copy, not
  measured results from the estate. They should be substantiated or softened before publication.
- **Contact address `hello@thetechprinciple.com` is invented** — no domain has been registered or
  verified as part of this task.
- **The stat figures are real but will drift** — 44/11/45 were counted from the filesystem on
  2026-07-19 and are hardcoded in `index.html`. They will go stale as the estate grows.
- **Follow-up task not yet created:** packaging `DESIGN.md` as a skill under `skills/` is the
  stated next step and remains outstanding.
- `.claude/launch.json` did not previously exist in this repo and was created by this task. If
  other work expects to add configs there, it should merge rather than overwrite.
