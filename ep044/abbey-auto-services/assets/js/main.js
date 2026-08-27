/*
 * Abbey Auto Services — demo site interactions.
 * Reads all content from config.js (garageConfig, servicesData, reviewsData,
 * galleryData, offersData, diagnosticSymptoms, paymentProducts) and renders
 * it into the page, then wires up the interactive components.
 */
(function () {
  "use strict";

  // ==========================================================================
  // Minimal inline icon set (stroke-based, matches design system)
  // ==========================================================================
  const ICONS = {
    wrench: "M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z",
    scan: "M3 7V5a2 2 0 0 1 2-2h2M17 3h2a2 2 0 0 1 2 2v2M21 17v2a2 2 0 0 1-2 2h-2M7 21H5a2 2 0 0 1-2-2v-2M3 12h18",
    tag: "M20.59 13.41 11 3.83A2 2 0 0 0 9.59 3.2L4 3a1 1 0 0 0-1 1l.2 5.59a2 2 0 0 0 .58 1.41l9.6 9.6a2 2 0 0 0 2.82 0l4.4-4.4a2 2 0 0 0 0-2.79zM7 7h.01",
    "map-pin": "M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z M12 13a3 3 0 1 0 0-6 3 3 0 0 0 0 6z",
    shield: "M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11z",
    car: "M5 17h14M5 17a2 2 0 1 1-4 0 2 2 0 0 1 4 0zM19 17a2 2 0 1 0 4 0 2 2 0 0 0-4 0zM3 17V11l2-5h14l2 5v6M3 11h18",
    "clipboard-check": "M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2 M9 3h6a1 1 0 0 1 1 1v1a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z M9 14l2 2 4-4",
    "clipboard-x": "M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2 M9 3h6a1 1 0 0 1 1 1v1a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z M10 12l4 4m0-4-4 4",
    settings: "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z",
    cog: "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM12 2v4M12 18v4M4.9 4.9l2.8 2.8M16.3 16.3l2.8 2.8M2 12h4M18 12h4M4.9 19.1l2.8-2.8M16.3 7.7l2.8-2.8",
    disc: "M12 12a2 2 0 1 0 0-4 2 2 0 0 0 0 4z M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z",
    "circle-dot": "M12 12a1 1 0 1 0 0-2 1 1 0 0 0 0 2z M12 20a8 8 0 1 0 0-16 8 8 0 0 0 0 16z",
    wind: "M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2",
    waves: "M2 6c1.5-2 3.5-2 5 0s3.5 2 5 0 3.5-2 5 0 3.5 2 5 0M2 12c1.5-2 3.5-2 5 0s3.5 2 5 0 3.5-2 5 0 3.5 2 5 0M2 18c1.5-2 3.5-2 5 0s3.5 2 5 0 3.5-2 5 0 3.5 2 5 0",
    snowflake: "M12 2v20M20 7l-8 5-8-5M20 17l-8-5-8 5M4.5 9.5l15 5M4.5 14.5l15-5",
    circle: "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z",
    move: "M5 9l-3 3 3 3M9 5l3-3 3 3M15 19l-3 3-3-3M19 9l3 3-3 3M2 12h20M12 2v20",
    "battery-charging": "M5 6H3a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h2M15 6h4a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1h-4M23 10v4M13 6l-3 5h4l-3 5",
    "battery-warning": "M17 6H3a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V7a1 1 0 0 0-1-1zM23 10v4M10 9v3M10 15h.01",
    zap: "M13 2 3 14h8l-1 8 10-12h-8l1-8z",
    link: "M10 13a5 5 0 0 0 7.5.5l2-2a5 5 0 0 0-7-7l-1 1M14 11a5 5 0 0 0-7.5-.5l-2 2a5 5 0 0 0 7 7l1-1",
    droplet: "M12 2s6 7 6 12a6 6 0 1 1-12 0c0-5 6-12 6-12z",
    "alert-triangle": "M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0zM12 9v4M12 17h.01",
    "alert-circle": "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 8v4M12 16h.01",
    truck: "M1 3h13v13H1zM14 8h4l3 3v5h-7V8zM5.5 20a2 2 0 1 0 0-4 2 2 0 0 0 0 4zM17.5 20a2 2 0 1 0 0-4 2 2 0 0 0 0 4z",
    leaf: "M11 20A7 7 0 0 1 4 13c0-6 9-12 17-12 0 8-6 17-12 17-1.5 0-3-.5-4-1.5zM4 13c3 0 8 1 11-4",
    "heart-pulse": "M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8zM3.5 12h4l2-4 3 7 2-4h6",
    power: "M12 2v10M18.4 6.6a9 9 0 1 1-12.8 0",
    activity: "M22 12h-4l-3 9L9 3l-3 9H2",
    "trending-down": "M23 18l-9.5-9.5-5 5L1 6M17 18h6v-6",
    thermometer: "M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z",
    "help-circle": "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM9.1 9a3 3 0 0 1 5.8 1c0 2-3 2-3 4M12 17h.01",
    check: "M20 6 9 17l-5-5",
    x: "M18 6 6 18M6 6l12 12",
    "chevron-left": "M15 18l-6-6 6-6",
    "chevron-right": "M9 18l6-6-6-6",
    "chevron-down": "M6 9l6 6 6-6",
    plus: "M12 5v14M5 12h14",
    star: "M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.9-6.2-3.3-6.2 3.3 1.2-6.9-5-4.9 6.9-1z",
    phone: "M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.1-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 3a2 2 0 0 1-.5 2.1L8 10.1a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c1 .3 2 .5 3 .7a2 2 0 0 1 1.7 2z",
    mail: "M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z M22 6l-10 7L2 6",
    "message-circle": "M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.4 8.4 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z",
    navigation: "M3 11l19-9-9 19-2-8-8-2z",
    facebook: "M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z",
    instagram: "M17 2H7a5 5 0 0 0-5 5v10a5 5 0 0 0 5 5h10a5 5 0 0 0 5-5V7a5 5 0 0 0-5-5z M12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM17.5 6.5h.01",
    "shopping-cart": "M9 22a1 1 0 1 0 0-2 1 1 0 0 0 0 2zM20 22a1 1 0 1 0 0-2 1 1 0 0 0 0 2zM1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6",
    "credit-card": "M1 4h22v16H1zM1 10h22",
    calendar: "M8 2v4M16 2v4M3 8h18M4 4h16a1 1 0 0 1 1 1v15a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1z",
    clock: "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 6v6l4 2",
    user: "M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z",
    users: "M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8",
    award: "M12 15a6 6 0 1 0 0-12 6 6 0 0 0 0 12zM8.2 13.9 7 23l5-3 5 3-1.2-9.1",
    play: "M5 3l16 9-16 9z",
    building: "M6 22V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v18M6 22h12M9 7h1M14 7h1M9 11h1M14 11h1M9 15h1M14 15h1",
    "arrow-right": "M5 12h14M13 6l6 6-6 6"
  };
  function icon(name, extra) {
    const d = ICONS[name] || ICONS.wrench;
    const parts = d.split(/(?=M)/g).filter(Boolean);
    const paths = parts.map((p) => `<path d="${p.trim()}"></path>`).join("");
    return `<svg class="icon ${extra || ""}" viewBox="0 0 24 24">${paths}</svg>`;
  }

  function renderInlineIcons(root) {
    (root || document).querySelectorAll("[data-icon]").forEach((el) => {
      el.innerHTML = icon(el.getAttribute("data-icon"));
    });
  }
  window.renderInlineIcons = renderInlineIcons;

  // ==========================================================================
  // Config bindings — every [data-cfg] / [data-cfg-href] element is populated here
  // ==========================================================================
  const telHref = "tel:" + garageConfig.phone.replace(/\s+/g, "");
  const mailHref = "mailto:" + garageConfig.email;

  const bindings = Object.assign({}, garageConfig, {
    year: "© " + new Date().getFullYear() + " " + garageConfig.businessName,
    telHref, mailHref,
    fullAddress: garageConfig.fullAddress,
    aboutBody: garageConfig.about.bodyCopy,
    videoHeading: "Take a Look Inside " + garageConfig.businessName,
    reviewsHeading: "What " + garageConfig.businessName + " customers say"
  });

  function applyBindings() {
    document.querySelectorAll("[data-cfg]").forEach((el) => {
      const key = el.getAttribute("data-cfg");
      if (bindings[key] !== undefined) el.textContent = bindings[key];
    });
    document.querySelectorAll("[data-cfg-href]").forEach((el) => {
      const key = el.getAttribute("data-cfg-href");
      if (bindings[key] !== undefined) el.setAttribute("href", bindings[key]);
    });
    document.querySelectorAll("[data-cfg-src]").forEach((el) => {
      const key = el.getAttribute("data-cfg-src");
      if (bindings[key]) el.setAttribute("src", bindings[key]);
    });
    if (document.body.dataset.page === "home") {
      document.title = garageConfig.seo.title;
      const metaDesc = document.querySelector('meta[name="description"]');
      if (metaDesc) metaDesc.setAttribute("content", garageConfig.seo.description);
    }
    document.querySelectorAll(".brand-emblem").forEach((el) => (el.textContent = garageConfig.emblemInitials));
  }

  // ==========================================================================
  // Renderers
  // ==========================================================================
  function renderTrustStrip() {
    const el = document.getElementById("trustGrid");
    if (!el) return;
    el.innerHTML = garageConfig.trustIndicators
      .map(
        (t) => `<div class="trust-item"><div class="icon-wrap">${icon(t.icon)}</div><span>${t.label}</span></div>`
      )
      .join("");
  }

  function renderServices(limit) {
    const el = document.getElementById("servicesGrid");
    if (!el) return;
    const list = limit ? servicesData.slice(0, limit) : servicesData;
    el.innerHTML = list
      .map(
        (s) => `
      <article class="service-card reveal">
        <div class="icon-wrap">${icon(s.icon)}</div>
        <h3>${s.title}</h3>
        <p class="desc">${s.short}</p>
        <div class="price">${s.price}</div>
        <div class="service-card-actions">
          <button class="btn btn-dark btn-sm" data-service-detail="${s.id}">Learn More</button>
          <button class="btn btn-outline btn-sm" data-quote-service="${s.title}" style="border-color:var(--paper-dim);color:var(--graphite)">Request Quote</button>
        </div>
      </article>`
      )
      .join("");
  }

  function populateServiceSelect() {
    const sel = document.getElementById("quoteService");
    if (!sel) return;
    sel.innerHTML =
      '<option value="">Select a service…</option>' +
      servicesData.map((s) => `<option value="${s.title}">${s.title}</option>`).join("");
  }

  function renderWhyChooseUs() {
    const el = document.getElementById("whyGrid");
    if (!el) return;
    el.innerHTML = garageConfig.whyChooseUs
      .map(
        (w) => `<div class="why-item reveal"><div class="icon-wrap">${icon("check")}</div><p>${w}</p></div>`
      )
      .join("");
  }

  function renderAboutValues() {
    const el = document.getElementById("aboutValues");
    if (!el) return;
    el.innerHTML = garageConfig.about.values
      .map((v) => `<li>${icon("check")}<span>${v}</span></li>`)
      .join("");
  }

  function renderSpecialisms() {
    const el = document.getElementById("specialismGrid");
    if (!el) return;
    el.innerHTML = garageConfig.vehicleSpecialisms
      .map((v) => `<span class="specialism-badge">${v}</span>`)
      .join("");
  }

  function renderOffers() {
    const el = document.getElementById("offersGrid");
    if (!el) return;
    const active = offersData.filter((o) => o.enabled);
    el.innerHTML = active
      .map(
        (o) => `
      <div class="offer-card reveal">
        <div class="offer-price">${o.price}</div>
        <h3>${o.title}</h3>
        <p class="desc">${o.description}</p>
        <span class="expiry">Ends ${formatDate(o.expiry)}</span>
        <span class="terms">${o.terms}</span>
        <button class="btn btn-primary btn-sm" data-quote-service="${o.title}">Claim Offer</button>
      </div>`
      )
      .join("");
  }

  function formatDate(iso) {
    const d = new Date(iso + "T00:00:00");
    return d.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
  }

  let currentGalleryFilter = "All";
  function renderGallery() {
    const grid = document.getElementById("galleryGrid");
    const filters = document.getElementById("galleryFilters");
    if (!grid) return;
    const cats = ["All", ...new Set(galleryData.map((g) => g.category))];
    if (filters) {
      filters.innerHTML = cats
        .map((c) => `<button class="chip${c === currentGalleryFilter ? " selected" : ""}" data-gallery-filter="${c}">${c}</button>`)
        .join("");
    }
    const items = galleryData.filter((g) => currentGalleryFilter === "All" || g.category === currentGalleryFilter);
    grid.innerHTML = items
      .map(
        (g, i) => `
      <div class="gallery-item reveal" data-gallery-open="${galleryData.indexOf(g)}">
        <div class="ph">${icon("car")}</div>
        <div class="cap">${g.caption}</div>
      </div>`
      )
      .join("");
  }

  function renderReviews() {
    const el = document.getElementById("reviewsTrack");
    if (!el) return;
    el.innerHTML = reviewsData
      .map(
        (r) => `
      <article class="review-card reveal">
        <div class="review-stars">${"★".repeat(r.rating)}${"☆".repeat(5 - r.rating)}</div>
        <p class="text">“${r.text}”</p>
        <div class="review-meta">
          <div class="review-avatar">${r.name.split(" ").map((n) => n[0]).join("")}</div>
          <div>
            <div class="review-name">${r.name}${r.placeholder ? ' <span style="color:var(--steel);font-weight:400">(sample)</span>' : ""}</div>
            <div class="review-sub">${r.service} · via ${r.source}</div>
          </div>
        </div>
      </article>`
      )
      .join("");
  }

  function renderStats() {
    const el = document.getElementById("statsRow");
    if (!el) return;
    el.innerHTML = garageConfig.stats
      .map(
        (s, i) => `
      <div class="stat-item reveal">
        <div class="stat-value" data-count="${s.value}" data-suffix="${s.suffix}">0${s.suffix}</div>
        <div class="stat-label">${s.label}</div>
        ${s.placeholder ? '<span class="stat-flag">Sample figure</span>' : ""}
      </div>`
      )
      .join("");
  }

  function renderHours() {
    const el = document.getElementById("hoursTable");
    if (!el) return;
    const todayIdx = (new Date().getDay() + 6) % 7; // Monday = 0
    el.innerHTML = garageConfig.openingHours
      .map((h, i) => `<tr class="${i === todayIdx ? "today" : ""}"><td>${h.day}</td><td>${h.hours}</td></tr>`)
      .join("");
  }

  function renderPayGrid() {
    const el = document.getElementById("payGrid");
    if (!el) return;
    el.innerHTML = paymentProducts
      .map(
        (p) => `
      <div class="pay-card reveal">
        <div class="icon-wrap" style="width:36px;height:36px;border-radius:9px;background:var(--paper-dim);color:var(--amber-dim);display:flex;align-items:center;justify-content:center">${icon("credit-card")}</div>
        <div class="pay-title">${p.name}</div>
        <div class="pay-price">${p.price}</div>
        <button class="btn btn-dark btn-sm btn-block" data-pay-item="${p.name}">${icon("shopping-cart")} Pay / Reserve</button>
      </div>`
      )
      .join("");
  }

  function renderSymptoms() {
    const el = document.getElementById("symptomGrid");
    if (!el) return;
    el.innerHTML = diagnosticSymptoms
      .map(
        (s) => `<button class="symptom-btn" data-symptom="${s.id}">${icon(s.icon)}<span>${s.label}</span></button>`
      )
      .join("");
  }

  const symptomResponses = {
    default:
      "This symptom may have several possible causes. Avoid relying on an online diagnosis alone — book an inspection so the fault can be assessed safely by a technician."
  };

  function renderDateChips() {
    const row = document.getElementById("dateChips");
    if (!row) return;
    const days = [];
    const d = new Date();
    let added = 0;
    while (added < 7) {
      d.setDate(d.getDate() + (added === 0 ? 1 : 1));
      if (d.getDay() !== 0) {
        days.push(new Date(d));
        added++;
      }
    }
    row.innerHTML = days
      .map(
        (day, i) => `
      <button class="date-chip${i === 0 ? " selected" : ""}" data-date="${day.toISOString().slice(0, 10)}">
        <div class="dow">${day.toLocaleDateString("en-GB", { weekday: "short" })}</div>
        <div class="dom">${day.getDate()}</div>
        <div class="mon">${day.toLocaleDateString("en-GB", { month: "short" })}</div>
      </button>`
      )
      .join("");
  }

  function renderTimeSlots() {
    const row = document.getElementById("timeSlots");
    if (!row) return;
    const slots = ["08:30", "09:30", "10:30", "11:30", "13:00", "14:00", "15:00", "16:00"];
    row.innerHTML = slots
      .map((t, i) => {
        const taken = i === 2 || i === 5;
        return `<button class="time-slot${i === 0 ? " selected" : ""}" ${taken ? "disabled" : ""} data-time="${t}">${t}</button>`;
      })
      .join("");
  }

  // ==========================================================================
  // Interactions
  // ==========================================================================
  function initNav() {
    const toggle = document.getElementById("navToggle");
    const drawer = document.getElementById("mobileDrawer");
    const close = document.getElementById("drawerClose");
    if (!toggle || !drawer) return;
    toggle.addEventListener("click", () => drawer.classList.add("open"));
    close.addEventListener("click", () => drawer.classList.remove("open"));
    drawer.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => drawer.classList.remove("open")));
  }

  function initTabs() {
    const tabs = document.querySelectorAll(".tool-tab");
    const panels = document.querySelectorAll(".tool-tab-panel");
    tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        tabs.forEach((t) => t.classList.remove("active"));
        panels.forEach((p) => (p.style.display = "none"));
        tab.classList.add("active");
        const target = document.getElementById(tab.dataset.target);
        if (target) target.style.display = "block";
      });
    });
  }

  function initServiceQuoteButtons() {
    document.body.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-quote-service]");
      if (!btn) return;
      const sel = document.getElementById("quoteService");
      const quoteTab = document.querySelector('.tool-tab[data-target="panel-quote"]');
      if (sel) sel.value = btn.dataset.quoteService;
      if (quoteTab) quoteTab.click();
      document.getElementById("toolPanel")?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  function initServiceDetailModal() {
    document.body.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-service-detail]");
      if (!btn) return;
      const svc = servicesData.find((s) => s.id === btn.dataset.serviceDetail);
      if (!svc) return;
      openModal(
        icon(svc.icon),
        svc.title,
        svc.description + `<br><br><strong style="color:var(--graphite)">${svc.price}</strong>`
      );
    });
  }

  function validateField(field) {
    const wrap = field.closest(".form-field");
    const errorEl = wrap?.querySelector(".form-error");
    let valid = field.checkValidity();
    if (valid) {
      wrap?.classList.remove("has-error");
      if (errorEl) errorEl.textContent = "";
    } else {
      wrap?.classList.add("has-error");
      if (errorEl) {
        if (field.validity.valueMissing) errorEl.textContent = "This field is required.";
        else if (field.validity.typeMismatch) errorEl.textContent = "Please check the format.";
        else if (field.validity.patternMismatch) errorEl.textContent = "Please check the format.";
        else errorEl.textContent = "Please check this field.";
      }
    }
    return valid;
  }

  function initForm(formId, successId, thankYouTemplate) {
    const form = document.getElementById(formId);
    const success = document.getElementById(successId);
    if (!form) return;
    form.querySelectorAll("input, select, textarea").forEach((f) => {
      f.addEventListener("blur", () => validateField(f));
    });
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const fields = [...form.querySelectorAll("input, select, textarea")];
      const valid = fields.map(validateField).every(Boolean);
      if (!valid) {
        form.querySelector(".has-error input, .has-error select, .has-error textarea")?.focus();
        return;
      }
      form.style.display = "none";
      if (success) {
        success.classList.add("show");
        success.innerHTML = thankYouTemplate();
      }
    });
  }

  function thankYouHtml() {
    return `
      <div class="icon-wrap">${icon("check")}</div>
      <h3>Thank you</h3>
      <p>Your enquiry has been prepared for <strong>${garageConfig.businessName}</strong>. A live version of this website can connect this form directly to the owner-approved contact or booking process.</p>
      <button class="btn btn-outline" style="border-color:var(--paper-dim);color:var(--graphite)" onclick="location.reload()">Start a new enquiry</button>
    `;
  }

  function initChips() {
    document.body.addEventListener("click", (e) => {
      const chip = e.target.closest(".chip[data-vehicle-type]");
      if (chip) {
        chip.parentElement.querySelectorAll(".chip").forEach((c) => c.classList.remove("selected"));
        chip.classList.add("selected");
        const input = document.getElementById("quoteVehicleType");
        if (input) input.value = chip.dataset.vehicleType;
      }
      const filterChip = e.target.closest("[data-gallery-filter]");
      if (filterChip) {
        currentGalleryFilter = filterChip.dataset.galleryFilter;
        renderGallery();
        attachRevealObserver();
      }
      const dateChip = e.target.closest(".date-chip");
      if (dateChip) {
        dateChip.parentElement.querySelectorAll(".date-chip").forEach((c) => c.classList.remove("selected"));
        dateChip.classList.add("selected");
      }
      const timeChip = e.target.closest(".time-slot:not([disabled])");
      if (timeChip) {
        timeChip.parentElement.querySelectorAll(".time-slot").forEach((c) => c.classList.remove("selected"));
        timeChip.classList.add("selected");
      }
    });
  }

  function initDiagnostic() {
    document.body.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-symptom]");
      if (!btn) return;
      document.querySelectorAll(".symptom-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const symptom = diagnosticSymptoms.find((s) => s.id === btn.dataset.symptom);
      const resultEl = document.getElementById("symptomResult");
      if (!resultEl || !symptom) return;
      resultEl.classList.add("show");
      resultEl.innerHTML = `
        <p><strong>${symptom.label}.</strong> ${symptomResponses.default}</p>
        <button class="btn btn-primary btn-sm" data-quote-service="Diagnostic Inspection — ${symptom.label}">Request a Diagnostic Inspection</button>
      `;
      resultEl.scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
  }

  // Gallery lightbox
  let lightboxIndex = 0;
  function openLightbox(index) {
    lightboxIndex = index;
    updateLightbox();
    document.getElementById("lightbox").classList.add("open");
  }
  function updateLightbox() {
    const g = galleryData[lightboxIndex];
    document.getElementById("lightboxCap").textContent = `${g.caption} — ${g.category}`;
  }
  function initLightbox() {
    document.body.addEventListener("click", (e) => {
      const item = e.target.closest("[data-gallery-open]");
      if (item) openLightbox(parseInt(item.dataset.galleryOpen, 10));
      if (e.target.closest("#lightboxClose") || e.target.id === "lightbox") {
        document.getElementById("lightbox").classList.remove("open");
      }
      if (e.target.closest("#lightboxPrev")) {
        lightboxIndex = (lightboxIndex - 1 + galleryData.length) % galleryData.length;
        updateLightbox();
      }
      if (e.target.closest("#lightboxNext")) {
        lightboxIndex = (lightboxIndex + 1) % galleryData.length;
        updateLightbox();
      }
    });
    document.addEventListener("keydown", (e) => {
      const lb = document.getElementById("lightbox");
      if (!lb || !lb.classList.contains("open")) return;
      if (e.key === "Escape") lb.classList.remove("open");
      if (e.key === "ArrowLeft") document.getElementById("lightboxPrev").click();
      if (e.key === "ArrowRight") document.getElementById("lightboxNext").click();
    });
  }

  // Review carousel controls
  function initReviewCarousel() {
    const track = document.getElementById("reviewsTrack");
    const prev = document.getElementById("reviewPrev");
    const next = document.getElementById("reviewNext");
    if (!track) return;
    const scrollAmt = () => track.querySelector(".review-card")?.offsetWidth + 20 || 340;
    prev?.addEventListener("click", () => track.scrollBy({ left: -scrollAmt(), behavior: "smooth" }));
    next?.addEventListener("click", () => track.scrollBy({ left: scrollAmt(), behavior: "smooth" }));
  }

  // Before/after slider
  function initBeforeAfter() {
    const slider = document.getElementById("baSlider");
    if (!slider) return;
    const handle = document.getElementById("baHandle");
    const after = document.getElementById("baAfter");
    let dragging = false;
    function setPos(clientX) {
      const rect = slider.getBoundingClientRect();
      let pct = ((clientX - rect.left) / rect.width) * 100;
      pct = Math.max(4, Math.min(96, pct));
      handle.style.left = pct + "%";
      after.style.clipPath = `inset(0 0 0 ${pct}%)`;
    }
    handle.addEventListener("pointerdown", () => (dragging = true));
    window.addEventListener("pointerup", () => (dragging = false));
    window.addEventListener("pointermove", (e) => dragging && setPos(e.clientX));
    slider.addEventListener("click", (e) => setPos(e.clientX));
  }

  // FAQ accordion
  function initFaq() {
    document.querySelectorAll(".faq-q").forEach((btn) => {
      btn.addEventListener("click", () => {
        const item = btn.closest(".faq-item");
        const answer = item.querySelector(".faq-a");
        const isOpen = item.classList.contains("open");
        document.querySelectorAll(".faq-item").forEach((i) => {
          i.classList.remove("open");
          i.querySelector(".faq-a").style.maxHeight = null;
        });
        if (!isOpen) {
          item.classList.add("open");
          answer.style.maxHeight = answer.scrollHeight + "px";
        }
      });
    });
  }

  // Payment demo modal
  function openModal(iconHtml, title, bodyHtml) {
    const overlay = document.getElementById("modalOverlay");
    document.getElementById("modalIcon").innerHTML = iconHtml;
    document.getElementById("modalTitle").textContent = title;
    document.getElementById("modalBody").innerHTML = bodyHtml;
    overlay.classList.add("open");
  }
  function initPaymentModal() {
    document.body.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-pay-item]");
      if (btn) {
        openModal(
          icon("credit-card"),
          "Payment demonstration only",
          `You selected <strong style="color:var(--graphite)">${btn.dataset.payItem}</strong>. The live website can be connected to Stripe, PayPal, SumUp, Square, or ${garageConfig.businessName}'s existing payment provider. No payment has been taken.`
        );
      }
      if (e.target.closest("[data-pay-generic]")) {
        openModal(
          icon("credit-card"),
          "Payment demonstration only",
          `The live website can be connected to Stripe, PayPal, SumUp, Square, or ${garageConfig.businessName}'s existing payment provider. No payment has been taken.`
        );
      }
      if (e.target.closest("#modalClose") || e.target.id === "modalOverlay") {
        document.getElementById("modalOverlay").classList.remove("open");
      }
    });
  }

  // Cookie banner
  function initCookieBanner() {
    const banner = document.getElementById("cookieBanner");
    if (!banner) return;
    if (localStorage.getItem("abbey-auto-services_cookie_choice")) return;
    setTimeout(() => banner.classList.add("show"), 900);
    document.getElementById("cookieAccept")?.addEventListener("click", () => {
      localStorage.setItem("abbey-auto-services_cookie_choice", "accepted");
      banner.classList.remove("show");
    });
    document.getElementById("cookieDecline")?.addEventListener("click", () => {
      localStorage.setItem("abbey-auto-services_cookie_choice", "declined");
      banner.classList.remove("show");
    });
  }

  // Animated counters
  function initCounters() {
    const items = document.querySelectorAll("[data-count]");
    if (!items.length) return;
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const el = entry.target;
          const target = parseFloat(el.dataset.count);
          const suffix = el.dataset.suffix || "";
          const isFloat = target % 1 !== 0;
          let start = 0;
          const duration = 1200;
          const t0 = performance.now();
          function tick(now) {
            const p = Math.min(1, (now - t0) / duration);
            const eased = 1 - Math.pow(1 - p, 3);
            const val = start + (target - start) * eased;
            el.textContent = (isFloat ? val.toFixed(1) : Math.round(val)) + suffix;
            if (p < 1) requestAnimationFrame(tick);
          }
          requestAnimationFrame(tick);
          obs.unobserve(el);
        });
      },
      { threshold: 0.5 }
    );
    items.forEach((el) => obs.observe(el));
  }

  // Scroll reveal
  function attachRevealObserver() {
    const items = document.querySelectorAll(".reveal:not(.in)");
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    items.forEach((el) => obs.observe(el));
  }

  // Header scroll shadow (subtle)
  function initHeaderScroll() {
    const header = document.querySelector(".site-header");
    if (!header) return;
    window.addEventListener("scroll", () => {
      header.style.boxShadow = window.scrollY > 12 ? "0 10px 30px -20px rgba(0,0,0,0.5)" : "none";
    });
  }

  // ==========================================================================
  // Init
  // ==========================================================================
  document.addEventListener("DOMContentLoaded", () => {
    applyBindings();
    renderInlineIcons();
    renderTrustStrip();
    renderServices(document.body.dataset.page === "home" ? 9 : null);
    populateServiceSelect();
    renderWhyChooseUs();
    renderAboutValues();
    renderSpecialisms();
    renderOffers();
    renderGallery();
    renderReviews();
    renderStats();
    renderHours();
    renderPayGrid();
    renderSymptoms();
    renderDateChips();
    renderTimeSlots();

    initNav();
    initTabs();
    initServiceQuoteButtons();
    initServiceDetailModal();
    initForm("quoteForm", "quoteSuccess", thankYouHtml);
    initForm("bookingForm", "bookingSuccess", thankYouHtml);
    initForm("contactForm", "contactSuccess", thankYouHtml);
    initChips();
    initDiagnostic();
    initLightbox();
    initReviewCarousel();
    initBeforeAfter();
    initFaq();
    initPaymentModal();
    initCookieBanner();
    initCounters();
    initHeaderScroll();
    attachRevealObserver();
  });
})();
