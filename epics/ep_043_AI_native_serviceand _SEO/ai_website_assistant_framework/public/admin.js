const MODULES = [
  ["assistant", "AI assistant"], ["faq", "FAQ"], ["navigation", "Navigation"], ["booking", "Booking"],
  ["callback", "Callback"], ["leadCapture", "Lead capture"], ["leadFollowup", "Lead follow-up"], ["contact", "Contact help"],
  ["demoBooking", "Demo booking"], ["demoPayment", "Demo payment"], ["demoEmail", "Demo email"], ["demoCrm", "Demo CRM"]
];
const DEPLOYMENT_STATUSES = ["local", "github", "github+render", "demo", "live"];
const WORKFLOW_STAGES = [
  ["candidate_qualified", "Candidate matches the offer and scope"],
  ["site_and_assistant_checked", "Current site and visible assistant checked"],
  ["public_facts_verified", "Public facts and owner contact route verified"],
  ["assistant_demo_prepared", "Current-site assistant demo prepared"],
  ["github_committed", "Source committed to GitHub"],
  ["hosted_url_verified", "Public hosted URL verified"],
  ["tenant_and_browser_qa", "Tenant, assistant controls, close/reopen and console QA passed"],
  ["outreach_copy_prepared", "Owner-specific outreach copy and reply route prepared"],
  ["ed_send_approval", "Ed approved exact recipient and send"],
  ["outreach_sent", "Outreach sent and logged"],
  ["inbound_outcome_recorded", "Reply / opt-out / next permitted action recorded"]
];
const state = { clients: [], selected: null, records: {}, recordType: "previewResponses" };
const $ = (selector) => document.querySelector(selector);

const tokenInput = $("#admin-token");
tokenInput.value = sessionStorage.getItem("assistant_admin_token") || "change-me-before-live-use";
$("#connect").addEventListener("click", connect);
$("#client-form").addEventListener("submit", saveClient);
$("#duplicate").addEventListener("click", duplicateClient);
$("#new-client").addEventListener("click", createClient);
$("#add-knowledge").addEventListener("click", () => addKnowledgeRow({ title: "", content: "" }));
$("#add-deployment").addEventListener("click", () => addDeploymentRow({}));
document.querySelectorAll("aside nav button").forEach((button) => button.addEventListener("click", () => switchView(button.dataset.view)));
document.querySelectorAll(".activity-filter button").forEach((button) => button.addEventListener("click", () => { state.recordType = button.dataset.type; document.querySelectorAll(".activity-filter button").forEach((item) => item.classList.toggle("active", item === button)); renderActivity(); }));
connect();

async function api(path, options = {}) {
  const response = await fetch(path, { ...options, headers: { "Authorization": `Bearer ${tokenInput.value}`, "Content-Type": "application/json", ...(options.headers || {}) } });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || "Request failed");
  return payload;
}

async function connect() {
  sessionStorage.setItem("assistant_admin_token", tokenInput.value);
  setConnection("Connecting", false);
  try {
    const [{ clients }, { records }] = await Promise.all([api("/api/admin/clients"), api("/api/admin/records")]);
    state.clients = clients; state.records = records;
    $("#client-count").textContent = clients.length;
    $("#activity-count").textContent = Object.values(records).reduce((total, items) => total + items.length, 0);
    renderClients(); renderActivity(); setConnection("Connected", true);
    if (state.selected) selectClient(state.selected.id);
  } catch (error) { setConnection("Authorization required", false); toast(error.message); }
}

function setConnection(label, online) { $("#connection-label").textContent = label; document.querySelector(".connection i").classList.toggle("online", online); }

function renderClients() {
  const list = $("#client-list"); list.replaceChildren();
  for (const client of state.clients) {
    const button = document.createElement("button"); button.className = `client-row${state.selected?.id === client.id ? " active" : ""}`;
    const title = document.createElement("strong"); title.textContent = client.businessName;
    const meta = document.createElement("span"); const dot = document.createElement("i"); dot.className = client.status; meta.append(dot, `${client.status} · ${client.enabledModules.length} modules`);
    button.append(title, meta); button.addEventListener("click", () => selectClient(client.id)); list.append(button);
  }
}

