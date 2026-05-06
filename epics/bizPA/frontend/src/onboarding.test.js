import {
  BUSINESS_TYPE_OPTIONS,
  MVP_SUPPORTED_BUSINESS_TYPE,
  buildSignupPayload,
  createAppUserFromSession,
  createDefaultOnboardingForm,
  mergeUserIntoList,
  normalizeOnboardingSession,
  validateOnboardingForm,
} from './onboarding';

describe('onboarding helpers', () => {
  test('default form starts in sole-trader mode', () => {
    const form = createDefaultOnboardingForm();

    expect(form.businessType).toBe(MVP_SUPPORTED_BUSINESS_TYPE);
    expect(form.disclaimerAcknowledged).toBe(false);
  });

  test('validation blocks unsupported business types and missing disclaimer', () => {
    const errors = validateOnboardingForm({
      fullName: 'Test User',
      email: 'test@example.com',
      password: 'StrongPass123!',
      tradingName: 'Test Trade',
      businessType: 'LIMITED_COMPANY',
      disclaimerAcknowledged: false,
    });

    expect(errors.businessType).toContain('sole trader');
    expect(errors.disclaimerAcknowledged).toContain('Disclaimer acknowledgement');
  });

  test('buildSignupPayload maps the frontend form to API fields', () => {
    const payload = buildSignupPayload({
      fullName: '  Maya Sole Trader ',
      email: '  Maya@Example.com ',
      password: 'StrongPass123!',
      mobileNumber: ' +447700900123 ',
      tradingName: ' Maya Repairs ',
      businessType: MVP_SUPPORTED_BUSINESS_TYPE,
      disclaimerAcknowledged: true,
    });

    expect(payload).toEqual({
      full_name: 'Maya Sole Trader',
      email: 'maya@example.com',
      password: 'StrongPass123!',
      mobile_number: '+447700900123',
      trading_name: 'Maya Repairs',
      business_type: MVP_SUPPORTED_BUSINESS_TYPE,
      disclaimer_acknowledged: true,
    });
  });

  test('normalize session and derive app user for downstream flows', () => {
    const session = normalizeOnboardingSession({
      token: 'jwt-token',
      user: {
        id: 'user-1',
        full_name: 'Maya Sole Trader',
        email: 'maya@example.com',
        role: 'owner',
      },
      onboarding: {
        business_profile_id: 'bp-1',
        bank_connection_ready: true,
      },
    });

    expect(session.token).toBe('');
    expect(session.onboarding.business_profile_id).toBe('bp-1');

    const appUser = createAppUserFromSession(session, 'tenant-bizpa-demo');
    expect(appUser).toEqual({
      id: 'user-1',
      name: 'Maya Sole Trader',
      email: 'maya@example.com',
      role: 'owner',
      tenant_id: 'tenant-bizpa-demo',
    });

    const merged = mergeUserIntoList([{ id: 'existing', name: 'Alice' }], appUser);
    expect(merged[0].id).toBe('user-1');
  });

  test('business type options clearly flag unsupported MVP choices', () => {
    const unsupported = BUSINESS_TYPE_OPTIONS.filter((option) => !option.supported);
    expect(unsupported.length).toBeGreaterThan(0);
    expect(unsupported.every((option) => option.description.includes('Blocked'))).toBe(true);
  });
});
