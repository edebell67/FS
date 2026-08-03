import type { Metadata } from "next";

export const metadata: Metadata = { robots: { index: false, follow: false }, referrer: "no-referrer" };

export default function CompletePage() {
  return <main className="mx-auto max-w-xl px-5 py-16">
    <p className="text-sm font-medium text-brand-600">Verification received</p>
    <h1 className="mt-2 text-2xl font-semibold text-slate-900">Thank you — we have received your verification.</h1>
    <p className="mt-3 text-slate-600">Your listing has not changed publicly. Your submission is now awaiting manual review.</p>
    <section className="mt-6 rounded-lg border border-green-200 bg-green-50 p-4 text-slate-800">
      <h2 className="font-semibold">What happens next</h2>
      <p className="mt-2 text-sm">A team member will review your information and claim request. We will contact you if anything further is needed.</p>
    </section>
  </main>;
}
