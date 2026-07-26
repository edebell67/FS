import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const migrationPath = new URL("../migrations/0003_business_verification.sql", import.meta.url);
test("verification migration enforces capability and audit relationships", async () => {
  const sql = await readFile(migrationPath, "utf8");
  assert.match(sql, /token_hash text NOT NULL UNIQUE/i);
  assert.match(sql, /expires_in_days integer NOT NULL DEFAULT 5 CHECK \(expires_in_days BETWEEN 1 AND 14\)/i);
  assert.match(sql, /link_id uuid NOT NULL UNIQUE REFERENCES verification_links/i);
  assert.match(sql, /submission_id uuid UNIQUE REFERENCES verification_submissions/i);
  assert.match(sql, /status text NOT NULL DEFAULT 'pending'/i);
  assert.doesNotMatch(sql, /raw_token/i);
});

test("delivery audit has no raw-token column", async () => {
  const sql = await readFile(migrationPath, "utf8");
  const delivery = sql.slice(sql.indexOf("CREATE TABLE IF NOT EXISTS verification_deliveries"));
  assert.doesNotMatch(delivery, /token_hash|raw_token/);
  assert.match(delivery, /verification_link_id uuid NOT NULL REFERENCES verification_links/);
});
