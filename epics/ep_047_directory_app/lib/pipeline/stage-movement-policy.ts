// Generic board movement is intentionally limited to pre-lifecycle triage.
// Every later state has a dedicated, eligibility-checking workflow service.
const PROTECTED_LIFECYCLE_STAGE_KEYS = new Set([
  "directory_published",
  "verification_email_pending",
  "verification_sent",
  "verification_opened",
  "verification_completed",
  "business_claimed",
  "awaiting_site_generation",
  "ready_for_preview",
  "site_in_review",
  "website_generated",
  "website_viewed",
  "website_ready",
  "publish_requested",
  "website_published",
  "ai_assistant_available",
  "ai_assistant_activated",
  "lead_received",
  "customer_contacted",
  "subscriber",
  "cancelled",
  "archived",
]);

export function canMoveBetweenPipelineStages(fromStageKey: string, toStageKey: string): boolean {
  return !PROTECTED_LIFECYCLE_STAGE_KEYS.has(fromStageKey)
    && !PROTECTED_LIFECYCLE_STAGE_KEYS.has(toStageKey);
}

export function protectedStageMoveError(): string {
  return "Protected lifecycle stages require their controlled workflow.";
}
