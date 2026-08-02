import fs from "node:fs/promises";
import path from "node:path";
import { config } from "dotenv";
import { sql } from "drizzle-orm";
import { db } from "@/lib/db/client";
import { contentHash, parseNewsIntakeBatch, resolveNewsIntakeDirectory } from "@/lib/news-intake/importer";
import { importNewsIntakeBatch } from "@/lib/news-intake/service";

config({ path: ".env.local" });
config();

async function recordInvalidFile(filename: string, raw: string, error: unknown) {
  const hash = contentHash(raw);
  await db.execute(sql`
    INSERT INTO news_intake_batches (batch_key, schema_version, source_filename, content_hash, status, attempt_count, last_error, completed_at)
    VALUES (${`invalid:${filename}:${hash}`}, 'invalid', ${filename}, ${hash}, 'completed_with_rejections', 0, ${error instanceof Error ? error.message : "Invalid batch"}, now())
    ON CONFLICT (batch_key) DO NOTHING
  `);
}

async function importFile(intakeDirectory: string, filename: string) {
  const raw = await fs.readFile(path.join(intakeDirectory, filename), "utf8");
  let batch;
  try {
    batch = parseNewsIntakeBatch(raw);
  } catch (error) {
    await recordInvalidFile(filename, raw, error);
    return;
  }
  await importNewsIntakeBatch(batch, `private-json:${filename}`);
}

async function main() {
  const intakeDirectory = resolveNewsIntakeDirectory();
  let files: string[];
  try { files = await fs.readdir(intakeDirectory); } catch (error: unknown) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") { console.log("No deployed private News intake directory; nothing to import."); return; }
    throw error;
  }
  const batches = files.filter((file) => file.endsWith(".json") && !file.startsWith(".")).sort();
  await Promise.all(batches.map((filename) => importFile(intakeDirectory, filename)));
  console.log(`News intake scan finished: ${batches.length} deployed JSON batch(es).`);
}

main().catch((error) => { console.error("News intake import failed:", error); process.exitCode = 1; });
