"use server";
import { redirect } from "next/navigation";
import { createPublicClaimIntake } from "@/lib/verification/claim-intake";
export async function publicClaimAction(formData: FormData) {
  await createPublicClaimIntake({
    businessRef: String(formData.get("businessRef") ?? ""),
    requesterName: String(formData.get("requesterName") ?? ""),
    relationship: String(formData.get("relationship") ?? ""),
    email: String(formData.get("email") ?? ""), phone: String(formData.get("phone") ?? ""),
    acknowledged: formData.get("acknowledged") === "on", website: String(formData.get("website") ?? ""),
  });
  redirect("/claim/complete");
}
