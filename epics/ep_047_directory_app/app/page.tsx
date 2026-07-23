import Link from "next/link";
import { format } from "date-fns";
import {
  getAvailableLetters,
  getCategoryCounts,
  getDirectorySummary,
  getNewestBusinesses,
  getTownCounts,
} from "@/lib/db/queries/directory";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  const [summary, categories, towns, newest, letters] = await Promise.all([
    getDirectorySummary(),
    getCategoryCounts(),
    getTownCounts(),
    getNewestBusinesses(8),
    getAvailableLetters(),
  ]);

  const topCategories = categories.slice(0, 12);
  const topTowns = towns.slice(0, 12);

  return (
    <main className="mx-auto max-w-6xl px-6 py-12">
      <section className="text-center">
        <h1 className="text-3xl font-semibold tracking-tight text-slate-900 sm:text-4xl">
          Find a business you can trust
        </h1>
        <p className="mx-auto mt-3 max-w-xl text-slate-600">
          {summary.total} businesses across {summary.categoryCount} categories and{" "}
          {summary.townCount} towns.
        </p>

        <form action="/search" className="mx-auto mt-6 flex max-w-lg gap-2">
          <input
            type="text"
            name="q"
            placeholder="Search by name, category, or town…"
            className="flex-1 rounded-md border border-slate-300 px-4 py-2.5 text-sm"
          />
          <button
            type="submit"
            className="rounded-md bg-brand-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-brand-700"
          >
            Search
          </button>
        </form>
      </section>

      <section className="mt-12">
        <div className="mb-3 flex items-baseline justify-between">
          <h2 className="text-lg font-semibold text-slate-900">Browse by category</h2>
          <Link href="/search" className="text-sm font-medium text-brand-600 hover:text-brand-700">
            All categories →
          </Link>
        </div>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-4">
          {topCategories.map((c) => (
            <Link
              key={c.slug}
              href={`/category/${c.slug}`}
              className="rounded-lg border border-slate-200 px-4 py-3 text-sm hover:border-brand-300 hover:bg-brand-50/40"
            >
              <span className="font-medium capitalize text-slate-900">{c.label}</span>
              <span className="ml-1.5 text-slate-400">({c.count})</span>
            </Link>
          ))}
        </div>
      </section>

      <section className="mt-12">
        <div className="mb-3 flex items-baseline justify-between">
          <h2 className="text-lg font-semibold text-slate-900">Browse by town</h2>
        </div>
        <div className="flex flex-wrap gap-2">
          {topTowns.map((t) => (
            <Link
              key={t.slug}
              href={`/town/${t.slug}`}
              className="rounded-full border border-slate-200 px-3 py-1.5 text-sm capitalize hover:border-brand-300 hover:bg-brand-50/40"
            >
              {t.label} <span className="text-slate-400">({t.count})</span>
            </Link>
          ))}
        </div>
      </section>

      <section className="mt-12">
        <h2 className="mb-3 text-lg font-semibold text-slate-900">A–Z</h2>
        <div className="flex flex-wrap gap-1.5">
          {letters.map((letter) => (
            <Link
              key={letter}
              href={`/search?letter=${letter}`}
              className="flex h-8 w-8 items-center justify-center rounded-md border border-slate-200 text-sm font-medium hover:border-brand-300 hover:bg-brand-50/40"
            >
              {letter}
            </Link>
          ))}
        </div>
      </section>

      <section className="mt-12">
        <h2 className="mb-3 text-lg font-semibold text-slate-900">Newest listings</h2>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          {newest.map((b) => (
            <Link
              key={b.id}
              href={`/business/${b.slug}`}
              className="flex items-center justify-between rounded-lg border border-slate-200 px-4 py-3 hover:border-brand-300 hover:bg-brand-50/40"
            >
              <div>
                <p className="font-medium text-slate-900">{b.businessName}</p>
                <p className="text-sm capitalize text-slate-500">
                  {b.category}
                  {b.town ? ` · ${b.town}` : ""}
                </p>
              </div>
              <span className="text-xs text-slate-400">{format(b.importDate, "d MMM")}</span>
            </Link>
          ))}
        </div>
      </section>
    </main>
  );
}
