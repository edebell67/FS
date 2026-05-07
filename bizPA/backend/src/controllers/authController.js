const db = require('../config/db');
const {
  DEFAULT_ROLE,
  OnboardingError,
  buildAuthToken,
  createSignup,
  getOnboardingProfile,
  normalizeEmail,
} = require('../services/onboardingService');
const { isSecurePasswordHash, verifyPassword } = require('../services/passwordService');
const { attachSessionCookie, clearSessionCookie } = require('../services/authSessionService');

function sendAuthPayload(req, res, payload, statusCode = 200) {
  const token = payload?.token || '';
  if (token) {
    attachSessionCookie(res, req, token);
  }

  res.set('Cache-Control', 'no-store');
  return res.status(statusCode).json({
    success: true,
    user: payload?.user || null,
    onboarding: payload?.onboarding || null,
    session: {
      authenticated: Boolean(token),
      storage: 'http_only_cookie',
    },
  });
}

async function withTransaction(work) {
  const client = await db.pool.connect();
  try {
    await client.query('BEGIN');
    const result = await work(client);
    await client.query('COMMIT');
    return result;
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}

/**
 * Simple login for demo purposes.
 * Returns JWT for existing users.
 * POST /api/v1/auth/login
 */
const login = async (req, res) => {
  const email = normalizeEmail(req.body?.email);
  const password = String(req.body?.password || '');

  if (!email) {
    return res.status(400).json({ error: 'Email is required' });
  }

  try {
    const result = await db.query('SELECT * FROM users WHERE email = $1', [email]);
    
    if (result.rows.length === 0) {
      return res.status(401).json({ error: 'Invalid user or account deactivated' });
    }

    const user = result.rows[0];
    if (user.is_active === false) {
      return res.status(401).json({ error: 'Invalid user or account deactivated' });
    }

    if (isSecurePasswordHash(user.password_hash)) {
      if (!password) {
        return res.status(400).json({ error: 'Password is required for this account' });
      }
      if (!verifyPassword(password, user.password_hash)) {
        return res.status(401).json({ error: 'Invalid email or password' });
      }
    }
    
    const token = buildAuthToken(user);
    const profile = await getOnboardingProfile(db, user.id);

    return sendAuthPayload(req, res, {
      token,
      user: profile,
      onboarding: profile.onboarding || null,
    });
  } catch (err) {
    console.error('[AuthController] Login Error:', err);
    return res.status(500).json({ error: 'Login failed' });
  }
};

/**
 * Secure signup for MVP sole-trader onboarding.
 * POST /api/v1/auth/signup
 */
const signup = async (req, res) => {
  try {
    const payload = await withTransaction((client) => createSignup(client, req.body || {}));
    return sendAuthPayload(req, res, payload, 201);
  } catch (err) {
    if (err instanceof OnboardingError) {
      return res.status(err.statusCode).json({ error: err.message, details: err.details });
    }
    console.error('[AuthController] Signup Error:', err);
    return res.status(500).json({ error: 'Signup failed' });
  }
};

/**
 * Get current profile from token
 * GET /api/v1/auth/me
 */
const getMe = async (req, res) => {
  try {
    const profile = await getOnboardingProfile(db, req.user.id);
    if (!profile) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.set('Cache-Control', 'no-store');
    return res.json(profile);
  } catch (err) {
    if (err instanceof OnboardingError) {
      return res.status(err.statusCode).json({ error: err.message, details: err.details });
    }
    return res.status(500).json({ error: 'Failed to fetch profile' });
  }
};

const logout = async (req, res) => {
  clearSessionCookie(res, req);
  res.set('Cache-Control', 'no-store');
  return res.status(200).json({
    success: true,
    session: {
      authenticated: false,
      storage: 'http_only_cookie',
    },
  });
};

module.exports = {
  signup,
  login,
  getMe,
  logout,
};
