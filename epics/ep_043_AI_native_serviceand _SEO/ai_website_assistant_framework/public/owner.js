const tenant = new URLSearchParams(location.search).get("tenant") || "";
const key = tenant ? `owner_console_code:${tenant}` : "";
const state = { data: null, code: sessionStorage.getItem(key) || "" };
const $ = (selector) => document.querySelector(selector);

$("#access-code").value = state.code;
$("#access-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  state.code = $("#access-code").value.trim();
  await loadActivity();
});
$("#export-csv").addEventListener("click", exportCsv);
if (!tenant) $("#access-error").textContent = "This owner link is incomplete. Ask for a new private review link.";
else if (state.code) loadActivity();

async function loadActivity() {
  $("#access-error").textContent = "";
  try {
    const response = await fetch(`/api/owner/activity?tenant=${encodeURIComponent(tenant)}`, { headers: { Authorization: `Bearer ${state.code}` } });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Could not open owner activity.");
    state.data = payload;
    sessionStorage.setItem(key, state.code);
    render();
  } catch (error) {
    sessionStorage.removeItem(key);
    $("#access-error").textContent = error.message;
  }
}

function render() {
  const { owner, summary } = state.data;
  $("#business-name").textContent = `${owner.businessName} activity`;
  $("#subtitle").textContent = "Private assistant review — visitor questions, actions and follow-up signals.";
  $("#mode").textContent = owner.status === "demo" ? "Demo mode" : "Live mode";
  $("#demo-note").hidden = owner.status !== "demo";
  renderPerformance(state.data.performance);
  renderOpportunityIntelligence();
  $("#access-card").hidden = true;
  $("#console").hidden = false;
  const metrics = [["conversations", "Conversations"], ["leads", "Enquiries"], ["callbacks", "Callbacks"], ["bookings", "Bookings"], ["payments", "Payments"], ["emails", "Email previews"], ["crmLeads", "CRM activity"], ["previewResponses", "Preview responses"]];
  const summaryNode = $("#summary"); summaryNode.replaceChildren();
  for (const [type, label] of metrics) { const card = document.createElement("article"); card.className = "metric"; const value = document.createElement("strong"); value.textContent = summary[type] || 0; const text = document.createElement("span"); text.textContent = label; card.append(value, text); summaryNode.append(card); }
  const records = Object.entries(state.data.records).flatMap(([type, entries]) => entries.map((entry) => ({ type, ...entry }))).sort((a, b) => String(b.createdAt).localeCompare(String(a.createdAt)));
  const activity = $("#activity"); activity.replaceChildren();
  if (!records.length) { const empty = document.createElement("p"); empty.className = "empty"; empty.textContent = "No visitor activity has been recorded yet."; activity.append(empty); return; }
  for (const record of records) activity.append(recordRow(record));
}

function renderOpportunityIntelligence() {
  const node = $("#opportunity-intelligence"); node.replaceChildren();
  const head = document.createElement("div"); const eyebrow = document.createElement("p"); eyebrow.className = "eyebrow"; eyebrow.textContent = "Optional owner intelligence"; const title = document.createElement("h2"); title.textContent = "What visitors want — and what becomes revenue"; const intro = document.createElement("p"); intro.textContent = "This is the linked assistant-to-outcome screen. These figures are illustrative examples, not this business’s data, until the relevant reporting modules are activated."; head.append(eyebrow, title, intro); node.append(head);
  const grid = document.createElement("div"); grid.className = "opportunity-grid";
  const cards = [
    ["Visitor-interest map", "Top needs", ["Air-conditioning enquiry · 20", "Refrigeration enquiry · 14", "Pricing / availability · 11"], "Captures shortcut, question, page and approved interest category."],
    ["Interest → lead conversion", "Where demand converts", ["Air-conditioning · 18 leads · 90%", "Refrigeration · 6 leads · 43%", "Pricing / availability · 2 leads · 18%"], "Shows which visitor needs create qualified opportunities."],
    ["Lead → deal outcome", "What creates revenue", ["Air-conditioning · 7 won · owner-confirmed", "Refrigeration · 2 won · owner-confirmed", "Revenue · recorded only after owner/CRM confirmation"], "Links assistant interest to owner-confirmed deal stages and value."],
    ["Content gaps", "What the site is missing", ["Repeated unanswered questions", "High-interest / low-conversion topics", "Slow response or follow-up bottlenecks"], "Gives the owner specific website, offer and staffing actions."]
  ];
  for (const [kicker, heading, items, description] of cards) { const card = document.createElement("article"); card.className = "opportunity-card"; const tag = document.createElement("span"); tag.textContent = "AVAILABLE WITH ACTIVATION"; const small = document.createElement("p"); small.className = "eyebrow"; small.textContent = kicker; const h = document.createElement("h3"); h.textContent = heading; const list = document.createElement("ul"); items.forEach((item) => { const li = document.createElement("li"); li.textContent = item; list.append(li); }); const note = document.createElement("p"); note.className = "module-note"; note.textContent = description; card.append(tag, small, h, list, note); grid.append(card); }
  node.append(grid);
  const footer = document.createElement("p"); footer.className = "activation-note"; footer.textContent = "Activation turns these examples into this tenant’s own observed interest, conversion, follow-up and owner-confirmed revenue data. It does not invent visitor interests, outcomes or revenue."; node.append(footer);
}

