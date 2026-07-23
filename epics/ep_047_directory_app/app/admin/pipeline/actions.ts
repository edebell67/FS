"use server";

import { revalidatePath } from "next/cache";
import { moveBusinessToStage } from "@/lib/db/queries/pipeline";

export async function moveStageAction(formData: FormData): Promise<void> {
  const businessId = String(formData.get("businessId") ?? "");
  const toStageKey = String(formData.get("toStageKey") ?? "");
  if (!businessId || !toStageKey) return;

  await moveBusinessToStage(businessId, toStageKey, "admin", "Moved manually from the pipeline board");
  revalidatePath("/admin/pipeline");
  revalidatePath("/admin/businesses");
}
