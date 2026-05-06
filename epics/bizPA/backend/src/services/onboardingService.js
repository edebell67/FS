const { hashPassword } = require('./passwordService');
const { signSessionToken } = require('./authSessionService');

const SUPPORTED_BUSINESS_TYPE = 'SOLE_TRADER';
const DEFAULT_TAX_COUNTRY = 'GB';
const DEFAULT_BASE_CURRENCY = 'GBP';
const DEFAULT_ROLE = 'owner';
const DEFAULT_AUTH_PROVIDER = 'password';

class OnboardingError extends Error {
  constructor(message, statusCode = 400, details = {}) {
    super(message);
    this.name = 'OnboardingError';
    this.statusCode = statusCode;
    this.details = details;
  }
}

function normalizeEmail(email) {
  return String(email || '').trim().toLowerCase();
}

function normalizeText(value) {
  return String(value || '').trim();
}

function buildAuthToken(user) {
  return signSessionToken({ id: user.id, email: user.email, role: user.role || DEFAULT_ROLE });
}

function assertSignupPayload(payload) {
  const fullName = normalizeText(payload.full_name);
  const email = normalizeEmail(payload.email);
  const password = String(payload.password || '');
  const tradingName = normalizeText(payload.trading_name);
  const businessType = normalizeText(payload.business_type).toUpperCase();
  const mobileNumber = normalizeText(payload.mobile_number);
  const disclaimerAcknowledged = payload.disclaimer_acknowledged === true;

  if (!fullName) {
    throw new OnboardingError('Full name is required.');
  }
  if (!email || !email.includes('@')) {
    throw new OnboardingError('A valid email is required.');
  }
  if (password.length < 8) {
    throw new OnboardingError('Password must be at least 8 characters long.');
  }
  if (!tradingName) {
    throw new OnboardingError('Trading name is required.');
  }
  if (businessType !== SUPPORTED_BUSINESS_TYPE) {
    throw new OnboardingError('Only sole trader businesses are supported in the MVP.', 409, {
      supported_business_types: [SUPPORTED_BUSINESS_TYPE],
      requested_business_type: businessType || null,
    });
  }
  if (!disclaimerAcknowledged) {
    throw new OnboardingError('You must acknowledge the MVP disclaimer before continuing.', 409, {
      disclaimer_required: true,
    });
  }

  return {
    fullName,
    email,
    password,
    tradingName,
    businessType,
    mobileNumber: mobileNumber || null,
    disclaimerAcknowledged,
  };
}

function buildOnboardingResponse({ user, businessProfile }) {
  return {
    token: buildAuthToken(user),
    user: {
      id: user.id,
      email: user.email,
      full_name: user.full_name,
      role: user.role || DEFAULT_ROLE,
      auth_provider: user.auth_provider || DEFAULT_AUTH_PROVIDER,
      mobile_number: user.mobile_number || null,
      created_at: user.created_at,
      updated_at: user.updated_at,
    },
    onboarding: {
      business_profile_id: businessProfile.id,
      user_id: businessProfile.user_id,
      business_type: businessProfile.business_type,
      trading_name: businessProfile.trading_name,
      legal_name: businessProfile.legal_name,
      tax_country: businessProfile.tax_country,
      base_currency: businessProfile.base_currency,
      disclaimer_acknowledged: businessProfile.disclaimer_acknowledged,
      disclaimer_acknowledged_at: businessProfile.disclaimer_acknowledged_at,
      created_at: businessProfile.created_at,
      updated_at: businessProfile.updated_at,
      next_step: 'connect_bank',
      bank_connection_ready: businessProfile.disclaimer_acknowledged === true,
      inbox_ready_user_id: businessProfile.user_id,
    },
  };
}

