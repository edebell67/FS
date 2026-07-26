CREATE TABLE IF NOT EXISTS verification_links (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  business_id uuid NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
  token_hash text NOT NULL UNIQUE,
  expires_at timestamptz NOT NULL,
  expires_in_days integer NOT NULL DEFAULT 5 CHECK (expires_in_days BETWEEN 1 AND 14),
  opened_at timestamptz, submitted_at timestamptz, revoked_at timestamptz,
  created_by_user_id uuid REFERENCES users(id),
  created_at timestamptz NOT NULL DEFAULT now()
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS verification_links_business_idx ON verification_links(business_id, created_at);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS verification_submissions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  link_id uuid NOT NULL UNIQUE REFERENCES verification_links(id),
  business_id uuid NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
  submitted_fields jsonb NOT NULL,
  relationship_to_business text NOT NULL,
  accuracy_confirmed_at timestamptz NOT NULL,
  privacy_notice_version text NOT NULL,
  requester_email text, requester_phone text,
  submitted_at timestamptz NOT NULL DEFAULT now()
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS verification_submissions_business_idx ON verification_submissions(business_id);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS claim_requests (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  business_id uuid NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
  submission_id uuid UNIQUE REFERENCES verification_submissions(id),
  status text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending_contact_verification','pending','approved','declined','withdrawn')),
  requester_name text NOT NULL,
  relationship text NOT NULL,
  contact_email text, contact_phone text, contact_fingerprint text,
  reviewer_user_id uuid REFERENCES users(id), reviewed_at timestamptz, decision_note text,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now()
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS claim_requests_business_idx ON claim_requests(business_id, status);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS claim_requests_contact_idx ON claim_requests(contact_fingerprint, created_at);
--> statement-breakpoint
CREATE UNIQUE INDEX IF NOT EXISTS claim_requests_one_active_submission_idx
  ON claim_requests(submission_id) WHERE submission_id IS NOT NULL AND status IN ('pending','approved');
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS verification_deliveries (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  claim_request_id uuid REFERENCES claim_requests(id),
  verification_link_id uuid NOT NULL REFERENCES verification_links(id),
  channel text NOT NULL DEFAULT 'email', recipient_address text NOT NULL,
  template_version text NOT NULL, actor_user_id uuid REFERENCES users(id),
  created_at timestamptz NOT NULL DEFAULT now(), sent_at timestamptz, failed_at timestamptz,
  provider_message_id text, failure_reason text
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS verification_deliveries_link_idx ON verification_deliveries(verification_link_id);
