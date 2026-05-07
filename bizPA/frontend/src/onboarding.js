export const MVP_SUPPORTED_BUSINESS_TYPE = 'SOLE_TRADER';
export const ONBOARDING_SESSION_KEY = 'mvpOnboardingSession';

export const BUSINESS_TYPE_OPTIONS = [
  {
    value: MVP_SUPPORTED_BUSINESS_TYPE,
    label: 'Sole trader',
    supported: true,
    description: 'Supported in the MVP bank-feed-first flow.',
  },
  {
    value: 'LIMITED_COMPANY',
    label: 'Limited company',
    supported: false,
    description: 'Blocked in this MVP release.',
  },
  {
    value: 'PARTNERSHIP',
    label: 'Partnership',
    supported: false,
    description: 'Blocked in this MVP release.',
  },
];

export function createDefaultOnboardingForm() {
  return {
    fullName: '',
    email: '',
    password: '',
    mobileNumber: '',
    tradingName: '',
    businessType: MVP_SUPPORTED_BUSINESS_TYPE,
    disclaimerAcknowledged: false,
  };
}

export function validateOnboardingForm(form) {
  const errors = {};

  if (!String(form.fullName || '').trim()) {
    errors.fullName = 'Full name is required.';
  }
  if (!String(form.email || '').trim() || !String(form.email).includes('@')) {
    errors.email = 'Enter a valid email address.';
  }
  if (String(form.password || '').length < 8) {
    errors.password = 'Password must be at least 8 characters.';
  }
  if (!String(form.tradingName || '').trim()) {
    errors.tradingName = 'Trading name is required.';
  }
  if (String(form.businessType || '').toUpperCase() !== MVP_SUPPORTED_BUSINESS_TYPE) {
    errors.businessType = 'Only sole trader is supported in the MVP.';
  }
  if (form.disclaimerAcknowledged !== true) {
    errors.disclaimerAcknowledged = 'Disclaimer acknowledgement is required before bank connection.';
  }

  return errors;
}

export function buildSignupPayload(form) {
  return {
    full_name: String(form.fullName || '').trim(),
    email: String(form.email || '').trim().toLowerCase(),
    password: String(form.password || ''),
    mobile_number: String(form.mobileNumber || '').trim(),
    trading_name: String(form.tradingName || '').trim(),
    business_type: String(form.businessType || '').toUpperCase(),
    disclaimer_acknowledged: form.disclaimerAcknowledged === true,
  };
}

export function normalizeOnboardingSession(payload) {
  return {
    token: '',
    user: payload?.user || null,
    onboarding: payload?.onboarding || null,
  };
}

export function createAppUserFromSession(session, tenantId) {
  const user = session?.user;
  return {
    id: user?.id,
    name: user?.full_name || user?.email || 'New user',
    email: user?.email || '',
    role: user?.role || 'owner',
    tenant_id: tenantId,
  };
}

export function mergeUserIntoList(users, appUser) {
  if (!appUser?.id) {
    return users;
  }
  const existing = users.find((user) => user.id === appUser.id);
  if (existing) {
    return users.map((user) => (user.id === appUser.id ? { ...user, ...appUser } : user));
  }
  return [appUser, ...users];
}
