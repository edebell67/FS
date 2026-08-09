(() => {
  const script = document.currentScript;
  const clientKey = script?.dataset.client;
  const apiBase = (script?.dataset.apiBase || new URL(script.src).origin).replace(/\/$/, "");
  if (!clientKey || document.querySelector("ai-website-assistant")) return;

  const host = document.createElement("ai-website-assistant");
  const root = host.attachShadow({ mode: "open" });
  document.body.append(host);
  // Share the analytics session id (aiw-session) when present, so a visitor's
  // page behaviour and their chat stitch into one journey; otherwise mint one.
  const sharedSessionId = (() => {
    try {
      const raw = sessionStorage.getItem("aiw-session");
      if (raw) return JSON.parse(raw).id;
      const id = crypto.randomUUID();
      sessionStorage.setItem("aiw-session", JSON.stringify({ id, t: Date.now() }));
      return id;
    } catch { return crypto.randomUUID(); }
  })();
  const state = { client: null, open: false, sessionId: sharedSessionId, history: [], proactive: false, owner: null };
  const declinedKey = `aiw-declined-${clientKey}`;
  // Email for the "no direct answer" fallback is asked at most once per
  // session: { asked: bool, email: string|null }. Once asked (accepted or
  // not), never asked again this session — later unanswered questions
  // either accumulate silently (email known) or get a quiet one-line note
  // (email not given), never a second prompt.
  const qaKey = `aiw-qa-${clientKey}`;
  function readQaState() { try { return JSON.parse(sessionStorage.getItem(qaKey) || "{}"); } catch { return {}; } }
  function writeQaState(patch) { try { sessionStorage.setItem(qaKey, JSON.stringify({ ...readQaState(), ...patch })); } catch { /* storage unavailable */ } }
  const NEGATIVE_REPLY = /^(no|nah|nope|no\s*thanks?|no\s*thank\s*you|not\s*now|not\s*interested|not\s*right\s*now|i'?m\s*(good|fine|ok|okay)|no\s*need|leave\s*me\s*alone|go\s*away|maybe\s*later|later)\b/i;

  const style = document.createElement("style");
  style.textContent = `
    :host { --accent:#e85d3f; --ink:#17211f; --surface:#f5f0e7; position:fixed; z-index:2147483000; right:22px; bottom:20px; font-family:"Trebuchet MS",sans-serif; color:var(--ink); }
    * { box-sizing:border-box; }
    button,input,textarea,select { font:inherit; }
    button { cursor:pointer; }
    .launcher { width:64px;height:64px;border:0;border-radius:50%;background:var(--ink);color:white;box-shadow:0 16px 44px #10171642;display:grid;place-items:center;transition:transform .25s ease,background .25s; }
    .launcher:hover { transform:translateY(-3px) rotate(-2deg);background:var(--accent); }
    .launcher svg { width:27px; }
    .pulse { position:absolute;right:2px;top:2px;width:13px;height:13px;border:3px solid white;border-radius:50%;background:#68a878; }
    .panel { position:absolute;right:0;bottom:76px;width:min(390px,calc(100vw - 24px));height:min(660px,calc(100svh - 112px));background:#fffdf8;border:1px solid #17211f1f;border-radius:26px;box-shadow:0 28px 90px #11191640;overflow:hidden;display:grid;grid-template-rows:auto 1fr auto;transform-origin:bottom right;animation:arrive .32s cubic-bezier(.2,.8,.2,1); }
    @keyframes arrive { from{opacity:0;transform:translateY(18px) scale(.96)}to{opacity:1;transform:none} }
    header { background:var(--ink);color:white;padding:20px 20px 17px;position:relative;overflow:hidden; }
    header:after { content:"";position:absolute;width:130px;height:130px;border:1px solid #ffffff2b;border-radius:50%;right:-45px;top:-72px;pointer-events:none; }
    .brand { display:flex;gap:12px;align-items:center; }
    .mark { width:40px;height:40px;border-radius:12px;background:var(--accent);display:grid;place-items:center;font-family:Georgia,serif;font-weight:700;letter-spacing:-1px; }
    h2 { margin:0;font:700 17px/1.1 Georgia,serif;letter-spacing:-.2px; }
    .status { margin:4px 0 0;font-size:11px;color:#d8dfdc;letter-spacing:.03em; }
    .console-toggle { position:absolute;right:112px;top:14px;width:32px;height:32px;border:0;border-radius:50%;background:#ffffff12;color:#ffffffb0;font-size:13px;line-height:1; }
    .console-toggle:hover { background:#ffffff2b;color:white; }
    .home { position:absolute;right:54px;top:14px;border:1px solid #ffffff42;border-radius:999px;background:#ffffff12;color:white;padding:7px 10px;font-size:10px;font-weight:700; }
    .home:hover { background:#ffffff2b; }
    .close { position:absolute;right:14px;top:14px;width:32px;height:32px;border:0;border-radius:50%;background:#ffffff12;color:white;font-size:22px;line-height:1; }
    .demo { background:#f8d89a;color:#533c16;padding:7px 18px;font-size:11px;font-weight:700;letter-spacing:.04em; }
    .messages { padding:19px 17px 12px;overflow-y:auto;scroll-behavior:smooth;background:linear-gradient(#fffdf8,#fbf7ef); }
    .message { max-width:88%;padding:12px 14px;margin:0 0 11px;border-radius:17px;font-size:13px;line-height:1.55;animation:message .23s ease both;white-space:pre-wrap; }
    @keyframes message { from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:none} }
    .assistant { background:#ece8de;border-bottom-left-radius:5px; }
    .user { margin-left:auto;background:var(--accent);color:white;border-bottom-right-radius:5px; }
    .sources { font-size:10px;display:block;margin-top:7px;opacity:.66; }
    .action { border:1px solid var(--ink);background:transparent;color:var(--ink);padding:9px 12px;border-radius:999px;margin:0 6px 11px 0;font-size:11px;font-weight:700;transition:.18s; }
    .action:hover { background:var(--ink);color:white; }
    .quick { display:flex;gap:7px;overflow-x:auto;padding:0 0 10px;scrollbar-width:none;flex-wrap:wrap; }
    .group-label { margin:2px 0 7px;padding-top:9px;border-top:1px solid #17211f16;font-size:9px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:#8a837a; }
    .quick button { white-space:nowrap;border:1px solid #17211f24;background:#fffdf8;border-radius:999px;padding:8px 10px;font-size:10px;color:var(--ink); }
    form.composer { padding:11px 13px 13px;border-top:1px solid #17211f12;display:flex;gap:8px;background:#fffdf8; }
    .composer input { min-width:0;flex:1;border:1px solid #17211f25;background:white;border-radius:999px;padding:11px 14px;color:var(--ink);outline:none; }
    .composer input:focus { border-color:var(--accent);box-shadow:0 0 0 3px color-mix(in srgb,var(--accent),transparent 82%); }
    .send { width:42px;height:42px;border:0;border-radius:50%;background:var(--accent);color:white;font-size:18px; }
    .module-form { background:white;border:1px solid #17211f1b;border-radius:16px;padding:13px;margin:0 0 12px;display:grid;gap:8px; }
    .module-form strong { font:700 14px Georgia,serif; }
    .module-form label { display:grid;gap:5px;font-size:9px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#6e6a62; }
    .module-form input,.module-form textarea,.module-form select { width:100%;border:1px solid #17211f24;border-radius:9px;padding:9px;font-size:11px;background:#fffdf8;color:var(--ink); }
    .module-form textarea { resize:vertical;min-height:62px; }
    .module-form button { border:0;border-radius:9px;background:var(--ink);color:white;padding:10px;font-weight:700;font-size:11px; }
    .demo-head { display:flex;align-items:center;justify-content:space-between;gap:10px; }
    .demo-pill { border:1px solid #9f711e55;background:#fff2d5;color:#6f4b0c;border-radius:999px;padding:4px 7px;font-size:8px;font-weight:800;letter-spacing:.08em; }
    .demo-note { margin:0;color:#70695f;font-size:10px;line-height:1.45; }
    .price-preview { border-left:3px solid var(--accent);background:#f7f1e7;padding:9px 10px;border-radius:4px 9px 9px 4px;font-size:11px;font-weight:700; }
    .demo-receipt { background:linear-gradient(145deg,#fff,#f7efe2);border:1px solid #17211f22;border-radius:16px;padding:14px;margin-bottom:12px;display:grid;gap:7px; }
    .demo-receipt strong { font:700 15px Georgia,serif; }
    .demo-receipt code { font:700 10px/1.2 monospace;color:var(--accent); }
    .demo-receipt span { font-size:10px;line-height:1.45;color:#655f56; }
    .error { color:#a63224;font-size:11px; }
    .console-login { padding:6px 3px 4px;display:grid;gap:12px; }
    .console-login strong { font:700 15px Georgia,serif; }
    .console-login label { display:grid;gap:6px;font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#6e6a62; }
    .console-login input { border:1px solid #17211f24;border-radius:9px;padding:11px;font-size:13px;background:#fffdf8;color:var(--ink); }
    .console-login button.primary { border:0;border-radius:9px;background:var(--ink);color:white;padding:11px;font-weight:700;font-size:12px; }
    .console-back { background:transparent;border:0;color:var(--accent);font-size:11px;font-weight:700;text-align:left;padding:0;justify-self:start; }
    .console { padding:2px 1px 4px; }
    .console-filter { display:grid;gap:8px;margin-bottom:10px; }
    .console-filter label { display:grid;gap:4px;font-size:9px;text-transform:uppercase;letter-spacing:.05em;color:#6e6a62; }
    .console-filter input,.console-filter select { border:1px solid #17211f24;border-radius:8px;padding:8px;font-size:11px;background:#fffdf8;color:var(--ink);width:100%; }
    .console-filter-actions { display:flex;gap:8px; }
    .console-filter-actions button { flex:1;border:1px solid #17211f24;background:#fffdf8;border-radius:8px;padding:8px;font-size:10px;font-weight:700;color:var(--ink); }
    .console-filter-actions button.primary { background:var(--ink);color:white;border-color:var(--ink); }
    .console-summary { font-size:10px;color:#6e6a62;margin:0 0 12px;min-height:12px; }
    .console-stats { display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:16px; }
    .console-stat { border:1px solid #17211f18;border-radius:10px;padding:10px;background:#fbfaf6; }
    .console-stat strong { display:block;font:700 18px Georgia,serif; }
    .console-stat span { font-size:8px;text-transform:uppercase;letter-spacing:.05em;color:#8a837a; }
    .console-section-h { font:700 11px Georgia,serif;margin:14px 0 8px;text-transform:uppercase;letter-spacing:.04em;color:#6e6a62; }
    .console-bar-row { display:grid;grid-template-columns:88px 1fr 24px;align-items:center;gap:6px;margin-bottom:5px;font-size:9px; }
    .console-bar-label { white-space:nowrap;overflow:hidden;text-overflow:ellipsis; }
    .console-bar-track { height:6px;background:#ece8de;border-radius:100px;overflow:hidden; }
    .console-bar-fill { height:100%;background:var(--accent);border-radius:100px; }
    .console-bar-val { text-align:right;color:#8a837a;font-family:monospace; }
    .console-actions { display:flex;gap:8px;margin-top:12px; }
    .console-actions button { flex:1;border:1px solid #17211f24;background:#fffdf8;border-radius:9px;padding:10px;font-size:11px;font-weight:700;color:var(--ink); }
    .console-actions button.primary { background:var(--ink);color:white;border-color:var(--ink); }
    @media(max-width:520px){ :host{right:12px;bottom:12px}.panel{position:fixed;inset:10px;width:auto;height:auto;border-radius:22px}.launcher{width:58px;height:58px}.panel header{padding-top:18px} }
    @media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
  `;
  root.append(style);

  const launcher = element("button", "launcher", `<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 5.5h14v10H9l-4 3v-13Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M9 10h6M9 13h3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg><span class="pulse"></span>`);
  launcher.type = "button";
  launcher.setAttribute("aria-label", "Open website assistant");
  launcher.addEventListener("click", toggle);
  launcher.style.display = "none";
  root.append(launcher);

  fetch(`${apiBase}/api/public/config?clientKey=${encodeURIComponent(clientKey)}&host=${encodeURIComponent(location.hostname)}`)
    .then((response) => response.ok ? response.json() : Promise.reject(new Error("Assistant unavailable")))
    .then(({ client }) => {
      state.client = client;
      applyTheme(client.theme);
      launcher.style.display = "";
      if (client.engagementMode === "proactive") scheduleProactivePrompt(client.proactiveDelayMs);
    })
    .catch(() => host.remove());

  function scheduleProactivePrompt(delayMs) {
    if (sessionStorage.getItem(declinedKey) === "1") return;
    const delay = Number.isFinite(delayMs) ? delayMs : 2500;
    setTimeout(() => {
      if (state.open || sessionStorage.getItem(declinedKey) === "1") return;
      state.proactive = true;
      toggle();
    }, delay);
  }

  function toggle() {
    state.open = !state.open;
    const existing = root.querySelector(".panel");
    if (existing) existing.remove();
    if (!state.open || !state.client) return;
    window.aiwTrack?.("assistant_open", state.proactive ? "proactive" : "manual");
    const panel = buildPanel();
    root.insertBefore(panel, launcher);
    panel.querySelector("input")?.focus();
  }

  // Phase 2d funnel: the promotion banner and case-study highlight banner
  // (both rendered by analytics-embed.js, a separate script) call this
  // instead of just navigating to #contact, so every path — chat, a
  // promotion click, a highlight click — lands on the exact same lead form,
  // not three different ones. Falls back to nothing (caller still has its
  // own #contact href as a fallback) if the widget hasn't loaded a client yet.
  window.aiwOpenLeadForm = (service) => {
    if (!state.client) return false;
    if (!state.open) toggle();
    const panel = root.querySelector(".panel");
    if (!panel) return false;
    showModuleForm("lead", panel.querySelector(".messages"), panel, service);
    return true;
  };

  function resetConversation() {
    state.sessionId = crypto.randomUUID();
    state.history = [];
    state.proactive = false;
    root.querySelector(".panel")?.remove();
    if (!state.open || !state.client) return;
    const panel = buildPanel();
    root.insertBefore(panel, launcher);
    panel.querySelector("input")?.focus();
  }

  function declineProactive(panel) {
    state.proactive = false;
    sessionStorage.setItem(declinedKey, "1");
    const messages = panel.querySelector(".messages");
    messages.querySelector(".quick")?.remove();
    addMessage(messages, "assistant", "No problem — I’ll stay tucked away. Click the icon anytime if you change your mind.");
    setTimeout(() => { if (state.open) toggle(); }, 1100);
  }

  function buildPanel() {
    const client = state.client;
    const panel = element("section", "panel");
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-label", `${client.businessName} assistant`);
    panel.innerHTML = `<div><header><div class="brand"><div class="mark"></div><div><h2></h2><p class="status">Online · answers from approved business information</p></div></div><button class="console-toggle" aria-label="Site owner console" title="Site owner console">⚙</button><button class="home" aria-label="Start a new conversation">Home</button><button class="close" aria-label="Close assistant">×</button></header>${client.status === "demo" ? '<div class="demo">DEMONSTRATION · no live notifications are sent</div>' : ""}</div><main class="messages" aria-live="polite"></main>`;
    panel.querySelector(".mark").textContent = client.logoText || client.businessName.slice(0, 2);
    panel.querySelector("h2").textContent = client.businessName;
    panel.querySelector(".console-toggle").addEventListener("click", () => openConsoleLogin(panel));
    panel.querySelector(".home").addEventListener("click", resetConversation);
    panel.querySelector(".close").addEventListener("click", toggle);
    const messages = panel.querySelector(".messages");
    addMessage(messages, "assistant", `Hello — I’m the ${client.businessName} assistant. What can I help you find or arrange?`);
    const quick = element("div", "quick");
    if (state.proactive) {
      const yes = element("button", "", "Yes, please"); yes.type = "button";
      yes.addEventListener("click", () => { state.proactive = false; send("Yes, please help me", panel); });
      const no = element("button", "", "No thanks"); no.type = "button";
      no.addEventListener("click", () => declineProactive(panel));
      quick.append(yes, no);
    }
    // Canonical blueprint functions, resolved server-side from this client's
    // pages and enabled modules. A "navigate" action opens the real page; a
    // "prompt" action asks the assistant so it can answer or offer a module.
    for (const action of client.assistantActions || []) quick.append(actionButton(action, panel));
    messages.append(quick);

    // Platform demonstration workflows are not blueprint visitor functions, so
    // they are grouped separately and labelled to avoid confusing a real visitor.
    const demoActions = client.demoActions || [];
    if (demoActions.length) {
      messages.append(textElement("p", "group-label", "Platform demonstration"));
      const demoQuick = element("div", "quick");
      for (const action of demoActions) demoQuick.append(actionButton(action, panel));
      messages.append(demoQuick);
    }
    const form = element("form", "composer", '<input maxlength="2000" aria-label="Your message" placeholder="Ask a question…" autocomplete="off"><button class="send" aria-label="Send message">↑</button>');
    form.addEventListener("submit", (event) => { event.preventDefault(); const input = form.querySelector("input"); const value = input.value.trim(); if (value) { input.value = ""; send(value, panel); } });
    panel.append(form);
    return panel;
  }

  function actionButton(action, panel) {
    const button = element("button", "", action.label);
    button.type = "button";
    button.dataset.blueprint = action.key;
    if (action.type === "navigate" && action.url) {
      button.addEventListener("click", () => {
        if (/^(https?:|tel:|mailto:)/.test(action.url)) window.open(action.url, "_blank", "noopener");
        else location.href = action.url;
      });
    } else {
      button.addEventListener("click", () => send(action.prompt, panel));
    }
    return button;
  }

  // --- Site owner console -----------------------------------------------
  // A hidden, password-gated view reachable from this site's own widget
  // only. Because the widget already knows just its own clientKey, the
  // console can never show another tenant's data - unlike the shared admin
  // panel, no separate per-site login system had to be built for that
  // guarantee. Shows anonymous, aggregated visitor behaviour only.

  function hideComposer(panel) {
    const form = panel.querySelector("form.composer");
    if (form) form.style.display = "none";
  }

  function returnToChat(panel) {
    const fresh = buildPanel();
    panel.replaceWith(fresh);
    fresh.querySelector("input")?.focus();
  }

  function openConsoleLogin(panel, errorMessage) {
    hideComposer(panel);
    const messages = panel.querySelector(".messages");
    messages.replaceChildren();
    const wrap = element("div", "console-login");
    wrap.append(
      textElement("strong", "", "Site owner console"),
      textElement("p", "demo-note", "Enter the console password for this site to see an anonymous summary of visitor activity — no visitor is ever identified.")
    );
    const label = element("label"); label.append(element("span", "", "Console password"));
    const input = document.createElement("input");
    input.type = "password"; input.autocomplete = "off"; input.maxLength = 200;
    label.append(input);
    wrap.append(label);
    const error = element("span", "error");
    if (errorMessage) error.textContent = errorMessage;
    wrap.append(error);
    const submit = element("button", "primary", "Unlock console"); submit.type = "button";
    submit.addEventListener("click", () => submitConsoleLogin(panel, input.value, submit, error));
    input.addEventListener("keydown", (event) => { if (event.key === "Enter") submitConsoleLogin(panel, input.value, submit, error); });
    wrap.append(submit);
    const back = element("button", "console-back", "← Back to chat"); back.type = "button";
    back.addEventListener("click", () => returnToChat(panel));
    wrap.append(back);
    messages.append(wrap);
    input.focus();
  }

  async function submitConsoleLogin(panel, password, submit, error) {
    if (!password) { error.textContent = "Enter the console password."; return; }
    submit.disabled = true; error.textContent = "";
    try {
      const response = await fetch(`${apiBase}/api/public/owner/login`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ clientKey, host: location.hostname, password }) });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || "Incorrect password.");
      state.owner = { token: payload.token, expiresAt: payload.expiresAt };
      renderConsole(panel);
    } catch (failure) {
      error.textContent = failure.message || "Could not connect.";
      submit.disabled = false;
    }
  }

  async function fetchConsoleInsights(filters = {}) {
    const params = new URLSearchParams({ clientKey, host: location.hostname, token: state.owner.token });
    if (filters.from) params.set("from", filters.from);
    if (filters.to) params.set("to", filters.to);
    if (filters.path) params.set("path", filters.path);
    const response = await fetch(`${apiBase}/api/public/owner/insights?${params.toString()}`);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Could not load insights.");
    return payload;
  }

  async function renderConsole(panel) {
    hideComposer(panel);
    const messages = panel.querySelector(".messages");
    messages.replaceChildren(textElement("p", "demo-note", "Loading…"));
    let data;
    try { data = await fetchConsoleInsights(); }
    catch (failure) {
      if (/session|log in/i.test(failure.message || "")) { state.owner = null; openConsoleLogin(panel, failure.message); return; }
      messages.replaceChildren(textElement("span", "error", failure.message)); return;
    }
    drawConsole(panel, data, {});
  }

  function consoleSummaryText(data, filters) {
    if (!filters.from && !filters.to && !filters.path) return "";
    const label = filters.path || "All pages";
    const fromLabel = filters.from ? new Date(filters.from).toLocaleString() : "the earliest record";
    const toLabel = filters.to ? new Date(filters.to).toLocaleString() : "now";
    return `${label}: ${data.pageViews} page view${data.pageViews === 1 ? "" : "s"} between ${fromLabel} and ${toLabel}.`;
  }

  function renderBarList(rows) {
    const el = element("div");
    if (!rows || !rows.length) { el.append(textElement("p", "demo-note", "No data yet.")); return el; }
    const max = rows[0][1] || 1;
    for (const [name, n] of rows) {
      const row = element("div", "console-bar-row");
      row.append(textElement("span", "console-bar-label", name));
      const track = element("div", "console-bar-track");
      const fill = element("div", "console-bar-fill"); fill.style.width = `${Math.round((n / max) * 100)}%`;
      track.append(fill);
      row.append(track, textElement("span", "console-bar-val", String(n)));
      el.append(row);
    }
    return el;
  }

  function drawConsole(panel, data, filters) {
    const messages = panel.querySelector(".messages");
    messages.replaceChildren();
    const wrap = element("div", "console");

    const filterBox = element("div", "console-filter");
    const fromLabel = element("label"); fromLabel.append(element("span", "", "From"));
    const fromInput = document.createElement("input"); fromInput.type = "datetime-local"; fromInput.value = filters.from || "";
    fromLabel.append(fromInput);
    const toLabel = element("label"); toLabel.append(element("span", "", "To"));
    const toInput = document.createElement("input"); toInput.type = "datetime-local"; toInput.value = filters.to || "";
    toLabel.append(toInput);
    const pageLabel = element("label"); pageLabel.append(element("span", "", "Page"));
    const pageSelect = document.createElement("select");
    const allOption = document.createElement("option"); allOption.value = ""; allOption.textContent = "All pages"; pageSelect.append(allOption);
    for (const path of data.paths || []) { const option = document.createElement("option"); option.value = path; option.textContent = path; pageSelect.append(option); }
    pageSelect.value = filters.path || "";
    pageLabel.append(pageSelect);
    filterBox.append(fromLabel, toLabel, pageLabel);
    const filterActions = element("div", "console-filter-actions");
    const apply = element("button", "primary", "Apply"); apply.type = "button";
    const clear = element("button", "", "Clear"); clear.type = "button";
    filterActions.append(apply, clear);
    filterBox.append(filterActions);
    wrap.append(filterBox);

    wrap.append(textElement("p", "console-summary", consoleSummaryText(data, filters)));

    const statGrid = element("div", "console-stats");
    const stats = [
      ["Unique visits", data.uniqueVisits], ["Page views", data.pageViews],
      ["Engaged visits", `${data.engagedVisits} (${data.engagedPct}%)`], ["Enquiries", data.enquiries],
      ["Phone taps", data.phoneTaps], ["Email taps", data.emailTaps],
      ["CTA clicks", data.ctaClicks], ["Assistant opens", data.assistantOpens],
      ["Assistant handoffs", data.assistantHandoffs], ["Avg time on page", `${data.avgDwellSeconds}s`],
      ["Avg scroll depth", `${data.avgScrollPct}%`]
    ];
    for (const [label, value] of stats) {
      const card = element("div", "console-stat");
      card.append(textElement("strong", "", String(value)), textElement("span", "", label));
      statGrid.append(card);
    }
    wrap.append(statGrid);

    wrap.append(textElement("h3", "console-section-h", "Top pages"), renderBarList(data.topPages));
    wrap.append(textElement("h3", "console-section-h", "Event breakdown"), renderBarList(data.eventBreakdown));

    const footerActions = element("div", "console-actions");
    const logout = element("button", "", "Log out"); logout.type = "button";
    const back = element("button", "primary", "Back to chat"); back.type = "button";
    footerActions.append(logout, back);
    wrap.append(footerActions);
    messages.append(wrap);

    apply.addEventListener("click", async () => {
      const newFilters = { from: fromInput.value, to: toInput.value, path: pageSelect.value };
      try { drawConsole(panel, await fetchConsoleInsights(newFilters), newFilters); }
      catch (failure) { if (/session|log in/i.test(failure.message || "")) { state.owner = null; openConsoleLogin(panel, failure.message); } }
    });
    clear.addEventListener("click", async () => {
      try { drawConsole(panel, await fetchConsoleInsights({}), {}); } catch { /* keep current view on transient failure */ }
    });
    logout.addEventListener("click", async () => {
      try { await fetch(`${apiBase}/api/public/owner/logout`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ token: state.owner.token }) }); } catch { /* best effort */ }
      state.owner = null;
      returnToChat(panel);
    });
    back.addEventListener("click", () => returnToChat(panel));
  }

  async function send(message, panel) {
    const isDecline = state.proactive && NEGATIVE_REPLY.test(message.trim());
    state.proactive = false;
    const messages = panel.querySelector(".messages");
    messages.querySelector(".quick")?.remove();
    addMessage(messages, "user", message);
    if (isDecline) { declineProactive(panel); return; }
    const pending = addMessage(messages, "assistant", "Thinking…");
    try {
      const response = await fetch(`${apiBase}/api/public/chat`, { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({ clientKey, host:location.hostname, pageUrl:location.href, sessionId:state.sessionId, message, history:state.history }) });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || "Request failed");
      pending.remove();
      addMessage(messages, "assistant", payload.reply.text, payload.reply.sources);
      if (payload.reply.action?.type === "question-followup") handleQuestionFollowup(message, messages);
      else if (payload.reply.action) addAction(messages, payload.reply.action, panel);
      state.history.push({ role:"user", content:message }, { role:"assistant", content:payload.reply.text });
      state.history = state.history.slice(-8);
    } catch (error) { pending.textContent = error.message || "The assistant is unavailable."; }
  }

  function addMessage(container, role, text, sources = []) {
    const node = element("div", `message ${role}`);
    node.textContent = text;
    if (sources.length) { const source = element("span", "sources", `From: ${sources.map((item) => item.title).join(", ")}`); node.append(source); }
    container.append(node);
    container.scrollTop = container.scrollHeight;
    return node;
  }

  function addAction(container, action, panel) {
    const button = element("button", "action", action.label);
    button.type = "button";
    if (["navigate", "booking", "contact"].includes(action.type)) button.addEventListener("click", () => { if (/^(https?:|tel:|mailto:)/.test(action.url)) window.open(action.url, "_blank", "noopener"); else location.href = action.url; });
    if (["callback", "lead"].includes(action.type)) button.addEventListener("click", () => showModuleForm(action.type, container, panel));
    if (action.type.startsWith("demo-")) button.addEventListener("click", () => showDemoWorkflow(action.type.slice(5), container));
    container.append(button);
  }

  // "No direct answer" fallback. Email is asked at most once per session:
  // - Never asked before: mark asked immediately (so even an ignored prompt
  //   doesn't ask twice), show the email form for this question.
  // - Already have an email: accumulate this question silently, no new UI.
  // - Asked before but no email given: quiet one-line note, no repeat ask.
  function handleQuestionFollowup(question, container) {
    const qa = readQaState();
    if (qa.email) {
      submitQuestionFollowup(qa.email, question).catch(() => {});
      addMessage(container, "assistant", "(Added to what I'll send you.)");
      return;
    }
    if (qa.asked) {
      addMessage(container, "assistant", "(Noted — I don't have an email for you yet, so I can't include this in a reply.)");
      return;
    }
    writeQaState({ asked: true });
    const form = element("form", "module-form qa-followup-form");
    form.innerHTML = `<strong>Get a researched answer by email</strong><input name="email" type="email" required maxlength="160" placeholder="you@example.com"><button>Send me the answer</button><span class="error"></span>`;
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const button = form.querySelector("button"); button.disabled = true;
      const email = new FormData(form).get("email");
      try {
        await submitQuestionFollowup(email, question);
        writeQaState({ email });
        form.replaceChildren(element("strong", "", "Thanks — I'll get a properly researched answer back to you by email."));
      } catch (error) { form.querySelector(".error").textContent = error.message || "Could not submit."; button.disabled = false; }
    });
    container.append(form);
    container.scrollTop = container.scrollHeight;
  }

  async function submitQuestionFollowup(email, question) {
    const response = await fetch(`${apiBase}/api/public/question-followups`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ clientKey, host: location.hostname, sessionId: state.sessionId, email, question })
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Could not submit.");
    return payload;
  }

  function showModuleForm(type, container, _panel, serviceHint) {
    container.querySelector(".module-form")?.remove();
    const form = element("form", "module-form");
    const lead = type === "lead";
    // Phase 2d: a client-specific fixed reason-for-visit taxonomy, in place
    // of the free-text service field, only when the client has one
    // configured — other clients keep the plain text input unchanged.
    // serviceHint (the service the visitor was engaging with when they
    // opened this form — from a promotion/highlight banner) pre-selects the
    // best-guess match via the client's own serviceReasonMap, still fully
    // editable; chat-triggered forms have no hint and fall back to the
    // unselected placeholder, same as before.
    const reasonOptions = lead ? (state.client.leadReasonOptions || []) : [];
    const defaultReason = lead ? state.client.serviceReasonMap?.[serviceHint] : undefined;
    const serviceField = reasonOptions.length
      ? `<select name="reasonForVisit" required>${defaultReason ? "" : '<option value="" disabled selected>Reason for visit</option>'}${reasonOptions.map((option) => `<option value="${option.replace(/"/g, "&quot;")}"${option === defaultReason ? " selected" : ""}>${option.replace(/</g, "&lt;")}</option>`).join("")}</select>`
      : '<input name="service" maxlength="160" placeholder="Service required">';
    form.innerHTML = `<strong>${lead ? "Send an enquiry" : "Request a callback"}</strong><input name="name" required maxlength="120" placeholder="Name"><input name="telephone" required maxlength="40" placeholder="Telephone"><input name="email" type="email" maxlength="160" placeholder="Email (optional)">${lead ? serviceField : '<input name="preferredTime" maxlength="120" placeholder="Preferred callback time">'}<textarea name="reason" maxlength="1000" placeholder="${lead ? "Additional notes" : "Reason for callback"}"></textarea><button>Submit ${state.client.status === "demo" ? "demo" : "request"}</button><span class="error"></span>`;
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const button = form.querySelector("button"); button.disabled = true;
      const values = Object.fromEntries(new FormData(form));
      try {
        const response = await fetch(`${apiBase}/api/public/${lead ? "leads" : "callbacks"}`, { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({ clientKey, host:location.hostname, ...values }) });
        const payload = await response.json(); if (!response.ok) throw new Error(payload.error);
        window.aiwTrack?.("assistant_handoff", lead ? "lead" : "callback");
        form.replaceChildren(element("strong", "", payload.simulated ? "Demo captured — no notification was sent." : "Thank you — the team has your request."));
      } catch (error) { form.querySelector(".error").textContent = error.message || "Could not submit."; button.disabled = false; }
    });
    container.append(form); container.scrollTop = container.scrollHeight;
  }

  function showDemoWorkflow(type, container) {
    container.querySelector(".module-form")?.remove();
    const names = { booking:"Appointment simulation", payment:"Checkout simulation", email:"Email preview", crm:"CRM lead simulation" };
    const config = state.client.demoWorkflows || {};
    const services = config.booking?.services || [];
    const form = element("form", "module-form demo-workflow");
    const head = element("div", "demo-head");
    head.append(element("strong", "", names[type]), element("span", "demo-pill", "DEMO ONLY"));
    form.append(head, element("p", "demo-note", "Uses fictional processing only. No booking, charge, email or CRM update will occur."));

    if (type === "booking") {
      form.append(
        demoInput("Name", "name", { required:true, maxLength:120, placeholder:"Alex Demo" }),
        demoInput("Telephone", "telephone", { required:true, maxLength:40, placeholder:"07000 000000" }),
        demoInput("Email (optional)", "email", { type:"email", maxLength:160, placeholder:"alex@example.com" }),
        demoSelect("Treatment", "service", services.map((item) => item.name)),
        demoSelect("Seeded availability", "slot", config.booking?.slots || [])
      );
    } else if (type === "payment") {
      const service = demoSelect("Treatment", "service", services.map((item) => item.name));
      const price = element("output", "price-preview");
      const updatePrice = () => {
        const selected = services.find((item) => item.name === service.querySelector("select").value);
        price.textContent = `${config.payment?.testCardLabel || "Demo card"} · ${money(selected?.price || 0, config.payment?.currency || "GBP")} · no charge`;
      };
      service.querySelector("select").addEventListener("change", updatePrice); updatePrice();
      form.append(demoInput("Customer name", "customerName", { required:true, maxLength:120, placeholder:"Alex Demo" }), service, price);
    } else if (type === "email") {
      form.append(
        demoInput("Recipient name", "recipientName", { required:true, maxLength:120, placeholder:"Alex Demo" }),
        demoInput("Recipient email", "email", { required:true, type:"email", maxLength:160, placeholder:"alex@example.com" }),
        demoSelect("Subject", "subject", config.email?.subjects || []),
        demoInput("Preview message", "message", { required:true, textarea:true, maxLength:1200, placeholder:"Your appointment details are ready for review." })
      );
    } else {
      form.append(
        demoInput("Lead name", "name", { required:true, maxLength:120, placeholder:"Alex Demo" }),
        demoInput("Telephone", "telephone", { maxLength:40, placeholder:"07000 000000" }),
        demoInput("Email", "email", { type:"email", maxLength:160, placeholder:"alex@example.com" }),
        demoInput("Interest", "interest", { required:true, maxLength:160, placeholder:"Full-body spray tan" }),
        demoSelect("Pipeline stage", "stage", config.crm?.pipelineStages || [])
      );
    }

    const submit = element("button", "", `Run ${names[type].toLowerCase()}`); submit.type = "submit";
    const error = element("span", "error"); form.append(submit, error);
    form.addEventListener("submit", async (event) => {
      event.preventDefault(); submit.disabled = true; error.textContent = "";
      try {
        const response = await fetch(`${apiBase}/api/public/demo/${type}`, { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({ clientKey, host:location.hostname, ...Object.fromEntries(new FormData(form)) }) });
        const payload = await response.json(); if (!response.ok) throw new Error(payload.error || "Simulation failed.");
        form.replaceWith(demoReceipt(type, payload.record));
      } catch (failure) { error.textContent = failure.message || "Simulation failed."; submit.disabled = false; }
    });
    container.append(form); container.scrollTop = container.scrollHeight;
  }

  function demoInput(labelText, name, options = {}) {
    const label = element("label"); label.append(element("span", "", labelText));
    const control = document.createElement(options.textarea ? "textarea" : "input");
    control.name = name; if (options.type) control.type = options.type; if (options.required) control.required = true;
    if (options.maxLength) control.maxLength = options.maxLength; if (options.placeholder) control.placeholder = options.placeholder;
    label.append(control); return label;
  }

  function demoSelect(labelText, name, options) {
    const label = element("label"); label.append(element("span", "", labelText));
    const select = document.createElement("select"); select.name = name; select.required = true;
    for (const value of options) { const option = document.createElement("option"); option.value = value; option.textContent = value; select.append(option); }
    label.append(select); return label;
  }

  function demoReceipt(type, record) {
    const titles = { booking:"Appointment reserved", payment:"Payment approved", email:"Email preview created", crm:"CRM lead created" };
    const details = {
      booking:`${record.service} · ${record.slot} · ${money(record.amount, record.currency)}`,
      payment:`${record.service} · ${money(record.amount, record.currency)} · ${record.cardLabel}`,
      email:`${record.subject} · previewed, not sent`,
      crm:`${record.interest} · ${record.stage}`
    };
    const receipt = element("div", "demo-receipt");
    receipt.append(textElement("span", "demo-pill", "SIMULATED RESULT"), textElement("strong", "", titles[type]), textElement("code", "", record.reference), textElement("span", "", details[type]), textElement("span", "", "No external system was contacted and no real-world action occurred."));
    return receipt;
  }

  function money(value, currency) {
    return new Intl.NumberFormat("en-GB", { style:"currency", currency:currency || "GBP" }).format(Number(value) || 0);
  }

  function applyTheme(theme = {}) { for (const key of ["accent", "ink", "surface"]) if (/^#[0-9a-f]{6}$/i.test(theme[key] || "")) host.style.setProperty(`--${key}`, theme[key]); }
  function textElement(tag, className, value) { const node = element(tag, className); node.textContent = value; return node; }
  function element(tag, className = "", html = "") { const node = document.createElement(tag); if (className) node.className = className; if (html) node.innerHTML = html; return node; }
})();
