import { Pool } from "pg";
import { drizzle, type NodePgDatabase } from "drizzle-orm/node-postgres";
import * as schema from "./schema";

declare global {
  // eslint-disable-next-line no-var
  var __ep047Pool: Pool | undefined;
  // eslint-disable-next-line no-var
  var __ep047Db: NodePgDatabase<typeof schema> | undefined;
}

function createPool(): Pool {
  const connectionString = process.env.DATABASE_URL;
  if (!connectionString) {
    throw new Error(
      "DATABASE_URL is not set. Copy .env.example to .env.local and point it at a Postgres instance."
    );
  }

  return new Pool({
    connectionString,
    // Render Postgres requires SSL outside its own private network; local dev does not.
    ssl: connectionString.includes("localhost") ? false : { rejectUnauthorized: false },
    max: 10,
  });
}

// Lazily constructed: Next's build-time page-data collection imports this
// module without DATABASE_URL ever being set, so the pool must not be built
// at import time — only on first actual query, at request time.
function getDb(): NodePgDatabase<typeof schema> {
  if (globalThis.__ep047Db) return globalThis.__ep047Db;

  const pool = globalThis.__ep047Pool ?? createPool();
  globalThis.__ep047Pool = pool;

  const instance = drizzle(pool, { schema });
  globalThis.__ep047Db = instance;
  return instance;
}

// Proxy so call sites can keep writing `db.execute(...)`, `db.select()...`
// etc. without knowing the underlying client is created lazily.
export const db = new Proxy({} as NodePgDatabase<typeof schema>, {
  get(_target, prop, receiver) {
    return Reflect.get(getDb(), prop, receiver);
  },
});
export type Database = NodePgDatabase<typeof schema>;
