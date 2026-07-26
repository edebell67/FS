export type VerificationDeliveryState =
  | "prepared" | "sent" | "opened" | "clicked"
  | "completed" | "failed" | "revoked";

const PRESENTATION: Record<
  VerificationDeliveryState,
  { label: string; explanation?: string }
> = {
  prepared: { label: "Prepared", explanation: "Preview created; no email has been sent." },
  sent: { label: "Sent", explanation: "The SMTP provider accepted handoff; delivery is not guaranteed." },
  opened: { label: "Opened (best effort)", explanation: "A tracking pixel was requested; this signal may be incomplete." },
  clicked: { label: "Clicked", explanation: "The tracked verification link was followed." },
  completed: { label: "Completed", explanation: "The recipient submitted the verification form." },
  failed: { label: "Failed", explanation: "The SMTP provider did not accept handoff." },
  revoked: { label: "Revoked", explanation: "This verification capability can no longer be used." },
};

export function getDeliveryStatePresentation(state: VerificationDeliveryState) {
  return PRESENTATION[state];
}
