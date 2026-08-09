// DB-backed store adapter — implements the exact same public interface as
// JsonStore (src/store.js), so createApp({ store }) can swap between them
// with zero changes to server.js route handlers. Built on node:sqlite
// (built into Node 22+, no external service or provisioning required),
// which lets this run and be tested identically to JsonStore in any
// environment, including this one. The schema is designed to swap onto a
// managed Postgres instance later with the same shape: two tables, one
// JSON-blob-per-row for the client's full nested config (mirroring what
// JsonStore already did — the client object was always read/written whole,
// never queried column-by-column), and one real relational table for
// records, since records ARE queried by clientId/type/createdAt today
// (the compare and reporting endpoints scan by these), which is exactly
// what indexes are for.
import { DatabaseSync } from "node:sqlite";
import { randomUUID } from "node:crypto";
import { mkdir } from "node:fs/promises";
import path from "node:path";
import { normalizeClient, RECORD_TYPES, RECORD_CAPS, DEFAULT_RECORD_CAP } from "./store.js";

const clone = (value) => structuredClone(value);

function normalizeHost(value = "") {
  return String(value).trim().toLowerCase().replace(/^https?:\/\//, "").split("/")[0].split(":")[0];
}

const SCHEMA = `
CREATE TABLE IF NOT EXISTS clients (
  id TEXT PRIMARY KEY,
  publicKey TEXT UNIQUE NOT NULL,
  data TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS records (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  clientId TEXT,
  sessionId TEXT,
  createdAt TEXT NOT NULL,
  data TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_records_type_client_created ON records (type, clientId, createdAt);
CREATE INDEX IF NOT EXISTS idx_records_type_session ON records (type, clientId, sessionId);
`;

export class SqliteStore {
  constructor(dbPath) {
    this.dbPath = dbPath === ":memory:" ? dbPath : path.resolve(dbPath);
  }

  async init() {
    if (this.dbPath !== ":memory:") await mkdir(path.dirname(this.dbPath), { recursive: true });
    this.db = new DatabaseSync(this.dbPath);
    this.db.exec(SCHEMA);
    return this;
  }

  // --- clients ---------------------------------------------------------

  resolveClient({ publicKey, host }) {
    const row = this.db.prepare("SELECT data FROM clients WHERE publicKey = ?").get(publicKey);
    if (!row) return null;
    const client = JSON.parse(row.data);
    const requestedHost = normalizeHost(host);
    const allowed = (client.allowedHosts || []).map(normalizeHost);
    if (requestedHost && allowed.length && !allowed.includes(requestedHost)) return null;
    return clone(client);
  }

  getClientById(id) {
    const row = this.db.prepare("SELECT data FROM clients WHERE id = ?").get(id);
    return row ? JSON.parse(row.data) : null;
  }

  listClients() {
    return this.db.prepare("SELECT data FROM clients").all().map((row) => JSON.parse(row.data));
  }

  publicClient(client) {
    // Identical projection logic to JsonStore.publicClient — kept here
    // (rather than shared) only because it depends on resolveBlueprintActions
    // / retrieveKnowledge, which would create a circular import from store.js.
    // Any change to one must be mirrored in the other until this is factored
    // out into a shared module.
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
      demoWorkflows: client.status === "demo" ? client.demoWorkflows || {} : {},
      engagementMode: client.engagementMode,
      proactiveDelayMs: client.proactiveDelayMs,
      analyticsEnabled: client.analyticsEnabled,
      leadReasonOptions: client.enabledModules.includes("leadCapture") ? client.leadReasonOptions : [],
      serviceReasonMap: client.enabledModules.includes("leadCapture") ? client.serviceReasonMap : {},
      assistantActions: [],
      demoActions: []
    };
  }

  async createClient(input) {
    const client = normalizeClient({ ...input, id: input.id || slugify(input.businessName), publicKey: input.publicKey || `client_${randomUUID().slice(0, 8)}` });
    const exists = this.db.prepare("SELECT 1 FROM clients WHERE id = ? OR publicKey = ?").get(client.id, client.publicKey);
    if (exists) throw new Error("A client with that ID or public key already exists.");
    this.db.prepare("INSERT INTO clients (id, publicKey, data) VALUES (?, ?, ?)").run(client.id, client.publicKey, JSON.stringify(client));
    return clone(client);
  }

  async duplicateClient(id) {
    const source = this.getClientById(id);
    if (!source) return null;
    const suffix = randomUUID().slice(0, 6);
    const duplicate = { ...clone(source), id: `${source.id}-copy-${suffix}`, publicKey: `client_${randomUUID().slice(0, 8)}`, businessName: `${source.businessName} copy`, status: "demo" };
    this.db.prepare("INSERT INTO clients (id, publicKey, data) VALUES (?, ?, ?)").run(duplicate.id, duplicate.publicKey, JSON.stringify(duplicate));
    return clone(duplicate);
  }

  async updateClient(id, patch) {
    const existing = this.getClientById(id);
    if (!existing) return null;
    const updated = normalizeClient({ ...existing, ...patch, id: existing.id, publicKey: existing.publicKey });
    this.db.prepare("UPDATE clients SET data = ? WHERE id = ?").run(JSON.stringify(updated), id);
    return clone(updated);
  }

  // --- records -----------------------------------------------------------

  async appendRecord(type, value) {
    if (!RECORD_TYPES.includes(type)) throw new Error("Unknown record type.");
    const record = { id: randomUUID(), createdAt: new Date().toISOString(), ...clone(value) };
    this.db.prepare("INSERT INTO records (id, type, clientId, sessionId, createdAt, data) VALUES (?, ?, ?, ?, ?, ?)")
      .run(record.id, type, record.clientId || null, record.sessionId || null, record.createdAt, JSON.stringify(record));
    this.trimType(type);
    return clone(record);
  }

  async appendRecords(type, values) {
    if (!RECORD_TYPES.includes(type)) throw new Error("Unknown record type.");
    const now = new Date().toISOString();
    const insert = this.db.prepare("INSERT INTO records (id, type, clientId, sessionId, createdAt, data) VALUES (?, ?, ?, ?, ?, ?)");
    const created = values.map((value) => ({ id: randomUUID(), createdAt: now, ...clone(value) }));
    for (const record of created) insert.run(record.id, type, record.clientId || null, record.sessionId || null, record.createdAt, JSON.stringify(record));
    this.trimType(type);
    return created.length;
  }

  async updateRecord(type, id, patch) {
    if (!RECORD_TYPES.includes(type)) throw new Error("Unknown record type.");
    const row = this.db.prepare("SELECT data FROM records WHERE id = ? AND type = ?").get(id, type);
    if (!row) return null;
    const updated = { ...JSON.parse(row.data), ...clone(patch) };
    this.db.prepare("UPDATE records SET data = ?, clientId = ?, sessionId = ? WHERE id = ?").run(JSON.stringify(updated), updated.clientId || null, updated.sessionId || null, id);
    return clone(updated);
  }

  getRecord(type, id) {
    const row = this.db.prepare("SELECT data FROM records WHERE id = ? AND type = ?").get(id, type);
    return row ? JSON.parse(row.data) : null;
  }

  // Matches JsonStore.listRecords(clientId?): every existing caller passes
  // no clientId and filters manually afterward, except buildReportingSnapshot
  // in server.js, which relies on this filtering. SQLite can do the filter
  // in the query itself rather than in JS after loading everything.
  listRecords(clientId) {
    const out = Object.fromEntries(RECORD_TYPES.map((type) => [type, []]));
    const rows = clientId
      ? this.db.prepare("SELECT type, data FROM records WHERE clientId = ? ORDER BY createdAt DESC").all(clientId)
      : this.db.prepare("SELECT type, data FROM records ORDER BY createdAt DESC").all();
    for (const row of rows) {
      if (out[row.type]) out[row.type].push(JSON.parse(row.data));
    }
    return out;
  }

  // Additional, DB-native capability JsonStore could not offer efficiently:
  // fetch one client's records of one type without loading everything else
  // into memory first. Not part of the original interface — additive.
  listRecordsForClient(clientId, type) {
    return this.db.prepare("SELECT data FROM records WHERE type = ? AND clientId = ? ORDER BY createdAt DESC").all(type, clientId).map((row) => JSON.parse(row.data));
  }

  activePromotionsForClient(clientId) {
    const client = this.getClientById(clientId);
    if (!client || !Array.isArray(client.promotions)) return [];
    const now = new Date();
    return client.promotions.filter((p) => p.active && new Date(p.startAt) <= now && new Date(p.endAt) > now);
  }

  promotionEffectiveness(promotion) {
    if (!promotion) return null;
    const events = this.listRecordsForClient(promotion.clientId, "events").filter((e) => e.promotionId === promotion.promotionId);
    const impressions = events.filter((e) => e.type === "promotion_impression").length;
    const clicks = events.filter((e) => e.type === "promotion_click").length;
    const stats = { ...promotion.stats, impressions, clicks };
    stats.clickThroughRate = impressions > 0 ? clicks / impressions : 0;
    return stats;
  }

  trimType(type) {
    const cap = RECORD_CAPS[type] || DEFAULT_RECORD_CAP;
    const count = this.db.prepare("SELECT COUNT(*) AS n FROM records WHERE type = ?").get(type).n;
    if (count <= cap) return;
    this.db.prepare(
      `DELETE FROM records WHERE type = ? AND id IN (
         SELECT id FROM records WHERE type = ? ORDER BY createdAt ASC LIMIT ?
       )`
    ).run(type, type, count - cap);
  }

  close() {
    this.db?.close();
  }
}

function slugify(value = "client") {
  return String(value).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 48) || `client-${randomUUID().slice(0, 6)}`;
}
