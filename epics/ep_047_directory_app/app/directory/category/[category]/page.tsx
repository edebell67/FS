import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { listBusinesses, parsePage } from "@/lib/db/queries/businesses";
import { fromSlug, getCategoryCounts } from "@/lib/db/queries/directory";
import { Breadcrumbs } from "@/components/directory/Breadcrumbs";
import { BusinessCard } from "@/components/directory/BusinessCard";
import { Pagination } from "@/components/directory/Pagination";
import { SITE_URL } from "@/lib/site-config";

export const dynamic = "force-dynamic";

interface PageProps {
  params: Promise<{ category: string }>;
  searchParams: Promise<{ page?: string; town?: string }>;
}

async function resolveCategory(slug: string) {
  const categories = await getCategoryCounts();
  return categories.find((c) => c.slug === slug) ?? null;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { category: slug } = await params;
  const category = await resolveCategory(slug);
  if (!category) return {};
  const title = `${category.label} businesses`;
  return {
    title,
    description: `Browse ${category.count} ${category.label} businesses in the directory.`,
  };
}

export default async function CategoryPage({ params, searchParams }: PageProps) {
  const { category: slug } = await params;
  const search = await searchParams;
  const category = await resolveCategory(slug);
  if (!category) notFound();

  const page = parsePage(search.page);
  const { rows, total, pageCount } = await listBusinesses({
    category: fromSlug(slug),
    town: search.town ? fromSlug(search.town) : undefined,
    page,
    sort: "name",
  });

  return (
    <main className="mx-auto max-w-4xl px-6 py-12">
      <Breadcrumbs baseUrl={SITE_URL} items={[{ label: "Home", href: "/directory" }, { label: category.label }]} />
      <h1 className="text-2xl font-semibold capitalize tracking-tight text-slate-900">
        {category.label}
      </h1>
      <p className="mt-2 text-slate-600">
        {total} business{total === 1 ? "" : "es"} in this category.
      </p>

      <div className="mt-8 grid grid-cols-1 gap-3 sm:grid-cols-2">
        {rows.map((row) => (
          <BusinessCard key={row.id} business={row} />
        ))}
      </div>

      <Pagination
        page={page}
        pageCount={pageCount}
        basePath={`/directory/category/${slug}`}
        searchParams={{ town: search.town }}
      />
    </main>
  );
}
