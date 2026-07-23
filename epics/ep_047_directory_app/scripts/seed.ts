// Seeds reference data. Phase 0: no-op placeholder — the schema it would seed
// (pipeline_stages, categories) doesn't exist until Phase 1's migration lands.
//
// Phase 1 replaces this with: 22 default pipeline stages, the category tree,
// and the six default roles, all as idempotent upserts (safe to re-run).
//
// Usage:
//   npm run db:seed

import { config } from "dotenv";
config({ path: ".env.local" });
config();

async function main() {
  console.log(
    "Phase 0 placeholder — nothing to seed yet. Pipeline stages and categories arrive in Phase 1."
  );
}

main().catch((err) => {
  console.error("Seed failed:", err);
  process.exit(1);
});
