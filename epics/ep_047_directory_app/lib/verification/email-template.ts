export const VERIFICATION_TEMPLATE_VERSION = "verification-v4-legitimate-sender";

const SENDER_NAME = "The Tech Principle";
const SENDER_CONTACT_EMAIL = "edward.bell@thetechprinciple.com";
// TODO: replace with the real registered business address before sending to
// any real (non-test) recipient. A placeholder here is a legitimacy signal
// only once it is truthful.
const SENDER_PHYSICAL_ADDRESS = "[Registered business address — to be added]";

export function renderVerificationEmail(input: {
  businessName: string; verificationUrl: string; trackingPixelUrl?: string; expiresAt: Date;
}) {
  const expiry = input.expiresAt.toISOString();
  const businessName = input.businessName;

  const text = `Hello,

We're contacting you because ${businessName} appears in our local business directory at thetechprinciple.com.

We'd like to check that the contact details customers see for your business are accurate. Please review them using this secure link:

${input.verificationUrl}

This takes about a minute and does not require an account or password. Submitting sends the details for manual review; it does not publish changes automatically. This secure link expires ${expiry}.

If you believe this was sent in error, or you'd rather we didn't contact you about this listing, just reply to this email and let us know.

${SENDER_NAME}
${SENDER_CONTACT_EMAIL}
${SENDER_PHYSICAL_ADDRESS}`;

  const html = [
    `<p>Hello,</p>`,
    `<p>We're contacting you because <strong>${escapeHtml(businessName)}</strong> appears in our local business directory at thetechprinciple.com.</p>`,
    `<p>We'd like to check that the contact details customers see for your business are accurate.</p>`,
    `<p><a href="${escapeHtml(input.verificationUrl)}">Review and verify this listing</a></p>`,
    `<p>This takes about a minute and does not require an account or password. Submitting sends the details for manual review; it does not publish changes automatically. This secure link expires ${escapeHtml(expiry)}.</p>`,
    `<p>If you believe this was sent in error, or you'd rather we didn't contact you about this listing, just reply to this email and let us know.</p>`,
    `<p>${escapeHtml(SENDER_NAME)}<br>${escapeHtml(SENDER_CONTACT_EMAIL)}<br>${escapeHtml(SENDER_PHYSICAL_ADDRESS)}</p>`,
    input.trackingPixelUrl
      ? `<img src="${escapeHtml(input.trackingPixelUrl)}" width="1" height="1" alt="" style="display:none" />`
      : "",
  ].join("");

  return {
    subject: `Verify the listing for ${businessName}`,
    text, html,
  };
}

function escapeHtml(value: string) {
  return value.replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[character]!);
}