function renderPerformance(performance) {
  const node = $("#performance"); node.replaceChildren();
  if (!performance) return;
  const heading = document.createElement("div"); const eyebrow = document.createElement("p"); eyebrow.className = "eyebrow"; eyebrow.textContent = "Performance comparison"; const title = document.createElement("h2"); title.textContent = "Today vs previous process"; const description = document.createElement("p"); description.textContent = "Assistant visitors are unique assistant conversation sessions, not total website traffic."; heading.append(eyebrow, title, description); node.append(heading);
  const table = document.createElement("table"); table.className = "comparison"; const header = document.createElement("thead"); const body = document.createElement("tbody"); const headerRow = document.createElement("tr"); ["Measure", "Today", "Previously"].forEach((text) => { const cell = document.createElement("th"); cell.textContent = text; headerRow.append(cell); }); header.append(headerRow);
  const today = performance.today || {}; const previous = performance.baseline || {};
  const rows = [["Assistant visitors", today.assistantVisitors, previous.assistantVisitors], ["Leads captured", today.leadsCaptured, previous.leadsCaptured], ["Lead capture rate", today.leadRate == null ? null : `${today.leadRate}%`, previous.leadRate == null ? null : `${previous.leadRate}%`], ["Callback requests", today.callbacks, previous.callbacks], ["Average time to complete callback", today.averageCallbackMinutes == null ? null : `${today.averageCallbackMinutes} min`, previous.averageCallbackMinutes == null ? null : `${previous.averageCallbackMinutes} min`]];
  for (const [label, current, baseline] of rows) { const row = document.createElement("tr"); const name = document.createElement("td"); name.textContent = label; const currentCell = metricCell(current); const baselineCell = metricCell(baseline); row.append(name, currentCell, baselineCell); body.append(row); }
  table.append(header, body); node.append(table);
  const source = document.createElement("p"); source.className = "baseline-source"; source.textContent = `Previous-process baseline: ${previous.source || "Not supplied."}`; node.append(source);
}

function metricCell(value) { const cell = document.createElement("td"); if (value == null) { cell.textContent = "Unknown"; cell.className = "unknown"; } else cell.textContent = String(value); return cell; }

function recordRow(record) {
  const row = document.createElement("article"); row.className = "row";
  const time = document.createElement("time"); time.dateTime = record.createdAt; time.textContent = new Date(record.createdAt).toLocaleString();
  const type = document.createElement("strong"); type.className = "type"; type.textContent = typeLabel(record.type);
  const detail = document.createElement("div"); detail.className = "detail"; detail.textContent = recordDetail(record);
  const tag = document.createElement("span"); tag.className = "tag"; tag.textContent = record.simulated || record.mode === "demo" ? "Simulated" : "Live";
  row.append(time, type, detail, tag);
  if (record.type === "callbacks" && !record.handledAt) { const complete = document.createElement("button"); complete.className = "complete"; complete.textContent = "Mark callback complete"; complete.addEventListener("click", () => completeCallback(record.id, complete)); detail.append(document.createElement("br"), complete); }
  return row;
}

function typeLabel(type) { return ({ conversations:"Conversation", previewResponses:"Preview response", leads:"Enquiry", callbacks:"Callback", bookings:"Booking", payments:"Payment", emails:"Email preview", crmLeads:"CRM lead" })[type] || type; }
function recordDetail(record) { return [record.summary, record.reference, record.message, record.reason, record.service, record.subject, record.interest, record.name].filter(Boolean).join(" · ") || "Activity recorded"; }

function completeCallback(id, button) {
  button.disabled = true; button.textContent = "Saving…";
  fetch(`/api/owner/callbacks/${encodeURIComponent(id)}/complete?tenant=${encodeURIComponent(tenant)}`, { method:"POST", headers:{ Authorization:`Bearer ${state.code}` } })
    .then(async (response) => { const payload = await response.json(); if (!response.ok) throw new Error(payload.error || "Could not complete callback."); return loadActivity(); })
    .catch((error) => { button.disabled = false; button.textContent = error.message; });
}

function exportCsv() {
  if (!state.data) return;
  const rows = [["time", "type", "status", "detail"]];
  for (const record of Object.entries(state.data.records).flatMap(([type, entries]) => entries.map((entry) => ({ type, ...entry })))) rows.push([record.createdAt, typeLabel(record.type), record.simulated || record.mode === "demo" ? "simulated" : "live", recordDetail(record)]);
  const csv = rows.map((row) => row.map((value) => `"${String(value).replaceAll('"', '""')}"`).join(",")).join("\n");
  const file = new Blob([csv], { type:"text/csv;charset=utf-8" }); const url = URL.createObjectURL(file); const link = document.createElement("a"); link.href = url; link.download = `${tenant}-assistant-activity.csv`; link.click(); URL.revokeObjectURL(url);
}