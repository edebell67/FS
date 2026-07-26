"use client";
import { useState } from "react";
import {
  getDeliveryStatePresentation,
  type VerificationDeliveryState,
} from "@/lib/verification/delivery-status";

type PreparedLink = {
  url: string;
  linkId: string;
  expiresAt: string;
  deliveryState: "not_sent";
};

export function VerificationLinkPanel({
  businessRef,
  initialDeliveryState = "not_sent",
}: {
  businessRef: string;
  initialDeliveryState?: VerificationDeliveryState;
}) {
  const [expiry, setExpiry] = useState(5);
  const [result, setResult] = useState<PreparedLink | null>(null);
  const [deliveryState, setDeliveryState] =
    useState<VerificationDeliveryState>(initialDeliveryState);
  const [error, setError] = useState("");
  const delivery = getDeliveryStatePresentation(deliveryState);
  async function create() {
    setError("");
    const response = await fetch(`/directoryadmin/api/businesses/${encodeURIComponent(businessRef)}/verification-link`, {
      method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ expiresInDays: expiry }),
    });
    const body = await response.json();
    if (!response.ok) return setError(body.error || "Unable to create link.");
    setResult(body);
    setDeliveryState("not_sent");
  }
  async function revoke() {
    if (!result) return;
    const response = await fetch(`/directoryadmin/api/businesses/${encodeURIComponent(businessRef)}/verification-link?linkId=${encodeURIComponent(result.linkId)}`, { method: "DELETE" });
    if (response.ok) setDeliveryState("revoked"); else setError("Unable to revoke link.");
  }
  return <section className="mt-8 rounded-xl border border-slate-200 p-5">
    <h2 className="font-semibold">Verification delivery</h2>
    <p className="mt-1 text-sm text-slate-600">Prepare and preview a secure link. This does not send email or any external message.</p>
    <div role="status" aria-live="polite" className="mt-4 rounded-lg border-2 border-amber-300 bg-amber-50 p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-amber-800">Immutable delivery state</p>
      <p className="mt-1 text-lg font-semibold text-slate-900">{delivery.label}</p>
      {delivery.explanation && <p className="mt-1 text-sm font-medium text-slate-700">{delivery.explanation}</p>}
    </div>
    <div className="mt-4 flex items-end gap-3"><label className="text-sm">Expiry
      <select value={expiry} onChange={(e) => setExpiry(Number(e.target.value))} className="mt-1 block rounded border px-3 py-2">
        {[1,3,5,7,10,14].map((d) => <option key={d} value={d}>{d} day{d === 1 ? "" : "s"}</option>)}
      </select></label><button onClick={create} className="rounded bg-brand-600 px-4 py-2 text-sm font-medium text-white">Prepare verification delivery</button></div>
    {error && <p role="alert" className="mt-3 text-sm text-red-700">{error}</p>}
    {result && <div className="mt-4 rounded bg-amber-50 p-3 text-sm"><p className="font-medium">Copy-only preview — shown once</p>
      <input readOnly value={result.url} onFocus={(e) => e.currentTarget.select()} className="mt-2 w-full rounded border bg-white px-2 py-2 font-mono text-xs" />
      <p className="mt-1 text-xs text-slate-600">Expires {new Date(result.expiresAt).toLocaleString()}</p>
      {deliveryState !== "revoked" &&
        <button onClick={revoke} className="mt-2 text-sm font-medium text-red-700">Revoke link</button>}
    </div>}
  </section>;
}
