import { test } from "node:test";
import assert from "node:assert/strict";

import { hashPassword, verifyPassword } from "../lib/auth/password";

test("password hashes verify only the original password", async () => {
  const hash = await hashPassword("correct horse battery staple");

  assert.notEqual(hash, "correct horse battery staple");
  assert.equal(await verifyPassword("correct horse battery staple", hash), true);
  assert.equal(await verifyPassword("wrong password", hash), false);
});
