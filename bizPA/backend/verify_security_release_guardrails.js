const assert = require('assert');

const userMiddleware = require('./src/middleware/userMiddleware');
const {
  SESSION_COOKIE_NAME,
  extractSessionToken,
  parseAllowedOrigins,
  sanitizeRequestPath,
  signSessionToken,
} = require('./src/services/authSessionService');

function runMiddleware(req) {
  return new Promise((resolve) => {
    const response = {
      statusCode: 200,
      body: null,
      status(code) {
        this.statusCode = code;
        return this;
      },
      json(payload) {
        this.body = payload;
        resolve({ proceeded: false, statusCode: this.statusCode, body: payload, req });
      },
    };

    userMiddleware(req, response, () => {
      resolve({ proceeded: true, statusCode: response.statusCode, body: response.body, req });
    });
  });
}

async function main() {
  const originalInsecureAuth = process.env.ALLOW_INSECURE_DEV_AUTH;
  process.env.ALLOW_INSECURE_DEV_AUTH = 'false';

  const missingAuth = await runMiddleware({
    path: '/api/v1/inbox',
    headers: {},
  });
  assert.strictEqual(missingAuth.proceeded, false);
  assert.strictEqual(missingAuth.statusCode, 401);
  assert.strictEqual(missingAuth.body.error, 'Authentication required');

  const token = signSessionToken({
    id: 'user-1',
    email: 'owner@example.com',
    role: 'owner',
  });
  const cookieAuth = await runMiddleware({
    path: '/api/v1/inbox',
    headers: {
      cookie: `${SESSION_COOKIE_NAME}=${encodeURIComponent(token)}`,
    },
  });
  assert.strictEqual(cookieAuth.proceeded, true);
  assert.strictEqual(cookieAuth.req.user.id, 'user-1');

  const publicRoute = await runMiddleware({
    path: '/api/v1/auth/login',
    headers: {},
  });
  assert.strictEqual(publicRoute.proceeded, true);

  assert.strictEqual(
    extractSessionToken({
      headers: {
        cookie: `${SESSION_COOKIE_NAME}=${encodeURIComponent(token)}`,
      },
    }),
    token
  );

  const allowedOrigins = parseAllowedOrigins();
  assert(allowedOrigins.has('http://127.0.0.1:3001'));
  assert.strictEqual(sanitizeRequestPath('/api/v1/inbox?limit=50&token=secret'), '/api/v1/inbox');

  process.env.ALLOW_INSECURE_DEV_AUTH = originalInsecureAuth;

  console.log('verify_security_release_guardrails=PASS');
  console.log(JSON.stringify({
    cookie_name: SESSION_COOKIE_NAME,
    allowed_origin_count: allowedOrigins.size,
    auth_mode: 'http_only_cookie',
  }));
}

main().catch((error) => {
  console.error('verify_security_release_guardrails=FAIL');
  console.error(error);
  process.exit(1);
});
