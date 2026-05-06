const crypto = require('crypto');

const SCRYPT_PREFIX = 'scrypt';
const SALT_BYTES = 16;
const KEY_LENGTH = 64;

function hashPassword(password) {
  const salt = crypto.randomBytes(SALT_BYTES).toString('hex');
  const derivedKey = crypto.scryptSync(password, salt, KEY_LENGTH).toString('hex');
  return `${SCRYPT_PREFIX}$${salt}$${derivedKey}`;
}

function verifyPassword(password, storedHash) {
  if (!storedHash || typeof storedHash !== 'string') {
    return false;
  }

  const [prefix, salt, expectedKey] = storedHash.split('$');
  if (prefix !== SCRYPT_PREFIX || !salt || !expectedKey) {
    return false;
  }

  const actualKey = crypto.scryptSync(password, salt, KEY_LENGTH);
  const expectedBuffer = Buffer.from(expectedKey, 'hex');

  if (actualKey.length !== expectedBuffer.length) {
    return false;
  }

  return crypto.timingSafeEqual(actualKey, expectedBuffer);
}

function isSecurePasswordHash(storedHash) {
  return typeof storedHash === 'string' && storedHash.startsWith(`${SCRYPT_PREFIX}$`);
}

module.exports = {
  hashPassword,
  isSecurePasswordHash,
  verifyPassword,
};
