#!/usr/bin/env node
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { runAllTownCollection } from "../src/all-town-news-runner.js";

const args = process.argv.slice(2);
const valueAfter = (flag) => args.includes(flag) ? args[args.indexOf(flag) + 1] : undefined;
const appRoot = process.cwd();
const defaultRegistry = path.resolve(appRoot, "..", "ep_047_directory_app", "private", "news-source-registry", "all-active-towns-v1.json");
const registryPath = path.resolve(valueAfter("--registry") || defaultRegistry);
const ledgerPath = path.resolve(valueAfter("--ledger") || path.join("private", "news-last-seen", "all-active-towns-v1.json"));
const reportPath = path.resolve(valueAfter("--report") || path.join("private", "news-collection-runs", `${new Date().toISOString().slice(0, 10)}.json`));
const maxCandidates = Number(valueAfter("--max-candidates") || 8);
const baseline = args.includes("--baseline");
if (!Number.isInteger(maxCandidates) || maxCandidates < 1 || maxCandidates > 24) throw new Error("--max-candidates must be an integer from 1 to 24.");

const result = await runAllTownCollection({ registryPath, ledgerPath, maxCandidates, baseline });
await mkdir(path.dirname(reportPath), { recursive: true });
await writeFile(reportPath, `${JSON.stringify(result, null, 2)}\n`, "utf8");
console.log(JSON.stringify({ reportPath, ledgerPath, summary: result.summary }, null, 2));
