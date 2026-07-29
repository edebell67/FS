"use server";
import { revalidatePath } from "next/cache";
import { db } from "@/lib/db/client";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { sql } from "drizzle-orm";

export async function saveScope(formData: FormData) {
  await requireAdminUserForPage("/directoryadmin/visibility");
  const townMode = formData.get("townMode") === "selected" ? "selected" : "all";
  const categoryMode = formData.get("categoryMode") === "selected" ? "selected" : "all";
  await db.execute(sql`INSERT INTO public_directory_settings (id, town_mode, category_mode)
    VALUES ('default', ${townMode}, ${categoryMode})
    ON CONFLICT (id) DO UPDATE SET town_mode=${townMode}, category_mode=${categoryMode}, updated_at=now()`);
  revalidatePath("/directory", "layout");
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
