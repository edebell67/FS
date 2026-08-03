import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = { robots: { index: false, follow: false }, referrer: "no-referrer" };

export default function RequestVerificationLinkPage() {
  return <main className="mx-auto max-w-xl px-5 py-16">
    <p className="text-sm font-medium text-brand-600">Verification link request</p>
    <h1 className="mt-2 text-2xl font-semibold text-slate-900">Request a new verification link</h1>
    <p className="mt-3 text-slate-600">To protect listings, a replacement link is prepared only after the business and contact route have been reviewed. It is never sent automatically.</p>
    <Link href="/directory" className="mt-6 inline-block rounded-md bg-brand-600 px-4 py-3 font-medium text-white">Find your business listing</Link>
    <p className="mt-4 text-sm text-slate-500">Open your listing and use “Claim my listing” to submit the request for review.</p>
  </main>;
}
