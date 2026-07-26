"use server";

import { revalidatePath } from "next/cache";
import { requireAdminUserForPage } from "@/lib/auth/require";
import {
  applyFieldRepair, canManageValidation, processBusinessValidationJobChunk,
  replaceValidationRule, runBusinessValidation, setPartialVerificationPolicy,
  startBusinessValidationJob,
} from "@/lib/validation/repository";

async function authorizedUser() {
  const user = await requireAdminUserForPage("/directoryadmin/validation");
  if (!canManageValidation(user.role)) throw new Error("Forbidden.");
  return user;
}

export async function saveValidationRuleAction(formData: FormData) {
  const user = await authorizedUser();
  const optionalNumber = (name: string) => {
    const raw = String(formData.get(name) ?? "").trim();
    return raw === "" ? undefined : Number(raw);
  };
  await replaceValidationRule({
    fieldName: String(formData.get("fieldName") ?? ""),
    label: String(formData.get("label") ?? ""),
    ruleType: String(formData.get("ruleType") ?? ""),
    mandatory: formData.get("mandatory") === "on",
    blocksVerification: formData.get("blocksVerification") === "on",
    pattern: String(formData.get("pattern") ?? "").trim() || undefined,
    min: optionalNumber("min"), max: optionalNumber("max"),
  }, user.id);
  revalidatePath("/directoryadmin/validation");
}

export async function startValidationJobAction() {
  const user = await authorizedUser();
  const job = await startBusinessValidationJob(user.id);
  revalidatePath("/directoryadmin/validation");
  return job;
}

export async function processValidationJobChunkAction(jobId: string) {
  const user = await authorizedUser();
  const job = await processBusinessValidationJobChunk(jobId, user.id);
  revalidatePath("/directoryadmin/validation");
  revalidatePath("/directoryadmin/verification-batches");
  return job;
}

export async function runBusinessValidationAction(formData: FormData) {
  const user = await authorizedUser();
  await runBusinessValidation(String(formData.get("businessId") ?? ""), "admin", user.id);
  revalidatePath("/directoryadmin/validation");
  revalidatePath("/directoryadmin/verification-batches");
}

export async function setPartialPolicyAction(formData: FormData) {
  const user = await authorizedUser();
  await setPartialVerificationPolicy(formData.get("allowPartial") === "on", user.id);
  revalidatePath("/directoryadmin/validation");
  revalidatePath("/directoryadmin/verification-batches");
}

export async function applyFieldRepairAction(formData: FormData) {
  const user = await authorizedUser();
  await applyFieldRepair({
    businessId: String(formData.get("businessId") ?? ""),
    outcomeId: String(formData.get("outcomeId") ?? ""),
    fieldName: String(formData.get("fieldName") ?? ""),
    proposedValue: String(formData.get("proposedValue") ?? "").trim(),
    evidence: String(formData.get("evidence") ?? "").trim(),
  }, user.id);
  revalidatePath("/directoryadmin/validation");
  revalidatePath("/directoryadmin/verification-batches");
}
