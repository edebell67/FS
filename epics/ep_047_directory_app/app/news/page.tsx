import Link from "next/link";
import { sql } from "drizzle-orm";
import { db } from "@/lib/db/client";
import { publicScopeWhere } from "@/ep047_visibility_news/lib/public-scope";

export const dynamic = "force-dynamic";

type Story = {
  id: string;
  slug: string;
  headline: string;
  town: string;
  source_name: string;
  source_url: string;
  verified_update: string;
  local_reading: string;
  published_at: Date | null;
};

export default async function PublicNewsPage() {
  const result = await db.execute(sql`
    SELECT a.id, a.slug, a.headline, a.town, a.source_name, a.source_url,
      a.verified_update, a.local_reading, a.published_at
    FROM news_articles a
    WHERE a.status = 'published'
      AND EXISTS (SELECT 1 FROM businesses WHERE lower(trim(town)) = lower(trim(a.town)) AND ${publicScopeWhere()})
    ORDER BY a.published_at DESC NULLS LAST, a.created_at DESC
  `);
  const stories = ((result as any).rows ?? []) as Story[];

  return <main className="mx-auto max-w-6xl px-6 py-10">
    <section className="border-b-2 border-[#152022] pb-8">
      <p className="font-mono text-[11px] font-medium uppercase tracking-[0.12em] text-brand-700">Independent local business briefing</p>
      <div className="mt-3 flex flex-wrap items-end justify-between gap-5">
        <div>
          <h1 className="font-display text-4xl font-semibold tracking-[-0.045em] text-[#152022] sm:text-6xl">The Tech Principle <span className="text-brand-600">News</span></h1>
          <p className="mt-3 max-w-2xl text-[#667174]">Verified local updates, clearly separated from editorial local-business reading.</p>
        </div>
        <Link href="/directory" className="font-mono text-[11px] font-medium uppercase tracking-[0.08em] text-brand-700 hover:text-brand-600">Browse the Directory →</Link>
      </div>
    </section>

    {stories.length ? <section className="mt-10 grid gap-5 lg:grid-cols-[1.1fr_.9fr]">
      <div className="space-y-4">
        {stories.map((story, index) => <article key={story.id} className={`rounded-sm border p-5 ${index === 0 ? "border-[#152022] bg-[#fffdf8]" : "border-[#d6d2c9] bg-[#fffdf8]"}`}>
          <p className="font-mono text-[11px] font-medium uppercase tracking-[0.1em] text-brand-700">{story.town}{story.published_at ? ` · ${new Intl.DateTimeFormat("en-GB", { day: "numeric", month: "long", year: "numeric" }).format(new Date(story.published_at))}` : ""}</p>
          <h2 className="mt-2 font-display text-2xl font-semibold tracking-[-0.025em] text-[#152022]">{story.headline}</h2>
          <p className="mt-3 text-sm leading-6 text-[#4c5657]">{story.verified_update}</p>
          <p className="mt-3 border-l-2 border-brand-600 pl-3 text-sm leading-6 text-[#667174]"><strong className="text-[#152022]">Local reading: </strong>{story.local_reading}</p>
          {story.source_url ? <a className="mt-4 inline-block text-sm font-semibold text-brand-700 hover:text-brand-600" href={story.source_url} target="_blank" rel="noreferrer">Source: {story.source_name || "Read update"} ↗</a> : null}
        </article>)}
      </div>
      <aside className="h-fit rounded-sm border border-[#d6d2c9] bg-[#fffdf8] p-6 lg:sticky lg:top-6">
        <p className="font-mono text-[11px] font-medium uppercase tracking-[0.1em] text-brand-700">Editorial standard</p>
        <h2 className="mt-2 font-display text-3xl font-semibold tracking-[-0.03em] text-[#152022]">Useful local news, without pretending.</h2>
        <p className="mt-4 text-sm leading-6 text-[#667174]">Each item names its source, distinguishes the verified update from editorial interpretation, and avoids predictions about individual businesses.</p>
      </aside>
    </section> : <section className="mt-12 rounded-sm border border-[#d6d2c9] bg-[#fffdf8] p-8"><h2 className="font-display text-3xl font-semibold text-[#152022]">Local news is being prepared.</h2><p className="mt-3 max-w-xl text-[#667174]">Published articles will appear here once their source, verified update and local reading have passed editorial review.</p></section>}
  </main>;
}
