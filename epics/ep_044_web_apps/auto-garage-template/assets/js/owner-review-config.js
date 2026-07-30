/*
 * assets/js/owner-review-config.js — per-site review screens, questions and options.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-07-29 · Initial version: 6 screens x 5 questions x 5 options as a
 *   starting default (deliberately not a fixed limit), plus the operator recipient
 *   the structured submission is addressed to.
 */

/*
 * ============================================================================
 *  OWNER REVIEW CONFIGURATION — SAMPLE / STARTING CONTENT
 * ============================================================================
 *  Drives the point-and-click review UI embedded in owner-preview.html via
 *  owner-review-embed.js. Every screen listed here gets its own review card
 *  with N questions (each with M options) plus one free-text field.
 *
 *  The 5 questions x 5 options below are a STARTING DEFAULT, not a fixed
 *  limit — categories can add/remove questions or options per screen. The
 *  option wording here is generic and placeholder; category skills should
 *  tailor it to what actually varies for that trade (see
 *  ../ep044_common_site_blueprint/000_site_blueprint.md Section 2/3 for the
 *  page list this should be built against).
 * ============================================================================
 */

const ownerReviewRecipient = "edward.bell@thetechprinciple.com";

const ownerReviewQuestions = [
  "Overall design and layout",
  "Colours and branding",
  "Images and photos",
  "Text and wording",
  "Trust signals and calls to action",
];

const ownerReviewOptions = [
  "Keep as-is",
  "Small tweak needed",
  "Significant change needed",
  "Not sure — let's discuss",
  "Remove this section",
];

const ownerReviewScreens = [
  { screenName: "home", label: "Home" },
  { screenName: "services", label: "Services" },
  { screenName: "gallery", label: "Gallery / Our Work" },
  { screenName: "reviews", label: "Reviews / Testimonials" },
  { screenName: "about", label: "About / Meet the Team" },
  { screenName: "contact", label: "Contact / Request a Quote" },
];
