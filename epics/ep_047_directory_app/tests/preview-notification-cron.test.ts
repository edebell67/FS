import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";

test("unattended preview notification cron does not use a fabricated user foreign key", async () => {
  const [route, delivery] = await Promise.all([
    readFile(new URL("../app/api/internal/site-generation/notify/route.ts", import.meta.url), "utf8"),
    readFile(new URL("../lib/verification/preview-delivery.ts", import.meta.url), "utf8"),
  ]);
  assert.match(route, /const SYSTEM_ACTOR_ID = null/);
  assert.match(delivery, /actorUserId: string \| null/);
});
