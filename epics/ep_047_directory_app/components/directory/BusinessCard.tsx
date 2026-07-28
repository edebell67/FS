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
      className="block rounded-sm border border-[#d6d2c9] bg-[#fffdf8] p-4 transition-colors hover:border-brand-600 hover:bg-brand-50"
    >
      <p className="font-medium text-[#152022]">{business.businessName}</p>
      <p className="mt-1 text-sm capitalize text-[#667174]">
        {business.category}
        {business.town ? ` · ${business.town}` : ""}
      </p>
    </Link>
  );
}
