import { NextResponse } from "next/server";
import { sql } from "drizzle-orm";
import { db } from "@/lib/db/client";
import { APP_VERSION } from "@/lib/app-version";
import { publicScopeWhere } from "@/ep047_visibility_news/lib/public-scope";

// EP047-2026.08.01.2 — shared published/scope/date/deduped News selection.
export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  const url = new URL(request.url);
  const town = url.searchParams.get("town");
  const history = url.searchParams.get("history") === "1";
  try {
    const result = await db.execute(sql`
      WITH eligible AS (
        SELECT a.id, a.slug, a.headline, a.town AS place,
          '' AS postcode, COALESCE(MIN(c.category_label), 'Local news') AS topic,
          a.source_name AS source, a.source_url AS url, a.verified_update, a.local_reading,
          a.business_voices, to_char(COALESCE(a.effective_story_date, a.published_at::date), 'YYYY-MM-DD') AS date,
          a.effective_date_kind, a.date_provenance,
          COALESCE(json_agg(json_build_object('key', c.category_key, 'label', c.category_label))
            FILTER (WHERE c.id IS NOT NULL), '[]'::json) AS categories,
          COALESCE(a.effective_story_date, a.published_at::date) AS effective_date,
          a.published_at, a.created_at,
          ROW_NUMBER() OVER (
            PARTITION BY lower(trim(a.town))
            ORDER BY COALESCE(a.effective_story_date, a.published_at::date) DESC,
              a.published_at DESC NULLS LAST, a.created_at DESC
          ) AS town_rank
        FROM news_articles a
        LEFT JOIN news_article_categories c ON c.article_id = a.id
        WHERE a.status = 'published' AND a.duplicate_state = 'unique'
          AND (CAST(${town} AS text) IS NULL OR lower(trim(a.town)) = lower(trim(CAST(${town} AS text))))
          AND (CAST(${history} AS boolean) OR COALESCE(a.effective_story_date, a.published_at::date) >= CURRENT_DATE - COALESCE((SELECT lookback_days FROM public_news_display_settings WHERE id = true), 30))
          AND EXISTS (SELECT 1 FROM businesses WHERE lower(trim(town)) = lower(trim(a.town)) AND ${publicScopeWhere()})
        GROUP BY a.id
      )
      SELECT id, slug, headline, place, postcode, topic, source, url, verified_update, local_reading,
        business_voices, date, effective_date_kind, date_provenance, categories
      FROM eligible
      WHERE town_rank <= COALESCE((SELECT max_articles_per_town FROM public_news_display_settings WHERE id = true), 10)
      ORDER BY effective_date DESC, published_at DESC NULLS LAST, created_at DESC
    `);
    return NextResponse.json({ version: APP_VERSION, stories: (result as any).rows ?? [] });
  } catch (error) {
    console.error("EP047 public-news query failed", error);
    return NextResponse.json({ version: APP_VERSION, stories: [], error: "news_unavailable" }, { status: 503 });
  }
}