function selectClient(id) {
  const client = state.clients.find((item) => item.id === id); if (!client) return;
  state.selected = structuredClone(client); renderClients();
  $("#empty-state").hidden = true; $("#client-form").hidden = false;
  $("#editor-title").textContent = client.businessName; $("#client-key").textContent = `Public key · ${client.publicKey}`;
  const form = $("#client-form");
  setValue(form, "businessName", client.businessName); setValue(form, "tagline", client.tagline); setValue(form, "allowedHosts", client.allowedHosts.join(", ")); setValue(form, "status", client.status);
  setValue(form, "engagementMode", client.engagementMode || "on_demand"); setValue(form, "proactiveDelayMs", client.proactiveDelayMs ?? 2500);
  setValue(form, "analyticsEnabled", String(client.analyticsEnabled !== false));
  setValue(form, "leadFollowupDelayMs", client.leadFollowupDelayMs ?? 7200000); setValue(form, "averageJobValue", client.averageJobValue ?? 0);
  setValue(form, "logoText", client.logoText); setValue(form, "accent", client.theme?.accent || "#e85d3f"); setValue(form, "ink", client.theme?.ink || "#17211f"); setValue(form, "surface", client.theme?.surface || "#f5f0e7");
  setValue(form, "telephone", client.contact?.telephone); setValue(form, "email", client.contact?.email); setValue(form, "address", client.contact?.address); setValue(form, "openingHours", client.contact?.openingHours);
  setValue(form, "bookingProvider", client.booking?.provider); setValue(form, "bookingUrl", client.booking?.url);
  const moduleGrid = $("#module-grid"); moduleGrid.replaceChildren();
  for (const [key, label] of MODULES) { const wrap = document.createElement("label"); const input = document.createElement("input"); input.type = "checkbox"; input.value = key; input.checked = client.enabledModules.includes(key); input.disabled = key === "assistant"; wrap.append(input, label); moduleGrid.append(wrap); }
  const knowledge = $("#knowledge-list"); knowledge.replaceChildren(); (client.knowledge || []).forEach(addKnowledgeRow);
  const deployments = $("#deployment-list"); deployments.replaceChildren();
  const deploymentEntries = Array.isArray(client.deployments) ? client.deployments : (client.deployment ? [client.deployment] : []);
  if (deploymentEntries.length) deploymentEntries.forEach(addDeploymentRow); else addDeploymentRow({});
  const workflow = client.workflow || {};
  setValue(form, "workflowStatus", workflow.status || "not_started"); setValue(form, "workflowBlocker", workflow.blocker || "");
  renderWorkflowStages(workflow.stages || {});
}

function renderWorkflowStages(stages) {
  const list = $("#workflow-stage-list"); list.replaceChildren();
  for (const [key, label] of WORKFLOW_STAGES) {
    const row = document.createElement("label"); row.className = "workflow-stage";
    const text = document.createElement("span"); text.textContent = label;
    const select = document.createElement("select"); select.dataset.workflowStage = key;
    for (const [value, optionLabel] of [["pending", "Pending"], ["complete", "Complete"], ["not_applicable", "N/A"]]) { const option = document.createElement("option"); option.value = value; option.textContent = optionLabel; option.selected = (stages[key] || "pending") === value; select.append(option); }
    row.append(text, select); list.append(row);
  }
}

