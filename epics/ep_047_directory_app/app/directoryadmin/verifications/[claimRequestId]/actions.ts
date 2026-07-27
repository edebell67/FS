"use server";
import { redirect } from "next/navigation";
import { getCurrentUser } from "@/lib/auth/session";
import { approveClaim, canManageVerification, reopenApprovedClaimForTest } from "@/lib/verification/repository";
export async function approveClaimAction(claimRequestId: string, formData: FormData) {
  const user = await getCurrentUser();
  if (!user || !canManageVerification(user.role)) return;
  await approveClaim(claimRequestId, user.id, String(formData.get("note") ?? ""));
  redirect("/directoryadmin/pipeline");
}
export async function reopenClaimForTestAction(claimRequestId: string) {
  const user = await getCurrentUser();
  if (!user || !canManageVerification(user.role)) return;
  const ok = await reopenApprovedClaimForTest(claimRequestId, user.id);
  if (!ok) throw new Error("Only an approved claim can be reopened.");
  redirect(`/directoryadmin/verifications/${claimRequestId}`);
}
