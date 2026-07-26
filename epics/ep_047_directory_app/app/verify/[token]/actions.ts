"use server";

import { redirect } from "next/navigation";
import { EDITABLE_FIELDS, type SubmittedFields, type VerificationInput } from "@/lib/verification/types";
import { submitVerification } from "@/lib/verification/repository";

export async function submitVerificationAction(token: string, formData: FormData) {
  const fields = Object.fromEntries(
    EDITABLE_FIELDS.map((field) => [field, String(formData.get(field) ?? "").trim()])
  ) as SubmittedFields;
  const input: VerificationInput = {
    fields,
    requesterName: String(formData.get("requesterName") ?? ""),
    relationship: String(formData.get("relationship") ?? "") as VerificationInput["relationship"],
    accuracyConfirmed: formData.get("accuracyConfirmed") === "on",
    contactEmail: String(formData.get("contactEmail") ?? "").trim() || undefined,
    contactPhone: String(formData.get("contactPhone") ?? "").trim() || undefined,
  };
  const result = await submitVerification(token, input);
  if (!result) redirect(`/verify/${encodeURIComponent(token)}?error=invalid`);
  redirect(`/verify/${encodeURIComponent(token)}/complete`);
}
