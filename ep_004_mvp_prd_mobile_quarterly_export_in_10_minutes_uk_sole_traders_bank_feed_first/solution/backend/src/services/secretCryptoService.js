const crypto = require("crypto");

const TOKEN_PREFIX = "enc.v1";
const IV_BYTES = 12;

function getTokenEncryptionKey(rawKey = process.env.BANK_TOKEN_ENCRYPTION_KEY) {
  if (!rawKey || String(rawKey).trim().length < 16) {
    throw new Error("bank_token_encryption_key_required");
  }

  return crypto.createHash("sha256").update(String(rawKey)).digest();
}

function encryptSecret(plaintext, rawKey) {
  if (plaintext == null) {
    return null;
  }

  const key = getTokenEncryptionKey(rawKey);
  const iv = crypto.randomBytes(IV_BYTES);
  const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
  const ciphertext = Buffer.concat([cipher.update(String(plaintext), "utf8"), cipher.final()]);
  const tag = cipher.getAuthTag();
  return [
    TOKEN_PREFIX,
    iv.toString("base64"),
    tag.toString("base64"),
    ciphertext.toString("base64")
  ].join(":");
}

function decryptSecret(ciphertext, rawKey) {
  if (ciphertext == null) {
    return null;
  }

  const value = String(ciphertext);
  if (!value.startsWith(`${TOKEN_PREFIX}:`)) {
    return value;
  }

  const [prefix, ivB64, tagB64, payloadB64] = value.split(":");
  if (prefix !== TOKEN_PREFIX) {
    throw new Error("encrypted_secret_malformed");
  }
  if (!ivB64 || !tagB64 || !payloadB64) {
    throw new Error("encrypted_secret_malformed");
  }

  const key = getTokenEncryptionKey(rawKey);
  const decipher = crypto.createDecipheriv("aes-256-gcm", key, Buffer.from(ivB64, "base64"));
  decipher.setAuthTag(Buffer.from(tagB64, "base64"));
  const plaintext = Buffer.concat([
    decipher.update(Buffer.from(payloadB64, "base64")),
    decipher.final()
  ]);
  return plaintext.toString("utf8");
}

module.exports = {
  TOKEN_PREFIX,
  decryptSecret,
  encryptSecret,
  getTokenEncryptionKey
};
