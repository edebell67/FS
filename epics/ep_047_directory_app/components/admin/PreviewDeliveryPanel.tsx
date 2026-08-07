"use client";

type PreviewMessage = {
  id: string;
  messageType: string;
  status: string;
  recipientAddress: string | null;
  subject: string | null;
  textBody: string | null;
  sentAt: Date | string | null;
  failureReason: string | null;
  createdAt: Date | string;
};

type StatusEntry = { label: string; border: string; bg: string; explanation: string };

const statusStyle: Record<string, StatusEntry> = {
  prepared: { label: "Prepared (not yet sent)",  border: "border-amber-300", bg: "bg-amber-50",   explanation: "The message has been composed and recorded; delivery has not been attempted or enabled." },
  sent:     { label: "Sent ✓",                   border: "border-green-300", bg: "bg-green-50",    explanation: "Successfully handed off to Gmail API." },
  failed:   { label: "Delivery failed ✗",        border: "border-red-300",   bg: "bg-red-50",       explanation: "Gmail API returned a non-retryable error." },
};

const defaultStyle: StatusEntry = { label: "Unknown", border: "border-slate-300", bg: "bg-slate-50", explanation: "" };

function fmt(d: Date | string): string {
  const dt = typeof d === "string" ? new Date(d) : d;
  return isNaN(dt.getTime()) ? "—" : dt.toLocaleString("en-GB", { day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" });
}

export function PreviewDeliveryPanel({ delivery }: { delivery: PreviewMessage | null }) {
  const st = delivery ? (statusStyle[delivery.status] ?? defaultStyle) : null;

  return <section className="mt-8 rounded-xl border border-slate-200 p-5">
    <h2 className="font-semibold">Ready for Review — email delivery</h2>
    <p className="mt-1 text-sm text-slate-600">
      Preview-ready email status for this business. Send owner-review invitations from the{" "}
      <a href="/directoryadmin/site-previews" className="text-brand-700 underline">Site Previews</a> page.
    </p>

    {delivery ? <>
      <div role="status" aria-live="polite" className={`mt-4 rounded-lg border-2 p-4 ${st!.border} ${st!.bg}`}>
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-800">Delivery status</p>
        <p className="mt-1 text-lg font-semibold text-slate-900">{st!.label}</p>
        {st!.explanation && <p className="mt-1 text-sm font-medium text-slate-700">{st!.explanation}</p>}
        {delivery.failureReason && <p className="mt-1 text-sm text-red-700">Reason: {delivery.failureReason}</p>}
      </div>

      <details className="mt-4">
        <summary className="cursor-pointer text-sm font-medium text-brand-700">View email content</summary>
        <div className="mt-3 space-y-2 rounded border border-slate-200 bg-slate-50 p-4 text-sm">
          <p><strong>Type:</strong> {delivery.messageType}</p>
          <p><strong>To:</strong> {delivery.recipientAddress ?? "—"}</p>
          <p><strong>Subject:</strong> {delivery.subject ?? "—"}</p>
          {delivery.sentAt && <p><strong>Sent:</strong> {fmt(delivery.sentAt)}</p>}
          <p><strong>Prepared:</strong> {fmt(delivery.createdAt)}</p>
          {delivery.textBody && <pre className="mt-3 whitespace-pre-wrap rounded bg-white p-3 font-sans text-sm">{delivery.textBody}</pre>}
        </div>
      </details>
    </> : <>
      <div role="status" aria-live="polite" className="mt-4 rounded-lg border-2 border-slate-300 bg-slate-50 p-4">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-800">Delivery status</p>
        <p className="mt-1 text-lg font-semibold text-slate-900">No preview email recorded</p>
        <p className="mt-1 text-sm text-slate-600">No preview-ready email has been prepared or sent for this business yet.</p>
      </div>
    </>}

    <p className="mt-4 text-sm">
      <a href="/directoryadmin/site-previews" className="font-medium text-brand-700 hover:underline">
        Send owner-review invitation from Site Previews →
      </a>
    </p>
  </section>;
}