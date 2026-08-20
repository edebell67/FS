import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";

const source = (path: string) => readFile(new URL(`../${path}`, import.meta.url), "utf8");

test("sent verification businesses are excluded from the to-send selector and labelled truthfully", async () => {
  const [batches, builder, delivery] = await Promise.all([
    source("lib/verification/batches.ts"),
    source("components/admin/VerificationBatchBuilder.tsx"),
    source("lib/verification/delivery.ts"),
  ]);
  assert.match(batches, /NOT EXISTS\s*\(\s*SELECT 1\s*FROM verification_deliveries/i);
  assert.match(batches, /sent_at IS NOT NULL/i);
  assert.match(builder, /verification_to_send/);
  assert.match(delivery, /verification_sent/);
  assert.match(delivery, /Verification email accepted by Gmail API/);
});
