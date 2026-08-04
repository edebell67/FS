import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";

const source = (path: string) => readFile(new URL(`../${path}`, import.meta.url), "utf8");

test("pipeline mounts an admin-only workflow modal instead of routing to a separate control page", async () => {
  const page = await source("app/directoryadmin/pipeline/page.tsx");
  assert.match(page, /WorkflowControlModal/);
  const modal = await source("components/admin/WorkflowControlModal.tsx");
  assert.match(modal, /Open workflow control/);
});

test("workflow control exposes the ordered lifecycle and confirmations", async () => {
  const modal = await source("components/admin/WorkflowControlModal.tsx");
  for (const label of [
    "Import businesses",
    "Run field validation",
    "Prepare verification batch",
    "Send verification emails",
    "Review and approve claims",
    "Run site generation",
    "Send site preview links",
  ]) assert.match(modal, new RegExp(label));
  assert.match(modal, /window\.confirm/);
  assert.match(modal, /role="dialog"/);
});

test("workflow actions re-check eligibility server side and use protected domain services", async () => {
  const actions = await source("app/directoryadmin/workflow/actions.ts");
  assert.match(actions, /requireAdminUserForPage/);
  assert.match(actions, /canManageVerification/);
  assert.match(actions, /startBusinessValidationJob/);
  assert.match(actions, /prepareVerificationBatch/);
  assert.match(actions, /approveSelectedClaims/);
  assert.match(actions, /runGenerationLoop/);
  assert.match(actions, /getBusinessesReadyForPreviewNotification/);
  assert.doesNotMatch(actions, /moveBusinessToStage/);
  assert.doesNotMatch(actions, /moveStageAction/);
});

test("generation is not offered as a completion operation without a configured real generation path", async () => {
  const page = await source("app/directoryadmin/pipeline/page.tsx");
  assert.match(page, /generationAvailable/);
  const actions = await source("app/directoryadmin/workflow/actions.ts");
  assert.match(actions, /generationPathAvailable/);
  assert.match(actions, /Generation is not configured/);
});
