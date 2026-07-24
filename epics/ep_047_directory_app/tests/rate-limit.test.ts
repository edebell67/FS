import { test } from "node:test";
import assert from "node:assert/strict";

import { isRateLimited, recordFailedAttempt, clearFailedAttempts } from "../lib/auth/rate-limit";

test("an email with no failed attempts is not rate limited", () => {
  assert.equal(isRateLimited("nobody-tried-this@example.com"), false);
});

test("rate limiting kicks in after 5 failed attempts and email is case-insensitive", () => {
  const email = "rate-limit-target@example.com";
  for (let i = 0; i < 4; i++) {
    recordFailedAttempt(email);
    assert.equal(isRateLimited(email), false, `should not be limited after ${i + 1} attempts`);
  }
  recordFailedAttempt(email);
  assert.equal(isRateLimited(email), true);
  // Case-insensitive: the same account tried with different casing still counts.
  assert.equal(isRateLimited(email.toUpperCase()), true);
});

test("clearFailedAttempts resets the counter", () => {
  const email = "clears-ok@example.com";
  for (let i = 0; i < 5; i++) recordFailedAttempt(email);
  assert.equal(isRateLimited(email), true);

  clearFailedAttempts(email);
  assert.equal(isRateLimited(email), false);
});

test("rate limiting is scoped per email", () => {
  const target = "victim@example.com";
  const other = "someone-else@example.com";
  for (let i = 0; i < 5; i++) recordFailedAttempt(target);

  assert.equal(isRateLimited(target), true);
  assert.equal(isRateLimited(other), false);
});
