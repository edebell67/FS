const assert = require('assert');
const {
  OnboardingError,
  SUPPORTED_BUSINESS_TYPE,
  createSignup,
} = require('./src/services/onboardingService');
const {
  hashPassword,
  isSecurePasswordHash,
  verifyPassword,
} = require('./src/services/passwordService');

function buildMockClient() {
  let userInsertCount = 0;
  let profileInsertCount = 0;
  let lastPasswordHash = null;

  return {
    async query(sql, params = []) {
      if (sql.includes('SELECT id FROM users WHERE email')) {
        return { rows: [] };
      }

      if (sql.includes('INSERT INTO users')) {
        userInsertCount += 1;
        lastPasswordHash = params[1];
        return {
          rows: [
            {
              id: '55555555-5555-5555-5555-555555555555',
              email: params[0],
              full_name: params[2],
              mobile_number: params[3],
              role: params[4],
              auth_provider: params[5],
              created_at: '2026-03-18T17:50:00.000Z',
              updated_at: '2026-03-18T17:50:00.000Z',
            },
          ],
        };
      }

      if (sql.includes('INSERT INTO business_profiles')) {
        profileInsertCount += 1;
        return {
          rows: [
            {
              id: '66666666-6666-6666-6666-666666666666',
              user_id: params[0],
              business_type: params[1],
              trading_name: params[2],
              legal_name: params[3],
              tax_country: params[4],
              base_currency: params[5],
              disclaimer_acknowledged: params[6],
              disclaimer_acknowledged_at: '2026-03-18T17:50:01.000Z',
              created_at: '2026-03-18T17:50:01.000Z',
              updated_at: '2026-03-18T17:50:01.000Z',
            },
          ],
        };
      }

      throw new Error(`Unexpected SQL in test harness: ${sql}`);
    },
    getState() {
      return {
        userInsertCount,
        profileInsertCount,
        lastPasswordHash,
      };
    },
  };
}

async function testSecurePasswordHelpers() {
  const password = 'StrongPass123!';
  const hash = hashPassword(password);

  assert.equal(isSecurePasswordHash(hash), true, 'Expected secure password hash format');
  assert.equal(verifyPassword(password, hash), true, 'Expected password to verify');
  assert.equal(verifyPassword('wrong-password', hash), false, 'Expected wrong password to fail');
}

async function testSignupSuccess() {
  const client = buildMockClient();
  const result = await createSignup(client, {
    full_name: 'Maya Sole Trader',
    email: 'maya@example.com',
    password: 'StrongPass123!',
    mobile_number: '+447700900123',
    trading_name: 'Maya Repairs',
    business_type: SUPPORTED_BUSINESS_TYPE,
    disclaimer_acknowledged: true,
  });

  const state = client.getState();
  assert.equal(state.userInsertCount, 1, 'Expected one user insert');
  assert.equal(state.profileInsertCount, 1, 'Expected one business profile insert');
  assert.equal(isSecurePasswordHash(state.lastPasswordHash), true, 'Expected stored password hash to be secure');
  assert.equal(result.user.id, '55555555-5555-5555-5555-555555555555');
  assert.equal(result.onboarding.business_profile_id, '66666666-6666-6666-6666-666666666666');
  assert.equal(result.onboarding.business_type, 'SOLE_TRADER');
  assert.equal(result.onboarding.disclaimer_acknowledged, true);
  assert.equal(result.onboarding.bank_connection_ready, true);
  assert.equal(result.onboarding.inbox_ready_user_id, result.user.id);
}

async function testUnsupportedBusinessType() {
  const client = buildMockClient();
  let error = null;

  try {
    await createSignup(client, {
      full_name: 'Limited Company User',
      email: 'limited@example.com',
      password: 'StrongPass123!',
      trading_name: 'Limited Co',
      business_type: 'LIMITED_COMPANY',
      disclaimer_acknowledged: true,
    });
  } catch (err) {
    error = err;
  }

  assert(error instanceof OnboardingError, 'Expected OnboardingError for unsupported business type');
  assert.equal(error.statusCode, 409);
}

async function testDisclaimerRequired() {
  const client = buildMockClient();
  let error = null;

  try {
    await createSignup(client, {
      full_name: 'No Disclaimer User',
      email: 'nodisclaimer@example.com',
      password: 'StrongPass123!',
      trading_name: 'No Disclaimer Trade',
      business_type: SUPPORTED_BUSINESS_TYPE,
      disclaimer_acknowledged: false,
    });
  } catch (err) {
    error = err;
  }

  assert(error instanceof OnboardingError, 'Expected OnboardingError for missing disclaimer');
  assert.equal(error.statusCode, 409);
}

async function run() {
  await testSecurePasswordHelpers();
  await testSignupSuccess();
  await testUnsupportedBusinessType();
  await testDisclaimerRequired();
  console.log('verify_signup_onboarding=PASS');
}

run().catch((error) => {
  console.error(`verify_signup_onboarding=FAIL: ${error.message}`);
  process.exit(1);
});
