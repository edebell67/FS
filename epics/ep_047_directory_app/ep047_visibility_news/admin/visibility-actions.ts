"use server";
// EP047-2026.08.01.2 — protected News display settings action.
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { db } from "@/lib/db/client";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { sql } from "drizzle-orm";
import { describeScopeChange } from "@/ep047_visibility_news/lib/scope-diff";

/**
 * Two-phase publish: the scope form always posts here first. Without `confirmed=1` this
 * only redirects to a preview of the named consequence — it never writes. The confirm
 * button on that preview resubmits the same values with `confirmed=1`, and the diff used
 * for the audit reason is recomputed server-side here (never trusted from the client) so
 * the recorded consequence always matches what actually changed.
 */
export async function saveScope(formData: FormData) {
  await requireAdminUserForPage("/directoryadmin/visibility");
  const townMode = formData.get("townMode") === "selected" ? "selected" : "all";
  const categoryMode = formData.get("categoryMode") === "selected" ? "selected" : "all";
  const confirmed = formData.get("confirmed") === "1";

  if (!confirmed) {
    redirect(`/directoryadmin/visibility?previewTownMode=${townMode}&previewCategoryMode=${categoryMode}`);
  }

  const current = await db.execute(sql`SELECT town_mode, category_mode FROM public_directory_settings WHERE id='default'`);
  const currentRow = (current as any).rows?.[0] ?? { town_mode: "all", category_mode: "all" };
  const disabledTowns = await db.execute(sql`SELECT initcap(trim(town_label)) AS label FROM public_town_visibility WHERE is_enabled = false ORDER BY label`);
  const disabledCategories = await db.execute(sql`SELECT initcap(trim(category_label)) AS label FROM public_category_visibility WHERE is_enabled = false ORDER BY label`);
  const reason = describeScopeChange({
    currentTownMode: currentRow.town_mode,
    currentCategoryMode: currentRow.category_mode,
    proposedTownMode: townMode,
    proposedCategoryMode: categoryMode,
    disabledTownLabels: ((disabledTowns as any).rows ?? []).map((r: any) => r.label),
    disabledCategoryLabels: ((disabledCategories as any).rows ?? []).map((r: any) => r.label),
  }).join(" | ");

  await db.execute(sql`INSERT INTO public_directory_settings (id, town_mode, category_mode)
    VALUES ('default', ${townMode}, ${categoryMode})
    ON CONFLICT (id) DO UPDATE SET town_mode=${townMode}, category_mode=${categoryMode}, updated_at=now()`);
  await db.execute(sql`INSERT INTO public_visibility_audit (entity_type, entity_key, action, reason)
    VALUES ('scope', 'default', 'apply', ${reason})`);
  revalidatePath("/directory", "layout");
  revalidatePath("/directoryadmin/visibility");
  redirect("/directoryadmin/visibility?scopeApplied=1");
}

export async function saveVisibility(formData: FormData) {
  await requireAdminUserForPage("/directoryadmin/visibility");
  const kind = String(formData.get("kind"));
  const key = String(formData.get("key")).trim().toLowerCase();
  const label = String(formData.get("label"));
  const enabled = formData.get("enabled") === "on";
  if (kind === "town") {
    await db.execute(sql`INSERT INTO public_town_visibility (town_key, town_label, is_enabled)
      VALUES (${key}, ${label}, ${enabled}) ON CONFLICT (town_key) DO UPDATE SET is_enabled=${enabled}, updated_at=now()`);
  } else {
    await db.execute(sql`INSERT INTO public_category_visibility (category_key, category_label, is_enabled)
      VALUES (${key}, ${label}, ${enabled}) ON CONFLICT (category_key) DO UPDATE SET is_enabled=${enabled}, updated_at=now()`);
  }
  await db.execute(sql`INSERT INTO public_visibility_audit (entity_type, entity_key, action, reason)
    VALUES (${kind}, ${key}, 'toggle', ${enabled ? "Enabled by admin" : "Hidden by admin"})`);
  revalidatePath("/directory", "layout");
}

const OVERRIDE_DECISIONS = new Set(["inherit", "show", "hide"]);

export async function saveBusinessOverride(formData: FormData) {
  await requireAdminUserForPage("/directoryadmin/visibility");
  const businessId = String(formData.get("businessId") ?? "").trim();
  const decision = String(formData.get("decision") ?? "").trim();
  const reason = String(formData.get("reason") ?? "").trim();
  const returnQuery = String(formData.get("returnQuery") ?? "").trim();
  if (!businessId) throw new Error("A business must be selected.");
  if (!OVERRIDE_DECISIONS.has(decision)) throw new Error("Decision must be inherit, show, or hide.");
  if (!reason) throw new Error("A reason is required to record or clear an override.");
  await db.execute(sql`INSERT INTO public_business_visibility (business_id, decision, reason)
    VALUES (${businessId}, ${decision}, ${reason})
    ON CONFLICT (business_id) DO UPDATE SET decision=${decision}, reason=${reason}, updated_at=now()`);
  await db.execute(sql`INSERT INTO public_visibility_audit (entity_type, entity_key, action, reason)
    VALUES ('business', ${businessId}, ${"override_" + decision}, ${reason})`);
  revalidatePath("/directoryadmin/visibility");
  revalidatePath("/directory", "layout");
  redirect(`/directoryadmin/visibility${returnQuery ? `?q=${encodeURIComponent(returnQuery)}` : ""}`);
}

export async function saveNewsDisplaySettings(formData: FormData) {
  await requireAdminUserForPage("/directoryadmin/visibility");
  const maxArticles = Math.max(1, Math.min(100, Number(formData.get("maxArticlesPerTown")) || 10));
  const lookbackDays = Math.max(1, Math.min(3650, Number(formData.get("lookbackDays")) || 30));
  await db.execute(sql`INSERT INTO public_news_display_settings (id, max_articles_per_town, lookback_days, updated_at)
    VALUES (true, ${maxArticles}, ${lookbackDays}, now())
    ON CONFLICT (id) DO UPDATE SET max_articles_per_town=${maxArticles}, lookback_days=${lookbackDays}, updated_at=now()`);
  await db.execute(sql`INSERT INTO public_visibility_audit (entity_type, entity_key, action, reason)
    VALUES ('news_display_settings', 'default', 'apply', ${`max_articles_per_town=${maxArticles}; lookback_days=${lookbackDays}`})`);
  revalidatePath("/news", "page");
  revalidatePath("/api/public-news");
}
