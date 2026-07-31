---
name: ep047-local-site-generation
description: Generate a real business's website locally (no LLM API key, no per-call cost) for a business sitting at the awaiting_site_generation pipeline stage in the EP047 directory app, then deploy the output to GitHub. Use when asked to run local site generation, process the generation queue, or generate a site for a specific claimed business.
version: 1.3.0
metadata:
  hermes:
    tags: [ep047, site-generation, ep044_group, github-deployment]
    related_skills: [ep044_group, github-deployment]
---

# EP047 Local Site Generation

VERSION HISTORY
v1.3.0 · 2026-07-31 · Makes the jsDelivr purge step unconditional and
  mandatory on every deploy (not just when regenerating an existing slug) --
  a business revising its live site later needs the exact same purge, so
  it's part of the standard deploy step, not a special case to remember.
v1.2.0 · 2026-07-31 · Updates the deploy-verification note: the proxy now
  serves from jsDelivr's GitHub CDN, not GitHub Pages directly (GitHub Pages
  for edebell67/epics has a stuck custom-domain redirect that jsDelivr
  sidesteps), and adds the purge-cache step needed only when regenerating
  an already-existing slug.
v1.1.0 · 2026-07-31 · Corrects the output/deploy location: local generation
  workspace is `epics/ep_044_web_apps/<slug>/`, deploy target is the
  separate `github.com/edebell67/epics` repo (flat, top-level `<slug>/`
  folders -- this is the actual working mechanism behind the 55 sites
  already generated, not `ep_006_website_rebuilds`, which is an unrelated
  project). v1.0.0's location guidance was wrong -- it copied ep044_group's
  generic "real evidence" rule without checking what that folder actually
  is or verifying the deploy path resolved to a live URL.
v1.0.0 · 2026-07-30 · Initial version.

This skill owns the **workflow** of turning a queued business into a deployed
site — get the business, pick the right content skill, generate, deploy,
report back. It does not own site content or design; that's `ep044_group`'s
job (the master blueprint plus one `ep044_app_<category>_demo_template` skill
per trade). This is the `GENERATION_MODE=local` path: you (the agent) run the
`ep044_group` skill yourself, using your own reasoning under the operator's
existing subscription — no LLM API call, no `INTERNAL_API_KEY`, no hosted
cron. That hosted path exists separately in `lib/generation/` and must stay
inert whenever this one runs (see the hard rule at the end).

## 1. Get the business details

The app lives at `epics/ep_047_directory_app/`. Query the database directly
— no HTTP round-trip needed, this skill runs inside the same repo:

```ts
import { getBusinessesAwaitingSiteGeneration } from "@/lib/verification/site-generation";
```

This returns every business at the `awaiting_site_generation` pipeline
stage: `{ id, businessRef, businessName, category, town, stageEnteredAt }`.
If asked to generate one specific business instead of the whole queue, query
it directly by `business_ref` and confirm it's actually at
`awaiting_site_generation` before proceeding — never generate for a business
at any other stage.

### Fresh-data gate (mandatory)

Immediately before choosing the category skill or writing any site file, read
the target row from the live production application/database and capture:
`businessRef`, `businessName`, `category`, `town`, pipeline stage, and
`chat_widget_opt_in`. Treat screenshots, chat history, local exports, cached
browser DOM, prior test evidence, and earlier queue reads as leads only — not
source of truth. If the fresh row differs in any of those fields, discard the
stale values, re-normalize the **fresh** category, and restart matching from
Step 2. Do not generate or deploy until this exact fresh snapshot is recorded
in the Test Results bundle.

Also read `chat_widget_opt_in` on that fresh business row (not currently in
the queue helper's return type — select it directly, or add it there) to
decide later whether the generated site wires in the chat widget.

## 2. Match category to the right ep044_group skill

Normalize the business's `category` (lowercase, non-alphanumeric → `-`) and
find the matching folder under `skills/ep044_group/`:
`ep044_app_<normalized-category>_demo_template`. The exact same
normalization is implemented in
`epics/ep_047_directory_app/lib/generation/skill-loader.ts` — use the same
rule so this path and the hosted path never disagree on which skill applies.

If nothing matches, **stop and say so** — do not guess a nearby skill or
build without one. Report which categories currently have no template so a
human can decide whether to add one or reassign the business's category.

Read `skills/ep044_group/ep044_common_site_blueprint/000_site_blueprint.md`
first — it's authoritative (page architecture, visual system, definition of
done). Then read the matched `ep044_app_<category>_demo_template/SKILL.md`
for the category-specific content, palette, and imagery guidance.