function addDeploymentRow(item) {
  const row = document.createElement("div"); row.className = "deployment-row"; row.dataset.id = item.id || `deploy-${crypto.randomUUID().slice(0, 6)}`;
  const topGrid = document.createElement("div"); topGrid.className = "grid";
  const labelField = document.createElement("label"); labelField.textContent = "Instance label";
  const labelInput = document.createElement("input"); labelInput.className = "deploy-label"; labelInput.placeholder = "Redesigned site + AI"; labelInput.value = item.label || ""; labelInput.maxLength = 80;
  labelField.append(labelInput);
  const statusField = document.createElement("label"); statusField.textContent = "Workflow status";
  const statusSelect = document.createElement("select"); statusSelect.className = "deploy-status";
  for (const status of DEPLOYMENT_STATUSES) { const option = document.createElement("option"); option.value = status; option.textContent = status; if ((item.status || "local") === status) option.selected = true; statusSelect.append(option); }
  statusField.append(statusSelect);
  topGrid.append(labelField, statusField);

  const bottomGrid = document.createElement("div"); bottomGrid.className = "grid wide";
  const locField = document.createElement("label"); locField.textContent = "App location";
  const locInput = document.createElement("input"); locInput.className = "deploy-location"; locInput.placeholder = "epics/ep_044_web_apps/funcut_redesigned/"; locInput.value = item.appLocation || "";
  locField.append(locInput);
  const urlField = document.createElement("label"); urlField.textContent = "Hosted URL";
  const urlInput = document.createElement("input"); urlInput.className = "deploy-url"; urlInput.type = "url"; urlInput.placeholder = "https://edebell67.github.io/epics/..."; urlInput.value = item.hostedUrl || "";
  urlField.append(urlInput);
  bottomGrid.append(locField, urlField);

  const remove = document.createElement("button"); remove.type = "button"; remove.className = "remove-deployment"; remove.textContent = "×"; remove.setAttribute("aria-label", "Remove deployment instance"); remove.addEventListener("click", () => row.remove());

  row.append(remove, topGrid, bottomGrid); $("#deployment-list").append(row);
}

function addKnowledgeRow(item) {
  const row = document.createElement("div"); row.className = "knowledge-row"; row.dataset.id = item.id || `knowledge-${crypto.randomUUID().slice(0, 6)}`;
  const title = document.createElement("input"); title.placeholder = "Topic"; title.value = item.title || ""; title.maxLength = 120;
  const content = document.createElement("textarea"); content.placeholder = "Approved business information"; content.value = item.content || ""; content.maxLength = 3000;
  const remove = document.createElement("button"); remove.type = "button"; remove.textContent = "×"; remove.setAttribute("aria-label", "Remove knowledge entry"); remove.addEventListener("click", () => row.remove());
  row.append(title, content, remove); $("#knowledge-list").append(row);
}

async function saveClient(event) {
  event.preventDefault(); if (!state.selected) return;
  const form = new FormData(event.currentTarget);
  const enabledModules = [...document.querySelectorAll("#module-grid input:checked")].map((input) => input.value);
  const knowledge = [...document.querySelectorAll(".knowledge-row")].map((row) => ({ id: row.dataset.id, title: row.querySelector("input").value.trim(), content: row.querySelector("textarea").value.trim() })).filter((item) => item.title && item.content);
  const deployments = [...document.querySelectorAll(".deployment-row")].map((row) => ({
    id: row.dataset.id,
    label: row.querySelector(".deploy-label").value.trim(),
    status: row.querySelector(".deploy-status").value,
    appLocation: row.querySelector(".deploy-location").value.trim(),
    hostedUrl: row.querySelector(".deploy-url").value.trim()
  })).filter((item) => item.label || item.appLocation || item.hostedUrl);
  const patch = {
    businessName: form.get("businessName"), tagline: form.get("tagline"), status: form.get("status"), logoText: form.get("logoText"),
    engagementMode: form.get("engagementMode"), proactiveDelayMs: Number(form.get("proactiveDelayMs")) || 2500,
    analyticsEnabled: form.get("analyticsEnabled") !== "false",
    leadFollowupDelayMs: Number(form.get("leadFollowupDelayMs")) || 7200000, averageJobValue: Number(form.get("averageJobValue")) || 0,
    allowedHosts: form.get("allowedHosts").split(",").map((item) => item.trim()).filter(Boolean), enabledModules, knowledge, deployments,
    theme: { accent: form.get("accent"), ink: form.get("ink"), surface: form.get("surface") },
    contact: { ...state.selected.contact, telephone: form.get("telephone"), email: form.get("email"), address: form.get("address"), openingHours: form.get("openingHours") },
    booking: { provider: form.get("bookingProvider"), url: form.get("bookingUrl") }
  };
  try { const { client } = await api(`/api/admin/clients/${encodeURIComponent(state.selected.id)}`, { method:"PUT", body:JSON.stringify(patch) }); const index = state.clients.findIndex((item) => item.id === client.id); state.clients[index] = client; state.selected = client; selectClient(client.id); toast("Client profile saved"); }
  catch (error) { toast(error.message); }
}

