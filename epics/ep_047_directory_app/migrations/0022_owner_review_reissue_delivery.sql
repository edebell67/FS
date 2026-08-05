-- migrations/0022_owner_review_reissue_delivery.sql — Adds the separately audited owner-review invitation type.
--
-- VERSION HISTORY
-- v1.0.0 · 2026-08-05 · Extends the controlled preview-delivery audit enum without changing business state.
--
-- This migration is additive in behavior: it only permits a distinct audit
-- message type for an admin-authorized owner-review invitation. Do not run it
-- without an authorized migration operation.
ALTER TABLE preview_delivery_messages
  DROP CONSTRAINT IF EXISTS preview_delivery_messages_message_type_check;

ALTER TABLE preview_delivery_messages
  ADD CONSTRAINT preview_delivery_messages_message_type_check CHECK (message_type IN (
    'preview_ready', 'owner_review_invitation', 'eta', 'ready_for_activation',
    'reminder_intake', 'reminder_review', 'reminder_activation'
  ));
