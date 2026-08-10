export type BrandEmailCta = {
  href: string;
  label: string;
};

export function escapeEmailHtml(value: string): string {
  return value.replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[character]!);
}

/** The shared visual shell for The Tech Principle outbound service messages. */
export function renderTheTechPrincipleEmail(input: {
  eyebrow: string;
  heading: string;
  bodyHtml: string;
  cta?: BrandEmailCta;
  footerDetail: string;
}): string {
  const cta = input.cta
    ? `<div class="cta-row"><a class="cta" href="${escapeEmailHtml(input.cta.href)}" style="background:#00765e;color:white!important;text-decoration:none;padding:13px 19px;border-radius:3px;font-weight:bold;margin:10px 0 18px;display:inline-block">${escapeEmailHtml(input.cta.label)}</a></div>`
    : "";

  return `<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{margin:0;background:#e7ecea;font:15px Arial,sans-serif;color:#152022}.wrap{max-width:620px;margin:auto;padding:38px 18px}.inbox{background:#fff;box-shadow:0 6px 26px #17332a22}.top{background:#152b2a;padding:30px;color:white}.brand{font:700 22px Georgia,serif}.tag{margin-top:5px;color:#b8d9ce;font-size:11px;letter-spacing:.12em;text-transform:uppercase}.body{padding:34px 34px 20px;line-height:1.6}.eyebrow{color:#00765e;font-size:11px;font-weight:bold;letter-spacing:.12em;text-transform:uppercase}.cta-row{margin:10px 0 18px}.foot{border-top:1px solid #dce3df;padding:22px 34px 30px;color:#63716b;font-size:12px;line-height:1.5}</style></head>
<body><div class="wrap"><div class="inbox"><div class="top"><div class="brand">The Tech Principle</div><div class="tag">Local business directory &amp; website support</div></div>
<div class="body"><div class="eyebrow">${escapeEmailHtml(input.eyebrow)}</div><h2 style="font-size:1.4rem;color:#152022;margin:10px 0 16px">${escapeEmailHtml(input.heading)}</h2>${input.bodyHtml}${cta}</div>
<div class="foot"><strong>The Tech Principle</strong><br>${input.footerDetail}</div></div></div></body></html>`;
}
