CREATE TABLE IF NOT EXISTS claim_success_messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  claim_request_id uuid NOT NULL UNIQUE REFERENCES claim_requests(id) ON DELETE CASCADE,
  business_id uuid NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
  recipient_address text,
  status text NOT NULL DEFAULT 'prepared' CHECK (status IN ('prepared','sent','failed','not_ready')),
  subject text NOT NULL,
  text_body text NOT NULL,
  actor_user_id uuid REFERENCES users(id),
  provider_message_id text,
  failure_reason text,
  created_at timestamptz NOT NULL DEFAULT now(),
  sent_at timestamptz,
  failed_at timestamptz
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS claim_success_messages_status_idx
  ON claim_success_messages(status, created_at);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS claim_requests_pending_review_idx
  ON claim_requests(created_at)
  WHERE status IN ('pending','pending_contact_verification');
