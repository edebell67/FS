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
      <section className="border-b-2 border-[#152022] pb-12 text-center">
        <p className="font-mono text-[11px] font-medium uppercase tracking-[0.12em] text-brand-700">Local business directory</p>
        <h1 className="mt-3 font-display text-4xl font-semibold tracking-[-0.045em] text-[#152022] sm:text-6xl">
          Find a business you can trust
        </h1>
        <p className="mx-auto mt-4 max-w-xl text-[#667174]">
          {summary.total} businesses across {summary.categoryCount} categories and{" "}
          {summary.townCount} towns.
        </p>

        <form action="/directory/search" className="mx-auto mt-7 flex max-w-xl gap-2">
          <input
            type="text"
            name="q"
            placeholder="Search by name, category, or town…"
            className="flex-1 rounded-sm border border-[#b9b6ad] bg-[#fffdf9] px-4 py-3 text-sm outline-none transition focus:border-brand-600 focus:ring-4 focus:ring-brand-100"
          />
          <button
            type="submit"
            className="rounded-sm bg-brand-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-brand-700"
          >
            Search
          </button>
        </form>
      </section>

      <section className="mt-12">
        <div className="mb-3 flex items-baseline justify-between">
          <h2 className="font-display text-3xl font-semibold tracking-[-0.03em] text-[#152022]">Browse by category</h2>
          <Link href="/directory/search" className="font-mono text-[11px] font-medium uppercase tracking-[0.08em] text-brand-700 hover:text-brand-600">
            All categories →
          </Link>
        </div>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-4">
          {topCategories.map((c) => (
            <Link
              key={c.slug}
              href={`/directory/category/${c.slug}`}
              className="rounded-sm border border-[#d6d2c9] bg-[#fffdf8] px-4 py-3 text-sm transition hover:border-brand-600 hover:bg-brand-50"
            >
              <span className="font-medium capitalize text-[#152022]">{c.label}</span>
              <span className="ml-1.5 text-[#7a8587]">({c.count})</span>
            </Link>
          ))}
        </div>
      </section>

      <section className="mt-12">
        <div className="mb-3 flex items-baseline justify-between">
          <h2 className="font-display text-3xl font-semibold tracking-[-0.03em] text-[#152022]">Browse by town</h2>
        </div>
        <div className="flex flex-wrap gap-2">
          {topTowns.map((t) => (
            <Link
              key={t.slug}
              href={`/directory/town/${t.slug}`}
              className="rounded-full border border-[#bfd4cf] bg-[#fffdf8] px-3 py-1.5 text-sm capitalize transition hover:border-brand-600 hover:bg-brand-50"
            >
              {t.label} <span className="text-[#7a8587]">({t.count})</span>
            </Link>
          ))}
        </div>
      </section>

      <section className="mt-12">
        <h2 className="mb-3 font-display text-3xl font-semibold tracking-[-0.03em] text-[#152022]">A–Z</h2>
        <div className="flex flex-wrap gap-1.5">
          {letters.map((letter) => (
            <Link
              key={letter}
              href={`/directory/search?letter=${letter}`}
              className="flex h-8 w-8 items-center justify-center rounded-sm border border-[#d6d2c9] bg-[#fffdf8] text-sm font-medium transition hover:border-brand-600 hover:bg-brand-50"
            >
              {letter}
            </Link>
          ))}
        </div>
      </section>

      <section className="mt-12">
        <h2 className="mb-3 font-display text-3xl font-semibold tracking-[-0.03em] text-[#152022]">Newest listings</h2>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          {newest.map((b) => (
            <Link
              key={b.id}
              href={`/directory/business/${b.slug}`}
              className="flex items-center justify-between rounded-sm border border-[#d6d2c9] bg-[#fffdf8] px-4 py-3 transition hover:border-brand-600 hover:bg-brand-50"
            >
              <div>
                <p className="font-medium text-[#152022]">{b.businessName}</p>
                <p className="text-sm capitalize text-[#667174]">
                  {b.category}
                  {b.town ? ` · ${b.town}` : ""}
                </p>
              </div>
              <span className="font-mono text-[11px] text-[#7a8587]">{format(b.importDate, "d MMM")}</span>
            </Link>
          ))}
        </div>
      </section>
    </main>
  );
}
