import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const routeFiles = {
  importClient: new URL("../app/directoryadmin/import/ImportPageClient.tsx", import.meta.url),
  validation: new URL("../app/directoryadmin/validation/page.tsx", import.meta.url),
  validationPanel: new URL("../app/directoryadmin/validation/ValidationJobPanel.tsx", import.meta.url),
  batches: new URL("../app/directoryadmin/verification-batches/page.tsx", import.meta.url),
  batchDetail: new URL("../app/directoryadmin/verification-batches/[batchId]/page.tsx", import.meta.url),
  visibility: new URL("../app/directoryadmin/visibility/page.tsx", import.meta.url),
  visibilityPreview: new URL("../app/directoryadmin/visibility/preview/page.tsx", import.meta.url),
};

async function source(file: URL) {
  return readFile(file, "utf8");
}

test("EP047 directory admin pages preserve a 360px content gutter", async () => {
  const files = await Promise.all([
    source(routeFiles.importClient),
    source(routeFiles.validation),
    source(routeFiles.batches),
    source(routeFiles.batchDetail),
    source(routeFiles.visibility),
    source(routeFiles.visibilityPreview),
  ]);
  for (const file of files) {
    assert.match(file, /px-4[\s\S]{0,40}sm:px-6/, "page should use a 16px mobile gutter before the desktop gutter");
  }
});

test("EP047 directory admin table views label their horizontal-scroll regions", async () => {
  const [validation, batchDetail] = await Promise.all([
    source(routeFiles.validation),
    source(routeFiles.batchDetail),
  ]);
  assert.match(validation, /role="region"\s+aria-label="Active validation rules"\s+tabIndex=\{0\}\s+className="mt-3 overflow-x-auto"/);
  assert.match(batchDetail, /role="region"\s+aria-label="Verification batch items"\s+tabIndex=\{0\}\s+className="mt-5 overflow-x-auto"/);
});

test("EP047 directory admin action groups stack or wrap below the sm breakpoint", async () => {
  const [importClient, validation, validationPanel, batches, visibility] = await Promise.all([
    source(routeFiles.importClient),
    source(routeFiles.validation),
    source(routeFiles.validationPanel),
    source(routeFiles.batches),
    source(routeFiles.visibility),
  ]);
  assert.match(importClient, /flex flex-col gap-2 sm:flex-row sm:items-baseline sm:justify-between/);
  assert.match(importClient, /flex flex-col gap-3 border-t[\s\S]*sm:flex-row sm:items-center sm:justify-between/);
  assert.match(validation, /flex flex-col gap-3 text-sm sm:flex-row sm:items-center/);
  assert.match(validationPanel, /flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between/);
  assert.match(batches, /flex flex-col gap-1 rounded border p-3 text-sm[\s\S]{0,50}sm:flex-row sm:items-center sm:justify-between/);
  assert.match(visibility, /mt-3 flex flex-col gap-3 sm:flex-row sm:items-center/);
});

test("EP047 directory admin forms and summaries start at one column", async () => {
  const [validation, visibility, preview] = await Promise.all([
    source(routeFiles.validation),
    source(routeFiles.visibility),
    source(routeFiles.visibilityPreview),
  ]);
  assert.match(validation, /grid gap-2 sm:grid-cols-\[1fr_1fr_auto\]/);
  assert.match(visibility, /mt-4 flex flex-col gap-2 sm:flex-row/);
  assert.match(preview, /grid gap-4 sm:grid-cols-3/);
});
