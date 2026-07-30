Task Type: recurring

Task Summary: Instructions for the automated agent that already redeploys
this app on a 30-minute cycle — on the same cycle, also run the EP047 local
site-generation loop (GENERATION_MODE=local), using this agent's own
reasoning under the existing Claude subscription rather than a metered LLM
API call. This is the active generation path until real paying clients
justify the hosted (API) path built in `lib/generation/`.

Dependency: The three internal endpoints (queue/complete/notify), the
compressed image library (git commit 06b58e7c), and the `chat_widget_opt_in`
column (commit 6ef526de) must already exist — they do, as of 2026-07-30.

VERSION HISTORY
v1.0.0 · 2026-07-30 · Initial version.

## What to do, each cycle

1. **Check the queue.**
   ```
   GET {PUBLIC_APP_ORIGIN}/api/internal/site-generation/queue
   Authorization: Bearer {INTERNAL_API_KEY}
   ```
   Returns `{ businesses: [{ id, businessRef, businessName, category, town, stageEnteredAt }] }`.
   Empty array → nothing to do this cycle, stop here.

2. **For each business, pick its skill template.**
   Normalize the business's `category` (lowercase, non-alphanumeric → `-`) and
   match it against the `ep044_app_*_demo_template` folders in
   `skills/ep044_group/` (same normalization logic as
   `lib/generation/skill-loader.ts`, so the two paths never disagree on which
   skill applies to a given category). If nothing matches, skip that business
   and log why — never guess a template.

3. **Generate the site yourself.**
   Read `skills/ep044_group/ep044_common_site_blueprint/000_site_blueprint.md`
   first (it's authoritative — fonts, type scale, image matrix, definition of
   done), then the matched `ep044_app_<category>_demo_template/SKILL.md`.
   Use the business's **real** name/category/town — never fabricate stats,
   reviews, or accreditations. Pull images from
   `epics/ep_044_web_apps/_images/batch_02/illustrative_gallery_sets/<category>/`
   (already compressed under 200KB each — do not re-source new images unless
   that folder is empty for the category).

4. **Read the `chat_widget_opt_in` column** on the business row (via the app's
   DB, or ask for it to be added to the queue response if not already there)
   to decide whether to wire in `assistant-embed.js` with
   `ASSISTANT_ENABLED = true` or `false`.

5. **Write and verify**, per the blueprint's Section 14 definition of done:
   every `<img>` loads, section/image counts match the matrix, responsive,
   accessible, no console errors.

6. **Output location — same as the hosted path would use:**
   `epics/ep_006_website_rebuilds/redesigns/<slug>/` (slug = business name,
   lowercased, non-alphanumeric → `-`). This is the same path
   `lib/github-pages-proxy.ts` already serves through, so nothing downstream
   needs to change.

7. **Commit and push** the generated files to the same branch/remote this
   agent already deploys from, as part of its normal commit cycle — no
   separate confirmation needed since this is exactly the standing
   commit/deploy behaviour already authorized for this agent.

8. **Report completion:**
   ```
   POST {PUBLIC_APP_ORIGIN}/api/internal/site-generation/complete
   Authorization: Bearer {INTERNAL_API_KEY}
   Content-Type: application/json
   { "businessId": "<id>", "siteUrl": "{PUBLIC_APP_ORIGIN}/epics/ep_006_website_rebuilds/redesigns/<slug>/index.html" }
   ```
   This advances the business's pipeline stage to `ready_for_preview`. Only
   call this once the site is genuinely live at that URL — never speculatively.

9. **Trigger the preview-ready notification:**
   ```
   POST {PUBLIC_APP_ORIGIN}/api/internal/site-generation/notify
   Authorization: Bearer {INTERNAL_API_KEY}
   ```
   Already idempotent — safe to call every cycle regardless of whether
   anything was generated this run.

## Hard rule — do not run if GENERATION_MODE is not "local"

Check the app's own `GENERATION_MODE` env var (Render dashboard or
`.env.local`) before doing any of the above. If it's set to `"hosted"`, the
Render cron (`ep047-site-generation`, `lib/generation/run-generation.ts`) is
the active path instead — stop immediately and do not touch the queue.
Both paths call the same `complete` endpoint; if both ran against the same
queued business, it could be double-generated or one completion could
silently overwrite the other's `siteUrl`. Exactly one path may be active at
a time.

Plan:
- [ ] Wire this instruction set into the deploying agent's own cycle (its
      operator/config decides how — this file is the source of truth for
      what that cycle should do, not itself an automation)
- [ ] First live run: confirm one real queued business gets a real generated
      site, a real commit/push, and a real `complete` call
- [ ] Confirm GENERATION_MODE=local is set wherever that agent reads env from

Evidence: (fill in on first real run) — business ref generated, commit hash,
siteUrl reported, screenshot or live URL check.

Objective-Delivery-Coverage: 0% — this is the instruction set only; no live
run has happened yet.