## 3. Generate the site

Follow the matched skill and the blueprint exactly, using the business's
**real** name, category, and town — never fabricate stats, reviews, ratings,
or accreditations (per the blueprint's own rule and per this skill's own
non-negotiable). Since the business has real evidence (a real claimed
listing), this is the "real facts" branch of the category skill's decision
rule, not the fictional-sample-identity branch.

Source images from the already-compressed category folder:
`epics/ep_044_web_apps/_images/batch_02/illustrative_gallery_sets/<category>/`
(already under 200KB each — do not re-source new images unless that folder
is empty for the category, and never commit any new image over 200KB).

Wire in `assistant-embed.js` with `ASSISTANT_ENABLED` set to match the
business's `chat_widget_opt_in` value from step 1.

Verify before calling anything done: every `<img>` on every page loads,
section/image counts match the blueprint's matrix, responsive, accessible,
no console errors — the blueprint's own Section 14 definition of done.

## 4. Output location and deployment

Write output locally to:
```
epics/ep_044_web_apps/<slug>/
```
where `<slug>` is the business name, lowercased, non-alphanumeric → `-`. This
is the local generation workspace only — it is never the deploy target and
is not itself pushed anywhere as-is.

**Deploy target is a separate repo:** `github.com/edebell67/epics`. Each
business site is a top-level folder at that repo's root, e.g.
`github.com/edebell67/epics/<slug>/index.html` (see the existing
`dg-maintenance-uk-ltd/` folder there for the established convention — flat,
no nesting under any subfolder).

To deploy: copy the finished `epics/ep_044_web_apps/<slug>/` folder into a
local clone of `edebell67/epics` (reuse an existing clone if one is already
on this machine rather than creating a new one -- check first), as a new
top-level `<slug>/` folder there, then commit and push. Use
`github-deployment`'s scoped-commit discipline (commit only the new
`<slug>/` folder, never a blanket `git add -A`).

The resulting live URL is proxied through the EP047 app via
`epics/ep_047_directory_app/lib/github-pages-proxy.ts`, which fetches from
jsDelivr's GitHub CDN (`https://cdn.jsdelivr.net/gh/edebell67/epics@master`),
not GitHub Pages directly -- GitHub Pages for that repo has a stuck
custom-domain redirect (`thetechprinciple.com`, which now points at Render)
that jsDelivr sidesteps entirely.

**Always purge jsDelivr's cache for every file just pushed, every deploy --
not only when regenerating an existing slug.** This is unconditional, not a
judgment call: a business revising and redeploying its site later needs the
same purge, and purging a brand-new file that was never cached is harmless.
For each file in `<slug>/` (at minimum `index.html` and any other page/asset
that changed):
```
https://purge.jsdelivr.net/gh/edebell67/epics@master/<slug>/<file>
```
Purge propagation across jsDelivr's edge network is not instant even when
the purge call itself reports success -- verify by re-fetching the file
after a short wait and confirming the content actually changed before
reporting the deploy as done.

## 5. Report completion back to the pipeline

Call the existing function directly (same process, no HTTP/API key needed):

```ts
import { recordSiteGenerated } from "@/lib/verification/site-generation";

await recordSiteGenerated({
  businessId, // from step 1
  siteUrl: `${PUBLIC_APP_ORIGIN}/<slug>/index.html`,
  actorUserId, // the acting admin/system user id
});
```

Only call this once the site is genuinely pushed and live — never
speculatively. This advances the business's pipeline stage to
`ready_for_preview`. The existing preview-ready notification logic
(`getBusinessesReadyForPreviewNotification`) picks it up separately; you
don't need to trigger it yourself.

## Hard rule — check GENERATION_MODE first

Before doing any of the above, check the app's `GENERATION_MODE` env var. If
it is `"hosted"`, **stop immediately** — the Render cron
(`epics/ep_047_directory_app/lib/generation/run-generation.ts`) is the active
path instead, and both paths calling `recordSiteGenerated()` for the same
business would double-generate it or silently overwrite each other's
`siteUrl`. Only proceed when `GENERATION_MODE` is `"local"` (or unset,
since `local` is the default).

## Example request

"Use $ep047-local-site-generation to process the site-generation queue" or
"Use $ep047-local-site-generation to generate the site for TP-TEST-000001."
