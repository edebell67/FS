import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";

test("batch verification sending is role-protected, explicitly confirmed, and reports per-recipient outcomes", async () => {
  const [route, batches] = await Promise.all([
    readFile(new URL("../app/directoryadmin/api/verification-batches/[batchId]/send/route.ts", import.meta.url), "utf8"),
    readFile(new URL("../lib/verification/batches.ts", import.meta.url), "utf8"),
  ]);
  assert.match(route, /canManageVerification\(user\.role\)/);
  assert.match(route, /body\.confirmed !== true/);
  assert.match(route, /sendPreparedVerificationBatch/);
  assert.match(batches, /generateVerificationToken\(\)/);
  assert.match(batches, /sendPreparedDelivery/);
  assert.match(batches, /sent: 0, failed: 0, skipped: 0/);
  assert.match(batches, /Prepared delivery recipient no longer matches the business email/);
});
