(() => {
  const script = document.currentScript;
  const clientKey = script?.dataset.client;
  const apiBase = (script?.dataset.apiBase || new URL(script.src).origin).replace(/\/$/, "");
  const autoOpen = script?.dataset.autoOpen === "true";
  if (!clientKey || document.querySelector("ai-website-assistant")) return;

  const host = document.createElement("ai-website-assistant");
  const root = host.attachShadow({ mode: "open" });
  document.body.append(host);
  const state = { client: null, open: false, sessionId: crypto.randomUUID(), history: [], ownerDashboardUrl: "" };

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
    header { background:var(--ink);color:white;padding:18px 18px 15px;position:relative;overflow:hidden; }
    header:after { content:"";position:absolute;width:130px;height:130px;border:1px solid #ffffff2b;border-radius:50%;right:-45px;top:-72px;pointer-events:none; }
    .brand { display:flex;gap:10px;align-items:flex-start;padding-right:151px;min-width:0; }
    .mark { width:40px;height:40px;flex:0 0 40px;border-radius:12px;background:var(--accent);display:grid;place-items:center;font-family:Georgia,serif;font-weight:700;letter-spacing:-1px; }
    .brand > div:last-child { min-width:0; }
    h2 { margin:0;font:700 15px/1.15 Georgia,serif;letter-spacing:-.2px;overflow-wrap:anywhere; }
    .status { margin:4px 0 0;font-size:10px;line-height:1.35;color:#d8dfdc;letter-spacing:.03em; }
    .functions { position:absolute;right:127px;top:14px;border:1px solid #ffffff42;border-radius:999px;background:#ffffff12;color:white;padding:7px 9px;font-size:10px;font-weight:700; }
    .functions:hover { background:#ffffff2b; }
    .home { position:absolute;right:54px;top:14px;border:1px solid #ffffff42;border-radius:999px;background:#ffffff12;color:white;padding:7px 10px;font-size:10px;font-weight:700; }
    .home:hover { background:#ffffff2b; }
    .close { position:absolute;right:14px;top:14px;width:32px;height:32px;border:0;border-radius:50%;background:#ffffff12;color:white;font-size:22px;line-height:1; }
    .owner-access { margin:10px 0 0;border:1px solid #ffffff42;border-radius:999px;background:#ffffff12;color:white;padding:7px 10px;font-size:10px;font-weight:800; }
    .owner-access.dashboard { background:var(--accent);border-color:var(--accent); }
    .owner-access:hover { background:#ffffff2b; }
    .owner-access.dashboard:hover { background:color-mix(in srgb,var(--accent),#000 14%); }
    .demo { background:#f8d89a;color:#533c16;padding:7px 18px;font-size:11px;font-weight:700;letter-spacing:.04em; }
    .messages { padding:19px 17px 12px;overflow-y:auto;scroll-behavior:smooth;background:linear-gradient(#fffdf8,#fbf7ef); }
    .message { max-width:88%;padding:12px 14px;margin:0 0 11px;border-radius:17px;font-size:13px;line-height:1.55;animation:message .23s ease both;white-space:pre-wrap; }
    @keyframes message { from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:none} }
    .assistant { background:#ece8de;border-bottom-left-radius:5px; }
    .user { margin-left:auto;background:var(--accent);color:white;border-bottom-right-radius:5px; }
    .sources { font-size:10px;display:block;margin-top:7px;opacity:.66; }
    .action { border:1px solid var(--ink);background:transparent;color:var(--ink);padding:9px 12px;border-radius:999px;margin:0 6px 11px 0;font-size:11px;font-weight:700;transition:.18s; }
    .action:hover { background:var(--ink);color:white; }
    .quick { display:flex;flex-wrap:wrap;gap:7px;overflow:visible;padding:0 0 10px; }
    .quick button { white-space:nowrap;border:1px solid #17211f24;background:#fffdf8;border-radius:999px;padding:8px 10px;font-size:10px;color:var(--ink); }
    .function-catalog { margin:0 0 12px;border:1px solid #17211f1b;border-radius:16px;background:white;overflow:hidden; }
    .function-catalog header { padding:12px 13px;background:#f2eee5;color:var(--ink);display:flex;justify-content:space-between;align-items:center; }
    .function-catalog header strong { font:700 14px Georgia,serif; }
    .function-catalog header button { border:0;background:transparent;color:var(--ink);font-size:16px;line-height:1; }
    .function-note { padding:9px 13px 3px;margin:0;color:#70695f;font-size:10px;line-height:1.45; }
    .function-row { display:grid;grid-template-columns:1fr auto;gap:8px;padding:9px 13px;border-top:1px solid #17211f10; }
    .function-row strong { display:block;font-size:11px; }
    .function-row span { display:block;margin-top:2px;color:#70695f;font-size:10px;line-height:1.35; }
    .function-state { align-self:start;border-radius:999px;padding:4px 6px;background:#f0ece3;color:#70695f;font-size:8px!important;font-weight:800;letter-spacing:.04em;text-transform:uppercase;white-space:nowrap; }
    .function-state.enabled { background:#e1f0e3;color:#356541; }
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
    @media(max-width:520px){ :host{right:12px;bottom:12px}.panel{position:fixed;inset:10px;width:auto;height:auto;border-radius:22px}.launcher{width:58px;height:58px}.panel header{padding-top:18px} }
    @media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
  `;
  root.append(style);

  const launcher = element("button", "launcher", `<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 5.5h14v10H9l-4 3v-13Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M9 10h6M9 13h3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg><span class="pulse"></span>`);
  launcher.type = "button";
  launcher.setAttribute("aria-label", "Open website assistant");
  launcher.addEventListener("click", toggle);
  root.append(launcher);

  fetch(`${apiBase}/api/public/config?clientKey=${encodeURIComponent(clientKey)}&host=${encodeURIComponent(location.hostname)}`)
    .then((response) => response.ok ? response.json() : Promise.reject(new Error("Assistant unavailable")))
    .then(({ client }) => {
      state.client = client;
      applyTheme(client.theme);
      if (autoOpen) toggle();
    })
    .catch(() => { launcher.disabled = true; launcher.title = "Assistant unavailable for this website"; });

  function toggle() {
    state.open = !state.open;
    const existing = root.querySelector(".panel");
    if (existing) existing.remove();
    if (!state.open || !state.client) return;
    const panel = buildPanel();
    root.insertBefore(panel, launcher);
    panel.querySelector("input")?.focus();
  }

  function resetConversation() {
    state.sessionId = crypto.randomUUID();
    state.history = [];
    root.querySelector(".panel")?.remove();
    if (!state.open || !state.client) return;
    const panel = buildPanel();
    root.insertBefore(panel, launcher);
    panel.querySelector("input")?.focus();
  }

  function showFunctionCatalog(panel) {
    const messages = panel.querySelector(".messages");
    messages.querySelector(".function-catalog")?.remove();
    const enabled = new Set(state.client.enabledModules || []);
    const catalog = element("section", "function-catalog");
    catalog.setAttribute("aria-label", "Assistant function catalogue");
    const head = element("header");
    const close = element("button", "", "×"); close.type = "button"; close.setAttribute("aria-label", "Close function catalogue");
    close.addEventListener("click", () => catalog.remove());
    head.append(element("strong", "", "Assistant functions"), close);
    catalog.append(head, element("p", "function-note", "This shows the complete product capability set. Only items marked Available are enabled for this tenant."));
    const capabilities = [
      ["faq", "FAQ", "Answers from the approved knowledge base"],
      ["navigation", "Navigation", "Finds and links to a matching page on the site"],
      ["booking", "Booking", "Links out to a configured booking provider"],
      ["callback", "Callback", "Collects callback details and submits a request"],
      ["leadCapture", "Lead capture", "Collects an enquiry and contact details"],
      ["contact", "Contact help", "Surfaces approved contact details with an appropriate action"],
      ["demoBooking", "Demo booking", "Simulated appointment flow with a fictional receipt"],
      ["demoPayment", "Demo payment", "Simulated checkout — no real charge"],
      ["demoEmail", "Demo email", "Simulated email preview — never sent"],
      ["demoCrm", "Demo CRM", "Simulated CRM lead creation"]
    ];
    for (const [key, label, description] of capabilities) {
      const row = element("div", "function-row");
      const detail = element("div"); detail.append(element("strong", "", label), element("span", "", description));
      const stateNode = element("span", `function-state${enabled.has(key) ? " enabled" : ""}`, enabled.has(key) ? "Available" : "Not enabled");
      row.append(detail, stateNode); catalog.append(row);
    }
    messages.append(catalog); messages.scrollTop = messages.scrollHeight;
  }

  function showOwnerSignIn(panel) {
    const messages = panel.querySelector(".messages");
    messages.querySelector(".owner-sign-in")?.remove();
    const form = element("form", "module-form owner-sign-in", '<strong>Owner dashboard sign in</strong><p class="demo-note">Private owner access only. Your password is checked securely and is never placed in this website’s source or URL.</p><input name="password" type="password" required autocomplete="current-password" placeholder="Owner Console Password"><button>Verify and show dashboard</button><span class="error"></span>');
    form.addEventListener("submit", async (event) => {
      event.preventDefault(); const password = form.password.value;
      const error = form.querySelector(".error"); const submit = form.querySelector("button"); error.textContent = ""; submit.disabled = true; submit.textContent = "Checking…";
      try {
        const response = await fetch(`${apiBase}/api/public/owner-dashboard-access`, { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({ clientKey, host:location.hostname, password }) });
        const payload = await response.json(); if (!response.ok) throw new Error(payload.error || "Owner access was not accepted.");
        state.ownerDashboardUrl = payload.dashboardUrl; root.querySelector(".panel")?.remove(); root.insertBefore(buildPanel(), launcher);
      } catch (errorValue) { error.textContent = errorValue.message || "Owner access was not accepted."; submit.disabled = false; submit.textContent = "Verify and show dashboard"; form.password.value = ""; }
    });
    messages.append(form); messages.scrollTop = messages.scrollHeight; form.password.focus();
  }

  function buildPanel() {
    const client = state.client;
    const panel = element("section", "panel");
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-label", `${client.businessName} assistant`);
    panel.innerHTML = `<div><header><div class="brand"><div class="mark"></div><div><h2></h2><p class="status">Online · answers from approved business information</p></div></div><button class="owner-access" aria-label="Owner dashboard sign in">Owner sign in</button><button class="functions" aria-label="Show assistant functions">Functions</button><button class="home" aria-label="Start a new conversation">Home</button><button class="close" aria-label="Close assistant">×</button></header>${client.status === "demo" ? '<div class="demo">DEMONSTRATION · no live notifications are sent</div>' : ""}</div><main class="messages" aria-live="polite"></main>`;
    panel.querySelector(".mark").textContent = client.logoText || client.businessName.slice(0, 2);
    panel.querySelector("h2").textContent = client.businessName;
    panel.querySelector(".home").addEventListener("click", resetConversation);
    const ownerAccess = panel.querySelector(".owner-access");
    if (state.ownerDashboardUrl) {
      ownerAccess.classList.add("dashboard"); ownerAccess.textContent = "Open owner dashboard ↗"; ownerAccess.setAttribute("aria-label", "Open owner dashboard");
      ownerAccess.addEventListener("click", () => window.open(`${apiBase}${state.ownerDashboardUrl}`, "_blank", "noopener"));
    } else ownerAccess.addEventListener("click", () => showOwnerSignIn(panel));
    panel.querySelector(".functions").addEventListener("click", () => showFunctionCatalog(panel));
    panel.querySelector(".close").addEventListener("click", toggle);
    const messages = panel.querySelector(".messages");
    addMessage(messages, "assistant", `Hello — I’m the ${client.businessName} assistant. What can I help you find or arrange?`);
    const quick = element("div", "quick");
    const choices = [
      ["Services", "What services do you provide?"], ["Opening hours", "What are your opening hours?"],
      ["Contact", "How can I contact you?"], ["Find information", "Where can I find more information on the website?"],
      ...(client.enabledModules.includes("demoBooking") ? [["Demo booking", "Show the demo booking flow"]] : client.enabledModules.includes("booking") ? [["Book", "I would like to book an appointment"]] : []),
      ...(client.enabledModules.includes("demoPayment") ? [["Demo payment", "Show the demo payment checkout"]] : []),
      ...(client.enabledModules.includes("demoEmail") ? [["Demo email", "Preview a demo email"]] : []),
      ...(client.enabledModules.includes("demoCrm") ? [["Demo CRM", "Create a demo CRM lead"]] : []),
      ...(client.enabledModules.includes("callback") ? [["Callback", "Please call me back"]] : []),
      ...(client.enabledModules.includes("leadCapture") ? [["Send enquiry", "I would like to send an enquiry"]] : [])
    ];
    for (const [label, prompt] of choices) { const button = element("button", "", label); button.type = "button"; button.addEventListener("click", () => send(prompt, panel)); quick.append(button); }
    messages.append(quick);
    const form = element("form", "composer", '<input maxlength="2000" aria-label="Your message" placeholder="Ask a question…" autocomplete="off"><button class="send" aria-label="Send message">↑</button>');
    form.addEventListener("submit", (event) => { event.preventDefault(); const input = form.querySelector("input"); const value = input.value.trim(); if (value) { input.value = ""; send(value, panel); } });
    panel.append(form);
    return panel;
  }

  async function send(message, panel) {
    const messages = panel.querySelector(".messages");
    messages.querySelector(".quick")?.remove();
    addMessage(messages, "user", message);
    const pending = addMessage(messages, "assistant", "Thinking…");
    try {
      const response = await fetch(`${apiBase}/api/public/chat`, { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({ clientKey, host:location.hostname, pageUrl:location.href, sessionId:state.sessionId, message, history:state.history }) });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || "Request failed");
      pending.remove();
      addMessage(messages, "assistant", payload.reply.text, payload.reply.sources);
      if (payload.reply.action) addAction(messages, payload.reply.action, panel);
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

  function showModuleForm(type, container) {
    container.querySelector(".module-form")?.remove();
    const form = element("form", "module-form");
    const lead = type === "lead";
    form.innerHTML = `<strong>${lead ? "Send an enquiry" : "Request a callback"}</strong><input name="name" required maxlength="120" placeholder="Name"><input name="telephone" required maxlength="40" placeholder="Telephone"><input name="email" type="email" maxlength="160" placeholder="Email (optional)">${lead ? '<input name="service" maxlength="160" placeholder="Service required">' : '<input name="preferredTime" maxlength="120" placeholder="Preferred callback time">'}<textarea name="reason" maxlength="1000" placeholder="${lead ? "Additional notes" : "Reason for callback"}"></textarea><button>Submit ${state.client.status === "demo" ? "demo" : "request"}</button><span class="error"></span>`;
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const button = form.querySelector("button"); button.disabled = true;
      const values = Object.fromEntries(new FormData(form));
      try {
        const response = await fetch(`${apiBase}/api/public/${lead ? "leads" : "callbacks"}`, { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({ clientKey, host:location.hostname, ...values }) });
        const payload = await response.json(); if (!response.ok) throw new Error(payload.error);
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
