---
name: landing-page-management
description: Workflow for creating, auditing, and deploying high-conversion landing page series. Covers multi-page decomposition, link verification (anchors/assets), URL shortening/aliasing via redirectors, and marketing documentation alignment. Use when asked to "build a landing page series", "check all links", or "optimize public URLs" for marketing campaigns.
---

# Landing Page Management Workflow

Execute this workflow to ensure high-quality, functional, and professional landing page deployments.

## 1. Research & Decomposition
- **Asset Review**: Analyze source material (images, PRDs, wireframes).
- **Segmentation**: Identify key audience pain points and map them to specific pages.
- **Backend Readiness**: Ensure a shared lead capture API (e.g. `https://ep-017.onrender.com/api/capture_lead`) is ready and healthy.

## 2. Page Creation
- **Folder Structure**: Create distinct folders for each page variant (e.g. `page_1_strongest_models`).
- **Standardized Assets**: Use consistent naming for `index.html`, `styles.css`, and `app.js`.
- **Component Integrity**: Ensure Hero, How It Works, Performance, and Pricing sections are clearly defined.

## 3. Link & Anchor Audit
- **Internal Anchors**: Every nav link (e.g. `#pricing`) MUST have a corresponding `id` on a container element (e.g. `<div id="pricing">`).
- **Placeholder Removal**: Replace `/login` or `#` with functional URLs (e.g. `https://piphunter.io/login`).
- **Asset Paths**: Verify that `styles.css` and `app.js` use relative paths correct for the folder depth.
- **Backend URL**: Confirm `BACKEND_URL` in `app.js` matches the intended environment (localhost for dev, Render/Vercel for public).

## 4. URL Aliasing & Shortening
- **Root Aliases**: Create top-level folders with professional names (e.g. `/models`, `/momentum`) in the repo root.
- **Redirector Logic**: Place an `index.html` in each alias folder with both `<meta http-equiv="refresh">` and JS `window.location` redirecting to the deep nested page.
- **Root Portal**: Update the repository's root `index.html` with a clean menu linking to all shortened aliases.

## 5. Marketing Alignment
- **Copy Matrix**: Update `marketing/copy_matrix.md` with the FINAL shortened public URLs.
- **Hook Verification**: Ensure social media (X/Twitter) and Reddit hooks contain working links and correct emoji formatting.

## 6. Deployment & Verification
- **Build Trigger**: Push changes to the hosting provider (e.g. GitHub Pages).
- **Public 404 Check**: Verify every shortened URL resolves correctly without case-sensitivity issues.
- **Capture Test**: Perform a live lead capture submission on each page and verify data appears in the backend logs/database.

## 7. Documentation
- **Task Lifecycle**: Move all related tasks to `300_complete`.
- **Epic Update**: Refresh the central Epic file with the final public URLs and completion timestamp.
