/*
 * First-party, PII-free visitor analytics for EP044 demo sites.
 * Self-contained: drop one <script src=".../analytics-embed.js" data-client="KEY"> tag.
 *
 * Anonymous by design: counts unique VISITS (an ephemeral, tab-scoped session
 * that expires after 30 min and is gone when the browser closes) and their
 * timing — with NO persistent visitor identifier, so a person is never tracked
 * across visits or days. The session id is shared with the AI assistant widget
 * (same "aiw-session" key) only so behaviour and chat join within one visit.
 *
 * - Auto-captures pageview, scroll depth, dwell, CTA/phone/email/WhatsApp/
 *   outbound clicks, form start/submit, and gallery opens.
 * - Sends batches with navigator.sendBeacon (text/plain, so no CORS preflight),
 *   flushing on an interval and on page hide.
 * - No PII and no cross-visit identity: only event type, page PATH (never query
 *   string), referrer HOST, device class, scroll %, and dwell ms leave the page.
 * - Honours Do Not Track and a per-visit opt-out; exposes window.aiwTrack()
 *   and window.aiwAnalytics.optOut()/optIn(). The site owner can also switch
 *   logging off per site (server-enforced via the client's analyticsEnabled).
 */
(() => {
  const script = document.currentScript;
  const clientKey = script?.dataset.client;
  const apiBase = (script?.dataset.apiBase || new URL(script.src).origin).replace(/\/$/, "");
  if (!clientKey) return;

  // --- consent / opt-out -----------------------------------------------------
  const OPT_OUT_KEY = "aiw-optout";
  const dnt = navigator.doNotTrack === "1" || window.doNotTrack === "1";
  let enabled = !dnt && localStorage.getItem(OPT_OUT_KEY) !== "1" && window.AIW_ANALYTICS_CONSENT !== false;

  // --- identity (first-party only) ------------------------------------------
  const uuid = () => (crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random());
  function persistent(store, key, maxAgeMs) {
    try {
      const raw = store.getItem(key);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (!maxAgeMs || Date.now() - parsed.t < maxAgeMs) {
          parsed.t = Date.now(); store.setItem(key, JSON.stringify(parsed));
          return parsed.id;
        }
      }
    } catch { /* ignore */ }
    const id = uuid();
    try { store.setItem(key, JSON.stringify({ id, t: Date.now() })); } catch { /* ignore */ }
    return id;
  }
  // Ephemeral, tab-scoped visit id only — no persistent (localStorage) visitor
  // id, so there is no cross-visit/day identity. A "visit" == one session.
  const sessionId = persistent(sessionStorage, "aiw-session", 30 * 60 * 1000); // 30-min visit

  // --- context ---------------------------------------------------------------
  const device = () => {
    const w = window.innerWidth || 1024;
    return w < 640 ? "mobile" : w < 1024 ? "tablet" : "desktop";
  };
  const referrerHost = (() => {
    try { return document.referrer ? new URL(document.referrer).hostname : ""; } catch { return ""; }
  })();
  const path = () => location.pathname;

  // --- queue + flush ---------------------------------------------------------
  let queue = [];
  const send = (payload) => {
    const body = JSON.stringify(payload);
    const url = `${apiBase}/api/public/events`;
    try {
      if (navigator.sendBeacon) {
        navigator.sendBeacon(url, new Blob([body], { type: "text/plain" }));
        return;
      }
    } catch { /* fall through */ }
    fetch(url, { method: "POST", headers: { "Content-Type": "text/plain" }, body, keepalive: true }).catch(() => {});
  };
  const flush = () => {
    if (!enabled || !queue.length) return;
    const events = queue.splice(0, 50);
    send({ clientKey, host: location.hostname, sessionId, events });
  };
  function track(type, label, extra) {
    if (!enabled) return;
    queue.push({ type, label: label || "", path: path(), referrerHost, device: device(), ts: new Date().toISOString(), ...(extra || {}) });
    if (queue.length >= 10) flush();
  }
  window.aiwTrack = track;
  window.aiwAnalytics = {
    optOut() { enabled = false; queue = []; try { localStorage.setItem(OPT_OUT_KEY, "1"); } catch {} },
    optIn() { try { localStorage.removeItem(OPT_OUT_KEY); } catch {} enabled = !dnt; },
    get enabled() { return enabled; }
  };

  if (!enabled) return;

  // --- auto-capture ----------------------------------------------------------
  const startedAt = Date.now();
  let maxScroll = 0;
  const scrollSent = {};
  track("pageview");

  window.addEventListener("scroll", () => {
    const doc = document.documentElement;
    const scrollable = (doc.scrollHeight - window.innerHeight) || 1;
    const pct = Math.max(0, Math.min(100, Math.round((window.scrollY / scrollable) * 100)));
    if (pct > maxScroll) maxScroll = pct;
    for (const t of [25, 50, 75, 100]) {
      if (pct >= t && !scrollSent[t]) { scrollSent[t] = 1; track("scroll_depth", String(t), { scrollPct: t }); }
    }
  }, { passive: true });

  document.addEventListener("click", (e) => {
    const a = e.target.closest("a, [data-ev]");
    if (!a) return;
    const explicit = a.getAttribute && a.getAttribute("data-ev");
    if (explicit) { track("cta_click", explicit); return; }
    const href = (a.getAttribute && a.getAttribute("href")) || "";
    if (/^tel:/i.test(href)) track("phone_click", href.replace(/^tel:/i, "").slice(0, 40));
    else if (/^mailto:/i.test(href)) track("email_click");
    else if (/wa\.me|whatsapp/i.test(href)) track("whatsapp_click");
    else if (/^https?:/i.test(href)) {
      try { if (new URL(href).hostname !== location.hostname) track("outbound_click", new URL(href).hostname); }
      catch { /* ignore */ }
    }
  }, true);

  const startedForms = new WeakSet();
  document.addEventListener("focusin", (e) => {
    const form = e.target.closest && e.target.closest("form");
    if (form && !startedForms.has(form)) { startedForms.add(form); track("form_start", form.getAttribute("name") || form.id || ""); }
  }, true);
  document.addEventListener("submit", (e) => {
    const form = e.target;
    if (form && form.tagName === "FORM") track("form_submit", form.getAttribute("name") || form.id || "");
  }, true);

  const flushExit = () => {
    if (document.visibilityState === "hidden") {
      track("page_exit", "", { dwellMs: Date.now() - startedAt, scrollPct: maxScroll });
      flush();
    }
  };
  document.addEventListener("visibilitychange", flushExit);
  window.addEventListener("pagehide", () => { track("page_exit", "", { dwellMs: Date.now() - startedAt, scrollPct: maxScroll }); flush(); });
  setInterval(flush, 5000);
})();
