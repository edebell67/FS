import Link from "next/link";

export interface BusinessCardData {
  slug: string;
  businessName: string;
  category: string;
  town: string | null;
}

export function BusinessCard({ business }: { business: BusinessCardData }) {
  return (
    <Link
      href={`/directory/business/${business.slug}`}
      className="block rounded-lg border border-slate-200 p-4 transition-colors hover:border-brand-300 hover:bg-brand-50/40"
    >
      <p className="font-medium text-slate-900">{business.businessName}</p>
      <p className="mt-1 text-sm capitalize text-slate-500">
        {business.category}
        {business.town ? ` · ${business.town}` : ""}
      </p>
    </Link>
  );
}
