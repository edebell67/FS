import React, { useMemo, useState } from 'react';
import { AlertTriangle, CheckCircle2, ShieldCheck } from 'lucide-react';
import {
  BUSINESS_TYPE_OPTIONS,
  MVP_SUPPORTED_BUSINESS_TYPE,
  buildSignupPayload,
  createDefaultOnboardingForm,
  validateOnboardingForm,
} from './onboarding';

const LEGAL_DISCLAIMER = 'No HMRC submission. Not tax advice. You remain responsible for filings.';

function fieldStyle(hasError) {
  return {
    width: '100%',
    borderRadius: 12,
    border: `1px solid ${hasError ? '#cc444b' : '#d9d2c3'}`,
    padding: '12px 14px',
    background: '#fffdf8',
    color: '#182224',
  };
}

function helperStyle(isSupported, isSelected) {
  if (isSelected && !isSupported) {
    return { color: '#cc444b' };
  }
  if (isSupported) {
    return { color: '#2d8f5b' };
  }
  return { color: '#5f6b6d' };
}

export default function OnboardingGate({ busy, errorMessage, onSubmit }) {
  const [form, setForm] = useState(() => createDefaultOnboardingForm());
  const [validationErrors, setValidationErrors] = useState({});

  const selectedBusinessType = String(form.businessType || '').toUpperCase();
  const selectedOption = useMemo(
    () => BUSINESS_TYPE_OPTIONS.find((option) => option.value === selectedBusinessType) || BUSINESS_TYPE_OPTIONS[0],
    [selectedBusinessType]
  );

  const handleChange = (field, value) => {
    setForm((previous) => ({ ...previous, [field]: value }));
    setValidationErrors((previous) => {
      if (!previous[field]) {
        return previous;
      }
      const next = { ...previous };
      delete next[field];
      return next;
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const nextErrors = validateOnboardingForm(form);
    setValidationErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) {
      return;
    }
    await onSubmit(buildSignupPayload(form));
  };

  return (
    <div style={{ minHeight: '100vh', display: 'grid', placeItems: 'center', padding: 20 }}>
      <div style={{ width: '100%', maxWidth: 1040, display: 'grid', gap: 18, gridTemplateColumns: 'minmax(0, 1.1fr) minmax(320px, 0.9fr)' }}>
        <section style={{ background: 'linear-gradient(155deg, #14353a 0%, #0d5c63 60%, #8bcbb5 140%)', color: '#fff', borderRadius: 28, padding: 28, boxShadow: '0 20px 48px rgba(24,34,36,0.18)' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8, borderRadius: 999, padding: '7px 12px', background: 'rgba(255,255,255,0.16)', fontSize: 12, fontWeight: 700, letterSpacing: '0.04em', textTransform: 'uppercase' }}>
            <ShieldCheck size={16} />
            MVP onboarding
          </div>
          <h1 style={{ marginTop: 18, marginBottom: 10, fontSize: '2.4rem', lineHeight: 1.05 }}>Set up your sole-trader account before connecting a bank feed.</h1>
          <p style={{ margin: 0, color: 'rgba(255,255,255,0.84)', maxWidth: 560 }}>
            This flow creates a secure account, stores your business profile, and records the legal disclaimer acknowledgement required before bank connection.
          </p>
          <div style={{ display: 'grid', gap: 12, marginTop: 22 }}>
            <div style={{ borderRadius: 18, padding: 16, background: 'rgba(255,255,255,0.12)' }}>
              <strong>What this creates</strong>
              <div style={{ marginTop: 6, color: 'rgba(255,255,255,0.84)' }}>A user account, a `SOLE_TRADER` business profile, and the IDs needed for bank connection and inbox setup.</div>
            </div>
            <div style={{ borderRadius: 18, padding: 16, background: 'rgba(255,255,255,0.12)' }}>
              <strong>Business type scope</strong>
              <div style={{ marginTop: 6, color: 'rgba(255,255,255,0.84)' }}>Only sole trader is enabled in this MVP. Limited companies and partnerships are clearly blocked.</div>
            </div>
            <div style={{ borderRadius: 18, padding: 16, background: 'rgba(255,255,255,0.12)' }}>
              <strong>Disclaimer gate</strong>
              <div style={{ marginTop: 6, color: 'rgba(255,255,255,0.84)' }}>{LEGAL_DISCLAIMER}</div>
            </div>
          </div>
        </section>

        <section style={{ background: '#fffdf8', border: '1px solid #d9d2c3', borderRadius: 28, padding: 24, boxShadow: '0 20px 48px rgba(24,34,36,0.1)' }}>
          <h2 style={{ marginTop: 0, marginBottom: 6 }}>Create account</h2>
          <p style={{ marginTop: 0, color: '#5f6b6d' }}>The account is created only after the sole-trader profile and disclaimer are confirmed.</p>

          {errorMessage ? (
            <div style={{ display: 'flex', gap: 10, alignItems: 'flex-start', borderRadius: 14, padding: 12, marginBottom: 14, background: 'rgba(204,68,75,0.12)', color: '#8b272d' }}>
              <AlertTriangle size={18} style={{ marginTop: 2 }} />
              <div>{errorMessage}</div>
            </div>
          ) : null}

          <form onSubmit={handleSubmit}>
            <div style={{ display: 'grid', gap: 12 }}>
              <div>
                <label htmlFor="fullName" style={{ display: 'block', marginBottom: 6, fontWeight: 700 }}>Full name</label>
                <input id="fullName" value={form.fullName} onChange={(event) => handleChange('fullName', event.target.value)} style={fieldStyle(validationErrors.fullName)} />
                {validationErrors.fullName ? <div style={{ color: '#cc444b', marginTop: 6, fontSize: 13 }}>{validationErrors.fullName}</div> : null}
              </div>

              <div>
                <label htmlFor="email" style={{ display: 'block', marginBottom: 6, fontWeight: 700 }}>Email</label>
                <input id="email" type="email" value={form.email} onChange={(event) => handleChange('email', event.target.value)} style={fieldStyle(validationErrors.email)} />
                {validationErrors.email ? <div style={{ color: '#cc444b', marginTop: 6, fontSize: 13 }}>{validationErrors.email}</div> : null}
              </div>

              <div>
                <label htmlFor="password" style={{ display: 'block', marginBottom: 6, fontWeight: 700 }}>Password</label>
                <input id="password" type="password" value={form.password} onChange={(event) => handleChange('password', event.target.value)} style={fieldStyle(validationErrors.password)} />
                {validationErrors.password ? <div style={{ color: '#cc444b', marginTop: 6, fontSize: 13 }}>{validationErrors.password}</div> : null}
              </div>

              <div>
                <label htmlFor="mobileNumber" style={{ display: 'block', marginBottom: 6, fontWeight: 700 }}>Mobile number</label>
                <input id="mobileNumber" value={form.mobileNumber} onChange={(event) => handleChange('mobileNumber', event.target.value)} style={fieldStyle(false)} />
              </div>

              <div>
                <label htmlFor="tradingName" style={{ display: 'block', marginBottom: 6, fontWeight: 700 }}>Trading name</label>
                <input id="tradingName" value={form.tradingName} onChange={(event) => handleChange('tradingName', event.target.value)} style={fieldStyle(validationErrors.tradingName)} />
                {validationErrors.tradingName ? <div style={{ color: '#cc444b', marginTop: 6, fontSize: 13 }}>{validationErrors.tradingName}</div> : null}
              </div>

              <div>
                <div style={{ display: 'block', marginBottom: 8, fontWeight: 700 }}>Business type</div>
                <div style={{ display: 'grid', gap: 10 }}>
                  {BUSINESS_TYPE_OPTIONS.map((option) => {
                    const isSelected = selectedBusinessType === option.value;
                    return (
                      <button
                        key={option.value}
                        type="button"
                        onClick={() => handleChange('businessType', option.value)}
                        style={{
                          textAlign: 'left',
                          borderRadius: 16,
                          border: `1px solid ${isSelected ? (option.supported ? '#0d5c63' : '#cc444b') : '#d9d2c3'}`,
                          background: isSelected ? '#f3f7f6' : '#fffdf8',
                          padding: 14,
                          cursor: 'pointer',
                        }}
                      >
                        <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, alignItems: 'center' }}>
                          <strong>{option.label}</strong>
                          {option.supported ? <CheckCircle2 size={16} color="#2d8f5b" /> : <AlertTriangle size={16} color="#cc444b" />}
                        </div>
                        <div style={{ marginTop: 6, ...helperStyle(option.supported, isSelected) }}>{option.description}</div>
                      </button>
                    );
                  })}
                </div>
                {selectedOption.value !== MVP_SUPPORTED_BUSINESS_TYPE || validationErrors.businessType ? (
                  <div style={{ color: '#cc444b', marginTop: 8, fontSize: 13 }}>{validationErrors.businessType || 'Only sole trader is supported in the MVP.'}</div>
                ) : null}
              </div>

              <label style={{ display: 'flex', gap: 10, alignItems: 'flex-start', borderRadius: 14, border: `1px solid ${validationErrors.disclaimerAcknowledged ? '#cc444b' : '#d9d2c3'}`, padding: 14, background: '#fff7d6' }}>
                <input
                  type="checkbox"
                  checked={form.disclaimerAcknowledged}
                  onChange={(event) => handleChange('disclaimerAcknowledged', event.target.checked)}
                  style={{ marginTop: 3 }}
                />
                <span>
                  <strong>Acknowledge disclaimer</strong>
                  <div style={{ marginTop: 4, color: '#7c5f12' }}>{LEGAL_DISCLAIMER}</div>
                </span>
              </label>
              {validationErrors.disclaimerAcknowledged ? <div style={{ color: '#cc444b', marginTop: -4, fontSize: 13 }}>{validationErrors.disclaimerAcknowledged}</div> : null}
            </div>

            <button
              type="submit"
              disabled={busy}
              style={{
                marginTop: 18,
                width: '100%',
                borderRadius: 999,
                border: 'none',
                padding: '14px 18px',
                background: '#0d5c63',
                color: '#fff',
                fontWeight: 700,
                cursor: busy ? 'progress' : 'pointer',
                opacity: busy ? 0.7 : 1,
              }}
            >
              {busy ? 'Creating account...' : 'Create sole-trader account'}
            </button>
          </form>
        </section>
      </div>
    </div>
  );
}
