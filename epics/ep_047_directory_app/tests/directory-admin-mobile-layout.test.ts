import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const routeFiles = [
  "app/directoryadmin/dashboard/page.tsx",
  "app/directoryadmin/pipeline/page.tsx",
  "app/directoryadmin/claims/page.tsx",
  "app/directoryadmin/businesses/page.tsx",
  "app/directoryadmin/businesses/[businessRef]/page.tsx",
  "app/directoryadmin/verifications/[claimRequestId]/page.tsx",
  "app/directoryadmin/login/page.tsx",
];

async function routeSource(path: string) {
  return readFile(new URL(`../${path}`, import.meta.url), "utf8");
}

test("directory admin routes use 360px-safe horizontal gutters", async () => {
  for (const path of routeFiles) {
    const source = await routeSource(path);
    assert.match(source, /px-4\b[^"\n]{0,40}\bsm:px-6/, `${path} must use 16px mobile gutters before wider-screen gutters`);
  }
});

test("directory admin tables are announced, horizontally scrollable regions", async () => {
  for (const path of [
    "app/directoryadmin/dashboard/page.tsx",
    "app/directoryadmin/claims/page.tsx",
    "app/directoryadmin/businesses/page.tsx",
  ]) {
    const source = await routeSource(path);
    assert.match(source, /role="region"[\s\S]{0,160}aria-label="[^"]+"[\s\S]{0,160}overflow-x-auto/, `${path} table wrapper must be a labelled scroll region`);
    assert.match(source, /<table className="min-w-max w-full/, `${path} table must retain readable column widths while its labelled wrapper scrolls`);
  }
});

test("directory admin dense layouts stack actions and grids before the sm breakpoint", async () => {
  const dashboard = await routeSource("app/directoryadmin/dashboard/page.tsx");
  assert.match(dashboard, /grid-cols-1\s+gap-3\s+sm:grid-cols-3/, "dashboard import stats must not force three columns at 360px");
  assert.match(dashboard, /flex-col\s+gap-2\s+sm:flex-row/, "dashboard header actions must stack at 360px");

  const pipeline = await routeSource("app/directoryadmin/pipeline/page.tsx");
  assert.match(pipeline, /flex-col\s+gap-1\.5\s+sm:flex-row/, "pipeline card move form must stack at 360px");

  const businesses = await routeSource("app/directoryadmin/businesses/page.tsx");
  assert.match(businesses, /flex-col\s+items-start\s+gap-3\s+sm:flex-row/, "businesses header and pagination must stack at 360px");
  assert.match(businesses, /flex-col\s+items-stretch\s+gap-3(?:\s+sm:[^\s"]+)*\s+sm:flex-row/, "business filter actions must stack at 360px");

  const detail = await routeSource("app/directoryadmin/businesses/[businessRef]/page.tsx");
  assert.match(detail, /flex-col\s+items-start\s+gap-4\s+sm:flex-row/, "business detail header must stack at 360px");
  assert.match(detail, /flex-col\s+items-stretch\s+gap-3(?:\s+(?!sm:flex-row)[^\s"]+)*\s+sm:flex-row/, "business stage actions must stack at 360px");
});
