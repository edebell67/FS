import fs from "node:fs";
import vm from "node:vm";
import { sql } from "drizzle-orm";
import { db } from "@/lib/db/client";

const source = fs.readFileSync("../ep_047_newssite/The Tech Principle News.html", "utf8");
const storySource = source.match(/(?:const|let) (?:staticStories|stories) = ([\s\S]*?);\s*\/\/ Each article/)?.[1];
const categorySource = source.match(/const directoryCategories=([\s\S]*?);\s*\/\/ The prototype/)?.[1];
if (!storySource) throw new Error("Static News stories were not found");
const stories = vm.runInNewContext(storySource) as Array<any>;
const categories = categorySource ? vm.runInNewContext(`(${categorySource})`) as Record<string, string[]> : {};
async function main() {
if (process.argv.includes("--dry-run")) {
  console.log(`Dry run: ${stories.length} stories and ${Object.keys(categories).length} category mappings extracted.`);
  return;
}
for (const story of stories) {
  const byLabel = (label: string) => String(story.body.find((p: string) => p.startsWith(`<strong>${label}:`)) ?? "").replace(/<[^>]+>/g, "").replace(new RegExp(`^${label}:\\s*`), "");
  const slug = `static-${story.id}-${String(story.headline).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "")}`;
  const articleResult = await db.execute(sql`INSERT INTO news_articles (slug, headline, town, source_name, source_url, verified_update, local_reading, business_voices, status, published_at)
    VALUES (${slug}, ${story.headline}, ${story.place}, ${story.source}, ${story.url}, ${byLabel("Verified update")}, ${byLabel("Our local reading")}, ${byLabel("Business voices")}, 'published', ${story.date}::timestamptz)
    ON CONFLICT (slug) DO UPDATE SET headline=excluded.headline, town=excluded.town, source_name=excluded.source_name, source_url=excluded.source_url, verified_update=excluded.verified_update, local_reading=excluded.local_reading, business_voices=excluded.business_voices, status='published', published_at=excluded.published_at RETURNING id`);
  const article = (articleResult as any).rows?.[0];
  for (const category of categories[String(story.id)] ?? []) await db.execute(sql`INSERT INTO news_article_categories (article_id, category_key, category_label) VALUES (${article.id}, ${category}, ${category}) ON CONFLICT DO NOTHING`);
}
console.log(`Seeded ${stories.length} News stories into the database.`);
}
main().catch((error) => { console.error(error); process.exitCode = 1; });