async function duplicateClient() {
  if (!state.selected) return;
  try { const { client } = await api(`/api/admin/clients/${encodeURIComponent(state.selected.id)}/duplicate`, { method:"POST" }); state.clients.push(client); $("#client-count").textContent = state.clients.length; selectClient(client.id); toast("Demo copy created"); }
  catch (error) { toast(error.message); }
}

async function createClient() {
  const businessName = prompt("Business name"); if (!businessName) return;
  try {
    const { client } = await api("/api/admin/clients", { method:"POST", body:JSON.stringify({ businessName, status:"demo", allowedHosts:["localhost"], logoText:businessName.slice(0,2).toUpperCase(), theme:{ accent:"#e85d3f", ink:"#17211f", surface:"#f5f0e7" }, contact:{}, booking:{}, deployment:{}, enabledModules:["assistant","faq","contact"], pages:[], knowledge:[], notificationDestinations:[] }) });
    state.clients.push(client); $("#client-count").textContent = state.clients.length; selectClient(client.id); toast("Client profile created");
  } catch (error) { toast(error.message); }
}

function switchView(view) {
  $("#clients-view").hidden = view !== "clients"; $("#activity-view").hidden = view !== "activity"; $("#roi-view").hidden = view !== "roi"; $("#insights-view").hidden = view !== "insights";
  $("#view-title").textContent = view === "clients" ? "Client profiles" : view === "activity" ? "Activity" : view === "insights" ? "Visitor insights" : "Lead ROI";
  document.querySelectorAll("aside nav button").forEach((button) => button.classList.toggle("nav-active", button.dataset.view === view));
  if (view === "roi") renderRoiClientPicker();
  if (view === "insights") renderInsightsPicker();
}

function renderInsightsPicker() {
  const select = $("#insights-client-select");
  const current = select.value;
  select.replaceChildren();
  for (const client of state.clients) { const option = document.createElement("option"); option.value = client.id; option.textContent = client.businessName; select.append(option); }
  if (current) select.value = current;
  select.onchange = () => { populateInsightsPageFilter(); renderInsights(); };
  $("#insights-from").onchange = renderInsights;
  $("#insights-to").onchange = renderInsights;
  $("#insights-page-filter").onchange = renderInsights;
  $("#insights-clear-filter").onclick = () => {
    $("#insights-from").value = ""; $("#insights-to").value = ""; $("#insights-page-filter").value = "";
    renderInsights();
  };
  if (select.value) { populateInsightsPageFilter(); renderInsights(); }
}

function populateInsightsPageFilter() {
  const clientId = $("#insights-client-select").value;
  const paths = [...new Set((state.records.events || [])
    .filter((e) => e.clientId === clientId && e.type === "pageview" && e.path)
    .map((e) => e.path))].sort();
  const select = $("#insights-page-filter");
  const current = select.value;
  select.replaceChildren();
  const all = document.createElement("option"); all.value = ""; all.textContent = "All pages"; select.append(all);
  for (const path of paths) { const option = document.createElement("option"); option.value = path; option.textContent = path; select.append(option); }
  if (paths.includes(current)) select.value = current;
}

