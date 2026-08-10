import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";

test("batch send aggregate states are valid database states", async () => {
  const [migration, batches] = await Promise.all([
    readFile(new URL("../migrations/0024_verification_batch_send_status.sql", import.meta.url), "utf8"),
    readFile(new URL("../lib/verification/batches.ts", import.meta.url), "utf8"),
  ]);
  assert.match(migration, /DROP CONSTRAINT IF EXISTS verification_batches_status_check/);
  for (const state of ["sent", "partially_sent", "failed"]) assert.match(migration, new RegExp(`'${state}'`));
  assert.match(batches, /const status = outcome\.failed/);
});
