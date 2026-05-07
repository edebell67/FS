const {
  redactTokens,
  storeConnectionTokens,
  updateConnectionStatus
} = require("./bankConnectionService");

function normalizeCallbackPayload(callbackPayload, context = {}) {
  if (typeof callbackPayload === "string") {
    return {
      code: callbackPayload,
      state: context.expectedState ?? context.state ?? null
    };
  }

  return {
    code: callbackPayload?.code ?? null,
    state: callbackPayload?.state ?? null
  };
}

function validateCallbackPayload(callbackPayload, context = {}) {
  const payload = normalizeCallbackPayload(callbackPayload, context);
  if (!context.userId || !context.businessProfileId) {
    throw new Error("connection_context_incomplete");
  }
  if (!payload.code) {
    throw new Error("provider_code_required");
  }
  if (context.expectedState && payload.state !== context.expectedState) {
    throw new Error("invalid_connection_state");
  }
  return payload;
}

function mapProviderAccount(providerAccount, context, providerName) {
  const providerAccountId = providerAccount.provider_account_id ?? providerAccount.providerAccountId;
  if (!providerAccountId) {
    throw new Error("provider_account_id_required");
  }

  return {
    user_id: context.userId,
    business_profile_id: context.businessProfileId,
    provider_account_id: String(providerAccountId),
    provider_name: providerName,
    display_name: String(
      providerAccount.account_name
        ?? providerAccount.display_name
        ?? providerAccount.name
        ?? "Connected account"
    ),
    account_mask: providerAccount.account_mask ?? providerAccount.accountMask ?? null,
    currency: String(providerAccount.currency ?? "GBP").toUpperCase(),
    status: "connected"
  };
}

async function upsertBankAccount(db, accountData) {
  const {
    user_id,
    business_profile_id,
    provider_account_id,
    provider_name,
    display_name,
    account_mask,
    currency,
    status
  } = accountData;

  const query = `
    INSERT INTO bank_accounts (
      bank_account_id,
      user_id,
      business_profile_id,
      provider_account_id,
      provider_name,
      display_name,
      account_mask,
      currency,
      status,
      last_synced_at,
      created_at,
      updated_at
    )
    VALUES (gen_random_uuid(), $1, $2, $3, $4, $5, $6, $7, $8, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    ON CONFLICT (user_id, provider_name, provider_account_id) DO UPDATE SET
      display_name = EXCLUDED.display_name,
      account_mask = EXCLUDED.account_mask,
      currency = EXCLUDED.currency,
      status = EXCLUDED.status,
      updated_at = CURRENT_TIMESTAMP
    RETURNING
      bank_account_id,
      user_id,
      business_profile_id,
      provider_account_id,
      provider_name,
      display_name,
      account_mask,
      currency,
      status,
      last_synced_at;
  `;

  const result = await db.query(query, [
    user_id,
    business_profile_id,
    provider_account_id,
    provider_name,
    display_name,
    account_mask,
    currency,
    status
  ]);

  return result.rows[0];
}

async function handleConnectionCallback(db, context, callbackPayload, adapter, config) {
  const payload = validateCallbackPayload(callbackPayload, context);
  const tokens = await adapter.exchangeCodeForTokens(config, payload.code, {
    userId: context.userId,
    businessProfileId: context.businessProfileId,
    state: payload.state
  });
  const providerAccounts = await adapter.fetchProviderAccounts(tokens.accessToken, config, {
    userId: context.userId,
    businessProfileId: context.businessProfileId
  });

  if (!Array.isArray(providerAccounts) || providerAccounts.length === 0) {
    throw new Error("provider_accounts_missing");
  }

  const connectedAccounts = [];
  for (const providerAccount of providerAccounts) {
    const accountRecord = await upsertBankAccount(
      db,
      mapProviderAccount(providerAccount, context, config.providerName)
    );
    await storeConnectionTokens(db, accountRecord.bank_account_id, tokens);
    connectedAccounts.push(accountRecord);
  }

  return {
    connectedAccountIds: connectedAccounts.map((account) => account.bank_account_id),
    primaryBankAccountId: connectedAccounts[0].bank_account_id,
    connectionStatus: "connected",
    providerName: config.providerName,
    scopes: tokens.scopes,
    providerConsentId: tokens.providerConsentId ?? null,
    tokens: redactTokens(tokens)
  };
}

async function reconnectBankAccount(db, bankAccountId, callbackPayload, adapter, config) {
  const payload = normalizeCallbackPayload(callbackPayload);
  if (!payload.code) {
    throw new Error("provider_code_required");
  }

  const tokens = await adapter.exchangeCodeForTokens(config, payload.code, {
    bankAccountId
  });
  await storeConnectionTokens(db, bankAccountId, tokens);
  await updateConnectionStatus(db, bankAccountId, "connected");

  return {
    bankAccountId,
    connectionStatus: "connected",
    tokens: redactTokens(tokens)
  };
}

module.exports = {
  handleConnectionCallback,
  reconnectBankAccount,
  upsertBankAccount,
  validateCallbackPayload
};
