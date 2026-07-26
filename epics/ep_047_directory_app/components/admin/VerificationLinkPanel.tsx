"use client";
import { useState } from "react";
import {
  getDeliveryStatePresentation,
  type VerificationDeliveryState,
} from "@/lib/verification/delivery-status";

type PreparedDelivery = {
  url: string; linkId: string; deliveryId: string; trackingKey: string;
  expiresAt: string; deliveryState: "prepared"; from: string;
  subject: string; text: string; deliveryEnabled: boolean; policyReason: string;
};

export function VerificationLinkPanel({
  businessRef, initialRecipient, initialDeliveryState = "prepared",
}: {
  businessRef: string;
  initialRecipient: string;
  initialDeliveryState?: VerificationDeliveryState;
}) {
  const [expiry, setExpiry] = useState(5);
  const [recipient, setRecipient] = useState(initialRecipient);
  const [result, setResult] = useState<PreparedDelivery | null>(null);
  const [deliveryState, setDeliveryState] = useState(initialDeliveryState);
  const [confirmed, setConfirmed] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const delivery = getDeliveryStatePresentation(deliveryState);

  async function create() {
    setBusy(true); setError(""); setConfirmed(false);
    try {
      const response = await fetch(
        `/directoryadmin/api/businesses/${encodeURIComponent(businessRef)}/verification-link`,
        { method: "POST", headers: { "content-type": "application/json" },
          body: JSON.stringify({ expiresInDays: expiry, recipientAddress: recipient }) },
      );
      const body = await response.json();
      if (!response.ok) return setError(body.error || "Unable to create preview.");
      setResult(body); setDeliveryState("prepared");
    } finally { setBusy(false); }
  }

  async function send() {
    if (!result || !confirmed) return;
    setBusy(true); setError("");
    try {
      const rawToken = result.url.split("/").pop() ?? "";
      const response = await fetch(
        `/directoryadmin/api/businesses/${encodeURIComponent(businessRef)}/verification-email`,
        { method: "POST", headers: { "content-type": "application/json" },
          body: JSON.stringify({
            deliveryId: result.deliveryId, trackingKey: result.trackingKey,
            rawToken, confirmed: true,
          }) },
      );
      const body = await response.json();
      if (!response.ok) {
        setDeliveryState(body.error?.includes("Gmail API handoff failed") ? "failed" : "prepared");
        return setError(body.error || "Unable to send email.");
      }
      setDeliveryState("sent"); setConfirmed(false);
    } finally { setBusy(false); }
  }

  async function revoke() {
    if (!result) return;
    setBusy(true); setError("");
    try {
      const response = await fetch(
        `/directoryadmin/api/businesses/${encodeURIComponent(businessRef)}/verification-link?linkId=${encodeURIComponent(result.linkId)}`,
        { method: "DELETE" },
      );
      if (response.ok) setDeliveryState("revoked");
      else setError("Unable to revoke link.");
    } finally { setBusy(false); }
  }

  return <section className="mt-8 rounded-xl border border-slate-200 p-5">
    <h2 className="font-semibold">Verification email delivery</h2>
    <p className="mt-1 text-sm text-slate-600">
      Prepare a single-recipient preview, review it, then explicitly confirm sending.
    </p>
    <div role="status" aria-live="polite" className="mt-4 rounded-lg border-2 border-amber-300 bg-amber-50 p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-amber-800">Delivery status</p>
      <p className="mt-1 text-lg font-semibold text-slate-900">{delivery.label}</p>
      {delivery.explanation && <p className="mt-1 text-sm font-medium text-slate-700">{delivery.explanation}</p>}
    </div>
    <div className="mt-4 grid gap-3 sm:grid-cols-[1fr_auto_auto] sm:items-end">
      <label className="text-sm">Recipient email
        <input type="email" required value={recipient} onChange={(event) => setRecipient(event.target.value)}
          className="mt-1 block w-full rounded border px-3 py-2" />
      </label>
      <label className="text-sm">Expiry
        <select value={expiry} onChange={(event) => setExpiry(Number(event.target.value))}
          className="mt-1 block rounded border px-3 py-2">
          {[1,3,5,7,10,14].map((days) =>
            <option key={days} value={days}>{days} day{days === 1 ? "" : "s"}</option>)}
        </select>
      </label>
      <button type="button" disabled={busy || !recipient} onClick={create}
        className="rounded bg-brand-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-50">
        Prepare preview
      </button>
    </div>
    {error && <p role="alert" className="mt-3 text-sm text-red-700">{error}</p>}
    {result && <div className="mt-4 rounded border border-slate-200 bg-slate-50 p-4 text-sm">
      <p><strong>From:</strong> {result.from}</p>
      <p><strong>To:</strong> {recipient}</p>
      <p><strong>Subject:</strong> {result.subject}</p>
      <pre className="mt-3 whitespace-pre-wrap rounded bg-white p-3 font-sans text-sm">{result.text}</pre>
      <p className="mt-2 text-xs text-slate-600">Expires {new Date(result.expiresAt).toLocaleString()}</p>
      <p className={`mt-3 text-sm font-medium ${result.deliveryEnabled ? "text-green-700" : "text-amber-800"}`}>
        {result.deliveryEnabled ? "Gmail API sending is enabled for this recipient." : `Preview only: ${result.policyReason}`}
      </p>
      {deliveryState === "prepared" && <>
        <label className="mt-4 flex gap-2 text-sm">
          <input type="checkbox" checked={confirmed}
            onChange={(event) => setConfirmed(event.target.checked)} />
          <span>I reviewed the recipient, sender, subject, and message and explicitly confirm this single send.</span>
        </label>
        <div className="mt-3 flex gap-4">
          <button type="button" onClick={send}
            disabled={busy || !confirmed || !result.deliveryEnabled}
            className="rounded bg-green-700 px-4 py-2 font-medium text-white disabled:opacity-40">
            Send verification email
          </button>
          <button type="button" onClick={revoke} disabled={busy}
            className="font-medium text-red-700">Revoke</button>
        </div>
      </>}
    </div>}
  </section>;
}
