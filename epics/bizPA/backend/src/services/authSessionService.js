const jwt = require('jsonwebtoken');

const SESSION_COOKIE_NAME = 'bizpa_session';
const DEV_JWT_SECRET = 'bizpa_voice_secret_2026';
const SESSION_MAX_AGE_MS = 7 * 24 * 60 * 60 * 1000;

function getJwtSecret() {
  if (process.env.JWT_SECRET) {
    return process.env.JWT_SECRET;
  }
  if (process.env.NODE_ENV === 'production') {
    throw new Error('JWT_SECRET must be configured in production.');
  }
  return DEV_JWT_SECRET;
}

function signSessionToken(claims) {
  return jwt.sign(claims, getJwtSecret(), { expiresIn: '7d' });
}

function verifySessionToken(token) {
  return jwt.verify(token, getJwtSecret());
}

function parseCookieHeader(headerValue) {
  const header = String(headerValue || '').trim();
  if (!header) {
    return {};
  }

  return header
    .split(';')
    .map((entry) => entry.trim())
    .filter(Boolean)
    .reduce((cookies, entry) => {
      const separatorIndex = entry.indexOf('=');
      if (separatorIndex <= 0) {
        return cookies;
      }
      const key = entry.slice(0, separatorIndex).trim();
      const value = entry.slice(separatorIndex + 1).trim();
      cookies[key] = decodeURIComponent(value);
      return cookies;
    }, {});
}

function extractSessionToken(req) {
  const authHeader = req?.headers?.authorization;
  if (authHeader && authHeader.startsWith('Bearer ')) {
    return authHeader.slice('Bearer '.length).trim();
  }

  const cookies = parseCookieHeader(req?.headers?.cookie);
  return cookies[SESSION_COOKIE_NAME] || '';
}

function isRequestSecure(req) {
  return Boolean(
    req?.secure
    || String(req?.headers?.['x-forwarded-proto'] || '').toLowerCase() === 'https'
  );
}

function buildSessionCookieOptions(req) {
  return {
    httpOnly: true,
    sameSite: 'lax',
    secure: process.env.NODE_ENV === 'production' || isRequestSecure(req),
    maxAge: SESSION_MAX_AGE_MS,
    path: '/',
  };
}

function attachSessionCookie(res, req, token) {
  res.cookie(SESSION_COOKIE_NAME, token, buildSessionCookieOptions(req));
}

function clearSessionCookie(res, req) {
  res.clearCookie(SESSION_COOKIE_NAME, buildSessionCookieOptions(req));
}

function parseAllowedOrigins() {
  const configured = String(process.env.CORS_ALLOWED_ORIGINS || '')
    .split(',')
    .map((entry) => entry.trim())
    .filter(Boolean);

  if (configured.length > 0) {
    return new Set(configured);
  }

  return new Set([
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:3001',
    'http://127.0.0.1:3001',
    'capacitor://localhost',
  ]);
}

function isAllowedOrigin(origin, allowedOrigins) {
  if (!origin) {
    return true;
  }
  return allowedOrigins.has(origin);
}

function sanitizeRequestPath(originalUrl) {
  return String(originalUrl || '/').split('?')[0];
}

module.exports = {
  SESSION_COOKIE_NAME,
  SESSION_MAX_AGE_MS,
  attachSessionCookie,
  buildSessionCookieOptions,
  clearSessionCookie,
  extractSessionToken,
  getJwtSecret,
  isAllowedOrigin,
  isRequestSecure,
  parseAllowedOrigins,
  parseCookieHeader,
  sanitizeRequestPath,
  signSessionToken,
  verifySessionToken,
};
