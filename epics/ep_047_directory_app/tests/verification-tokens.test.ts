import test from "node:test";
import assert from "node:assert/strict";
import {
  generateVerificationToken, hashVerificationToken, isValidRawToken, normalizeExpiryDays,
} from "../lib/verification/tokens";

test("verification tokens are 256-bit base64url capabilities and only hashes persist", () => {
  const token = generateVerificationToken();
  assert.equal(isValidRawToken(token), true);
  assert.equal(Buffer.from(token, "base64url").length, 32);
  const hash = hashVerificationToken(token);
  assert.match(hash, /^[a-f0-9]{64}$/);
  assert.notEqual(hash, token);
});

test("verification expiry defaults to five days and is bounded", () => {
  assert.equal(normalizeExpiryDays(undefined), 5);
  assert.equal(normalizeExpiryDays(1), 1);
  assert.equal(normalizeExpiryDays(14), 14);
  assert.throws(() => normalizeExpiryDays(0));
  assert.throws(() => normalizeExpiryDays(15));
  assert.throws(() => normalizeExpiryDays(1.5));
});

test("malformed tokens are rejected before lookup", () => {
  assert.equal(isValidRawToken("short"), false);
  assert.equal(isValidRawToken("x".repeat(43)), true);
  assert.equal(isValidRawToken(`${"x".repeat(42)}+`), false);
});
