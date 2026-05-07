const { decryptSecret, encryptSecret } = require("./secretCryptoService");

function ensureBankAccountId(bankAccountId) {
  if (!bankAccountId || typeof bankAccountId !== "string") {
    throw new Error("bank_account_id_required");
  }
}

function normalizeScopes(scopes) {
  const values = Array.isArray(scopes)
    ? scopes
    : typeof scopes === "string"
      ? scopes.split(/[,\s]+/)
      : [];

  return [...new Set(values.map((value) => String(value || "").trim().toLowerCase()).filter(Boolean))];
}

function normalizeTokenRecord(tokens) {
  if (!tokens || typeof tokens !== "object") {
    throw new Error("tokens_required");
  }

  const accessToken = tokens.accessToken ?? tokens.access_token;
  if (!accessToken) {
    throw new Error("access_token_required");
  }

  const refreshToken = tokens.refreshToken ?? tokens.refresh_token ?? null;
  const expiresAt = tokens.expiresAt ?? tokens.expires_at ?? null;
  const providerConsentId = tokens.providerConsentId ?? tokens.provider_consent_id ?? null;
  const scopes = normalizeScopes(tokens.scopes);

  return {
    accessToken: accessToken == null ? null : String(accessToken),
    refreshToken: refreshToken == null ? null : String(refreshToken),
    expiresAt: expiresAt == null ? null : new Date(expiresAt).toISOString(),
    scopes,
    providerConsentId: providerConsentId == null ? null : String(providerConsentId)
  };
}

function encryptTokenRecord(tokens) {
  const normalized = normalizeTokenRecord(tokens);
  return {
    accessToken: encryptSecret(normalized.accessToken),
    refreshToken: normalized.refreshToken == null ? null : encryptSecret(normalized.refreshToken),
    expiresAt: normalized.expiresAt,
    scopes: normalized.scopes,
    providerConsentId: normalized.providerConsentId
  };
}

function decryptTokenRecord(tokens) {
  const normalized = normalizeTokenRecord(tokens);
  return {
    accessToken: decryptSecret(normalized.accessToken),
    refreshToken: normalized.refreshToken == null ? null : decryptSecret(normalized.refreshToken),
    expiresAt: normalized.expiresAt,
    scopes: normalized.scopes,
    providerConsentId: normalized.providerConsentId
  };
}

function redactTokens(tokens) {
  if (!tokens) {
    return null;
  }

  const normalized = normalizeTokenRecord(tokens);
  return {
    accessToken: "[REDACTED]",
    refreshToken: normalized.refreshToken ? "[REDACTED]" : null,
    expiresAt: normalized.expiresAt,
    scopes: normalized.scopes,
    providerConsentId: normalized.providerConsentId
  };
}

async function storeConnectionTokens(db, bankAccountId, tokens) {
  ensureBankAccountId(bankAccountId);
  const encrypted = encryptTokenRecord(tokens);
  const query = `
    INSERT INTO bank_connection_tokens (
      bank_account_id,
      access_token,
      refresh_token,
      expires_at,
      scopes,
      provider_consent_id,
      updated_at
    )
    VALUES ($1, $2, $3, $4, $5, $6, CURRENT_TIMESTAMP)
    ON CONFLICT (bank_account_id) DO UPDATE SET
      access_token = EXCLUDED.access_token,
      refresh_token = EXCLUDED.refresh_token,
      expires_at = EXCLUDED.expires_at,
      scopes = EXCLUDED.scopes,
      provider_consent_id = EXCLUDED.provider_consent_id,
      updated_at = CURRENT_TIMESTAMP;
  `;

  await db.query(query, [
    bankAccountId,
    encrypted.accessToken,
    encrypted.refreshToken,
    encrypted.expiresAt,
    encrypted.scopes,
    encrypted.providerConsentId
  ]);

  return redactTokens(tokens);
}

async function getConnectionTokens(db, bankAccountId) {
  ensureBankAccountId(bankAccountId);
  const query = `
    SELECT
      bank_account_id,
      access_token,
      refresh_token,
      expires_at,
      scopes,
      provider_consent_id
    FROM bank_connection_tokens
    WHERE bank_account_id = $1;
  `;

  const result = await db.query(query, [bankAccountId]);
  if (!result.rows[0]) {
    return null;
  }

  const normalized = decryptTokenRecord(result.rows[0]);
  return {
    bank_account_id: bankAccountId,
    access_token: normalized.accessToken,
    refresh_token: normalized.refreshToken,
    expires_at: normalized.expiresAt,
    scopes: normalized.scopes,
    provider_consent_id: normalized.providerConsentId
  };
}

function isTokenExpired(tokens, bufferSeconds = 300) {
  if (!tokens || !tokens.expires_at) {
    return true;
  }

  const expiry = new Date(tokens.expires_at).getTime();
  if (Number.isNaN(expiry)) {
    return true;
  }

  return expiry - Date.now() < bufferSeconds * 1000;
}

async function updateConnectionStatus(db, bankAccountId, status, updates = {}) {
  ensureBankAccountId(bankAccountId);
  const lastSyncedAt = updates.lastSyncedAt ?? null;
  await db.query(
    `
      UPDATE bank_accounts
      SET status = $1,
          last_synced_at = COALESCE($2, last_synced_at),
          updated_at = CURRENT_TIMESTAMP
      WHERE bank_account_id = $3;
    `,
    [status, lastSyncedAt, bankAccountId]
  );
}

async function markConnectionSynced(db, bankAccountId, syncedAt = new Date()) {
  await updateConnectionStatus(db, bankAccountId, "connected", {
    lastSyncedAt: new Date(syncedAt).toISOString()
  });
}

async function getOrRefreshToken(db, bankAccountId, refreshFn) {
  const tokens = await getConnectionTokens(db, bankAccountId);
  if (!tokens) {
    throw new Error("connection_not_found");
  }

  if (!isTokenExpired(tokens)) {
    return tokens.access_token;
  }

  if (!tokens.refresh_token) {
    await updateConnectionStatus(db, bankAccountId, "reauth_required");
    throw new Error("refresh_token_missing");
  }

  try {
    const refreshed = normalizeTokenRecord(await refreshFn(tokens.refresh_token, tokens));
    await storeConnectionTokens(db, bankAccountId, refreshed);
    await updateConnectionStatus(db, bankAccountId, "connected");
    return refreshed.accessToken;
  } catch (error) {
    await updateConnectionStatus(db, bankAccountId, "reauth_required");
    throw error;
  }
}

module.exports = {
  getConnectionTokens,
  getOrRefreshToken,
  isTokenExpired,
  markConnectionSynced,
  normalizeScopes,
  normalizeTokenRecord,
  decryptTokenRecord,
  encryptTokenRecord,
  redactTokens,
  storeConnectionTokens,
  updateConnectionStatus
};
