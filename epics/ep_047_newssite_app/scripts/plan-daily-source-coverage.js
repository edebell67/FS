#!/usr/bin/env node
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { buildDailySourcePlan } from "../src/daily-source-rotation.js";
import { NEWS_SOURCE_REGISTRY } from "../src/source-registry.js";

const args = process.argv.slice(2);
const valueAfter = (flag) => args.includes(flag) ? args[args.indexOf(flag) + 1] : undefined;
const date = valueAfter("--date") || new Date().toISOString().slice(0, 10);
const requestedTowns = (valueAfter("--towns") || "").split(",").map((town) => town.trim()).filter(Boolean);
// Until production read-only Directory discovery is wired, use only explicitly
// declared registry towns; never infer all Directory towns from batch history.
const eligibleTowns = requestedTowns.length ? requestedTowns : [...new Set(NEWS_SOURCE_REGISTRY.flatMap((source) => source.towns))];
const plan = buildDailySourcePlan({ date, eligibleTowns });
const reportPath = path.resolve("private", "source-plans", `${plan.date}.json`);
await mkdir(path.dirname(reportPath), { recursive: true });
await writeFile(reportPath, `${JSON.stringify(plan, null, 2)}\n`, "utf8");
console.log(`Private source coverage plan written: ${reportPath}`);
console.log(`Selected ${plan.selections.length} enabled source(s); uncovered towns: ${plan.uncoveredTowns.length || "none"}.`);
