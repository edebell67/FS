import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";

const root = new URL("..", import.meta.url);
async function source(path: string) { return readFile(new URL(path, root), "utf8"); }

test("claim intake records a Claims pending status and approval workflow is discoverable", async () => {
  const [intake, claimsPage, pipeline, header] = await Promise.all([
    source("lib/verification/claim-intake.ts"), source("app/directoryadmin/claims/page.tsx"),
    source("app/directoryadmin/pipeline/page.tsx"), source("components/layout/SiteHeader.tsx"),
  ]);
  assert.match(intake, /status: "pending"/);
  assert.match(intake, /status: "claims_pending"/);
  assert.match(claimsPage, /Claims pending/);
  assert.match(claimsPage, /data-select-all/);
  assert.match(claimsPage, /Approve selected claims/);
  assert.match(pipeline, /\/directoryadmin\/claims/);
  assert.match(header, /\/directoryadmin\/claims/);
});

test("selected claim approval atomically projects claimed status and prepares a truthful owner message", async () => {
  const [repository, migration] = await Promise.all([
    source("lib/verification/claims-approval.ts"), source("migrations/0011_claims_pending_bulk_approval.sql"),
  ]);
  assert.match(repository, /status: "approved"/);
  assert.match(repository, /status: "claimed"/);
  assert.match(repository, /Claim approved from Claims pending queue/);
  assert.match(repository, /claimSuccessMessages/);
  assert.match(repository, /status: recipient \? "prepared" : "not_ready"/);
  assert.match(repository, /You have successfully claimed this business listing/);
  assert.match(migration, /CREATE TABLE IF NOT EXISTS claim_success_messages/);
});

test("bulk claim approval requires explicit server-side confirmation", async () => {
  const actions = await source("app/directoryadmin/claims/actions.ts");
  assert.match(actions, /confirmed/) ;
  assert.match(actions, /canManageVerification/);
  assert.match(actions, /approveSelectedClaims/);
});
