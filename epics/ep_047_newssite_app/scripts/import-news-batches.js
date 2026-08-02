import { readdir, readFile } from "node:fs/promises";
import path from "node:path";
import { batchHash, parseBatch } from "../src/intake.js";

const intakeDir = path.resolve(process.cwd(), "private", "news-intake");
const endpoint = process.env.NEWS_IMPORT_API_URL;
const apiKey = process.env.NEWS_IMPORT_API_KEY;
const files = (await readdir(intakeDir, { withFileTypes: true }).catch(() => [])).filter(x => x.isFile() && x.name.endsWith(".json")).map(x => x.name).sort();
if (!endpoint || !apiKey) {
  console.log(`Validated ${files.length} private batch file(s); import delivery is disabled until Render secrets are configured.`);
  for (const file of files) parseBatch(await readFile(path.join(intakeDir, file), "utf8"));
  process.exit(0);
}
for (const file of files) {
  const batch = parseBatch(await readFile(path.join(intakeDir, file), "utf8"));
  const response = await fetch(endpoint, { method: "POST", headers: { "content-type": "application/json", authorization: `Bearer ${apiKey}`, "x-news-batch-hash": batchHash(batch) }, body: JSON.stringify(batch) });
  if (!response.ok) throw new Error(`Private batch ${batch.batchId} delivery failed with HTTP ${response.status}.`);
  console.log(`Delivered private batch ${batch.batchId}.`);
}
