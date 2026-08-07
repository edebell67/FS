"use server";

/**
 * app/directoryadmin/site-previews/actions.ts — Authorized preview and owner-review email dispatch actions.
 *
 * VERSION HISTORY
 * v1.1.0 · 2026-08-05 · Adds an explicit, separately audited owner-review invitation reissue action without changing business state.
 * v1.0.0 · 2026-08-05 · Version history added; file predates this convention.
 */
import { redirect } from "next/navigation";
import { getCurrentUser } from "@/lib/auth/session";
import { canManageVerification } from "@/lib/verification/repository";
import { getBusinessesReadyForOwnerReviewInvitation, getBusinessesReadyForPreviewNotification } from "@/lib/verification/site-generation";
import { createOwnerReviewLink } from "@/lib/owner-review/repository";
import { preparePreviewMessage, previewReadyMessage, sendPreparedPreviewMessage } from "@/lib/verification/preview-delivery";
import { moveBusinessToStage } from "@/lib/db/queries/pipeline";

const reviewOrigin = () => (process.env.PUBLIC_APP_ORIGIN ?? "https://thetechprinciple.com").replace(/\/$/, "");

export async function sendSelectedPreviewLinksAction(formData: FormData) {
  const user = await getCurrentUser();
  if (!user || !canManageVerification(user.role)) redirect("/directoryadmin/login");
  const selected = new Set(formData.getAll("businessId").map(String));
  if (!selected.size) redirect("/directoryadmin/site-previews?error=selection");
  if (formData.get("confirmed") !== "on") redirect("/directoryadmin/site-previews?error=confirm");
  const eligible = (await getBusinessesReadyForPreviewNotification()).filter((business) => selected.has(business.id));
  let sent = 0; let skipped = 0;
  for (const business of eligible) {
    if (!business.email || !business.generatedSiteUrl) { skipped++; continue; }
    const issued = await createOwnerReviewLink({ businessId: business.id, actorUserId: user.id });
    const reviewUrl = `${reviewOrigin()}/review/${issued.token}`;
    const message = previewReadyMessage(business.businessName, business.generatedSiteUrl, reviewUrl);
    const id = await preparePreviewMessage({ businessId: business.id, messageType: "preview_ready", recipientAddress: business.email, subject: message.subject, textBody: message.text, actorUserId: user.id });
    const result = await sendPreparedPreviewMessage(id);
    if (result.sent) {
      sent++;
      await moveBusinessToStage(business.id, "site_in_review", "admin", `Preview-ready email sent to ${business.email}`, user.id, true);
    } else skipped++;
  }
  redirect(`/directoryadmin/site-previews?sent=${sent}&skipped=${skipped}`);
}

/** Sends a new one-time owner-review link only after an authorized admin explicitly confirms the selected recipient. */
export async function sendOwnerReviewInvitationAction(formData: FormData) {
  const user = await getCurrentUser();
  if (!user || !canManageVerification(user.role)) redirect("/directoryadmin/login");
  const selected = new Set(formData.getAll("businessId").map(String));
  if (!selected.size) redirect("/directoryadmin/site-previews?reviewError=selection");
  if (formData.get("confirmed") !== "on") redirect("/directoryadmin/site-previews?reviewError=confirm");
  const eligible = (await getBusinessesReadyForOwnerReviewInvitation()).filter((business) => selected.has(business.id));
  let sent = 0; let skipped = 0;
  for (const business of eligible) {
    if (!business.email || !business.generatedSiteUrl) { skipped++; continue; }
    const issued = await createOwnerReviewLink({ businessId: business.id, actorUserId: user.id });
    const reviewUrl = `${reviewOrigin()}/review/${issued.token}`;
    const message = previewReadyMessage(business.businessName, business.generatedSiteUrl, reviewUrl);
    const id = await preparePreviewMessage({ businessId: business.id, messageType: "owner_review_invitation", recipientAddress: business.email, subject: message.subject, textBody: message.text, actorUserId: user.id });
    const result = await sendPreparedPreviewMessage(id);
    if (result.sent) {
      sent++;
      await moveBusinessToStage(business.id, "site_in_review", "admin", `Owner-review invitation sent to ${business.email}`, user.id, true);
    } else skipped++;
  }
  redirect(`/directoryadmin/site-previews?reviewSent=${sent}&reviewSkipped=${skipped}`);
}
