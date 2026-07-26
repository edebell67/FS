"use server";
import { redirect } from "next/navigation";
import { getCurrentUser } from "@/lib/auth/session";
import { approveClaim, canManageVerification } from "@/lib/verification/repository";
export async function approveClaimAction(claimRequestId: string, formData: FormData) {
  const user = await getCurrentUser();
  if (!user || !canManageVerification(user.role)) return;
  await approveClaim(claimRequestId, user.id, String(formData.get("note") ?? ""));
  redirect("/directoryadmin/pipeline");
}
