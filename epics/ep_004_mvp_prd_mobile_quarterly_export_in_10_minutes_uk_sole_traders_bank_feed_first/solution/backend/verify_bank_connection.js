const assert = require("node:assert/strict");

const { handleConnectionCallback, reconnectBankAccount } = require("./src/services/bankAccountService");
const {
  getConnectionTokens,
  getOrRefreshToken,
  markConnectionSynced
} = require("./src/services/bankConnectionService");
const adapter = require("./src/services/openBankingAdapter");

class MockDb {
  constructor() {
    this.nextAccountNumber = 1;
    this.tables = {
      bank_accounts: [],
      bank_connection_tokens: []
    };
  }

  async query(text, params) {
    if (text.includes("INSERT INTO bank_accounts")) {
      const [
        user_id,
        business_profile_id,
        provider_account_id,
        provider_name,
        display_name,
        account_mask,
        currency,
        status
      ] = params;
      let account = this.tables.bank_accounts.find(
        (row) =>
          row.user_id === user_id &&
          row.provider_name === provider_name &&
          row.provider_account_id === provider_account_id
      );

      if (!account) {
        account = {
          bank_account_id: `bank-account-${this.nextAccountNumber++}`,
          user_id,
          business_profile_id,
          provider_account_id,
          provider_name,
          display_name,
          account_mask,
          currency,
          status,
          last_synced_at: null
        };
        this.tables.bank_accounts.push(account);
      } else {
        Object.assign(account, {
          display_name,
          account_mask,
          currency,
          status
        });
      }

      return {
        rows: [{ ...account }]
      };
    }

    if (text.includes("INSERT INTO bank_connection_tokens")) {
      const [bank_account_id, access_token, refresh_token, expires_at, scopes, provider_consent_id] = params;
      let token = this.tables.bank_connection_tokens.find((row) => row.bank_account_id === bank_account_id);

      if (!token) {
        token = { bank_account_id };
        this.tables.bank_connection_tokens.push(token);
      }

      Object.assign(token, {
        access_token,
        refresh_token,
        expires_at,
        scopes,
        provider_consent_id
      });
      return { rows: [] };
    }

    if (text.includes("SELECT") && text.includes("FROM bank_connection_tokens")) {
      const token = this.tables.bank_connection_tokens.find((row) => row.bank_account_id === params[0]);
      return { rows: token ? [{ ...token }] : [] };
    }

    if (text.includes("UPDATE bank_accounts")) {
      const account = this.tables.bank_accounts.find((row) => row.bank_account_id === params[2]);
      if (!account) {
        return { rows: [] };
      }

      account.status = params[0];
      if (params[1]) {
        account.last_synced_at = params[1];
      }
      return { rows: [{ ...account }] };
    }

    throw new Error(`Unhandled query in mock db: ${text}`);
  }
}

function createAdapterStub() {
  const baseAdapter = { ...adapter };

  baseAdapter.fetchProviderAccounts = async () => [
    {
      provider_account_id: "acc-001",
      account_name: "Business Current",
      currency: "GBP",
      account_mask: "****1234"
    },
    {
      provider_account_id: "acc-002",
      account_name: "Tax Saver",
      currency: "GBP",
      account_mask: "****5678"
    }
  ];

  return baseAdapter;
}

