import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { listBusinesses, parsePage } from "@/lib/db/queries/businesses";
import { fromSlug, getTownCounts } from "@/lib/db/queries/directory";
import { Breadcrumbs } from "@/components/directory/Breadcrumbs";
import { BusinessCard } from "@/components/directory/BusinessCard";
import { Pagination } from "@/components/directory/Pagination";
import { SITE_URL } from "@/lib/site-config";

export const dynamic = "force-dynamic";

interface PageProps {
  params: Promise<{ town: string }>;
  searchParams: Promise<{ page?: string; category?: string }>;
}

async function resolveTown(slug: string) {
  const towns = await getTownCounts();
  return towns.find((t) => t.slug === slug) ?? null;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { town: slug } = await params;
  const town = await resolveTown(slug);
  if (!town) return {};
  return {
    title: `Businesses in ${town.label}`,
    description: `Browse ${town.count} businesses in ${town.label}.`,
  };
}

export default async function TownPage({ params, searchParams }: PageProps) {
  const { town: slug } = await params;
  const search = await searchParams;
  const town = await resolveTown(slug);
  if (!town) notFound();

  const page = parsePage(search.page);
  const { rows, total, pageCount } = await listBusinesses({
    town: fromSlug(slug),
    category: search.category ? fromSlug(search.category) : undefined,
    page,
    sort: "name",
  });

  return (
    <main className="mx-auto max-w-4xl px-6 py-12">
      <Breadcrumbs baseUrl={SITE_URL} items={[{ label: "Home", href: "/directory" }, { label: town.label }]} />
      <h1 className="text-2xl font-semibold capitalize tracking-tight text-slate-900">
        Businesses in {town.label}
      </h1>
      <p className="mt-2 text-slate-600">
        {total} business{total === 1 ? "" : "es"} in this town.
      </p>

      <div className="mt-8 grid grid-cols-1 gap-3 sm:grid-cols-2">
        {rows.map((row) => (
          <BusinessCard key={row.id} business={row} />
        ))}
      </div>

      <Pagination
        page={page}
        pageCount={pageCount}
        basePath={`/directory/town/${slug}`}
        searchParams={{ category: search.category }}
      />
    </main>
  );
}
