const MODULES = [
  ["assistant", "AI assistant"], ["faq", "FAQ"], ["navigation", "Navigation"], ["booking", "Booking"],
  ["callback", "Callback"], ["leadCapture", "Lead capture"], ["contact", "Contact help"],
  ["demoBooking", "Demo booking"], ["demoPayment", "Demo payment"], ["demoEmail", "Demo email"], ["demoCrm", "Demo CRM"]
];
const state = { clients: [], selected: null, records: {}, recordType: "conversations" };
const $ = (selector) => document.querySelector(selector);

const tokenInput = $("#admin-token");
tokenInput.value = sessionStorage.getItem("assistant_admin_token") || "change-me-before-live-use";
$("#connect").addEventListener("click", connect);
$("#client-form").addEventListener("submit", saveClient);
$("#duplicate").addEventListener("click", duplicateClient);
$("#new-client").addEventListener("click", createClient);
$("#add-knowledge").addEventListener("click", () => addKnowledgeRow({ title: "", content: "" }));
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
  setValue(form, "logoText", client.logoText); setValue(form, "accent", client.theme?.accent || "#e85d3f"); setValue(form, "ink", client.theme?.ink || "#17211f"); setValue(form, "surface", client.theme?.surface || "#f5f0e7");
  setValue(form, "telephone", client.contact?.telephone); setValue(form, "email", client.contact?.email); setValue(form, "address", client.contact?.address); setValue(form, "openingHours", client.contact?.openingHours);
  setValue(form, "bookingProvider", client.booking?.provider); setValue(form, "bookingUrl", client.booking?.url);
  const moduleGrid = $("#module-grid"); moduleGrid.replaceChildren();
  for (const [key, label] of MODULES) { const wrap = document.createElement("label"); const input = document.createElement("input"); input.type = "checkbox"; input.value = key; input.checked = client.enabledModules.includes(key); input.disabled = key === "assistant"; wrap.append(input, label); moduleGrid.append(wrap); }
  const knowledge = $("#knowledge-list"); knowledge.replaceChildren(); (client.knowledge || []).forEach(addKnowledgeRow);
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
  const patch = {
    businessName: form.get("businessName"), tagline: form.get("tagline"), status: form.get("status"), logoText: form.get("logoText"),
    allowedHosts: form.get("allowedHosts").split(",").map((item) => item.trim()).filter(Boolean), enabledModules, knowledge,
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
    const { client } = await api("/api/admin/clients", { method:"POST", body:JSON.stringify({ businessName, status:"demo", allowedHosts:["localhost"], logoText:businessName.slice(0,2).toUpperCase(), theme:{ accent:"#e85d3f", ink:"#17211f", surface:"#f5f0e7" }, contact:{}, booking:{}, enabledModules:["assistant","faq","contact"], pages:[], knowledge:[], notificationDestinations:[] }) });
    state.clients.push(client); $("#client-count").textContent = state.clients.length; selectClient(client.id); toast("Client profile created");
  } catch (error) { toast(error.message); }
}

function switchView(view) {
  $("#clients-view").hidden = view !== "clients"; $("#activity-view").hidden = view !== "activity"; $("#view-title").textContent = view === "clients" ? "Client profiles" : "Activity";
  document.querySelectorAll("aside nav button").forEach((button) => button.classList.toggle("nav-active", button.dataset.view === view));
}

function renderActivity() {
  const table = $("#activity-table"); table.replaceChildren(); const records = state.records[state.recordType] || [];
  if (!records.length) { const empty = document.createElement("p"); empty.className = "notice"; empty.textContent = `No ${state.recordType} have been recorded.`; table.append(empty); return; }
  for (const record of records) {
    const row = document.createElement("div"); row.className = "record";
    const time = document.createElement("time"); time.textContent = new Date(record.createdAt).toLocaleString();
    const client = document.createElement("strong"); client.textContent = state.clients.find((item) => item.id === record.clientId)?.businessName || record.clientId;
    const detail = document.createElement("div"); detail.textContent = [record.reference, record.message || record.reason || record.service || record.subject || record.interest || record.name].filter(Boolean).join(" · ") || "—";
    const mode = document.createElement("span"); mode.textContent = record.simulated || record.mode === "demo" ? "Demo" : "Live";
    row.append(time, client, detail, mode); table.append(row);
  }
}

function setValue(form, name, value = "") { form.elements[name].value = value || ""; }
function toast(message) { document.querySelector(".toast")?.remove(); const node = document.createElement("div"); node.className = "toast"; node.textContent = message; document.body.append(node); setTimeout(() => node.remove(), 2600); }
