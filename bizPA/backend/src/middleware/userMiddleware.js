const { extractSessionToken, verifySessionToken } = require('../services/authSessionService');

const PUBLIC_PATHS = new Set([
  '/api/v1/auth/login',
  '/api/v1/auth/signup',
  '/api/v1/auth/logout',
  '/api/health',
]);

/**
 * JWT Verification Middleware.
 * Extracts and verifies token from 'Authorization' header.
 */
const userMiddleware = (req, res, next) => {
  // Allow public access to login
  if (PUBLIC_PATHS.has(req.path)) {
    return next();
  }

  const token = extractSessionToken(req);

  if (!token) {
    if (process.env.ALLOW_INSECURE_DEV_AUTH === 'true') {
      const userId = req.headers['x-user-id'] || '00000000-0000-0000-0000-000000000000';
      req.user = { id: userId, auth_mode: 'insecure_dev_header' };
      return next();
    }
    return res.status(401).json({ error: 'Authentication required' });
  }

  try {
    const decoded = verifySessionToken(token);
    req.user = decoded;
    return next();
  } catch (err) {
    console.warn('[Auth] Invalid token:', err.message);
    return res.status(403).json({ error: 'Invalid or expired session token' });
  }
};

module.exports = userMiddleware;
