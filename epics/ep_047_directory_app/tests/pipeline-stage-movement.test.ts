// tests/pipeline-stage-movement.test.ts
//
// VERSION HISTORY
// v1.1.0 · 2026-08-06 · Adds role-gating coverage for moveStageAction, matching
//   the fix in app/directoryadmin/pipeline/actions.ts v1.1.0.
// v1.0.0 · 2026-08-06 · Version history added; file predates this convention.
import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";
import { canMoveBetweenPipelineStages } from "../lib/pipeline/stage-movement-policy";

const root = new URL("..", import.meta.url);
async function source(path: string) { return readFile(new URL(path, root), "utf8"); }

test("generic moves reject every protected lifecycle stage as a destination", () => {
  for (const protectedStage of [
    "verification_email_pending",
    "business_claimed",
    "awaiting_site_generation",
    "ready_for_preview",
    "website_ready",
    "publish_requested",
    "website_published",
    "ai_assistant_available",
    "subscriber",
  ]) {
    assert.equal(canMoveBetweenPipelineStages("validated", protectedStage), false, protectedStage);
  }
});

test("generic moves reject every protected lifecycle stage as a source", () => {
  for (const protectedStage of [
    "verification_sent",
    "business_claimed",
    "awaiting_site_generation",
    "ready_for_preview",
    "website_viewed",
    "website_published",
    "ai_assistant_activated",
    "subscriber",
  ]) {
    assert.equal(canMoveBetweenPipelineStages(protectedStage, "validated"), false, protectedStage);
  }
});

test("generic moves preserve safe pre-lifecycle board movement", () => {
  assert.equal(canMoveBetweenPipelineStages("discovered", "imported"), true);
  assert.equal(canMoveBetweenPipelineStages("imported", "validated"), true);
  assert.equal(canMoveBetweenPipelineStages("validated", "categorised"), true);
});

test("generic database movement checks both the persisted source and requested destination", async () => {
  const pipeline = await source("lib/db/queries/pipeline.ts");
  assert.match(pipeline, /canMoveBetweenPipelineStages\(fromStage\.key, toStage\.key\)/);
  assert.match(pipeline, /protectedStageMoveError\(\)/);
});

test("the server action delegates movement to the guarded generic service", async () => {
  const action = await source("app/directoryadmin/pipeline/actions.ts");
  assert.match(action, /await moveBusinessToStage\(/);
  assert.doesNotMatch(action, /\.update\(businesses\)/);
});

test("the server action requires operations authority, not just an authenticated session", async () => {
  const action = await source("app/directoryadmin/pipeline/actions.ts");
  assert.match(
    action,
    /canManageVerification\(user\.role\)/,
    "moveStageAction must gate on role, not just presence of a session — " +
      "an authenticated session alone is not operations authority",
  );
  // The role check must run before any DB-affecting work, not after.
  const userCheckIndex = action.indexOf("canManageVerification");
  const dbCallIndex = action.indexOf("moveBusinessToStage(");
  assert.ok(userCheckIndex > -1 && dbCallIndex > -1 && userCheckIndex < dbCallIndex);
});
