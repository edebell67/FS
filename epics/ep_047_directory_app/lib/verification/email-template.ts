/**
 * lib/verification/email-template.ts — renders the business-verification email.
 *
 * VERSION HISTORY
 * v1.4.0 · 2026-08-10 · Moves verification delivery onto the approved shared
 *   black-and-lime The Tech Principle HTML system, retaining the plain-text
 *   fallback and making the complete sender address a hard delivery gate.
 * v1.3.0 · 2026-08-10 · Leads with why the listing matters, links the public
 *   directory, formats expiry as a human date, and drops phishing-like wording.
 */

export const VERIFICATION_TEMPLATE_VERSION = "verification-v6-ttp-black-lime";

const SENDER_PERSON = "Edward Bell";
const SENDER_NAME = "The Tech Principle";
const SENDER_CONTACT_EMAIL = "edward.bell@thetechprinciple.com";

export function senderPhysicalAddress(
  env: { VERIFICATION_SENDER_ADDRESS?: string } = process.env as { VERIFICATION_SENDER_ADDRESS?: string },
): string {
  return env.VERIFICATION_SENDER_ADDRESS?.trim() ?? "";
}

export function renderVerificationEmail(input: {
  businessName: string; verificationUrl: string; listingUrl: string;
  trackingPixelUrl?: string; expiresAt: Date;
}) {
  const expiry = input.expiresAt.toLocaleDateString("en-GB", {
    day: "numeric", month: "long", year: "numeric", timeZone: "Europe/London",
  });
  const address = senderPhysicalAddress() || "[Registered business address — to be added]";
  const businessName = input.businessName;

  const text = `Hello,

${businessName} is listed on thetechprinciple.com, our local business directory. You can view the public listing here:

${input.listingUrl}

People use the directory to find contact details, opening hours and directions for local businesses — so we'd like to make sure yours is right.

Review and correct details:
${input.verificationUrl}

It takes about a minute and doesn't need an account or password. Submitting sends your details for manual review; nothing is published automatically. This link is unique to your listing and expires on ${expiry}.

If this isn't your business, or you'd rather we didn't contact you about this listing, reply to this email and we'll take care of it.

${SENDER_PERSON}
${SENDER_NAME}
${SENDER_CONTACT_EMAIL}
${address}`;

  const html = `<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f2f2ee;color:#111111;font-family:Arial,Helvetica,sans-serif">
  <div style="max-width:620px;margin:0 auto;padding:32px 16px">
    <div style="background:#ffffff;border:1px solid #dfdfd8">
      <div style="background:#111111;padding:28px 32px">
        <div style="color:#ffffff;font-family:Georgia,'Times New Roman',serif;font-size:24px;font-weight:700;line-height:1.15">The Tech Principle</div>
        <div style="width:58px;height:4px;background:#d7f542;margin-top:14px"></div>
      </div>
      <div style="padding:32px;line-height:1.6;font-size:16px">
        <div style="color:#5b6400;font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase">Listing verification</div>
        <h1 style="margin:10px 0 18px;color:#111111;font-family:Georgia,'Times New Roman',serif;font-size:26px;line-height:1.25">Is this the right contact info for ${escapeHtml(businessName)}?</h1>
        <p style="margin:0 0 16px">Hello,</p>
        <p style="margin:0 0 16px"><strong>${escapeHtml(businessName)}</strong> is listed in our local business directory. People use it to find contact details, opening hours and directions for local businesses — so we'd like to make sure yours is right.</p>
        <p style="margin:0 0 22px">No account or password is needed. Submitted changes are checked manually; nothing is published automatically.</p>
        <div style="margin:0 0 12px"><a href="${escapeHtml(input.verificationUrl)}" style="background:#d7f542;color:#111111;display:inline-block;font-weight:700;padding:14px 20px;text-decoration:none">Review and correct details</a></div>
        <div style="margin:0 0 24px"><a href="${escapeHtml(input.listingUrl)}" style="background:#111111;color:#ffffff;display:inline-block;font-weight:700;padding:13px 19px;text-decoration:none">View public listing</a></div>
        <p style="margin:0 0 16px">The review link is unique to your listing and expires on ${escapeHtml(expiry)}.</p>
        <p style="margin:0 0 20px">If this isn't your business, or you'd rather we didn't contact you about this listing, reply to this email and we'll take care of it.</p>
        <p style="margin:0">${escapeHtml(SENDER_PERSON)}<br>${escapeHtml(SENDER_NAME)}<br><a href="mailto:${escapeHtml(SENDER_CONTACT_EMAIL)}" style="color:#111111">${escapeHtml(SENDER_CONTACT_EMAIL)}</a></p>
      </div>
      <div style="border-top:1px solid #dfdfd8;padding:22px 32px;color:#50504b;font-size:12px;line-height:1.55">
        <strong style="color:#111111">The Tech Principle</strong><br>
        ${escapeHtml(address)}<br>
        This is a service message about your business listing. Reply to this email for support or to update your contact preferences.
      </div>
    </div>
  </div>
  ${input.trackingPixelUrl ? `<img src="${escapeHtml(input.trackingPixelUrl)}" width="1" height="1" alt="" style="display:none" />` : ""}
</body>
</html>`;

  return { subject: `Is this the right contact info for ${businessName}?`, text, html };
}

function escapeHtml(value: string) {
  return value.replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[character]!);
}
