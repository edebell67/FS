import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Phone, Mail, Globe, MapPin, Facebook, Instagram, Linkedin } from "lucide-react";
import {
  getBusinessBySlug,
  getNearbyBusinesses,
  getRelatedBusinesses,
  toSlug,
} from "@/lib/db/queries/directory";
import { Breadcrumbs } from "@/components/directory/Breadcrumbs";
import { BusinessCard } from "@/components/directory/BusinessCard";
import { SITE_URL, SITE_NAME } from "@/lib/site-config";

export const dynamic = "force-dynamic";

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const business = await getBusinessBySlug(slug);
  if (!business) return {};

  const locationBit = business.town ? ` in ${business.town}` : "";
  const description =
    business.description ??
    `${business.businessName} — ${business.category}${locationBit}. Contact details, and how to get in touch, on ${SITE_NAME}.`;

  return {
    title: business.businessName,
    description,
    alternates: { canonical: `${SITE_URL}/directory/business/${business.slug}` },
  };
}

function normalizeWebsiteHref(website: string): string {
  return /^https?:\/\//i.test(website) ? website : `https://${website}`;
}

export default async function BusinessProfilePage({ params }: PageProps) {
  const { slug } = await params;
  const business = await getBusinessBySlug(slug);
  if (!business) notFound();

  const [related, nearby] = await Promise.all([
    getRelatedBusinesses(business.category, business.id, 4),
    business.town ? getNearbyBusinesses(business.town, business.id, 4) : Promise.resolve([]),
  ]);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    name: business.businessName,
    url: `${SITE_URL}/directory/business/${business.slug}`,
    ...(business.phone ? { telephone: business.phone } : {}),
    ...(business.email ? { email: business.email } : {}),
    ...(business.website ? { sameAs: [normalizeWebsiteHref(business.website)] } : {}),
    ...(business.address || business.town || business.postcode
      ? {
          address: {
            "@type": "PostalAddress",
            ...(business.address ? { streetAddress: business.address } : {}),
            ...(business.town ? { addressLocality: business.town } : {}),
            ...(business.county ? { addressRegion: business.county } : {}),
            ...(business.postcode ? { postalCode: business.postcode } : {}),
            addressCountry: "GB",
          },
        }
      : {}),
    ...(business.latitude && business.longitude
      ? { geo: { "@type": "GeoCoordinates", latitude: business.latitude, longitude: business.longitude } }
      : {}),
    ...(business.googleRating && business.reviewCount
      ? {
          aggregateRating: {
            "@type": "AggregateRating",
            ratingValue: business.googleRating,
            reviewCount: business.reviewCount,
          },
        }
      : {}),
  };

  return (
    <main className="mx-auto max-w-4xl px-6 py-12">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

      <Breadcrumbs
        baseUrl={SITE_URL}
        items={[
          { label: "Home", href: "/directory" },
          { label: business.category, href: `/directory/category/${toSlug(business.category)}` },
          { label: business.businessName },
        ]}
      />

      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-slate-900 sm:text-3xl">
            {business.businessName}
          </h1>
          <p className="mt-1 capitalize text-slate-500">
            {business.category}
            {business.subCategory ? ` · ${business.subCategory}` : ""}
            {business.town ? ` · ${business.town}` : ""}
          </p>
        </div>
        <span className="whitespace-nowrap rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700">
          {business.stageLabel ?? "Listed"}
        </span>
      </div>

      {business.description && <p className="mt-6 text-slate-700">{business.description}</p>}

      <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2">
        <section className="rounded-xl border border-slate-200 p-5">
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500">
            Contact
          </h2>
          <ul className="space-y-2 text-sm">
            {business.phone && (
              <li className="flex items-center gap-2">
                <Phone className="h-4 w-4 text-slate-400" aria-hidden="true" />
                <a href={`tel:${business.phone}`} className="text-slate-700 hover:text-brand-600">
                  {business.phone}
                </a>
              </li>
            )}
            {business.mobile && (
              <li className="flex items-center gap-2">
                <Phone className="h-4 w-4 text-slate-400" aria-hidden="true" />
                <a href={`tel:${business.mobile}`} className="text-slate-700 hover:text-brand-600">
                  {business.mobile} (mobile)
                </a>
              </li>
            )}
            {business.email && (
              <li className="flex items-center gap-2">
                <Mail className="h-4 w-4 text-slate-400" aria-hidden="true" />
                <a href={`mailto:${business.email}`} className="text-slate-700 hover:text-brand-600">
                  {business.email}
                </a>
              </li>
            )}
            {business.website && (
              <li className="flex items-center gap-2">
                <Globe className="h-4 w-4 text-slate-400" aria-hidden="true" />
                <a
                  href={normalizeWebsiteHref(business.website)}
                  target="_blank"
                  rel="noopener noreferrer nofollow"
                  className="text-slate-700 hover:text-brand-600"
                >
                  {business.website}
                </a>
              </li>
            )}
            {(business.address || business.town || business.postcode) && (
              <li className="flex items-start gap-2">
                <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-slate-400" aria-hidden="true" />
                <span className="text-slate-700">
                  {[business.address, business.town, business.county, business.postcode]
                    .filter(Boolean)
                    .join(", ")}
                </span>
              </li>
            )}
            {!business.phone && !business.mobile && !business.email && !business.website && (
              <li className="text-slate-400">No contact details on file yet.</li>
            )}
          </ul>

          {(business.facebook || business.instagram || business.linkedin) && (
            <div className="mt-4 flex gap-3 border-t border-slate-100 pt-4">
              {business.facebook && (
                <a href={business.facebook} target="_blank" rel="noopener noreferrer" aria-label="Facebook">
                  <Facebook className="h-5 w-5 text-slate-400 hover:text-brand-600" />
                </a>
              )}
              {business.instagram && (
                <a href={business.instagram} target="_blank" rel="noopener noreferrer" aria-label="Instagram">
                  <Instagram className="h-5 w-5 text-slate-400 hover:text-brand-600" />
                </a>
              )}
              {business.linkedin && (
                <a href={business.linkedin} target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
                  <Linkedin className="h-5 w-5 text-slate-400 hover:text-brand-600" />
                </a>
              )}
            </div>
          )}
        </section>

        <section className="rounded-xl border border-dashed border-slate-300 p-5">
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500">
            Is this your business?
          </h2>
          <p className="text-sm text-slate-600">Request a secure verification and manual ownership review.</p>
          <Link href={`/claim?business=${encodeURIComponent(business.businessRef)}`}
            className="mt-4 block w-full rounded-md bg-brand-600 px-4 py-2 text-center text-sm font-medium text-white">
            Claim my listing
          </Link>
        </section>
      </div>

      {related.length > 0 && (
        <section className="mt-10">
          <h2 className="mb-3 text-lg font-semibold text-slate-900">
            More <span className="capitalize">{business.category}</span> businesses
          </h2>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            {related.map((r) => (
              <BusinessCard key={r.slug} business={r} />
            ))}
          </div>
        </section>
      )}

      {nearby.length > 0 && (
        <section className="mt-10">
          <h2 className="mb-3 text-lg font-semibold text-slate-900">
            Nearby in <span className="capitalize">{business.town}</span>
          </h2>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            {nearby.map((n) => (
              <BusinessCard key={n.slug} business={n} />
            ))}
          </div>
        </section>
      )}

      <p className="mt-10 text-xs text-slate-400">
        Ref {business.businessRef} ·{" "}
        <Link href="/directory/search" className="hover:underline">
          Back to search
        </Link>
      </p>
    </main>
  );
}
