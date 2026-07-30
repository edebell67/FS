/**
 * lib/generation/run-generation.ts — the site-generation loop itself: pulls
 * the queue, runs the matching ep044_group skill through the configured LLM,
 * writes the output, and records completion via the existing internal API.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-07-30 · Initial version: single-call generation (no LLM tool
 *   use / image-verification loop yet -- see SKILL.md's stricter multi-step
 *   process for the eventual upgrade). Calls the three existing internal
 *   endpoints (queue/complete/notify) over HTTP rather than importing the DB
 *   layer directly, so this loop stays swappable for a wholly separate
 *   worker later, per the "model-agnostic" design already agreed. Writes
 *   files to disk only -- committing and pushing to GitHub (so GitHub Pages
 *   actually serves them) is a deliberate separate, confirmed step, not
 *   automated here.
 */

import { mkdir, writeFile, copyFile } from "node:fs/promises";
import path from "node:path";
import { getGenerationConfig, isGenerationConfigured } from "@/lib/generation/config";
import { callLlm } from "@/lib/generation/llm-client";
import { loadSkillForCategory } from "@/lib/generation/skill-loader";

const REPO_ROOT = path.resolve(process.cwd(), "..", "..");
const OUTPUT_ROOT = path.join(REPO_ROOT, "epics", "ep_006_website_rebuilds", "redesigns");

type QueuedBusiness = {
  id: string;
  businessRef: string;
  businessName: string;
  category: string;
  town: string | null;
};

function internalApiHeaders(): Record<string, string> {
  const key = process.env.INTERNAL_API_KEY?.trim();
  if (!key) throw new Error("INTERNAL_API_KEY is not set -- required to call the internal generation API.");
  return { authorization: `Bearer ${key}` };
}

function appOrigin(): string {
  const origin = process.env.PUBLIC_APP_ORIGIN?.trim();
  if (!origin) throw new Error("PUBLIC_APP_ORIGIN is not set -- required to build the recorded siteUrl.");
  return origin.replace(/\/$/, "");
}

async function fetchQueue(): Promise<QueuedBusiness[]> {
  const res = await fetch(`${appOrigin()}/api/internal/site-generation/queue`, { headers: internalApiHeaders() });
  if (!res.ok) throw new Error(`Failed to fetch generation queue: ${res.status} ${await res.text()}`);
  const data = (await res.json()) as { businesses: QueuedBusiness[] };
  return data.businesses;
}

async function recordComplete(businessId: string, siteUrl: string): Promise<void> {
  const res = await fetch(`${appOrigin()}/api/internal/site-generation/complete`, {
    method: "POST",
    headers: { ...internalApiHeaders(), "content-type": "application/json" },
    body: JSON.stringify({ businessId, siteUrl }),
  });
  if (!res.ok) throw new Error(`Failed to record generation completion: ${res.status} ${await res.text()}`);
}

function slugify(value: string): string {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

const SYSTEM_PROMPT_PREFIX = `You are generating one business's static website by following the skill
instructions below exactly. Respond with ONLY a single JSON object of the
shape {"files": {"<relative filename>": "<full file contents>"}} -- no
markdown fences, no commentary before or after. Every filename must be
relative (e.g. "index.html", "styles.css", "gallery.html"). Reference any
provided images via a relative "images/<filename>" path -- do not invent
image filenames beyond the ones listed in the user message.`;

type GenerationResult = { businessId: string; siteUrl: string } | { businessId: string; skipped: string };

async function generateOneBusiness(business: QueuedBusiness): Promise<GenerationResult> {
  const skill = await loadSkillForCategory(business.category);
  if (!skill) {
    return { businessId: business.id, skipped: `No ep044_group skill template matches category "${business.category}".` };
  }

  const config = getGenerationConfig();
  if (!config) {
    return { businessId: business.id, skipped: "LLM not configured (LLM_PROVIDER/LLM_MODEL/API key unset)." };
  }

  const imageNames = skill.imageFiles.map((f) => path.basename(f));
  const systemPrompt = `${SYSTEM_PROMPT_PREFIX}\n\n${skill.blueprintMarkdown}\n\n${skill.skillMarkdown}`;
  const userPrompt = `Business details (real, not placeholder -- use exactly as given, never invent stats/reviews/accreditations):
${JSON.stringify(
  {
    businessName: business.businessName,
    category: business.category,
    town: business.town,
  },
  null,
  2
)}

Available images (already verified, compressed, and provided -- reference by filename under images/, do not fabricate others):
${imageNames.join("\n")}`;

  const raw = await callLlm(config, systemPrompt, userPrompt);
  const parsed = parseGeneratedFiles(raw);

  const slug = slugify(business.businessName);
  const outputDir = path.join(OUTPUT_ROOT, slug);
  await mkdir(outputDir, { recursive: true });

  for (const [relPath, content] of Object.entries(parsed.files)) {
    const dest = path.join(outputDir, relPath);
    await mkdir(path.dirname(dest), { recursive: true });
    await writeFile(dest, content, "utf-8");
  }

  if (imageNames.length) {
    const imagesDir = path.join(outputDir, "images");
    await mkdir(imagesDir, { recursive: true });
    for (const src of skill.imageFiles) {
      await copyFile(src, path.join(imagesDir, path.basename(src)));
    }
  }

  const siteUrl = `${appOrigin()}/epics/ep_006_website_rebuilds/redesigns/${slug}/index.html`;
  await recordComplete(business.id, siteUrl);
  return { businessId: business.id, siteUrl };
}

function parseGeneratedFiles(raw: string): { files: Record<string, string> } {
  const trimmed = raw.trim().replace(/^```(?:json)?\s*/i, "").replace(/```\s*$/, "");
  let parsed: unknown;
  try {
    parsed = JSON.parse(trimmed);
  } catch (err) {
    throw new Error(`LLM response was not valid JSON: ${err instanceof Error ? err.message : String(err)}`);
  }
  if (
    typeof parsed !== "object" ||
    parsed === null ||
    !("files" in parsed) ||
    typeof (parsed as { files: unknown }).files !== "object"
  ) {
    throw new Error('LLM response JSON did not match {"files": {...}}.');
  }
  return parsed as { files: Record<string, string> };
}

export async function runGenerationLoop(): Promise<GenerationResult[]> {
  if (!isGenerationConfigured()) {
    console.log("Generation loop: LLM not configured yet -- skipping (not treated as an error).");
    return [];
  }

  const queue = await fetchQueue();
  console.log(`Generation loop: ${queue.length} business(es) awaiting site generation.`);

  const results: GenerationResult[] = [];
  for (const business of queue) {
    try {
      results.push(await generateOneBusiness(business));
    } catch (error) {
      console.error(`Generation failed for ${business.businessRef}:`, error);
    }
  }
  return results;
}
