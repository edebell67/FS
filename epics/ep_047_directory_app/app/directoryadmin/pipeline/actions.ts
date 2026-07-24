"use server";

import { revalidatePath } from "next/cache";
import { moveBusinessToStage } from "@/lib/db/queries/pipeline";
import { getCurrentUser } from "@/lib/auth/session";

export async function moveStageAction(formData: FormData): Promise<void> {
  // Server Actions aren't covered by middleware.ts's Edge cookie-presence
  // check in a meaningful way — a request with a stale/invalid cookie would
  // pass that check and reach here. This is the real check.
  const user = await getCurrentUser();
  if (!user) return;

  const businessId = String(formData.get("businessId") ?? "");
  const toStageKey = String(formData.get("toStageKey") ?? "");
  if (!businessId || !toStageKey) return;

  await moveBusinessToStage(
    businessId,
    toStageKey,
    "admin",
    "Moved manually from the pipeline board",
    user.id
  );
  revalidatePath("/directoryadmin/pipeline");
  revalidatePath("/directoryadmin/businesses");
}
