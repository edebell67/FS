import { randomUUID } from "node:crypto";
import { mkdir, readFile, rename, writeFile } from "node:fs/promises";
import path from "node:path";

const clone = (value) => structuredClone(value);
const RECORD_TYPES = ["conversations", "previewResponses", "leads", "callbacks", "bookings", "payments", "emails", "crmLeads"];
const WORKFLOW_STATUSES = new Set(["not_started", "in_progress", "ready_for_outreach", "blocked", "outreach_sent", "replied", "closed_do_not_contact"]);
const WORKFLOW_STAGE_STATES = new Set(["pending", "complete", "not_applicable"]);

function normalizeHost(value = "") {
  return String(value).trim().toLowerCase().replace(/^https?:\/\//, "").split("/")[0].split(":")[0];
}

export class JsonStore {
  constructor(dataDir) {
    this.dataDir = dataDir;
    this.clientsPath = path.join(dataDir, "clients.json");
    this.recordsPath = path.join(dataDir, "records.json");
    this.clients = [];
    this.records = Object.fromEntries(RECORD_TYPES.map((type) => [type, []]));
    this.writeQueue = Promise.resolve();
  }

  async init() {
    await mkdir(this.dataDir, { recursive: true });
    this.clients = JSON.parse(await readFile(this.clientsPath, "utf8")).map(normalizeClient);
    const records = JSON.parse(await readFile(this.recordsPath, "utf8"));
    this.records = Object.fromEntries(RECORD_TYPES.map((type) => [type, Array.isArray(records[type]) ? records[type] : []]));
    return this;
  }

  resolveClient({ publicKey, host }) {
    const client = this.clients.find((item) => item.publicKey === publicKey);
    if (!client) return null;
    const requestedHost = normalizeHost(host);
    const allowed = (client.allowedHosts || []).map(normalizeHost);
    if (requestedHost && allowed.length && !allowed.includes(requestedHost)) return null;
    return clone(client);
  }

  getClientById(id) {
    const client = this.clients.find((item) => item.id === id);
    return client ? clone(client) : null;
  }

  listClients() {
    return clone(this.clients);
  }

  publicClient(client) {
    return {
      businessName: client.businessName,
      tagline: client.tagline,
      logoText: client.logoText,
      theme: client.theme,
      contact: client.enabledModules.includes("contact") ? client.contact : null,
      booking: client.enabledModules.includes("booking") ? client.booking : null,
      status: client.status,
      enabledModules: client.enabledModules,
      pages: client.enabledModules.includes("navigation") ? client.pages : [],
      demoWorkflows: client.status === "demo" ? client.demoWorkflows || {} : {}
    };
  }

  async createClient(input) {
    const client = normalizeClient({ ...input, id: input.id || slugify(input.businessName), publicKey: input.publicKey || `client_${randomUUID().slice(0, 8)}` });
    if (this.clients.some((item) => item.id === client.id || item.publicKey === client.publicKey)) {
      throw new Error("A client with that ID or public key already exists.");
    }
    this.clients.push(client);
    await this.persistClients();
    return clone(client);
  }

  async duplicateClient(id) {
    const source = this.clients.find((item) => item.id === id);
    if (!source) return null;
    const suffix = randomUUID().slice(0, 6);
    const duplicate = clone(source);
    duplicate.id = `${source.id}-copy-${suffix}`;
    duplicate.publicKey = `client_${randomUUID().slice(0, 8)}`;
    duplicate.businessName = `${source.businessName} copy`;
    duplicate.status = "demo";
    this.clients.push(duplicate);
    await this.persistClients();
    return clone(duplicate);
  }

  async updateClient(id, patch) {
    const index = this.clients.findIndex((item) => item.id === id);
    if (index < 0) return null;
    const immutable = { id: this.clients[index].id, publicKey: this.clients[index].publicKey };
    this.clients[index] = normalizeClient({ ...this.clients[index], ...patch, ...immutable });
    await this.persistClients();
    return clone(this.clients[index]);
  }

  async appendRecord(type, value) {
    if (!Object.hasOwn(this.records, type)) throw new Error("Unknown record type.");
    const record = { id: randomUUID(), createdAt: new Date().toISOString(), ...clone(value) };
    this.records[type].unshift(record);
    this.records[type] = this.records[type].slice(0, 2000);
    await this.persistRecords();
    return clone(record);
  }

  listRecords() {
    return clone(this.records);
  }

  persistClients() {
    return this.enqueueWrite(this.clientsPath, this.clients);
  }

  persistRecords() {
    return this.enqueueWrite(this.recordsPath, this.records);
  }

  enqueueWrite(file, value) {
    this.writeQueue = this.writeQueue.then(async () => {
      const temporary = `${file}.tmp`;
      await writeFile(temporary, `${JSON.stringify(value, null, 2)}\n`, "utf8");
      await rename(temporary, file);
    });
    return this.writeQueue;
  }
}

function slugify(value = "client") {
  return String(value).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 48) || `client-${randomUUID().slice(0, 6)}`;
}

function normalizeWorkflow(workflow = {}) {
  const stages = Object.fromEntries(Object.entries(workflow?.stages || {}).map(([key, value]) => [String(key).slice(0, 80), WORKFLOW_STAGE_STATES.has(value) ? value : "pending"]));
  return {
    status: WORKFLOW_STATUSES.has(workflow?.status) ? workflow.status : "not_started",
    blocker: String(workflow?.blocker || "").replace(/[\u0000-\u001f]/g, " ").trim().slice(0, 1500),
    stages
  };
}

function normalizeClient(client) {
  const modules = ["assistant", ...(Array.isArray(client.enabledModules) ? client.enabledModules : [])];
  return {
    ...client,
    id: slugify(client.id),
    businessName: String(client.businessName || "Untitled business").trim().slice(0, 120),
    tagline: String(client.tagline || "").trim().slice(0, 160),
    status: client.status === "live" ? "live" : "demo",
    allowedHosts: [...new Set((client.allowedHosts || []).map(normalizeHost).filter(Boolean))],
    enabledModules: [...new Set(modules)],
    pages: Array.isArray(client.pages) ? client.pages : [],
    knowledge: Array.isArray(client.knowledge) ? client.knowledge : [],
    deployments: Array.isArray(client.deployments) ? client.deployments : (client.deployment ? [client.deployment] : []),
    notificationDestinations: Array.isArray(client.notificationDestinations) ? client.notificationDestinations : [],
    workflow: normalizeWorkflow(client.workflow),
    demoWorkflows: client.demoWorkflows && typeof client.demoWorkflows === "object" ? client.demoWorkflows : {}
  };
}
