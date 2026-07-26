import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";

test("pipeline exposes the imported-estate validation entry point before batch verification", async () => {
  const page = await readFile(new URL("../app/directoryadmin/pipeline/page.tsx", import.meta.url), "utf8");
  assert.match(page, /const importedCount = importedColumn\?\.count \?\? 0/);
  assert.match(page, /href="\/directoryadmin\/validation"/);
  assert.match(page, /Run field validation for/);
  assert.match(page, /importedCount > 0/);
  assert.match(page, /Select validated businesses for batch verification/);
});
