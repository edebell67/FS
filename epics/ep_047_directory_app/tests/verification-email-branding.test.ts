import assert from "node:assert/strict";
import test from "node:test";
import { renderVerificationEmail } from "../lib/verification/email-template";

test("verification email uses the established The Tech Principle brand shell and a review CTA", () => {
  const email = renderVerificationEmail({
    businessName: "Example Bathrooms",
    listingUrl: "https://thetechprinciple.com/directory/business/example-bathrooms",
    verificationUrl: "https://thetechprinciple.com/verify/example-capability",
    expiresAt: new Date("2026-08-17T09:00:00Z"),
  });

  assert.match(email.html, /<div class="brand">The Tech Principle<\/div>/);
  assert.match(email.html, /Local business directory &amp; website support/);
  assert.match(email.html, /class="cta" href="https:\/\/thetechprinciple\.com\/verify\/example-capability"/);
  assert.match(email.html, />Review and correct details<\/a>/);
  assert.match(email.html, /This is a service message about your business listing/);
  assert.match(email.text, /You can review and correct it here:/);
});
