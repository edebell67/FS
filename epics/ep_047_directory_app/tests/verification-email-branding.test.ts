import assert from "node:assert/strict";
import test from "node:test";
import { renderVerificationEmail } from "../lib/verification/email-template";

test("verification email uses the approved black-and-lime TTP hierarchy and CTA pair", () => {
  const verificationUrl = "https://thetechprinciple.com/verify/example-capability";
  const listingUrl = "https://thetechprinciple.com/directory/business/example-bathrooms";
  const email = renderVerificationEmail({ businessName: "Example Bathrooms", listingUrl, verificationUrl, expiresAt: new Date("2026-08-17T09:00:00Z") });
  assert.match(email.html, /background:#080808/);
  assert.match(email.html, /background:#b6ff00/);
  assert.match(email.html, />Review and correct details<\/a>/);
  assert.match(email.html, />View public listing<\/a>/);
  assert.match(email.html, /This is a service message about your business listing/);
  assert.doesNotMatch(email.html, /prepared message has not been sent/i);
  assert.doesNotMatch(email.html, />https:\/\/thetechprinciple\.com\//);
  assert.match(email.text, new RegExp(verificationUrl));
  assert.match(email.text, new RegExp(listingUrl));
});
