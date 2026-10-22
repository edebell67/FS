import Link from "next/link";
import { sql } from "drizzle-orm";
import { db } from "@/lib/db/client";
import { publicScopeWhere } from "@/ep047_visibility_news/lib/public-scope";
import { PublicNewsReader } from "./PublicNewsReader";

export const dynamic = "force-dynamic";

type Story = {
  id: string;
  slug: string;
  headline: string;
  town: string;
  postcode: string | null;
  topic: string | null;
  source_name: string;
  source_url: string;
  verified_update: string;
  local_reading: string;
  business_voices: string | null;
  published_at: string | null;
};

export default async function PublicNewsPage() {
  const result = await db.execute(sql`
    SELECT a.id, a.slug, a.headline, a.town, NULL::text AS postcode,
      COALESCE(MIN(c.category_label), 'Local news') AS topic,
      a.source_name, a.source_url, a.verified_update, a.local_reading, a.business_voices,
      a.published_at::text AS published_at
    FROM news_articles a
    LEFT JOIN news_article_categories c ON c.article_id = a.id
    WHERE a.status = 'published'
      AND a.duplicate_state = 'unique'
      AND EXISTS (SELECT 1 FROM businesses WHERE lower(trim(town)) = lower(trim(a.town)) AND ${publicScopeWhere()})
    GROUP BY a.id
    ORDER BY COALESCE(a.effective_story_date, a.published_at::date) DESC, a.published_at DESC NULLS LAST, a.created_at DESC
  `);
  const stories = ((result as any).rows ?? []) as Story[];

  return <>
    <header className="border-b-2 border-[#152022]">
      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <p className="font-mono text-[11px] font-medium uppercase tracking-[0.12em] text-brand-700">Independent local business briefing</p>
        <div className="mt-3 flex flex-wrap items-end justify-between gap-5">
          <div>
            <h1 className="font-display text-4xl font-semibold tracking-[-0.045em] text-[#152022] sm:text-6xl">The Tech Principle <span className="text-brand-600">News</span></h1>
            <p className="mt-3 max-w-2xl text-[#667174]">Verified local updates, clearly separated from editorial local-business reading.</p>
          </div>
          <Link href="/directory" className="inline-flex min-h-11 items-center font-mono text-[11px] font-medium uppercase tracking-[0.08em] text-brand-700 underline underline-offset-4 hover:text-brand-600">Browse the Directory →</Link>
        </div>
      </div>
    </header>
    {stories.length ? <PublicNewsReader stories={stories} /> : <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8"><section className="border border-[#d6d2c9] bg-[#fffdf8] p-8"><h2 className="font-display text-3xl font-semibold text-[#152022]">Local news is being prepared.</h2><p className="mt-3 max-w-xl text-[#667174]">Published articles will appear here once their source, verified update and local reading have passed editorial review.</p></section></main>}
  </>;
}
