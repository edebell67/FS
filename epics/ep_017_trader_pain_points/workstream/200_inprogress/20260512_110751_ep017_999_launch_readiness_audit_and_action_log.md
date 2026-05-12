# EP017 Launch Readiness Audit and Action Log

Source: User request to proceed with launch tasks after GitHub was updated, followed by instruction to ensure a task captures all actions in the workstream folder and includes `ep017` in the filename.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: true
- workflow_name: EP017 launch readiness
- workflow_stage: in_progress
- depends_on:
  - GitHub remote `master` updated to commit `59508107c1024242fa3cf35ff40daf39d43f86f2`
- feeds_into:
  - EP017 public launch / outreach execution

Task Summary: Capture and verify EP017 launch-readiness actions, including public page checks, backend lead-capture health, email-capture focus, and a central change/action library for launch traceability.

Context:
- Epic root: `C:\Users\edebe\eds\epics\ep_017_trader_pain_points`
- WSL path: `/mnt/c/Users/edebe/eds/epics/ep_017_trader_pain_points`
- Public pages:
  - `https://edebell67.github.io/epics/models/`
  - `https://edebell67.github.io/epics/momentum/`
  - `https://edebell67.github.io/epics/verify/`
  - `https://edebell67.github.io/epics/ranked/`
- Backend:
  - `https://ep-017.onrender.com/api/capture_lead`
  - `https://ep-017.onrender.com/api/stats`

Destination Folder: `epics/ep_017_trader_pain_points/workstream/`

Dependency: GitHub Pages source pushed to GitHub and Render backend available.

## Plan

- [x] 1. Load project context and landing-page workflow.
  - [x] Test: Read `/mnt/c/Users/edebe/Downloads/ed_project_context_inventory.md` and `/mnt/c/Users/edebe/eds/skills/landing-page-management/SKILL.md`; expected both files readable.
  - Evidence: Both files read successfully. Landing-page workflow confirmed requirements for URL aliases, link/anchor checks, backend URL, public 404 check, and capture testing.

- [x] 2. Inventory EP017 files and public-page configuration.
  - [x] Test: Search `/mnt/c/Users/edebe/eds/epics/ep_017_trader_pain_points`; expected page folders, app.js files, API files, marketing copy, and verification scripts visible.
  - Evidence: Found 45 EP017 files including four page folders, `marketing/copy_matrix.md`, `verify_email_capture_focus.py`, and `verify_backend_capture.py`.

- [x] 3. Verify email-capture focus and links/anchors.
  - [x] Test: Run `python verify_email_capture_focus.py`; expected pass for four pages.
  - Evidence: `EMAIL CAPTURE FOCUS CHECK PASSED` / `Checked 4 pages`.

- [x] 4. Verify public URLs resolve.
  - [x] Test: HTTP check root portal plus four aliases; expected HTTP 200.
  - Evidence: All returned `200`: `/epics/`, `/epics/models/`, `/epics/momentum/`, `/epics/verify/`, `/epics/ranked/`.

- [x] 5. Verify backend lead capture and CORS.
  - [x] Test: POST lead payload with `email`, `page_id`, `pain_point_key`; expected 201 and stats visibility.
  - Evidence: POST returned `201 {"message":"Lead captured in JSON storage"}`. Stats returned page count for probe keys. OPTIONS/POST from origin `https://edebell67.github.io` returned CORS allow-origin headers.

- [x] 6. Fix stale backend verification script payload shape.
  - [x] Test: Run `python verify_backend_capture.py`; expected successful direct POST and stats check.
  - Evidence: Script now sends `page_id` and `pain_point_key`; output shows `✅ SUCCESS: Lead capture backend is functional and incrementing.`

- [x] 7. Browser-check first public alias redirect target.
  - [x] Test: Navigate to `https://edebell67.github.io/epics/models/`; expected public page loads and resolves to actual page folder.
  - Evidence: Browser loaded title `TradeEdge | The Strongest Live Trading Models`; final URL `https://edebell67.github.io/epics/ep_017_trader_pain_points/page_1_strongest_models/`.

