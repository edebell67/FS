import { db } from "@/lib/db/client";
import { verificationDeliveries } from "@/lib/db/schema";
import { VERIFICATION_TEMPLATE_VERSION, renderVerificationEmail } from "./email-template";

/** Preview-only by policy: this module deliberately has no network/provider adapter. */
export async function prepareDeliveryPreview(input: {
  claimRequestId?: string; verificationLinkId: string; recipientAddress: string;
  actorUserId: string; businessName: string; verificationUrl: string; expiresAt: Date;
}) {
  const message = renderVerificationEmail(input);
  const [audit] = await db.insert(verificationDeliveries).values({
    claimRequestId: input.claimRequestId, verificationLinkId: input.verificationLinkId,
    channel: "email", recipientAddress: input.recipientAddress,
    templateVersion: VERIFICATION_TEMPLATE_VERSION, actorUserId: input.actorUserId,
  }).returning({ id: verificationDeliveries.id });
  if (!audit) throw new Error("Unable to record delivery preview.");
  return { auditId: audit.id, message, deliveryEnabled: false as const };
}
