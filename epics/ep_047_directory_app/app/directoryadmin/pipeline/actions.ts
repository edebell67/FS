/**
 * app/directoryadmin/pipeline/actions.ts — pipeline board server actions.
 *
 * VERSION HISTORY
 * v1.1.0 · 2026-08-06 · moveStageAction now requires canManageVerification(role)
 *   in addition to an authenticated session. Previously any logged-in session
 *   could move any business through any non-protected pipeline stage — gap
 *   `role` on EP047_end_to_end_workflow_gap_register.html ("Generic stage
 *   action currently accepts any authenticated session"). Reuses the same role
 *   gate already applied to verification sending and owner-review delivery
 *   rather than a new authorization model.
 * v1.0.0 · 2026-08-06 · Version history added; file predates this convention.
 */
"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { moveBusinessToStage } from "@/lib/db/queries/pipeline";
import { getCurrentUser } from "@/lib/auth/session";
import { canManageVerification } from "@/lib/verification/repository";

export async function moveStageAction(formData: FormData): Promise<void> {
  // Server Actions aren't covered by middleware.ts's Edge cookie-presence
  // check in a meaningful way — a request with a stale/invalid cookie would
  // pass that check and reach here. This is the real check.
  const user = await getCurrentUser();
  // An authenticated session is not operations authority. Any logged-in user
  // could otherwise move any business through any (non-protected) stage —
  // this reuses the same role gate already applied to verification sending
  // and owner-review delivery (lib/verification/repository.ts) rather than
  // inventing a separate authorization model for the pipeline board.
  if (!user || !canManageVerification(user.role)) redirect("/directoryadmin/login");

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
