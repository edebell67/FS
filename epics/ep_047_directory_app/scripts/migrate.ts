// Applies every pending SQL migration in ./migrations against DATABASE_URL.
//
// Migrations are generated with `npm run db:generate` after editing
// lib/db/schema.ts, then checked into git as plain SQL (see PLAN.md §1: SQL is
// the source of truth, not the ORM's internal migration state). This runner
// just applies them in order and records each in drizzle's own bookkeeping
// table (`__drizzle_migrations`) so re-running is a no-op.
//
// Usage:
//   npm run db:migrate

import { config } from "dotenv";
config({ path: ".env.local" });
config(); // fall back to .env if present
import { Pool } from "pg";
import { drizzle } from "drizzle-orm/node-postgres";
import { migrate } from "drizzle-orm/node-postgres/migrator";

async function main() {
  const connectionString = process.env.DATABASE_URL;
  if (!connectionString) {
    throw new Error(
      "DATABASE_URL is not set. Copy .env.example to .env.local (or set it in the shell) before migrating."
    );
  }

  const pool = new Pool({
    connectionString,
    ssl: connectionString.includes("localhost") ? false : { rejectUnauthorized: false },
  });

  const db = drizzle(pool);

  console.log("Applying migrations from ./migrations ...");
  await migrate(db, { migrationsFolder: "./migrations" });
  console.log("Migrations up to date.");

  await pool.end();
}

main().catch((err) => {
  console.error("Migration failed:", err);
  process.exit(1);
});
