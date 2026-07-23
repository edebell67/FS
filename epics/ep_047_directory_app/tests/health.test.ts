// Phase 0 smoke test. Confirms the route module loads and exports a GET
// handler — full request/response integration testing (against a real
// Postgres) is wired up in Phase 1 once there's schema worth asserting on.

import { test } from "node:test";
import assert from "node:assert/strict";

test("health route exports a GET handler", async () => {
  const mod = await import("../app/api/health/route");
  assert.equal(typeof mod.GET, "function");
});
