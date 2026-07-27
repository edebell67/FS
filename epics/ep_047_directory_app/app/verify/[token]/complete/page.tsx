import type { Metadata } from "next";
export const metadata: Metadata = { robots: { index: false, follow: false }, referrer: "no-referrer" };
export default function CompletePage() {
  return <main className="mx-auto max-w-xl px-5 py-20"><p className="text-sm font-medium text-green-700">Submitted</p>
    <h1 className="mt-2 text-2xl font-semibold">Your listing and claim request have been received.</h1>
    <section className="mt-6 rounded-lg border border-green-200 bg-green-50 p-4">
      <h2 className="text-lg font-semibold text-slate-900">Claim request submitted</h2>
      <p className="mt-2 text-slate-700">You have already requested to claim this business. A team member will review your request before any listing changes go live.</p>
    </section></main>;
}
