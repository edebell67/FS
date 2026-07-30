// scripts/generate-sites.ts — Render Cron Job entrypoint for the site-
// generation loop (lib/generation/run-generation.ts). Reads config from
// .env.local locally or Render's env vars in production. A no-op, not a
// failure, when LLM_PROVIDER/LLM_MODEL/API key aren't set yet.
//
// Usage:
//   npm run generate:sites

import { config } from "dotenv";
config({ path: ".env.local" });
config();

import { runGenerationLoop } from "@/lib/generation/run-generation";

runGenerationLoop()
  .then((results) => {
    console.log(`Generation loop finished: ${results.length} business(es) processed.`);
  })
  .catch((err) => {
    console.error("Generation loop failed:", err);
    process.exit(1);
  });
