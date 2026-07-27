"use server";
import { redirect } from "next/navigation";
import { getCurrentUser } from "@/lib/auth/session";
import { canManageVerification } from "@/lib/verification/repository";
import { approveSelectedClaims } from "@/lib/verification/claims-approval";
import { sendPreparedClaimSuccessMessages } from "@/lib/verification/claim-success-delivery";

export async function approveSelectedClaimsAction(formData: FormData) {
  const user = await getCurrentUser();
  if (!user || !canManageVerification(user.role)) return;
  const claimIds = formData.getAll("claimId").map(String);
  if (formData.get("confirmed") !== "on") throw new Error("Confirm the selected-claim approval before continuing.");
  const result = await approveSelectedClaims({ claimIds, actorUserId: user.id, note: String(formData.get("note") ?? "") });
  await sendPreparedClaimSuccessMessages(result.messageIds);
  redirect("/directoryadmin/claims?approved=1");
}
