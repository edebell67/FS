-- migrations/0021_owner_review_intake.sql — Durable capability-protected owner review submissions.
--
-- VERSION HISTORY
-- v1.0.0 · 2026-08-05 · Adds hashed owner-review links, immutable decisions, and per-page structured feedback without mail transport.
CREATE TABLE IF NOT EXISTS owner_review_links (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), business_id uuid NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
  token_hash text NOT NULL UNIQUE, expires_at timestamptz NOT NULL, opened_at timestamptz, submitted_at timestamptz, revoked_at timestamptz,
  created_by_user_id uuid REFERENCES users(id), created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS owner_review_submissions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), link_id uuid NOT NULL UNIQUE REFERENCES owner_review_links(id),
  business_id uuid NOT NULL REFERENCES businesses(id) ON DELETE CASCADE, decision text NOT NULL CHECK (decision IN ('accept','change','decline')),
  submitted_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS owner_review_page_responses (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), submission_id uuid NOT NULL REFERENCES owner_review_submissions(id) ON DELETE CASCADE,
  page_key text NOT NULL, no_action_required boolean NOT NULL DEFAULT true, selections jsonb NOT NULL DEFAULT '[]'::jsonb,
  anything_else text NOT NULL DEFAULT '', page_open_date_time timestamptz, UNIQUE(submission_id, page_key)
);
CREATE INDEX IF NOT EXISTS owner_review_links_business_idx ON owner_review_links(business_id, created_at DESC);
CREATE INDEX IF NOT EXISTS owner_review_submissions_business_idx ON owner_review_submissions(business_id, submitted_at DESC);
