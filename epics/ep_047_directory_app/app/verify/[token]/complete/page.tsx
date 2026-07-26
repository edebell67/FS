import type { Metadata } from "next";
export const metadata: Metadata = { robots: { index: false, follow: false }, referrer: "no-referrer" };
export default function CompletePage() {
  return <main className="mx-auto max-w-xl px-5 py-20"><p className="text-sm font-medium text-green-700">Submitted</p>
    <h1 className="mt-2 text-2xl font-semibold">Your details have been received.</h1>
    <h2 className="mt-6 text-lg font-semibold">Claim Your Business</h2>
    <p className="mt-2 text-slate-600">Your claim is pending. A team member will review this claim before changes go live.</p></main>;
}
