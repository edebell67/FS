import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const root = new URL("../", import.meta.url);
const read = (path: string) => readFile(new URL(path, root), "utf8");

test("preview dispatch mints an owner-review capability link through the protected repository", async () => {
  const [repository, action] = await Promise.all([
    read("lib/owner-review/repository.ts"),
    read("app/directoryadmin/site-previews/actions.ts"),
  ]);
  assert.match(repository, /export async function createOwnerReviewLink/);
  assert.match(repository, /generateVerificationToken/);
  assert.match(repository, /hashVerificationToken/);
  assert.match(action, /createOwnerReviewLink/);
  assert.match(action, /\/review\//);
});
