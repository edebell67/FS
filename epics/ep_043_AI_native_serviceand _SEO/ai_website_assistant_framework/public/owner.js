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

function recordRow(record) {
  const row = document.createElement("article"); row.className = "row";
  const time = document.createElement("time"); time.dateTime = record.createdAt; time.textContent = new Date(record.createdAt).toLocaleString();
  const type = document.createElement("strong"); type.className = "type"; type.textContent = typeLabel(record.type);
  const detail = document.createElement("div"); detail.className = "detail"; detail.textContent = recordDetail(record);
  const tag = document.createElement("span"); tag.className = "tag"; tag.textContent = record.simulated || record.mode === "demo" ? "Simulated" : "Live";
  row.append(time, type, detail, tag); return row;
}

function typeLabel(type) { return ({ conversations:"Conversation", previewResponses:"Preview response", leads:"Enquiry", callbacks:"Callback", bookings:"Booking", payments:"Payment", emails:"Email preview", crmLeads:"CRM lead" })[type] || type; }
function recordDetail(record) { return [record.summary, record.reference, record.message, record.reason, record.service, record.subject, record.interest, record.name].filter(Boolean).join(" · ") || "Activity recorded"; }

function exportCsv() {
  if (!state.data) return;
  const rows = [["time", "type", "status", "detail"]];
  for (const record of Object.entries(state.data.records).flatMap(([type, entries]) => entries.map((entry) => ({ type, ...entry })))) rows.push([record.createdAt, typeLabel(record.type), record.simulated || record.mode === "demo" ? "simulated" : "live", recordDetail(record)]);
  const csv = rows.map((row) => row.map((value) => `"${String(value).replaceAll('"', '""')}"`).join(",")).join("\n");
  const file = new Blob([csv], { type:"text/csv;charset=utf-8" }); const url = URL.createObjectURL(file); const link = document.createElement("a"); link.href = url; link.download = `${tenant}-assistant-activity.csv`; link.click(); URL.revokeObjectURL(url);
}