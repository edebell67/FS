"use server";
import { revalidatePath } from "next/cache";
import { db } from "@/lib/db/client";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { sql } from "drizzle-orm";
function value(data: FormData, key: string) { return String(data.get(key) ?? "").trim(); }
export async function saveArticle(data: FormData) {
  await requireAdminUserForPage("/directoryadmin/news");
  const slug = value(data, "slug") || value(data, "headline").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  await db.execute(sql`INSERT INTO news_articles (slug, headline, town, source_name, source_url, verified_update, local_reading, business_voices)
    VALUES (${slug}, ${value(data,"headline")}, ${value(data,"town")}, ${value(data,"sourceName")}, ${value(data,"sourceUrl")}, ${value(data,"verifiedUpdate")}, ${value(data,"localReading")}, NULL)
    ON CONFLICT (slug) DO UPDATE SET headline=excluded.headline, town=excluded.town, source_name=excluded.source_name, source_url=excluded.source_url, verified_update=excluded.verified_update, local_reading=excluded.local_reading, updated_at=now()`);
  revalidatePath("/directoryadmin/news");
}
export async function publishArticle(data: FormData) {
  await requireAdminUserForPage("/directoryadmin/news");
  const id = value(data, "id");
  await db.execute(sql`UPDATE news_articles SET status='published', published_at=now(), updated_at=now() WHERE id=${id} AND source_url <> '' AND verified_update <> '' AND local_reading <> ''`);
  revalidatePath("/directoryadmin/news");
}
