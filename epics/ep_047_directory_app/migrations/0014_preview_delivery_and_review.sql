-- migrations/0014_preview_delivery_and_review.sql — businesses columns and the
-- message table backing the preview-delivery-and-review workflow.
--
-- VERSION HISTORY
-- v1.0.0 · 2026-07-29 · Initial version: 6 additive businesses columns (generated
--   site URL, generation timestamp, reminder/ETA timestamps, next service date)
--   plus preview_delivery_messages, one table keyed by message_type so reminders
--   are their own records rather than resends of the message they nudge.

-- EP047: Preview delivery and review workflow (schema step only, payment
-- excluded as a self-contained follow-up unit per its own workflow doc).
-- Additive only: no existing column is altered or dropped.

ALTER TABLE businesses
  ADD COLUMN IF NOT EXISTS generated_site_url text,
  ADD COLUMN IF NOT EXISTS website_generated_at timestamptz,
  ADD COLUMN IF NOT EXISTS awaiting_owner_response_since timestamptz,
  ADD COLUMN IF NOT EXISTS ready_for_activation_set_at timestamptz,
  ADD COLUMN IF NOT EXISTS ready_for_activation_date timestamptz,
  ADD COLUMN IF NOT EXISTS next_service_date timestamptz;

CREATE TABLE IF NOT EXISTS preview_delivery_messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  business_id uuid NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
  message_type text NOT NULL CHECK (message_type IN (
    'preview_ready', 'eta', 'ready_for_activation',
    'reminder_intake', 'reminder_review', 'reminder_activation'
  )),
  recipient_address text,
  status text NOT NULL DEFAULT 'prepared' CHECK (status IN ('prepared', 'sent', 'failed')),
  subject text NOT NULL,
  text_body text NOT NULL,
  actor_user_id uuid REFERENCES users(id),
  provider_message_id text,
  failure_reason text,
  created_at timestamptz NOT NULL DEFAULT now(),
  sent_at timestamptz,
  failed_at timestamptz
);

CREATE INDEX IF NOT EXISTS preview_delivery_messages_business_type_idx
  ON preview_delivery_messages (business_id, message_type, created_at);
