/**
 * app/directoryadmin/businesses/[businessRef]/actions.ts — business edit server action.
 *
 * VERSION HISTORY
 * v1.1.0 · 2026-08-06 · updateBusinessAction now requires canManageVerification(role)
 *   in addition to an authenticated session — matching the fix applied to
 *   moveStageAction (pipeline/actions.ts v1.1.0). Same gap `role` on the gap
 *   register, found by auditing every "use server" action file for the same
 *   session-only check. Notably this action also controls chatWidgetOptIn
 *   (the assistant activation flag, gap `assistant`) and generatedSiteUrl —
 *   both were previously editable by any authenticated session.
 * v1.0.0 · 2026-08-06 · Version history added; file predates this convention.
 */
"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { getCurrentUser } from "@/lib/auth/session";
import { canManageVerification } from "@/lib/verification/repository";
import { updateBusinessDetails, type BusinessEditableFields } from "@/lib/db/queries/businesses";

const TEXT_FIELDS = [
  "businessName", "tradingName", "category", "subCategory", "email", "phone", "mobile",
  "website", "facebook", "instagram", "linkedin", "address", "town", "county", "postcode", "description",
  "generatedSiteUrl",
] as const satisfies readonly (keyof BusinessEditableFields)[];

/**
 * Same auth shape as pipeline/actions.ts's moveStageAction -- Server Actions
 * bypass middleware.ts's cookie-presence check, so this is the real gate.
 */
export async function updateBusinessAction(formData: FormData): Promise<void> {
  const user = await getCurrentUser();
  if (!user || !canManageVerification(user.role)) redirect("/directoryadmin/login");

  const businessId = String(formData.get("businessId") ?? "");
  if (!businessId) return;

  const fields: Partial<BusinessEditableFields> = {};
  for (const key of TEXT_FIELDS) {
    const raw = formData.get(key);
    if (raw === null) continue;
    const value = String(raw).trim();
    if (key === "businessName" || key === "category") {
      if (value) fields[key] = value; // required fields -- never blank them out
    } else {
      (fields as Record<string, string | null>)[key] = value || null;
    }
  }
  // The form renders the checkbox before a hidden "off" fallback of the same
  // name, so FormData always has an entry -- .get() returns whichever came
  // first in DOM order, "on" if checked, "off" if not.
  if (formData.has("chatWidgetOptIn")) {
    fields.chatWidgetOptIn = formData.get("chatWidgetOptIn") === "on";
  }

  await updateBusinessDetails(businessId, fields, user.id);

  const businessRef = String(formData.get("businessRef") ?? "");
  revalidatePath(`/directoryadmin/businesses/${businessRef}`);
  revalidatePath("/directoryadmin/businesses");
}
