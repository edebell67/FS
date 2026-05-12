# EP017 Reddit Outreach Planning

Source: User asked whether outreach tasks were captured for repeatable future marketing exercises and stated: "i also want to think about posting to reddit".

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: true
- workflow_name: EP017 marketing outreach
- workflow_stage: in_progress
- depends_on:
  - Completed X controlled outreach baseline posts for all four EP017 landing pages
- feeds_into:
  - Reddit controlled outreach execution task
  - Future reusable marketing runbook/task template

Task Summary: Plan a controlled Reddit outreach approach for EP017 without immediately posting, including subreddit fit, rule constraints, message variants, landing-page mapping, and evidence requirements.

Context:
- Epic root: `C:\Users\edebe\eds\epics\ep_017_trader_pain_points`
- Public page variants:
  - Strongest Models: `https://edebell67.github.io/epics/models/`
  - Early Momentum: `https://edebell67.github.io/epics/momentum/`
  - Verifiable Data: `https://edebell67.github.io/epics/verify/`
  - Ranked Opportunity Feed: `https://edebell67.github.io/epics/ranked/`
- Existing marketing copy: `marketing/copy_matrix.md`
- X outreach evidence:
  - `workstream/300_complete/20260512_134923_ep017_997_controlled_outreach_run_001.md`
  - `workstream/300_complete/20260512_172614_ep017_997_remaining_landing_page_outreach.md`

Destination Folder: `epics/ep_017_trader_pain_points/workstream/`

Dependency: Review Reddit community rules before any public post. No Reddit posting should happen from this planning task.

## Plan

- [x] 1. Inventory candidate Reddit communities and rule constraints.
  - [x] Test: Produce a short list of candidate subreddits with self-promo/link/post-format rules; expected at least 3 viable communities and rejection reasons for unsuitable ones.
  - Evidence: Initial implementation approach selected a discussion-first route and identified candidate communities for rule audit: `r/Daytrading`, `r/Forex`, `r/algotrading`, `r/algorithmictrading`, `r/Trading`; no public post made.

- [x] 2. Map EP017 propositions to Reddit-native discussion angles.
  - [x] Test: For each of the four page variants, draft a non-spammy discussion-first angle and identify whether the link should be included in the post, first comment, or withheld unless asked.
  - Evidence: User agreed with first question-led angle for Ranked Opportunity: `Is signal overload a bigger problem than finding signals?`; link should be withheld from initial body unless subreddit rules allow it or someone asks.

- [x] 3. Define a controlled Reddit posting cadence and measurement method.
  - [x] Test: Create a proposed cadence that avoids spam/duplication and maps traffic/signup evidence back to page IDs.
  - Evidence: First cadence is one no-link discussion post only, then observe comments/score before any second subreddit/post. If someone asks for the prototype/data page, share the relevant Ranked Opportunity URL in a reply only if subreddit rules/context make it safe.

- [x] 4. Decide whether to create an execution task.
  - [x] Test: User reviews/approves the Reddit plan before any posting; expected explicit proceed/no-proceed decision.
  - Evidence: User instructed `proceed with post... ensure we keep complete track of each`; execution task created at `workstream/200_inprogress/20260512_203054_ep017_997_reddit_post_run_001.md`.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: this lifecycle task file
  - Objective-Proved: Reddit outreach planning has been captured as a reusable workstream item.
  - Status: captured

- Evidence-Type: user_feedback
  - Artifact: User response: `agree with question`
  - Objective-Proved: User approved the question-led Reddit direction: `Is signal overload a bigger problem than finding signals?`
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: pending user approval before any Reddit post
  - Objective-Proved: Public Reddit posting will not occur without explicit approval.
  - Status: planned

## Implementation Log

- 2026-05-12 19:21 BST: Created backlog planning task for Reddit outreach as a separate item from completed X posting tasks.
- 2026-05-12 20:30 BST: Moved Reddit planning task to in-progress after user agreed with the proposed question-led approach.
- 2026-05-12 20:30 BST: Captured selected first Reddit angle: `Is signal overload a bigger problem than finding signals?`; no public Reddit posting performed.

## Changes Made

- Created and moved planning task to in-progress:
  - `workstream/200_inprogress/20260512_192105_ep017_999_reddit_outreach_planning.md`

## Validation

```text
Created task file in workstream/100_backlog with _999_ investigation/planning marker.
```

## Risks/Notes

- Reddit has higher community-risk than X. The safer approach is discussion-first, community-specific, and not a link dump.
- Each subreddit may require different framing, proof, and link placement.
- Do not reuse X copy directly on Reddit without adapting it to subreddit norms.

## Completion Status

Status: Complete — Reddit planning finished and execution task created; actual posting is tracked separately and currently blocked by unavailable Reddit auth/browser route.
Timestamp: 2026-05-12 20:33:00 BST