- [x] 8. Create/update central EP017 change/action library under workstream.
  - [x] Test: File exists under `workstream/` and includes all actions above.
  - Evidence: Created `workstream/EP017_MAIN_CHANGE_LIBRARY.md` with launch baseline, applied changes/actions, evidence, open launch actions, and related lifecycle files.

- [x] 9. Final verification of lifecycle storage.
  - [x] Test: List workstream files and confirm this task filename contains `ep017`.
  - Evidence: Verified both `workstream/200_inprogress/20260512_110751_ep017_999_launch_readiness_audit_and_action_log.md` and `workstream/EP017_MAIN_CHANGE_LIBRARY.md` exist; both contain EP017/action references.

## Evidence

Objective-Delivery-Coverage: 98%
Auto-Acceptance: false

- Evidence-Type: test_output
  - Artifact: `python verify_email_capture_focus.py` output: `EMAIL CAPTURE FOCUS CHECK PASSED` / `Checked 4 pages`
  - Objective-Proved: Four landing pages remain focused on email capture with required lead form elements.
  - Status: captured

- Evidence-Type: url
  - Artifact: HTTP 200 checks for `https://edebell67.github.io/epics/`, `/models/`, `/momentum/`, `/verify/`, `/ranked/`
  - Objective-Proved: Public portal and short aliases resolve.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: Direct backend POST returned `201 {"message":"Lead captured in JSON storage"}` and stats showed probe count.
  - Objective-Proved: Render lead-capture backend accepts production-shaped payloads.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: CORS OPTIONS/POST checks showed `access-control-allow-origin: https://edebell67.github.io`
  - Objective-Proved: GitHub Pages origin can submit to Render backend.
  - Status: captured

- Evidence-Type: demo
  - Artifact: Browser navigation to `https://edebell67.github.io/epics/models/` loaded page title `TradeEdge | The Strongest Live Trading Models`.
  - Objective-Proved: First short public alias redirects/loads the live page.
  - Status: captured

- Evidence-Type: demo
  - Artifact: Browser form-submit checks on all four aliases: `/models/`, `/momentum/`, `/verify/`, `/ranked/`; all returned success toast and cleared email input.
  - Objective-Proved: Live public pages can submit lead-capture forms to the Render backend from a browser.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `/api/stats` returned `{"early_momentum":1,"ranked_opportunity":1,"strongest_models":1,"verifiable_data":1}` after browser submissions.
  - Objective-Proved: Lead submissions are recorded under the expected page IDs for all four variants.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `workstream/200_inprogress/20260512_110751_ep017_999_launch_readiness_audit_and_action_log.md`
  - Objective-Proved: Workstream lifecycle record exists with `ep017` reference in filename.
  - Status: captured

## Implementation Log

