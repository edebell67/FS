"use server";

import { revalidatePath } from "next/cache";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { canManageValidation, processBusinessValidationJobChunk, startBusinessValidationJob } from "@/lib/validation/repository";
import { canManageVerification } from "@/lib/verification/repository";
import { getEligibleVerificationBusinesses, prepareVerificationBatch } from "@/lib/verification/batches";
import { approveSelectedClaims, listPendingClaims } from "@/lib/verification/claims-approval";
import { sendPreparedClaimSuccessMessages } from "@/lib/verification/claim-success-delivery";
import { getBusinessesReadyForPreviewNotification } from "@/lib/verification/site-generation";
import { preparePreviewMessage, previewReadyMessage, sendPreparedPreviewMessage } from "@/lib/verification/preview-delivery";
import { isGenerationConfigured } from "@/lib/generation/config";
import { runGenerationLoop } from "@/lib/generation/run-generation";

export type WorkflowOperation = "validate" | "prepare-verification" | "approve-claims" | "generate" | "send-previews";
export type WorkflowResult = { ok: true; message: string } | { ok: false; message: string };

/** The hosted generation loop needs a real, authenticated completion seam; otherwise it is not a workflow control. */
export async function generationPathAvailable() {
  return isGenerationConfigured() && Boolean(process.env.INTERNAL_API_KEY?.trim()) && Boolean(process.env.PUBLIC_APP_ORIGIN?.trim());
}

async function authorizedWorkflowUser() {
  const user = await requireAdminUserForPage("/directoryadmin/pipeline");
  if (!canManageValidation(user.role) || !canManageVerification(user.role)) throw new Error("Forbidden.");
  return user;
}

function refreshWorkflowViews() {
  revalidatePath("/directoryadmin/pipeline");
  revalidatePath("/directoryadmin/validation");
  revalidatePath("/directoryadmin/verification-batches");
  revalidatePath("/directoryadmin/claims");
  revalidatePath("/directoryadmin/site-previews");
}

/**
 * Each operation re-queries its eligible records immediately before calling the existing protected domain service.
 * No generic stage movement is used for verification or claims.
 */
export async function runWorkflowOperation(operation: WorkflowOperation, confirmed: boolean): Promise<WorkflowResult> {
  if (!confirmed) return { ok: false, message: "Confirmation is required before running a workflow operation." };
  const user = await authorizedWorkflowUser();

  if (operation === "validate") {
    const job = await startBusinessValidationJob(user.id);
    let current = job;
    while ((current.status === "pending" || current.status === "running") && !current.busy) {
      current = await processBusinessValidationJobChunk(current.id, user.id);
    }
    refreshWorkflowViews();
    return { ok: true, message: `Validation processed ${current.processedCount.toLocaleString()} of ${current.totalCount.toLocaleString()} eligible businesses; ${current.errorCount.toLocaleString()} errors.` };
  }

  if (operation === "prepare-verification") {
    // Deliberately excludes partial validation: a bulk workflow operation cannot silently opt into the separate partial policy.
    const eligible = (await getEligibleVerificationBusinesses()).filter((business) => business.validationStatus === "validated");
    if (!eligible.length) return { ok: true, message: "No validated active businesses are eligible for a verification batch." };
    const batch = await prepareVerificationBatch(eligible.map((business) => business.id), user.id, 5, false);
    refreshWorkflowViews();
    return { ok: true, message: `Prepared verification batch ${batch.batchId} for ${batch.totalCount.toLocaleString()} eligible businesses; ${batch.readyCount.toLocaleString()} have an email route. Sending remains a separate capability-confirmed operation.` };
  }

  if (operation === "approve-claims") {
    const claims = await listPendingClaims();
    if (!claims.length) return { ok: true, message: "No pending claims are eligible for approval." };
    const result = await approveSelectedClaims({ claimIds: claims.map((claim) => claim.id), actorUserId: user.id, note: "Approved from workflow control." });
    await sendPreparedClaimSuccessMessages(result.messageIds);
    refreshWorkflowViews();
    return { ok: true, message: `Approved ${result.approved.toLocaleString()} eligible claims; ${result.skipped.toLocaleString()} stale selections skipped; ${result.messagesPrepared.toLocaleString()} owner messages prepared.` };
  }

  if (operation === "generate") {
    if (!await generationPathAvailable()) return { ok: false, message: "Generation is not configured with a real authenticated generation and completion path." };
    const results = await runGenerationLoop();
    const generated = results.filter((result) => "siteUrl" in result).length;
    const skipped = results.length - generated;
    refreshWorkflowViews();
    return { ok: true, message: `Generation completed for ${generated.toLocaleString()} eligible queued businesses; ${skipped.toLocaleString()} skipped.` };
  }

  const eligible = await getBusinessesReadyForPreviewNotification();
  let sent = 0;
  let skipped = 0;
  for (const business of eligible) {
    if (!business.email || !business.generatedSiteUrl) { skipped++; continue; }
    const message = previewReadyMessage(business.businessName, business.generatedSiteUrl);
    const messageId = await preparePreviewMessage({ businessId: business.id, messageType: "preview_ready", recipientAddress: business.email, subject: message.subject, textBody: message.text, actorUserId: user.id });
    const outcome = await sendPreparedPreviewMessage(messageId);
    if (outcome.sent) sent++; else skipped++;
  }
  refreshWorkflowViews();
  return { ok: true, message: `Preview delivery considered ${eligible.length.toLocaleString()} eligible businesses: ${sent.toLocaleString()} sent, ${skipped.toLocaleString()} skipped or blocked by delivery policy.` };
}
