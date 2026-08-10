export type BrandEmailCta = { href: string; label: string; tone: "lime" | "black" };

export function escapeEmailHtml(value: string): string {
  return value.replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[character]!);
}

/** Shared black-and-lime The Tech Principle shell for service messages. */
export function renderTheTechPrincipleEmail(input: {
  eyebrow: string; heading: string; bodyHtml: string; ctas?: BrandEmailCta[]; footerDetail: string;
}): string {
  const ctas = (input.ctas ?? []).map((cta) => `<a href="${escapeEmailHtml(cta.href)}" style="background:${cta.tone === "lime" ? "#b6ff00" : "#080808"};color:${cta.tone === "lime" ? "#080808" : "#ffffff"}!important;text-decoration:none;padding:14px 20px;border-radius:3px;font-weight:700;margin:0 8px 10px 0;display:inline-block">${escapeEmailHtml(cta.label)}</a>`).join("");
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;background:#f1f1ed;font:15px Arial,sans-serif;color:#171717"><div style="max-width:620px;margin:auto;padding:32px 16px"><div style="background:#fff;border:1px solid #deded8"><div style="background:#080808;border-top:6px solid #b6ff00;padding:28px 32px;color:#fff"><div style="font:700 23px Georgia,serif">The Tech Principle</div><div style="margin-top:6px;color:#b6ff00;font-size:11px;letter-spacing:.12em;text-transform:uppercase">Local business directory</div></div><div style="padding:32px;line-height:1.6"><div style="color:#527300;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase">${escapeEmailHtml(input.eyebrow)}</div><h2 style="font-size:1.45rem;color:#080808;margin:10px 0 16px">${escapeEmailHtml(input.heading)}</h2>${input.bodyHtml}<div style="margin:24px 0 8px">${ctas}</div></div><div style="border-top:1px solid #deded8;padding:22px 32px 28px;color:#555;font-size:12px;line-height:1.5"><strong>The Tech Principle</strong><br>${input.footerDetail}</div></div></div></body></html>`;
}
