"use server";
import { redirect } from "next/navigation";
import { getCurrentUser } from "@/lib/auth/session";
import { canManageVerification } from "@/lib/verification/repository";
import { approveSelectedClaims } from "@/lib/verification/claims-approval";
import { sendPreparedClaimSuccessMessages, sendAllPreparedClaimSuccessMessages } from "@/lib/verification/claim-success-delivery";

export async function approveSelectedClaimsAction(formData: FormData) {
  const user = await getCurrentUser();
  if (!user || !canManageVerification(user.role)) return;
  const claimIds = formData.getAll("claimId").map(String);
  if (!claimIds.length) redirect("/directoryadmin/claims?error=select");
  if (formData.get("confirmed") !== "on") redirect("/directoryadmin/claims?error=confirm");
  const result = await approveSelectedClaims({ claimIds, actorUserId: user.id, note: String(formData.get("note") ?? "") });
  await sendPreparedClaimSuccessMessages(result.messageIds);
  redirect("/directoryadmin/claims?approved=1");
}

export async function sendPreparedClaimSuccessMessagesAction() {
  const user = await getCurrentUser();
  if (!user || !canManageVerification(user.role)) return;
  await sendAllPreparedClaimSuccessMessages();
  redirect("/directoryadmin/claims?messages=sent");
}
