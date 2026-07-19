# ep_046 — The Tech Principle

The umbrella tech agency brand behind the work in `epics/`. This epic holds the agency's own
site, built as a **reference implementation of a design language** distilled from a set of
premium agency sites — with the stated intent that the language be packaged as a reusable
skill under `skills/`.

Created 2026-07-19.

---

## Contents

| Path | What it is |
|---|---|
| `DESIGN.md` | **The design language.** Palette, type scale, section rhythm, motion rules, imagery approach, accessibility baseline, anti-patterns. This is the skill precursor — the artefact the future skill is built from. |
| `site/index.html` | Single-page agency site — nav + drawer, hero, marquee, stats, 4 services, 6 work cards, process, principles, CTA, footer. |
| `site/styles.css` | The design system implementation. |
| `site/script.js` | Nav scroll state, accessible mobile drawer, scroll reveal, animated counters. Progressive enhancement throughout. |
| `site/serve_site.bat` | Local preview launcher (port 8130). |
| `record/` | Build record — the workstream task file and a copy of the preview launch config. |

## Running it

```bat
site\serve_site.bat
```

Serves on `http://localhost:8130` and opens a browser. Alternatively, the repo-level
`.claude/launch.json` defines a `thetechprinciple-site` config on the same port (a reference
copy lives in `record/launch.json.reference` — the live file must stay at the repo root to
function).

No build step, no dependencies, no external image assets. Fonts load from Google Fonts; the
site degrades to a clean system-font stack without them.

## Scope

The site covers all four service lines and grounds its claims in the real estate:

| Line | Backed by |
|---|---|
| Web design & rebuilds | 44 built sites in `ep_044_web_apps`, 11 rebuilds in `ep_006_website_rebuilds/redesigns` |
| AI site assistants | `ep_043` assistant framework |
| Local SEO & lead generation | `ep_043`, `ep_034_lead_gen` |
| Trading & data products | `ep_001`, `ep_024_hermes_digitals` and the wider trading estate |

## Status

Built and verified structurally, behaviourally and for contrast. **Not visually reviewed** —
screenshots were unavailable in the build environment, so the aesthetic result is unproven.
Open it and look before it goes near a client or a deploy.

Known caveats, carried from the task record:

- Per-service outcome claims ("converts twice as well as the one it replaced") are positioning
  copy, not measured results. **Unresolved** — these are public advertising claims now that the
  site is production-bound, and should be substantiated or softened.
- `hello@thetechprinciple.com` needs a real mailbox behind it or enquiries are lost.
- Production essentials not yet added: favicon, OG/Twitter cards, canonical URL, `robots.txt`,
  `sitemap.xml`.

## The stat band — read this before changing it

The figures describe **work in progress**, not completed client work, and the labels are
worded deliberately:

| Figure | Label | Basis |
|---|---|---|
| `25+` | Site builds in the deployment pipeline | Deliberately conservative. 44 folders in `ep_044_web_apps` carry a built `index.html`, but 32 of 46 READMEs read *"queued — not yet processed"*, so the true shipped count is lower and moving. 25+ is defensible without qualification. |
| `10` | Legacy rebuilds in progress | Folder count in `ep_006_website_rebuilds/redesigns`. |
| `47` | Products in the estate | `ep_*` folder count. |
| `4` | Disciplines under one roof | The four service lines. |

An earlier draft of this site labelled these *"Client sites shipped"* and *"Legacy rebuilds"*.
That was wrong and was corrected before any deployment: the `ep_044` folders are **unsolicited
outreach demos** for businesses that are not clients and in most cases have not been contacted,
and `ep_006/redesigns` is described by its own `DESIGN.md` as a *"Premium Salon Sales Tool"* —
speculative pitch material. Do not restore completion language to these figures without
evidence of actual signed, delivered client work.

## Next step

Package `DESIGN.md` as a skill under `skills/`. Not yet started — worth doing *after* a visual
review, so the skill captures any tuning rather than baking in unreviewed choices.
