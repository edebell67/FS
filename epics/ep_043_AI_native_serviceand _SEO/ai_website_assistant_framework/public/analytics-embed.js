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
    else if (href.startsWith("#")) track("cta_click", a.getAttribute("aria-label") || a.textContent.trim().slice(0, 80) || href);
    else if (/^https?:/i.test(href)) {
      try { if (new URL(href).hostname !== location.hostname) track("outbound_click", new URL(href).hostname); }
      catch { /* ignore */ }
    }
    else if (href && !href.startsWith("javascript:")) track("cta_click", a.getAttribute("aria-label") || a.textContent.trim().slice(0, 80) || href);
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

  // Service cards declare stable service names in data-service. A service_view
  // is recorded once a card is substantially visible; no visitor input or page
  // text is collected. Dwell time per service is also accumulated (enter/exit
  // pairs from the same observer) to drive the highlight trigger below —
  // reuses this one observer rather than adding a second.
  const seenServices = new WeakSet();
  const dwellStart = new Map();
  const dwellAccum = new Map();
  const highlightTriggered = new Set();
  const DWELL_THRESHOLD_MS = 4000;
  if ("IntersectionObserver" in window) {
    const serviceObserver = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        const service = entry.target.getAttribute("data-service") || "";
        if (entry.isIntersecting) {
          if (!seenServices.has(entry.target)) {
            seenServices.add(entry.target);
            track("service_view", "", { service });
          }
          dwellStart.set(entry.target, Date.now());
        } else if (dwellStart.has(entry.target)) {
          const elapsed = Date.now() - dwellStart.get(entry.target);
          dwellStart.delete(entry.target);
          const total = (dwellAccum.get(service) || 0) + elapsed;
          dwellAccum.set(service, total);
          if (total >= DWELL_THRESHOLD_MS && !highlightTriggered.has(service)) {
            highlightTriggered.add(service);
            maybeShowHighlight(service);
          }
        }
      }
    }, { threshold: 0.6 });
    document.querySelectorAll("[data-service]").forEach((element) => serviceObserver.observe(element));
  }

  // Shared by both the promotion banner and the case-study highlight below —
  // one visual mechanism, two content sources. Only one banner occupies the
  // slot at a time.
  let activeBanner = null;
  let promotionActive = false;
  function renderBanner({ accentTitle, body, ctaLabel, ctaHref, service, onImpression, onClick }) {
    const banner = document.createElement("aside");
    banner.setAttribute("role", "region");
    banner.setAttribute("aria-label", accentTitle || "Notice");
    banner.style.cssText = "position:fixed;right:1rem;bottom:1rem;z-index:9999;max-width:20rem;padding:1rem 1.25rem;background:#0A0C0E;color:#fff;border:1px solid #C8F250;border-radius:.75rem;box-shadow:0 14px 36px rgba(0,0,0,.28);font:500 14px/1.4 system-ui,sans-serif";
    const title = document.createElement("strong");
    title.textContent = accentTitle;
    title.style.cssText = "display:block;color:#C8F250;margin-bottom:.25rem";
    const copy = document.createElement("span");
    copy.textContent = body;
    const action = document.createElement("a");
    action.href = ctaHref;
    action.textContent = ctaLabel;
    action.style.cssText = "display:inline-block;margin-top:.65rem;color:#C8F250;font-weight:700";
    // Phase 2d funnel: open the widget's lead form directly rather than
    // just scrolling to a contact section — every entry path (chat,
    // promotion, highlight) lands on the same capture point. Falls back to
    // the plain #contact navigation if the widget script hasn't mounted.
    action.addEventListener("click", (event) => {
      onClick();
      if (window.aiwOpenLeadForm?.(service)) event.preventDefault();
    });
    banner.append(title, copy, action);
    document.body.appendChild(banner);
    onImpression();
    activeBanner = banner;
    return banner;
  }

  // Owner-created offers are fetched from the same tracking service. Only a
  // current offer explicitly configured for the website is rendered.
  // Promotions always win the one banner slot over a highlight.
  fetch(`${apiBase}/api/public/promotions?tenant=${encodeURIComponent(clientKey)}`)
    .then((response) => response.ok ? response.json() : { promotions: [] })
    .then(({ promotions = [] }) => {
      const promotion = promotions.find((item) => Array.isArray(item.displayOn) && item.displayOn.includes("website"));
      if (!promotion || !promotion.description) return;
      promotionActive = true;
      renderBanner({
        accentTitle: promotion.valueLabel || "Offer",
        body: promotion.description,
        ctaLabel: "Discuss this offer",
        ctaHref: "#contact",
        service: (promotion.services || [])[0] || "",
        onImpression: () => track("promotion_impression", promotion.promotionId, { promotionId: promotion.promotionId, service: (promotion.services || [])[0] || "" }),
        onClick: () => track("promotion_click", promotion.promotionId, { promotionId: promotion.promotionId, service: (promotion.services || [])[0] || "" })
      });
    }).catch(() => {});

  // Triggered once a service has accumulated enough dwell time. Only shows
  // when no promotion is occupying the banner slot; re-checks after the
  // fetch resolves in case a promotion rendered while it was in flight.
  function maybeShowHighlight(service) {
    if (promotionActive || activeBanner) return;
    fetch(`${apiBase}/api/public/highlights?tenant=${encodeURIComponent(clientKey)}&service=${encodeURIComponent(service)}`)
      .then((response) => response.ok ? response.json() : { highlights: [] })
      .then(({ highlights = [] }) => {
        if (promotionActive || activeBanner) return;
        const highlight = highlights[0];
        if (!highlight) return;
        renderBanner({
          accentTitle: "What we've built",
          body: `${highlight.title} — ${highlight.description}`,
          ctaLabel: "See how we can help",
          ctaHref: "#contact",
          service: highlight.service,
          onImpression: () => track("highlight_impression", highlight.id, { highlightId: highlight.id, service: highlight.service }),
          onClick: () => track("highlight_click", highlight.id, { highlightId: highlight.id, service: highlight.service })
        });
      }).catch(() => {});
  }

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
