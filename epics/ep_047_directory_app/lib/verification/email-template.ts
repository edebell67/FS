/**
 * lib/verification/email-template.ts — renders the business-verification email.
 *
 * VERSION HISTORY
 * v1.3.0 · 2026-08-10 · Updates subject and copy to identify the public
 *   listing URL explicitly and use the owner-requested verification wording.
 * v1.2.0 · 2026-07-28 · Moves the sender's physical address out of source into
 *   VERIFICATION_SENDER_ADDRESS so no address is a literal in tracked files.
 * v1.1.0 · 2026-07-28 · Redesigns the email as a legitimate business sender
 *   (why-you-received-this, signature block, reply-based opt-out) after a
 *   plaintext-vs-link test proved the bare single-link CTA was what Gmail was
 *   silently discarding; bumps the template version to v4.
 * v1.0.0 · 2026-07-28 · Version history added; file predates this convention.
 */

export const VERIFICATION_TEMPLATE_VERSION = "verification-v5-listing-context";

const SENDER_NAME = "The Tech Principle";
const SENDER_CONTACT_EMAIL = "edward.bell@thetechprinciple.com";
const SENDER_PHYSICAL_ADDRESS =
  process.env.VERIFICATION_SENDER_ADDRESS?.trim() || "[Registered business address — to be added]";

export function renderVerificationEmail(input: {
  businessName: string;
  listingUrl: string;
  verificationUrl: string;
  trackingPixelUrl?: string;
  expiresAt: Date;
}) {
  const expiry = input.expiresAt.toISOString();
  const businessName = input.businessName;

  const text = `Hello,

${businessName} is listed on thetechprinciple.com, our local business directory — you can see the current listing here: ${input.listingUrl}

Customers use this directory to find contact details, hours, and location for local businesses. We want to make sure what they see for you is accurate, so could you take a minute to check it?

${input.verificationUrl}

It takes about a minute, doesn't need an account or password, and submitting sends your details for manual review — nothing is published automatically. This link is unique to your listing and expires ${expiry}.

If this isn't your business, or you'd rather we didn't contact you about this listing, just reply to this email and we'll take care of it.

Edward Bell
${SENDER_NAME}
${SENDER_CONTACT_EMAIL}
${SENDER_PHYSICAL_ADDRESS}`;

  const html = [
    `<p>Hello,</p>`,
    `<p><strong>${escapeHtml(businessName)}</strong> is listed on thetechprinciple.com, our local business directory — you can see the current listing here: <a href="${escapeHtml(input.listingUrl)}">${escapeHtml(input.listingUrl)}</a></p>`,
    `<p>Customers use this directory to find contact details, hours, and location for local businesses. We want to make sure what they see for you is accurate, so could you take a minute to check it?</p>`,
    `<p><a href="${escapeHtml(input.verificationUrl)}">Review and verify this listing</a></p>`,
    `<p>It takes about a minute, doesn't need an account or password, and submitting sends your details for manual review — nothing is published automatically. This link is unique to your listing and expires ${escapeHtml(expiry)}.</p>`,
    `<p>If this isn't your business, or you'd rather we didn't contact you about this listing, just reply to this email and we'll take care of it.</p>`,
    `<p>Edward Bell<br>${escapeHtml(SENDER_NAME)}<br>${escapeHtml(SENDER_CONTACT_EMAIL)}<br>${escapeHtml(SENDER_PHYSICAL_ADDRESS)}</p>`,
    input.trackingPixelUrl
      ? `<img src="${escapeHtml(input.trackingPixelUrl)}" width="1" height="1" alt="" style="display:none" />`
      : "",
  ].join("");

  return {
    subject: `Is ${businessName}'s listing on thetechprinciple.com correct?`,
    text,
    html,
  };
}

function escapeHtml(value: string) {
  return value.replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[character]!);
}
