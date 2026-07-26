export type VerificationDeliveryState =
  | "not_sent"
  | "queued"
  | "sent"
  | "delivered"
  | "bounced"
  | "failed"
  | "revoked";

const PRESENTATION: Record<
  VerificationDeliveryState,
  { label: string; explanation?: string }
> = {
  not_sent: {
    label: "Not sent — preview only",
    explanation: "No external delivery is enabled.",
  },
  queued: { label: "Queued" },
  sent: { label: "Sent" },
  delivered: { label: "Delivered" },
  bounced: { label: "Bounced" },
  failed: { label: "Failed" },
  revoked: { label: "Revoked" },
};

export function getDeliveryStatePresentation(state: VerificationDeliveryState) {
  return PRESENTATION[state];
}
