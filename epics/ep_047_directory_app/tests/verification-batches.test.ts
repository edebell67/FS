import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { getDeliveryPolicy } from "../lib/verification/delivery";
import { normalizeBusinessIds } from "../lib/verification/batches";

const migrationPath = new URL("../migrations/0004_verification_batches.sql", import.meta.url);

test("batch migration durably relates batch, item, link and delivery audits", async () => {
  const sql = await readFile(migrationPath, "utf8");
  assert.match(sql, /CREATE TABLE IF NOT EXISTS verification_batches/i);
  assert.match(sql, /CREATE TABLE IF NOT EXISTS verification_batch_items/i);
  assert.match(sql, /verification_link_id uuid NOT NULL UNIQUE REFERENCES verification_links/i);
  assert.match(sql, /batch_item_id uuid REFERENCES verification_batch_items/i);
  assert.match(sql, /UNIQUE\(batch_id, business_id\)/i);
  assert.doesNotMatch(sql, /raw_token/i);
});

test("delivery policy is disabled without both explicit configuration and approval", () => {
  assert.deepEqual(getDeliveryPolicy({}).canSend, false);
  assert.equal(getDeliveryPolicy({ VERIFICATION_DELIVERY_MODE: "audit_only" }).approved, false);
  const approved = getDeliveryPolicy({
    VERIFICATION_DELIVERY_MODE: "audit_only",
    VERIFICATION_DELIVERY_APPROVED: "true",
  });
  assert.equal(approved.mode, "audit_only");
  assert.equal(approved.approved, true);
  assert.equal(approved.canSend, false);
});

test("batch selections reject empty, duplicate, malformed, and over-limit IDs", () => {
  const id = "00000000-0000-4000-8000-000000000001";
  assert.deepEqual(normalizeBusinessIds([id]), [id]);
  assert.throws(() => normalizeBusinessIds([]));
  assert.throws(() => normalizeBusinessIds([id, id]));
  assert.throws(() => normalizeBusinessIds(["not-an-id"]));
  assert.throws(() => normalizeBusinessIds(Array.from({ length: 251 }, (_, index) =>
    `00000000-0000-4000-8000-${String(index).padStart(12, "0")}`)));
});

test("batch preparation enforces calculated validation eligibility and partial policy inside its locking transaction", async () => {
  const source = await readFile(new URL("../lib/verification/batches.ts", import.meta.url), "utf8");
  assert.match(source, /b\.validation_status IN \('validated', 'partially_validated'\)/);
  assert.doesNotMatch(source, /p\.board_column = 'Validated'/);
  assert.match(source, /b\.status = 'active'/);
  assert.match(source, /FOR UPDATE OF b/);
  assert.match(source, /locked\.rows\.length !== businessIds\.length/);
  assert.match(source, /allowPartialVerification/);
  assert.match(source, /requestPartial/);
});

test("batch and single verification routes use role authorization", async () => {
  const batchRoute = await readFile(new URL("../app/directoryadmin/api/verification-batches/route.ts", import.meta.url), "utf8");
  const singleRoute = await readFile(new URL("../app/directoryadmin/api/businesses/[businessRef]/verification-link/route.ts", import.meta.url), "utf8");
  assert.match(batchRoute, /canManageVerification\(user\.role\)/);
  assert.match(singleRoute, /canManageVerification\(user\.role\)/);
});
