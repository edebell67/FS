-- Backfill the supplied listing email for pending verification-origin claims
-- where the optional preferred-contact field was left blank.
UPDATE claim_requests AS claim
SET contact_email = NULLIF(BTRIM(submission.submitted_fields->>'email'), '')
FROM verification_submissions AS submission
WHERE claim.submission_id = submission.id
  AND claim.status = 'pending'
  AND claim.contact_email IS NULL
  AND NULLIF(BTRIM(submission.submitted_fields->>'email'), '') IS NOT NULL;
