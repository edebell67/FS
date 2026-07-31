"use server";

import { revalidatePath } from "next/cache";
import { getCurrentUser } from "@/lib/auth/session";
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
  if (!user) return;

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
