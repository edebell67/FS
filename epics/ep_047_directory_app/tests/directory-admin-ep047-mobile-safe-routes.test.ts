import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const routeFiles = {
  news: new URL("../app/directoryadmin/news/page.tsx", import.meta.url),
  workflow: new URL("../app/directoryadmin/workflow/page.tsx", import.meta.url),
  sitePreviews: new URL("../app/directoryadmin/site-previews/page.tsx", import.meta.url),
};

async function source(file: URL) {
  return readFile(file, "utf8");
}

test("EP047 news, workflow, and site-preview routes preserve 360px gutters", async () => {
  const files = await Promise.all(Object.values(routeFiles).map(source));

  for (const file of files) {
    assert.match(file, /px-4\s+sm:px-6/, "route should use a 16px mobile gutter before the desktop gutter");
  }
});

test("EP047 news review actions stack before the sm breakpoint", async () => {
  const news = await source(routeFiles.news);

  assert.match(news, /flex-col\s+items-start\s+gap-3\s+sm:flex-row\s+sm:items-center/, "review rows must not compress article metadata and publish controls at 360px");
  assert.match(news, /w-full\s+sm:w-fit\s+rounded\s+bg-brand-600/, "the draft-save action should use the available mobile width");
});

test("EP047 site-preview tables remain labelled, scrollable regions", async () => {
  const sitePreviews = await source(routeFiles.sitePreviews);

  assert.match(sitePreviews, /role="region"\s+aria-label="Preview delivery candidates"\s+tabIndex=\{0\}\s+className="overflow-x-auto/, "candidate tables need an announced keyboard-focusable horizontal scroll region");
  assert.match(sitePreviews, /<table className="min-w-\[42rem\]\s+w-full/, "candidate table needs a readable minimum width inside its scroll region");
});

test("EP047 site-preview confirmations keep controls usable at 360px", async () => {
  const sitePreviews = await source(routeFiles.sitePreviews);

  assert.match(sitePreviews, /flex\s+items-start\s+gap-2\s+text-sm/, "confirmation checkbox labels must top-align beside wrapped text");
  assert.match(sitePreviews, /mt-4\s+w-full\s+rounded\s+bg-brand-700[\s\S]{0,80}sm:w-fit/, "send buttons should be full-width on mobile and content-width from sm upward");
});
