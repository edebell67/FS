// One-time migration: JsonStore's data/ directory -> a SqliteStore database.
// Dogfoods the SqliteStore's own write methods as the import path, rather
// than hand-crafting INSERT statements, so the migration exercises exactly
// the same normalization (normalizeClient etc.) that live traffic would.
//
// Usage:
//   node tools/migrate_to_sqlite.js [--data <dir>] [--out <sqlite-file>]
//
// Verifies row counts after import match the source JSON array lengths per
// client and per record type, and exits non-zero if any mismatch is found
// — this script is meant to be safe to run against a copy before touching
// anything real.
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { JsonStore, RECORD_TYPES } from "../src/store.js";
import { SqliteStore } from "../src/sqliteStore.js";

const rootDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function parseArgs(argv) {
  const out = { data: path.join(rootDir, "data"), out: path.join(rootDir, "data", "app.db") };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === "--data") out.data = path.resolve(argv[++i]);
    if (argv[i] === "--out") out.out = path.resolve(argv[++i]);
  }
  return out;
}

export async function migrate({ dataDir, outPath, log = console.log }) {
  const source = new JsonStore(dataDir);
  await source.init();

  const target = new SqliteStore(outPath);
  await target.init();

  let clientsImported = 0;
  for (const client of source.listClients()) {
    await target.createClient(client);
    clientsImported += 1;
  }
  log(`clients: ${clientsImported} imported`);

  const sourceRecords = source.listRecords();
  const countsImported = {};
  for (const type of RECORD_TYPES) {
    const entries = sourceRecords[type] || [];
    if (entries.length) await target.appendRecords(type, entries.map((entry) => ({ ...entry })));
    countsImported[type] = entries.length;
    log(`${type}: ${entries.length} imported`);
  }

  // Verify: row counts in the target must match the source exactly.
  const targetClients = target.listClients();
  const mismatches = [];
  if (targetClients.length !== clientsImported) mismatches.push(`clients: source ${clientsImported} vs target ${targetClients.length}`);
  const targetRecords = target.listRecords();
  for (const type of RECORD_TYPES) {
    const expected = countsImported[type];
    const actual = (targetRecords[type] || []).length;
    if (actual !== expected) mismatches.push(`${type}: source ${expected} vs target ${actual}`);
  }

  target.close();
  if (mismatches.length) {
    throw new Error(`Migration count mismatch:\n${mismatches.join("\n")}`);
  }
  log("Verified: all row counts match source.");
  return { clientsImported, recordCounts: countsImported };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const { data, out } = parseArgs(process.argv.slice(2));
  migrate({ dataDir: data, outPath: out })
    .then(() => console.log(`Done. SQLite database written to ${out}`))
    .catch((error) => { console.error(error.message); process.exitCode = 1; });
}
