import assert from "node:assert/strict";
import test from "node:test";
import { canRequestPublicClaim } from "../lib/verification/claim-eligibility";

test("public claims are unavailable before a verification is completed", () => {
  assert.equal(canRequestPublicClaim("verification_email_pending"), false);
  assert.equal(canRequestPublicClaim("verification_sent"), false);
  assert.equal(canRequestPublicClaim("verification_opened"), false);
  assert.equal(canRequestPublicClaim(null), false);
});

test("public claims become available only after verification is completed", () => {
  assert.equal(canRequestPublicClaim("verification_completed"), true);
  assert.equal(canRequestPublicClaim("business_claimed"), false);
});
