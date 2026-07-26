export const VERIFICATION_TEMPLATE_VERSION = "verification-v1";
export function renderVerificationEmail(input: { businessName: string; verificationUrl: string; expiresAt: Date }) {
  return {
    subject: `Verify the listing for ${input.businessName}`,
    text: `Please review the directory listing for ${input.businessName} using this secure link:\n\n${input.verificationUrl}\n\nThe link expires ${input.expiresAt.toISOString()}. Submitting sends the details for manual review; it does not publish changes automatically.`,
  };
}
