import type { Metadata } from "next";
import { getBusinessByRef } from "@/lib/db/queries/directory";
import { listBusinesses } from "@/lib/db/queries/businesses";
import { publicClaimAction } from "./actions";
export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Claim my listing", robots: { index: false, follow: true } };
export default async function ClaimPage({ searchParams }: { searchParams: Promise<{ business?: string; q?: string }> }) {
  const { business: ref, q } = await searchParams;
  const selected = ref ? await getBusinessByRef(ref) : null;
  const results = !selected && q ? (await listBusinesses({ q, page: 1, sort: "name" })).rows.slice(0, 10) : [];
  return <main className="mx-auto max-w-xl px-5 py-12"><h1 className="text-2xl font-semibold">Claim my listing</h1>
    <p className="mt-2 text-slate-600">Request verification and manual review. No listing changes are made now.</p>
    {!selected && <form className="mt-6 flex gap-2"><input name="q" defaultValue={q} required placeholder="Business name or town" className="flex-1 rounded-md border px-3 py-2" /><button className="rounded-md border px-4">Search</button></form>}
    {results.map((r) => <a key={r.id} href={`/claim?business=${encodeURIComponent(r.businessRef)}`} className="mt-2 block rounded border p-3">{r.businessName}<span className="block text-sm text-slate-500">{r.category}{r.town ? ` · ${r.town}` : ""}</span></a>)}
    {selected && <form action={publicClaimAction} className="mt-6 space-y-4">
      <input type="hidden" name="businessRef" value={selected.businessRef} />
      <p className="rounded bg-slate-50 p-3 font-medium">{selected.businessName}<span className="block text-sm font-normal text-slate-500">{selected.town}</span></p>
      <label className="block text-sm">Your name<input name="requesterName" required maxLength={200} className="mt-1 block w-full rounded border px-3 py-2" /></label>
      <label className="block text-sm">Relationship<select name="relationship" required className="mt-1 block w-full rounded border px-3 py-2"><option value="owner">Owner</option><option value="employee">Employee</option><option value="authorised_representative">Authorised representative</option><option value="other">Other</option></select></label>
      <label className="block text-sm">Email<input name="email" type="email" maxLength={320} className="mt-1 block w-full rounded border px-3 py-2" /></label>
      <label className="block text-sm">Mobile number<input name="phone" maxLength={50} className="mt-1 block w-full rounded border px-3 py-2" /></label>
      <label className="hidden" aria-hidden="true">Website<input name="website" tabIndex={-1} autoComplete="off" /></label>
      <label className="flex gap-2 text-sm"><input type="checkbox" name="acknowledged" required />I confirm this request is accurate and agree to the privacy notice.</label>
      <button className="w-full rounded bg-brand-600 px-4 py-3 font-medium text-white">Request verification</button>
    </form>}
  </main>;
}
