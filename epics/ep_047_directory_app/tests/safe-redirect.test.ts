import { test } from "node:test";
import assert from "node:assert/strict";

import { safeNextPath } from "../lib/auth/safe-redirect";

test("safeNextPath allows a same-site admin path", () => {
  assert.equal(safeNextPath("/directoryadmin/pipeline"), "/directoryadmin/pipeline");
});

test("safeNextPath falls back to the dashboard for null/empty", () => {
  assert.equal(safeNextPath(null), "/directoryadmin/dashboard");
  assert.equal(safeNextPath(undefined), "/directoryadmin/dashboard");
  assert.equal(safeNextPath(""), "/directoryadmin/dashboard");
});

test("safeNextPath rejects a path outside /directoryadmin", () => {
  assert.equal(safeNextPath("/directory"), "/directoryadmin/dashboard");
  assert.equal(safeNextPath("/admin/pipeline"), "/directoryadmin/dashboard");
});

test("safeNextPath rejects an absolute URL (open-redirect attempt)", () => {
  assert.equal(safeNextPath("https://evil.example/steal"), "/directoryadmin/dashboard");
  assert.equal(safeNextPath("http://evil.example/directoryadmin/x"), "/directoryadmin/dashboard");
});

test("safeNextPath rejects a protocol-relative URL (open-redirect attempt)", () => {
  assert.equal(safeNextPath("//evil.example/directoryadmin"), "/directoryadmin/dashboard");
});
