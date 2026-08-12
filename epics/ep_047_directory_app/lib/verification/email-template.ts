import { escapeEmailHtml, renderTheTechPrincipleEmail } from "@/lib/email/brand";

export const VERIFICATION_TEMPLATE_VERSION = "verification-v7-ttp-black-lime";
const SENDER_PERSON = "Edward Bell";
const SENDER_NAME = "The Tech Principle";
const SENDER_CONTACT_EMAIL = "edward.bell@thetechprinciple.com";

export function senderPhysicalAddress(
  env: { VERIFICATION_SENDER_ADDRESS?: string } = process.env as { VERIFICATION_SENDER_ADDRESS?: string },
): string { return env.VERIFICATION_SENDER_ADDRESS?.trim() ?? ""; }

export function renderVerificationEmail(input: {
  businessName: string; verificationUrl: string; listingUrl: string;
  trackingPixelUrl?: string; expiresAt: Date;
}) {
  const expiry = input.expiresAt.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric", timeZone: "Europe/London" });
  const address = senderPhysicalAddress() || "[Registered business address — to be added]";
  const text = `Hello,

${input.businessName} is listed on thetechprinciple.com, our local business directory. You can view the public listing here:

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
  const bodyHtml = [
    `<p style="margin:0 0 16px">Hello,</p>`,
    `<p style="margin:0 0 16px"><strong>${escapeEmailHtml(input.businessName)}</strong> is listed in our local business directory. People use it to find contact details, opening hours and directions for local businesses — so we'd like to make sure yours is right.</p>`,
    `<p style="margin:0 0 16px">No account or password is needed. Submitted changes are checked manually; nothing is published automatically.</p>`,
    `<p style="margin:0 0 16px">The review link is unique to your listing and expires on ${escapeEmailHtml(expiry)}.</p>`,
    `<p style="margin:0 0 20px">If this isn't your business, or you'd rather we didn't contact you about this listing, reply to this email and we'll take care of it.</p>`,
    input.trackingPixelUrl ? `<img src="${escapeEmailHtml(input.trackingPixelUrl)}" width="1" height="1" alt="" style="display:none" />` : "",
  ].join("");
  const html = renderTheTechPrincipleEmail({
    eyebrow: "Listing verification", heading: `Is this the right contact info for ${input.businessName}?`, bodyHtml,
    ctas: [
      { href: input.verificationUrl, label: "Review and correct details", tone: "lime" },
      { href: input.listingUrl, label: "View public listing", tone: "black" },
    ],
    footerDetail: `${escapeEmailHtml(address)}<br><br>This is a service message about your business listing. Reply to this email for support or to update your contact preferences.`,
  });
  return { subject: `Is this the right contact info for ${input.businessName}?`, text, html };
}
