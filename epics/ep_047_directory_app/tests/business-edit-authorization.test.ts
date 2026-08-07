// tests/business-edit-authorization.test.ts
//
// VERSION HISTORY
// v1.0.0 · 2026-08-06 · Initial version: covers the role-gating fix in
//   app/directoryadmin/businesses/[businessRef]/actions.ts v1.1.0. Found via an
//   audit of every "use server" action file for the same gap fixed on
//   moveStageAction (gap `role` on EP047_end_to_end_workflow_gap_register.html).
import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";

const root = new URL("..", import.meta.url);
async function source(path: string) { return readFile(new URL(path, root), "utf8"); }

test("updateBusinessAction requires operations authority, not just an authenticated session", async () => {
  const action = await source("app/directoryadmin/businesses/[businessRef]/actions.ts");
  assert.match(
    action,
    /canManageVerification\(user\.role\)/,
    "an authenticated session alone is not operations authority -- this action " +
      "can edit generatedSiteUrl and chatWidgetOptIn (the assistant activation flag)",
  );
  const userCheckIndex = action.indexOf("canManageVerification");
  const dbCallIndex = action.indexOf("updateBusinessDetails(");
  assert.ok(
    userCheckIndex > -1 && dbCallIndex > -1 && userCheckIndex < dbCallIndex,
    "the role check must run before the database write, not after",
  );
});

test("chatWidgetOptIn (assistant activation) is gated by the same authorization check as every other field", async () => {
  const action = await source("app/directoryadmin/businesses/[businessRef]/actions.ts");
  const authCheckIndex = action.indexOf("canManageVerification");
  const chatWidgetIndex = action.indexOf("chatWidgetOptIn");
  assert.ok(
    authCheckIndex > -1 && chatWidgetIndex > -1 && authCheckIndex < chatWidgetIndex,
    "the assistant activation flag must not be settable before the role check runs",
  );
});
