/**
 * lib/verification/email-template.ts — renders the business-verification email.
 *
 * VERSION HISTORY
 * v1.3.0 · 2026-08-10 · Rewrites the body to lead with why the listing matters
 *   to the recipient, links the public directory so the sender can be checked
 *   before any link is clicked, formats the expiry as a human date rather than
 *   an ISO timestamp, and drops the "secure link" phrasing that reads as a
 *   phishing idiom; bumps the template version to v5.
 * v1.2.0 · 2026-07-28 · Moves the sender's physical address out of source into
 *   VERIFICATION_SENDER_ADDRESS so no address is a literal in tracked files.
 * v1.1.0 · 2026-07-28 · Redesigns the email as a legitimate business sender
 *   (why-you-received-this, signature block, reply-based opt-out) after a
 *   plaintext-vs-link test proved the bare single-link CTA was what Gmail was
 *   silently discarding; bumps the template version to v4.
 * v1.0.0 · 2026-07-28 · Version history added; file predates this convention.
 */

export const VERIFICATION_TEMPLATE_VERSION = "verification-v5-value-and-trust";

const SENDER_PERSON = "Edward Bell";
const SENDER_NAME = "The Tech Principle";
const SENDER_CONTACT_EMAIL = "edward.bell@thetechprinciple.com";
// Sourced from config, not hardcoded, so no physical address is ever a
// literal in tracked source. Falls back to a visible placeholder if unset,
// which is itself a signal that this must be configured before real sending.
const SENDER_PHYSICAL_ADDRESS =
  process.env.VERIFICATION_SENDER_ADDRESS?.trim() || "[Registered business address — to be added]";

export function renderVerificationEmail(input: {
  businessName: string; verificationUrl: string; listingUrl: string;
  trackingPixelUrl?: string; expiresAt: Date;
}) {
  // A human date, not an ISO timestamp: no legitimate email to a local
  // business contains "2026-08-17T14:32:11.000Z", and it reads as machine
  // output at exactly the moment the reader is deciding whether to trust us.
  const expiry = input.expiresAt.toLocaleDateString("en-GB", {
    day: "numeric", month: "long", year: "numeric", timeZone: "Europe/London",
  });
  const businessName = input.businessName;

  const text = `Hello,

${businessName} is listed on thetechprinciple.com, our local business directory. This is the page customers see:

${input.listingUrl}

People use the directory to find contact details, opening hours and directions for local businesses — so we'd like to make sure yours is right. You can review and correct it here:

${input.verificationUrl}

It takes about a minute and doesn't need an account or password. Submitting sends your details for manual review; nothing is published automatically. This link is unique to your listing and expires on ${expiry}.

If this isn't your business, or you'd rather we didn't contact you about this listing, just reply to this email and we'll take care of it.

${SENDER_PERSON}
${SENDER_NAME}
${SENDER_CONTACT_EMAIL}
${SENDER_PHYSICAL_ADDRESS}`;

  const html = [
    `<p>Hello,</p>`,
    `<p><strong>${escapeHtml(businessName)}</strong> is listed on thetechprinciple.com, our local business directory. This is the page customers see: <a href="${escapeHtml(input.listingUrl)}">${escapeHtml(input.listingUrl)}</a></p>`,
    `<p>People use the directory to find contact details, opening hours and directions for local businesses — so we'd like to make sure yours is right.</p>`,
    `<p><a href="${escapeHtml(input.verificationUrl)}">Review and correct the details for ${escapeHtml(businessName)}</a></p>`,
    `<p>It takes about a minute and doesn't need an account or password. Submitting sends your details for manual review; nothing is published automatically. This link is unique to your listing and expires on ${escapeHtml(expiry)}.</p>`,
    `<p>If this isn't your business, or you'd rather we didn't contact you about this listing, just reply to this email and we'll take care of it.</p>`,
    `<p>${escapeHtml(SENDER_PERSON)}<br>${escapeHtml(SENDER_NAME)}<br>${escapeHtml(SENDER_CONTACT_EMAIL)}<br>${escapeHtml(SENDER_PHYSICAL_ADDRESS)}</p>`,
    input.trackingPixelUrl
      ? `<img src="${escapeHtml(input.trackingPixelUrl)}" width="1" height="1" alt="" style="display:none" />`
      : "",
  ].join("");

  return {
    subject: `Is this the right contact info for ${businessName}?`,
    text, html,
  };
}

function escapeHtml(value: string) {
  return value.replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[character]!);
}
