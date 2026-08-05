import test from "node:test";
import assert from "node:assert/strict";
import { buildDailySourcePlan } from "../src/daily-source-rotation.js";

const source = (id, status = "enabled") => ({ id, status, name: id, publisher: id, kind: "official_council", towns: ["bristol"], allowedHosts: ["example.org"], discovery: { mode: "manual_research", url: "https://example.org" }, coverage: { categories: ["builders"], priority: "primary" }, termsDecision: status === "enabled" ? "permitted_link_and_fact_extraction" : "curator_review_required", termsCheckedAt: status === "enabled" ? "2026-08-05" : null, reviewDueAt: "2026-11-05" });

test("daily plan is deterministic and rotates enabled sources", () => {
  const registry = [source("bristol-a"), source("bristol-b"), source("bristol-draft", "draft")];
  const first = buildDailySourcePlan({ date: "2026-08-05", eligibleTowns: ["bristol", "leeds"], registry });
  const next = buildDailySourcePlan({ date: "2026-08-06", eligibleTowns: ["bristol", "leeds"], registry });
  assert.equal(first.selections.length, 1);
  assert.notEqual(first.selections[0].sourceId, next.selections[0].sourceId);
  assert.deepEqual(first.uncoveredTowns, ["leeds"]);
  assert.deepEqual(first, buildDailySourcePlan({ date: "2026-08-05", eligibleTowns: ["bristol", "leeds"], registry }));
});
