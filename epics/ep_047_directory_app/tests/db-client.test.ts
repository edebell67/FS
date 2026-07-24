import assert from "node:assert/strict";
import { test } from "node:test";

import { db } from "../lib/db/client";

test("production reuses one process-wide Postgres pool", async () => {
  const processEnv = process.env as Record<string, string | undefined>;
  const originalNodeEnv = processEnv.NODE_ENV;
  const originalDatabaseUrl = processEnv.DATABASE_URL;
  const originalPool = globalThis.__ep047Pool;
  const originalDb = globalThis.__ep047Db;

  try {
    processEnv.NODE_ENV = "production";
    processEnv.DATABASE_URL = "postgres://user:password@localhost:5432/ep047_directory";
    globalThis.__ep047Pool = undefined;
    globalThis.__ep047Db = undefined;

    void db.select;
    const firstPool = globalThis.__ep047Pool;
    void db.select;

    assert.ok(firstPool, "the first database access should retain its pool");
    assert.equal(globalThis.__ep047Pool, firstPool, "later accesses must reuse the same pool");
  } finally {
    await globalThis.__ep047Pool?.end();
    globalThis.__ep047Pool = originalPool;
    globalThis.__ep047Db = originalDb;
    processEnv.NODE_ENV = originalNodeEnv;
    processEnv.DATABASE_URL = originalDatabaseUrl;
  }
});
