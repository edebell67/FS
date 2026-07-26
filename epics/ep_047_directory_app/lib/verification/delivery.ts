import { db } from "@/lib/db/client";
import { verificationDeliveries } from "@/lib/db/schema";
import { VERIFICATION_TEMPLATE_VERSION, renderVerificationEmail } from "./email-template";

export type DeliveryMode = "disabled" | "audit_only";

/**
 * A second, explicit approval flag is required even for a configured mode.
 * There is intentionally no network provider in this implementation.
 */
export function getDeliveryPolicy(env: Partial<Record<string, string | undefined>> = process.env) {
  const requested = env.VERIFICATION_DELIVERY_MODE;
  const mode: DeliveryMode = requested === "audit_only" ? "audit_only" : "disabled";
  const approved = env.VERIFICATION_DELIVERY_APPROVED === "true";
  return {
    mode,
    approved,
    canSend: false as const,
    reason: mode === "disabled"
      ? "Outbound delivery is disabled."
      : approved
        ? "Audit-only mode is approved; no provider is installed."
        : "Delivery mode has not been explicitly approved.",
  };
}

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
    status: "prepared", deliveryMode: getDeliveryPolicy().mode,
  }).returning({ id: verificationDeliveries.id });
  if (!audit) throw new Error("Unable to record delivery preview.");
  return { auditId: audit.id, message, deliveryEnabled: false as const };
}

export async function sendPreparedDelivery(): Promise<never> {
  const policy = getDeliveryPolicy();
  throw new Error(`${policy.reason} Network delivery is unavailable by design.`);
}
