import assert from "node:assert/strict";
import test from "node:test";
import { renderVerificationEmail } from "../lib/verification/email-template";

test("verification email uses the approved black-and-lime TTP hierarchy and CTA pair", () => {
  const email = renderVerificationEmail({
    businessName: "Example Bathrooms",
    listingUrl: "https://thetechprinciple.com/directory/business/example-bathrooms",
    verificationUrl: "https://thetechprinciple.com/verify/example-capability",
    expiresAt: new Date("2026-08-17T09:00:00Z"),
  });

  assert.match(email.html, /background:#111111/);
  assert.match(email.html, /background:#d7f542;color:#111111/);
  assert.match(email.html, />Review and correct details<\/a>/);
  assert.match(email.html, />View public listing<\/a>/);
  assert.match(email.html, /This is a service message about your business listing/);
  assert.doesNotMatch(email.html, /prepared message has not been sent/i);
  assert.doesNotMatch(email.html, />https:\/\/thetechprinciple\.com\//);
});
