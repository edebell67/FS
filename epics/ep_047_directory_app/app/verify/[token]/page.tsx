import type { Metadata } from "next";
import { getVerificationByRawToken } from "@/lib/verification/repository";
import { submitVerificationAction } from "./actions";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { robots: { index: false, follow: false }, referrer: "no-referrer" };

export default async function VerifyPage({ params, searchParams }: {
  params: Promise<{ token: string }>; searchParams: Promise<{ error?: string }>;
}) {
  const { token } = await params;
  const record = await getVerificationByRawToken(token);
  const { error } = await searchParams;
  if (!record) return <Unavailable />;
  const action = submitVerificationAction.bind(null, token);
  const fields = [
    ["businessName", "Business name"], ["tradingName", "Trading name"], ["phone", "Phone"],
    ["email", "Listing email"], ["website", "Website"], ["address", "Address"],
    ["town", "Town"], ["postcode", "Postcode"], ["category", "Category"],
  ] as const;
  const outstanding = record.validationStatusAtIssue === "partially_validated"
    ? new Set(Array.isArray(record.outstandingFields) ? record.outstandingFields.filter((field): field is string => typeof field === "string") : [])
    : new Set<string>();
  return (
    <main className="mx-auto max-w-xl px-5 py-10">
      <p className="text-sm font-medium text-brand-600">Verify your listing</p>
      <h1 className="mt-2 text-2xl font-semibold">We have a listing for {record.businessName}.</h1>
      <p className="mt-2 text-slate-600">Help us make sure local customers see the right details.</p>
      {outstanding.size > 0 && <p className="mt-4 rounded border border-amber-300 bg-amber-50 p-3 text-sm text-amber-900">
        Fields marked “Needs confirmation” are the only outstanding data-quality items for this listing.
      </p>}
      {error && <p role="alert" className="mt-4 rounded bg-red-50 p-3 text-sm text-red-700">Please complete every required confirmation.</p>}
      <form action={action} className="mt-6 space-y-4">
        {fields.map(([name, label]) => (
          <label key={name} className={`block rounded text-sm font-medium text-slate-700 ${outstanding.has(name) ? "border border-amber-300 bg-amber-50 p-3" : ""}`}>
            {label} {outstanding.has(name) && <span className="ml-2 rounded bg-amber-200 px-2 py-0.5 text-xs text-amber-900">Needs confirmation</span>}
            <input name={name} defaultValue={record[name] ?? ""} maxLength={300}
              className="mt-1 block w-full rounded-md border border-slate-300 px-3 py-2" />
          </label>
        ))}
        <div className="border-t pt-4">
          <label className="block text-sm font-medium">Your name
            <input name="requesterName" required maxLength={200} className="mt-1 block w-full rounded-md border px-3 py-2" />
          </label>
          <label className="mt-3 block text-sm font-medium">Your relationship
            <select name="relationship" required defaultValue="" className="mt-1 block w-full rounded-md border px-3 py-2">
              <option value="" disabled>Select…</option><option value="owner">Owner</option>
              <option value="employee">Employee</option><option value="authorised_representative">Authorised representative</option>
              <option value="other">Other</option>
            </select>
          </label>
          <div className="mt-3 grid gap-3 sm:grid-cols-2">
            <label className="text-sm">Preferred email<input name="contactEmail" type="email" maxLength={320} className="mt-1 block w-full rounded-md border px-3 py-2" /></label>
            <label className="text-sm">Preferred phone<input name="contactPhone" maxLength={50} className="mt-1 block w-full rounded-md border px-3 py-2" /></label>
          </div>
          <label className="mt-4 flex gap-2 text-sm"><input name="accuracyConfirmed" type="checkbox" required />
            <span>I confirm the information I submitted is accurate to the best of my knowledge.</span>
          </label>
          <p className="mt-3 text-xs text-slate-500">Your submission is sent for review and will not automatically change the public listing.</p>
        </div>
        <button className="w-full rounded-md bg-brand-600 px-4 py-3 font-medium text-white">Submit verification</button>
      </form>
    </main>
  );
}

function Unavailable() {
  return <main className="mx-auto max-w-xl px-5 py-20"><h1 className="text-2xl font-semibold">This verification link is unavailable</h1>
    <p className="mt-3 text-slate-600">It may have expired or already been used. You can request a new review from the listing page.</p></main>;
}