async function createSignup(client, payload) {
  const input = assertSignupPayload(payload);
  const passwordHash = hashPassword(input.password);

  const existingUser = await client.query('SELECT id FROM users WHERE email = $1 LIMIT 1', [input.email]);
  if (existingUser.rows.length > 0) {
    throw new OnboardingError('An account already exists for that email address.', 409, {
      email: input.email,
    });
  }

  const userInsert = await client.query(
    `INSERT INTO users (email, password_hash, full_name, mobile_number, role, auth_provider, is_active)
     VALUES ($1, $2, $3, $4, $5, $6, true)
     RETURNING id, email, full_name, mobile_number, role, auth_provider, created_at, updated_at`,
    [input.email, passwordHash, input.fullName, input.mobileNumber, DEFAULT_ROLE, DEFAULT_AUTH_PROVIDER]
  );

  const user = userInsert.rows[0];

  const profileInsert = await client.query(
    `INSERT INTO business_profiles (
        user_id,
        business_type,
        trading_name,
        legal_name,
        tax_country,
        base_currency,
        disclaimer_acknowledged,
        disclaimer_acknowledged_at,
        onboarding_completed_at
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
      RETURNING
        id,
        user_id,
        business_type,
        trading_name,
        legal_name,
        tax_country,
        base_currency,
        disclaimer_acknowledged,
        disclaimer_acknowledged_at,
        created_at,
        updated_at`,
    [
      user.id,
      input.businessType,
      input.tradingName,
      input.fullName,
      DEFAULT_TAX_COUNTRY,
      DEFAULT_BASE_CURRENCY,
      input.disclaimerAcknowledged,
    ]
  );

  return buildOnboardingResponse({
    user,
    businessProfile: profileInsert.rows[0],
  });
}

async function getOnboardingProfile(client, userId) {
  const result = await client.query(
    `SELECT
        u.id,
        u.email,
        u.full_name,
        COALESCE(u.role, $2) AS role,
        COALESCE(u.auth_provider, $3) AS auth_provider,
        u.mobile_number,
        COALESCE(u.is_active, true) AS is_active,
        u.created_at,
        u.updated_at,
        bp.id AS business_profile_id,
        bp.business_type,
        bp.trading_name,
        bp.legal_name,
        bp.tax_country,
        bp.base_currency,
        bp.disclaimer_acknowledged,
        bp.disclaimer_acknowledged_at,
        bp.onboarding_completed_at,
        bp.created_at AS business_profile_created_at,
        bp.updated_at AS business_profile_updated_at
      FROM users u
      LEFT JOIN business_profiles bp ON bp.user_id = u.id
      WHERE u.id = $1
      LIMIT 1`,
    [userId, DEFAULT_ROLE, DEFAULT_AUTH_PROVIDER]
  );

  if (result.rows.length === 0) {
    throw new OnboardingError('User not found.', 404);
  }

  const row = result.rows[0];
  return {
    id: row.id,
    email: row.email,
    full_name: row.full_name,
    role: row.role,
    auth_provider: row.auth_provider,
    mobile_number: row.mobile_number,
    is_active: row.is_active,
    created_at: row.created_at,
    updated_at: row.updated_at,
    onboarding: row.business_profile_id
      ? {
          business_profile_id: row.business_profile_id,
          user_id: row.id,
          business_type: row.business_type,
          trading_name: row.trading_name,
          legal_name: row.legal_name,
          tax_country: row.tax_country,
          base_currency: row.base_currency,
          disclaimer_acknowledged: row.disclaimer_acknowledged,
          disclaimer_acknowledged_at: row.disclaimer_acknowledged_at,
          onboarding_completed_at: row.onboarding_completed_at,
          created_at: row.business_profile_created_at,
          updated_at: row.business_profile_updated_at,
          next_step: 'connect_bank',
          bank_connection_ready: row.disclaimer_acknowledged === true,
          inbox_ready_user_id: row.id,
        }
      : null,
  };
}

module.exports = {
  DEFAULT_ROLE,
  OnboardingError,
  SUPPORTED_BUSINESS_TYPE,
  assertSignupPayload,
  buildAuthToken,
  createSignup,
  getOnboardingProfile,
  normalizeEmail,
};
