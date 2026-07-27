-- Forward repair for deployments where migration 0008 was recorded without
-- adding delivery-tracking columns. This is intentionally additive and
-- idempotent: the business-detail delivery audit must render for both
-- pre-existing and newly created deliveries.
ALTER TABLE verification_deliveries
  ADD COLUMN IF NOT EXISTS status text NOT NULL DEFAULT 'prepared',
  ADD COLUMN IF NOT EXISTS delivery_mode text NOT NULL DEFAULT 'disabled',
  ADD COLUMN IF NOT EXISTS tracking_key_hash text,
  ADD COLUMN IF NOT EXISTS handoff_started_at timestamptz,
  ADD COLUMN IF NOT EXISTS opened_at timestamptz,
  ADD COLUMN IF NOT EXISTS clicked_at timestamptz,
  ADD COLUMN IF NOT EXISTS completed_at timestamptz,
  ADD COLUMN IF NOT EXISTS revoked_at timestamptz;