- 2026-05-12 11:03 BST: Confirmed local and remote GitHub `master` both at `59508107c1024242fa3cf35ff40daf39d43f86f2`.
- 2026-05-12 11:04 BST: Loaded project context inventory and landing-page-management skill.
- 2026-05-12 11:05 BST: Audited EP017 file tree, page app.js backend URLs, links, href anchors, root aliases, and marketing copy URLs.
- 2026-05-12 11:05 BST: Ran email-capture focus check; passed.
- 2026-05-12 11:05 BST: Ran old backend verification script; found it used stale payload key `page` and backend rejected with `400 Missing email or page_id`.
- 2026-05-12 11:05 BST: Verified all public URLs returned HTTP 200.
- 2026-05-12 11:06 BST: Manually POSTed production-shaped lead payload with `page_id` and `pain_point_key`; backend returned 201 and stats reflected count.
- 2026-05-12 11:06 BST: Updated `verify_backend_capture.py` payload shape to match live `app.js` and backend API contract.
- 2026-05-12 11:06 BST: Re-ran `verify_backend_capture.py`; successful.
- 2026-05-12 11:07 BST: Browser loaded `/epics/models/` and confirmed page title/final redirected URL.
- 2026-05-12 11:07 BST: Created this lifecycle file under `workstream/200_inprogress/` with `ep017` in filename.
- 2026-05-12 11:08 BST: Created `workstream/EP017_MAIN_CHANGE_LIBRARY.md` as the main library of all applied EP017 launch-readiness changes/actions.
- 2026-05-12 11:08 BST: Verified both workstream records exist and contain EP017/action references.
- 2026-05-12 11:10 BST: Created local Git commit `2ad06359793e6016e275f01f9a2bdbc889e3ea6f` for verification helper and workstream docs.
- 2026-05-12 11:10 BST: Attempted push to GitHub; push blocked because no HTTPS token/credential helper/gh auth/SSH key is available in this environment.
- 2026-05-12 11:11 BST: Browser-submitted live forms for `/models/`, `/momentum/`, `/verify/`, and `/ranked/`; all returned success toast messages.
- 2026-05-12 11:11 BST: Verified `/api/stats` records all four page IDs: `strongest_models`, `early_momentum`, `verifiable_data`, `ranked_opportunity`.

## Changes Made

- Updated verification helper:
  - `verify_backend_capture.py`
  - Changed payload from stale `page`/`metadata` shape to live shape: `email`, `page_id`, `pain_point_key`.
  - Changed stats check from `total_leads` to the submitted `page_id` count because `/api/stats` returns a page-id keyed object.
- Created lifecycle record:
  - `workstream/200_inprogress/20260512_110751_ep017_999_launch_readiness_audit_and_action_log.md`
- Created central change/action library:
  - `workstream/EP017_MAIN_CHANGE_LIBRARY.md`

## Validation

Commands/checks run:

```text
python verify_email_capture_focus.py
# EMAIL CAPTURE FOCUS CHECK PASSED
# Checked 4 pages

python verify_backend_capture.py
# Direct POST Result: 201 {"message":"Lead captured in JSON storage"}
# New Lead Count For verification_script: 1
# ✅ SUCCESS: Lead capture backend is functional and incrementing.

curl -L public URL checks
# /epics/, /models/, /momentum/, /verify/, /ranked/ all returned HTTP 200

CORS probe
# OPTIONS 200 with access-control-allow-origin: https://edebell67.github.io
# POST 201 with access-control-allow-origin: https://edebell67.github.io

Browser form-submit checks
# /models/ toast: Success! Your trial is being activated.
# /momentum/ toast: Success! Your edge is being prepared.
# /verify/ toast: Success! Access granted to the data feed.
# /ranked/ toast: Success! Access granted to the data feed.

/api/stats after browser submissions
# {"early_momentum":1,"ranked_opportunity":1,"strongest_models":1,"verifiable_data":1}

Local Git commit
# 2ad06359793e6016e275f01f9a2bdbc889e3ea6f docs(ep017): record launch readiness audit

GitHub push attempt
# fatal: could not read Username for 'https://github.com': No such device or address
```

## Risks/Notes

- GitHub push is currently blocked by missing authentication in this environment. Local commit exists and is ready to push once credentials are restored.
- Test lead submissions created probe entries in the live backend stats (`launch_readiness_probe`, `verification_script`, `cors_probe`) plus browser-test page counts (`strongest_models`, `early_momentum`, `verifiable_data`, `ranked_opportunity`).
- Marketing copy exists and points to live aliases, but external posting still requires explicit approval.

## Completion Status

Status: In progress — launch-readiness audit record and central change/action library created; all four public aliases browser/form-submit tested successfully. Local Git commit created but GitHub push is blocked pending authentication restoration. Remaining launch work is controlled outreach-run execution.
Timestamp: 2026-05-12 11:12:00 BST
