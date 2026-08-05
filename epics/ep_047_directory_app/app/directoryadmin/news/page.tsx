import { requireAdminUserForPage } from "@/lib/auth/require";
import { db } from "@/lib/db/client";
import { sql } from "drizzle-orm";
import { saveArticle, publishArticle } from "./actions";

export const dynamic = "force-dynamic";

export default async function NewsAdminPage() {
  await requireAdminUserForPage("/directoryadmin/news");
  const result = await db.execute(sql`
    SELECT id, slug, headline, town, status, source_name, source_published_at, original_event_date,
      effective_story_date, effective_date_kind, duplicate_state, duplicate_reason, updated_at
    FROM news_articles ORDER BY updated_at DESC
  `);
  const articles = (result as any).rows ?? [];

  return <main className="mx-auto max-w-5xl px-4 sm:px-6 py-10 sm:py-12">
    <p className="text-sm font-medium uppercase tracking-wide text-brand-600">Protected editorial desk</p>
    <h1 className="mt-1 text-3xl font-semibold">News drafts, review & publish</h1>
    <p className="mt-2 text-slate-600">Date evidence is required for publication. Incomplete or duplicate stories remain in review and published stories are never overwritten.</p>
    <form action={saveArticle} className="mt-8 grid gap-3 rounded-xl border p-5">
      <input name="headline" required placeholder="Headline" className="rounded border p-2" />
      <div className="grid gap-3 sm:grid-cols-2">
        <input name="town" required placeholder="Town" className="rounded border p-2" />
        <input name="sourceName" required placeholder="Source name" className="rounded border p-2" />
        <input name="sourceUrl" required type="url" placeholder="Source URL" className="rounded border p-2" />
        <input name="slug" placeholder="Slug (optional)" className="rounded border p-2" />
        <input name="eventIdentity" placeholder="Event identity (for duplicate review)" className="rounded border p-2 sm:col-span-2" />
      </div>
      <fieldset className="grid gap-3 rounded border p-4 sm:grid-cols-2">
        <legend className="px-1 text-sm font-medium">Date evidence (all fields required to publish)</legend>
        <input name="originalEventDate" type="date" aria-label="Original event date" className="rounded border p-2" />
        <input name="sourcePublishedAt" type="date" aria-label="Source publication date" className="rounded border p-2" required />
        <select name="selectedDateKind" required defaultValue="" className="rounded border p-2">
          <option value="" disabled>Select effective date</option>
          <option value="original_event">Original event date</option>
          <option value="source_publication">Source publication date</option>
        </select>
        <select name="dateConfidence" required defaultValue="" className="rounded border p-2">
          <option value="" disabled>Date evidence confidence</option>
          <option value="high">High confidence</option>
          <option value="medium">Medium confidence</option>
          <option value="low">Low confidence</option>
        </select>
        <textarea name="dateProvenanceNote" required placeholder="Date provenance / extraction note — identify the source text or metadata" className="min-h-20 rounded border p-2 sm:col-span-2" />
        <textarea name="dateSelectionRationale" required placeholder="Selection rationale — explain why this date is the effective story date" className="min-h-20 rounded border p-2 sm:col-span-2" />
      </fieldset>
      <textarea name="verifiedUpdate" required placeholder="Verified update — sourced facts only" className="min-h-24 rounded border p-2" />
      <textarea name="localReading" required placeholder="Local reading — clearly labelled editorial interpretation" className="min-h-24 rounded border p-2" />
      <button className="w-full sm:w-fit rounded bg-brand-600 px-4 py-2 text-white">Save draft for review</button>
    </form>
    <section className="mt-10">
      <h2 className="text-xl font-semibold">Review queue</h2>
      <div className="mt-3 divide-y rounded-xl border">
        {articles.length === 0 ? <p className="p-5 text-slate-500">No articles yet.</p> : articles.map((a: any) => <div key={a.id} className="flex flex-col items-start gap-3 sm:flex-row sm:items-center p-4">
          <div className="flex-1">
            <p className="font-medium">{a.headline}</p>
            <p className="text-sm text-slate-500">{a.town} · {a.source_name} · {a.status} · effective {a.effective_story_date ?? "not selected"}</p>
            {a.status === "review_required" && <p className="mt-1 text-sm text-amber-700">Review required: {a.duplicate_reason ?? "complete or reconcile date evidence before publication."}</p>}
          </div>
          {a.status === "draft" && a.duplicate_state === "unique" && <form action={publishArticle} className="w-full sm:w-auto"><input type="hidden" name="id" value={a.id} /><button className="w-full rounded border px-3 py-1 text-sm sm:w-auto">Approve & publish</button></form>}
        </div>)}
      </div>
    </section>
  </main>;
}