async function runVerification() {
  process.env.BANK_TOKEN_ENCRYPTION_KEY = "release-ready-demo-encryption-key";
  const db = new MockDb();
  const adapterStub = createAdapterStub();
  const config = {
    providerBaseUrl: "https://mockbank.example",
    clientId: "mock-client-id",
    redirectUri: "https://app.example/open-banking/callback",
    providerName: "MockBank",
    scopes: ["accounts", "transactions", "offline_access"]
  };
  const context = {
    userId: "user-001",
    businessProfileId: "biz-001",
    expectedState: "state-123"
  };

  const consentUrl = adapter.buildConsentUrl(config, { state: context.expectedState });
  assert.match(consentUrl, /scope=accounts\+transactions\+offline_access/);
  assert.throws(
    () => adapter.buildConsentUrl({ ...config, scopes: ["transactions", "payments"] }, { state: context.expectedState }),
    /disallowed_scope/
  );
  assert.throws(
    () => adapter.buildConsentUrl({ ...config, providerBaseUrl: "http://mockbank.example" }, { state: context.expectedState }),
    /secure_transport_required/
  );
  assert.throws(
    () => adapter.buildConsentUrl({ ...config, redirectUri: "http://app.example/open-banking/callback" }, { state: context.expectedState }),
    /secure_redirect_uri_required/
  );
  assert.match(
    adapter.buildConsentUrl(
      { ...config, redirectUri: "http://127.0.0.1:3000/open-banking/callback" },
      { state: context.expectedState }
    ),
    /redirect_uri=http%3A%2F%2F127\.0\.0\.1%3A3000%2Fopen-banking%2Fcallback/
  );

  const callbackResult = await handleConnectionCallback(
    db,
    context,
    { code: "provider-code-123", state: context.expectedState },
    adapterStub,
    config
  );

  assert.equal(callbackResult.connectionStatus, "connected");
  assert.equal(callbackResult.connectedAccountIds.length, 2);
  assert.equal(callbackResult.tokens.accessToken, "[REDACTED]");
  assert.equal(db.tables.bank_accounts.length, 2);
  assert.equal(db.tables.bank_connection_tokens.length, 2);
  assert.notEqual(db.tables.bank_connection_tokens[0].access_token, "mock_access_provider-code-123");
  assert.match(db.tables.bank_connection_tokens[0].access_token, /^enc\.v1:/);
  assert.match(db.tables.bank_connection_tokens[0].refresh_token, /^enc\.v1:/);

  const primaryAccountId = callbackResult.primaryBankAccountId;
  const initialTokens = await getConnectionTokens(db, primaryAccountId);
  assert.deepEqual(initialTokens.scopes, ["accounts", "transactions", "offline_access"]);

  db.tables.bank_connection_tokens[0].expires_at = new Date(Date.now() - 60_000).toISOString();
  const refreshedAccessToken = await getOrRefreshToken(db, primaryAccountId, async () => ({
    accessToken: "refreshed-access-token",
    refreshToken: "refreshed-refresh-token",
    expiresAt: new Date(Date.now() + 60 * 60 * 1000).toISOString(),
    scopes: ["accounts", "transactions", "offline_access"],
    providerConsentId: "consent-refresh-001"
  }));
  assert.equal(refreshedAccessToken, "refreshed-access-token");

  db.tables.bank_connection_tokens[0].expires_at = new Date(Date.now() - 60_000).toISOString();
  await assert.rejects(
    () => getOrRefreshToken(db, primaryAccountId, async () => {
      throw new Error("provider_refresh_failed");
    }),
    /provider_refresh_failed/
  );
  assert.equal(db.tables.bank_accounts[0].status, "reauth_required");

  const reconnectResult = await reconnectBankAccount(
    db,
    primaryAccountId,
    { code: "provider-code-reauth-001" },
    adapter,
    config
  );
  assert.equal(reconnectResult.connectionStatus, "connected");
  assert.equal(db.tables.bank_accounts[0].status, "connected");

  await markConnectionSynced(db, primaryAccountId, "2026-03-21T12:00:00.000Z");
  assert.equal(db.tables.bank_accounts[0].last_synced_at, "2026-03-21T12:00:00.000Z");

  console.log("VERIFICATION PASSED");
  console.log("PASS: production redirects require secure transport");
  console.log("PASS: bank tokens are encrypted at rest and redacted in outputs");
  console.log(
    JSON.stringify(
      {
        consentUrl,
        connectedAccountIds: callbackResult.connectedAccountIds,
        finalAccountState: db.tables.bank_accounts[0],
        finalTokenRecord: {
          ...db.tables.bank_connection_tokens[0],
          access_token: "[REDACTED]",
          refresh_token: "[REDACTED]"
        }
      },
      null,
      2
    )
  );
}

module.exports = {
  runVerification
};

if (require.main === module) {
  runVerification().catch((error) => {
    console.error("VERIFICATION FAILED", error);
    process.exit(1);
  });
}
