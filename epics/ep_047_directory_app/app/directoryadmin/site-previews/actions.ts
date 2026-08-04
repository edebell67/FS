"use server";

import { redirect } from "next/navigation";
import { getCurrentUser } from "@/lib/auth/session";
import { canManageVerification } from "@/lib/verification/repository";
import { getBusinessesReadyForPreviewNotification } from "@/lib/verification/site-generation";
import { preparePreviewMessage, previewReadyMessage, sendPreparedPreviewMessage } from "@/lib/verification/preview-delivery";

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
    const message = previewReadyMessage(business.businessName, business.generatedSiteUrl);
    const id = await preparePreviewMessage({ businessId: business.id, messageType: "preview_ready", recipientAddress: business.email, subject: message.subject, textBody: message.text, actorUserId: user.id });
    const result = await sendPreparedPreviewMessage(id);
    if (result.sent) sent++; else skipped++;
  }
  redirect(`/directoryadmin/site-previews?sent=${sent}&skipped=${skipped}`);
}
