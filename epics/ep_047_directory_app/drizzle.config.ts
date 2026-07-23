import { defineConfig } from "drizzle-kit";

// Loads DATABASE_URL from process.env — populate via `.env.local` locally
// (tsx/next auto-load it) or Render's environment settings in production.
export default defineConfig({
  schema: "./lib/db/schema.ts",
  out: "./migrations",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL ?? "postgres://user:password@localhost:5432/ep047_directory",
  },
  verbose: true,
  strict: true,
});
