---
name: Web_app_owner_review_skill
description: Adds a point-and-click, per-page review UI woven directly into a generated site's owner-preview.html, so the business owner can request changes without a phone call or an unstructured email. Use when building or updating any ep044_group template so its owner-preview page lets the owner review each site page and submit structured feedback. Reference implementation: epics/ep_044_web_apps/auto-garage-template/owner-review-embed.js, owner-review-config.js, and the "Your review" section in owner-preview.html.
---

# Owner Review Skill

Weaves a structured, point-and-click review UI into `owner-preview.html`,
replacing the previous free-form "Request Changes" mailto with something
that produces reliable, parseable feedback while staying entirely static —
no backend, no build step, consistent with every other EP044 template.

## Inherit the master blueprint

Build every generated site against `../ep044_common_site_blueprint/000_site_blueprint.md`
first — this skill only adds the review layer on top of an already-generated
site's pages (Section 2/3 of the blueprint defines that page list). Do not
invent a different page structure here.

## Why not a free-form email or a phone call

A phone call doesn't scale past a handful of businesses. A free-text "reply
with your thoughts" email is ambiguous and hard to action consistently at
scale. This skill exists specifically so owner feedback arrives in one
predictable shape regardless of which business or category it came from.

## What this skill adds

1. **`assets/js/owner-review-config.js`** — per-site config: which screens
   (pages) are reviewable, the N questions asked per screen, and the M
   point-and-click options per question. Ships with a 5-question x 5-option
   starting default (not a fixed limit — categories may add/remove either).
   Category skills should tailor the question/option wording to what
   genuinely varies for that trade rather than leaving the generic default
   in a real deployment.
2. **`owner-review-embed.js`** — the engine. Follows the exact same
   self-contained, flag-toggled pattern as `assistant-embed.js`
   (`OWNER_REVIEW_ENABLED` at the top). Renders one `<details>` card per
   screen into `#owner-review-root`, each with:
   - a "No action required for this page" default option,
   - N questions x M point-and-click radio options (option 1 pre-selected
     as the sensible "keep as-is" default),
   - one free-text "anything else" field,
   - a `page_open_date_time` recorded client-side the first time that
     screen's card is expanded.
3. **`owner-preview.html` wiring** — a new "Your review" section containing
   `<div id="owner-review-root"></div>`, plus the two new script tags after
   the existing `config.js`/`main.js` includes.

## Submission format (non-negotiable)

On "Submit review," the engine composes a single `mailto:` to the
configured `ownerReviewRecipient` (the operator's inbox, e.g.
`edward.bell@thetechprinciple.com` — **never** the business's own
customer-facing email) with a body in exactly this shape:

```text
<business_name>
{
  screen_name: <screen>, page_open_date_time: <ISO timestamp or "not opened">, 1:<option>, 2:<option>, ..., anything_else: "<text>"
  screen_name: <screen>, page_open_date_time: <ISO timestamp or "not opened">, no_action_required: true, anything_else: "<text>"
  ...
}
```

`1:1` means "question 1, option 1 selected." The owner never sees or types
these numbers — they only ever see the option's real text. A screen with
"No action required" checked omits the numbered answers entirely rather
than defaulting them to option 1, so a genuinely-reviewed-and-fine page is
distinguishable from a page nobody opened.

## No live tracking beacon

`page_open_date_time` is recorded entirely client-side and travels with the
eventual submission — there is no ping back to any server when a page is
opened. The operator only learns anything once (or if) the owner actually
submits. This is deliberate: it keeps the template genuinely static, and it
means the correct trigger for a reminder nudge is **absence of any
submission** within an expected window, not partial view telemetry.

## What this skill does not do

- **Activation stays untouched by this skill.** The existing "Activate This
  Website" mailto link is a separate, later concern (site activation is a
  payment action, tracked as its own EP047 unit) — do not conflate the two.
- **No database, no API call.** If a future integration needs the
  submission to also land somewhere queryable (not just an inbox), that is
  an EP047-side concern (see `ep047_preview_delivery_and_review_workflow.html`),
  not something this skill should grow into.
- **Does not choose page/question content for a category.** The shipped
  config is a generic starting point; a category skill customising this
  template should replace the question/option wording with what actually
  matters for that trade, keeping the N x M x free-text x no-action-required
  shape intact.

## Verification

Before treating this as done for a given site:

1. Open `owner-preview.html` in a browser; confirm one review card renders
   per screen listed in `ownerReviewScreens`.
2. Expand a card, select at least one non-default option, fill the
   free-text field, and confirm `page_open_date_time` is set only for cards
   that were actually opened.
3. Check a screen with "No action required" ticked: confirm its submission
   line omits numbered answers and includes `no_action_required: true`.
4. Confirm the composed body's recipient is the operator's inbox, never the
   business's own contact address.
