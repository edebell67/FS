/**
 * app/review/[token]/page.tsx — Capability-scoped owner review screen with structured per-page feedback.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-08-05 · Initial non-indexed owner review UI; does not expose administration.
 */
import type { Metadata } from "next";
import { getOwnerReviewByRawToken } from "@/lib/owner-review/repository";
import { submitOwnerReviewAction } from "./actions";
export const dynamic = "force-dynamic";
export const metadata: Metadata = { robots: { index: false, follow: false }, referrer: "no-referrer" };
export default async function OwnerReviewPage({ params }: { params: Promise<{ token: string }> }) {
  const { token } = await params; const review = await getOwnerReviewByRawToken(token);
  if (!review) return <main className="mx-auto max-w-xl p-8"><h1 className="text-2xl font-semibold">This review link is unavailable</h1><p className="mt-2">It may have expired or already been used.</p></main>;
  const action = submitOwnerReviewAction.bind(null, token);
  return <main className="mx-auto max-w-xl p-8"><h1 className="text-2xl font-semibold">Review {review.businessName}</h1><p className="mt-2 text-slate-600">Choose an outcome and leave concise per-page feedback. Your review is saved directly; no email is sent.</p><form action={action} className="mt-6 space-y-4"><fieldset><legend className="font-medium">Overall decision</legend><label><input type="radio" name="decision" value="accept" required /> Accept</label> <label><input type="radio" name="decision" value="change" /> Request changes</label> <label><input type="radio" name="decision" value="decline" /> Decline</label></fieldset><details className="rounded border p-3"><summary>Home page</summary><p><label><input type="checkbox" name="noActionRequired" defaultChecked /> No action required for this page</label></p><p>Structured selections and anything else are included by the protected preview client.</p></details><input type="hidden" name="pages" value={JSON.stringify([{ pageKey: "home", noActionRequired: true, selections: [], anythingElse: "", pageOpenDateTime: null }])} /><input type="hidden" name="pageOpenDateTime" value="" /><input type="hidden" name="anythingElse" value="" /><button className="rounded bg-brand-600 px-4 py-2 text-white">Submit review</button></form></main>;
}
