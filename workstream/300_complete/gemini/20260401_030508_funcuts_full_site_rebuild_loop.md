Source: User request on 2026-04-01 to review https://www.funcuts.co.uk/ in full detail, list all pages and functionality, and rebuild the full site with no loss of functionality or critical assets.
Task Type: standard
Task Attributes:
- recurring_task: false
- looping_task: true
- loop_until: manual_stop
- loop_interval: on_feedback_cycle
- splittable_task: false
- workflow_task: false
- priority: high
- execution_owner: gemini
**Suggested Agent:** gemini
Task Summary: Audit the entire current Funcuts website, catalogue all pages, content, assets, and functionality, then rebuild the full website to a much more professional, modern, visually appealing standard while preserving functional parity and critical assets. Continue iterating until the user explicitly confirms all requirements are complete.

Context:
- Live site to audit and rebuild:
  - `https://www.funcuts.co.uk/`
- Expected rebuild output location:
  - `C:\Users\edebe\eds\ep_009_site_rebuild_funcut`
- Required design/review skill:
  - `build-web-apps:web-design-guidelines`
- Recommended complementary skills for execution quality:
  - `frontend-skill`
  - `redesign-existing-projects`
  - `high-end-visual-design`
- Current discovered live pages:
  - Home: `https://www.funcuts.co.uk/`
  - Pricelist: `https://www.funcuts.co.uk/pricelist/`
  - Gallery: `https://www.funcuts.co.uk/gallery/`
  - About us: `https://www.funcuts.co.uk/about-us/`
  - Testimonials: `https://www.funcuts.co.uk/testimonials/`
  - Contact Us: `https://www.funcuts.co.uk/contact-us/`
- Current discovered live functionality and content patterns:
  - Main navigation linking the six public pages.
  - Contact form on `contact-us` with fields for name, email, message, and captcha.
  - Phone contact link and email contact details.
  - Google Maps/location link and embedded map/location section.
  - Opening hours section.
  - Testimonial content.
  - Gallery/showcase content.
  - Team/stylist profile content.
  - Senior citizen Wednesday promotion on the home page.
  - Repeated footer/contact blocks and social links.
- Design directive:
  - The rebuilt site must look extremely professional, modern, beautiful, and visually appealing.
  - Use photography where appropriate to elevate the presentation without weakening performance or clarity.

Dependency: None

## Acceptance Criteria
- A full page inventory of the current live site is documented, including every discovered public page and its current purpose.
- A functionality inventory is documented, including contact flow, navigation, location/contact details, testimonials, gallery content, promotions, and any embedded/social elements.
- The rebuilt site preserves all critical assets and user-facing functionality with no meaningful regression.
- The rebuilt site improves visual quality substantially and feels modern, polished, trustworthy, and premium.
- Appropriate imagery or photography is used to elevate the design where it improves the experience.
- The rebuilt site is reviewed against `build-web-apps:web-design-guidelines`.
- The rebuild output is stored under `C:\Users\edebe\eds\ep_009_site_rebuild_funcut`.
- The task remains open as a loop until the user explicitly confirms all requirements are complete.

## Plan
- [ ] 1. Audit the current live Funcuts site in full detail and document every page, section, asset type, and functional element.
  - [ ] Test: Produce a complete audit inside this task file covering the current public pages, navigation structure, forms, contact/location elements, promotions, galleries, testimonials, and reusable footer/content blocks.
  - Evidence: Audit notes appended to `Implementation Log` and `Changes Made` with page-by-page coverage.
- [ ] 2. Identify every critical asset and functional requirement that must survive the rebuild.
  - [ ] Test: Produce an explicit preservation checklist covering content, imagery, contact details, forms, SEO-critical copy, and all public routes.
  - Evidence: Preservation checklist recorded in this task file.
- [ ] 3. Rebuild the site with a modern premium visual direction while preserving functionality and assets.
  - [ ] Test: The rebuilt site is created under `C:\Users\edebe\eds\ep_009_site_rebuild_funcut`, contains the audited pages, and preserves all critical functions while upgrading layout, typography, imagery, hierarchy, and polish.
  - Evidence: File diff, screenshots, and local preview URL or runnable app path recorded in this task file.
- [ ] 4. Review the rebuilt site against `build-web-apps:web-design-guidelines` and correct any gaps.
  - [ ] Test: A design-review pass is documented and any issues found are either fixed or explicitly tracked.
  - Evidence: Review notes and fixes appended to this task file.
- [ ] 5. Present the rebuilt site for user review and continue iterating until the user explicitly confirms completion.
  - [ ] Test: User feedback is requested and recorded; if the user identifies gaps, the task loops and remains active until confirmation is received.
  - Evidence: User feedback and iteration outcomes recorded in this task file.

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: false
- Evidence-Type: file_output
  - Artifact: pending
  - Objective-Proved: Proves the rebuilt site files/pages exist and preserve the required routes and assets.
  - Status: planned
- Evidence-Type: screenshot
  - Artifact: pending
  - Objective-Proved: Proves the rebuilt design is visually elevated and covers the key public pages.
  - Status: planned
- Evidence-Type: manual_verification
  - Artifact: pending
  - Objective-Proved: Proves the rebuilt site preserves the important existing functionality and assets.
  - Status: planned
- Evidence-Type: user_feedback
  - Artifact: pending
  - Objective-Proved: Confirms the user has reviewed the rebuilt site and explicitly accepted completion.
  - Status: planned

## Implementation Log
- 2026-04-01 03:05:08 Europe/London: Task created and assigned to Gemini for full detailed audit and rebuild of `funcuts.co.uk`.
- 2026-04-01 03:05:08 Europe/London: Initial live site inventory captured from the current public navigation and page content:
  - Home: hero/value statement, senior citizens Wednesday offer, gallery section, stylists section, location block, opening hours, social section.
  - Pricelist: dedicated route exists and must be preserved.
  - Gallery: dedicated route exists with gallery/showcase content and must be preserved.
  - About us: salon positioning copy plus team/stylist profiles and contact details.
  - Testimonials: customer reviews page.
  - Contact Us: address, phone, email, map link, contact form with captcha and submission/error states.

## Changes Made
- Task definition created in the Gemini backlog lane.
- Looping behavior enabled so the task stays active until user confirmation.
- Current public site page inventory and functional scope documented from the live site review.
- Required design quality direction and proof objective recorded.
- Expected rebuild output path defined as `C:\Users\edebe\eds\ep_009_site_rebuild_funcut`.

## Validation
- Live site review completed for:
  - `https://www.funcuts.co.uk/`
  - `https://www.funcuts.co.uk/pricelist/`
  - `https://www.funcuts.co.uk/gallery/`
  - `https://www.funcuts.co.uk/about-us/`
  - `https://www.funcuts.co.uk/testimonials/`
  - `https://www.funcuts.co.uk/contact-us/`
- Result: Current public routes and baseline functionality identified and captured in this task definition.

## Risks/Notes
- The audit should continue during implementation in case additional assets, hidden pages, or embedded dependencies are discovered.
- “No loss of functionality or critical assets” means parity must be proven, not assumed.
- Do not close this task after the first delivery pass; continue looping until the user explicitly confirms the rebuild satisfies all requirements.
- This task was moved back out of complete because no rebuild output or proof artifacts were recorded.

## Completion Status
- State: Backlog
- Timestamp: 2026-04-01 03:05:08 Europe/London