function renderInsights() {
  const clientId = $("#insights-client-select").value;
  const fromValue = $("#insights-from").value;   // "" or "YYYY-MM-DDTHH:mm" (local time)
  const toValue = $("#insights-to").value;
  const pageFilter = $("#insights-page-filter").value;
  const fromMs = fromValue ? new Date(fromValue).getTime() : null;
  const toMs = toValue ? new Date(toValue).getTime() : null;
  const inRange = (record) => {
    const t = new Date(record.createdAt).getTime();
    if (fromMs !== null && t < fromMs) return false;
    if (toMs !== null && t > toMs) return false;
    return true;
  };

  let events = (state.records.events || []).filter((e) => e.clientId === clientId).filter(inRange);
  if (pageFilter) events = events.filter((e) => e.path === pageFilter);
  const enquiries = [...(state.records.leads || []), ...(state.records.callbacks || [])].filter((r) => r.clientId === clientId).filter(inRange);

  const summary = $("#insights-filter-summary");
  if (pageFilter || fromValue || toValue) {
    const views = events.filter((e) => e.type === "pageview").length;
    const label = pageFilter || "All pages";
    const fromLabel = fromValue ? new Date(fromValue).toLocaleString() : "the earliest record";
    const toLabel = toValue ? new Date(toValue).toLocaleString() : "now";
    summary.textContent = `${label}: ${views} page view${views === 1 ? "" : "s"} between ${fromLabel} and ${toLabel}.`;
  } else {
    summary.textContent = "";
  }

  const sessions = new Set(events.map((e) => e.sessionId).filter(Boolean));
  const pageviews = events.filter((e) => e.type === "pageview").length;
  const engagedTypes = new Set(["cta_click", "phone_click", "email_click", "whatsapp_click", "form_start", "form_submit", "assistant_open", "gallery_open"]);
  const engagedSessions = new Set(events.filter((e) => engagedTypes.has(e.type) || (e.type === "scroll_depth" && Number(e.scrollPct) >= 50)).map((e) => e.sessionId));
  const count = (t) => events.filter((e) => e.type === t).length;
  const exits = events.filter((e) => e.type === "page_exit");
  const avg = (arr, key) => arr.length ? Math.round(arr.reduce((s, e) => s + (Number(e[key]) || 0), 0) / arr.length) : 0;

  const sess = sessions.size || 0;
  const stats = [
    ["Unique visits", sess],
    ["Page views", pageviews],
    ["Engaged visits", `${engagedSessions.size}${sess ? ` (${Math.round(engagedSessions.size / sess * 100)}%)` : ""}`],
    ["Enquiries", enquiries.length],
    ["Phone taps", count("phone_click")],
    ["Email taps", count("email_click")],
    ["CTA clicks", count("cta_click")],
    ["Assistant opens", count("assistant_open")],
    ["Assistant handoffs", count("assistant_handoff")],
    ["Avg time on page", `${Math.round(avg(exits, "dwellMs") / 1000)}s`],
    ["Avg scroll depth", `${avg(exits, "scrollPct")}%`]
  ];
  const grid = $("#insights-stats"); grid.replaceChildren();
  stats.forEach(([label, value], index) => {
    const card = document.createElement("div"); card.className = `roi-stat${index === 3 ? " highlight" : ""}`;
    const v = document.createElement("strong"); v.textContent = value;
    const l = document.createElement("span"); l.textContent = label;
    card.append(v, l); grid.append(card);
  });

  const topN = (key, type) => {
    const counts = {};
    for (const e of events) { if (type && e.type !== type) continue; const k = e[key] || "—"; counts[k] = (counts[k] || 0) + 1; }
    return Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 10);
  };
  const renderBars = (target, rows) => {
    const el = $(target); el.replaceChildren();
    if (!rows.length) { const p = document.createElement("p"); p.className = "notice"; p.textContent = "No data yet."; el.append(p); return; }
    const max = rows[0][1] || 1;
    for (const [name, n] of rows) {
      const row = document.createElement("div"); row.className = "insights-bar";
      const label = document.createElement("span"); label.className = "insights-bar-label"; label.textContent = name;
      const track = document.createElement("div"); track.className = "insights-bar-track"; const fill = document.createElement("div"); fill.className = "insights-bar-fill"; fill.style.width = `${Math.round(n / max * 100)}%`; track.append(fill);
      const val = document.createElement("span"); val.className = "insights-bar-val"; val.textContent = n;
      row.append(label, track, val); el.append(row);
    }
  };
  renderBars("#insights-pages", topN("path", "pageview"));
  renderBars("#insights-events", topN("type"));
}

function renderRoiClientPicker() {
  const select = $("#roi-client-select");
  const previous = select.value;
  select.replaceChildren();
  for (const client of state.clients) { const option = document.createElement("option"); option.value = client.id; option.textContent = client.businessName; select.append(option); }
  select.value = state.clients.some((item) => item.id === previous) ? previous : (state.clients[0]?.id || "");
  select.onchange = renderRoi;
  if (select.value) renderRoi();
}

