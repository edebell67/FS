"use server";
/**
 * app/review/[token]/actions.ts — Parses a scoped owner-review form without external delivery.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-08-05 · Adds one-click durable owner review submission action.
 */
import { redirect } from "next/navigation";
import { submitOwnerReview } from "@/lib/owner-review/repository";
export async function submitOwnerReviewAction(token: string, formData: FormData) {
  const decision = String(formData.get("decision") ?? "") as "accept" | "change" | "decline";
  let pages: unknown = [];
  try { pages = JSON.parse(String(formData.get("pages") ?? "[]")); } catch { redirect(`/review/${encodeURIComponent(token)}?error=invalid`); }
  const result = await submitOwnerReview(token, { decision, pages: Array.isArray(pages) ? pages as never[] : [] });
  if (!result) redirect(`/review/${encodeURIComponent(token)}?error=invalid`);
  redirect(`/review/${encodeURIComponent(token)}/complete`);
}
