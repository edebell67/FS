-- Permit durable aggregate outcomes produced by explicit batch email sending.
-- Per-recipient delivery remains the source of truth; this is an audit summary only.
ALTER TABLE verification_batches DROP CONSTRAINT IF EXISTS verification_batches_status_check;
ALTER TABLE verification_batches ADD CONSTRAINT verification_batches_status_check
  CHECK (status IN ('prepared','partially_ready','ready','cancelled','sent','partially_sent','failed'));
