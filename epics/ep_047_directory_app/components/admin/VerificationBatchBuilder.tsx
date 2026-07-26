"use client";

import Link from "next/link";
import { useMemo, useState } from "react";

type Business = {
  id: string; businessRef: string; businessName: string; email: string | null;
  town: string | null; validationStatus: string;
};
type PreparedItem = {
  itemId: string; businessRef: string; businessName: string; recipientChannel: string;
  recipientAddress: string | null; readiness: string; readinessReason: string | null;
  status: string; expiresAt: string; url: string;
};
type Result = {
  batchId: string; status: string; readyCount: number; totalCount: number;
  delivery: { canSend: false; reason: string }; items: PreparedItem[];
};

export function VerificationBatchBuilder({ businesses, allowPartial }: { businesses: Business[]; allowPartial: boolean }) {
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [expiry, setExpiry] = useState(5);
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [includePartial, setIncludePartial] = useState(false);
  const selectable = useMemo(() => businesses.filter((business) =>
    business.validationStatus === "validated" || (allowPartial && includePartial)), [businesses, allowPartial, includePartial]);
  const selectedReady = useMemo(() =>
    businesses.filter((b) => selected.has(b.id) && b.email).length, [businesses, selected]);

  function toggle(id: string) {
    setSelected((current) => {
      const next = new Set(current);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  }

  async function prepare() {
    setBusy(true); setError("");
    try {
      const response = await fetch("/directoryadmin/api/verification-batches", {
        method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify({ businessIds: [...selected], expiresInDays: expiry, includePartial }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error || "Unable to prepare batch.");
      setResult(body);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to prepare batch.");
    } finally { setBusy(false); }
  }

  if (result) return <section>
    <div className="rounded-lg border border-amber-200 bg-amber-50 p-4">
      <h2 className="font-semibold">Batch prepared — secure links shown once</h2>
      <p className="mt-1 text-sm">
        {result.readyCount}/{result.totalCount} individually ready. Batch status: <strong>{result.status}</strong>.
        Outbound send: <strong>not ready</strong> — {result.delivery.reason}
      </p>
      <Link href={`/directoryadmin/verification-batches/${result.batchId}`}
        className="mt-2 inline-block text-sm font-medium text-brand-700">Open durable audit queue →</Link>
    </div>
    <div className="mt-5 overflow-x-auto">
      <table className="w-full text-left text-sm"><thead><tr className="border-b">
        <th className="p-2">Business</th><th className="p-2">Recipient route</th>
        <th className="p-2">Expiry</th><th className="p-2">Status/readiness</th><th className="p-2">Secure link</th>
      </tr></thead><tbody>{result.items.map((item) => <tr key={item.itemId} className="border-b align-top">
        <td className="p-2">{item.businessName}<br/><span className="font-mono text-xs">{item.businessRef}</span></td>
        <td className="p-2">{item.recipientChannel}: {item.recipientAddress || "not configured"}</td>
        <td className="p-2">{new Date(item.expiresAt).toLocaleString()}</td>
        <td className="p-2">{item.status} / {item.readiness}
          {item.readinessReason && <div className="text-xs text-red-700">{item.readinessReason}</div>}</td>
        <td className="p-2"><input aria-label={`Secure link for ${item.businessName}`} readOnly value={item.url}
          onFocus={(event) => event.currentTarget.select()} className="w-72 rounded border bg-white px-2 py-1 font-mono text-xs"/></td>
      </tr>)}</tbody></table>
    </div>
  </section>;

  return <section>
    <div className="flex flex-wrap items-end gap-3 rounded-lg border border-slate-200 p-4">
      <label className="text-sm">Expiry
        <select value={expiry} onChange={(event) => setExpiry(Number(event.target.value))}
          className="mt-1 block rounded border px-3 py-2">
          {[1, 3, 5, 7, 10, 14].map((days) => <option key={days} value={days}>{days} day{days === 1 ? "" : "s"}</option>)}
        </select>
      </label>
      <button disabled={busy || selected.size === 0} onClick={prepare}
        className="rounded bg-brand-600 px-4 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-50">
        {busy ? "Preparing…" : `Prepare ${selected.size} verification link${selected.size === 1 ? "" : "s"}`}
      </button>
      <p className="text-sm text-slate-600">{selectedReady}/{selected.size} selected have an email route.</p>
      {allowPartial && <label className="flex items-center gap-2 text-sm">
        <input type="checkbox" checked={includePartial} onChange={(event) => {
          setIncludePartial(event.target.checked);
          if (!event.target.checked) setSelected((current) => new Set([...current].filter((id) =>
            businesses.find((business) => business.id === id)?.validationStatus === "validated")));
        }} />
        Allow explicitly marked partially validated records
      </label>}
    </div>
    {error && <p role="alert" className="mt-3 text-sm text-red-700">{error}</p>}
    <div className="mt-5 overflow-x-auto"><table className="w-full text-left text-sm">
      <thead><tr className="border-b"><th className="p-2">
        <input aria-label="Select all eligible businesses" type="checkbox"
          checked={selected.size === selectable.length && selectable.length > 0}
          onChange={(event) => setSelected(event.target.checked ? new Set(selectable.map((b) => b.id)) : new Set())}/>
      </th><th className="p-2">Business</th><th className="p-2">Calculated validation</th><th className="p-2">Recipient route</th><th className="p-2">Send readiness</th></tr></thead>
      <tbody>{businesses.map((business) => <tr key={business.id} className="border-b">
        <td className="p-2"><input aria-label={`Select ${business.businessName}`} type="checkbox"
          disabled={business.validationStatus === "partially_validated" && (!allowPartial || !includePartial)}
          checked={selected.has(business.id)} onChange={() => toggle(business.id)}/></td>
        <td className="p-2"><Link className="font-medium hover:text-brand-600"
          href={`/directoryadmin/businesses/${business.businessRef}`}>{business.businessName}</Link>
          <div className="font-mono text-xs text-slate-500">{business.businessRef}</div></td>
        <td className="p-2"><span className={business.validationStatus === "validated"
          ? "rounded bg-emerald-50 px-2 py-1 text-emerald-700"
          : "rounded bg-amber-100 px-2 py-1 font-semibold text-amber-800"}>
          {business.validationStatus === "validated" ? "Validated" : "Partial — outstanding fields"}
        </span></td>
        <td className="p-2">email: {business.email || "not configured"}</td>
        <td className="p-2">{business.email ? "individually ready" : "not ready"}</td>
      </tr>)}</tbody>
    </table>{businesses.length === 0 && <p className="p-6 text-center text-slate-500">No active businesses have a validated or partially validated calculated status.</p>}</div>
  </section>;
}
