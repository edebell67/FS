export const VERIFICATION_TEMPLATE_VERSION = "verification-v2-tracked";
export function renderVerificationEmail(input: {
  businessName: string; verificationUrl: string; trackingPixelUrl: string; expiresAt: Date;
}) {
  return {
    subject: `Verify the listing for ${input.businessName}`,
    text: `Please review the directory listing for ${input.businessName} using this secure link:\n\n${input.verificationUrl}\n\nThe link expires ${input.expiresAt.toISOString()}. Submitting sends the details for manual review; it does not publish changes automatically.`,
    html: `<p>Please review the directory listing for ${escapeHtml(input.businessName)}.</p><p><a href="${escapeHtml(input.verificationUrl)}">Review and verify this listing</a></p><p>This secure link expires ${escapeHtml(input.expiresAt.toISOString())}. Submitting sends the details for manual review; it does not publish changes automatically.</p><img src="${escapeHtml(input.trackingPixelUrl)}" width="1" height="1" alt="" style="display:none" />`,
  };
}

function escapeHtml(value: string) {
  return value.replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[character]!);
}
