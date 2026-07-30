/**
 * lib/generation/skill-loader.ts — resolves a business's category to its
 * ep044_group skill template, and lists the compressed images available
 * for it.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-07-30 · Initial version: normalizes category strings and
 *   skill-folder / image-folder names to the same lowercase-hyphen key so no
 *   hand-maintained mapping table has to track every category; unmatched
 *   categories return null so the orchestrator can skip and log clearly
 *   rather than guess the wrong template.
 */

import { readdir, readFile } from "node:fs/promises";
import path from "node:path";

const REPO_ROOT = path.resolve(process.cwd(), "..", "..");
const SKILLS_DIR = path.join(REPO_ROOT, "skills", "ep044_group");
const BLUEPRINT_PATH = path.join(SKILLS_DIR, "ep044_common_site_blueprint", "000_site_blueprint.md");
const IMAGES_DIR = path.join(
  REPO_ROOT,
  "epics",
  "ep_044_web_apps",
  "_images",
  "batch_02",
  "illustrative_gallery_sets"
);

const SKILL_FOLDER_SUFFIX = "_demo_template";
const SKILL_FOLDER_PREFIX = "ep044_app_";

/** "Dog Grooming", "dog-grooming", "dog_grooming" all normalize to "dog-grooming". */
function normalizeKey(value: string): string {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export type CategorySkill = {
  category: string;
  skillFolder: string;
  skillMarkdown: string;
  blueprintMarkdown: string;
  imageFiles: string[];
};

/** Null when no skill template matches this category — caller must skip, not fabricate a template. */
export async function loadSkillForCategory(category: string): Promise<CategorySkill | null> {
  const targetKey = normalizeKey(category);

  const skillDirs = await readdir(SKILLS_DIR, { withFileTypes: true });
  const match = skillDirs.find((entry) => {
    if (!entry.isDirectory() || !entry.name.endsWith(SKILL_FOLDER_SUFFIX)) return false;
    const middle = entry.name.slice(SKILL_FOLDER_PREFIX.length, -SKILL_FOLDER_SUFFIX.length);
    return normalizeKey(middle) === targetKey;
  });
  if (!match) return null;

  const skillFolder = match.name;
  const [skillMarkdown, blueprintMarkdown] = await Promise.all([
    readFile(path.join(SKILLS_DIR, skillFolder, "SKILL.md"), "utf-8"),
    readFile(BLUEPRINT_PATH, "utf-8"),
  ]);

  const imageFiles = await listImagesForCategory(targetKey);

  return { category, skillFolder, skillMarkdown, blueprintMarkdown, imageFiles };
}

async function listImagesForCategory(targetKey: string): Promise<string[]> {
  let imageDirs: string[];
  try {
    imageDirs = (await readdir(IMAGES_DIR, { withFileTypes: true }))
      .filter((e) => e.isDirectory())
      .map((e) => e.name);
  } catch {
    return [];
  }

  const dirMatch = imageDirs.find((name) => normalizeKey(name) === targetKey);
  if (!dirMatch) return [];

  const categoryDir = path.join(IMAGES_DIR, dirMatch);
  const files = await collectImageFiles(categoryDir);
  return files;
}

async function collectImageFiles(dir: string): Promise<string[]> {
  const entries = await readdir(dir, { withFileTypes: true });
  const results: string[] = [];
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...(await collectImageFiles(full)));
    } else if (/\.(jpg|jpeg|png|webp)$/i.test(entry.name)) {
      results.push(full);
    }
  }
  return results;
}