async function renderRoi() {
  const clientId = $("#roi-client-select").value;
  if (!clientId) return;
  let roi, records;
  try { [roi, records] = await Promise.all([api(`/api/admin/roi?clientId=${encodeURIComponent(clientId)}`), api("/api/admin/records")]); }
  catch (error) { toast(error.message); return; }
  state.records = records.records;
  const stats = $("#roi-stats"); stats.replaceChildren();
  const cards = [
    ["Leads captured", roi.totalLeads],
    ["Follow-ups sent", roi.followupsSent],
    ["Converted (same session)", roi.convertedSameSession],
    ["Converted after follow-up", roi.convertedAfterFollowup],
    ["Follow-up recovery rate", `${Math.round(roi.recoveryRate * 100)}%`],
    ["Estimated recovered revenue", `£${roi.estimatedRecoveredRevenue.toLocaleString()}`]
  ];
  cards.forEach(([label, value], index) => {
    const card = document.createElement("div"); card.className = `roi-stat${index === cards.length - 1 ? " highlight" : ""}`;
    const span = document.createElement("span"); span.textContent = label;
    const strong = document.createElement("strong"); strong.textContent = value;
    card.append(span, strong); stats.append(card);
  });

  const leads = (state.records.leads || []).filter((item) => item.clientId === clientId);
  const list = $("#roi-leads"); list.replaceChildren();
  if (!leads.length) { const empty = document.createElement("p"); empty.className = "notice"; empty.textContent = "No leads captured yet."; list.append(empty); return; }
  for (const lead of leads) {
    const row = document.createElement("div"); row.className = "roi-lead-row";
    const time = document.createElement("time"); time.textContent = new Date(lead.createdAt).toLocaleString();
    const name = document.createElement("span"); name.textContent = [lead.name, lead.service].filter(Boolean).join(" · ") || "—";
    const followup = document.createElement("span"); followup.textContent = lead.followupStatus === "sent" ? "Follow-up sent" : lead.followupStatus === "scheduled" ? "Follow-up scheduled" : "No follow-up";
    const action = document.createElement("button"); action.type = "button";
    if (lead.convertedAt) { action.textContent = `Converted (${lead.convertedVia === "after_followup" ? "recovered" : "same session"})`; action.disabled = true; }
    else { action.textContent = "Mark converted"; action.addEventListener("click", async () => { try { await api(`/api/admin/leads/${encodeURIComponent(lead.id)}/convert`, { method: "POST" }); await connect(); renderRoi(); toast("Lead marked converted"); } catch (error) { toast(error.message); } }); }
    row.append(time, name, followup, action); list.append(row);
  }
}

function renderActivity() {
  const table = $("#activity-table"); table.replaceChildren(); const records = state.records[state.recordType] || [];
  if (!records.length) { const empty = document.createElement("p"); empty.className = "notice"; empty.textContent = `No ${state.recordType} have been recorded.`; table.append(empty); return; }
  for (const record of records) {
    const row = document.createElement("div"); row.className = "record";
    const time = document.createElement("time"); time.textContent = new Date(record.createdAt).toLocaleString();
    const client = document.createElement("strong"); client.textContent = state.clients.find((item) => item.id === record.clientId)?.businessName || record.clientId;
    const eventDetail = record.type ? [record.type, record.label, record.path, record.device].filter(Boolean).join(" · ") : "";
    const detail = document.createElement("div"); detail.textContent = eventDetail || [record.summary, record.reference, record.message || record.reason || record.service || record.subject || record.interest || record.name].filter(Boolean).join(" · ") || "—";
    const mode = document.createElement("span"); mode.textContent = record.simulated || record.mode === "demo" ? "Demo" : "Live";
    row.append(time, client, detail, mode); table.append(row);
  }
}

function setValue(form, name, value = "") { form.elements[name].value = value || ""; }
function toast(message) { document.querySelector(".toast")?.remove(); const node = document.createElement("div"); node.className = "toast"; node.textContent = message; document.body.append(node); setTimeout(() => node.remove(), 2600); }
